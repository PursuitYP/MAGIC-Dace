#!/bin/bash


# ============================================================================

# 批量测试脚本 - 固定Attacker对多个Defender评测

# ============================================================================

# 用于测试固定attacker在不同defender checkpoint上的表现

# ============================================================================


# 配置

BASE_CHECKPOINT_DIR="/mnt/shared-storage-user/wenxiaoyu/game-private"

EXPERIMENT_NAME="v4-D-q257bi-A-q257bi-ratio11-freq15-reward1_0.5_0-woDformat-wo_label_reward-revised_label-2026-01-13_14-25-54"

DEFENDER_STEPS=(15 45 75 105)

ATTACKER_MODEL_PATH="/mnt/shared-storage-user/wenxiaoyu/game-private/src/360-LLaMA-Factory/saves/qwen2.5-7B-Base-cot_w_harm_gemini/full/sft/checkpoint-8800"

BASE_RESULTS_DIR="/mnt/shared-storage-user/wenxiaoyu/game-private/eval/safety-eval-fork/results/eval-1.14/fixed-attacker-vs-defenders-$(date +%Y%m%d_%H%M%S)"


# 环境变量

export WILDGUARD_API_ENDPOINT='http://s-20251119153749-lp69w-decode.ailab-safethm.svc:23344/v1'

export WILDGUARD_API_KEY='FAKE_API_KEY'

export HF_DATASETS_CACHE=/data/hf_cache

export OPENAI_API_KEY="fake-key-for-safety-eval"

export HF_TOKEN="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"


# 激活环境

eval "$(conda shell.bash hook)"

conda activate safety-eval


echo "🚀 批量测试 Fixed Attacker vs Multiple Defenders..."

echo "Defender steps: ${DEFENDER_STEPS[@]}"

echo "Attacker model: $ATTACKER_MODEL_PATH"

echo "总结果目录: $BASE_RESULTS_DIR"

mkdir -p $BASE_RESULTS_DIR

# 检查attacker模型是否存在

if [ ! -d "$ATTACKER_MODEL_PATH" ]; then

    echo "❌ 错误: Attacker模型不存在: $ATTACKER_MODEL_PATH"

    exit 1

fi

# 循环测试每个defender

for DEFENDER_STEP in "${DEFENDER_STEPS[@]}"; do

    echo ""

    echo "========================================"

    echo "测试 Defender Step: $DEFENDER_STEP"

    echo "========================================"

    

    DEFENDER_MODEL_PATH="${BASE_CHECKPOINT_DIR}/checkpoints/Game-separated/${EXPERIMENT_NAME}/global_step_${DEFENDER_STEP}/defender/actor/huggingface"

    RESULTS_DIR="${BASE_RESULTS_DIR}/defender_step${DEFENDER_STEP}"

    mkdir -p $RESULTS_DIR

    

    # 检查defender模型是否存在

    if [ ! -d "$DEFENDER_MODEL_PATH" ]; then

        echo "⚠️  警告: Defender模型不存在: $DEFENDER_MODEL_PATH"

        echo "跳过此step..."

        continue

    fi

    

    echo "📂 Attacker: $ATTACKER_MODEL_PATH"

    echo "📂 Defender: $DEFENDER_MODEL_PATH"

    echo "📂 结果: $RESULTS_DIR"

    

    # 运行评测
    timeout 7200 python -u evaluation/eval.py generators \
        "$DEFENDER_MODEL_PATH" \
        "harmbench:attacker_defender" \
        "game_defender" \
        "$RESULTS_DIR/metrics.json" \
        --save_individual_results_path "$RESULTS_DIR/all_results.json" \
        --use_vllm \
        --classifier_model_name "Qwen3GuardAPI" \
        --attacker_model_path "$ATTACKER_MODEL_PATH" \
        --attacker_template "hf" \
        --batch_size 1 2>&1 | tee "$RESULTS_DIR/eval.log"

    

    if [ $? -eq 0 ]; then

        echo "✅ Defender step${DEFENDER_STEP} 完成"

    else

        echo "❌ Defender step${DEFENDER_STEP} 失败或超时"

    fi

done


echo ""

echo "========================================"

echo "🎉 所有测试完成！"

echo "========================================"

echo "结果汇总目录: $BASE_RESULTS_DIR"

echo ""

echo "查看各step结果:"

for DEFENDER_STEP in "${DEFENDER_STEPS[@]}"; do

    METRICS_FILE="${BASE_RESULTS_DIR}/defender_step${DEFENDER_STEP}/metrics.json"

    if [ -f "$METRICS_FILE" ]; then

        echo "  - Defender Step ${DEFENDER_STEP}: cat $METRICS_FILE"

    fi

done