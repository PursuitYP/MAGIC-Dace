#!/bin/bash

# ==============================================================================
# MAJIC Evaluation Launcher  (Table 3 · Defender generalization)
# Use this script to configure parameters in advance and run MAJIC evaluation.
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. API Configuration  (mirrors eval-dace/OpenRT/run_eval.sh)
# ------------------------------------------------------------------------------

# Target Model Configuration (Defender)
# Used as the target model for attacks
#export DEFENDER_API_BASE_URL="https://api.boyuerichdata.opensphereai.com/v1"
#export DEFENDER_API_KEY="sk-43Usgp7ge22R5UjYVpJOca1OGvTOsOK3PQfhnYiqLN3JuHvR"
#export DEFENDER_API_MODEL="gemini-2.5-flash"

# rl defender from merged defender checkpoint path
# export DEFENDER_API_BASE_URL="http://s-20260120150339-pccms-decode.ailab-safethm.svc:22320/v1"
export DEFENDER_API_BASE_URL="http://s-20260429151904-5j4n7-decode.ailab-safethm.svc:28658/v1"
export DEFENDER_API_KEY="FAKE_API_KEY"
export DEFENDER_API_MODEL="orm"

# base attacker from initial qwen/llama path
# export ATTACKER_API_BASE_URL="http://s-20251216145244-8xhw4-decode.ailab-safethm.svc:23300/v1"
export ATTACKER_API_BASE_URL="http://s-20260429151806-6gxrd-decode.ailab-safethm.svc:28648/v1"
export ATTACKER_API_KEY="FAKE_API_KEY"
export ATTACKER_API_MODEL="orm"
ATTACKER_ANSWER_EXTRACT="true"

# Judge/Attacker Configuration (OpenAI/Compatible)
# Used for judging results
# export OPENAI_API_KEY="sk-xI8zGRXkgJzoejUP7KtcBbRfqNazmWnFqSNuw6zMn5rZClFy"
export OPENAI_API_KEY="sk-ua4rD1WerZKpDyb7JHOSKxVvMmvMZIKi6rXGPotdX9nfxNXr"
# export OPENAI_BASE_URL="https://api.boyuerichdata.opensphereai.com/v1"
export OPENAI_BASE_URL="http://35.220.164.252:3888/v1/"

# ------------------------------------------------------------------------------
# 2. Model Assignments
# ------------------------------------------------------------------------------

# The target model to be attacked (Defender)
TARGET_MODEL="$DEFENDER_API_MODEL"

# The attacker model used to generate adversarial prompts
ATTACKER_MODEL="$ATTACKER_API_MODEL"

# The judge model used to evaluate success
JUDGE_MODEL="gpt-4o"

# Run-name shown in the output directory
MODEL_NAME="DACE-Qwen2.5-7B-full-step300"

# ------------------------------------------------------------------------------
# 3. MAJIC Hyper-parameters
# ------------------------------------------------------------------------------
# Markov init mode (Table 4 variants):
#   uniform        -- MAJIC(-Init)      (default, ASR 70.3% on GPT-4o in paper)
#   learned        -- Full MAJIC        (requires MAJIC_INIT_MATRIX; ASR 95.7%)
#   learned_static -- MAJIC(-DynUpd)    (requires MAJIC_INIT_MATRIX; ASR 76.5%)
MAJIC_INIT_MODE="uniform"
MAJIC_INIT_MATRIX="markov_methods/init_matrix.npy"

# Outer chain count (Nmax) and per-chain optimization steps. From upstream
# markov_attack_api_dynamic.py: chain_count=10, chain_length=3.
MAJIC_CHAIN_COUNT=10
MAJIC_CHAIN_LENGTH=3

# ------------------------------------------------------------------------------
# 4. Test Prompts / Dataset
# ------------------------------------------------------------------------------
# Use HarmBench dataset (matches OpenRT/run_eval.sh).  Switch to
# data/harmbench400.json for the upstream MAJIC repo split if desired.
DATASET_PATH="/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/seed/harmbench/harmbench_behaviors_text_test.csv"
NUM_SAMPLES=""        # empty -> all
NUM_SAMPLES=5

# ------------------------------------------------------------------------------
# 5. Output Configuration
# ------------------------------------------------------------------------------
# Directory to save results (JSON history, summaries, logs)
RESULTS_DIR="/mnt/shared-storage-user/yupeng/MAGIC/eval-dace/MAJIC/results/dace/$MODEL_NAME-$(date +%Y%m%d_%H%M%S)"

# ------------------------------------------------------------------------------
# Execution (Do not modify below unless necessary)
# ==============================================================================

echo "----------------------------------------------------------------"
echo "Starting MAJIC Evaluation"
echo "Target Model (API): $TARGET_MODEL"
echo "Target Base URL:    $DEFENDER_API_BASE_URL"
echo "Attacker Model:     $ATTACKER_MODEL"
echo "Judge Model:        $JUDGE_MODEL"
echo "Init Mode:          $MAJIC_INIT_MODE"
echo "Init Matrix:        $MAJIC_INIT_MATRIX"
echo "Chain Count/Length: $MAJIC_CHAIN_COUNT / $MAJIC_CHAIN_LENGTH"
echo "Dataset:            $DATASET_PATH"
echo "Num Samples:        $NUM_SAMPLES"
echo "Results Dir:        $RESULTS_DIR"
echo "----------------------------------------------------------------"

# Ensure we are in the script's directory
cd "$(dirname "$0")"

CMD="python3 -m majic_eval.runner \
    --target-api-key \"$DEFENDER_API_KEY\" \
    --target-base-url \"$DEFENDER_API_BASE_URL\" \
    --target-model \"$TARGET_MODEL\" \
    --attacker-api-key \"$ATTACKER_API_KEY\" \
    --attacker-base-url \"$ATTACKER_API_BASE_URL\" \
    --attacker-model \"$ATTACKER_MODEL\" \
    --judge-api-key \"$OPENAI_API_KEY\" \
    --judge-base-url \"$OPENAI_BASE_URL\" \
    --judge-model \"$JUDGE_MODEL\" \
    --dataset-path \"$DATASET_PATH\" \
    --init-mode \"$MAJIC_INIT_MODE\" \
    --init-matrix-path \"$MAJIC_INIT_MATRIX\" \
    --chain-count \"$MAJIC_CHAIN_COUNT\" \
    --chain-length \"$MAJIC_CHAIN_LENGTH\" \
    --results-dir \"$RESULTS_DIR\""

if [ -n "$NUM_SAMPLES" ]; then
    CMD="$CMD --num-samples \"$NUM_SAMPLES\""
fi
if [ "$ATTACKER_ANSWER_EXTRACT" = "true" ]; then
    CMD="$CMD --attacker-answer-extract"
fi

eval $CMD

echo "----------------------------------------------------------------"
echo "MAJIC Evaluation Finished"
