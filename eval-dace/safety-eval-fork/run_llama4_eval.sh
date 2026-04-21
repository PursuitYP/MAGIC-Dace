#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 配置
MODEL_PATH="/mnt/shared-storage-user/wenxiaoyu/models/Self-RedTeam-Qwen2.5-7B-Instruct"
MODEL_NAME="self-redteam-q257i"
TASKS="wildguardtest,harmbench_precompute,wildjailbreak:benign,wildjailbreak:harmful,do_anything_now,harmbench,or_bench:hard-1k,or_bench:toxic,xstest"
CLASSIFIER="LlamaGuard4API"
RESULTS_DIR="/mnt/shared-storage-user/wenxiaoyu/game-private/eval/safety-eval-fork/results/rebuttal/$MODEL_NAME/$CLASSIFIER/-2048-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULTS_DIR"

# 环境变量
export LLAMAGUARD_API_ENDPOINT='http://s-20260326183818-h2297-decode.ailab-safethm.svc:22312/v1'
export LLAMAGUARD_API_KEY='FAKE_API_KEY'
export LLAMAGUARD_API_MODEL='orm'
export HF_DATASETS_CACHE=/data/hf_cache
export OPENAI_API_KEY="fake-key-for-safety-eval"
export HF_TOKEN="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"
export HF_HUB_OFFLINE=0
export HF_DATASETS_VERBOSITY=info
export VLLM_WORKER_MULTIPROC_METHOD=spawn

# 激活环境
 eval "$(conda shell.bash hook)"
 conda activate safety-eval

CUDA_VISIBLE_DEVICES=0,1 python -u evaluation/eval.py generators     --model_name_or_path "$MODEL_PATH"     --model_input_template_path_or_name "game_defender"     --tasks "$TASKS"     --report_output_path "$RESULTS_DIR/metrics.json"     --save_individual_results_path "$RESULTS_DIR/all_results.json"     --use_vllm     --classifier_model_name "$CLASSIFIER"     --no_extract_answer false     --batch_size 1 2>&1 | tee "$RESULTS_DIR/eval.log"

echo "✓ 评测完成: $RESULTS_DIR"
