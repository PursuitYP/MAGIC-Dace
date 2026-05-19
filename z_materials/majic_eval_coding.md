# Plan: Integrate MAJIC Attack into the eval-dace Defender Generalization Suite

## Context

The MAJIC paper (`z_materials/MAJIC.pdf`, AAAI 2026) proposes a black-box jailbreak:
a 10-strategy **Disguise Strategy Pool** (Hypothetical / Historical / Spatial /
Reverse / Security / Word / Char / Literary / Language / Emoji) combined with a
**Markov Transition Matrix** that is dynamically updated by a Q-learning-inspired
rule (`M_ij <- M_ij + α(r + γ max_k M_jk − M_ij)`) with learning-rate decay
(`α *= η`) and periodic uniform-reset (`M <- (1-β)M + β/K`). The authors claim
>90% ASR at <15 queries on GPT-4o/Gemini-2.0, and our Table-3 pipeline
(`eval-dace/OpenRT/run_eval.sh`) uses PAIR/TAP/AutoDAN-turbo-r against the
DACE defender. Adding MAJIC gives a **stronger upper-bound attack** to
demonstrate the DACE defender's robustness.

The upstream MAJIC code at `eval-dace/MAJIC/` is a half-ported research dump:
every `methods/m*_attackLLM.py` still uses HuggingFace pipelines and
hard-coded `"xxx"` API keys, and `markov_methods/markov_attack_api_dynamic.py`
does not load (imports `m4_dialogue_attackLLM` which is named
`m4_reverse_attackLLM.py` in this repo, references a missing `methods.csv`,
uses `exec`-level side effects, etc.). It cannot run today.

**Goal:** make MAJIC runnable out-of-the-box under `conda activate openrt`,
consuming the same endpoints as `OpenRT/run_eval.sh` (DACE defender API,
base-attacker API, GPT-4o judge), writing results into the same
`results/dace/$MODEL_NAME-.../majic/` tree used by the other Table-3 attacks.

## User Decisions (already collected)

- **Attacker:** reuse the `ATTACKER_API_BASE_URL`/`ATTACKER_API_MODEL` from
  `run_eval.sh` (base-attacker endpoint). The actual backend model is flexible
  (Qwen / Llama / Mistral — whatever the user self-deploys); our code must stay
  model-agnostic and only speak the OpenAI-compatible Chat API. Do **not** spin
  up a separate Mistral/Llama endpoint.
- **Defender:** reuse `DEFENDER_API_BASE_URL`/`DEFENDER_API_MODEL` (dace-defender).
- **Judge:** GPT-4o via `OPENAI_API_KEY`/`OPENAI_BASE_URL`.
- **Dataset:** support both HarmBench CSV (aligned with `run_eval.sh`) and the
  built-in `data/harmbench400.json`; switch via env var in the shell wrapper.
- **Matrix init:** implement **all three Table-4 variants** and select at runtime
  via `MAJIC_INIT_MODE` env var:
  | Mode | Variant | Behaviour |
  | --- | --- | --- |
  | `uniform` (**default**) | MAJIC(–Init) | `M_ij = 1/K` start + dynamic Q-learning update (ASR 70.3% on GPT-4o). |
  | `learned_static` | MAJIC(–DynUpd) | Load pre-built matrix (`MAJIC_INIT_MATRIX` path, default `markov_methods/init_matrix.npy`); **freeze** it during attack (no Q-learning update, no reset). ASR 76.5%. |
  | `learned` | full MAJIC | Load the same learned matrix but **keep** dynamic updates. ASR 95.7%. |
  `run_majic.sh` defaults to `uniform`; users switch by exporting
  `MAJIC_INIT_MODE=learned` (or `learned_static`) and optionally
  `MAJIC_INIT_MATRIX=/path/to/10x10.npy`. A helper script
  `majic/build_init_matrix.py` (separate from the evaluation entry point)
  reproduces the paper's offline initialization on `data/harmful_behaviors_50.json`
  using the same attacker/judge endpoints, but is **not run** by
  `run_majic.sh`.

## Environment

The `OpenRT` conda env already ships everything MAJIC needs
(`openai 2.31`, `numpy 2.2`, `pandas 2.3`, `tqdm 4.67`, `tiktoken`,
`python-dotenv`). **No extra installs required.** `eval-dace/MAJIC/requirements.txt`
is trimmed to `openai>=1.0`, `numpy>=1.24`, `pandas>=2.0`, `tqdm>=4.65`
(purely informational — mirrors the subset of `OpenRT/requirements.txt`
we actually import).

