#!/bin/bash


# ============================================================================

# 单个Attacker对单个Defender评测脚本

# ============================================================================

# 用于测试固定的attacker和defender模型的表现

# ============================================================================


# 配置

ATTACKER_MODEL_PATH="/mnt/shared-storage-user/wenxiaoyu/game-private/src/360-LLaMA-Factory/saves/qwen2.5-7B-Base-cot_w_harm_gemini/full/sft/checkpoint-8800"

DEFENDER_MODEL_PATH="/mnt/shared-storage-user/wenxiaoyu/models/Qwen2.5-7B-Instruct"

BASE_RESULTS_DIR="/mnt/shared-storage-user/wenxiaoyu/game-private/eval/safety-eval-fork/results/v2-12.12-eval-12.14/single-attacker-defender-$(date +%Y%m%d_%H%M%S)"


# 环境变量

export WILDGUARD_API_ENDPOINT='http://s-20251119153749-lp69w-decode.ailab-safethm.svc:23344/v1'

export WILDGUARD_API_KEY='FAKE_API_KEY'

export HF_DATASETS_CACHE=/data/hf_cache

export OPENAI_API_KEY="fake-key-for-safety-eval"

export HF_TOKEN="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"


# 激活环境

eval "$(conda shell.bash hook)"

conda activate safety-eval


echo "🚀 单个Attacker vs Defender 测试..."

echo "Attacker model: $ATTACKER_MODEL_PATH"

echo "Defender model: $DEFENDER_MODEL_PATH"

echo "结果目录: $BASE_RESULTS_DIR"

mkdir -p $BASE_RESULTS_DIR

# 检查attacker模型是否存在

if [ ! -d "$ATTACKER_MODEL_PATH" ]; then

    echo "❌ 错误: Attacker模型不存在: $ATTACKER_MODEL_PATH"

    exit 1

fi

# 检查defender模型是否存在

if [ ! -d "$DEFENDER_MODEL_PATH" ]; then

    echo "❌ 错误: Defender模型不存在: $DEFENDER_MODEL_PATH"

    exit 1

fi


echo ""

echo "========================================"

echo "开始测试"

echo "========================================"

echo "📂 Attacker: $ATTACKER_MODEL_PATH"

echo "📂 Defender: $DEFENDER_MODEL_PATH"

echo "📂 结果: $BASE_RESULTS_DIR"

echo ""

# 运行评测
timeout 7200 python -u evaluation/eval.py generators \
    "$DEFENDER_MODEL_PATH" \
    "harmbench:attacker_defender" \
    "hf" \
    "$BASE_RESULTS_DIR/metrics.json" \
    --save_individual_results_path "$BASE_RESULTS_DIR/all_results.json" \
    --use_vllm \
    --classifier_model_name "Qwen3GuardAPI" \
    --attacker_model_path "$ATTACKER_MODEL_PATH" \
    --attacker_template "hf" \
    --batch_size 1 2>&1 | tee "$BASE_RESULTS_DIR/eval.log"

if [ $? -eq 0 ]; then

    echo "✅ 测试完成"

else

    echo "❌ 测试失败或超时"

    exit 1

fi


echo ""

echo "========================================"

echo "🎉 测试完成！"

echo "========================================"

echo "结果目录: $BASE_RESULTS_DIR"

echo "查看结果: cat $BASE_RESULTS_DIR/metrics.json"