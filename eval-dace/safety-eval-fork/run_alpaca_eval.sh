#!/bin/bash

# AlpacaEval Evaluation Script with Defender API + GPT-4o
# 使用部署的Defender API生成回答，然后用GPT-4o进行AlpacaEval评分

# ==============================================================================
# 配置部分
# ==============================================================================

# Defender API（生成回答）
# export DEFENDER_API_BASE_URL="http://s-20260304150204-6bjfm-decode.ailab-safethm.svc:22103/v1"
export DEFENDER_API_BASE_URL="http://s-20260429151904-5j4n7-decode.ailab-safethm.svc:28658/v1"
export DEFENDER_API_KEY="FAKE_API_KEY"
export DEFENDER_API_MODEL="orm"

# GPT-4o API（用于AlpacaEval内部评分）
#export OPENAI_API_KEY="sk-xI8zGRXkgJzoejUP7KtcBbRfqNazmWnFqSNuw6zMn5rZClFy"
# export OPENAI_API_KEY="sk-D0wGaXJBOV1f6VTnJzwRuhLewJ0Crn1KNQeSXnRRn2dM6ITR"
export OPENAI_API_KEY="sk-ua4rD1WerZKpDyb7JHOSKxVvMmvMZIKi6rXGPotdX9nfxNXr"
# export OPENAI_BASE_URL="https://api.boyuerichdata.opensphereai.com/v1"
export OPENAI_BASE_URL="http://35.220.164.252:3888/v1/"
export OPENAI_MODEL="gpt-4o"
### dace: use the self-contained annotator config under eval-dace so we don't depend on hezhida/wenxiaoyu's home paths ###
export ALPACA_EVAL_ANNOTATORS_CONFIG="${ALPACA_EVAL_ANNOTATORS_CONFIG:-/mnt/shared-storage-user/yupeng/MAGIC/eval-dace/safety-eval-fork/evaluation/tasks/generation/alpacaeval/weighted_alpaca_eval_gpt4o}"
export ALPACA_EVAL_EXTRA_RETRIES=3
export ALPACA_EVAL_RETRY_SLEEP_SECONDS=5
export ALPACA_EVAL_SKIP_CONTENT_FILTER=1


# 任务与结果配置
#MODEL_NAME="def-direct_harm_pair_large_step39" # 对应 DefenderAPIModel
# MODEL_NAME="q257i"
MODEL_NAME="DACE-Qwen2.5-7B-full-step300"
TASKS="alpacaeval"
# RESULTS_DIR="./results/multi-turn-defense/$MODEL_NAME-alpaca/alpacaeval/-$(date +%Y%m%d_%H%M%S)"
RESULTS_DIR="/mnt/shared-storage-user/yupeng/MAGIC/eval-dace/safety-eval-fork/results/dace/$TASKS-$MODEL_NAME-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULTS_DIR"

# Hugging Face 相关（这里主要是保持环境一致，虽然后面用不到 HF datasets）
export HF_DATASETS_CACHE=/data/hf_cache
### dace: point hf_hub_download (used by alpaca_eval for df_gamed.csv) at the same shared cache as HF_DATASETS_CACHE ###
export HF_HUB_CACHE=/data/hf_cache/hub
export HF_TOKEN="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"
### dace: force HF hub offline so alpaca_eval's length_controlled_winrate reads pre-staged df_gamed.csv from HF_HUB_CACHE instead of timing out on huggingface.co ###
export HF_HUB_OFFLINE=1
export HF_DATASETS_VERBOSITY=info

# ==============================================================================
# 环境激活
# ==============================================================================
eval "$(conda shell.bash hook)"
conda activate safety-eval

# ==============================================================================
# 打印配置信息
# ==============================================================================
echo "=========================================================="
echo "AlpacaEval Evaluation: Defender API + GPT-4o"
echo "=========================================================="
echo ""
echo "【Defender API配置】（生成回答）"
echo "  Base URL: $DEFENDER_API_BASE_URL"
echo "  Model: $DEFENDER_API_MODEL"
echo "  API Key: ${DEFENDER_API_KEY:0:10}..."
echo ""
echo "【GPT-4 API配置】（评分）"
echo "  Base URL: $OPENAI_BASE_URL"
echo "  Model: $OPENAI_MODEL"
echo "  Annotator Config: $ALPACA_EVAL_ANNOTATORS_CONFIG"
echo "  API Key: ${OPENAI_API_KEY:0:10}..."
echo ""
echo "【评测配置】"
echo "  Tasks: $TASKS"
echo "  Results: $RESULTS_DIR"
echo ""
echo "=========================================================="
echo ""

# ==============================================================================
# 运行评测（Defender API 生成 + AlpacaEval GPT-4o 评测）
# ==============================================================================
timeout 72000 python -u evaluation/eval.py generators \
    --model_name_or_path "$MODEL_NAME" \
    --model_input_template_path_or_name "hf" \
    --tasks "$TASKS" \
    --report_output_path "$RESULTS_DIR/metrics.json" \
    --save_individual_results_path "$RESULTS_DIR/all_results.json" \
    --use_defender_api \
    --batch_size 1 2>&1 | tee "$RESULTS_DIR/eval.log"

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "=========================================================="
    echo "✓ AlpacaEval 评测完成！"
    echo "=========================================================="
    echo ""
    echo "结果文件："
    echo "  - 指标摘要: $RESULTS_DIR/metrics.json"
    echo "  - 详细结果: $RESULTS_DIR/all_results.json"
    echo "  - 运行日志: $RESULTS_DIR/eval.log"
    echo "=========================================================="
else
    echo "=========================================================="
    echo "✗ AlpacaEval 评测失败，退出码: $EXIT_CODE"
    echo "=========================================================="
    echo ""
    echo "请查看日志："
    echo "  cat $RESULTS_DIR/eval.log"
    echo ""
fi

exit $EXIT_CODE