## Design Overview

We leave the existing `methods/m*_attackLLM.py` alone as research artifacts and
add a thin, self-contained runner that mirrors OpenRT's evaluation pattern.
The runner reuses only the **prompt templates** carved out of those files.

### New/modified files (all inside `eval-dace/MAJIC/`)

| Path | Purpose |
| --- | --- |
| `majic/__init__.py` | Package marker for the new, runnable code. |
| `majic/api_client.py` | Thin OpenAI-compatible wrapper with `attacker(...)`, `victim(...)`, `judge_score(...)` helpers. Honors env vars exactly like `OpenRT/unified_eval.py` (`DEFENDER_API_*`, `ATTACKER_API_*`, `OPENAI_*`). Includes optional `<answer>` tag extraction (matches `run_eval.sh --attacker-answer-extract`). |
| `majic/strategies.py` | The 10 disguise-strategy prompt templates (hypothetical, historical, spatial, reverse, security, word, char, literary, language, emoji), copied verbatim from `methods/m*_attackLLM.py`. Each strategy exposes `render_init(goal)` and `render_compose(goal, prev_disguised)` for the two-step fusion described in §Dynamic Strategy Selection. Keep the module side-effect free. |
| `majic/markov.py` | Numeric core: `softmax_row`, `update_mtm_and_softmax`, learning-rate decay (`α *= η` every 40 queries), periodic partial reset (`β`-blend with uniform every 80 queries), softmax-normalized initial vector. Exposes a `MatrixController` with three modes — `uniform`, `learned_static`, `learned` — that gate whether Q-learning updates and β-reset are applied (see Table 4). Ported from `markov_methods/markov_attack_api_dynamic.py` and `markov_methods/norm_matrix.py` with the Q-learning step intact. |
| `majic/judge.py` | PAIR-style GPT-4o judge (reuses the same system prompt already in `methods/judgeutils.py::judge_gpt`). Returns `(score∈[0,1], raw_rating∈[1,10])` so we can compare against `run_eval.sh`'s `judge_threshold`. |
| `majic/runner.py` | Orchestrator: dataset loading (CSV `Behavior` column / JSONL `vanilla` field / `data/*.json` `goal` field, matching `OpenRT/unified_eval.py`), chain loop (`chain_count` attempts × `chain_length` optimization steps), matrix update, results & summary writing in the same `history_<ts>.json` / `summary_<ts>.json` / `majic_<ts>.log` layout used by `OpenRT/unified_eval.py::save_results`. Writes `AttackResult`-shaped dicts (`target`, `success`, `final_prompt`, `output_text`, `method="majic"`, `history`, `query_num`). |
| `run_majic.sh` | **New entry point** mirroring `OpenRT/run_eval.sh`: exports defender/attacker/judge endpoints, picks dataset, sets `NUM_SAMPLES/MAX_TURNS/JUDGE_THRESHOLD/MAJIC_CHAIN_COUNT/MAJIC_CHAIN_LENGTH/MAJIC_INIT_MODE/MAJIC_INIT_MATRIX`, writes into `results/dace/$MODEL_NAME-$(date)/majic/`. |
| `majic/build_init_matrix.py` | **Optional offline tool** (not triggered by `run_majic.sh`). Reproduces the paper's §Initializing-Markov-Transition-Matrix pipeline using the same OpenAI-compatible endpoints on `data/harmful_behaviors_50.json`, producing `markov_methods/init_matrix.npy` for use with `MAJIC_INIT_MODE=learned` / `learned_static`. |
| `majic.py` | Replace the broken `from methods.m1_... import ...` aggregator with a 5-line shim that re-exports `majic.runner.main` so `python3 majic.py ...` still works. |
| `requirements.txt` | Drop `torch`/`transformers` (no longer needed); add `openai>=1.0` and `tqdm`. Keep `numpy`, `pandas`. |
| `README.md` | Replace upstream install/usage section with an `eval-dace` quick-start referencing `run_majic.sh`. Note that this is a **fork adapted for the MAGIC evaluation pipeline**. |

### Chain behaviour (mirrors the paper)

1. Build `M ∈ R^{10×10}` according to `MAJIC_INIT_MODE`:
   - `uniform` → `M_ij = 1/10`;
   - `learned_static` / `learned` → `np.load(MAJIC_INIT_MATRIX)` (assert shape `(10,10)`).
