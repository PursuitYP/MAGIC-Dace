### dace: diversity metrics (self-BLEU, distinct-n, n-gram entropy) over rewrite_prompts ###
"""
Computes n-gram based diversity metrics on the three jsonl files:
  - scripts/dace_history.jsonl
  - scripts/magic_history.jsonl
  - scripts/dace_replay_pool.jsonl

Metrics:
  - self-BLEU for n=1..5   (Zhu et al. 2018, Texygen; headline is usually BLEU-4)
  - distinct-n for n=1..4  (Li et al. 2016)
  - n-gram entropy (nats) for n=1..4

Tokenization is lowercase + alphanumeric word pieces — standard for diversity metrics.

Tradeoff note: self-BLEU is O(K * |hyp_ngrams| * N) in the naive impl. This
script uses a top-1/top-2 precompute across the full corpus so each hypothesis's
max-ref-count lookup is O(|hyp_ngrams|), keeping the full run under a minute
per source even with K=1000. No smoothing is applied to p_n; a 0-count BLEU
reports 0 (matches Texygen's convention). Brevity penalty is omitted (standard
simplification for self-BLEU on same-corpus hypotheses).

Usage:
  conda activate magic
  python scripts/diversity_metrics.py                  # all three
  python scripts/diversity_metrics.py --self-bleu-k 1000
  python scripts/diversity_metrics.py --sources dace_history
"""

import argparse
import json
import math
import os
import random
import re
from collections import Counter
from pathlib import Path

from tqdm import tqdm


SCRIPT_DIR = Path(__file__).resolve().parent

SOURCES = {
    "dace_history":     SCRIPT_DIR / "dace_history.jsonl",
    "magic_history":    SCRIPT_DIR / "magic_history.jsonl",
    "dace_replay_pool": SCRIPT_DIR / "dace_replay_pool.jsonl",
}

MAX_BLEU_N = 5        # report BLEU-1..BLEU-5
MAX_DISTINCT_N = 4    # distinct-1..4
MAX_ENTROPY_N = 4     # H_1..H_4

_WORD_RE = re.compile(r"[a-zA-Z0-9]+")


def tokenize(text: str) -> list[str]:
    return _WORD_RE.findall(text.lower())


def load_prompts(path: Path) -> list[str]:
    out: list[str] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            p = json.loads(line).get("rewrite_prompt")
            if not isinstance(p, str):
                raise ValueError(f"non-string rewrite_prompt in {path}")
            out.append(p)
    return out


def ngrams(tokens: list[str], n: int):
    """Generator of n-gram tuples (no allocation of an intermediate list)."""
    if len(tokens) < n:
        return
    for i in range(len(tokens) - n + 1):
        yield tuple(tokens[i : i + n])


def distinct_and_entropy(token_lists: list[list[str]], n: int) -> tuple[float, float, int, int]:
    """Return (distinct_n, H_n_nats, unique_ngrams, total_ngrams) over the whole corpus."""
    c: Counter = Counter()
    for toks in token_lists:
        for g in ngrams(toks, n):
            c[g] += 1
    total = sum(c.values())
    if total == 0:
        return 0.0, 0.0, 0, 0
    unique = len(c)
    distinct = unique / total
    H = 0.0
    for cnt in c.values():
        p = cnt / total
        H -= p * math.log(p)
    return distinct, H, unique, total


def self_bleu(
    token_lists: list[list[str]],
    max_n: int,
    k_hyps: int,
    seed: int,
) -> dict[str, float]:
    """Mean self-BLEU for n=1..max_n over k_hyps randomly-sampled hypotheses.

    For each sampled hypothesis i:
        p_n(i) = sum_g min(count_g_in_hyp, max_count_g_across_refs_excluding_i)
                 / sum_g count_g_in_hyp
        BLEU_n(i) = exp(mean over 1..n of log p_n(i))   (0 if any p_n==0)

    The top-1/top-2 trick avoids rescanning all references per hypothesis.
    """
    N = len(token_lists)
    if N < 2:
        return {f"bleu-{n}": 0.0 for n in range(1, max_n + 1)}

    # Per-sample n-gram Counters, for each n
    per_sample_counters: list[list[Counter]] = []
    for n in range(1, max_n + 1):
        per_sample_counters.append(
            [Counter(ngrams(toks, n)) for toks in token_lists]
        )

    # Per n-gram: (top1_count, top1_idx, top2_count) across the full corpus.
    # For a hypothesis i, max_ref_count(g) = top1_count if top1_idx != i else top2_count.
    per_ngram_top: list[dict[tuple, list[int]]] = [dict() for _ in range(max_n)]
    for n_idx in range(max_n):
        table = per_ngram_top[n_idx]
        for i, counter in enumerate(per_sample_counters[n_idx]):
            for g, cnt in counter.items():
                top = table.get(g)
                if top is None:
                    table[g] = [cnt, i, 0]
                else:
                    if cnt > top[0]:
                        top[2] = top[0]
                        top[0] = cnt
                        top[1] = i
                    elif cnt > top[2]:
                        top[2] = cnt

    rng = random.Random(seed)
    k = min(k_hyps, N)
    sampled = rng.sample(range(N), k)

    # Accumulate BLEU-n per sampled hyp
    scores = {n: [] for n in range(1, max_n + 1)}
    for i in tqdm(sampled, desc="self-BLEU", leave=False):
        log_p = []
        zero_hit = False
        for n_idx in range(max_n):
            hyp_c = per_sample_counters[n_idx][i]
            total_h = sum(hyp_c.values())
            if total_h == 0:
                zero_hit = True
                log_p.append(float("-inf"))
                continue
            clipped = 0
            table = per_ngram_top[n_idx]
            for g, c in hyp_c.items():
                top = table.get(g)
                if top is None:
                    max_ref = 0
                else:
                    max_ref = top[0] if top[1] != i else top[2]
                if max_ref:
                    clipped += c if c <= max_ref else max_ref
            if clipped == 0:
                zero_hit = True
                log_p.append(float("-inf"))
            else:
                log_p.append(math.log(clipped / total_h))
            # cumulative BLEU-(n_idx+1)
            n = n_idx + 1
            if any(math.isinf(x) for x in log_p[:n]):
                scores[n].append(0.0)
            else:
                scores[n].append(math.exp(sum(log_p[:n]) / n))
            if zero_hit:
                for m in range(n + 1, max_n + 1):
                    scores[m].append(0.0)
                break

    return {f"bleu-{n}": (sum(scores[n]) / len(scores[n])) if scores[n] else 0.0
            for n in range(1, max_n + 1)}


