### dace: cross-eval (attacker vs defender) ASR heatmap ###
"""
Read metrics.json under each A{a}_vs_D{d} subdir of one or more heatmap-cross-eval/
directories, extract harmbench:attacker_defender -> "micro ASR (lower)", and plot
a single heatmap with cells labeled as "x.xx%". Output PDF, no title.

Defaults to the three known cross-eval dirs (D0 Instruct baseline + D30/60/90/120
RL iters covering A15/45/75/105/135), merged into one 5x5 heatmap with Instruct
as the first defender column.

Usage:
  python scripts/plot_cross_eval_heatmap.py
  python scripts/plot_cross_eval_heatmap.py --dir OTHER_DIR --out OTHER.pdf
"""

import argparse
import glob
import json
import os
import re

import numpy as np
import matplotlib.pyplot as plt


_SUBDIR_RE = re.compile(r"^A(\d+)_vs_D(\d+)$")


### dace: default three cross-eval dirs (Instruct D0 + two RL-iter batches) ###
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_DIRS = [
    os.path.join(
        _REPO_ROOT,
        "eval-dace/safety-eval-fork/results/dace/heatmap-cross-eval-20260507_090909",
    ),  # D0 = Instruct
    os.path.join(
        _REPO_ROOT,
        "eval-dace/safety-eval-fork/results/dace/heatmap-cross-eval-20260506_160114",
    ),  # D30..120 x A15..105
    os.path.join(
        _REPO_ROOT,
        "eval-dace/safety-eval-fork/results/dace/heatmap-cross-eval-20260507_083432",
    ),  # D30..120 x A135
]

DEFAULT_OUT = os.path.join(
    _REPO_ROOT,
    "eval-dace/safety-eval-fork/results/dace/heatmap_cross_eval_asr.pdf",
)


### dace: scan input dirs, collect {(a, d): asr_percent} ###
def collect(dirs):
    data = {}

    for root in dirs:
        for sub in sorted(glob.glob(os.path.join(root, "A*_vs_D*"))):
            m = _SUBDIR_RE.match(os.path.basename(sub))
            if not m:
                continue

            metrics_path = os.path.join(sub, "metrics.json")
            if not os.path.isfile(metrics_path):
                continue

            with open(metrics_path, "r", encoding="utf-8") as f:
                obj = json.load(f)

            try:
                asr = obj["harmbench:attacker_defender"]["micro ASR (lower)"]
            except (KeyError, TypeError):
                continue

            a, d = int(m.group(1)), int(m.group(2))
            data[(a, d)] = float(asr) * 100.0

    return data


def build_matrix(data):
    rows = sorted({a for (a, _) in data})
    cols = sorted({d for (_, d) in data})

    mat = np.full((len(rows), len(cols)), np.nan, dtype=np.float64)

    for i, a in enumerate(rows):
        for j, d in enumerate(cols):
            if (a, d) in data:
                mat[i, j] = data[(a, d)]

    return mat, rows, cols


### dace: map A/D step values to label strings (default=A#/D#, rl-iter=RL-iter naming) ###
def make_labels(rows, cols, style):
    if style == "rl-iter":
        # A{15,45,75,105,135,...} -> RL-iter-{1,2,3,4,5,...}
        # step = 15 + 30 * (i - 1)
        row_labels = []
        for a in rows:
            if a >= 15 and (a - 15) % 30 == 0:
                row_labels.append(f"RL-iter-{(a - 15) // 30 + 1}")
            else:
                row_labels.append(f"A{a}")

        # D0 -> Instruct, D{30,60,90,120,...} -> RL-iter-{1,2,3,4,...}
        col_labels = []
        for d in cols:
            if d == 0:
                col_labels.append("Instruct")
            elif d > 0 and d % 30 == 0:
                col_labels.append(f"RL-iter-{d // 30}")
            else:
                col_labels.append(f"D{d}")

        return row_labels, col_labels

    return [f"A{a}" for a in rows], [f"D{d}" for d in cols]


