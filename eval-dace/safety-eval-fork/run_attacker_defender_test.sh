#!/bin/bash

# ============================================================================
# 批量测试脚本 - 多个Attacker对多个Defender交叉评测
# ============================================================================
# 用于测试所有attacker和defender checkpoint的组合
# ============================================================================

# 配置
BASE_CHECKPOINT_DIR="/mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/wenxiaoyu/game"
EXPERIMENT_NAME="v5-D-q257bi-A-sft_wocode-ratio11-freq15-reward1_0.5_0-woDformat-wo_label_reward-revised_label-2026-01-17_09-37-46"
# v3-D-q257bi-A-sftv4-balanced-reward1_0.5_0.5-woDformat-ratio21-freq10-add_label_reward-revised_label-2026-01-04_14-57-52"
#ATTACKER_STEPS=(30 45 60 90 105 120 150 165 180 210 225 240 270 285 300)
#DEFENDER_STEPS=(15 75 135 195 255)
ATTACKER_STEPS=(30 60 90)
DEFENDER_STEPS=(15 45 75)

BASE_RESULTS_DIR="/mnt/shared-storage-user/wenxiaoyu/game-private/eval/safety-eval-fork/results/eval-1.18/heatmap-cross-eval-$(date +%Y%m%d_%H%M%S)"

# 环境变量
export WILDGUARD_API_ENDPOINT='http://s-20251119153749-lp69w-decode.ailab-safethm.svc:23344/v1'
export WILDGUARD_API_KEY='FAKE_API_KEY'
export HF_DATASETS_CACHE=/data/hf_cache
export OPENAI_API_KEY="fake-key-for-safety-eval"
export HF_TOKEN="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"

# 激活环境
eval "$(conda shell.bash hook)"
conda activate safety-eval

echo "🚀 交叉评测 Attackers vs Defenders..."
echo "Attacker steps: ${ATTACKER_STEPS[@]}"
echo "Defender steps: ${DEFENDER_STEPS[@]}"
echo "总结果目录: $BASE_RESULTS_DIR"
mkdir -p $BASE_RESULTS_DIR

