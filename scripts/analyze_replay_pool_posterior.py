### dace: per-slot mean posterior harmfulness for dace-replay-pool ###
"""
For each (risk_category, attack_style) slot in an archive_pool.json, compute the
mean posterior harm rate p_hat = (alpha + successes) / (alpha + s + beta + f)
over entries whose p_hat >= --threshold (default 0.5). Entries below the
threshold are dropped (treated as low-quality / non-harmful enough to keep).

The raw rewrite prompts behind dace_replay_pool.jsonl come from the same
archive_pool.json (see scripts/extract_responses_and_prompts.py). We re-load
that pool here to recover the per-entry posterior + strategy.

Outputs (under scripts/replay_pool_posterior/<pool_tag>/):
  - heatmap_posterior_all.pdf         mean p_hat per slot (all kept entries)
  - heatmap_posterior_harmful.pdf     mean p_hat per slot (vanilla_harmful only)
  - heatmap_posterior_benign.pdf      mean p_hat per slot (vanilla_benign only)
  - heatmap_kept_count.pdf            # kept entries per slot (sanity check)

Usage:
  python scripts/analyze_replay_pool_posterior.py \
      --pool /mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/yupeng/ckpt/Game-separated/\
DACE-Diversity-Qwen2.5_7B_Instruct-w_dace_sft_v4-2026-05-03_14-30-23 \
      --step 300

  python scripts/analyze_replay_pool_posterior.py --pool .../archive_pool.json
  python scripts/analyze_replay_pool_posterior.py --pool /mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/yupeng/ckpt/Game-separated/DACE-Diversity-Qwen2.5_7B_Instruct-w_dace_sft_v4-2026-05-03_14-30-23 --step 300
      2>&1 | tail -5
"""

import argparse
import json
import os

import numpy as np
import matplotlib.pyplot as plt

# Reuse helpers from the existing archive_pool analyzer
from analyze_archive_pool import (
    RISK_CATEGORIES,
    ATTACK_STYLES,
    N_RISK,
    N_STYLE,
    load_pool,
    resolve_pool_path,
    derive_pool_tag,
)


_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))


### dace: short labels for tick axes (too long otherwise) ###
RISK_CATEGORIES_SHORT = [
    "VC",    # Violent Crimes
    "NVC",   # Non-Violent Crimes
    "SRC",   # Sex-Related Crimes
    "CSE",   # Child Sexual Exploitation
    "Def",   # Defamation
    "SA",    # Specialized Advice
    "Priv",  # Privacy
    "IP",    # Intellectual Property
    "IW",    # Indiscriminate Weapons
    "Hate",  # Hate
    "SSH",   # Suicide & Self-Harm
    "Elec",  # Elections
]

ATTACK_STYLES_SHORT = [
    "Slang",  # Slang
    "TT",     # Technical Terms
    "RP",     # Role Play
    "AM",     # Authority Manipulation
    "MSp",    # Misspellings
    "WP",     # Word Play
    "EM",     # Emotional Manipulation
    "Hyp",    # Hypotheticals
    "HS",     # Historical Scenario
    "UD",     # Uncommon Dialects
]

assert len(RISK_CATEGORIES_SHORT) == N_RISK
assert len(ATTACK_STYLES_SHORT) == N_STYLE


### dace: aggregate posterior p_hat per (risk, style) slot, dropping p_hat < threshold ###
def collect_posterior(entries, alpha_prior, beta_prior, threshold):
    sums = {
        "all": np.zeros((N_RISK, N_STYLE), dtype=np.float64),
        "vanilla_harmful": np.zeros((N_RISK, N_STYLE), dtype=np.float64),
        "vanilla_benign": np.zeros((N_RISK, N_STYLE), dtype=np.float64),
    }

    counts = {
        "all": np.zeros((N_RISK, N_STYLE), dtype=np.int64),
        "vanilla_harmful": np.zeros((N_RISK, N_STYLE), dtype=np.int64),
        "vanilla_benign": np.zeros((N_RISK, N_STYLE), dtype=np.int64),
    }

    n_total = 0
    n_bad_strategy = 0
    n_dropped_threshold = 0
    n_dropped_zero_trials = 0

    for e in entries:
        n_total += 1
        strat = e.get("strategy")

        if not strat or len(strat) != 2:
            n_bad_strategy += 1
            continue

        r, s = int(strat[0]), int(strat[1])

        if not (0 <= r < N_RISK and 0 <= s < N_STYLE):
            n_bad_strategy += 1
            continue

        succ = float(e.get("successes", 0.0))
        fail = float(e.get("failures", 0.0))
        trials = succ + fail

        if trials <= 0:
            # No posterior signal yet -- skip rather than fall back to prior 0.5
            n_dropped_zero_trials += 1
            continue

        p_hat = (alpha_prior + succ) / (alpha_prior + succ + beta_prior + fail)

        if p_hat < threshold:
            n_dropped_threshold += 1
            continue

        dtype = e.get("data_type", "unknown")

        sums["all"][r, s] += p_hat
        counts["all"][r, s] += 1

        if dtype in sums:
            sums[dtype][r, s] += p_hat
            counts[dtype][r, s] += 1

    means = {
        k: np.where(
            counts[k] > 0,
            sums[k] / np.maximum(counts[k], 1),
            np.nan,
        )
        for k in sums
    }

    return means, counts, {
        "n_total": n_total,
        "n_bad_strategy": n_bad_strategy,
        "n_dropped_zero_trials": n_dropped_zero_trials,
        "n_dropped_threshold": n_dropped_threshold,
    }


