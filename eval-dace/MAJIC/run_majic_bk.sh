#!/bin/bash

# ==============================================================================
# MAJIC Evaluation Launcher  (Table 3 · Defender generalization)
# Usage: bash run_majic.sh
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. API Configuration  (mirrors eval-dace/OpenRT/run_eval.sh)
# ------------------------------------------------------------------------------

# DACE defender (victim) endpoint
export DEFENDER_API_BASE_URL="${DEFENDER_API_BASE_URL:-http://s-20260429151904-5j4n7-decode.ailab-safethm.svc:28658/v1}"
export DEFENDER_API_KEY="${DEFENDER_API_KEY:-FAKE_API_KEY}"
export DEFENDER_API_MODEL="${DEFENDER_API_MODEL:-orm}"

# Base attacker endpoint (Qwen / Llama / Mistral -- whatever we self-deploy).
export ATTACKER_API_BASE_URL="${ATTACKER_API_BASE_URL:-http://s-20260429151806-6gxrd-decode.ailab-safethm.svc:28648/v1}"
export ATTACKER_API_KEY="${ATTACKER_API_KEY:-FAKE_API_KEY}"
export ATTACKER_API_MODEL="${ATTACKER_API_MODEL:-orm}"
ATTACKER_ANSWER_EXTRACT="${ATTACKER_ANSWER_EXTRACT:-true}"

# GPT-4o judge (OpenAI-compatible).
export OPENAI_API_KEY="${OPENAI_API_KEY:-sk-ua4rD1WerZKpDyb7JHOSKxVvMmvMZIKi6rXGPotdX9nfxNXr}"
export OPENAI_BASE_URL="${OPENAI_BASE_URL:-http://35.220.164.252:3888/v1/}"
JUDGE_MODEL="${JUDGE_MODEL:-gpt-4o}"

# Convenience aliases used in result paths.
TARGET_MODEL="${TARGET_MODEL:-$DEFENDER_API_MODEL}"
ATTACKER_MODEL="${ATTACKER_MODEL:-$ATTACKER_API_MODEL}"
MODEL_NAME="${MODEL_NAME:-DACE-Qwen2.5-7B-full-step300}"

# ------------------------------------------------------------------------------
# 2. Dataset Selection
# ------------------------------------------------------------------------------
# MAJIC supports both the HarmBench CSV used by run_eval.sh and the MAJIC-repo
# harmbench400.json. Pick one via DATASET_PATH; CSV defaults to HarmBench.
DATASET_PATH="${DATASET_PATH:-/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/seed/harmbench/harmbench_behaviors_text_test.csv}"
DATASET_COLUMN="${DATASET_COLUMN:-Behavior}"
DATASET_JSONL_FIELD="${DATASET_JSONL_FIELD:-vanilla}"
NUM_SAMPLES="${NUM_SAMPLES:-}"     # empty -> all
START_INDEX="${START_INDEX:-0}"

# ------------------------------------------------------------------------------
# 3. MAJIC Hyper-parameters
# ------------------------------------------------------------------------------
# Markov init mode (Table 4 variants):
#   uniform        -- MAJIC(-Init)      (default, ASR 70.3% on GPT-4o in paper)
#   learned        -- Full MAJIC        (requires MAJIC_INIT_MATRIX; ASR 95.7%)
#   learned_static -- MAJIC(-DynUpd)    (requires MAJIC_INIT_MATRIX; ASR 76.5%)
MAJIC_INIT_MODE="${MAJIC_INIT_MODE:-uniform}"
MAJIC_INIT_MATRIX="${MAJIC_INIT_MATRIX:-markov_methods/init_matrix.npy}"

MAJIC_CHAIN_COUNT="${MAJIC_CHAIN_COUNT:-10}"
MAJIC_CHAIN_LENGTH="${MAJIC_CHAIN_LENGTH:-3}"
MAJIC_INIT_QNUM="${MAJIC_INIT_QNUM:-1}"
MAJIC_CHAIN_QNUM="${MAJIC_CHAIN_QNUM:-1}"
MAJIC_ALPHA="${MAJIC_ALPHA:-0.1}"
MAJIC_GAMMA="${MAJIC_GAMMA:-0.5}"
MAJIC_BETA="${MAJIC_BETA:-0.01}"
MAJIC_SOFTMAX_T="${MAJIC_SOFTMAX_T:-0.15}"
MAJIC_DECAY_ETA="${MAJIC_DECAY_ETA:-0.95}"
MAJIC_DECAY_INTERVAL="${MAJIC_DECAY_INTERVAL:-40}"
MAJIC_RESET_INTERVAL="${MAJIC_RESET_INTERVAL:-80}"
MAJIC_SEED="${MAJIC_SEED:-0}"

# ------------------------------------------------------------------------------
# 4. Output
# ------------------------------------------------------------------------------
RESULTS_DIR="${RESULTS_DIR:-/mnt/shared-storage-user/yupeng/MAGIC/eval-dace/MAJIC/results/dace/$MODEL_NAME-$(date +%Y%m%d_%H%M%S)}"

# ------------------------------------------------------------------------------
# Execution
# ==============================================================================
cd "$(dirname "$0")"

echo "----------------------------------------------------------------"
echo "MAJIC Evaluation"
echo "Target Model (defender): $TARGET_MODEL @ $DEFENDER_API_BASE_URL"
echo "Attacker Model:          $ATTACKER_MODEL @ $ATTACKER_API_BASE_URL"
echo "Judge Model:             $JUDGE_MODEL"
echo "Dataset:                 $DATASET_PATH"
echo "Num Samples:             ${NUM_SAMPLES:-<all>}"
echo "Start Index:             $START_INDEX"
echo "Init Mode:               $MAJIC_INIT_MODE"
echo "Init Matrix:             $MAJIC_INIT_MATRIX"
echo "Chain Count / Length:    $MAJIC_CHAIN_COUNT / $MAJIC_CHAIN_LENGTH"
echo "Results Dir:             $RESULTS_DIR"
echo "----------------------------------------------------------------"

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
    --dataset-column \"$DATASET_COLUMN\" \
    --dataset-jsonl-field \"$DATASET_JSONL_FIELD\" \
    --start-index \"$START_INDEX\" \
    --init-mode \"$MAJIC_INIT_MODE\" \
    --init-matrix-path \"$MAJIC_INIT_MATRIX\" \
    --chain-count \"$MAJIC_CHAIN_COUNT\" \
    --chain-length \"$MAJIC_CHAIN_LENGTH\" \
    --init-qnum \"$MAJIC_INIT_QNUM\" \
    --chain-qnum \"$MAJIC_CHAIN_QNUM\" \
    --alpha \"$MAJIC_ALPHA\" \
    --gamma \"$MAJIC_GAMMA\" \
    --beta \"$MAJIC_BETA\" \
    --temperature \"$MAJIC_SOFTMAX_T\" \
    --decay-eta \"$MAJIC_DECAY_ETA\" \
    --decay-interval \"$MAJIC_DECAY_INTERVAL\" \
    --reset-interval \"$MAJIC_RESET_INTERVAL\" \
    --seed \"$MAJIC_SEED\" \
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
