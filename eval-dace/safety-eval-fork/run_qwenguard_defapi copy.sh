#!/bin/bash

# 配置
# MODEL_PATH="/mnt/shared-storage-user/wenxiaoyu/models/Qwen2.5-7B-Instruct"
MODEL_NAME="defender_api"
TASKS="harmbench"
# STEP="240"
CLASSIFIER="Qwen3GuardAPI"  # 新增：指定分类器
RESULTS_DIR="/mnt/shared-storage-user/wenxiaoyu/game-private/eval/safety-eval-fork/results/v2-12.2/$MODEL_NAME-class-$CLASSIFIER-$(date +%Y%m%d_%H%M%S)"
mkdir -p $RESULTS_DIR

# 环境变量 - Defender API配置
export DEFENDER_API_BASE_URL="http://s-20251222100447-d4zb8-decode.ailab-safethm.svc:23202/v1"
export DEFENDER_API_KEY="FAKE_API_KEY"
export DEFENDER_API_MODEL="orm"

# 环境变量 - 使用WildGuard API端点 (Qwen3GuardAPI)
export WILDGUARD_API_ENDPOINT='http://s-20251119153749-lp69w-decode.ailab-safethm.svc:23344/v1'
export WILDGUARD_API_KEY='FAKE_API_KEY'

export HF_DATASETS_CACHE=/data/hf_cache
export OPENAI_API_KEY="fake-key-for-safety-eval"
export HF_TOKEN="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"
export HF_HUB_OFFLINE=0
export HF_DATASETS_VERBOSITY=info

# 激活环境
eval "$(conda shell.bash hook)"
conda activate safety-eval

# 运行评测 - 使用Defender API生成 + WildGuardAPI评估
# 注意：使用 --use_defender_api 替代 --use_vllm
timeout 3600 python -u evaluation/eval.py generators \
    --model_name_or_path "$MODEL_NAME" \
    --model_input_template_path_or_name "hf" \
    --tasks $TASKS \
    --report_output_path "$RESULTS_DIR/metrics.json" \
    --save_individual_results_path "$RESULTS_DIR/all_results.json" \
    --use_defender_api \
    --classifier_model_name "$CLASSIFIER" \
    --batch_size 1 2>&1 | tee "$RESULTS_DIR/eval.log"

echo "✓ 评测完成: $RESULTS_DIR"
echo "  Classifier: $CLASSIFIER"
echo "  Defender API: $DEFENDER_API_BASE_URL"