def _style_square_grid_axes(ax):
    """
    Make the whole 12 x 10 heatmap body a square and reduce local whitespace.
    This intentionally stretches individual cells slightly, because the goal is
    to make the whole 12 x 10 block square.
    """
    ax.set_box_aspect(1)  # key: the entire 12 x 10 grid block is square

    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")

    ax.set_xticks(range(N_STYLE))
    ax.set_xticklabels(ATTACK_STYLES_SHORT, fontsize=11)

    ax.set_yticks(range(N_RISK))
    ax.set_yticklabels(RISK_CATEGORIES_SHORT, fontsize=11)

    ax.set_xlabel("Attack Style", fontsize=12, labelpad=4)
    ax.set_ylabel("Risk Category", fontsize=12, labelpad=4)

    # White grid lines between cells
    ax.set_xticks(np.arange(-0.5, N_STYLE, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, N_RISK, 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.0)
    ax.tick_params(which="minor", length=0)

    # Reduce tick-label padding
    ax.tick_params(axis="x", pad=1)
    ax.tick_params(axis="y", pad=1)

    for spine in ax.spines.values():
        spine.set_visible(False)


### dace: heatmap with NaN-aware coloring + cell annotations ###
def plot_mean_heatmap(matrix, title, out_path, vmin=0.0, vmax=1.0, fmt="{:.2f}"):
    # Square-ish figure; actual heatmap body is forced square by ax.set_box_aspect(1)
    fig, ax = plt.subplots(figsize=(5.2, 5.2))

    cmap = plt.get_cmap("YlOrRd").copy()
    cmap.set_bad(color="lightgray")

    masked = np.ma.masked_invalid(matrix)

    im = ax.imshow(
        masked,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        aspect="auto",  # fill the square axes, making the 12 x 10 body square
    )

    _style_square_grid_axes(ax)

    thr = vmin + 0.6 * (vmax - vmin)

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            v = matrix[i, j]
            txt = "-" if np.isnan(v) else fmt.format(v)
            # color = "white" if (not np.isnan(v) and v > thr) else "black"
            color = "white"
            ax.text(
                j,
                i,
                txt,
                ha="center",
                va="center",
                fontsize=9.5,
                color=color,
            )

    # Compact colorbar
    cbar = fig.colorbar(
        im,
        ax=ax,
        fraction=0.045,
        pad=0.012,
        shrink=0.82,
    )
    cbar.ax.tick_params(labelsize=10)

    # Tight output: remove large surrounding whitespace
    fig.savefig(
        out_path,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0.03,
    )
    plt.close(fig)

    print(f"[saved] {out_path}")


def plot_count_heatmap(matrix, title, out_path):
    # Square-ish figure; actual heatmap body is forced square by ax.set_box_aspect(1)
    fig, ax = plt.subplots(figsize=(5.2, 5.2))

    vmax = float(matrix.max()) if matrix.size else 1.0

    im = ax.imshow(
        matrix,
        cmap="Blues",
        vmin=0.0,
        vmax=max(vmax, 1.0),
        aspect="auto",  # fill the square axes, making the 12 x 10 body square
    )

    _style_square_grid_axes(ax)

    thr = 0.6 * max(vmax, 1.0)

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            v = int(matrix[i, j])
            # color = "white" if v > thr else "black"
            color = "white"
            ax.text(
                j,
                i,
                str(v),
                ha="center",
                va="center",
                fontsize=8.5,
                color=color,
            )

    # Compact colorbar
    cbar = fig.colorbar(
        im,
        ax=ax,
        fraction=0.045,
        pad=0.012,
        shrink=0.82,
    )
    cbar.ax.tick_params(labelsize=10)

    # Tight output: remove large surrounding whitespace
    fig.savefig(
        out_path,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0.03,
    )
    plt.close(fig)

    print(f"[saved] {out_path}")


def build_parser():
    parser = argparse.ArgumentParser(
        description="Per-slot mean posterior harmfulness heatmap of an archive_pool.json"
    )

    parser.add_argument(
        "--pool",
        required=True,
        help="archive_pool.json path, global_step_N dir, or experiment root.",
    )

    parser.add_argument(
        "--step",
        type=int,
        default=None,
        help="When --pool is an experiment root, pick global_step_<STEP>.",
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Drop entries with posterior p_hat < threshold (default 0.5).",
    )

    parser.add_argument(
        "--out-dir",
        default=None,
        help="Output dir. Default scripts/replay_pool_posterior/<pool_tag>/.",
    )

    parser.add_argument(
        "--tag",
        default=None,
        help="Override auto pool tag.",
    )

    return parser


def main():
    args = build_parser().parse_args()

    pool_path = resolve_pool_path(args.pool, args.step)
    pool_tag = args.tag or derive_pool_tag(pool_path)

    out_dir = args.out_dir or os.path.join(
        _SCRIPTS_DIR,
        "replay_pool_posterior",
        pool_tag,
    )
    os.makedirs(out_dir, exist_ok=True)

    data = load_pool(pool_path)
    config = data.get("config", {})
    entries = data.get("entries", [])

    alpha_prior = float(config.get("alpha_prior", 1.0))
    beta_prior = float(config.get("beta_prior", 1.0))

    print(f"Loaded archive pool: {pool_path}")
    print(f"  pool tag: {pool_tag}")
    print(f"  out dir:  {out_dir}")
    print(f"  entries:  {len(entries)}")
    print(
        f"  alpha_prior={alpha_prior}, "
        f"beta_prior={beta_prior}, "
        f"threshold={args.threshold}"
    )

    means, counts, stats = collect_posterior(
        entries,
        alpha_prior,
        beta_prior,
        args.threshold,
    )

    print("\n===== filter stats =====")
    print(f"  total entries:           {stats['n_total']}")
    print(f"  bad/missing strategy:    {stats['n_bad_strategy']}")
    print(f"  dropped (zero trials):   {stats['n_dropped_zero_trials']}")
    print(f"  dropped (p_hat<{args.threshold}):    {stats['n_dropped_threshold']}")
    print(f"  kept (all):              {int(counts['all'].sum())}")
    print(f"  kept (vanilla_harmful):  {int(counts['vanilla_harmful'].sum())}")
    print(f"  kept (vanilla_benign):   {int(counts['vanilla_benign'].sum())}")

    for key in ("all", "vanilla_harmful", "vanilla_benign"):
        c = counts[key]
        m = means[key]

        n_occ = int((c > 0).sum())
        flat = m[c > 0]

        if flat.size:
            print(
                f"  [{key}] occupied slots: {n_occ}/{N_RISK * N_STYLE}  "
                f"mean p_hat: {flat.mean():.4f}  "
                f"(min {flat.min():.4f}, max {flat.max():.4f})"
            )
        else:
            print(f"  [{key}] no kept entries")

    title_suffix = f"  [threshold p_hat>={args.threshold}]"

    plot_mean_heatmap(
        means["all"],
        f"replay_pool [{pool_tag}]: mean posterior p_hat (ALL){title_suffix}",
        os.path.join(out_dir, "heatmap_posterior_all.pdf"),
    )

    plot_mean_heatmap(
        means["vanilla_harmful"],
        f"replay_pool [{pool_tag}]: mean posterior p_hat (vanilla_harmful){title_suffix}",
        os.path.join(out_dir, "heatmap_posterior_harmful.pdf"),
    )

    plot_mean_heatmap(
        means["vanilla_benign"],
        f"replay_pool [{pool_tag}]: mean posterior p_hat (vanilla_benign){title_suffix}",
        os.path.join(out_dir, "heatmap_posterior_benign.pdf"),
    )

    plot_count_heatmap(
        counts["all"],
        f"replay_pool [{pool_tag}]: # kept entries per slot{title_suffix}",
        os.path.join(out_dir, "heatmap_kept_count.pdf"),
    )

    summary = {
        "pool_path": pool_path,
        "pool_tag": pool_tag,
        "threshold": args.threshold,
        "alpha_prior": alpha_prior,
        "beta_prior": beta_prior,
        "filter_stats": stats,
        "kept_counts": {k: int(v.sum()) for k, v in counts.items()},
    }

    summary_path = os.path.join(out_dir, "summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"[saved] {summary_path}")


if __name__ == "__main__":
    main()