# Project Overview

MAGIC (Multi-Agent Adversarial Game for Robust LLM Safety) is a research codebase focused on improving the safety and robustness of Large Language Models (LLMs) through a co-evolving adversarial game between an attacker model and a defender model.

Key aspects of the architecture:
- **Asymmetric Game:** Sequential turn-based interactions (attacker generates a prompt → defender responds), avoiding gradient conflicts found in symmetric self-play.
- **Co-evolving MARL:** Online Multi-Agent Reinforcement Learning using GRPO. The attacker learns to discover long-tail vulnerabilities, while the defender learns pointwise-safe responses.
- **Two Phases:** Phase 1 initializes offensive capabilities via SFT on a CoT-enriched Attack Pool. Phase 2 involves iterative co-evolution via alternate optimization (fixing one agent to train the other).
- **Core Technologies:** PyTorch, vLLM (for fast inference), Transformers, PEFT, and RL frameworks (`src/verl` and `src/360-LLaMA-Factory`).

# Directory Overview

- `eval/`: Contains separate evaluation pipelines for safety (`safety-eval-fork`), general capabilities (`olmes`), automated red-teaming (`OpenRT`), and attack pattern analysis (`pattern`).
- `scripts/rl/separated/`: Contains the primary bash scripts for kicking off the MARL training runs.
- `src/`: Contains the core training frameworks modified for this project (`360-LLaMA-Factory` for SFT and `verl` for RL).
- `data/` and `data-sft/`: Datasets and preprocessing scripts for training.
- `logs/` and `outputs/`: Typical directories for storing training run artifacts and evaluation results.

# Building and Running

## Environment Setup
It is recommended to use CUDA 12.4, PyTorch 2.6, and Python 3.10.

```bash
conda create -n magic python=3.10.0
conda activate magic
pip install flash-attn==2.7.4.post1 --no-build-isolation

# Install SFT and RL frameworks
cd src/360-LLaMA-Factory && pip install -e .
cd ../verl && pip install -e .

# Install dependencies
cd ../../
pip install -r requirements.txt
```

*Note: Evaluation tools in `eval/` require their own separate conda environments (e.g., `safety-eval`, `olmes`, `OpenRT`) to prevent dependency conflicts and ensure reproducibility. See `eval/README.md` for specific setup commands.*

## Training
Training scripts are located in `scripts/rl/separated/`. You must configure specific environment variables before running.

Example for running the public GRPO training script:
```bash
export WANDB_API_KEY=<API_KEY>
export WILDGUARD_API_ENDPOINT="http://<API URL>/v1"
export WORKSPACE=<ROOT_PATH>
export CHECKPOINT_DIR=<ROOT_PATH>/MAGIC/checkpoints
export MODEL_DEFENDER_BASE=$WORKSPACE/models/Qwen2.5-7B-Instruct
export MODEL_ATTACKER_SFT=$WORKSPACE/models/Qwen2.5-7B-Instruct

bash scripts/rl/separated/grpo_public.sh
```

## Evaluation
Evaluation is modularized. To evaluate safety models, deploy a Guard classifier API (e.g., Qwen3Guard or WildGuard) and run:

```bash
cd eval/safety-eval-fork
# Ensure the safety-eval conda environment is active
python -u evaluation/eval.py generators \
  --model_name_or_path "$MODEL_PATH" \
  --model_input_template_path_or_name "game_defender" \
  --tasks "harmbench" \
  --report_output_path "$safety_dir/metrics.json" \
  --use_vllm \
  --classifier_model_name "Qwen3GuardAPI"
```
Refer to `eval/README.md` for evaluating general capabilities (OLMES) or running automated red-teaming (OpenRT).

# Development Conventions

- **Modular Environments:** Always switch to the appropriate conda environment when working in `eval/` subdirectories. Do not pollute the main `magic` training environment with evaluation dependencies.
- **Configuration over Code:** Training hyperparameters, agent switching frequency, reward formulas, and model paths are heavily parameterized in bash scripts and YAML configs. Modify these scripts/configs rather than hardcoding values in Python.
- **Safety APIs:** The pipeline relies on external or locally hosted API endpoints for moderation models (e.g., WildGuard) during both training rewards and evaluation. Ensure these endpoints are mockable or accessible during development.