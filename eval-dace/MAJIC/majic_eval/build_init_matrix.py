"""Offline initialization of the MAJIC Markov transition matrix.

Reproduces the paper's §Initializing-Markov-Transition-Matrix pipeline using
the same OpenAI-compatible endpoints as ``run_majic.sh``:

1. For every strategy i in the pool, apply it to every query in the local
   50-sample harmful dataset (``data/harmful_behaviors_50.json`` by default).
2. Record successful attempts in a success set H; failed disguised prompts in F.
3. For every failed prompt q'_i, rewrite it with each strategy j and record
   whether that second-pass succeeds.
4. Compute ``A[i, j] = N_success(j | i failed) / N_fail(i)``.
5. Apply row-wise softmax with temperature T to obtain the transition matrix M.

The resulting matrix is saved to ``--out`` (default
``markov_methods/init_matrix.npy``) and can then be consumed by
``run_majic.sh`` via ``MAJIC_INIT_MODE=learned`` (or ``learned_static``).

This module is NOT invoked by ``run_majic.sh`` -- it is a separate offline tool.
"""
from __future__ import annotations

import argparse
import json
import os
from typing import List

import numpy as np

from .api_client import build_clients
from .judge import judge_score
from .markov import DEFAULT_TEMPERATURE, softmax_row
from .strategies import NUM_STRATEGIES, get_strategy


def _load_goals(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    goals = []
    for item in data:
        if isinstance(item, str):
            goals.append(item)
        elif isinstance(item, dict):
            val = item.get("goal") or item.get("prompt") or item.get("Behavior")
            if val:
                goals.append(val)
    if not goals:
        raise ValueError(f"No goals loaded from {path}.")
    return goals


def _apply_init(attacker, defender, judge_client, strategy_idx: int, goal: str):
    strategy = get_strategy(strategy_idx)
    disguised = attacker.chat(
        [{"role": "user", "content": strategy.render_init(goal)}],
        temperature=attacker.temperature,
    )
    disguised = (disguised or "").strip().strip('"')
    if not disguised or disguised.startswith("API_ERROR"):
        disguised = goal
    victim_prompt = disguised + (strategy.victim_suffix or "")
    victim_response = defender.chat(
        [{"role": "user", "content": victim_prompt}],
        temperature=defender.temperature,
    )
    score, rating = judge_score(judge_client, goal, victim_response)
    return score, rating, disguised, victim_response


def _apply_compose(attacker, defender, judge_client, strategy_idx: int, goal: str, prev_disguised: str):
    strategy = get_strategy(strategy_idx)
    disguised = attacker.chat(
        [{"role": "user", "content": strategy.render_compose(goal, prev_disguised)}],
        temperature=attacker.temperature,
    )
    disguised = (disguised or "").strip().strip('"')
    if not disguised or disguised.startswith("API_ERROR"):
        disguised = prev_disguised
    victim_prompt = disguised + (strategy.victim_suffix or "")
    victim_response = defender.chat(
        [{"role": "user", "content": victim_prompt}],
        temperature=defender.temperature,
    )
    score, rating = judge_score(judge_client, goal, victim_response)
    return score, rating, disguised, victim_response


def get_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Offline MAJIC Markov matrix initializer.")
    p.add_argument("--target-api-key", default=None)
    p.add_argument("--target-base-url", default=None)
    p.add_argument("--target-model", default=None)
    p.add_argument("--attacker-api-key", default=None)
    p.add_argument("--attacker-base-url", default=None)
    p.add_argument("--attacker-model", default=None)
    p.add_argument("--judge-api-key", default=None)
    p.add_argument("--judge-base-url", default=None)
    p.add_argument("--judge-model", default=None)
    p.add_argument("--attacker-answer-extract", action="store_true")
    p.add_argument("--attacker-temperature", type=float, default=0.9)

    p.add_argument(
        "--local-dataset",
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "harmful_behaviors_50.json"),
    )
    p.add_argument("--num-samples", type=int, default=None)
    p.add_argument("--softmax-temperature", type=float, default=DEFAULT_TEMPERATURE)
    p.add_argument(
        "--out",
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "markov_methods", "init_matrix.npy"),
    )
    p.add_argument("--log", default=None, help="Optional JSONL path to log every H/F entry.")
    return p.parse_args()


def main() -> None:
    args = get_args()
    attacker, defender, judge_client = build_clients(
        attacker_key=args.attacker_api_key,
        attacker_url=args.attacker_base_url,
        attacker_model=args.attacker_model,
        defender_key=args.target_api_key,
        defender_url=args.target_base_url,
        defender_model=args.target_model,
        judge_key=args.judge_api_key,
        judge_url=args.judge_base_url,
        judge_model=args.judge_model,
        attacker_temperature=args.attacker_temperature,
        attacker_extract_answer=args.attacker_answer_extract,
    )

    goals = _load_goals(args.local_dataset)
    if args.num_samples:
        goals = goals[: args.num_samples]
    print(f"[init] Using {len(goals)} goals from {args.local_dataset}")

    log_fp = open(args.log, "w", encoding="utf-8") if args.log else None

    K = NUM_STRATEGIES
    # A[i, j] success counter of strategy j after strategy i failed.
    n_fail = np.zeros(K, dtype=np.int64)
    n_succeed_after_fail = np.zeros((K, K), dtype=np.int64)

    for g_idx, goal in enumerate(goals):
        print(f"\n[init] ({g_idx + 1}/{len(goals)}) goal: {goal[:100]}")
        # Phase 1: single-strategy attempts -> populate H and F.
        failed: list[tuple[int, str]] = []  # (strategy_idx_1based, disguised_prompt)
        for i in range(1, K + 1):
            score, rating, disguised, response = _apply_init(
                attacker, defender, judge_client, i, goal
            )
            if log_fp:
                json.dump({
                    "phase": "init",
                    "goal": goal,
                    "strategy": i,
                    "score": score,
                    "rating": rating,
                    "disguised": disguised,
                    "response": response,
                }, log_fp)
                log_fp.write("\n")
                log_fp.flush()
            if score < 1.0:
                n_fail[i - 1] += 1
                failed.append((i, disguised))

        # Phase 2: composition attempts for each failed (i, disguised).
        for i_1based, disguised in failed:
            for j in range(1, K + 1):
                score, rating, new_disguised, response = _apply_compose(
                    attacker, defender, judge_client, j, goal, disguised
                )
                if log_fp:
                    json.dump({
                        "phase": "compose",
                        "goal": goal,
                        "prev_strategy": i_1based,
                        "strategy": j,
                        "score": score,
                        "rating": rating,
                        "disguised": new_disguised,
                        "response": response,
                    }, log_fp)
                    log_fp.write("\n")
                    log_fp.flush()
                if score >= 1.0:
                    n_succeed_after_fail[i_1based - 1, j - 1] += 1

    # Build the empirical attack score matrix A and its softmax.
    A = np.zeros((K, K), dtype=np.float64)
    for i in range(K):
        if n_fail[i] > 0:
            A[i] = n_succeed_after_fail[i] / float(n_fail[i])
    M = np.vstack([softmax_row(row, temperature=args.softmax_temperature) for row in A])

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    np.save(args.out, M)
    print(f"\n[init] Saved Markov transition matrix (shape {M.shape}) to {args.out}")
    print(f"[init] n_fail={n_fail.tolist()}")
    print(f"[init] n_succeed_after_fail row-sums={n_succeed_after_fail.sum(axis=1).tolist()}")

    if log_fp:
        log_fp.close()


if __name__ == "__main__":
    main()
