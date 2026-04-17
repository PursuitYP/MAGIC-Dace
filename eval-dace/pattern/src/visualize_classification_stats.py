"""
Visualize classification statistics across training steps
Create bar charts for primary strategy distributions (fine-grained 0-19).
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import argparse
from pathlib import Path

try:
    from prompts_grained import FINE_GRAINED_CATEGORIES
except ImportError:
    FINE_GRAINED_CATEGORIES = None


# NOTE (2025-01-16): Sync visualization to fine-grained 20-category taxonomy.
FALLBACK_STRATEGY_NAMES = {
    "0": "Role-playing",
    "1": "Simulated decision-making scenarios",
    "2": "Academic/Educational pretext",
    "3": "Concealment of key information",
    "4": "Causation confusion",
    "5": "False analogies & Fact distortion",
    "6": "Concept substitution",
    "7": "False premise assumption",
    "8": "Legitimacy pretext",
    "9": "Ignore previous instructions",
    "10": "Step-by-step questioning",
    "11": "Multi-condition stacking",
    "12": "Complex logic nesting",
    "13": "Encoding rewriting",
    "14": "Templated output format",
    "15": "Code by pseudonym",
    "16": "Structured response",
    "17": "Surrogate modality",
    "18": "Language translation",
    "19": "None of these"
}


def get_strategy_names() -> dict:
    if FINE_GRAINED_CATEGORIES:
        return {
            str(entry["id"]): entry["name"]
            for entry in FINE_GRAINED_CATEGORIES.values()
        }
    return FALLBACK_STRATEGY_NAMES


def get_strategy_order(stats_by_step: dict, selected_steps: list) -> list:
    strategies = set()
    for step in selected_steps:
        step_stats = stats_by_step.get(str(step), {})
        primary_counts = step_stats.get("primary_strategy_counts", {})
        for key in primary_counts.keys():
            strategies.add(str(key))
    return sorted(
        strategies,
        key=lambda x: int(x) if x.isdigit() else x
    )


def get_strategy_colors(strategies: list) -> dict:
    cmap = plt.get_cmap("tab20", max(1, len(strategies)))
    return {strategy: cmap(i) for i, strategy in enumerate(strategies)}


def load_statistics(stats_file: str):
    """Load statistics from JSON file"""
    with open(stats_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def plot_primary_strategy_distribution(stats_data: dict, selected_steps: list, output_dir: str):
    """
    Plot bar chart for primary strategy distribution across selected steps
    
    Args:
        stats_data: Statistics data loaded from JSON
        selected_steps: List of steps to visualize (e.g., [20, 120, 220, 320, 420])
        output_dir: Directory to save plots
    """
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    stats_by_step = stats_data["statistics_by_step"]
    strategy_names = get_strategy_names()
    strategies = get_strategy_order(stats_by_step, selected_steps)
    strategy_colors = get_strategy_colors(strategies)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Width of bars and positions
    bar_width = min(0.8 / max(1, len(strategies)), 0.08)
    x_positions = np.arange(len(selected_steps))
    
    # Plot bars for each strategy
    for idx, strategy in enumerate(strategies):
        counts = []
        for step in selected_steps:
            step_stats = stats_by_step.get(str(step), {})
            primary_counts = step_stats.get("primary_strategy_counts", {})
            total = step_stats.get("successful_records", 1)
            # Calculate percentage
            count = primary_counts.get(strategy, 0)
            percentage = (count / total * 100) if total > 0 else 0
            counts.append(percentage)
        
        # Plot bars
        offset = (idx - 2) * bar_width
        label = f"{strategy}: {strategy_names.get(strategy, 'Unknown')}"
        ax.bar(
            x_positions + offset,
            counts,
            bar_width,
            label=label,
            color=strategy_colors[strategy],
            alpha=0.85
        )
    
    # Customize plot
    ax.set_xlabel('Training Step', fontsize=14, fontweight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=14, fontweight='bold')
    ax.set_title('Primary Strategy Distribution Across Training Steps',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x_positions)
    ax.set_xticklabels([f'Step {s}' for s in selected_steps], fontsize=12)
    ax.legend(fontsize=9, loc='upper right', ncol=2)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, 100)
    
    plt.tight_layout()
    output_path = Path(output_dir) / "primary_strategy_distribution.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved plot: {output_path}")
    plt.close()


def plot_diversity_trends(stats_data: dict, output_dir: str):
    """
    Plot diversity trends over all steps
    """
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    stats_by_step = stats_data["statistics_by_step"]
    steps = sorted([int(s) for s in stats_by_step.keys()])
    
    # Extract diversity metrics
    primary_diversity = []
    combined_diversity = []
    hybrid_ratios = []
    
    for step in steps:
        step_stats = stats_by_step[str(step)]
        primary_diversity.append(step_stats.get("primary_strategy_diversity", 0))
        combined_diversity.append(step_stats.get("combined_strategy_diversity", 0))
        hybrid_ratios.append(step_stats.get("hybrid_ratio", 0) * 100)
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Plot 1: Diversity trends
    ax1.plot(steps, primary_diversity, marker='o', linewidth=2, 
             markersize=6, label='Primary Strategy Diversity', color='#FF6B6B')
    ax1.plot(steps, combined_diversity, marker='s', linewidth=2, 
             markersize=6, label='Combined Strategy Diversity', color='#4ECDC4')
    ax1.set_xlabel('Training Step', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Shannon Entropy', fontsize=14, fontweight='bold')
    ax1.set_title('Strategy Diversity Trends (Higher = More Diverse)', 
                  fontsize=16, fontweight='bold', pad=20)
    ax1.legend(fontsize=12)
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # Plot 2: Hybrid strategy ratio
    ax2.plot(steps, hybrid_ratios, marker='D', linewidth=2, 
             markersize=6, label='Hybrid Strategy Usage', color='#FFA07A')
    ax2.set_xlabel('Training Step', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Hybrid Strategy Ratio (%)', fontsize=14, fontweight='bold')
    ax2.set_title('Hybrid Strategy Usage Trends', 
                  fontsize=16, fontweight='bold', pad=20)
    ax2.legend(fontsize=12)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_ylim(0, 100)
    
    plt.tight_layout()
    output_path = Path(output_dir) / "diversity_and_hybrid_trends.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved plot: {output_path}")
    plt.close()


def plot_stacked_bar_chart(stats_data: dict, selected_steps: list, output_dir: str):
    """
    Plot stacked bar chart showing composition of strategies at each step
    """
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    stats_by_step = stats_data["statistics_by_step"]
    strategy_names = get_strategy_names()
    strategies = get_strategy_order(stats_by_step, selected_steps)
    strategy_colors = get_strategy_colors(strategies)
    
    # Prepare data
    data_matrix = []
    for step in selected_steps:
        step_stats = stats_by_step.get(str(step), {})
        primary_counts = step_stats.get("primary_strategy_counts", {})
        total = step_stats.get("successful_records", 1)
        
        row = []
        for strategy in strategies:
            count = primary_counts.get(strategy, 0)
            percentage = (count / total * 100) if total > 0 else 0
            row.append(percentage)
        data_matrix.append(row)
    
    data_matrix = np.array(data_matrix).T
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot stacked bars
    x_positions = np.arange(len(selected_steps))
    bottom = np.zeros(len(selected_steps))
    
    for idx, strategy in enumerate(strategies):
        label = f"{strategy}: {strategy_names.get(strategy, 'Unknown')}"
        ax.bar(
            x_positions,
            data_matrix[idx],
            bottom=bottom,
            label=label,
            color=strategy_colors[strategy],
            alpha=0.85
        )
        bottom += data_matrix[idx]
    
    # Customize plot
    ax.set_xlabel('Training Step', fontsize=14, fontweight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=14, fontweight='bold')
    ax.set_title('Primary Strategy Composition Across Training Steps', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x_positions)
    ax.set_xticklabels([f'Step {s}' for s in selected_steps], fontsize=12)
    ax.legend(fontsize=11, loc='upper left', bbox_to_anchor=(1, 1))
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    output_path = Path(output_dir) / "stacked_strategy_composition.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved plot: {output_path}")
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Visualize classification statistics")
    
    parser.add_argument(
        "--stats-file",
        default="/mnt/shared-storage-user/wenxiaoyu/game-private/eval/pattern/classification_statistics.json",
        help="Path to statistics JSON file"
    )
    
    parser.add_argument(
        "--output-dir",
        default="/mnt/shared-storage-user/wenxiaoyu/game-private/eval/pattern/plots",
        help="Directory to save plots"
    )
    
    parser.add_argument(
        "--selected-steps",
        type=int,
        nargs="+",
        default=[20, 120, 220, 320, 420],
        help="Steps to visualize in bar charts"
    )
    
    args = parser.parse_args()
    
    # Load statistics
    print(f"Loading statistics from {args.stats_file}...")
    stats_data = load_statistics(args.stats_file)
    
    print(f"Creating visualizations for steps: {args.selected_steps}")
    
    # Create plots
    plot_primary_strategy_distribution(stats_data, args.selected_steps, args.output_dir)
    plot_diversity_trends(stats_data, args.output_dir)
    plot_stacked_bar_chart(stats_data, args.selected_steps, args.output_dir)
    
    print("\n" + "=" * 80)
    print("Visualization completed!")
    print(f"Plots saved to: {args.output_dir}")
    print("=" * 80)


if __name__ == "__main__":
    main()
