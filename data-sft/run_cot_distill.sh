#!/usr/bin/env bash
### dace: idempotent driver that finishes distilling benign+harmful vanilla prompts to CoT JSONL ###
#
# Usage:
#   bash data-sft/run_cot_distill.sh               # clean failed rows + run both scripts in parallel
#   bash data-sft/run_cot_distill.sh --no-clean    # do NOT remove answer=null rows before running
#   bash data-sft/run_cot_distill.sh --only benign # only run the benign pipeline
#   bash data-sft/run_cot_distill.sh --only harmful
#
# Safe to run repeatedly. Each invocation:
#   1. (by default) strips records whose answer/output is null/empty to .err file (so BadRequestError rows get retried)
#   2. re-runs both python scripts, which internally dedup + drop 8192-truncated rows for regeneration
#   3. prints a completion summary
#
# Targets:
#   benign  : sft_data_source_benign.jsonl          (~20000 unique)   -> sft_data_cot_benign.jsonl   (~20000 rows)
#   harmful : sft_data_source_harmful_dedup.jsonl   (~5794 unique)    -> sft_data_cot_harmful.jsonl  (5794 x NUM_RUNS=4 ~= 23176 rows)

set -euo pipefail

### dace: resolve project root from this script's own location so it works from any cwd ###
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

CLEAN_ERRORS=1
ONLY=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-clean) CLEAN_ERRORS=0; shift ;;
    --only)     ONLY="${2:-}"; shift 2 ;;
    -h|--help)
      grep -E "^#( |$)" "$0" | sed 's/^# \{0,1\}//'
      exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

mkdir -p logs

### dace: activate conda env 'magic'; fall back to current interpreter if conda is unavailable ###
if command -v conda >/dev/null 2>&1; then
  # shellcheck disable=SC1091
  source "$(conda info --base)/etc/profile.d/conda.sh"
  conda activate magic
fi

BENIGN_OUT="data-sft/sft_data_cot_benign.jsonl"
HARMFUL_OUT="data-sft/sft_data_cot_harmful.jsonl"

### dace: strip answer=null / output=null rows so BadRequestError failures get re-requested next run ###
clean_failed_rows() {
  python - "$BENIGN_OUT" "$HARMFUL_OUT" <<'PY'
import json, sys
from pathlib import Path
for arg in sys.argv[1:]:
    p = Path(arg)
    if not p.exists():
        print(f"[clean] {p.name}: not found, skip")
        continue
    kept, dropped = [], []
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            dropped.append(line)
            continue
        if r.get("answer") in (None, "") or r.get("output") in (None, ""):
            dropped.append(line)
        else:
            kept.append(line)
    p.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")
    if dropped:
        p.with_suffix(p.suffix + ".err").write_text("\n".join(dropped) + "\n", encoding="utf-8")
    print(f"[clean] {p.name}: kept={len(kept)}, removed={len(dropped)}")
PY
}

### dace: report per-file completion counts (ok = answer non-empty; err = answer null/missing) ###
summarize() {
  python - "$BENIGN_OUT" "$HARMFUL_OUT" <<'PY'
import json, sys
from pathlib import Path
for arg in sys.argv[1:]:
    p = Path(arg)
    if not p.exists():
        print(f"[summary] {p.name}: not found")
        continue
    ok = err = 0
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            err += 1
            continue
        (ok := ok + 1) if r.get("answer") else (err := err + 1)
    print(f"[summary] {p.name}: ok={ok}, err_or_null={err}")
PY
}

if [[ "$CLEAN_ERRORS" -eq 1 ]]; then
  clean_failed_rows
else
  echo "[clean] skipped (--no-clean)"
fi

PIDS=()
if [[ -z "$ONLY" || "$ONLY" == "benign" ]]; then
  echo "[run] launching benign distillation -> logs/distill_benign.log"
  python data-sft/distill_vanilla_benign_jsonl.py > logs/distill_benign.log 2>&1 &
  PIDS+=($!)
fi
if [[ -z "$ONLY" || "$ONLY" == "harmful" ]]; then
  echo "[run] launching harmful distillation -> logs/distill_harmful.log"
  python data-sft/distill_vanilla_harmful_jsonl.py > logs/distill_harmful.log 2>&1 &
  PIDS+=($!)
fi

STATUS=0
for pid in "${PIDS[@]}"; do
  if wait "$pid"; then
    echo "[run] pid=$pid finished OK"
  else
    rc=$?
    echo "[run] pid=$pid FAILED with exit=$rc" >&2
    STATUS=$rc
  fi
done

summarize
exit "$STATUS"
