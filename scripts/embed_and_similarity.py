### dace: embed rewrite_prompts and compute mean pairwise cosine similarity ###
"""
For the three jsonl files produced by extract_responses_and_prompts.py:
  - scripts/dace_history.jsonl
  - scripts/magic_history.jsonl
  - scripts/dace_replay_pool.jsonl

embed each `rewrite_prompt` with text-embedding-3-small (same OpenAI-compatible
endpoint used by eval-dace/OpenRT/run_eval.sh) and report the mean pairwise
cosine similarity.

Cached embeddings land at:
  scripts/similarity_stats/<tag>/embeddings.npy      (float32, N x 1536, L2-normalized)
  scripts/similarity_stats/<tag>/prompts_sha1.txt    (one sha1 per row, for cache integrity)
  scripts/similarity_stats/<tag>/summary.json        (mean/std/percentiles + cross-source)

Usage:
  conda activate magic
  python scripts/embed_and_similarity.py                   # all three
  python scripts/embed_and_similarity.py --sources dace_history
  python scripts/embed_and_similarity.py --stats-only      # skip API, recompute from cached npy
"""

import argparse
import hashlib
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
from openai import OpenAI
from tqdm import tqdm


SCRIPT_DIR = Path(__file__).resolve().parent

EMBED_BASE_URL = "http://35.220.164.252:3888/v1/"
EMBED_API_KEY = "sk-ua4rD1WerZKpDyb7JHOSKxVvMmvMZIKi6rXGPotdX9nfxNXr"
EMBED_MODEL = "text-embedding-3-small"
EMBED_DIM = 1536

# text-embedding-3-small token limit is 8192; ~4 chars/token for English, so
# 24000 chars leaves plenty of headroom while covering 99%+ of rewrite_prompts.
PROMPT_TRUNCATE_CHARS = 24000

SOURCES = {
    "dace_history":     SCRIPT_DIR / "dace_history.jsonl",
    "magic_history":    SCRIPT_DIR / "magic_history.jsonl",
    "dace_replay_pool": SCRIPT_DIR / "dace_replay_pool.jsonl",
}


def _strip_proxies():
    for v in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"):
        os.environ.pop(v, None)


def build_client() -> OpenAI:
    _strip_proxies()
    return OpenAI(base_url=EMBED_BASE_URL, api_key=EMBED_API_KEY, timeout=60)


def load_prompts(path: Path) -> list[str]:
    prompts: list[str] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            p = obj.get("rewrite_prompt")
            if not isinstance(p, str):
                raise ValueError(f"non-string rewrite_prompt in {path}")
            prompts.append(p)
    return prompts


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


def truncate(p: str) -> str:
    return p if len(p) <= PROMPT_TRUNCATE_CHARS else p[:PROMPT_TRUNCATE_CHARS]


def embed_batch(client: OpenAI, texts: list[str], retries: int = 3) -> np.ndarray:
    """Embed a list of texts; returns (len(texts), EMBED_DIM) float32 array."""
    last_err = None
    for attempt in range(retries):
        try:
            r = client.embeddings.create(model=EMBED_MODEL, input=texts)
            arr = np.array([d.embedding for d in r.data], dtype=np.float32)
            return arr
        except Exception as e:
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"embed_batch failed after {retries} retries: {last_err}")


def embed_source(tag: str, prompts: list[str], out_dir: Path,
                 batch_size: int, max_workers: int) -> np.ndarray:
    out_dir.mkdir(parents=True, exist_ok=True)
    emb_path = out_dir / "embeddings.npy"
    sha_path = out_dir / "prompts_sha1.txt"

    want_sha = [sha1(p) for p in prompts]

    # Try cache
    if emb_path.exists() and sha_path.exists():
        cached_sha = sha_path.read_text().splitlines()
        if cached_sha == want_sha:
            arr = np.load(emb_path)
            if arr.shape == (len(prompts), EMBED_DIM):
                print(f"[{tag}] cache hit: loaded {arr.shape} from {emb_path}")
                return arr
        print(f"[{tag}] cache stale; re-embedding")

    client = build_client()
    N = len(prompts)
    arr = np.zeros((N, EMBED_DIM), dtype=np.float32)

    batches = [(i, [truncate(p) for p in prompts[i : i + batch_size]])
               for i in range(0, N, batch_size)]

    def _do(idx: int, texts: list[str]):
        return idx, embed_batch(client, texts)

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = [ex.submit(_do, i, t) for i, t in batches]
        with tqdm(total=N, desc=f"embed {tag}") as pbar:
            for fut in as_completed(futures):
                i, batch_arr = fut.result()
                arr[i : i + batch_arr.shape[0]] = batch_arr
                pbar.update(batch_arr.shape[0])

    # L2-normalize once so cosine similarity == dot product later.
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    arr = (arr / norms).astype(np.float32)

    np.save(emb_path, arr)
    sha_path.write_text("\n".join(want_sha))
    print(f"[{tag}] saved {arr.shape} -> {emb_path}")
    return arr


