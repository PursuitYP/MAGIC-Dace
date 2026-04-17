"""
Regenerate `output` for Alpaca-style records (instruction/input/output/system)
using an OpenAI-compatible chat API.

Example:
    python scripts/regenerate_alpaca_outputs.py \
        --input data/safety/game_cot_gemini_idx3500.jsonl \
        --output data/safety/game_cot_gemini_idx3500_regen.jsonl \
        --model gemini-2.5-pro \
        --api-base https://api.boyuerichdata.opensphereai.com/v1 \
        --max-tokens 8192

The script:
    * reads JSONL records with fields: instruction, input, system, output
    * sends system/instruction/input to the chat API
    * replaces `output` with the new completion text
    * writes updated records as JSONL
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from openai import OpenAI


def iter_jsonl(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, 1):
            raw = line.strip()
            if not raw:
                continue
            try:
                yield json.loads(raw)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Failed to parse {path} at line {line_no}: {exc}") from exc


def build_messages(system: str, instruction: str, user_input: str) -> list[dict]:
    return [
        {"role": "system", "content": system or ""},
        {"role": "user", "content": f"{instruction}\n\n{user_input}".strip()},
    ]


def regenerate_record(
    client: OpenAI,
    record: dict,
    model: str,
    max_tokens: int,
    temperature: float,
) -> dict:
    system = record.get("system", "")
    instruction = record.get("instruction", "")
    user_input = record.get("input", "")

    resp = client.chat.completions.create(
        model=model,
        messages=build_messages(system, instruction, user_input),
        temperature=temperature,
        max_tokens=max_tokens,
    )
    choice = resp.choices[0]
    record["output"] = choice.message.content
    record["stop_reason"] = choice.finish_reason
    if getattr(resp, "usage", None):
        record["usage"] = {
            "prompt_tokens": resp.usage.prompt_tokens,
            "completion_tokens": resp.usage.completion_tokens,
            "total_tokens": resp.usage.total_tokens,
        }
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description="Regenerate Alpaca-style outputs via chat API.")
    parser.add_argument("--input", type=Path, required=True, help="Source JSONL file.")
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Destination JSONL file for regenerated records.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-2.5-pro",
        help="Model name to send to the chat API.",
    )
    parser.add_argument(
        "--api-base",
        type=str,
        default="https://api.boyuerichdata.opensphereai.com/v1",
        help="OpenAI-compatible API base URL.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=8192,
        help="Max tokens for the completion.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature.",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="API key (defaults to OPENAI_API_KEY env when omitted).",
    )
    args = parser.parse_args()

    client = OpenAI(api_key=args.api_key, base_url=args.api_base)

    out_lines = []
    for rec in iter_jsonl(args.input):
        new_rec = regenerate_record(
            client=client,
            record=rec,
            model=args.model,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
        )
        out_lines.append(json.dumps(new_rec, ensure_ascii=False))

    args.output.write_text("\n".join(out_lines) + ("\n" if out_lines else ""), encoding="utf-8")
    print(f"Wrote {len(out_lines)} records to {args.output}")


if __name__ == "__main__":
    main()
