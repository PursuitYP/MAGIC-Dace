#!/bin/bash

# Configuration
# export OPENAI_API_KEY="sk-xI8zGRXkgJzoejUP7KtcBbRfqNazmWnFqSNuw6zMn5rZClFy"
# export OPENAI_BASE_URL="https://api.boyuerichdata.opensphereai.com/v1"
export OPENAI_API_KEY="sk-ua4rD1WerZKpDyb7JHOSKxVvMmvMZIKi6rXGPotdX9nfxNXr"
# export OPENAI_API_KEY="sk-K6VceMUqp4nb0awvQ6Mp8leG4HDsqJ557AW1r6Z8umNpnRX2"     # api-key from jc
export OPENAI_BASE_URL="http://35.220.164.252:3888/v1/"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Default directories if not provided as arguments
# modify the default target directories as needed
ATTACKS="gcg"
# MODEL_NAME="DACE-Qwen2.5-7B-full-step300"
# TIMESTAMP="20260430_191400"    # replace with fixed timestamp
# MODEL_NAME="DACE-Qwen2.5-7B-v4-step300"
# TIMESTAMP="20260504_231641"
# MODEL_NAME="DACE-Qwen2.5-7B-v4-attacker1st-step300"
# TIMESTAMP="20260506_083014"
# MODEL_NAME="DACE-Qwen2.5-14B-v4-attacker1st-step300"
# TIMESTAMP="20260522_191924"   # attacker1st replace with real timestamp
# MODEL_NAME="DACE-Qwen2.5-14B-v4-defender1st-step300"
# TIMESTAMP="20260522_104901"   # run defender1st evaluation first
# MODEL_NAME="DACE-Llama3.1-8B-v4-attacker1st-step300"
# TIMESTAMP="20260528_103941"   # run atacker1st evaluation first
MODEL_NAME="DACE-Llama3.1-8B-v4-defender1st-step300"
TIMESTAMP="20260528_152106"   # defender1st replace with real timestamp
if [ "$#" -gt 0 ]; then
  TARGET_DIRS=("$@")
else
  TARGET_DIRS=(
#   "$SCRIPT_DIR/results/baseline/qwen2.5-7b-it/gcg"
#    "$SCRIPT_DIR/results/smoothllm-qwen2.5-14b-it-defense/gcg"
#    "$SCRIPT_DIR/results/0118-wocode-qwen2.5-14b-it/gcg"
#    "$SCRIPT_DIR/results/selfeval-qwen2.5-14b-it-defense/gcg"
#    "$SCRIPT_DIR/results/baseline/llama3.1-8b-it/gcg"
    # "$SCRIPT_DIR/results/0119-wocode-s195-llama3.1-8b-it/gcg"
    "/mnt/shared-storage-user/yupeng/MAGIC/eval-dace/OpenRT/results/dace/$ATTACKS-$MODEL_NAME-$TIMESTAMP/gcg"
  )
fi
echo "----------------------------------------------------------------"
echo "Starting GCG Evaluation"
echo "Target Directories:"
for dir in "${TARGET_DIRS[@]}"; do
  echo "  - $dir"
done
echo "Judge Model: gpt-4o"
echo "----------------------------------------------------------------"

# Ensure we are in the script's directory
cd "$SCRIPT_DIR"

for dir in "${TARGET_DIRS[@]}"; do
  name="$(basename "$(dirname "$dir")")"
  outdir="/mnt/shared-storage-user/yupeng/MAGIC/eval-dace/OpenRT/results/dace/$ATTACKS-$MODEL_NAME-$TIMESTAMP/judge-gcg"
  mkdir -p "$outdir"
  out_file="$outdir/gcg_evaluation_summary.json"
  python3 judge_gcg.py \
      --results-dir "$dir" \
      --judge-api-key "$OPENAI_API_KEY" \
      --judge-base-url "$OPENAI_BASE_URL" \
      --judge-model "gpt-4o" \
      --judge-threshold 5 \
      --output-file "$out_file"
done

echo "----------------------------------------------------------------"
echo "Evaluation Finished."
