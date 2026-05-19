import json
import re
import os
import argparse
import matplotlib.pyplot as plt
import numpy as np

# =========================
# DACE 官方定义（与结果文件对齐；v4: 12 risks — pruned S12 Sexual Content + S14 Code Interpreter Abuse）
# =========================

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

risk2idx = {k: i for i, k in enumerate(RISK_CATEGORIES)}
style2idx = {k: i for i, k in enumerate(ATTACK_STYLES)}


def parse_strategy(strategy_text):
    """
    strategy 格式：
    risk category: X
    attack style: Y
    """
    if not strategy_text:
        return None, None

    # 逐行匹配，不能用 re.S + (.+)
    risk_match = re.search(r"(?im)^\s*risk category:\s*([^\n\r]+)\s*$", strategy_text)
    style_match = re.search(r"(?im)^\s*attack style:\s*([^\n\r]+)\s*$", strategy_text)

    risk = risk_match.group(1).strip() if risk_match else None
    style = style_match.group(1).strip() if style_match else None
    return risk, style


def init_matrix():
    return np.zeros((len(RISK_CATEGORIES), len(ATTACK_STYLES)), dtype=int)


def update_matrix(matrix, risk, style):
    if risk in risk2idx and style in style2idx:
        matrix[risk2idx[risk], style2idx[style]] += 1


def load_and_count(path, label):
    matrix = init_matrix()
    total = 0
    parsed = 0
    matched = 0
    unmatched_examples = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            total += 1
            r = json.loads(line)
            strategy = r.get("strategy")

            risk, style = parse_strategy(strategy)
            if risk and style:
                parsed += 1
                if risk in risk2idx and style in style2idx:
                    matched += 1
                    update_matrix(matrix, risk, style)
                elif len(unmatched_examples) < 10:
                    unmatched_examples.append((risk, style))

    print(f"[debug] {label}: total={total}, parsed={parsed}, matched={matched}")
    if unmatched_examples:
        print(f"[debug] {label}: unmatched examples:")
        for risk, style in unmatched_examples:
            print(f"    risk={risk!r}, style={style!r}")

    return matrix


### dace: print top-2 / bottom-2 risk categories and attack styles by marginal counts instead of the full matrix ###
def print_top_bottom(matrix, title, k=5):
    print(f"\n===== {title} =====")
    total = int(matrix.sum())
    print(f"total matched samples: {total}")
    if total == 0:
        print("  (no samples matched; nothing to rank)")
        return

    def _show(axis_label, counts, names):
        order_desc = np.argsort(-counts, kind="stable")
        order_asc = np.argsort(counts, kind="stable")
        width = max(len(n) for n in names)

        print(f"[{axis_label}] top-{k}:")
        for idx in order_desc[:k]:
            c = int(counts[idx])
            pct = 100.0 * c / total
            print(f"  {names[idx]:<{width}}  {c:>8d}  ({pct:5.2f}%)")
        print(f"[{axis_label}] bottom-{k}:")
        for idx in order_asc[:k]:
            c = int(counts[idx])
            pct = 100.0 * c / total
            print(f"  {names[idx]:<{width}}  {c:>8d}  ({pct:5.2f}%)")

    _show("risk category", matrix.sum(axis=1), RISK_CATEGORIES)
    _show("attack style",  matrix.sum(axis=0), ATTACK_STYLES)


### dace: out_dir is now an explicit arg so v1 vs v2 heatmaps can be landed into different directories ###
def plot_heatmap(matrix, title, out_dir):
    plt.figure(figsize=(14, 7))
    plt.imshow(matrix, cmap="YlOrRd")

    plt.xticks(range(len(ATTACK_STYLES)), ATTACK_STYLES, rotation=45, ha="right")
    plt.yticks(range(len(RISK_CATEGORIES)), RISK_CATEGORIES)

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            plt.text(j, i, str(matrix[i, j]), ha="center", va="center", fontsize=8)

    plt.title(title)
    plt.colorbar()
    plt.tight_layout()

    filename = f"heatmap{title.replace(' ', '_').lower()}.png"
    filepath = os.path.join(out_dir, filename)
    plt.savefig(filepath, dpi=300)
    plt.close()
    print(f"[saved] {filepath}")


