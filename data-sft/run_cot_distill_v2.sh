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
#   1. (by default) strips records that are unusable for SFT and moves them to a .err file so the Python
#      distiller re-requests them next run. A row is dropped when ANY of the following holds:
#        - output is null/empty (BadRequestError from Gemini)
#        - answer extraction yielded empty (no <answer> block)
#        - output violates the <think><strategy><answer> format enforced by
#          format_reward_func_dace (src/verl/verl/utils/reward_score/game.py)
#        - the <strategy> block cannot be parsed as "risk category: X\nattack style: Y",
#          or the named risk category / attack style is outside the canonical DACE 14x10 space
#          (case-insensitive match; words must otherwise be verbatim)
#        - the line itself is not valid JSON
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

### dace: strip rows whose answer/output is null, whose raw output violates the <think><strategy><answer> format (mirrors format_reward_func_dace in verl/utils/reward_score/game.py), or whose <strategy> block names a risk category / attack style outside the 14x10 DACE space; dropped rows go to <out>.err so the Python distiller re-requests them next run ###
clean_failed_rows() {
  python - "$BENIGN_OUT" "$HARMFUL_OUT" <<'PY'
import json, re, sys
from pathlib import Path

### dace: keep this regex/counter pair in sync with format_reward_func_dace in src/verl/verl/utils/reward_score/game.py ###
DACE_ORDER_PATTERN = re.compile(
    r"^<think>[\s\S]*?</think>\s*<strategy>[\s\S]*?</strategy>\s*<answer>[\s\S]*?</answer>$",
    re.DOTALL,
)
DACE_REQUIRED_COUNTS = (1, 1, 1, 1, 1, 1)

### dace: strategy regex mirrors extract_strategy_text in src/verl/verl/utils/reward_score/game.py ###
STRATEGY_PATTERN = re.compile(
    r"<strategy>\s*risk category:\s*(.+?)\s*\n\s*attack style:\s*(.+?)\s*</strategy>",
    re.DOTALL | re.IGNORECASE,
)

### dace: canonical 14 risk categories and 10 attack styles from the DACE strategy space (see distill_vanilla_*_jsonl.py / data/safety/preprocess_dace.py); case-insensitive match but words must be verbatim ###
RISK_CATEGORIES_CANONICAL = [
    "Violent Crimes",
    "Non-Violent Crimes",
    "Sex-Related Crimes",
    "Child Sexual Exploitation",
    "Defamation",
    "Specialized Advice",
    "Privacy",
    "Intellectual Property",
    "Indiscriminate Weapons",
    "Hate",
    "Suicide & Self-Harm",
    "Sexual Content",
    "Elections",
    "Code Interpreter Abuse",
]
ATTACK_STYLES_CANONICAL = [
    "Slang",
    "Technical Terms",
    "Role Play",
    "Authority Manipulation",
    "Misspellings",
    "Word Play",
    "Emotional Manipulation",
    "Hypotheticals",
    "Historical Scenario",
    "Uncommon Dialects",
]
RISK_SET  = {s.casefold() for s in RISK_CATEGORIES_CANONICAL}
STYLE_SET = {s.casefold() for s in ATTACK_STYLES_CANONICAL}


def check_dace_format(text: str) -> bool:
    """Return True iff `text` satisfies format_reward_func_dace (exactly one ordered think/strategy/answer block)."""
    text = (text or "").strip()
    if not text:
        return False
    counts = (
        text.count("<think>"),    text.count("</think>"),
        text.count("<strategy>"), text.count("</strategy>"),
        text.count("<answer>"),   text.count("</answer>"),
    )
    if counts != DACE_REQUIRED_COUNTS:
        return False
    return DACE_ORDER_PATTERN.search(text) is not None


def classify_strategy(text: str) -> str | None:
    """Return None if the <strategy> block is fully valid; otherwise a reason tag:
    - 'bad_strategy_parse': <strategy> block missing / not in 'risk category: X\nattack style: Y' form
    - 'bad_risk'          : parsable but risk category not one of the canonical 14
    - 'bad_style'         : parsable but attack style not one of the canonical 10
    Matching is case-insensitive; the captured words must otherwise be verbatim (whitespace-stripped).
    """
    m = STRATEGY_PATTERN.search(text or "")
    if not m:
        return "bad_strategy_parse"
    risk  = (m.group(1) or "").strip().casefold()
    style = (m.group(2) or "").strip().casefold()
    if risk not in RISK_SET:
        return "bad_risk"
    if style not in STYLE_SET:
        return "bad_style"
    return None


for arg in sys.argv[1:]:
    p = Path(arg)
    if not p.exists():
        print(f"[clean] {p.name}: not found, skip")
        continue

    kept, dropped = [], []
    stats = {
        "total": 0,
        "ok": 0,
        "bad_json": 0,             # 整行 JSON 解析失败
        "null_output": 0,          # BadRequestError 兜底：Gemini 调用失败，output=None/""
        "null_answer": 0,          # output 非空但抠不出 <answer> → answer=""
        "bad_format": 0,           # output 不满足 format_reward_func_dace 的三段式
        "bad_strategy_parse": 0,   # <strategy> 块缺失或非 "risk category: X / attack style: Y" 形式
        "bad_risk": 0,             # risk category 不在 canonical 14 之内
        "bad_style": 0,            # attack style 不在 canonical 10 之内
    }

    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        stats["total"] += 1

        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            stats["bad_json"] += 1
            dropped.append(line)
            continue

        output = r.get("output")
        answer = r.get("answer")

        if output in (None, ""):
            stats["null_output"] += 1
            dropped.append(line)
            continue
        if answer in (None, ""):
            stats["null_answer"] += 1
            dropped.append(line)
            continue
        if not check_dace_format(output):
            stats["bad_format"] += 1
            dropped.append(line)
            continue

        strat_reason = classify_strategy(output)
        if strat_reason is not None:
            stats[strat_reason] += 1
            dropped.append(line)
            continue

        stats["ok"] += 1
        kept.append(line)

    p.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")
    err_path = p.with_suffix(p.suffix + ".err")
    if dropped:
        err_path.write_text("\n".join(dropped) + "\n", encoding="utf-8")

    removed = len(dropped)
    err_note = f" -> {err_path.name}" if dropped else ""
    print(
        f"[clean] {p.name}: total={stats['total']}, kept={stats['ok']}, removed={removed} "
        f"(null_output={stats['null_output']}, null_answer={stats['null_answer']}, "
        f"bad_format={stats['bad_format']}, bad_strategy_parse={stats['bad_strategy_parse']}, "
        f"bad_risk={stats['bad_risk']}, bad_style={stats['bad_style']}, "
        f"bad_json={stats['bad_json']}){err_note}"
    )
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
