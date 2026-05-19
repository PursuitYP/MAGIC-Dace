#!/bin/bash

# StrongREJECT Evaluation Script with Defender API + GPT-4 Autograder
# 使用部署的Defender API生成回答，然后用GPT-4o评分

# ==============================================================================
# 配置部分
# ==============================================================================

# Defender API配置（用于生成回答）
# export DEFENDER_API_BASE_URL="http://s-20260330132942-vvph7-decode.ailab-safethm.svc:23302/v1"
export DEFENDER_API_BASE_URL="http://s-20260429151904-5j4n7-decode.ailab-safethm.svc:28658/v1"
export DEFENDER_API_KEY="FAKE_API_KEY"
export DEFENDER_API_MODEL="orm"


# GPT-4o API配置（用于评分）有点问题，为什么连不上了
#export OPENAI_API_KEY="sk-xI8zGRXkgJzoejUP7KtcBbRfqNazmWnFqSNuw6zMn5rZClFy"
# export OPENAI_API_KEY="sk-D0wGaXJBOV1f6VTnJzwRuhLewJ0Crn1KNQeSXnRRn2dM6ITR"
# export OPENAI_BASE_URL="https://api.boyuerichdata.opensphereai.com/v1"
export OPENAI_API_KEY="sk-ua4rD1WerZKpDyb7JHOSKxVvMmvMZIKi6rXGPotdX9nfxNXr"
export OPENAI_BASE_URL="http://35.220.164.252:3888/v1/"
export OPENAI_MODEL="gpt-4o"

# 任务和结果配置
# MODEL_NAME="CoT-s165"  # 使用defender_api标识
# MODEL_NAME="DACE-Qwen2.5-7B-full-step300"
MODEL_NAME="DACE-Qwen2.5-7B-v4-attacker1st-step300"

TASKS="strongreject"  # 使用完整数据集（313个样本），如需测试可用"strongreject:small"（60个样本）
# RESULTS_DIR="./results/rebuttal/$MODEL_NAME/$TASKS/-$(date +%Y%m%d_%H%M%S)"
RESULTS_DIR="/mnt/shared-storage-user/yupeng/MAGIC/eval-dace/safety-eval-fork/results/dace/$TASKS-$MODEL_NAME-$(date +%Y%m%d_%H%M%S)"
mkdir -p $RESULTS_DIR

# Hugging Face配置
export HF_DATASETS_CACHE=/data/hf_cache
export HF_TOKEN="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"
export HF_HUB_OFFLINE=0
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
echo "StrongREJECT Evaluation: Defender API + GPT-4 Autograder"
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
echo "  API Key: ${OPENAI_API_KEY:0:10}..."
echo ""
echo "【评测配置】"
echo "  Tasks: $TASKS"
echo "  Results: $RESULTS_DIR"
echo ""
echo "=========================================================="
echo ""

# ==============================================================================
# 运行评测
# ==============================================================================
# 使用defender_api模式 + GPT-4 autograder
# 注意：不使用--use_vllm，而是使用--use_defender_api
timeout 7200 python -u evaluation/eval.py generators \
    --model_name_or_path "$MODEL_NAME" \
    --model_input_template_path_or_name "hf" \
    --tasks "$TASKS" \
    --report_output_path "$RESULTS_DIR/metrics.json" \
    --save_individual_results_path "$RESULTS_DIR/all_results.json" \
    --use_defender_api \
    --use_gpt4_autograder \
    --batch_size 1 2>&1 | tee "$RESULTS_DIR/eval.log"

EXIT_CODE=$?

# ==============================================================================
# 结果总结
# ==============================================================================
echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "=========================================================="
    echo "✓ 评测完成！"
    echo "=========================================================="
    echo ""
    echo "结果文件："
    echo "  - 指标摘要: $RESULTS_DIR/metrics.json"
    echo "  - 详细结果: $RESULTS_DIR/all_results.json"
    echo "  - 运行日志: $RESULTS_DIR/eval.log"
    echo ""
    echo "查看指标："
    echo "  cat $RESULTS_DIR/metrics.json | jq ."
    echo ""
    echo "关键指标："
    if [ -f "$RESULTS_DIR/metrics.json" ]; then
        echo "  ASR (Attack Success Rate): $(cat $RESULTS_DIR/metrics.json | jq -r '.strongreject[\"ASR (Attack Success Rate)\"]' 2>/dev/null || echo 'N/A')"
        echo "  RTA (Robustness to Attacks): $(cat $RESULTS_DIR/metrics.json | jq -r '.strongreject[\"RTA (Robustness to Attacks)\"]' 2>/dev/null || echo 'N/A')"
    fi
    echo "=========================================================="
else
    echo "=========================================================="
    echo "✗ 评测失败，退出码: $EXIT_CODE"
    echo "=========================================================="
    echo ""
    echo "请查看日志："
    echo "  cat $RESULTS_DIR/eval.log"
    echo ""
    echo "常见问题："
    echo "  1. Defender API连接失败 -> 检查DEFENDER_API_BASE_URL是否可访问"
    echo "  2. GPT-4 API连接失败 -> 检查OPENAI_API_KEY是否有效"
    echo "  3. 环境问题 -> 确认safety-eval环境已正确安装"
    echo "=========================================================="
fi

exit $EXIT_CODE
