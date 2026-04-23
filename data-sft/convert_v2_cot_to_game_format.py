### dace: v2 of the convert script — builds the v3 hybrid dataset (all v2 samples + v1 samples from the 3 rarest risk categories) as two intermediate jsonl files and three Alpaca-style json files ###
"""
Build the v3 hybrid SFT dataset from the v1 and v2 distilled CoT jsonl files.

v3 = ALL v2 samples  UNION  v1 samples whose risk category ∈ {rare risks}

Default rare risks (the 3 bottom categories from v1's distribution):
    - Sexual Content
    - Elections
    - Code Interpreter Abuse

Outputs:
  Two intermediate jsonl files (original record fields preserved, for downstream
  analysis like analyze_strategy_distribution.py):
    sft_data_cot_v1nv2_v3_benign.jsonl
    sft_data_cot_v1nv2_v3_harmful.jsonl
  Three Alpaca-style json files (slim, 5-key schema, for 360-LLaMA-Factory SFT):
    game_cot_dace_v1nv2_v3_benign.json
    game_cot_dace_v1nv2_v3_harmful.json
    game_cot_dace_v1nv2_v3_all.json

Dedup policy:
    - Within each side, dedup by (input, output). The same vanilla often appears
      in BOTH v1 (rare-risk CoT) and v2 (directed-style CoT); they have different
      outputs, so both are kept. Exact duplicates are dropped defensively.

Risk-filter rule on v1:
    - Parse the record's `strategy` field with the same line-anchored regex
      analyze_strategy_distribution.py uses (case-insensitive).
    - Keep iff parsed risk (casefold, trimmed) is in the rare-risk set.

Drop policy (both v1 and v2):
    - output / answer / input is null/empty.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable


TARGET_KEYS = ("instruction", "input", "output", "answer", "system")

### dace: default rare-risk set — the 3 bottom risk categories in v1's distribution ###
RARE_RISKS_DEFAULT = ["Sexual Content", "Elections", "Code Interpreter Abuse"]


### dace: mirror parse_strategy in analyze_strategy_distribution.py — line-anchored, case-insensitive ###
RISK_LINE_RE  = re.compile(r"^\s*risk category:\s*([^\n\r]+)\s*$",  re.IGNORECASE | re.MULTILINE)
STYLE_LINE_RE = re.compile(r"^\s*attack style:\s*([^\n\r]+)\s*$",   re.IGNORECASE | re.MULTILINE)


def parse_strategy(strategy_text: str | None) -> tuple[str | None, str | None]:
    if not strategy_text:
        return None, None
    r = RISK_LINE_RE.search(strategy_text)
    s = STYLE_LINE_RE.search(strategy_text)
    risk  = r.group(1).strip() if r else None
    style = s.group(1).strip() if s else None
    return risk, style


def load_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_no}: {exc}") from exc
    return records


def _slim(rec: dict) -> dict:
    return {k: (rec.get(k) if rec.get(k) is not None else "") for k in TARGET_KEYS}


def is_usable(rec: dict) -> bool:
    """Same as the convert v1 require_answer gate: non-empty input/output/answer."""
    return bool(rec.get("input")) and bool(rec.get("output")) and bool(rec.get("answer"))


### dace: v3 compose — start with all v2 records, then append v1 records whose risk ∈ rare set; dedup by (input, output) ###
def compose_v3(
    v2_records: Iterable[dict],
    v1_records: Iterable[dict],
    rare_risks_cf: set[str],
    require_answer: bool = True,
) -> tuple[list[dict], dict]:
    out: list[dict] = []
    seen: set[tuple[str, str]] = set()
    stats = {
        "v2_total": 0, "v2_kept": 0, "v2_drop_empty": 0, "v2_drop_dup": 0,
        "v1_total": 0, "v1_kept": 0, "v1_drop_empty": 0, "v1_drop_dup": 0,
        "v1_no_strategy": 0, "v1_non_rare_risk": 0,
    }

    def _try_add(rec: dict, prefix: str) -> None:
        if require_answer and not is_usable(rec):
            stats[f"{prefix}_drop_empty"] += 1
            return
        key = (rec.get("input") or "", rec.get("output") or "")
        if key in seen:
            stats[f"{prefix}_drop_dup"] += 1
            return
        seen.add(key)
        out.append(rec)
        stats[f"{prefix}_kept"] += 1

    for rec in v2_records:
        stats["v2_total"] += 1
        _try_add(rec, "v2")

    for rec in v1_records:
        stats["v1_total"] += 1
        risk, _ = parse_strategy(rec.get("strategy"))
        if not risk:
            stats["v1_no_strategy"] += 1
            continue
        if risk.strip().casefold() not in rare_risks_cf:
            stats["v1_non_rare_risk"] += 1
            continue
        _try_add(rec, "v1")

    return out, stats


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def write_json_array(path: Path, records: list[dict]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    slim = [_slim(r) for r in records]
    path.write_text(json.dumps(slim, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(slim)


def build_parser() -> argparse.ArgumentParser:
    here = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(
        description="Build v3 = ALL v2 + v1-rare-risk hybrid dataset (two intermediate jsonl + three Alpaca json)."
    )

    # inputs
    p.add_argument("--v1-benign-src",  type=Path, default=here / "sft_data_cot_benign.jsonl")
    p.add_argument("--v1-harmful-src", type=Path, default=here / "sft_data_cot_harmful.jsonl")
    p.add_argument("--v2-benign-src",  type=Path, default=here / "sft_data_cot_v2_benign.jsonl")
    p.add_argument("--v2-harmful-src", type=Path, default=here / "sft_data_cot_v2_harmful.jsonl")

    # intermediate jsonl outputs (full record, not slimmed)
    p.add_argument("--v3-benign-jsonl",  type=Path, default=here / "sft_data_cot_v1nv2_v3_benign.jsonl")
    p.add_argument("--v3-harmful-jsonl", type=Path, default=here / "sft_data_cot_v1nv2_v3_harmful.jsonl")

    # final Alpaca json outputs (5-key slim)
    p.add_argument("--v3-benign-json",  type=Path, default=here / "game_cot_dace_v1nv2_v3_benign.json")
    p.add_argument("--v3-harmful-json", type=Path, default=here / "game_cot_dace_v1nv2_v3_harmful.json")
    p.add_argument("--v3-merged-json",  type=Path, default=here / "game_cot_dace_v1nv2_v3_all.json")

    p.add_argument(
        "--rare-risks", nargs="+", default=RARE_RISKS_DEFAULT,
        help="Canonical risk category names (case-insensitive match) to include from v1. "
             f"Default: {RARE_RISKS_DEFAULT}",
    )
    p.add_argument(
        "--no-require-answer", action="store_true",
        help="Keep rows even when output/answer/input is empty (default: drop them).",
    )
    return p


def _format_stats(label: str, stats: dict) -> str:
    return (
        f"[{label}] v2: total={stats['v2_total']} kept={stats['v2_kept']} "
        f"empty={stats['v2_drop_empty']} dup={stats['v2_drop_dup']}  | "
        f"v1: total={stats['v1_total']} kept={stats['v1_kept']} "
        f"non_rare={stats['v1_non_rare_risk']} no_strategy={stats['v1_no_strategy']} "
        f"empty={stats['v1_drop_empty']} dup={stats['v1_drop_dup']}"
    )


def main() -> None:
    args = build_parser().parse_args()
    rare_risks_cf = {r.strip().casefold() for r in args.rare_risks}
    require_answer = not args.no_require_answer

    print(f"[rare-risks] (case-insensitive) {sorted(rare_risks_cf)}")

    # benign
    v2_b = load_jsonl(args.v2_benign_src)
    v1_b = load_jsonl(args.v1_benign_src)
    benign_v3, bs = compose_v3(v2_b, v1_b, rare_risks_cf, require_answer)
    write_jsonl(args.v3_benign_jsonl, benign_v3)
    b_rows = write_json_array(args.v3_benign_json, benign_v3)
    print(_format_stats("benign", bs))
    print(f"  -> {args.v3_benign_jsonl} ({len(benign_v3)} rows)")
    print(f"  -> {args.v3_benign_json}  ({b_rows} rows)")

    # harmful
    v2_h = load_jsonl(args.v2_harmful_src)
    v1_h = load_jsonl(args.v1_harmful_src)
    harmful_v3, hs = compose_v3(v2_h, v1_h, rare_risks_cf, require_answer)
    write_jsonl(args.v3_harmful_jsonl, harmful_v3)
    h_rows = write_json_array(args.v3_harmful_json, harmful_v3)
    print(_format_stats("harmful", hs))
    print(f"  -> {args.v3_harmful_jsonl} ({len(harmful_v3)} rows)")
    print(f"  -> {args.v3_harmful_json}  ({h_rows} rows)")

    # merged
    merged = benign_v3 + harmful_v3
    m_rows = write_json_array(args.v3_merged_json, merged)
    print(f"[merged]  total={len(merged)} (benign={len(benign_v3)} + harmful={len(harmful_v3)})")
    print(f"  -> {args.v3_merged_json}  ({m_rows} rows)")


if __name__ == "__main__":
    main()


"""Example usage:

# Default — reads v1 + v2 jsonl from data-sft/, writes v3 jsonl + json to data-sft/
python data-sft/convert_v2_cot_to_game_format.py

# Land v3 Alpaca json directly into LLaMA-Factory's data/ (requires registering
# game_cot_dace_v1nv2_v3_{benign,harmful,all} in dataset_info.json beforehand)
python data-sft/convert_v2_cot_to_game_format.py \\
    --v3-benign-json  src/360-LLaMA-Factory/data/game_cot_dace_v1nv2_v3_benign.json \\
    --v3-harmful-json src/360-LLaMA-Factory/data/game_cot_dace_v1nv2_v3_harmful.json \\
    --v3-merged-json  src/360-LLaMA-Factory/data/game_cot_dace_v1nv2_v3_all.json

# Different rare-risk set (e.g., include all four bottom categories)
python data-sft/convert_v2_cot_to_game_format.py \\
    --rare-risks "Sexual Content" "Elections" "Code Interpreter Abuse" "Defamation"
"""
