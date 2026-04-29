#!/bin/bash

# Configuration
export OPENAI_API_KEY="sk-xI8zGRXkgJzoejUP7KtcBbRfqNazmWnFqSNuw6zMn5rZClFy"
export OPENAI_BASE_URL="https://api.boyuerichdata.opensphereai.com/v1"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Default directories if not provided as arguments
if [ "$#" -gt 0 ]; then
  TARGET_DIRS=("$@")
else
  TARGET_DIRS=(
#   "$SCRIPT_DIR/results/baseline/qwen2.5-7b-it/gcg"
#    "$SCRIPT_DIR/results/smoothllm-qwen2.5-14b-it-defense/gcg"
#    "$SCRIPT_DIR/results/0118-wocode-qwen2.5-14b-it/gcg"
#    "$SCRIPT_DIR/results/selfeval-qwen2.5-14b-it-defense/gcg"
#    "$SCRIPT_DIR/results/baseline/llama3.1-8b-it/gcg"
    "$SCRIPT_DIR/results/0119-wocode-s195-llama3.1-8b-it/gcg"
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
  out_file="gcg_evaluation_summary_${name}.json"
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
