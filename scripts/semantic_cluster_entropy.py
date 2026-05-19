### dace: Semantic Cluster H over pooled embeddings — single KMeans, per-source entropy ###
"""
Computes the "Semantic Cluster H" diversity metric for the three sources:
  - dace_history
  - magic_history
  - dace_replay_pool

Protocol (following the reviewer note / reference in conversation):
  1. Pool the L2-normalized embeddings from all sources
     (text-embedding-3-small, cached at scripts/similarity_stats/<tag>/embeddings.npy
     from embed_and_similarity.py).
  2. Fit ONE MiniBatchKMeans on the pooled set.
  3. For each source, compute normalized cluster-label entropy:
         H_sem = -sum_k p_k log p_k     ,   H_sem_norm = H_sem / log(K)
     where p_k is the fraction of that source's samples assigned to cluster k.

Defaults: K=30 (main), also reports K=20 and K=50 as sensitivity.
Equal-size subsampling to min(N) is reported alongside the full-N numbers.

Usage:
  conda activate magic
  python scripts/semantic_cluster_entropy.py
  python scripts/semantic_cluster_entropy.py --K 30 --subsample 3840 --seed 0
"""

import argparse
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.cluster import MiniBatchKMeans


SCRIPT_DIR = Path(__file__).resolve().parent
SIM_ROOT = SCRIPT_DIR / "similarity_stats"
OUT_DIR = SCRIPT_DIR / "semantic_cluster_stats"

SOURCES = ["dace_history", "magic_history", "dace_replay_pool"]


def load_embeddings(tag: str) -> np.ndarray:
    p = SIM_ROOT / tag / "embeddings.npy"
    if not p.exists():
        raise FileNotFoundError(
            f"Missing cached embeddings for {tag} at {p}.\n"
            f"Run: python scripts/embed_and_similarity.py --sources {tag}"
        )
    arr = np.load(p)
    # Defensive re-normalize in case the cache was not normalized
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return (arr / norms).astype(np.float32)


def normalized_entropy(labels: np.ndarray, K: int) -> tuple[float, float]:
    counts = Counter(labels.tolist())
    p = np.array([counts.get(k, 0) for k in range(K)], dtype=np.float64)
    p = p / p.sum()
    nz = p[p > 0]
    H = float(-(nz * np.log(nz)).sum())
    return H, H / math.log(K)


def cluster_H_for_K(pooled: np.ndarray, spans: dict[str, tuple[int, int]], K: int,
                    seed: int) -> dict:
    km = MiniBatchKMeans(
        n_clusters=K,
        batch_size=8192,
        n_init=1,
        init="k-means++",
        random_state=seed,
        max_iter=50,
        max_no_improvement=10,
        reassignment_ratio=0.01,
    )
    labels = km.fit_predict(pooled)

    out = {"K": K, "per_source": {}, "pooled": {}}
    for tag, (s, e) in spans.items():
        H, Hn = normalized_entropy(labels[s:e], K)
        occ = int(np.unique(labels[s:e]).size)
        out["per_source"][tag] = {
            "N": e - s,
            "H_sem_nats": H,
            "H_sem_norm": Hn,
            "clusters_occupied": occ,
            "coverage_frac": occ / K,
        }
    # Pooled (reference)
    H_all, Hn_all = normalized_entropy(labels, K)
    out["pooled"] = {
        "N": pooled.shape[0],
        "H_sem_nats": H_all,
        "H_sem_norm": Hn_all,
        "clusters_occupied": int(np.unique(labels).size),
    }
    return out


def run_protocol(subsample: int | None, seed: int, K_list: list[int]) -> dict:
    # Load embeddings
    embs = {tag: load_embeddings(tag) for tag in SOURCES}
    sizes_full = {t: e.shape[0] for t, e in embs.items()}
    print(f"[sizes] full: {sizes_full}")

    # Optional equal-size subsample
    rng = np.random.default_rng(seed)
    used = {}
    for tag, arr in embs.items():
        if subsample is not None and arr.shape[0] > subsample:
            idx = rng.choice(arr.shape[0], size=subsample, replace=False)
            used[tag] = arr[idx]
        else:
            used[tag] = arr
    sizes_used = {t: e.shape[0] for t, e in used.items()}
    print(f"[sizes] used: {sizes_used}")

    # Pool and remember spans
    pooled_chunks = []
    spans: dict[str, tuple[int, int]] = {}
    offset = 0
    for tag in SOURCES:
        n = used[tag].shape[0]
        spans[tag] = (offset, offset + n)
        pooled_chunks.append(used[tag])
        offset += n
    pooled = np.concatenate(pooled_chunks, axis=0)
    print(f"[pooled] shape={pooled.shape}")

    report = {
        "subsample": subsample,
        "seed": seed,
        "sizes_full": sizes_full,
        "sizes_used": sizes_used,
        "by_K": {},
    }
    for K in K_list:
        r = cluster_H_for_K(pooled, spans, K=K, seed=seed)
        report["by_K"][str(K)] = r
        print(f"\n===== K={K} =====")
        for tag, d in r["per_source"].items():
            print(f"[{tag:<18}] N={d['N']}  H={d['H_sem_nats']:.4f}  "
                  f"H_norm={d['H_sem_norm']:.4f}  "
                  f"clusters_occupied={d['clusters_occupied']}/{K}")
        p = r["pooled"]
        print(f"[pooled           ] N={p['N']}  H={p['H_sem_nats']:.4f}  "
              f"H_norm={p['H_sem_norm']:.4f}  clusters_occupied={p['clusters_occupied']}/{K}")
    return report


def build_parser():
    p = argparse.ArgumentParser()
    p.add_argument("--K", type=int, default=30,
                   help="Main K for Semantic Cluster H (default 30).")
    p.add_argument("--K-sensitivity", type=int, nargs="+", default=[20, 30, 50],
                   help="All K values to run (default: 20 30 50).")
    p.add_argument("--subsample", type=int, default=None,
                   help="Optional equal-size subsample per source (e.g. 3840).")
    p.add_argument("--seed", type=int, default=0)
    return p


def main():
    args = build_parser().parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    K_list = sorted(set(args.K_sensitivity) | {args.K})

    # Run once with full sizes
    print("\n######## Full-size protocol ########")
    full_report = run_protocol(subsample=None, seed=args.seed, K_list=K_list)
    (OUT_DIR / "semantic_cluster_entropy_full.json").write_text(
        json.dumps(full_report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Run once with equal-size subsample (default: min N across the three sources)
    sizes_full = full_report["sizes_full"]
    sub_n = args.subsample if args.subsample is not None else min(sizes_full.values())
    print(f"\n######## Equal-size protocol (N={sub_n} per source) ########")
    sub_report = run_protocol(subsample=sub_n, seed=args.seed, K_list=K_list)
    (OUT_DIR / f"semantic_cluster_entropy_sub{sub_n}.json").write_text(
        json.dumps(sub_report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"\nreports written under: {OUT_DIR}")


if __name__ == "__main__":
    main()
