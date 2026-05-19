### dace: analyze archive_pool.json sample distribution (risk x attack style x data_type) ###
"""
Analyze the sample distribution of an archive_pool.json checkpoint produced by
ArchivePool.save (src/verl/verl/separated_trainer/ppo/archive_pool.py).

Outputs:
- Overall pool statistics (size, slot occupancy, coverage entropy, zombie fraction)
- Per-data_type counts (vanilla_harmful vs vanilla_benign)
- Marginal counts of risk categories and attack styles (top / bottom)
- Bayesian posterior summary (mean success rate, trial counts)
- Heatmaps: risk x attack_style for ALL / harmful / benign

Strategy index space follows preprocess_dace.py / archive_pool.py:
  RISK_CATEGORIES has 12 entries, ATTACK_STYLES has 10 entries (v4: pruned S12 Sexual Content + S14 Code Interpreter Abuse).

Usage:
  # Pass a file directly:
  python scripts/analyze_archive_pool.py \
      --pool /path/to/global_step_300/archive_pool.json

  # Or pass a checkpoint directory (auto-locates archive_pool.json inside):
  python scripts/analyze_archive_pool.py \
      --pool /path/to/global_step_300

  # Or pass an experiment root + --step N (resolves global_step_N/archive_pool.json);
  # if --step is omitted, the latest global_step_* subdir is picked automatically:
  python scripts/analyze_archive_pool.py \
      --pool /path/to/Game-separated/DACE-Diversity-... --step 300

  # Default out dir is scripts/archive_pool_analysis/<experiment>__<global_step_N>/
  # so multiple pools stay separated. Override with --out-dir or --tag if needed:
  python scripts/analyze_archive_pool.py --pool ... --out-dir scripts/out
  python scripts/analyze_archive_pool.py --pool ... --tag my_run_step300

Example (the DACE-Diversity run referenced in the original task):
conda activate magic
python scripts/analyze_archive_pool.py \
    --pool /mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/yupeng/ckpt/Game-separated/DACE-Diversity-Qwen2.5_7B_Instruct-w_dace_sft_full-2026-04-26_22-00-31 \
    --step 300

python scripts/analyze_archive_pool.py \
    --pool /mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/yupeng/ckpt/Game-separated/DACE-Diversity-Qwen2.5_7B_Instruct-w_dace_sft_v4-defender1st_2026-05-03_14-47-05 \
    --step 300

python scripts/analyze_archive_pool.py \
    --pool /mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/yupeng/ckpt/Game-separated/DACE-Diversity-Qwen2.5_7B_Instruct-w_dace_sft_v4-2026-05-03_14-30-23 \
    --step 300
"""

import argparse
import json
import math
import os
from collections import Counter

import numpy as np
import matplotlib.pyplot as plt


RISK_CATEGORIES = [
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
    "Elections",
]

