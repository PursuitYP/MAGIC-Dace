#!/bin/bash

# API Evaluation Script for OLMES Benchmarks
# This script runs API-based evaluation for all 7 general capability benchmarks

# Environment setup
export HF_DATASETS_CACHE=/data/hf_cache
export HF_TOKEN="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"
#export HF_DATASETS_OFFLINE=1
#export HF_HUB_OFFLINE=1
export HF_DATASETS_VERBOSITY=info
export TIKTOKEN_CACHE_DIR=/data/tiktoken_cache

# API Configuration
API_KEY="FAKE_API_KEY"
BASE_URL="http://s-20260128194228-qfmqp-decode.ailab-safethm.svc:23320/v1"
MODEL="orm"

# Output directory
OUTPUT_DIR="./results/ablation/nocot-s150-q257b-it/if-eval-qwen-defonly-$(date +%Y%m%d_%H%M%S)"

#OUTPUT_DIR="./results/eval-1.20/0120-s255-l318/if-eval-qwen-defonly-$(date +%Y%m%d_%H%M%S)"

# Python script path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="${SCRIPT_DIR}/api_eval.py"

# Activate conda environment
source /home/wenxiaoyu/miniconda3/etc/profile.d/conda.sh
conda activate olmes

echo "==================================================="
echo "API Evaluation for OLMES Benchmarks"
echo "==================================================="
echo "API Base URL: ${BASE_URL}"
echo "Model: ${MODEL}"
echo "Output Directory: ${OUTPUT_DIR}"
echo "==================================================="

# Task to run (can be overridden by command line argument)
#"ifeval", "arc_challenge", "gpqa", "truthfulqa", "mmlu", "gsm8k", "bbh", "all"
TASK=${1:-"ifeval"}
LIMIT=${2:-""}

# Build command
CMD="python ${PYTHON_SCRIPT} \
    --task ${TASK} \
    --api-key ${API_KEY} \
    --base-url ${BASE_URL} \
    --model ${MODEL} \
    --output-dir ${OUTPUT_DIR}"

if [ -n "$LIMIT" ]; then
    CMD="${CMD} --limit ${LIMIT}"
fi

echo "Running command:"
echo "${CMD}"
echo "==================================================="

# Run evaluation
eval ${CMD}

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "==================================================="
    echo "Evaluation completed successfully!"
    echo "Results saved to: ${OUTPUT_DIR}"
    echo "==================================================="
else
    echo ""
    echo "==================================================="
    echo "Evaluation failed with exit code: ${EXIT_CODE}"
    echo "==================================================="
fi

exit $EXIT_CODE