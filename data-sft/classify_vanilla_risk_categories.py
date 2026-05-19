### dace: classify vanilla prompts (last N of benign/harmful origin jsonl) with locally-deployed Llama-Guard-4 prompt-assessment to build a per-sample risk-category index for rare-slot supplementation ###
"""
Classify the `vanilla` field of the last N samples of:
  - data-sft/vanilla_benign_dataset_origin.jsonl
  - data-sft/vanilla_harmful_dataset_origin.jsonl
using a locally-deployed Llama-Guard-4 OpenAI-compatible endpoint in
Prompt-Assessment mode (single user turn).

Sync loop + tqdm (mirrors scripts/check_benign_data_quality.py style).

Outputs per-sample JSONL (resumable) and a summary JSON under
  data-sft/risk_category_stats/

Run:
  cd /mnt/shared-storage-user/yupeng/MAGIC
  conda activate magic
  python data-sft/classify_vanilla_risk_categories.py            # both files, tail 20000
  python data-sft/classify_vanilla_risk_categories.py --stats-only
"""

import argparse
import json
import os
from collections import Counter
from pathlib import Path

from openai import OpenAI
from tqdm import tqdm


### dace: hardcoded local Guard endpoint (kept inline per user instruction) ###
GUARD_BASE_URL = "http://s-20260502121717-vtcm2-decode.ailab-safethm.svc:28618/v1"
GUARD_API_KEY = "{{FAKE_API_KEY}}"
GUARD_MODEL = "orm"


### dace: S1-S14 → short name mapping as specified by user; used to annotate guard categories ###
RISK_CODE_TO_NAME: dict[str, str] = {
    "S1": "Violent Crimes",
    "S2": "Non-Violent Crimes",
    "S3": "Sex Crimes",
    "S4": "Child Exploitation",
    "S5": "Defamation",
    "S6": "Specialized Advice",
    "S7": "Privacy",
    "S8": "Intellectual Property",
    "S9": "Indiscriminate Weapons",
    "S10": "Hate",
    "S11": "Self-Harm",
    "S12": "Sexual Content",
    "S13": "Elections",
    "S14": "Code Interpreter Abuse",
}


DATASETS = {
    "benign": {
        "input":  Path("data-sft/vanilla_benign_dataset_origin.jsonl"),
        "output": Path("data-sft/risk_category_stats/vanilla_benign_last20k_guard.jsonl"),
        "summary": Path("data-sft/risk_category_stats/vanilla_benign_last20k_summary.json"),
    },
    "harmful": {
        "input":  Path("data-sft/vanilla_harmful_dataset_origin.jsonl"),
        "output": Path("data-sft/risk_category_stats/vanilla_harmful_last20k_guard.jsonl"),
        "summary": Path("data-sft/risk_category_stats/vanilla_harmful_last20k_summary.json"),
    },
}


def load_tail_vanilla(input_path: Path, tail_n: int) -> list[dict]:
    """Load the last `tail_n` lines and keep (idx_global, vanilla). idx_global is the 0-based index in the full file so later re-sampling can reference the original dataset directly."""
    with input_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    total = len(lines)
    start = max(0, total - tail_n)
    records: list[dict] = []
    for idx_global in range(start, total):
        raw = lines[idx_global].strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        vanilla = obj.get("vanilla")
        if not isinstance(vanilla, str):
            continue
        records.append({"idx": idx_global, "vanilla": vanilla})
    return records


def load_done(out_path: Path) -> set[int]:
    done: set[int] = set()
    if not out_path.exists():
        return done
    with out_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if "idx" in obj:
                    done.add(int(obj["idx"]))
            except Exception:
                continue
    return done


def parse_guard_output(text: str) -> tuple[str, list[str]]:
    """Parse LG4 prompt/response-assessment output.
    Expected shapes:
        "safe"
        "unsafe\nS2"
        "unsafe\nS3,S10"
    Tolerate leading whitespace/newlines and case.
    Returns (safety_label, [risk_codes])."""
    if not text:
        return "unknown", []
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    if not lines:
        return "unknown", []
    label = lines[0].lower()
    if label not in {"safe", "unsafe"}:
        for ln in lines:
            low = ln.lower()
            if low in {"safe", "unsafe"}:
                label = low
                break
            if low.startswith("safety:"):
                label = low.split(":", 1)[1].strip()
                break
    codes: list[str] = []
    if label == "unsafe":
        for ln in lines[1:]:
            for tok in ln.replace(" ", "").split(","):
                tok = tok.upper().strip()
                if tok.startswith("S") and tok[1:].isdigit():
                    if tok not in codes:
                        codes.append(tok)
    return label, codes


