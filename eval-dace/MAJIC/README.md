# MAJIC: Markovian Adaptive Jailbreaking via Iterative Composition of Diverse Innovative Strategies

Fork of [MAJIC (AAAI 2026)](https://arxiv.org/abs/2508.13048) adapted to the
**eval-dace** pipeline (`eval-dace/OpenRT/run_eval.sh`) so MAJIC can be run as
a Table 3 attack alongside PAIR / TAP / AutoDAN-turbo-r against the DACE
defender.

## What's different from upstream

The upstream repo (`methods/`, `markov_methods/`, `majic.py`) relies on
HuggingFace pipelines and contains placeholder API keys (`"xxx"`), making it
unrunnable as-is. We keep the upstream sources untouched (they document the
10 disguise-strategy prompt templates) and add a thin adapter under
`majic_eval/` that:

- talks only to OpenAI-compatible Chat Completions endpoints (DACE defender,
  base-attacker, GPT-4o judge) so it matches `OpenRT/run_eval.sh`;
- implements the paper's Markov matrix, Q-learning update, α-decay and
  β-reset faithfully;
- exposes all **three Table-4 matrix initialization modes** via one env var.

## Quickstart

```bash
conda activate OpenRT            # openai / numpy / pandas / tqdm are already installed
cd eval-dace/MAJIC
bash run_majic.sh                # defaults: uniform init + HarmBench CSV
```

Results are written to
`results/dace/<MODEL_NAME>-<ts>/majic/{history,summary,majic}_*.{json,log}`
using the same file layout as `OpenRT/unified_eval.py::save_results`.

## How to run

### 1. Activate the env and enter the MAJIC dir

```bash
conda activate OpenRT
cd eval-dace/MAJIC
```

### 2. Configure endpoints (optional — defaults match `OpenRT/run_eval.sh`)

`run_majic.sh` reads the same env vars as the OpenRT launcher; override only
what you need:

```bash
# DACE defender (victim)
export DEFENDER_API_BASE_URL="http://<defender-host>:<port>/v1"
export DEFENDER_API_KEY="FAKE_API_KEY"
export DEFENDER_API_MODEL="orm"

# Base attacker (Qwen / Llama / Mistral — whatever you self-deploy)
export ATTACKER_API_BASE_URL="http://<attacker-host>:<port>/v1"
export ATTACKER_API_KEY="FAKE_API_KEY"
export ATTACKER_API_MODEL="orm"
export ATTACKER_ANSWER_EXTRACT="true"   # set to "false" if attacker doesn't emit <answer>...</answer>

# GPT-4o judge (OpenAI-compatible)
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="http://<judge-host>:<port>/v1/"
export JUDGE_MODEL="gpt-4o"

# Naming for output dir
export MODEL_NAME="DACE-Qwen2.5-7B-full-step300"
```

### 3. Default run (uniform init, HarmBench CSV)

```bash
bash run_majic.sh
```

### 4. Smoke test (2 prompts, 1-step chain)

```bash
NUM_SAMPLES=2 \
MAJIC_CHAIN_COUNT=1 MAJIC_CHAIN_LENGTH=1 \
bash run_majic.sh
```

### 5. Switch the matrix initialization mode

| `MAJIC_INIT_MODE` | Variant | Paper ASR on GPT-4o | Needs `.npy`? |
| --- | --- | --- | --- |
| `uniform` (default) | MAJIC(–Init) | 70.3% | No |
| `learned` | Full MAJIC | 95.7% | Yes |
| `learned_static` | MAJIC(–DynUpd) | 76.5% | Yes |

```bash
# uniform (default; MAJIC(-Init), Table 4)
MAJIC_INIT_MODE=uniform bash run_majic.sh

# learned: full MAJIC -- requires a pre-built 10x10 matrix
MAJIC_INIT_MODE=learned \
MAJIC_INIT_MATRIX="$PWD/markov_methods/init_matrix.npy" \
bash run_majic.sh

# learned_static: MAJIC(-DynUpd) -- frozen matrix, no Q-learning update
MAJIC_INIT_MODE=learned_static \
MAJIC_INIT_MATRIX="$PWD/markov_methods/init_matrix.npy" \
bash run_majic.sh
```

### 6. Switch the dataset

```bash
# HarmBench CSV (default, aligned with run_eval.sh)
DATASET_PATH=/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/seed/harmbench/harmbench_behaviors_text_test.csv \
bash run_majic.sh

# MAJIC repo-internal 400-prompt JSON
DATASET_PATH=data/harmbench400.json bash run_majic.sh

# 50-sample subset bundled with the repo
DATASET_PATH=data/harmful_behaviors_50.json bash run_majic.sh
```

### 7. Build the learned matrix (offline, one-time)

Required only for `MAJIC_INIT_MODE=learned` / `learned_static`:

```bash
python -m majic_eval.build_init_matrix \
    --target-api-key "$DEFENDER_API_KEY" --target-base-url "$DEFENDER_API_BASE_URL" --target-model "$DEFENDER_API_MODEL" \
    --attacker-api-key "$ATTACKER_API_KEY" --attacker-base-url "$ATTACKER_API_BASE_URL" --attacker-model "$ATTACKER_API_MODEL" \
    --judge-api-key "$OPENAI_API_KEY"  --judge-base-url "$OPENAI_BASE_URL"  --judge-model gpt-4o \
    --local-dataset data/harmful_behaviors_50.json \
    --out markov_methods/init_matrix.npy
```

### 8. Run the orchestrator directly (for ad-hoc flag tweaking)

`run_majic.sh` is a thin shell wrapper around the same Python entry point
used by every other Table-3 attack; you can call it directly:

```bash
python -m majic_eval.runner \
    --target-api-key "$DEFENDER_API_KEY" --target-base-url "$DEFENDER_API_BASE_URL" --target-model "$DEFENDER_API_MODEL" \
    --attacker-api-key "$ATTACKER_API_KEY" --attacker-base-url "$ATTACKER_API_BASE_URL" --attacker-model "$ATTACKER_API_MODEL" \
    --judge-api-key "$OPENAI_API_KEY"  --judge-base-url "$OPENAI_BASE_URL"  --judge-model gpt-4o \
    --dataset-path /mnt/shared-storage-user/.../harmbench_behaviors_text_test.csv \
    --init-mode uniform \
    --chain-count 10 --chain-length 3 \
    --results-dir ./results/dace/$MODEL_NAME-$(date +%Y%m%d_%H%M%S) \
    --attacker-answer-extract
```

### 9. Inspect the results

After a run finishes:

```bash
# Top-level artefacts
ls results/dace/<MODEL_NAME>-<ts>/majic/
#   history_<ts>.json   per-sample AttackResult dicts + chain history
#   summary_<ts>.json   attack-success-rate, avg-queries, init mode, matrix snapshots
#   majic_<ts>.log      mirrored stdout (DualLogger)

# Quick ASR / AQC peek
python - <<'PY'
import json, glob, os
for s in sorted(glob.glob("results/dace/*/majic/summary_*.json"))[-1:]:
    with open(s) as f: m = json.load(f)["metrics"]
    print(s)
    print(f"  init_mode={m['init_mode']}  ASR={m['attack_success_rate']:.2%}  "
          f"AQC={m['avg_queries_per_sample']:.1f}  matrix_changed={m['matrix_changed']}")
PY
```

## Entry points

| File | Purpose |
| --- | --- |
| `run_majic.sh` | Shell launcher; mirrors `eval-dace/OpenRT/run_eval.sh`. |
| `majic_eval/runner.py` | Attack orchestrator (`python -m majic_eval.runner ...`). |
| `majic_eval/build_init_matrix.py` | Offline matrix initialization tool. |
| `majic_eval/strategies.py` | 10-strategy disguise prompts (carved from `methods/`). |
| `majic_eval/markov.py` | Markov transition matrix + three init modes. |
| `majic_eval/judge.py` | PAIR-style GPT-4o judge (OpenAI-compatible). |
| `majic_eval/api_client.py` | Chat client + credential resolution. |
| `methods/`, `markov_methods/` | Upstream research artifacts (kept for reference). |

## Citation

```bibtex
@inproceedings{qi2026majic,
  title={Majic: Markovian adaptive jailbreaking via iterative composition of diverse innovative strategies},
  author={Qi, Weiwei and Shao, Shuo and Gu, Wei and Zheng, Tianhang and Zhao, Puning and Qin, Zhan and Ren, Kui},
  booktitle={Proceedings of the AAAI Conference on Artificial Intelligence},
  volume={40},
  number={39},
  pages={32755--32763},
  year={2026}
}
```

## License

MIT (see LICENSE).
