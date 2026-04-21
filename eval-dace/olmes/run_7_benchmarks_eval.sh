#!/bin/bash

# 7个通用能力基准评测脚本 (IFEval, ARC-C, GPQA, TruthfulQA, MMLU, GSM8K, BBH)
# 使用OLMES框架统一评测

# 配置/mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/wenxiaoyu/game/checkpoints/Game-separated/v3-D-q257bi-A-sftv4-balanced-reward1_0.5_0.5-woDformat-ratio21-freq10-add_label_reward-revised_label-2026-01-04_14-57-52/global_step_285/defender/actor/huggingface"
#/mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/wenxiaoyu/game/checkpoints/Game-separated/v3-D-q257bi-A-sftv4-balanced-8192-reward1_0.5_0.5-woDformat-ratio11-freq15-add_label_reward-revised_label-2026-01-04_14-57-50/global_step_285/defender/actor/huggingface"
#MODEL_PATH="/mnt/shared-storage-gpfs2/gpfs2-shared-public/huggingface/hub/models--Qwen--Qwen2.5-14B-Instruct/snapshots/cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8"
MODEL_PATH="/mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/wenxiaoyu/game/checkpoints/Game-separated/v5-D-q257bi-A-q257bisft_wocode-reward1_0.5_0-wDformat-wo_label_reward-revised_label-2026-01-25_07-32-02/global_step_150/defender/actor/huggingface"

MODEL_NAME=nocot-s210-q257b-it
RESULTS_BASE_DIR="/mnt/shared-storage-user/wenxiaoyu/game-private/eval/olmes/results/ablation/$MODEL_NAME/7benchmarks-$(date +%Y%m%d_%H%M%S)"
mkdir -p $RESULTS_BASE_DIR

# 环境变量
export HF_DATASETS_CACHE=/data/hf_cache
export HF_TOKEN="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"
#export HF_DATASETS_OFFLINE=1
#export HF_HUB_OFFLINE=1
export HF_DATASETS_VERBOSITY=info

# 激活环境
eval "$(conda shell.bash hook)"
conda activate olmes

echo "========================================"
echo "7个通用能力基准评测"
echo "模型: $MODEL_PATH"
echo "结果目录: $RESULTS_BASE_DIR"
echo "========================================"

# Debug: Check if model path exists and is accessible
echo "DEBUG: Checking model path..."
if [ -d "$MODEL_PATH" ]; then
    echo "DEBUG: Model path exists."
    ls -ld "$MODEL_PATH"
else
    echo "DEBUG: Model path DOES NOT EXIST or is not a directory."
    echo "DEBUG: Checking parent directories..."
    parent_dir=$(dirname "$MODEL_PATH")
    if [ -d "$parent_dir" ]; then
         echo "DEBUG: Parent exists: $parent_dir"
         ls -ld "$parent_dir"
         echo "DEBUG: Contents of parent:"
         ls -F "$parent_dir" | head -n 20
    else
         echo "DEBUG: Parent DOES NOT EXIST: $parent_dir"
         # Go up one more
         grandparent=$(dirname "$parent_dir")
         if [ -d "$grandparent" ]; then
             echo "DEBUG: Grandparent exists: $grandparent"
             ls -F "$grandparent" | head -n 20
         else
             echo "DEBUG: Grandparent DOES NOT EXIST: $grandparent"
         fi
    fi
fi

# 定义所有任务
TASKS=(
  "ifeval"
#  "arc_challenge"
#   "gpqa"
#   "truthfulqa"
#   "mmlu"
#   "gsm8k"
#   "bbh"
)

# 逐个任务运行
for TASK in "${TASKS[@]}"; do
    echo ""
    echo "-----------------------------------------------------------------------"
    echo "开始评测: $TASK"
    echo "-----------------------------------------------------------------------"
    
    TASK_RESULTS_DIR="$RESULTS_BASE_DIR/$TASK"
    mkdir -p $TASK_RESULTS_DIR
    
    # 根据任务类型设置特定参数
    case $TASK in
        "ifeval")
            TASK_ARGS="--task ifeval --model-type hf --batch-size 16"
            ;;
        "arc_challenge")
            TASK_ARGS="--task arc_challenge --model-type hf --batch-size 16"
            ;;
        "gpqa")
            TASK_ARGS="--task gpqa --model-type hf --batch-size 4"
            ;;
        "truthfulqa")
            TASK_ARGS="--task truthfulqa --model-type hf --batch-size 16"
            ;;
        "mmlu")
            TASK_ARGS="--task mmlu --model-type hf --batch-size 16 --num-shots 5"
            ;;
        "gsm8k")
            TASK_ARGS="--task gsm8k --model-type hf --batch-size 16 --num-shots 8"
            ;;
        "bbh")
            TASK_ARGS="--task bbh --model-type hf --batch-size 16 --num-shots 3"
            ;;
        *)
            echo "未知任务: $TASK"
            continue
            ;;
    esac
    
    # 运行评测
    timeout 7200 python -m oe_eval.run_eval \
        --model-path "$MODEL_PATH" \
        $TASK_ARGS \
        --output-dir "$TASK_RESULTS_DIR" \
        2>&1 | tee "$TASK_RESULTS_DIR/eval.log"
    
    # 检查结果
    if [ ${PIPESTATUS[0]} -eq 0 ] && [ -f "$TASK_RESULTS_DIR/metrics.json" ]; then
        echo "✓ $TASK 评测完成"
        echo "  结果: $TASK_RESULTS_DIR/metrics.json"
    else
        echo "❌ $TASK 评测失败"
    fi
done

echo ""
echo "========================================"
echo "所有评测完成"
echo "========================================"
echo "结果汇总目录: $RESULTS_BASE_DIR"
echo ""
echo "各任务结果:"
for TASK in "${TASKS[@]}"; do
    METRICS_FILE="$RESULTS_BASE_DIR/$TASK/metrics.json"
    if [ -f "$METRICS_FILE" ]; then
        echo "  ✓ $TASK: $METRICS_FILE"
    else
        echo "  ✗ $TASK: 无结果"
    fi
done
echo ""