# 统计变量
TOTAL_TESTS=$((${#ATTACKER_STEPS[@]} * ${#DEFENDER_STEPS[@]}))
CURRENT_TEST=0
SUCCESS_COUNT=0
FAILED_COUNT=0
SKIPPED_COUNT=0

# 嵌套循环：对每个attacker测试所有defender
for ATTACKER_STEP in "${ATTACKER_STEPS[@]}"; do
    ATTACKER_MODEL_PATH="${BASE_CHECKPOINT_DIR}/checkpoints/Game-separated/${EXPERIMENT_NAME}/global_step_${ATTACKER_STEP}/attacker/actor/huggingface"
    
    # 检查attacker模型是否存在
    if [ ! -d "$ATTACKER_MODEL_PATH" ]; then
        echo ""
        echo "⚠️  警告: Attacker模型不存在: $ATTACKER_MODEL_PATH"
        echo "跳过Attacker step${ATTACKER_STEP}的所有测试..."
        SKIPPED_COUNT=$((SKIPPED_COUNT + ${#DEFENDER_STEPS[@]}))
        continue
    fi
    
    for DEFENDER_STEP in "${DEFENDER_STEPS[@]}"; do
        CURRENT_TEST=$((CURRENT_TEST + 1))
        
        echo ""
        echo "========================================"
        echo "测试 [$CURRENT_TEST/$TOTAL_TESTS]"
        echo "Attacker Step: $ATTACKER_STEP"
        echo "Defender Step: $DEFENDER_STEP"
        echo "========================================"
        
        DEFENDER_MODEL_PATH="${BASE_CHECKPOINT_DIR}/checkpoints/Game-separated/${EXPERIMENT_NAME}/global_step_${DEFENDER_STEP}/defender/actor/huggingface"
        RESULTS_DIR="${BASE_RESULTS_DIR}/A${ATTACKER_STEP}_vs_D${DEFENDER_STEP}"
        mkdir -p $RESULTS_DIR
        
        # 检查defender模型是否存在
        if [ ! -d "$DEFENDER_MODEL_PATH" ]; then
            echo "⚠️  警告: Defender模型不存在: $DEFENDER_MODEL_PATH"
            echo "跳过此组合..."
            SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
            continue
        fi
        
        echo "📂 Attacker: $ATTACKER_MODEL_PATH"
        echo "📂 Defender: $DEFENDER_MODEL_PATH"
        echo "📂 结果: $RESULTS_DIR"
        echo "⏰ 开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
        
        # 运行评测
        timeout 3600 python -u evaluation/eval.py generators \
            --model_name_or_path "$DEFENDER_MODEL_PATH" \
            --model_input_template_path_or_name "game_defender" \
            --tasks "harmbench:attacker_defender" \
            --report_output_path "$RESULTS_DIR/metrics.json" \
            --save_individual_results_path "$RESULTS_DIR/all_results.json" \
            --use_vllm \
            --classifier_model_name "Qwen3GuardAPI" \
            --attacker_model_path "$ATTACKER_MODEL_PATH" \
            --attacker_template "hf" \
            --batch_size 1 2>&1 | tee "$RESULTS_DIR/eval.log"
        
        EXIT_CODE=$?
        echo "⏰ 结束时间: $(date '+%Y-%m-%d %H:%M:%S')"
        
        if [ $EXIT_CODE -eq 0 ]; then
            echo "✅ A${ATTACKER_STEP} vs D${DEFENDER_STEP} 完成"
            SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        else
            echo "❌ A${ATTACKER_STEP} vs D${DEFENDER_STEP} 失败或超时 (退出码: $EXIT_CODE)"
            FAILED_COUNT=$((FAILED_COUNT + 1))
        fi
    done
done

echo ""
echo "========================================"
echo "🎉 所有测试完成！"
echo "========================================"
echo "📊 测试统计:"
echo "  总测试数: $TOTAL_TESTS"
echo "  成功: $SUCCESS_COUNT"
echo "  失败: $FAILED_COUNT"
echo "  跳过: $SKIPPED_COUNT"
echo ""
echo "📁 结果汇总目录: $BASE_RESULTS_DIR"
echo ""
echo "📋 生成结果矩阵..."

# 生成结果矩阵CSV
SUMMARY_CSV="${BASE_RESULTS_DIR}/results_matrix.csv"
echo -n "Attacker\\Defender" > $SUMMARY_CSV
for DEFENDER_STEP in "${DEFENDER_STEPS[@]}"; do
    echo -n ",D${DEFENDER_STEP}" >> $SUMMARY_CSV
done
echo "" >> $SUMMARY_CSV

for ATTACKER_STEP in "${ATTACKER_STEPS[@]}"; do
    echo -n "A${ATTACKER_STEP}" >> $SUMMARY_CSV
    for DEFENDER_STEP in "${DEFENDER_STEPS[@]}"; do
        METRICS_FILE="${BASE_RESULTS_DIR}/A${ATTACKER_STEP}_vs_D${DEFENDER_STEP}/metrics.json"
        if [ -f "$METRICS_FILE" ]; then
            # 提取ASR值（假设metrics.json中有asr字段）
            ASR=$(grep -oP '"asr":\s*\K[0-9.]+' "$METRICS_FILE" 2>/dev/null || echo "N/A")
            echo -n ",${ASR}" >> $SUMMARY_CSV
        else
            echo -n ",SKIP" >> $SUMMARY_CSV
        fi
    done
    echo "" >> $SUMMARY_CSV
done

echo "✅ 结果矩阵已保存: $SUMMARY_CSV"
echo ""
echo "查看各组合结果:"
echo "  cat $SUMMARY_CSV"