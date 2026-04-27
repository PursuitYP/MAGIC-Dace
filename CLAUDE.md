# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MAGIC (Multi-Agent Adversarial Game for Robust LLM Safety) is a co-evolving attacker-defender adversarial game framework for improving LLM safety. It uses online multi-agent reinforcement learning (MARL) with bilevel game formulation (SPNE) to iteratively train safer language models through attacker-defender co-evolution.

## Architecture

The codebase has two core subsystems:

- **`src/verl/`** — RL training framework (Volcano Engine RL fork). Handles GRPO-based multi-agent training with Ray distributed computing, vLLM rollouts, and FSDP model sharding.
- **`src/360-LLaMA-Factory/`** — SFT framework (LLaMA-Factory fork). Used for Phase 1 offensive initialization (attacker SFT).

**Training pipeline flow:**
1. Phase 1: SFT attacker initialization via LLaMA-Factory
2. Phase 2: Iterative co-evolution — alternating attacker/defender GRPO training

**Key entry point chain:**
```
scripts/rl/separated/grpo_public.sh
  → python -m verl.separated_trainer.main_ppo
    → RayReMASeparatedTrainer (ray_trainer.py)
```

**Critical files:**
- `src/verl/verl/separated_trainer/main_ppo.py` — Main training loop
- `src/verl/verl/separated_trainer/ppo/ray_trainer.py` — Ray trainer with agent switching logic
- `src/verl/verl/utils/reward_score/game.py` — Game reward computation (harm, refusal, format rewards)
- `src/verl/verl/separated_trainer/config/ppo_trainer.yaml` — Default Hydra config
- `src/verl/verl/protocol.py` — DataProto: TensorDict-based inter-component data protocol
- `data/safety/preprocess.py` — Data conversion (JSONL → Parquet)
- `prompt/game/` — Attacker/defender prompt templates (single-turn and multi-turn)

## Build & Installation

```bash
conda create -n magic python=3.10.0
conda activate magic
pip install flash-attn==2.7.4.post1 --no-build-isolation
cd src/360-LLaMA-Factory && pip install -e .
cd ../verl && pip install -e .
pip install -r requirements.txt
```

Requires CUDA 12.4, PyTorch 2.6.0, vLLM 0.8.5.post1.

## Linting & Testing

LLaMA-Factory submodule uses ruff (line length 119, target py38):
```bash
cd src/360-LLaMA-Factory
make style     # Format with ruff
make quality   # Check with ruff
make test      # Run pytest
```

Run tests directly:
```bash
CUDA_VISIBLE_DEVICES= WANDB_DISABLED=true pytest -vv tests/
```

## Configuration

Uses Hydra for config management. Override via CLI or the main training script. Key environment variables:
- `WANDB_API_KEY` — Experiment tracking
- `WILDGUARD_API_ENDPOINT` — Safety classifier API URL
- `WORKSPACE` — Root path for models/data
- `CHECKPOINT_DIR` — Checkpoint save location
- `MODEL_DEFENDER_BASE` / `MODEL_ATTACKER_SFT` — Model paths
- `SAFETY_SCORE_MODE` — "classifier" or "rule_api"
- `REWARD_HARM`, `REWARD_REFUSAL`, etc. — Reward shaping parameters

## Evaluation

Four evaluation suites in `eval/`:
- **safety-eval-fork/** — Safety benchmarks (HarmBench, WildGuardTest, DAN, XSTest, StrongReject)
- **olmes/** — General capability (IFEval, GPQA, ARC-C) to monitor for degradation
- **OpenRT/** — Automated red-teaming (GCG, PAIR, TAP, AutoDAN)
- **pattern/** — Attack pattern extraction and classification

See `eval/README.md` for detailed instructions.

## Code Comment Convention

When modifying code, always add a standardized annotation comment above the new or changed module/function, using the following format:

```
### dace: <feature description> ###
```

Replace `<feature description>` with a concise explanation of the change or new functionality. This makes it easy to trace what was added or modified and why.

**Example:**
```python
### dace: add multi-turn reward scaling for defender ###
def compute_defender_reward(responses, turn_count):
    ...
```

## Editing Guidelines

Always read and fully understand existing code before making any modifications. Never skip the exploration step — thoroughly examine the relevant files, their dependencies, and surrounding context first, then propose changes. This ensures edits are consistent with the existing codebase and avoids introducing unintended side effects.

Always keep changes minimal and goal-driven. Define a short success criterion for the task first, prefer the simplest implementation that satisfies it, and make only the edits that are directly required. This avoids speculative abstractions, adjacent cleanup, or extra configurability that was not requested, and keeps the change focused and easy to review.

## Data Format

Training data uses Parquet format. Each example has fields: `data_source`, `prompt` (chat format), `ability`, `question`, `data_type` (vanilla_harmful/vanilla_benign), `adversarial`, `extra_info`. Data stored in `data/safety/`.