2. Derive initial selection vector `v` from `softmax(column_sums(M), T=1.0)` — identical formula to upstream.
3. For each harmful prompt, up to `chain_count` chains:
   - Pick `init_idx` ∼ `v`; call attacker once to disguise the goal (`strategies.render_init`), query victim, score with judge.
   - On success (`score == 1.0`), stop.
   - Otherwise, for up to `chain_length` optimization steps: sample `next_idx` ∼ `M[failed_idx-1]`, rewrite the failed disguise with strategy `next_idx` (`strategies.render_compose`), query victim, score.
   - **Matrix update gating** (via `MatrixController`):
     - `uniform` / `learned` → call `update_mtm_and_softmax` with `r = success_reward | fail_reward`; apply `α *= η` every 40 queries; apply β-uniform reset every 80 queries.
     - `learned_static` → **skip** Q-learning update, decay, and reset entirely (MAJIC(–DynUpd)).
4. Record total queries per prompt → enables Table-2-style AQC reporting.

### Credentials & compatibility

`api_client.py` reads from `argparse` first, then env vars (the exact names
exported by `run_eval.sh`), then a legacy fallback `OPENAI_API_KEY` — identical
precedence to `OpenRT/unified_eval.py::get_creds`. This lets a user run
`bash run_majic.sh` without editing Python and also plug in new endpoints via
flags for ad-hoc testing.

### Output format

To stay consistent with Table-3 consumers, each run writes:

```
results/dace/<MODEL_NAME>-<TS>/majic/
  history_<TS>.json   # per-sample AttackResult dicts + chain history
  summary_<TS>.json   # {"attack":"majic", "metrics":{"attack_success_rate":...,"avg_queries":...}}
  majic_<TS>.log      # mirrored stdout (DualLogger)
```

Keys match `OpenRT/unified_eval.py::save_results` so the existing aggregation
scripts keep working.

## Verification

1. **Environment check** (no install needed):
   ```bash
   conda activate OpenRT
   python -c "import openai, numpy, pandas, tqdm; print('ok')"
   ```
2. **Static**: `python3 -c "from majic.runner import main"` should import without
   errors under `conda activate OpenRT`.
3. **Smoke test — default uniform init** (2 prompts, `MAX_TURNS=1`, `CHAIN_COUNT=1`, `CHAIN_LENGTH=1`):
   ```bash
   conda activate OpenRT
   cd eval-dace/MAJIC
   NUM_SAMPLES=2 MAX_TURNS=1 MAJIC_CHAIN_COUNT=1 MAJIC_CHAIN_LENGTH=1 \
     bash run_majic.sh
   ```
   Expected: new `results/.../majic/{history,summary,majic}_*.{json,log}` files;
   `summary_*.json` contains a finite `attack_success_rate` and `init_mode: "uniform"`.
4. **Init-mode switch test**: rerun with `MAJIC_INIT_MODE=learned_static MAJIC_INIT_MATRIX=markov_methods/init_matrix.npy`
   (after running `python -m majic.build_init_matrix` once) and confirm the
   summary records `init_mode: "learned_static"` and that `M` is unchanged
   across samples (logged hash).
5. **Endpoint-parity test**: diff the first 3 log lines of the MAJIC log against
   a fresh `run_eval.sh` log and confirm both hit `DEFENDER_API_BASE_URL`
   and use the same base-attacker model name.
6. **Full run** (optional, blocking on HarmBench 400): `bash run_majic.sh`
   without `NUM_SAMPLES` matches the Table-3 cadence.

## Risks / Notes

- Upstream `m4_reverse_attackLLM.py` is named differently from the imports in
  `markov_methods/*`; we sidestep this by extracting templates into
  `strategies.py` rather than re-exposing upstream methods.
- The paper reports 95.7% ASR with the **learned** initial matrix; the uniform
  start caps us at ~70% on GPT-4o but still far exceeds every Table-3 baseline
  (PAIR/TAP/AutoDAN-turbo-r ≤ 35%), so `MAJIC_INIT_MODE=uniform` already
  substantiates the defender's robustness claim. The `learned` and
  `learned_static` modes are available for users who want to reproduce the
  higher Table-1 numbers via `majic/build_init_matrix.py`.
- The attacker backend is intentionally decoupled — the runner only calls the
  OpenAI-compatible Chat Completions endpoint, so swapping Qwen ↔ Llama ↔
  Mistral behind `ATTACKER_API_BASE_URL` requires zero code change.
- `strongreject` / `alpaca_eval` / `olmes` suites are untouched — this plan
  only adds a new entry under Table 3.
