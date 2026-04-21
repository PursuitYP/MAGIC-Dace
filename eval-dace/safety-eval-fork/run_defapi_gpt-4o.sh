#!/bin/bash

set -u
set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 配置
MODEL_PATH="/mnt/shared-storage-user/wenxiaoyu/selfplay-redteaming/checkpoints/selfplay_RL_FULL_PTX_SFT_wjbhs_re++_rtg_0327T13:52/ckpt/global_step200_hf"
MODEL_NAME="self-redteam-l318i-qwenguard2"
TASKS="wildguardtest,harmbench_precompute,wildjailbreak:benign,wildjailbreak:harmful,do_anything_now,harmbench,or_bench:toxic,xstest"
#TASKS="or_bench:toxic,xstest"
CLASSIFIER="gpt-4o"


RESULTS_DIR="/mnt/shared-storage-user/wenxiaoyu/game-private/eval/safety-eval-fork/results/rebuttal/$MODEL_NAME/$CLASSIFIER/-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULTS_DIR"

AGG_METRICS_PATH="$RESULTS_DIR/metrics.json"
AGG_ALL_RESULTS_PATH="$RESULTS_DIR/all_results.json"
SUMMARY_PATH="$RESULTS_DIR/task_status.tsv"

echo -e "task	status	task_dir" > "$SUMMARY_PATH"

# 环境变量 - Defender API 配置
export DEFENDER_API_BASE_URL="http://s-20260329204906-l7cll-decode.ailab-safethm.svc:23301/v1"
export DEFENDER_API_KEY="FAKE_API_KEY"
export DEFENDER_API_MODEL="orm"

# 环境变量 - GPT-4o judge 配置
export OPENAI_BASE_URL="https://api.boyuerichdata.opensphereai.com/v1"
export OPENAI_API_KEY="sk-D0wGaXJBOV1f6VTnJzwRuhLewJ0Crn1KNQeSXnRRn2dM6ITR"
export OPENAI_MODEL="gpt-4o"
export Judge_API_BASE_URL="$OPENAI_BASE_URL"
export Judge_API_KEY="$OPENAI_API_KEY"
export JUDGE_MODEL="$OPENAI_MODEL"

# 激活环境
eval "$(conda shell.bash hook)"
conda activate safety-eval

merge_json_reports() {
    local src_path="$1"
    local dst_path="$2"
    python - "$src_path" "$dst_path" <<'PY_MERGE'
import json
import os
import sys
from pathlib import Path

src_path = Path(sys.argv[1])
dst_path = Path(sys.argv[2])
if not src_path.exists():
    raise SystemExit(0)

with src_path.open() as f:
    src = json.load(f)

if dst_path.exists():
    with dst_path.open() as f:
        dst = json.load(f)
else:
    dst = {}

dst.update(src)
dst_path.parent.mkdir(parents=True, exist_ok=True)
with dst_path.open('w') as f:
    json.dump(dst, f, indent=4)
PY_MERGE
}

run_single_task() {
    local task_name="$1"
    local safe_task_name="${task_name//:/__}"
    safe_task_name="${safe_task_name//\//__}"
    local task_dir="$RESULTS_DIR/$safe_task_name"
    local task_metrics_path="$task_dir/metrics.json"
    local task_all_results_path="$task_dir/all_results.json"
    local task_log_path="$task_dir/eval.log"

    mkdir -p "$task_dir"

    echo "============================================================"
    echo "[RUN] Task: $task_name"
    echo "[DIR] $task_dir"
    echo "============================================================"

    python -u evaluation/eval.py generators         --model_name_or_path "$MODEL_PATH"         --model_input_template_path_or_name "hf"         --tasks "$task_name"         --report_output_path "$task_metrics_path"         --save_individual_results_path "$task_all_results_path"         --use_defender_api         --classifier_model_name "$CLASSIFIER"         --batch_size 1 2>&1 | tee "$task_log_path"
    local cmd_status=${PIPESTATUS[0]}

    if [ "$cmd_status" -eq 0 ]; then
        merge_json_reports "$task_metrics_path" "$AGG_METRICS_PATH"
        merge_json_reports "$task_all_results_path" "$AGG_ALL_RESULTS_PATH"
        echo -e "$task_name	SUCCESS	$task_dir" >> "$SUMMARY_PATH"
        echo "[OK] Task finished: $task_name"
    else
        echo -e "$task_name	FAILED($cmd_status)	$task_dir" >> "$SUMMARY_PATH"
        echo "[FAIL] Task failed: $task_name (exit=$cmd_status)"
    fi

    return "$cmd_status"
}

IFS=',' read -r -a TASK_ARRAY <<< "$TASKS"
FAILED_TASKS=0

for task_name in "${TASK_ARRAY[@]}"; do
    if ! run_single_task "$task_name"; then
        FAILED_TASKS=$((FAILED_TASKS + 1))
    fi
done

echo
if [ "$FAILED_TASKS" -eq 0 ]; then
    echo "✓ 全部评测完成: $RESULTS_DIR"
else
    echo "⚠ 部分任务失败，但已完成任务的结果已经保存: $RESULTS_DIR"
    echo "  Failed tasks: $FAILED_TASKS"
fi

echo "  Classifier: $CLASSIFIER"
echo "  Defender API: $DEFENDER_API_BASE_URL"
echo "  Aggregate metrics: $AGG_METRICS_PATH"
echo "  Aggregate histories: $AGG_ALL_RESULTS_PATH"
echo "  Task status: $SUMMARY_PATH"

if [ "$FAILED_TASKS" -ne 0 ]; then
    exit 1
fi
