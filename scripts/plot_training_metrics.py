### dace: plot four training metrics (archive + replay) from output.log as raw line charts ###
import re
import argparse
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


METRIC_KEYS = [
    "archive/strategy_coverage",
    "archive/pool_size",
    "archive/coverage_entropy",
    "replay/pool_mean_posterior",
]


def parse_log(log_path: Path):
    step_pat = re.compile(r"^step:(\d+)\s")
    metric_pats = {k: re.compile(rf"\b{re.escape(k)}:(-?\d+\.?\d*)") for k in METRIC_KEYS}

    raw = {k: {} for k in METRIC_KEYS}  # step -> value (last occurrence wins)

    with log_path.open() as f:
        for line in f:
            m = step_pat.match(line)
            if not m:
                continue
            step = int(m.group(1))
            for key, pat in metric_pats.items():
                vm = pat.search(line)
                if vm is None:
                    continue
                raw[key][step] = float(vm.group(1))

    series = {}
    for k, d in raw.items():
        steps_sorted = sorted(d.keys())
        series[k] = (steps_sorted, [d[s] for s in steps_sorted])
    return series


def plot_series(series, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    for key in METRIC_KEYS:
        steps, values = series[key]
        fig, ax = plt.subplots(figsize=(6, 4))
        if steps:
            steps_arr = np.asarray(steps)
            vals_arr = np.asarray(values, dtype=float)
            ax.plot(steps_arr, vals_arr, linewidth=1.2, color="tab:blue")
        ax.set_title(key)
        ax.set_xlabel("step")
        ax.set_ylabel(key.split("/")[-1])
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fname = key.replace("/", "_") + ".pdf"
        out_path = out_dir / fname
        fig.savefig(out_path, bbox_inches="tight")
        plt.close(fig)
        print(f"saved: {out_path}  ({len(steps)} points)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default="scripts/output.log")
    parser.add_argument("--out_dir", default="scripts/training_metrics")
    args = parser.parse_args()

    log_path = Path(args.log)
    out_dir = Path(args.out_dir)
    series = parse_log(log_path)
    for k, (steps, _) in series.items():
        print(f"{k}: {len(steps)} points, step range [{min(steps) if steps else '-'}, {max(steps) if steps else '-'}]")
    plot_series(series, out_dir)


if __name__ == "__main__":
    main()
