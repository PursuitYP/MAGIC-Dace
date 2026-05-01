"""
Check the actual safety of rewritten prompts in SFT benign JSON files
using the guard API. Supports resume via a temp JSONL cache file.
"""

import argparse
import json
import os
from pathlib import Path

from openai import OpenAI
from tqdm import tqdm

base_url = "http://s-20251119153749-lp69w-decode.ailab-safethm.svc:23344/v1"
api_key = '{{FAKE_API_KEY}}'

DATA_FILES = {
    "magic": "src/360-LLaMA-Factory/data/game_cot_benign.json",
    "dace":  "src/360-LLaMA-Factory/data/game_cot_dace_v1nv2_v3_benign.json",
}

CACHE_DIR = Path("scripts/check_benign_cache")


def parse_guard_response(text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line.lower().startswith("safety:"):
            return line.split(":", 1)[1].strip().lower()
    return "unknown"


def load_cache(cache_path: Path) -> dict:
    results = {}
    if cache_path.exists():
        with open(cache_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    results[entry["idx"]] = entry["result"]
                except Exception:
                    pass
    return results


def process_dataset(name: str, data_path: str, stats_only: bool):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / f"{name}_results.jsonl"

    with open(data_path) as f:
        data = json.load(f)

    total = len(data)
    print(f"\n{'='*60}")
    print(f"Dataset: {name}  ({total} entries)")
    print(f"Cache:   {cache_path}")

    cached = load_cache(cache_path)
    print(f"Already cached: {len(cached)} / {total}")

    if not stats_only:
        # clear proxy env vars so the internal guard API is reached directly
        for _var in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"]:
            os.environ.pop(_var, None)

        client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )

        todo = [i for i in range(total) if i not in cached]
        print(f"Remaining to check: {len(todo)}")

        with open(cache_path, "a") as cache_f:
            for idx in tqdm(todo, desc=name):
                answer = data[idx].get("answer", "")
                try:
                    messages = [{"role": "user", "content": answer}]
                    completion = client.chat.completions.create(
                        model="orm",
                        messages=messages,
                    )
                    text = completion.choices[0].message.content
                    result = parse_guard_response(text)
                except Exception as e:
                    result = f"error:{e}"
                cached[idx] = result
                cache_f.write(json.dumps({"idx": idx, "result": result}) + "\n")
                cache_f.flush()

    counts = {"safe": 0, "unsafe": 0, "controversial": 0, "unknown": 0, "error": 0}
    for i in range(total):
        r = cached.get(i, "missing")
        if r == "safe":
            counts["safe"] += 1
        elif r == "unsafe":
            counts["unsafe"] += 1
        elif r == "controversial":
            counts["controversial"] += 1
        elif r and r.startswith("error"):
            counts["error"] += 1
        else:
            counts["unknown"] += 1

    covered = counts["safe"] + counts["unsafe"] + counts["controversial"]
    not_safe = counts["unsafe"] + counts["controversial"]
    print(f"\n--- Results for [{name}] ---")
    print(f"Total entries       : {total}")
    print(f"Checked             : {covered}  ({100*covered/total:.1f}%)")
    print(f"  Safe (benign)     : {counts['safe']}  ({100*counts['safe']/total:.1f}%)")
    print(f"  Unsafe (harmful)  : {counts['unsafe']}  ({100*counts['unsafe']/total:.1f}%)")
    print(f"  Controversial     : {counts['controversial']}  ({100*counts['controversial']/total:.1f}%)")
    if counts["error"]:
        print(f"  API errors        : {counts['error']}")
    if counts["unknown"]:
        print(f"  Unknown/miss      : {counts['unknown']}")
    if covered > 0:
        print(f"  Not-safe rate (of checked): {100*not_safe/covered:.1f}%  (unsafe+controversial)")

    return counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stats-only", action="store_true",
                        help="Only compute stats from existing cache, no API calls")
    parser.add_argument("--dataset", choices=list(DATA_FILES.keys()) + ["all"], default="all",
                        help="Which dataset to process")
    args = parser.parse_args()

    datasets = list(DATA_FILES.items()) if args.dataset == "all" else [(args.dataset, DATA_FILES[args.dataset])]

    repo_root = Path(__file__).parent.parent
    os.chdir(repo_root)

    for name, path in datasets:
        if not Path(path).exists():
            print(f"ERROR: {path} not found, skipping.")
            continue
        process_dataset(name, path, args.stats_only)

    print("\nDone.")


if __name__ == "__main__":
    main()

# python3 scripts/check_benign_data_quality.py
