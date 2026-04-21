import json
import re
import os
import matplotlib.pyplot as plt
import numpy as np

# =========================
# DACE 官方定义（与结果文件对齐）
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
    "Sexual Content",
    "Elections",
    "Code Interpreter Abuse",
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


def print_matrix(matrix, title):
    print(f"\n===== {title} =====")
    header = ["Risk \\ Style"] + ATTACK_STYLES
    print("\t".join(header))

    for i, risk in enumerate(RISK_CATEGORIES):
        row = [risk] + [str(matrix[i, j]) for j in range(len(ATTACK_STYLES))]
        print("\t".join(row))


def plot_heatmap(matrix, title):
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

    out_dir = os.path.dirname(__file__)
    filename = f"heatmap_{title.replace(' ', '_').lower()}.png"
    filepath = os.path.join(out_dir, filename)
    plt.savefig(filepath, dpi=300)
    plt.close()
    print(f"[saved] {filepath}")


def main():
    base_dir = os.path.dirname(__file__)
    benign_path = os.path.join(base_dir, "sft_data_cot_benign.jsonl")
    harmful_path = os.path.join(base_dir, "sft_data_cot_harmful.jsonl")

    benign_matrix = load_and_count(benign_path, "BENIGN")
    harmful_matrix = load_and_count(harmful_path, "HARMFUL")
    all_matrix = benign_matrix + harmful_matrix

    print_matrix(benign_matrix, "BENIGN")
    print_matrix(harmful_matrix, "HARMFUL")
    print_matrix(all_matrix, "ALL")

    plot_heatmap(benign_matrix, "benign_strategy_distribution")
    plot_heatmap(harmful_matrix, "harmful_strategy_distribution")
    plot_heatmap(all_matrix, "all_strategy_distribution")


if __name__ == "__main__":
    main()


# python data-sft/analyze_strategy_distribution.py