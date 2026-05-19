"""MAJIC evaluation orchestrator.

Runs the MAJIC attack against an OpenAI-compatible defender endpoint, using
an OpenAI-compatible attacker endpoint to produce disguised prompts and
GPT-4o (also OpenAI-compatible) as the judge.

Outputs match OpenRT/unified_eval.py::save_results so downstream aggregation
across Table 3 stays consistent:

    <results-dir>/majic/
        history_<ts>.json   # per-sample AttackResult-like dicts + chain history
        summary_<ts>.json   # {"attack": "majic", "metrics": {...}}
        majic_<ts>.log      # mirrored stdout
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional

import numpy as np

from .api_client import ChatClient, build_clients
from .judge import judge_score
from .markov import (
    DEFAULT_ALPHA,
    DEFAULT_BETA,
    DEFAULT_DECAY_ETA,
    DEFAULT_DECAY_INTERVAL,
    DEFAULT_GAMMA,
    DEFAULT_RESET_INTERVAL,
    DEFAULT_TEMPERATURE,
    FAIL_REWARD,
    INIT_MODES,
    SUCCESS_REWARD,
    MatrixController,
)
from .strategies import NUM_STRATEGIES, get_strategy, strategy_names


# ---------------------------------------------------------------------------
# Utilities (DualLogger + dataset loaders mirror OpenRT/unified_eval.py).
# ---------------------------------------------------------------------------

class DualLogger:
    def __init__(self, filepath: str) -> None:
        self.terminal = sys.stdout
        self.log = open(filepath, "w", encoding="utf-8")

    def write(self, message: str) -> None:
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    def flush(self) -> None:
        self.terminal.flush()
        self.log.flush()

    def close(self) -> None:
        self.log.close()


def load_prompts(
    dataset_path: str,
    dataset_column: str,
    jsonl_field: str,
    num_samples: Optional[int],
    start_index: int,
) -> List[str]:
    prompts: List[str] = []
    lower = dataset_path.lower()
    if lower.endswith(".csv"):
        with open(dataset_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if dataset_column not in reader.fieldnames:
                raise ValueError(
                    f"Column '{dataset_column}' not found in {dataset_path}. "
                    f"Available columns: {reader.fieldnames}"
                )
            for row in reader:
                val = row.get(dataset_column, "")
                if val:
                    prompts.append(val)
    elif lower.endswith(".jsonl"):
        with open(dataset_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                val = record.get(jsonl_field) or record.get("goal") or record.get("prompt")
                if val:
                    prompts.append(val)
    elif lower.endswith(".json"):
        with open(dataset_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            for item in data:
                if isinstance(item, str):
                    prompts.append(item)
                elif isinstance(item, dict):
                    val = (
                        item.get("goal")
                        or item.get(jsonl_field)
                        or item.get(dataset_column)
                        or item.get("prompt")
                    )
                    if val:
                        prompts.append(val)
        else:
            raise ValueError(f"Unexpected JSON structure in {dataset_path}.")
    else:
        raise ValueError(f"Unsupported dataset extension: {dataset_path}")

    total = len(prompts)
    end = start_index + num_samples if num_samples else total
    return prompts[start_index:end]


# ---------------------------------------------------------------------------
# Strategy application (attacker + victim + judge for a single disguise step).
# ---------------------------------------------------------------------------

def _run_strategy_step(
    *,
    attacker: ChatClient,
    defender: ChatClient,
    judge_client: ChatClient,
    goal: str,
    strategy_idx: int,
    prev_disguised: Optional[str],
    iter_num: int,
    suffix: Optional[str],
) -> Dict[str, Any]:
    """Run ``iter_num`` attempts for a single strategy, keep the best.

    Returns a dict with ``score, rating, disguised_prompt, victim_response, logs``.
    """
    strategy = get_strategy(strategy_idx)
    best = {
        "score": -1.0,
        "rating": 0,
        "disguised_prompt": "",
        "victim_response": "",
        "logs": [],
    }

    for attempt in range(iter_num):
        if prev_disguised is None:
            attacker_prompt = strategy.render_init(goal)
        else:
            attacker_prompt = strategy.render_compose(goal, prev_disguised)

        disguised = attacker.chat(
            [{"role": "user", "content": attacker_prompt}],
            temperature=attacker.temperature,
        )
        disguised = (disguised or "").strip().strip('"')
        if not disguised or disguised.startswith("API_ERROR"):
            # fallback: just send the original goal so downstream judge has
            # something to score and we don't silently drop a query.
            disguised = goal

        # Victim suffix (reverse strategy needs a specific follow-up).
        victim_prompt = disguised
        if strategy.victim_suffix:
            victim_prompt = disguised + strategy.victim_suffix
        if suffix and suffix.lower() != "none":
            victim_prompt = victim_prompt + " " + suffix

        victim_response = defender.chat(
            [{"role": "user", "content": victim_prompt}],
            temperature=defender.temperature,
        )

        score, rating = judge_score(judge_client, goal, victim_response)
        step_log = {
            "strategy": strategy.short,
            "attempt": attempt,
            "disguised_prompt": disguised,
            "victim_prompt": victim_prompt,
            "victim_response": victim_response,
            "rating": rating,
            "score": score,
        }
        best["logs"].append(step_log)

        if score > best["score"]:
            best["score"] = score
            best["rating"] = rating
            best["disguised_prompt"] = disguised
            best["victim_response"] = victim_response

        if best["score"] >= 1.0:
            break

    return best


# ---------------------------------------------------------------------------
# Main loop.
# ---------------------------------------------------------------------------

def _env_float(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name, default))
    except (ValueError, TypeError):
        return default


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except (ValueError, TypeError):
        return default


def get_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="MAJIC attack evaluation (eval-dace adapter).")
    # API credentials (legacy + per-role; parallels OpenRT/unified_eval.py).
    p.add_argument("--target-api-key", default=None)
    p.add_argument("--target-base-url", default=None)
    p.add_argument("--target-model", default=None)
    p.add_argument("--attacker-api-key", default=None)
    p.add_argument("--attacker-base-url", default=None)
    p.add_argument("--attacker-model", default=None)
    p.add_argument("--judge-api-key", default=None)
    p.add_argument("--judge-base-url", default=None)
    p.add_argument("--judge-model", default=None)
    p.add_argument(
        "--attacker-answer-extract",
        action="store_true",
        help="Extract <answer>...</answer> blocks from attacker outputs.",
    )
    p.add_argument("--attacker-temperature", type=float, default=0.9)

    # Dataset.
    p.add_argument("--dataset-path", required=True)
    p.add_argument("--dataset-column", default="Behavior")
    p.add_argument("--dataset-jsonl-field", default="vanilla")
    p.add_argument("--num-samples", type=int, default=None)
    p.add_argument("--start-index", type=int, default=0)

    # MAJIC hyper-params.
    p.add_argument("--chain-count", type=int, default=10)
    p.add_argument("--chain-length", type=int, default=3)
    p.add_argument("--init-qnum", type=int, default=1, help="Attempts for the initial strategy.")
    p.add_argument("--chain-qnum", type=int, default=1, help="Attempts per composition step.")
    p.add_argument("--init-mode", choices=INIT_MODES, default="uniform")
    p.add_argument("--init-matrix-path", default=None)
    p.add_argument("--alpha", type=float, default=DEFAULT_ALPHA)
    p.add_argument("--gamma", type=float, default=DEFAULT_GAMMA)
    p.add_argument("--beta", type=float, default=DEFAULT_BETA)
    p.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    p.add_argument("--decay-eta", type=float, default=DEFAULT_DECAY_ETA)
    p.add_argument("--decay-interval", type=int, default=DEFAULT_DECAY_INTERVAL)
    p.add_argument("--reset-interval", type=int, default=DEFAULT_RESET_INTERVAL)
    p.add_argument("--suffix", default="none", help="Optional suffix appended to every victim prompt.")

    # Output.
    p.add_argument("--results-dir", required=True)

    return p.parse_args()


def run(args: argparse.Namespace) -> Dict[str, Any]:
    # --- Directory setup ---------------------------------------------------
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    attack_dir = os.path.join(args.results_dir, "majic")
    os.makedirs(attack_dir, exist_ok=True)
    log_file = os.path.join(attack_dir, f"majic_{timestamp}.log")
    history_file = os.path.join(attack_dir, f"history_{timestamp}.json")
    summary_file = os.path.join(attack_dir, f"summary_{timestamp}.json")
    logger = DualLogger(log_file)
    original_stdout = sys.stdout
    sys.stdout = logger

    try:
        print("\n>>> Running MAJIC Attack <<<")
        print(f"Log file:      {log_file}")
        print(f"History file:  {history_file}")
        print(f"Summary file:  {summary_file}")

        # --- Credentials + clients ----------------------------------------
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
        print(f"Target Model (defender): {defender.cfg.model} @ {defender.cfg.base_url}")
        print(f"Attacker Model:          {attacker.cfg.model} @ {attacker.cfg.base_url}")
        print(f"Judge Model:             {judge_client.cfg.model} @ {judge_client.cfg.base_url}")
        print(f"Attacker answer extract: {args.attacker_answer_extract}")

        # --- Matrix controller --------------------------------------------
        controller = MatrixController.build(
            mode=args.init_mode,
            k=NUM_STRATEGIES,
            init_matrix_path=args.init_matrix_path,
            alpha=args.alpha,
            gamma=args.gamma,
            beta=args.beta,
            temperature=args.temperature,
            decay_eta=args.decay_eta,
            decay_interval=args.decay_interval,
            reset_interval=args.reset_interval,
        )
        print(
            f"Init mode: {controller.mode} (updates_enabled={controller.updates_enabled})"
        )
        print(f"Strategy pool: {strategy_names()}")
        initial_matrix_snapshot = controller.snapshot()

        # --- Dataset -------------------------------------------------------
        prompts = load_prompts(
            args.dataset_path,
            args.dataset_column,
            args.dataset_jsonl_field,
            args.num_samples,
            args.start_index,
        )
        print(f"Loaded {len(prompts)} prompts from {args.dataset_path}")

        rng = np.random.default_rng()

        # --- Attack loop ---------------------------------------------------
        results: List[Dict[str, Any]] = []
        success_count = 0
        total_queries = 0
        matrix_hash_before = hash(controller.matrix.tobytes())

        for idx, goal in enumerate(prompts):
            print(f"\n[MAJIC {idx + 1}/{len(prompts)}] goal: {goal[:120]}")
            chain_history: List[Dict[str, Any]] = []
            chain_queries = 0
            best_score = -1.0
            best_rating = 0
            best_prompt = ""
            best_response = ""
            best_strategy_short = ""
            success = False

            for chain_i in range(args.chain_count):
                init_idx = controller.sample_initial(rng)
                chain_queries += args.init_qnum
                total_queries += args.init_qnum
                init_result = _run_strategy_step(
                    attacker=attacker,
                    defender=defender,
                    judge_client=judge_client,
                    goal=goal,
                    strategy_idx=init_idx,
                    prev_disguised=None,
                    iter_num=args.init_qnum,
                    suffix=args.suffix,
                )
                chain_history.append(
                    {
                        "chain": chain_i,
                        "step": "init",
                        "strategy_idx": init_idx,
                        "strategy": get_strategy(init_idx).short,
                        **{k: v for k, v in init_result.items() if k != "logs"},
                        "attempts": init_result["logs"],
                    }
                )

                if init_result["score"] > best_score:
                    best_score = init_result["score"]
                    best_rating = init_result["rating"]
                    best_prompt = init_result["disguised_prompt"]
                    best_response = init_result["victim_response"]
                    best_strategy_short = get_strategy(init_idx).short

                if init_result["score"] >= 1.0:
                    success = True
                    break

                failed_idx = init_idx
                failed_disguised = init_result["disguised_prompt"]

                for step_i in range(args.chain_length):
                    next_idx = controller.sample_next(failed_idx, rng)
                    chain_queries += args.chain_qnum
                    total_queries += args.chain_qnum
                    step_result = _run_strategy_step(
                        attacker=attacker,
                        defender=defender,
                        judge_client=judge_client,
                        goal=goal,
                        strategy_idx=next_idx,
                        prev_disguised=failed_disguised,
                        iter_num=args.chain_qnum,
                        suffix=args.suffix,
                    )
                    reward = SUCCESS_REWARD if step_result["score"] >= 1.0 else FAIL_REWARD
                    controller.apply_periodic_schedule(total_queries)
                    controller.update_on_feedback(failed_idx, next_idx, reward)

                    chain_history.append(
                        {
                            "chain": chain_i,
                            "step": step_i,
                            "strategy_idx": next_idx,
                            "strategy": get_strategy(next_idx).short,
                            "prev_strategy_idx": failed_idx,
                            "reward": reward,
                            **{k: v for k, v in step_result.items() if k != "logs"},
                            "attempts": step_result["logs"],
                        }
                    )

                    if step_result["score"] > best_score:
                        best_score = step_result["score"]
                        best_rating = step_result["rating"]
                        best_prompt = step_result["disguised_prompt"]
                        best_response = step_result["victim_response"]
                        best_strategy_short = get_strategy(next_idx).short

                    if step_result["score"] >= 1.0:
                        success = True
                        break

                    failed_idx = next_idx
                    failed_disguised = step_result["disguised_prompt"]

                if success:
                    break

            if success:
                success_count += 1

            result_entry: Dict[str, Any] = {
                "target": goal,
                "success": success,
                "final_prompt": best_prompt,
                "output_text": best_response,
                "method": "majic",
                "best_score": best_score,
                "best_rating": best_rating,
                "best_strategy": best_strategy_short,
                "query_num": chain_queries,
                "history": chain_history,
            }
            results.append(result_entry)

            # Incremental save -- so a long run won't lose everything on a crash.
            _write_json(history_file, {
                "attack": "majic",
                "timestamp": timestamp,
                "args": _args_to_serializable(args),
                "results": results,
            })
            print(
                f"  -> success={success} best_rating={best_rating} "
                f"queries={chain_queries} total_queries={total_queries}"
            )

        # --- Summary -------------------------------------------------------
        matrix_hash_after = hash(controller.matrix.tobytes())
        asr = success_count / len(results) if results else 0.0
        avg_queries = (total_queries / len(results)) if results else 0.0
        metrics = {
            "attack": "majic",
            "init_mode": controller.mode,
            "attack_success_rate": asr,
            "total_samples": len(results),
            "success_count": success_count,
            "total_queries": total_queries,
            "avg_queries_per_sample": avg_queries,
            "matrix_changed": matrix_hash_before != matrix_hash_after,
            "strategy_pool": strategy_names(),
            "final_alpha": controller.alpha,
            "initial_matrix_snapshot": initial_matrix_snapshot,
            "final_matrix_snapshot": controller.snapshot(),
        }
        _write_json(summary_file, {
            "attack": "majic",
            "timestamp": timestamp,
            "args": _args_to_serializable(args),
            "metrics": metrics,
        })

        print(f"\nMAJIC attack finished. ASR={asr:.2%} avg_queries={avg_queries:.2f}")
        print(f"History: {os.path.abspath(history_file)}")
        print(f"Summary: {os.path.abspath(summary_file)}")
        return metrics

    finally:
        sys.stdout = original_stdout
        logger.close()


def _args_to_serializable(args: argparse.Namespace) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, v in vars(args).items():
        if "key" in k:
            out[k] = "***REDACTED***" if v else ""
        else:
            out[k] = v
    return out


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, default=str)
    os.replace(tmp, path)


def main() -> None:
    args = get_args()
    run(args)


if __name__ == "__main__":
    main()
