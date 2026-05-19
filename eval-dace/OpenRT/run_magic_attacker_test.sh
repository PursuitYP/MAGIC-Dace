#!/bin/bash

# ==============================================================================
# MAGIC Attack Cross Experiment (1 rewrite, temp=0.7, WildJailbreak harmful JSONL)
# ==============================================================================

set -euo pipefail

# Common API credentials
export DEFENDER_API_KEY="FAKE_API_KEY"
export DEFENDER_API_MODEL="orm"
export ATTACKER_API_KEY="FAKE_API_KEY"
export ATTACKER_API_MODEL="orm"

# Gemini defender (OpenAI-compatible)
# export GEMINI_DEFENDER_API_BASE_URL="https://api.boyuerichdata.opensphereai.com/v1"
# export GEMINI_DEFENDER_API_KEY="sk-43Usgp7ge22R5UjYVpJOca1OGvTOsOK3PQfhnYiqLN3JuHvR"
# export GEMINI_DEFENDER_API_KEY="sk-K6VceMUqp4nb0awvQ6Mp8leG4HDsqJ557AW1r6Z8umNpnRX2"     # api-key from jc
export GEMINI_DEFENDER_API_KEY="sk-ua4rD1WerZKpDyb7JHOSKxVvMmvMZIKi6rXGPotdX9nfxNXr"
export GEMINI_DEFENDER_API_BASE_URL="http://35.220.164.252:3888/v1/"
export GEMINI_DEFENDER_API_MODEL="gemini-2.5-flash"

# Judge Model (OpenAI/Compatible)
# export OPENAI_API_KEY="sk-43Usgp7ge22R5UjYVpJOca1OGvTOsOK3PQfhnYiqLN3JuHvR"
# export OPENAI_BASE_URL="https://api.boyuerichdata.opensphereai.com/v1"
# export OPENAI_API_KEY="sk-K6VceMUqp4nb0awvQ6Mp8leG4HDsqJ557AW1r6Z8umNpnRX2"     # api-key from jc
export OPENAI_API_KEY="sk-ua4rD1WerZKpDyb7JHOSKxVvMmvMZIKi6rXGPotdX9nfxNXr"
export OPENAI_BASE_URL="http://35.220.164.252:3888/v1/"

ATTACKER_ANSWER_EXTRACT="true"

# Dataset
DATASET_PATH="/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/seed/Wildjailbreak/harmful.jsonl"
NUM_SAMPLES=600

# MAGIC settings
MAGIC_NUM_REWRITES=1
MAGIC_TEMPERATURE=0.0

# Defender endpoints (name|url)
DEFENDERS=(
  "llama|http://s-20260507012755-x92kd-decode.ailab-safethm.svc:28648/v1"
  "dace|http://s-20260429151904-5j4n7-decode.ailab-safethm.svc:28658/v1"
  "magic|http://s-20260507010133-jlxhr-decode.ailab-safethm.svc:28648/v1"

  "gemini-2.5-flash|$GEMINI_DEFENDER_API_BASE_URL|$GEMINI_DEFENDER_API_MODEL|$GEMINI_DEFENDER_API_KEY"

  "mistral|http://s-20260507012850-zgq65-decode.ailab-safethm.svc:28648/v1"
#   "attacker-base|http://s-20260117120746-p2wr6-decode.ailab-safethm.svc:23260/v1"
#   "attacker-sft|http://s-20260118130233-zr9p5-decode.ailab-safethm.svc:23261/v1"
#   "vicuna-7b-v1.5|http://s-20260128205316-q27jg-decode.ailab-safethm.svc:24001/v1"
  "qwen|http://s-20260429151806-6gxrd-decode.ailab-safethm.svc:28648/v1"
  # "llama|http://s-20260507012755-x92kd-decode.ailab-safethm.svc:28648/v1"
  # "dace|http://s-20260429151904-5j4n7-decode.ailab-safethm.svc:28658/v1"
  # "magic|http://s-20260507010133-jlxhr-decode.ailab-safethm.svc:28648/v1"
#  "def-s15|http://s-20260128171557-z57qc-decode.ailab-safethm.svc:22361/v1"
#  "def-s45|http://s-20260128171632-jtfxm-decode.ailab-safethm.svc:22362/v1"
#  "def-s75|http://s-20260128171520-t5www-decode.ailab-safethm.svc:22360/v1"
)