def names_for_codes(codes: list[str]) -> list[str]:
    return [RISK_CODE_TO_NAME.get(c, c) for c in codes]


def build_client() -> OpenAI:
    for _var in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"]:
        os.environ.pop(_var, None)
    return OpenAI(base_url=GUARD_BASE_URL, api_key=GUARD_API_KEY)


def aggregate_summary(out_path: Path) -> dict:
    safety_counter: Counter[str] = Counter()
    code_primary: Counter[str] = Counter()
    code_any: Counter[str] = Counter()
    total = 0
    multi_label = 0
    safe_count = 0
    unknown_count = 0
    with out_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            total += 1
            safety = obj.get("safety", "unknown")
            codes = obj.get("risk_codes") or []
            safety_counter[safety] += 1
            if safety == "unsafe":
                if codes:
                    code_primary[codes[0]] += 1
                    if len(codes) > 1:
                        multi_label += 1
                for c in codes:
                    code_any[c] += 1
            elif safety == "safe":
                safe_count += 1
            else:
                unknown_count += 1

    ordered_codes = [f"S{i}" for i in range(1, 15)]
    return {
        "total_classified": total,
        "safety_distribution": dict(safety_counter),
        "unsafe_multi_label_samples": multi_label,
        "risk_primary_by_code": {c: code_primary.get(c, 0) for c in ordered_codes},
        "risk_primary_by_name": {RISK_CODE_TO_NAME[c]: code_primary.get(c, 0) for c in ordered_codes},
        "risk_any_by_code": {c: code_any.get(c, 0) for c in ordered_codes},
        "risk_any_by_name": {RISK_CODE_TO_NAME[c]: code_any.get(c, 0) for c in ordered_codes},
        "safe_sample_count": safe_count,
        "unknown_or_error_sample_count": unknown_count,
    }


def process_dataset(name: str, tail_n: int, stats_only: bool) -> None:
    cfg = DATASETS[name]
    input_path: Path = cfg["input"]
    out_path: Path = cfg["output"]
    summary_path: Path = cfg["summary"]
    out_path.parent.mkdir(parents=True, exist_ok=True)

    records = load_tail_vanilla(input_path, tail_n)
    print(f"\n{'='*60}\nDataset: {name}")
    print(f"Input : {input_path} (tail {tail_n} → {len(records)} samples, idx {records[0]['idx']}..{records[-1]['idx']})")
    print(f"Out   : {out_path}")

    if not stats_only:
        done = load_done(out_path)
        remaining = [r for r in records if r["idx"] not in done]
        print(f"Already cached: {len(done)} / {len(records)}   Remaining: {len(remaining)}")

        if remaining:
            client = build_client()
            with out_path.open("a", encoding="utf-8") as f:
                for r in tqdm(remaining, desc=name):
                    vanilla = r["vanilla"]
                    try:
                        completion = client.chat.completions.create(
                            model=GUARD_MODEL,
                            messages=[{"role": "user", "content": vanilla}],
                        )
                        raw = completion.choices[0].message.content or ""
                        safety, codes = parse_guard_output(raw)
                        item = {
                            "idx": r["idx"],
                            "vanilla": vanilla,
                            "safety": safety,
                            "risk_codes": codes,
                            "risk_names": names_for_codes(codes),
                            "raw": raw,
                            "error": None,
                        }
                    except Exception as e:
                        item = {
                            "idx": r["idx"],
                            "vanilla": vanilla,
                            "safety": "error",
                            "risk_codes": [],
                            "risk_names": [],
                            "raw": "",
                            "error": f"{type(e).__name__}: {e}",
                        }
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")
                    f.flush()

    summary = aggregate_summary(out_path)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n--- Summary [{name}] ---")
    print(f"total_classified: {summary['total_classified']}")
    print(f"safety         : {summary['safety_distribution']}")
    print(f"risk_primary   :")
    for code in [f"S{i}" for i in range(1, 15)]:
        n = summary["risk_primary_by_code"].get(code, 0)
        print(f"  {code:>3}  {RISK_CODE_TO_NAME[code]:<25} {n}")
    print(f"Summary written to {summary_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=list(DATASETS.keys()) + ["all"], default="all")
    parser.add_argument("--tail", type=int, default=20000, help="Number of tail samples to classify per file.")
    parser.add_argument("--stats-only", action="store_true", help="Skip API calls; only aggregate existing cache.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    os.chdir(repo_root)

    names = list(DATASETS.keys()) if args.dataset == "all" else [args.dataset]
    for n in names:
        process_dataset(n, args.tail, args.stats_only)


if __name__ == "__main__":
    main()
