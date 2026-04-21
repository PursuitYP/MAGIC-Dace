#!/bin/bash

# ============================================================================
# API-based Attacker-Defender Evaluation Script
# ============================================================================
# This script runs evaluation using API-deployed attacker and defender models
# instead of loading models locally with vLLM
# ============================================================================

# Environment variables
export WILDGUARD_API_ENDPOINT='http://s-20251119153749-lp69w-decode.ailab-safethm.svc:23344/v1'
export WILDGUARD_API_KEY='FAKE_API_KEY'
export HF_DATASETS_CACHE=/data/hf_cache
export OPENAI_API_KEY="fake-key-for-safety-eval"
export HF_TOKEN="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"

# Results directory
RESULTS_DIR="/mnt/shared-storage-user/wenxiaoyu/game-private/eval/safety-eval-fork/results/api-eval-$(date +%Y%m%d_%H%M%S)"
mkdir -p $RESULTS_DIR

# Activate environment
eval "$(conda shell.bash hook)"
conda activate safety-eval

echo "🚀 Starting API-based Attacker-Defender Evaluation..."
echo "📂 Results: $RESULTS_DIR"
echo ""

# Run the standalone Python script
python evaluation/run_api_eval.py 2>&1 | tee "$RESULTS_DIR/eval.log"

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "✅ Evaluation completed successfully!"
    echo "========================================"
    echo "📊 Metrics: $RESULTS_DIR/metrics.json"
    echo "📄 Results: $RESULTS_DIR/all_results.json"
    echo "📝 Log: $RESULTS_DIR/eval.log"
else
    echo ""
    echo "========================================"
    echo "❌ Evaluation failed"
    echo "========================================"
    echo "📝 Check log: $RESULTS_DIR/eval.log"
fi