# Attacker endpoints (name|url)
ATTACKERS=(
  # "att-q257b-it|http://s-20251216145244-8xhw4-decode.ailab-safethm.svc:23300/v1"
  # "qwen-attacker|http://s-20260429151806-6gxrd-decode.ailab-safethm.svc:28648/v1"
  # "magic-attacker|http://s-20260507001634-nbbrd-decode.ailab-safethm.svc:28648/v1"
  "dace|http://s-20260507013934-wnjjb-decode.ailab-safethm.svc:28658/v1"
#  "att-s15|http://s-20260128170920-875kd-decode.ailab-safethm.svc:22325/v1"
#  "att-s45|http://s-20260128171310-r4d9v-decode.ailab-safethm.svc:22326/v1"
  # "att-s75|http://s-20260128122554-xhknl-decode.ailab-safethm.svc:22324/v1"
#  "att-s105|http://s-20260129111752-4tshq-decode.ailab-safethm.svc:22327/v1"
)

# BASE_RESULTS_DIR="./results/magic_attacker_cross_$(date +%Y%m%d_%H%M%S)"
BASE_RESULTS_DIR="/mnt/shared-storage-user/yupeng/MAGIC/eval-dace/OpenRT/results/dace/magic_attacker_cross_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BASE_RESULTS_DIR"

cd "$(dirname "$0")"

for defender in "${DEFENDERS[@]}"; do
  IFS='|' read -r DEFENDER_NAME DEFENDER_URL DEFENDER_MODEL DEFENDER_KEY <<< "$defender"
  DEFENDER_MODEL="${DEFENDER_MODEL:-$DEFENDER_API_MODEL}"
  DEFENDER_KEY="${DEFENDER_KEY:-$DEFENDER_API_KEY}"

  for attacker in "${ATTACKERS[@]}"; do
    ATTACKER_NAME="${attacker%%|*}"
    ATTACKER_URL="${attacker##*|}"

    RESULTS_DIR="${BASE_RESULTS_DIR}/${DEFENDER_NAME}_defender__${ATTACKER_NAME}_attacker"
    mkdir -p "$RESULTS_DIR"

    echo "----------------------------------------------------------------"
    echo "Starting MAGIC Cross Test"
    echo "Defender: ${DEFENDER_NAME} | ${DEFENDER_URL}"
    echo "Attacker: ${ATTACKER_NAME} | ${ATTACKER_URL}"
    echo "Dataset: $DATASET_PATH (first $NUM_SAMPLES)"
    echo "MAGIC rewrites: $MAGIC_NUM_REWRITES"
    echo "MAGIC temperature: $MAGIC_TEMPERATURE"
    echo "Results Dir: $RESULTS_DIR"
    echo "----------------------------------------------------------------"

    CMD="python3 unified_eval.py \
      --target-api-key \"$DEFENDER_KEY\" \
      --target-base-url \"$DEFENDER_URL\" \
      --attacker-api-key \"$ATTACKER_API_KEY\" \
      --attacker-base-url \"$ATTACKER_URL\" \
      --judge-api-key \"$OPENAI_API_KEY\" \
      --judge-base-url \"$OPENAI_BASE_URL\" \
      --target-model \"$DEFENDER_MODEL\" \
      --attacker-model \"$ATTACKER_API_MODEL\" \
      --judge-model \"gpt-4o\" \
      --attacks magic \
      --dataset-path \"$DATASET_PATH\" \
      --dataset-jsonl-field \"vanilla\" \
      --num-samples \"$NUM_SAMPLES\" \
      --magic-num-rewrites \"$MAGIC_NUM_REWRITES\" \
      --magic-temperature \"$MAGIC_TEMPERATURE\" \
      --results-dir \"$RESULTS_DIR\""

    if [ "$ATTACKER_ANSWER_EXTRACT" = "true" ]; then
      CMD="$CMD --attacker-answer-extract"
    fi

    eval $CMD

    echo "----------------------------------------------------------------"
    echo "Finished: ${DEFENDER_NAME} x ${ATTACKER_NAME}"
  done
done
