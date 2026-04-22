### dace: convert distilled CoT JSONL (benign + harmful) to the Alpaca-style JSON array consumed by src/360-LLaMA-Factory ###
"""
Convert the two distilled CoT JSONL files into Alpaca-style JSON arrays
(same 5-key schema as src/360-LLaMA-Factory/data/game_cot_benign.json), mirroring
/mnt/shared-storage-user/wenxiaoyu/game-private/data/safety/convert_benign_to_game_format.py.

Inputs  (defaults, same dir as this script):
    sft_data_cot_benign.jsonl
    sft_data_cot_harmful.jsonl

Outputs (defaults, same dir):
    sft_data_cot_benign.json
    sft_data_cot_harmful.json
    (and optionally --merged-out <path> for the concatenation)

Kept fields per record: instruction, input, output, answer, system.

Dedup policy:
    - benign : dedup by `input` (one CoT per unique vanilla).
    - harmful: NO input-level dedup; each question has NUM_RUNS (=4) distinct CoT
               traces and we want to keep all of them. Only exact (input, output)
               duplicates are dropped, defensively.

Drop policy (applied to both):
    - output is null/empty (e.g., BadRequestError rows still sitting in the file)
    - answer is null/empty
    Pass --no-require-answer to keep those rows as-is.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TARGET_KEYS = ("instruction", "input", "output", "answer", "system")


def load_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}: JSON decode error at line {line_no}: {exc}") from exc
            records.append(obj)
    return records


def _slim(rec: dict) -> dict:
    return {k: (rec.get(k) if rec.get(k) is not None else "") for k in TARGET_KEYS}


### dace: convert one jsonl to the list-of-dicts target format with configurable dedup ###
def convert(
    records: list[dict],
    *,
    dedup_key: str,              # "input" | "input_output" | "none"
    require_answer: bool,
) -> tuple[list[dict], dict]:
    out: list[dict] = []
    seen: set = set()
    stats = {"total": 0, "kept": 0, "drop_empty": 0, "drop_dup": 0}

    for rec in records:
        stats["total"] += 1

        input_text = rec.get("input") or ""
        output_text = rec.get("output")
        answer_text = rec.get("answer")

        if require_answer and (not output_text or not answer_text or not input_text):
            stats["drop_empty"] += 1
            continue

        if dedup_key == "input":
            key = input_text
        elif dedup_key == "input_output":
            key = (input_text, output_text)
        else:
            key = None

        if key is not None:
            if key in seen:
                stats["drop_dup"] += 1
                continue
            seen.add(key)

        out.append(_slim(rec))
        stats["kept"] += 1

    return out, stats


def _dump_json(path: Path, payload: list[dict]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Convert distilled CoT JSONL to Alpaca-style JSON for SFT.")
    parser.add_argument("--benign-src",  type=Path, default=here / "sft_data_cot_benign.jsonl")
    parser.add_argument("--harmful-src", type=Path, default=here / "sft_data_cot_harmful.jsonl")
    parser.add_argument("--benign-out",  type=Path, default=here / "sft_data_cot_benign.json")
    parser.add_argument("--harmful-out", type=Path, default=here / "sft_data_cot_harmful.json")
    parser.add_argument(
        "--merged-out", type=Path, default=None,
        help="If set, also write a merged JSON (benign first, then harmful).",
    )
    parser.add_argument(
        "--no-require-answer", action="store_true",
        help="Keep rows even when output/answer/input is empty (default: drop them).",
    )
    parser.add_argument(
        "--only", choices=("benign", "harmful", "both"), default="both",
        help="Process only one side (default: both).",
    )
    args = parser.parse_args()

    require_answer = not args.no_require_answer
    benign_out: list[dict] = []
    harmful_out: list[dict] = []

    if args.only in ("benign", "both"):
        benign_records = load_jsonl(args.benign_src)
        benign_out, bs = convert(benign_records, dedup_key="input", require_answer=require_answer)
        _dump_json(args.benign_out, benign_out)
        print(
            f"[benign]  {args.benign_src.name}: total={bs['total']}, kept={bs['kept']}, "
            f"drop_empty={bs['drop_empty']}, drop_dup={bs['drop_dup']} -> {args.benign_out}"
        )

    if args.only in ("harmful", "both"):
        harmful_records = load_jsonl(args.harmful_src)
        harmful_out, hs = convert(harmful_records, dedup_key="input_output", require_answer=require_answer)
        _dump_json(args.harmful_out, harmful_out)
        print(
            f"[harmful] {args.harmful_src.name}: total={hs['total']}, kept={hs['kept']}, "
            f"drop_empty={hs['drop_empty']}, drop_dup={hs['drop_dup']} -> {args.harmful_out}"
        )

    if args.merged_out and args.only == "both":
        merged = benign_out + harmful_out
        _dump_json(args.merged_out, merged)
        print(f"[merged]  total={len(merged)} (benign={len(benign_out)} + harmful={len(harmful_out)}) -> {args.merged_out}")


if __name__ == "__main__":
    main()


"""Example usage:
python data-sft/convert_cot_to_game_format.py

python data-sft/convert_cot_to_game_format.py \
    --merged-out data-sft/sft_data_cot_all.json

python data-sft/convert_cot_to_game_format.py \
    --benign-out  src/360-LLaMA-Factory/data/game_cot_dace_benign.json \
    --harmful-out src/360-LLaMA-Factory/data/game_cot_dace_harmful.json \
    --merged-out  src/360-LLaMA-Factory/data/game_cot_dace_all.json
"""