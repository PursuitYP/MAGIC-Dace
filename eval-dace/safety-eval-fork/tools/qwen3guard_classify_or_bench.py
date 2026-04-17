#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""调用 Qwen3Guard API 对 or_bench 的 prompt 进行有害性判断，并保存结果。"""
import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import datetime
from typing import Optional, Tuple

import requests


def parse_qwen3guard_output(text: str) -> Tuple[Optional[str], Optional[str], Optional[str], bool]:
    """
    解析 Qwen3Guard 输出。
    期望格式：
      Safety: Safe|Unsafe|Controversial
      Categories: ...
      Refusal: Yes|No
    返回：prompt_harmfulness, response_harmfulness, response_refusal, is_parsing_error
    """
    safe_pattern = r"Safety:\s*(Safe|Unsafe|Controversial)"
    refusal_pattern = r"Refusal:\s*(Yes|No)"

    safe_match = re.search(safe_pattern, text, re.IGNORECASE)
    refusal_match = re.search(refusal_pattern, text, re.IGNORECASE)

    safe_label = safe_match.group(1).lower() if safe_match else None
    refusal_label = refusal_match.group(1).lower() if refusal_match else None

    is_parsing_error = False

    if safe_label == "unsafe":
        prompt_harmfulness = "harmful"
        response_harmfulness = "harmful"
    elif safe_label in ("safe", "controversial"):
        prompt_harmfulness = "unharmful"
        response_harmfulness = "unharmful"
    else:
        prompt_harmfulness = None
        response_harmfulness = None
        is_parsing_error = True

    if refusal_label == "yes":
        response_refusal = "refusal"
    elif refusal_label == "no":
        response_refusal = "compliance"
    elif refusal_label is None:
        response_refusal = None
    else:
        response_refusal = None
        is_parsing_error = True

    return prompt_harmfulness, response_harmfulness, response_refusal, is_parsing_error


def call_qwen3guard(prompt: str, base_url: str, api_key: str, model: str, timeout: int, max_retries: int) -> str:
    url = base_url.rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "top_p": 1.0,
    }

    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=timeout)
            if resp.status_code != 200:
                last_err = f"HTTP {resp.status_code}: {resp.text}"
                time.sleep(min(2 ** attempt, 10))
                continue
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            last_err = str(e)
            time.sleep(min(2 ** attempt, 10))

    raise RuntimeError(f"Qwen3Guard API 调用失败: {last_err}")


def main():
    parser = argparse.ArgumentParser(description="用 Qwen3Guard API 判别 or_bench 的 prompt 有害性")
    parser.add_argument(
        "--input_csv",
        default="/mnt/shared-storage-user/wenxiaoyu/game-private/eval/safety-eval-fork/evaluation/tasks/generation/or_bench/or_bench-hard-1k.csv",
        help="输入 CSV（需含 prompt 列）",
    )
    parser.add_argument(
        "--output_csv",
        default=None,
        help="输出 CSV 路径（默认带时间戳）",
    )
    parser.add_argument(
        "--base_url",
        default=os.environ.get("WILDGUARD_API_ENDPOINT", "http://s-20251119153749-lp69w-decode.ailab-safethm.svc:23344/v1"),
        help="Qwen3Guard API base_url",
    )
    parser.add_argument(
        "--api_key",
        default=os.environ.get("WILDGUARD_API_KEY", "FAKE_API_KEY"),
        help="Qwen3Guard API key",
    )
    parser.add_argument(
        "--model",
        default="orm",
        help="模型名",
    )
    parser.add_argument("--timeout", type=int, default=30, help="单次请求超时（秒）")
    parser.add_argument("--max_retries", type=int, default=3, help="重试次数")
    parser.add_argument("--sleep", type=float, default=0.0, help="每条请求间隔（秒）")
    parser.add_argument("--start", type=int, default=0, help="起始行索引")
    parser.add_argument("--limit", type=int, default=-1, help="最多处理条数（-1 为全部）")

    args = parser.parse_args()

    if args.output_csv is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output_csv = os.path.join(
            "/mnt/shared-storage-user/wenxiaoyu/game-private/eval/safety-eval-fork/results",
            f"or_bench-hard-1k-qwen3guard-{ts}.csv",
        )

    os.makedirs(os.path.dirname(args.output_csv), exist_ok=True)

    with open(args.input_csv, newline="", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        if "prompt" not in reader.fieldnames:
            raise ValueError("输入 CSV 缺少 prompt 列")

        rows = list(reader)

    if args.start < 0:
        raise ValueError("--start 不能小于 0")
    if args.limit == 0:
        print("limit=0，未处理任何样本")
        return

    end = len(rows) if args.limit < 0 else min(len(rows), args.start + args.limit)
    rows = rows[args.start:end]

    out_fields = [
        "index",
        "prompt",
        "category",
        "qwen3guard_raw",
        "prompt_harmfulness",
        "response_harmfulness",
        "response_refusal",
        "is_parsing_error",
    ]

    with open(args.output_csv, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=out_fields)
        writer.writeheader()

        for i, row in enumerate(rows, start=args.start):
            prompt = row.get("prompt", "")
            category = row.get("category", "")

            try:
                raw = call_qwen3guard(
                    prompt=prompt,
                    base_url=args.base_url,
                    api_key=args.api_key,
                    model=args.model,
                    timeout=args.timeout,
                    max_retries=args.max_retries,
                )
                prompt_h, resp_h, resp_ref, parse_err = parse_qwen3guard_output(raw)
                out_row = {
                    "index": i,
                    "prompt": prompt,
                    "category": category,
                    "qwen3guard_raw": raw,
                    "prompt_harmfulness": prompt_h,
                    "response_harmfulness": resp_h,
                    "response_refusal": resp_ref,
                    "is_parsing_error": parse_err,
                }
            except Exception as e:
                out_row = {
                    "index": i,
                    "prompt": prompt,
                    "category": category,
                    "qwen3guard_raw": "",
                    "prompt_harmfulness": None,
                    "response_harmfulness": None,
                    "response_refusal": None,
                    "is_parsing_error": True,
                }
                sys.stderr.write(f"[ERROR] index={i} 调用失败: {e}\n")

            writer.writerow(out_row)
            f_out.flush()

            if args.sleep > 0:
                time.sleep(args.sleep)

    print(f"已保存结果: {args.output_csv}")


if __name__ == "__main__":
    main()
