#!/bin/bash

# ==============================================================================
# OpenRT Evaluation Launcher (SmoothLLM Defense Mode)
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. API Configuration
# ------------------------------------------------------------------------------

# Target Model (Qwen 2.5) wrapped by SmoothLLM
# The actual API endpoint for Qwen
export DEFENDER_API_BASE_URL="http://s-20260115114238-6mplv-decode.ailab-safethm.svc:22310/v1"
export DEFENDER_API_KEY="FAKE_API_KEY"
# We use a special name to trigger the SmoothLLM wrapper in unified_eval.py
export DEFENDER_API_MODEL="orm"

# Attacker Model (Your existing Attacker API)
export ATTACKER_API_BASE_URL="http://s-20251216145244-8xhw4-decode.ailab-safethm.svc:23300/v1"
export ATTACKER_API_KEY="FAKE_API_KEY"
export ATTACKER_API_MODEL="orm"

# Judge Model (OpenAI/Compatible)
export OPENAI_API_KEY="sk-xI8zGRXkgJzoejUP7KtcBbRfqNazmWnFqSNuw6zMn5rZClFy"
export OPENAI_BASE_URL="https://api.boyuerichdata.opensphereai.com/v1"

# ------------------------------------------------------------------------------
# 2. Evaluation Settings
# ------------------------------------------------------------------------------

TARGET_MODEL="smoothllm-${DEFENDER_API_MODEL}"
ATTACKER_MODEL="$ATTACKER_API_MODEL"
JUDGE_MODEL="gpt-4o"

# Embedding model for AutoDAN-Turbo-R (requires OpenAI API or compatible)
EMBEDDING_MODEL="text-embedding-3-small"

# [GCG Only] Local path to the model weights (HuggingFace format)
LOCAL_MODEL_PATH="/mnt/shared-storage-user/wenxiaoyu/models/Meta-Llama-3.1-8B-Instruct"

# Attacks to run (e.g., pair, tree, autodan_turbo)
ATTACKS="gcg"

# Dataset
DATASET_PATH="/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/seed/harmbench/harmbench_behaviors_text_test.csv"
MAX_TURNS=3
JUDGE_THRESHOLD=5
RESULTS_DIR="./results/smoothllm-llama3.1-8b-it-defense"

# ------------------------------------------------------------------------------
# 3. Execution
# ------------------------------------------------------------------------------

echo "----------------------------------------------------------------"
echo "Starting OpenRT Evaluation with SmoothLLM Defense"
echo "Target: $TARGET_MODEL (Wraps Qwen API with SmoothLLM)"
echo "Attacks: $ATTACKS"
echo "----------------------------------------------------------------"

cd "$(dirname "$0")"

python3 unified_eval.py \
    --target-api-key "$DEFENDER_API_KEY" \
    --target-base-url "$DEFENDER_API_BASE_URL" \
    --attacker-api-key "$ATTACKER_API_KEY" \
    --attacker-base-url "$ATTACKER_API_BASE_URL" \
    --judge-api-key "$OPENAI_API_KEY" \
    --judge-base-url "$OPENAI_BASE_URL" \
    --target-model "$TARGET_MODEL" \
    --attacker-model "$ATTACKER_MODEL" \
    --embedding-model "$EMBEDDING_MODEL" \
    --judge-model "$JUDGE_MODEL" \
    --local-model-path "$LOCAL_MODEL_PATH" \
    --attacks $ATTACKS \
    --dataset-path "$DATASET_PATH" \
    --max-turns "$MAX_TURNS" \
    --judge-threshold "$JUDGE_THRESHOLD" \
    --results-dir "$RESULTS_DIR"

echo "Done."
