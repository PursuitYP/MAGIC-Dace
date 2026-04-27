# Repository Guidelines

## Project Overview

MAGIC (Multi-Agent Adversarial Game for Robust LLM Safety) is a co-evolving attacker-defender adversarial game framework for improving LLM safety. It uses online multi-agent reinforcement learning (MARL) with a bilevel game formulation (SPNE) to iteratively train safer language models through attacker-defender co-evolution.

## Project Structure & Module Organization

MAGIC is a Python research codebase for attacker-defender LLM safety training. The main implementation lives under `src/`:

- **`src/verl/`** — RL training framework (Volcano Engine RL fork). Handles GRPO-based multi-agent training with Ray distributed computing, vLLM rollouts, and FSDP model sharding.
- **`src/360-LLaMA-Factory/`** — SFT framework (LLaMA-Factory fork). Used for Phase 1 offensive initialization (attacker SFT).

Top-level training launchers are in `scripts/rl/separated/`, with `grpo_public.sh` as the main reference. Data preparation scripts and datasets are under `data/` and `data-sft/`. Prompt templates live in `prompt/`, figures and paper assets in `assets/`, and evaluation suites in `eval/` and `eval-dace/`. Generated runs, checkpoints, logs, and W&B output should stay in `outputs/`, `logs/`, and `wandb/`.

**Training pipeline flow:**
1. Phase 1: SFT attacker initialization via LLaMA-Factory.
2. Phase 2: Iterative co-evolution — alternating attacker/defender GRPO training.

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

## Build, Test, and Development Commands

Use Python 3.10 with CUDA 12.4, PyTorch 2.6, and vLLM 0.8.5.post1-compatible dependencies.

```bash
conda create -n magic python=3.10.0
conda activate magic
pip install flash-attn==2.7.4.post1 --no-build-isolation
cd src/360-LLaMA-Factory && pip install -e .
cd ../verl && pip install -e .
cd ../.. && pip install -r requirements.txt
```

Run RL training from the repository root:

```bash
bash scripts/rl/separated/grpo_public.sh
```

Before training, set environment variables such as `WANDB_API_KEY`, `WILDGUARD_API_ENDPOINT`, `WORKSPACE`, `CHECKPOINT_DIR`, `MODEL_DEFENDER_BASE`, and `MODEL_ATTACKER_SFT`. Reward shaping is controlled via `SAFETY_SCORE_MODE` (`classifier` or `rule_api`) and `REWARD_HARM`, `REWARD_REFUSAL`, etc. Training uses Hydra for config management; override values via CLI or the main training script.

## Coding Style & Naming Conventions

Use 4-space indentation for Python. In `src/360-LLaMA-Factory`, follow the configured Ruff style: double quotes, line length 119, sorted imports, and Python 3.8-compatible syntax. Prefer descriptive snake_case for functions, variables, config keys, and script names.

When modifying MAGIC-specific code, always add a standardized annotation above new or changed modules/functions, using the following format:

```python
### dace: <feature description> ###
```

Replace `<feature description>` with a concise explanation of the change or new functionality. This makes it easy to trace what was added or modified and why.

## Testing Guidelines

For LLaMA-Factory changes, run:

```bash
cd src/360-LLaMA-Factory
make style     # Format with ruff
make quality   # Check with ruff
make test      # Run pytest
```

Direct pytest run (without GPU / W&B):

```bash
CUDA_VISIBLE_DEVICES= WANDB_DISABLED=true pytest -vv tests/
```

For `verl` or top-level changes, add focused `pytest` tests when practical and run the smallest relevant subset, for example `pytest -vv src/verl/tests/...` or `python test_check.py` for syntax checks around modified training files. GPU-heavy training and evaluation changes should include the exact smoke-test command and key environment variables used.

## Evaluation

Four evaluation suites live in `eval/`:
- **safety-eval-fork/** — Safety benchmarks (HarmBench, WildGuardTest, DAN, XSTest, StrongReject)
- **olmes/** — General capability (IFEval, GPQA, ARC-C) to monitor for degradation
- **OpenRT/** — Automated red-teaming (GCG, PAIR, TAP, AutoDAN)
- **pattern/** — Attack pattern extraction and classification

See `eval/README.md` for detailed instructions.

## Data Format

Training data uses Parquet format. Each example has fields: `data_source`, `prompt` (chat format), `ability`, `question`, `data_type` (`vanilla_harmful` / `vanilla_benign`), `adversarial`, `extra_info`. Data is stored under `data/safety/`.

## Editing Guidelines

Always read and fully understand existing code before making any modifications. Never skip the exploration step — thoroughly examine the relevant files, their dependencies, and surrounding context first, then propose changes. This ensures edits are consistent with the existing codebase and avoids introducing unintended side effects.

Always keep changes minimal and goal-driven. Define a short success criterion for the task first, prefer the simplest implementation that satisfies it, and make only the edits that are directly required. This avoids speculative abstractions, adjacent cleanup, or extra configurability that was not requested, and keeps the change focused and easy to review.

## Commit & Pull Request Guidelines

Recent history uses short imperative commit messages such as `add sft script` and `update sft training script`; keep messages concise and action-oriented. Pull requests should describe the training/evaluation behavior changed, list affected scripts or configs, note required model/API paths, and include logs, metrics, or screenshots for experiment-facing changes. Avoid committing large generated artifacts unless they are required inputs.

## Security & Configuration Tips

Do not hard-code API keys, private model paths, or service endpoints. Keep secrets in environment variables and avoid committing local logs that expose prompts, keys, or internal URLs.