def _style_square_heatmap_axes(ax, rows, cols, row_labels, col_labels):
    """
    Force the full heatmap body to be square and use compact paper-style spacing.

    Note:
      This makes the whole matrix block square.
      If the matrix is not square, individual cells are slightly stretched.
    """
    # Key: make the whole heatmap box square
    ax.set_box_aspect(1)

    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")

    ax.set_xticks(range(len(cols)))
    ax.set_yticks(range(len(rows)))

    # 5x5 这里可以不旋转，整体更像论文图。
    # 如果后续列数变多，可以把 rotation 改成 25。
    ax.set_xticklabels(
        col_labels,
        fontsize=12,
        rotation=0,
        ha="center",
    )
    ax.set_yticklabels(
        row_labels,
        fontsize=12,
    )

    ax.set_xlabel("Defender", fontsize=14, labelpad=8)
    ax.set_ylabel("Attacker", fontsize=14, labelpad=8)

    # White grid lines between cells
    ax.set_xticks(np.arange(-0.5, len(cols), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(rows), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.4)
    ax.tick_params(which="minor", length=0)

    # Reduce padding around tick labels
    ax.tick_params(axis="x", pad=3)
    ax.tick_params(axis="y", pad=3)

    for spine in ax.spines.values():
        spine.set_visible(False)


### dace: heatmap with YlOrRd, no title, cell text as x.xx% ###
def plot_heatmap(mat, rows, cols, out_path, label_style):
    # Square-ish figure; heatmap body itself is forced square by ax.set_box_aspect(1)
    # 5x5 图可以稍微小一点，但字体更大。
    fig, ax = plt.subplots(figsize=(5.6, 5.6))

    cmap = plt.get_cmap("YlOrRd").copy()
    cmap.set_bad(color="lightgray")

    masked = np.ma.masked_invalid(mat)

    vmax = float(np.nanmax(mat)) if np.any(~np.isnan(mat)) else 1.0

    im = ax.imshow(
        masked,
        cmap=cmap,
        vmin=0.0,
        vmax=vmax,
        aspect="auto",  # fill the square axes
    )

    row_labels, col_labels = make_labels(rows, cols, label_style)

    _style_square_heatmap_axes(
        ax=ax,
        rows=rows,
        cols=cols,
        row_labels=row_labels,
        col_labels=col_labels,
    )

    # Cell annotations
    threshold = 0.6 * vmax

    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            v = mat[i, j]
            txt = "-" if np.isnan(v) else f"{v:.2f}"
            color = "white" if (not np.isnan(v) and v > threshold) else "black"

            ax.text(
                j,
                i,
                txt,
                ha="center",
                va="center",
                fontsize=14,
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
    cbar.ax.tick_params(labelsize=13)

    # Tight PDF output with minimal surrounding whitespace
    fig.savefig(
        out_path,
        format="pdf",
        dpi=300,
        bbox_inches="tight",
        pad_inches=0.03,
    )

    plt.close(fig)

    print(f"[saved] {out_path}")


def build_parser():
    p = argparse.ArgumentParser(description="Cross-eval ASR heatmap (PDF).")

    p.add_argument(
        "--dir",
        action="append",
        default=None,
        help=(
            "heatmap-cross-eval-* directory. Can be passed multiple times; "
            "entries from all dirs are merged. If omitted, uses the three "
            "default dirs hardcoded in the script."
        ),
    )

    p.add_argument(
        "--out",
        default=DEFAULT_OUT,
        help="Output PDF path.",
    )

    p.add_argument(
        "--label-style",
        choices=["default", "rl-iter"],
        default="rl-iter",
        help=(
            "Axis tick labels. 'rl-iter' maps A/D steps to RL iteration "
            "names (D0 -> Instruct). Default 'rl-iter'."
        ),
    )

    return p


def main():
    args = build_parser().parse_args()

    dirs = args.dir if args.dir else DEFAULT_DIRS

    data = collect(dirs)

    if not data:
        raise SystemExit("No metrics.json entries found in the given dir(s).")

    mat, rows, cols = build_matrix(data)

    print(f"rows (A): {rows}")
    print(f"cols (D): {cols}")

    for i, a in enumerate(rows):
        line = [f"A{a:>4}"]
        for j, d in enumerate(cols):
            v = mat[i, j]
            line.append("   -   " if np.isnan(v) else f"{v:6.2f}")
        print("  ".join(line))

    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)

    plot_heatmap(
        mat=mat,
        rows=rows,
        cols=cols,
        out_path=args.out,
        label_style=args.label_style,
    )


if __name__ == "__main__":
    main()