### dace: CLI-driven so v1 and v2 result files can both be analyzed without path edits ###
def build_parser():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="DACE strategy distribution analyzer (risk x attack style).")
    parser.add_argument(
        "--benign", default=os.path.join(base_dir, "sft_data_cot_benign.jsonl"),
        help="Path to the benign distilled jsonl (default: v1 output).",
    )
    parser.add_argument(
        "--harmful", default=os.path.join(base_dir, "sft_data_cot_harmful.jsonl"),
        help="Path to the harmful distilled jsonl (default: v1 output).",
    )
    parser.add_argument(
        "--tag", default="",
        help="Optional suffix appended to section headers and heatmap filenames (e.g., 'v2').",
    )
    parser.add_argument(
        "--out-dir", default=base_dir,
        help="Directory to save heatmap PNGs (default: this script's directory).",
    )
    return parser


def main():
    args = build_parser().parse_args()

    title_tag   = f"_{args.tag}" if args.tag else ""   # appended to heatmap filenames (lowercase snake_case)
    section_tag = f" ({args.tag})" if args.tag else "" # appended to printed section headers

    os.makedirs(args.out_dir, exist_ok=True)

    benign_matrix  = load_and_count(args.benign,  f"BENIGN{section_tag}")
    harmful_matrix = load_and_count(args.harmful, f"HARMFUL{section_tag}")
    all_matrix = benign_matrix + harmful_matrix

    print_top_bottom(benign_matrix,  f"BENIGN{section_tag}")
    print_top_bottom(harmful_matrix, f"HARMFUL{section_tag}")
    print_top_bottom(all_matrix,     f"ALL{section_tag}")

    plot_heatmap(benign_matrix,  f"{title_tag}_benign_strategy_distribution",  args.out_dir)
    plot_heatmap(harmful_matrix, f"{title_tag}_harmful_strategy_distribution", args.out_dir)
    plot_heatmap(all_matrix,     f"{title_tag}_all_strategy_distribution",     args.out_dir)


if __name__ == "__main__":
    main()

"""
# Run commands:

# v1 (pre-directed-style distillation, hardcoded-default paths):
python data-sft/analyze_strategy_distribution.py

# v1 with explicit paths (equivalent to the default):
python data-sft/analyze_strategy_distribution.py \
    --benign  data-sft/sft_data_cot_benign.jsonl \
    --harmful data-sft/sft_data_cot_harmful.jsonl

# v2 (directed-style distillation, after running bash data-sft/run_cot_distill_v2.sh):
python data-sft/analyze_strategy_distribution.py \
    --benign  data-sft/sft_data_cot_v2_benign.jsonl \
    --harmful data-sft/sft_data_cot_v2_harmful.jsonl \
    --tag v2

# v3 (v1nv2 hybrid, after running python data-sft/convert_v2_cot_to_game_format.py):
#   all v2 samples + v1 samples of the 3 rarest risk categories
python data-sft/analyze_strategy_distribution.py \
    --benign  data-sft/sft_data_cot_v1nv2_v3_benign.jsonl \
    --harmful data-sft/sft_data_cot_v1nv2_v3_harmful.jsonl \
    --tag v3

python data-sft/analyze_strategy_distribution.py \
    --benign  data-sft/sft_data_cot_v4_benign.jsonl \
    --harmful data-sft/sft_data_cot_v4_harmful.jsonl \
    --tag v4

# The --tag suffix keeps v1 / v2 / v3 heatmaps side by side (heatmap_..._v2.png, heatmap_..._v3.png)
# and labels the printed section headers so you can eyeball the before/after comparison.
"""