# Repository Guidelines

## Project Structure & Module Organization

MAGIC is a Python research codebase for attacker-defender LLM safety training. The main implementation lives under `src/`: `src/verl/` contains the RL/GRPO training stack and `src/360-LLaMA-Factory/` contains the SFT stack. Top-level training launchers are in `scripts/rl/separated/`, with `grpo_public.sh` as the main reference. Data preparation scripts and datasets are under `data/` and `data-sft/`. Prompt templates live in `prompt/`, figures and paper assets in `assets/`, and evaluation suites in `eval/` and `eval-dace/`. Generated runs, checkpoints, logs, and W&B output should stay in `outputs/`, `logs/`, and `wandb/`.

## Build, Test, and Development Commands

Use Python 3.10 with CUDA 12.4, PyTorch 2.6, and vLLM 0.8.5-compatible dependencies.

```bash
pip install flash-attn==2.7.4.post1 --no-build-isolation
cd src/360-LLaMA-Factory && pip install -e .
cd ../verl && pip install -e .
cd ../.. && pip install -r requirements.txt
```

Run RL training from the repository root:

```bash
bash scripts/rl/separated/grpo_public.sh
```

Before training, set environment variables such as `WANDB_API_KEY`, `WILDGUARD_API_ENDPOINT`, `WORKSPACE`, `CHECKPOINT_DIR`, `MODEL_DEFENDER_BASE`, and `MODEL_ATTACKER_SFT`.

## Coding Style & Naming Conventions

Use 4-space indentation for Python. In `src/360-LLaMA-Factory`, follow the configured Ruff style: double quotes, line length 119, sorted imports, and Python 3.8-compatible syntax. Prefer descriptive snake_case for functions, variables, config keys, and script names. When modifying MAGIC-specific code, add a concise annotation above changed modules/functions:

```python
### dace: add multi-turn reward scaling ###
```

## Testing Guidelines

For LLaMA-Factory changes, run:

```bash
cd src/360-LLaMA-Factory
make style
make quality
make test
```

For `verl` or top-level changes, add focused `pytest` tests when practical and run the smallest relevant subset, for example `pytest -vv src/verl/tests/...` or `python test_check.py` for syntax checks around modified training files. GPU-heavy training and evaluation changes should include the exact smoke-test command and key environment variables used.

## Commit & Pull Request Guidelines

Recent history uses short imperative commit messages such as `add sft script` and `update sft training script`; keep messages concise and action-oriented. Pull requests should describe the training/evaluation behavior changed, list affected scripts or configs, note required model/API paths, and include logs, metrics, or screenshots for experiment-facing changes. Avoid committing large generated artifacts unless they are required inputs.

## Security & Configuration Tips

Do not hard-code API keys, private model paths, or service endpoints. Keep secrets in environment variables and avoid committing local logs that expose prompts, keys, or internal URLs.
