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

### Known Issue: tiktoken offline-download hang (huge eval slowdown)

On offline GPU/compute nodes, `tiktoken` blocks trying to fetch its BPE vocab from `openaipublic.blob.core.windows.net`. Because `tiktoken.get_encoding` holds a global registry lock, the first thread stalls on the download timeout while **all other worker threads serialize behind the lock** — turning a ~1s op into ~131s/call and slowing the whole eval ~40x. Symptom in `py-spy dump --pid <pid>`: workers stuck in `tiktoken/registry.py get_encoding`, one in `urllib3 create_connection`; process `wchan=futex_wait_queue_me`. The LLM endpoints (attacker/target/judge) are NOT the cause even when judge calls appear right after the slow op in logs.

Fix = point `TIKTOKEN_CACHE_DIR` at a pre-populated cache. The cache filename must be `sha1(<download_url>).hexdigest()` (not the original filename). Two suites need **different vocabs**:

- **x-teaming** (`eval-dace/safety-eval-fork/.../x-teaming/`, conda env `x-teaming`, py3.11) — needs **`o200k_base`** (for `gpt-4o-2024-08-06`). Download URL `https://openaipublic.blob.core.windows.net/encodings/o200k_base.tiktoken` (expected sha256 `446a9538...`), cache key `fb374d419588a4632f3f557e76b4b70aebbca790`. **Two separate scripts call `tiktoken.encoding_for_model("gpt-4o-2024-08-06")` and each needs the fix independently** — the attack run (`agents/target_model.py:truncate_response()`) AND the metrics step (`analytics/metrics.py:count_tokens()`, runs as `python analytics/metrics.py <timestamp> -v`; `metrics.py` is a standalone entrypoint that does NOT import `target_model`). Both fixed in-code via `os.environ.setdefault("TIKTOKEN_CACHE_DIR", "/home/yupeng/.cache/tiktoken")` before `import tiktoken` (set before first `encoding_for_model` call; env var is read at lookup time). A verified copy of the vocab exists at `/mnt/shared-storage-user/wenxiaoyu/models/gptencodings/o200k_base.tiktoken`.
- **olmes** (`eval-dace/olmes/`, conda env `olmes`, py3.10) — uses litellm's **`cl100k_base`**. Fixed in `run_7_benchmarks_eval.sh` via `export TIKTOKEN_CACHE_DIR=$CONDA_PREFIX/lib/python3.10/site-packages/litellm/litellm_core_utils/tokenizers`. Note: litellm only bundles `cl100k_base`, so this dir does NOT satisfy x-teaming's `o200k_base` need.

Debugging lesson: when a process is slow but the LLM endpoints test fast in isolation, `py-spy dump` the running PID to read thread stacks instead of guessing from log timestamps. Verify you're probing in the **same conda env** that runs the benchmark (the base env may lack `textgrad`/`openai`).

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