def intra_stats(arr: np.ndarray, sample_pairs: int = 200_000, rng_seed: int = 0) -> dict:
    """Mean/std of off-diagonal cosine sim.

    Exact mean is computed via ||sum(E)||^2 — cheap and exact.
    Std is estimated from a random sample of N_SAMPLE off-diagonal pairs so
    we don't need to materialize an NxN matrix (N up to 4000 ~ 64 MB would
    still fit but the sample works fine).
    """
    N, d = arr.shape
    s = arr.sum(axis=0)
    total_sum = float(s @ s)          # sum of all entries of E E^T
    # sum of diagonal = N (L2-normalized)
    off_sum = total_sum - N
    off_count = N * (N - 1)
    mean_off = off_sum / off_count if off_count > 0 else 0.0

    rng = np.random.default_rng(rng_seed)
    K = min(sample_pairs, off_count)
    i = rng.integers(0, N, size=K)
    j = rng.integers(0, N, size=K)
    mask = i != j
    i, j = i[mask], j[mask]
    sims = (arr[i] * arr[j]).sum(axis=1)
    pcts = np.percentile(sims, [5, 25, 50, 75, 95]).tolist()

    return {
        "N": int(N),
        "dim": int(d),
        "mean_pairwise_cosine_exact": mean_off,
        "sampled_pairs": int(len(sims)),
        "std_pairwise_cosine_sampled": float(sims.std()),
        "sampled_percentiles": {"p5": pcts[0], "p25": pcts[1], "p50": pcts[2], "p75": pcts[3], "p95": pcts[4]},
    }


def cross_stats(A: np.ndarray, B: np.ndarray, sample_pairs: int = 200_000, rng_seed: int = 1) -> dict:
    """Mean/std of cosine sim between every prompt in A and every prompt in B."""
    NA, _ = A.shape
    NB, _ = B.shape
    sA = A.sum(axis=0)
    sB = B.sum(axis=0)
    mean_cross = float((sA @ sB) / (NA * NB))

    rng = np.random.default_rng(rng_seed)
    K = min(sample_pairs, NA * NB)
    i = rng.integers(0, NA, size=K)
    j = rng.integers(0, NB, size=K)
    sims = (A[i] * B[j]).sum(axis=1)
    pcts = np.percentile(sims, [5, 25, 50, 75, 95]).tolist()
    return {
        "NA": int(NA), "NB": int(NB),
        "mean_pairwise_cosine_exact": mean_cross,
        "sampled_pairs": int(len(sims)),
        "std_pairwise_cosine_sampled": float(sims.std()),
        "sampled_percentiles": {"p5": pcts[0], "p25": pcts[1], "p50": pcts[2], "p75": pcts[3], "p95": pcts[4]},
    }


def build_parser():
    p = argparse.ArgumentParser()
    p.add_argument("--sources", nargs="+", default=list(SOURCES.keys()),
                   choices=list(SOURCES.keys()))
    p.add_argument("--out-root", default=str(SCRIPT_DIR / "similarity_stats"))
    p.add_argument("--batch-size", type=int, default=128)
    p.add_argument("--max-workers", type=int, default=8)
    p.add_argument("--stats-only", action="store_true",
                   help="Skip API; recompute stats from cached .npy (must exist).")
    return p


def main():
    args = build_parser().parse_args()
    out_root = Path(args.out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    # Embed (or load from cache) each source
    emb: dict[str, np.ndarray] = {}
    for tag in args.sources:
        sub = out_root / tag
        sub.mkdir(parents=True, exist_ok=True)
        prompts = load_prompts(SOURCES[tag])
        if args.stats_only:
            path = sub / "embeddings.npy"
            if not path.exists():
                raise FileNotFoundError(f"[{tag}] --stats-only but no cache at {path}")
            arr = np.load(path)
            print(f"[{tag}] stats-only: loaded {arr.shape} from {path}")
        else:
            arr = embed_source(tag, prompts, sub, args.batch_size, args.max_workers)
        emb[tag] = arr

    # Intra-source stats
    report = {"intra": {}, "cross": {}}
    print("\n===== intra-source mean pairwise cosine similarity =====")
    for tag, arr in emb.items():
        stats = intra_stats(arr)
        report["intra"][tag] = stats
        print(f"[{tag}] N={stats['N']}  mean={stats['mean_pairwise_cosine_exact']:.4f}  "
              f"std~{stats['std_pairwise_cosine_sampled']:.4f}  "
              f"median={stats['sampled_percentiles']['p50']:.4f}  "
              f"p5={stats['sampled_percentiles']['p5']:.4f}  "
              f"p95={stats['sampled_percentiles']['p95']:.4f}")

    # Cross-source stats (only when we have ≥2 sources)
    if len(emb) >= 2:
        print("\n===== cross-source mean pairwise cosine similarity =====")
        tags = list(emb.keys())
        for i in range(len(tags)):
            for j in range(i + 1, len(tags)):
                a, b = tags[i], tags[j]
                stats = cross_stats(emb[a], emb[b])
                report["cross"][f"{a}__vs__{b}"] = stats
                print(f"[{a} vs {b}] mean={stats['mean_pairwise_cosine_exact']:.4f}  "
                      f"std~{stats['std_pairwise_cosine_sampled']:.4f}  "
                      f"median={stats['sampled_percentiles']['p50']:.4f}")

    (out_root / "similarity_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nreport: {out_root / 'similarity_report.json'}")


if __name__ == "__main__":
    main()