def analyze_source(tag: str, path: Path, k_hyps: int, seed: int) -> dict:
    prompts = load_prompts(path)
    toks_list = [tokenize(p) for p in prompts]
    lens = [len(t) for t in toks_list]
    result = {
        "tag": tag,
        "N": len(prompts),
        "avg_tokens": sum(lens) / len(lens) if lens else 0.0,
        "total_tokens": sum(lens),
        "distinct_n": {},
        "ngram_entropy_nats": {},
        "ngram_unique_counts": {},
        "ngram_total_counts": {},
        "self_bleu": {},
        "self_bleu_k_hyps": min(k_hyps, len(prompts)),
    }

    # distinct-n and entropy
    for n in range(1, max(MAX_DISTINCT_N, MAX_ENTROPY_N) + 1):
        d, H, uniq, tot = distinct_and_entropy(toks_list, n)
        if n <= MAX_DISTINCT_N:
            result["distinct_n"][str(n)] = d
        if n <= MAX_ENTROPY_N:
            result["ngram_entropy_nats"][str(n)] = H
        result["ngram_unique_counts"][str(n)] = uniq
        result["ngram_total_counts"][str(n)] = tot

    # self-BLEU
    result["self_bleu"] = self_bleu(toks_list, MAX_BLEU_N, k_hyps, seed)
    return result


def pretty(res: dict):
    print(f"\n===== [{res['tag']}] =====")
    print(f"  N={res['N']}  avg_tokens={res['avg_tokens']:.1f}  total_tokens={res['total_tokens']}")
    print(f"  self-BLEU (k={res['self_bleu_k_hyps']} sampled hypotheses):")
    for k, v in res["self_bleu"].items():
        print(f"    {k}: {v:.4f}")
    print(f"  distinct-n:")
    for k, v in res["distinct_n"].items():
        uniq = res["ngram_unique_counts"][k]
        tot = res["ngram_total_counts"][k]
        print(f"    n={k}: {v:.4f}  (unique={uniq}, total={tot})")
    print(f"  n-gram entropy (nats):")
    for k, v in res["ngram_entropy_nats"].items():
        uniq = res["ngram_unique_counts"][k]
        print(f"    n={k}: H={v:.4f}  (ln(unique={uniq})={math.log(uniq) if uniq else 0:.4f})")


def build_parser():
    p = argparse.ArgumentParser()
    p.add_argument("--sources", nargs="+", default=list(SOURCES.keys()),
                   choices=list(SOURCES.keys()))
    p.add_argument("--out-root", default=str(SCRIPT_DIR / "diversity_stats"))
    p.add_argument("--self-bleu-k", type=int, default=1000,
                   help="Number of hypotheses to sample for self-BLEU (default 1000).")
    p.add_argument("--seed", type=int, default=0)
    return p


def main():
    args = build_parser().parse_args()
    out_root = Path(args.out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    combined = {}
    for tag in args.sources:
        res = analyze_source(tag, SOURCES[tag], args.self_bleu_k, args.seed)
        combined[tag] = res
        pretty(res)
        sub = out_root / tag
        sub.mkdir(parents=True, exist_ok=True)
        (sub / "diversity.json").write_text(
            json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    (out_root / "diversity_report.json").write_text(
        json.dumps(combined, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nreport: {out_root / 'diversity_report.json'}")


if __name__ == "__main__":
    main()