ATTACK_STYLES = [
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

N_RISK = len(RISK_CATEGORIES)
N_STYLE = len(ATTACK_STYLES)


def init_matrix():
    return np.zeros((N_RISK, N_STYLE), dtype=np.int64)


def shannon_entropy(counts: np.ndarray) -> float:
    total = counts.sum()
    if total <= 0:
        return 0.0
    p = counts.flatten() / total
    p = p[p > 0]
    return float(-np.sum(p * np.log(p)))


def load_pool(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def collect_matrices(entries):
    matrices = {
        "all": init_matrix(),
        "vanilla_harmful": init_matrix(),
        "vanilla_benign": init_matrix(),
    }
    data_type_counts = Counter()
    bad_strategy = 0
    step_added = []
    successes = []
    failures = []

    for e in entries:
        strat = e.get("strategy")
        dtype = e.get("data_type", "unknown")
        data_type_counts[dtype] += 1
        step_added.append(int(e.get("step_added", 0)))
        successes.append(float(e.get("successes", 0.0)))
        failures.append(float(e.get("failures", 0.0)))
        if not strat or len(strat) != 2:
            bad_strategy += 1
            continue
        r, s = int(strat[0]), int(strat[1])
        if not (0 <= r < N_RISK and 0 <= s < N_STYLE):
            bad_strategy += 1
            continue
        matrices["all"][r, s] += 1
        if dtype in matrices:
            matrices[dtype][r, s] += 1

    return matrices, data_type_counts, bad_strategy, step_added, successes, failures


def print_marginals(matrix, title, k=3):
    total = int(matrix.sum())
    print(f"\n===== {title} =====")
    print(f"total samples: {total}")
    if total == 0:
        return
    n_occupied = int((matrix > 0).sum())
    print(f"slots occupied: {n_occupied}/{N_RISK * N_STYLE}")
    print(f"coverage entropy H(p): {shannon_entropy(matrix):.4f}  "
          f"(max log({N_RISK * N_STYLE})={math.log(N_RISK * N_STYLE):.4f})")

    def _show(axis_label, counts, names):
        order_desc = np.argsort(-counts, kind="stable")
        order_asc = np.argsort(counts, kind="stable")
        width = max(len(n) for n in names)

        print(f"[{axis_label}] top-{k}:")
        for idx in order_desc[:k]:
            c = int(counts[idx])
            pct = 100.0 * c / total
            print(f"  {names[idx]:<{width}}  {c:>6d}  ({pct:5.2f}%)")
        print(f"[{axis_label}] bottom-{k}:")
        for idx in order_asc[:k]:
            c = int(counts[idx])
            pct = 100.0 * c / total
            print(f"  {names[idx]:<{width}}  {c:>6d}  ({pct:5.2f}%)")

    _show("risk category", matrix.sum(axis=1), RISK_CATEGORIES)
    _show("attack style", matrix.sum(axis=0), ATTACK_STYLES)


def plot_heatmap(matrix, title, out_path):
    plt.figure(figsize=(14, 7))
    plt.imshow(matrix, cmap="YlOrRd")
    plt.xticks(range(N_STYLE), ATTACK_STYLES, rotation=45, ha="right")
    plt.yticks(range(N_RISK), RISK_CATEGORIES)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            plt.text(j, i, str(int(matrix[i, j])), ha="center", va="center", fontsize=8)
    plt.title(title)
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()
    print(f"[saved] {out_path}")


def print_posterior_summary(successes, failures, alpha_prior=1.0, beta_prior=1.0):
    if not successes:
        return
    successes = np.array(successes, dtype=np.float64)
    failures = np.array(failures, dtype=np.float64)
    trials = successes + failures
    p_hat = (alpha_prior + successes) / (alpha_prior + successes + beta_prior + failures)

    print(f"\n===== Bayesian posterior summary =====")
    print(f"trials  -- mean: {trials.mean():.2f}, median: {np.median(trials):.2f}, "
          f"max: {trials.max():.2f}, zero-trial fraction: {(trials == 0).mean():.3f}")
    print(f"p_hat   -- mean: {p_hat.mean():.4f}, median: {np.median(p_hat):.4f}, "
          f"min: {p_hat.min():.4f}, max: {p_hat.max():.4f}")
    print(f"successes (raw, decayed) -- mean: {successes.mean():.3f}, max: {successes.max():.3f}")
    print(f"failures  (raw, decayed) -- mean: {failures.mean():.3f}, max: {failures.max():.3f}")


def print_step_added_summary(step_added):
    if not step_added:
        return
    arr = np.array(step_added, dtype=np.int64)
    print(f"\n===== step_added summary =====")
    print(f"min: {arr.min()}, max: {arr.max()}, mean: {arr.mean():.1f}, "
          f"median: {int(np.median(arr))}")


### dace: resolve --pool input to a concrete archive_pool.json file ###
def resolve_pool_path(pool_arg: str, step: int = None) -> str:
    """Accept a file, a global_step_N dir, or an experiment root (+ --step N)."""
    p = os.path.abspath(pool_arg)
    if os.path.isfile(p):
        return p
    if os.path.isdir(p):
        # Direct hit: <dir>/archive_pool.json
        candidate = os.path.join(p, "archive_pool.json")
        if os.path.isfile(candidate):
            return candidate
        # Experiment root + --step N -> <root>/global_step_N/archive_pool.json
        if step is not None:
            candidate = os.path.join(p, f"global_step_{step}", "archive_pool.json")
            if os.path.isfile(candidate):
                return candidate
        # Otherwise, fall back to picking the latest global_step_* subdir
        steps = []
        for name in os.listdir(p):
            if name.startswith("global_step_"):
                try:
                    steps.append((int(name.split("_")[-1]), name))
                except ValueError:
                    continue
        if steps:
            steps.sort()
            latest = steps[-1][1]
            candidate = os.path.join(p, latest, "archive_pool.json")
            if os.path.isfile(candidate):
                print(f"[info] --step not given; picked latest checkpoint: {latest}")
                return candidate
    raise FileNotFoundError(
        f"Could not locate archive_pool.json from --pool={pool_arg}"
        + (f" --step={step}" if step is not None else "")
    )


### dace: derive a unique pool tag from the resolved file path for output dir naming ###
def derive_pool_tag(pool_path: str) -> str:
    """Build a tag like '<experiment_name>__<global_step_N>' from the archive_pool.json path.

    Falls back to the parent dir name if the path layout is unexpected.
    """
    abs_path = os.path.abspath(pool_path)
    step_dir = os.path.basename(os.path.dirname(abs_path))           # e.g. global_step_300
    exp_dir = os.path.basename(os.path.dirname(os.path.dirname(abs_path)))  # e.g. DACE-Diversity-...
    if step_dir.startswith("global_step_") and exp_dir:
        return f"{exp_dir}__{step_dir}"
    return step_dir or "archive_pool"


def build_parser():
    parser = argparse.ArgumentParser(
        description="Analyze sample distribution of an archive_pool.json checkpoint."
    )
    parser.add_argument(
        "--pool", required=True,
        help="Path to archive_pool.json, a global_step_N dir, or an experiment root.",
    )
    parser.add_argument(
        "--step", type=int, default=None,
        help="When --pool is an experiment root, pick global_step_<STEP>/archive_pool.json.",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help=(
            "Directory to save heatmap PNGs. "
            "Default: scripts/archive_pool_analysis/<experiment>__<global_step_N>/."
        ),
    )
    parser.add_argument(
        "--tag", default=None,
        help="Optional override for the auto-derived pool tag (used in default out-dir).",
    )
    parser.add_argument("--top-k", type=int, default=3,
                        help="Top/bottom-k for marginal printout (default: 3).")
    return parser


### dace: results land in scripts/archive_pool_analysis/<pool_tag>/ to keep different pools separated ###
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    args = build_parser().parse_args()
    pool_path = resolve_pool_path(args.pool, args.step)
    pool_tag = args.tag or derive_pool_tag(pool_path)
    out_dir = args.out_dir or os.path.join(_SCRIPTS_DIR, "archive_pool_analysis", pool_tag)
    os.makedirs(out_dir, exist_ok=True)

    data = load_pool(pool_path)
    config = data.get("config", {})
    entries = data.get("entries", [])

    print(f"Loaded archive pool: {pool_path}")
    print(f"  pool tag: {pool_tag}")
    print(f"  out dir:  {out_dir}")
    print(f"  entries: {len(entries)}")
    print(f"  config:  {json.dumps(config)}")

    matrices, dtype_counts, bad_strategy, step_added, successes, failures = collect_matrices(entries)

    print(f"\n===== data_type breakdown =====")
    for k, v in sorted(dtype_counts.items(), key=lambda x: -x[1]):
        pct = 100.0 * v / max(1, len(entries))
        print(f"  {k:<20s}  {v:>6d}  ({pct:5.2f}%)")
    if bad_strategy:
        print(f"  [warn] {bad_strategy} entries had missing/invalid strategy index")

    print_marginals(matrices["all"], "ALL", k=args.top_k)
    print_marginals(matrices["vanilla_harmful"], "vanilla_harmful", k=args.top_k)
    print_marginals(matrices["vanilla_benign"], "vanilla_benign", k=args.top_k)

    print_posterior_summary(
        successes, failures,
        alpha_prior=float(config.get("alpha_prior", 1.0)),
        beta_prior=float(config.get("beta_prior", 1.0)),
    )
    print_step_added_summary(step_added)

    plot_heatmap(matrices["all"],
                 f"archive_pool [{pool_tag}]: ALL (risk x attack_style)",
                 os.path.join(out_dir, "heatmap_all.png"))
    plot_heatmap(matrices["vanilla_harmful"],
                 f"archive_pool [{pool_tag}]: vanilla_harmful",
                 os.path.join(out_dir, "heatmap_harmful.png"))
    plot_heatmap(matrices["vanilla_benign"],
                 f"archive_pool [{pool_tag}]: vanilla_benign",
                 os.path.join(out_dir, "heatmap_benign.png"))


if __name__ == "__main__":
    main()
