#!/bin/bash
# 批量合并分布式保存的模型分片脚本

set -o pipefail

# ============ 配置部分 ============
BASE_CHECKPOINT_DIR="/mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/wenxiaoyu/game/checkpoints/Game-separated"
EXPERIMENT_NAME="D-q257bi-A-q257bi-2026-03-29_14-00-52"

# 合并配置：当前 model_merger.py 仅支持 --local_dir / --hf_upload_path。
# 这里保留档位信息仅用于日志展示，不再向 Python 合并脚本传递不支持的参数。
MERGE_PROFILE="7b"

case "$MERGE_PROFILE" in
    7b|14b)
        ;;
    *)
        echo "错误: MERGE_PROFILE 必须是 7b 或 14b"
        exit 1
        ;;
esac

# 要合并的global_step数组
STEPS=(165 195)

# 模型合并脚本路径
MERGER_SCRIPT="/mnt/shared-storage-user/wenxiaoyu/game-private/src/verl/scripts/model_merger.py"

# 日志文件
LOG_FILE="model_merge_$(date +%Y%m%d_%H%M%S).log"

# ============ 配置部分结束 ============

echo "========================================" | tee -a "$LOG_FILE"
echo "模型分片合并脚本启动" | tee -a "$LOG_FILE"
echo "时间: $(date)" | tee -a "$LOG_FILE"
echo "实验目录: $EXPERIMENT_NAME" | tee -a "$LOG_FILE"
echo "要合并的steps: ${STEPS[@]}" | tee -a "$LOG_FILE"
echo "合并档位: $MERGE_PROFILE (当前 model_merger.py 不支持额外 merge 参数)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

if [ ! -f "$MERGER_SCRIPT" ]; then
    echo "错误: 合并脚本不存在: $MERGER_SCRIPT" | tee -a "$LOG_FILE"
    exit 1
fi

if [ ! -d "$BASE_CHECKPOINT_DIR/$EXPERIMENT_NAME" ]; then
    echo "错误: 实验目录不存在: $BASE_CHECKPOINT_DIR/$EXPERIMENT_NAME" | tee -a "$LOG_FILE"
    exit 1
fi

TOTAL_STEPS=${#STEPS[@]}
SUCCESS_COUNT=0
FAILED_COUNT=0

ensure_hf_dir_writable() {
    local hf_dir="$1"

    if [ ! -d "$hf_dir" ]; then
        return 0
    fi

    echo "  检测到已存在的huggingface目录，检查权限..." | tee -a "$LOG_FILE"
    if [ -w "$hf_dir" ]; then
        return 0
    fi

    echo "  尝试修改权限..." | tee -a "$LOG_FILE"
    if chmod -R u+w "$hf_dir" 2>/dev/null; then
        return 0
    fi

    echo "  权限修改失败，尝试删除并重建..." | tee -a "$LOG_FILE"
    if rm -rf "$hf_dir"; then
        return 0
    fi

    echo "  ✗ 无法删除huggingface目录，请手动执行: sudo rm -rf $hf_dir" | tee -a "$LOG_FILE"
    return 1
}

merge_one_target() {
    local role="$1"
    local actor_dir="$2"
    local hf_dir="$actor_dir/huggingface"

    if [ ! -d "$actor_dir" ]; then
        echo "  警告: $role 目录不存在: $actor_dir" | tee -a "$LOG_FILE"
        return 1
    fi

    echo "  合并 $role..." | tee -a "$LOG_FILE"

    if ! ensure_hf_dir_writable "$hf_dir"; then
        return 1
    fi

    if python3 "$MERGER_SCRIPT" --local_dir "$actor_dir" >> "$LOG_FILE" 2>&1; then
        echo "  ✓ $role 合并成功" | tee -a "$LOG_FILE"
        return 0
    else
        echo "  ✗ $role 合并失败" | tee -a "$LOG_FILE"
        return 1
    fi
}

merge_model() {
    local step="$1"
    local experiment_dir="$BASE_CHECKPOINT_DIR/$EXPERIMENT_NAME"
    local step_dir="$experiment_dir/global_step_$step"
    local step_failed=0
    local found_target=0

    if [ ! -d "$step_dir" ]; then
        echo "警告: step目录不存在: $step_dir" | tee -a "$LOG_FILE"
        return 1
    fi

    echo "---" | tee -a "$LOG_FILE"
    echo "开始合并 global_step_$step" | tee -a "$LOG_FILE"
    echo "时间: $(date)" | tee -a "$LOG_FILE"

    local attacker_dir="$step_dir/attacker/actor"
    if [ -d "$attacker_dir" ]; then
        found_target=1
        merge_one_target "attacker" "$attacker_dir" || step_failed=1
    else
        echo "  警告: attacker目录不存在: $attacker_dir" | tee -a "$LOG_FILE"
    fi

    local defender_dir="$step_dir/defender/actor"
    if [ -d "$defender_dir" ]; then
        found_target=1
        merge_one_target "defender" "$defender_dir" || step_failed=1
    else
        echo "  警告: defender目录不存在: $defender_dir" | tee -a "$LOG_FILE"
    fi

    if [ "$found_target" -eq 0 ]; then
        return 1
    fi

    if [ "$step_failed" -eq 0 ]; then
        return 0
    else
        return 1
    fi
}

for step in "${STEPS[@]}"; do
    if merge_model "$step"; then
        ((SUCCESS_COUNT++))
    else
        ((FAILED_COUNT++))
    fi
done

echo "" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "合并完成统计" | tee -a "$LOG_FILE"
echo "总steps数: $TOTAL_STEPS" | tee -a "$LOG_FILE"
echo "成功: $SUCCESS_COUNT" | tee -a "$LOG_FILE"
echo "失败: $FAILED_COUNT" | tee -a "$LOG_FILE"
echo "完成时间: $(date)" | tee -a "$LOG_FILE"
echo "日志文件: $LOG_FILE" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

if [ $FAILED_COUNT -gt 0 ]; then
    exit 1
else
    exit 0
fi
