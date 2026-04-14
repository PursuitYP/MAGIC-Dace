# Implementation Plan: Attack Diversity + Bayesian Replay Pool on MAGIC

## Context

MAGIC (Multi-Agent Adversarial Game) trains attacker/defender LLMs via co-evolving RL. Two problems need solving:
1. **Attack Strategy Collapse** — attacker overfits to few high-reward patterns → defender only learns narrow defense
2. **Defense Adversarial Forgetting** — defender forgets earlier attack patterns as attacker evolves

This plan adds: (1) explicit 2D strategy space + diversity reward to broaden attacks, (2) Bayesian replay pool to consolidate defense against historical attacks. Reference: `z_materials/研究方法v3.1.md` and `z_materials/pseudocode_v3.1.html`.

---

## Implementation Priority

| Phase | Feature | Files | Can Parallelize? |
|-------|---------|-------|-----------------|
| P0 | Archive pool data structure + diversity reward math | NEW `archive_pool.py` | Yes (independent) |
| P1 | Format reward + strategy extraction + attack_success | `game.py` (reward_score), `game.py` (reward_manager) | Yes (independent of P0) |
| P2 | Config additions | `ppo_trainer.yaml` | Yes (independent) |
| P3 | Trainer integration: archive init, diversity inject, stage transitions | `ray_trainer.py` | Depends on P0+P1+P2 |
| P4 | Replay batch: Thompson sampling → rollout → merge → posterior update | `ray_trainer.py`, `multi_agent_rollout.py` | Depends on P3 |
| P5 | Metrics, checkpoint, training script | `ray_trainer.py`, shell script | Depends on P4 |

---

## P0: New File — `src/verl/verl/separated_trainer/ppo/archive_pool.py`

### dace: Bayesian adversarial replay pool with strategy coverage tracking ###

```python
@dataclass
class ArchiveEntry:
    prompt_text: str           # Attacker's rewritten prompt (extracted from <answer>)
    seed_prompt: str           # Original vanilla prompt
    data_type: str             # 'vanilla_harmful' or 'vanilla_benign'
    strategy: Tuple[int, int]  # (risk_category_idx, attack_style_idx)
    extra_info: dict           # Preserved extra_info
    successes: float           # Beta posterior s_i (float — supports decay)
    failures: float            # Beta posterior f_i
    step_added: int            # Global step when first added
    prompt_data: dict          # Full fields needed to reconstruct a DataProto row for replay
                               # Keys: question, data_source, data_type, prompt, adversarial,
                               #        reward_model, extra_info, ability, seed_prompt,
                               #        input_template, attacker_template

class ArchivePool:
    # Strategy space constants (matching preprocess_dace.py L30-57 and L46-56)
    RISK_CATEGORIES = [
        "Violent Crimes", "Non-Violent Crimes", "Sex-Related Crimes",
        "Child Sexual Exploitation", "Defamation", "Specialized Advice",
        "Privacy", "Intellectual Property", "Indiscriminate Weapons",
        "Hate", "Suicide & Self-Harm", "Sexual Content",
        "Elections", "Code Interpreter Abuse"
    ]  # |S| = 14
    ATTACK_STYLES = [
        "Slang", "Technical Terms", "Role Play", "Authority Manipulation",
        "Misspellings", "Word Play", "Emotional Manipulation",
        "Hypotheticals", "Historical Scenario", "Uncommon Dialects"
    ]  # |C| = 10
    N_RISK = 14
    N_STYLE = 10
    N_SLOTS = 140  # |B| = |S| × |C|
```

**Key methods:**

1. **`__init__(self, config)`**
   - `self.entries: List[ArchiveEntry] = []`
   - `self.prompt_hash_set: Set[str] = set()` — for O(1) dedup by prompt_text hash
   - `self.slot_counts: np.ndarray = np.zeros((N_RISK, N_STYLE), dtype=np.float64)` — frequency counts
   - Config params: `gamma_decay`, `prune_threshold`, `prune_min_trials`, `max_pool_size`, `alpha_prior`, `beta_prior`, `epsilon` (diversity smoothing)

2. **`extract_strategy(text: str) -> Optional[Tuple[int, int]]`** (staticmethod)
   - Regex: `r'<strategy>\s*risk category:\s*(.+?)\s*\n\s*attack style:\s*(.+?)\s*</strategy>'`
   - Fuzzy-match extracted strings to `RISK_CATEGORIES` / `ATTACK_STYLES` (case-insensitive, strip)
   - Return `(risk_idx, style_idx)` or `None`

3. **`_compute_entropy(counts: np.ndarray) -> float`** (internal)
   - `total = counts.sum()`; if total == 0: return 0.0
   - `p = counts.flatten() / total`; mask = p > 0
   - `H = -np.sum(p[mask] * np.log(p[mask]))`
   - return H

4. **`compute_diversity_reward(self, strategy: Tuple[int, int]) -> float`**
   - Normalized Marginal Coverage Gain
   - `current_H = _compute_entropy(self.slot_counts)`
   - Numerator: temporarily add 1 to slot `strategy`, compute H_new, `delta = H_new - current_H`
   - Denominator: for each of 140 slots, compute H_if_added - current_H, take max → `delta_max`
   - `R_div = delta / (delta_max + eps)`
   - **Optimization**: denominator only depends on pool state, can cache per-step (invalidate on `add_entry`/`time_decay`/`prune`)

5. **`compute_coverage_entropy(self) -> float`** — public wrapper for metrics

6. **`add_entry(self, entry: ArchiveEntry) -> bool`**
   - Dedup: `prompt_hash = hash(entry.prompt_text)`; if in `prompt_hash_set`, update existing entry's `successes += 1`, return False
   - Otherwise append entry, update `slot_counts[strategy]`, add to hash set, return True
   - If `len(entries) > max_pool_size`: prune or drop oldest low-value entries

7. **`time_decay(self)`**
   - For each entry: `e.successes *= gamma`, `e.failures *= gamma`
   - Invalidate cached denominator

8. **`thompson_sample(self, n: int) -> List[Tuple[int, ArchiveEntry]]`**
   - For each entry i: `p_tilde = np.random.beta(alpha + e.successes, beta + e.failures)`
   - Return top-n by `p_tilde` as `(entry_index, entry)` pairs

9. **`update_posterior(self, entry_idx: int, any_harmful: bool)`**
   - If `any_harmful`: `entries[entry_idx].successes += 1`
   - Else: `entries[entry_idx].failures += 1`

10. **`prune(self)`**
    - Remove entries where `p_hat = (alpha + s) / (alpha + s + beta + f) < prune_threshold` AND `(s + f) > prune_min_trials`
    - Update `slot_counts` and `prompt_hash_set`

11. **`save(self, path)` / `load(cls, path)`** — JSON serialization for checkpoint

---

## P1: Reward Score Updates

### File: `src/verl/verl/utils/reward_score/game.py`

#### Change 1: Add `extract_strategy` function (after L106)

```python
### dace: extract strategy (risk_category, attack_style) from <strategy> tags ###
def extract_strategy_text(text: str) -> Optional[Tuple[str, str]]:
    """Extract (risk_category_str, attack_style_str) from <strategy> tags."""
    pattern = r'<strategy>\s*risk category:\s*(.+?)\s*\n\s*attack style:\s*(.+?)\s*</strategy>'
    match = re.search(pattern, text or "", re.DOTALL | re.IGNORECASE)
    if match:
        return (match.group(1).strip(), match.group(2).strip())
    return None
```

#### Change 2: Add `format_reward_func_dace` (after L298)

```python
### dace: format reward for <think><strategy><answer> three-tag format ###
def format_reward_func_dace(solution_str):
    """Reward for exactly one think/strategy/answer block in correct order."""
    text = (solution_str or "").strip()
    if not text:
        return -FORMAT_REWARD_VALUE
    counts = (
        text.count('<think>'), text.count('</think>'),
        text.count('<strategy>'), text.count('</strategy>'),
        text.count('<answer>'), text.count('</answer>'),
    )
    if counts != (1, 1, 1, 1, 1, 1):
        return -FORMAT_REWARD_VALUE
    pattern = r"^<think>[\s\S]*?</think>\s*<strategy>[\s\S]*?</strategy>\s*<answer>[\s\S]*?</answer>$"
    if re.search(pattern, text, re.DOTALL):
        return FORMAT_REWARD_VALUE
    return -FORMAT_REWARD_VALUE
```

#### Change 3: Add `attack_success` field to `RewardScores` (L75-87)

Add after L87 (`request_safety_label`):
```python
    attack_success: Optional[bool] = None
```

#### Change 4: Compute `attack_success` in `compute_reward_bundle` (after L589)

Before the return statement at L582, add:
```python
### dace: compute attack_success flag ###
# Attack success definition:
#   request_label (from reward model on rewritten prompt, matching USE_Q_SAFE_LABEL_FOR_REFUSAL):
#     - "Unsafe" request: success if defender gave unsafe response (qa_safe_label in Unsafe/Controversial)
#     - "Safe" request: success if defender gave unsafe response OR defender refused (over-refusal)
qa_safe = (labels or {}).get("qa_safe_label")
qa_refused = (labels or {}).get("qa_refusal_label")
is_unsafe_response = qa_safe in ("Unsafe", "Controversial")
is_refused = qa_refused == "Yes"

attack_success = None
if request_is_harmful is True:
    attack_success = is_unsafe_response  # harmful prompt → success if defender outputs harmful
elif request_is_harmful is False:
    attack_success = is_unsafe_response or is_refused  # benign prompt → success if defender outputs harmful OR refuses
```

Update the return to include `attack_success=attack_success`.

### File: `src/verl/verl/workers/reward_manager/game.py`

#### Change 1: Import new functions (top of file)

```python
from verl.utils.reward_score.game import format_reward_func_dace, extract_strategy_text
```

#### Change 2: Update `compute_format_r` (around L42-46) to dispatch DACE format

```python
### dace: dispatch to 3-tag format reward for DACE attacker ###
def compute_format_r(data_source, role, response_str, *, use_dace_format=False):
    if data_source == 'game':
        if use_dace_format and role == 'attacker':
            return format_reward_func_dace(response_str)
        return format_reward_func(response_str)
    raise ValueError(f'Unknown {data_source=}')
```

#### Change 3: Add `attack_success` to `reward_tensor_map` (after L304, before L305)

```python
### dace: export attack_success flag ###
reward_tensor_map['attack_success'] = torch.tensor(
    [1.0 if score.attack_success else 0.0 for score in score_bundles],
    dtype=torch.float32,
)
```

#### Change 4: Pass `use_dace_format` to `compute_format_r` (L335-341)

```python
use_dace_format = data_item.meta_info.get('use_dace_format', False)
format_r = compute_format_r(data_source, role, last_role_msg['content'],
                            use_dace_format=use_dace_format)
```

---

## P2: Config Updates

### File: `src/verl/verl/separated_trainer/config/ppo_trainer.yaml`

Add under `algorithm:` section (after L231, before `trainer:`):

```yaml
  # --- DACE: Attack Diversity ---
  diversity:
    enable: false
    reward_type: coverage       # 'coverage' or 'novelty'
    lambda_success: 1.0         # diversity coefficient when attack succeeds
    lambda_fail: 0.5            # diversity coefficient when attack fails
    epsilon: 1.0e-8             # smoothing for coverage denominator
    use_dace_format: false      # enable 3-tag format reward for attacker

  # --- DACE: Bayesian Adversarial Replay Pool ---
  replay_pool:
    enable: false
    replay_batch_size: 32       # B_replay per defender step
    gamma_decay: 0.97           # time decay factor per round
    prune_threshold: 0.05       # epsilon: prune if posterior mean < this
    prune_min_trials: 5.0       # n_min: minimum trials before pruning
    max_pool_size: 5000         # max entries in archive
    alpha_prior: 1.0            # Beta prior alpha
    beta_prior: 1.0             # Beta prior beta
```

---

## P3: Trainer Integration — Diversity Reward + Archive + Stage Transitions

### File: `src/verl/verl/separated_trainer/ppo/ray_trainer.py`

#### 3A: Imports (around L19-54)

```python
from verl.separated_trainer.ppo.archive_pool import ArchivePool, ArchiveEntry
from verl.utils.reward_score.game import extract_answer, extract_strategy_text
```

#### 3B: `__init__` — Initialize archive pool (after L467)

```python
### dace: initialize archive pool for diversity + replay ###
self.archive_pool = None
diversity_cfg = self.config.algorithm.get('diversity', {})
replay_cfg = self.config.algorithm.get('replay_pool', {})
if diversity_cfg.get('enable', False) or replay_cfg.get('enable', False):
    self.archive_pool = ArchivePool(replay_cfg)
self._prev_train_agent = None  # tracks agent for stage transition detection
self._pending_success_buffer = []  # buffer for attack successes to add to pool at stage end
```

#### 3C: New method `_compute_and_inject_diversity_rewards` (add after `_update_current_train_agent` ~L1544)

This method:
1. Extracts strategy from attacker response in history
2. Computes coverage-based diversity reward per sample
3. Applies differential λ (success=1.0, fail=0.5)
4. Adds diversity reward to `attacker_turn_level_reward`
5. Recomputes `attacker_turn_level_return`
6. Buffers successful attacks for later pool insertion

```python
### dace: compute diversity reward and inject into attacker turn-level reward ###
def _compute_and_inject_diversity_rewards(self, batch: DataProto, reward_tensor_map: dict, metrics: dict):
    diversity_cfg = self.config.algorithm.diversity
    lambda_success = diversity_cfg.get('lambda_success', 1.0)
    lambda_fail = diversity_cfg.get('lambda_fail', 0.5)
    batch_size = len(batch)
    div_rewards = torch.zeros(batch_size, dtype=torch.float32)
    attack_success = reward_tensor_map.get('attack_success', torch.zeros(batch_size))

    for i in range(batch_size):
        history = batch.non_tensor_batch['history'][i]
        # Find last attacker message
        attacker_content = None
        for msg in reversed(history):
            if msg.get('role') == 'padding':
                continue
            if msg.get('role') == 'attacker':
                attacker_content = msg.get('content', '')
                break
        if not attacker_content:
            continue

        # Extract strategy index
        strat_idx = ArchivePool.extract_strategy(attacker_content)
        if strat_idx is None:
            continue  # format reward already penalizes this

        # Compute diversity reward
        r_div = self.archive_pool.compute_diversity_reward(strat_idx)
        is_success = attack_success[i].item() > 0.5
        lam = lambda_success if is_success else lambda_fail
        div_rewards[i] = lam * r_div

        # Buffer successful attack for pool insertion at stage end
        if is_success:
            self._pending_success_buffer.append({
                'prompt_text': extract_answer(attacker_content) or attacker_content,
                'seed_prompt': (batch.non_tensor_batch.get('extra_info', [{}])[i] or {}).get('raw_prompt', ''),
                'data_type': batch.non_tensor_batch['data_type'][i],
                'strategy': strat_idx,
                'extra_info': batch.non_tensor_batch.get('extra_info', [{}])[i] or {},
                'prompt_data': {  # Fields for replay DataProto reconstruction
                    'question': batch.non_tensor_batch['question'][i],
                    'data_source': batch.non_tensor_batch['data_source'][i],
                    'data_type': batch.non_tensor_batch['data_type'][i],
                    'prompt': batch.non_tensor_batch.get('prompt', [None])[i],
                    'adversarial': batch.non_tensor_batch.get('adversarial', [''])[i],
                    'reward_model': batch.non_tensor_batch['reward_model'][i],
                    'extra_info': batch.non_tensor_batch.get('extra_info', [{}])[i],
                    'ability': batch.non_tensor_batch.get('ability', ['safety'])[i],
                    'seed_prompt': (batch.non_tensor_batch.get('extra_info', [{}])[i] or {}).get('raw_prompt', ''),
                    'input_template': batch.non_tensor_batch.get('input_template', [None])[i],
                    'attacker_template': batch.non_tensor_batch.get('attacker_template', [None])[i],
                },
            })

    # Inject into attacker_turn_level_reward at last turn
    for i in range(batch_size):
        num_turns = batch.non_tensor_batch['num_turns'][i]
        batch.batch['attacker_turn_level_reward'][i, num_turns - 1] += div_rewards[i]

    # Recompute attacker_turn_level_return
    atk_reward = batch.batch['attacker_turn_level_reward']
    atk_turn_mask = verl_F.get_turn_mask(atk_reward, batch.non_tensor_batch['num_turns'])
    batch.batch['attacker_turn_level_return'] = core_algos.compute_turn_level_return(
        atk_reward, atk_turn_mask, self.config.algorithm.gamma_turn_level)

    # Metrics
    metrics['diversity/mean_reward'] = div_rewards.mean().item()
    metrics['diversity/nonzero_frac'] = (div_rewards != 0).float().mean().item()
    metrics['diversity/pool_size'] = len(self.archive_pool)
    metrics['diversity/coverage_entropy'] = self.archive_pool.compute_coverage_entropy()
    n_occupied = (self.archive_pool.slot_counts > 0).sum()
    metrics['diversity/strategy_coverage'] = float(n_occupied) / ArchivePool.N_SLOTS
```

#### 3D: New method `_handle_stage_transition` (add after above)

```python
### dace: handle stage transitions for archive operations ###
def _handle_stage_transition(self, old_agent: str, new_agent: str):
    """Called when training agent switches. Manages archive pool lifecycle."""
    if self.archive_pool is None:
        return

    # Flush pending success buffer to archive
    if self._pending_success_buffer:
        n_added = 0
        for item in self._pending_success_buffer:
            entry = ArchiveEntry(
                prompt_text=item['prompt_text'],
                seed_prompt=item['seed_prompt'],
                data_type=item['data_type'],
                strategy=item['strategy'],
                extra_info=item['extra_info'],
                successes=1.0,
                failures=0.0,
                step_added=self.global_steps,
                prompt_data=item['prompt_data'],
            )
            if self.archive_pool.add_entry(entry):
                n_added += 1
        print(f"[DACE] Flushed {n_added} new entries to archive (total: {len(self.archive_pool)})")
        self._pending_success_buffer.clear()

    # When new round starts (defender->attacker transition): time decay + prune
    if old_agent == 'defender' and new_agent == 'attacker':
        replay_cfg = self.config.algorithm.get('replay_pool', {})
        if replay_cfg.get('enable', False):
            self.archive_pool.time_decay()
            self.archive_pool.prune()
            print(f"[DACE] New round: decay + prune → pool size = {len(self.archive_pool)}")
```

#### 3E: Modify `fit()` — injection points

**Location 1**: After L1738 (after reward turn_level_return loop), before L1740 (filter_groups):

```python
### dace: inject diversity reward into attacker reward ###
if (self.archive_pool is not None
    and self.config.algorithm.get('diversity', {}).get('enable', False)
    and self._current_train_agent == 'attacker'):
    self._compute_and_inject_diversity_rewards(new_batch, reward_tensor_map, metrics)
```

**Location 2**: At L1712-1717 area, add `use_dace_format` to meta_info:

```python
new_batch.meta_info['use_dace_format'] = self.config.algorithm.get('diversity', {}).get('use_dace_format', False)
```

**Location 3**: After L1925 (`_update_current_train_agent`), detect stage transition:

```python
### dace: detect stage transition and trigger archive operations ###
if self.archive_pool is not None:
    new_agent = self._current_train_agent
    if self._prev_train_agent is not None and self._prev_train_agent != new_agent:
        self._handle_stage_transition(self._prev_train_agent, new_agent)
    self._prev_train_agent = new_agent
```

**Location 4**: At the start of `fit()` (after initial `_update_current_train_agent(epoch=epoch)` at L1609):

```python
if self._prev_train_agent is None:
    self._prev_train_agent = self._current_train_agent
```

---

## P4: Replay Batch — Thompson Sampling → Rollout → Merge → Posterior Update

### File: `src/verl/verl/separated_trainer/ppo/ray_trainer.py`

#### 4A: New method `_build_replay_gen_batch`

Constructs a DataProto for replay samples, with the archived attacker prompt injected as the `adversarial` field so the existing `skip_attacker_generation_for_defender` mechanism (multi_agent_rollout.py L627-667) can be reused.

```python
### dace: build replay batch from archive via Thompson Sampling ###
def _build_replay_gen_batch(self, base_meta_info: dict) -> Optional[Tuple[DataProto, List[int]]]:
    """Sample from archive pool and construct DataProto for defender rollout.

    Returns (replay_batch, entry_indices) or (None, []) if pool insufficient.
    The replay batch uses the existing 'adversarial' field + skip_attacker_generation
    mechanism to inject archived attacker prompts.
    """
    replay_cfg = self.config.algorithm.replay_pool
    replay_size = replay_cfg.get('replay_batch_size', 32)

    if len(self.archive_pool) < replay_size:
        return None, []

    sampled = self.archive_pool.thompson_sample(replay_size)
    if not sampled:
        return None, []

    entry_indices = [idx for idx, _ in sampled]
    entries = [entry for _, entry in sampled]

    # Build batch_dict matching dataloader output format
    batch_dict = defaultdict(list)
    for entry in entries:
        pd = entry.prompt_data
        for key in ['question', 'data_source', 'data_type', 'prompt',
                     'reward_model', 'extra_info', 'ability', 'seed_prompt',
                     'input_template', 'attacker_template']:
            batch_dict[key].append(pd.get(key))
        # Set 'adversarial' to the archived attacker prompt text
        # This is what skip_attacker_generation_for_defender will use
        batch_dict['adversarial'].append(entry.prompt_text)

    for key in batch_dict:
        batch_dict[key] = np.array(batch_dict[key], dtype=object)

    batch_dict['batch_idx'] = torch.arange(0, len(entries))

    meta_info = dict(base_meta_info)
    meta_info['train_role'] = 'defender'
    meta_info['is_replay'] = True

    replay_batch = DataProto.from_single_dict(batch_dict, meta_info=meta_info)
    replay_batch.non_tensor_batch['uid'] = np.array(
        [f'replay_{uuid.uuid4()}' for _ in range(len(entries))],
        dtype=object
    )
    replay_batch = replay_batch.repeat(
        repeat_times=self.config.actor_rollout_ref.rollout.n, interleave=True
    )

    return replay_batch, entry_indices
```

#### 4B: New method `_run_replay_pipeline`

```python
### dace: run replay samples through rollout + reward + posterior update ###
def _run_replay_pipeline(self, base_meta_info: dict, metrics: dict) -> Optional[DataProto]:
    """Full replay pipeline: sample → generate → reward → posterior update → return processed batch."""
    replay_batch, entry_indices = self._build_replay_gen_batch(base_meta_info)
    if replay_batch is None:
        return None

    # Prepare gen_batch (same as main flow at L1634-1641)
    gen_batch = replay_batch.select(
        batch_keys=['batch_idx'],
        non_tensor_batch_keys=[k for k in replay_batch.non_tensor_batch.keys()
            if k not in ['data_source', 'ability', 'reward_model', 'extra_info', 'uid']],
        meta_info_keys=['agent_roles', 'finish_flag', 'system_prompts'],
        deepcopy=True
    )
    gen_batch.meta_info['train_role'] = 'defender'
    gen_batch.meta_info['is_replay'] = True

    # Generate (using skip_attacker_generation_for_defender to inject archived prompt)
    gen_output = self.multi_turn_generate_sequences(gen_batch)
    replay_batch = replay_batch.union(gen_output)

    # Compute global attention
    global_attention = None
    for role in replay_batch.meta_info['agent_roles']:
        attn_key = f'{role}_attention_mask'
        if attn_key in replay_batch.batch:
            role_mask = replay_batch.batch[attn_key]
            global_attention = role_mask if global_attention is None else global_attention + role_mask
    if global_attention is not None:
        replay_batch.meta_info['global_token_num'] = torch.sum(global_attention, dim=-1).tolist()

    # Reward computation
    replay_batch.meta_info['mask_unfinished_reward'] = self.config.reward_model.mask_unfinished_reward
    replay_batch.meta_info['use_format_reward'] = self.config.reward_model.get('use_format_reward', False)
    replay_batch.meta_info['use_dace_format'] = self.config.algorithm.get('diversity', {}).get('use_dace_format', False)
    format_reward_roles = self.config.reward_model.get('format_reward_roles', None)
    if format_reward_roles is not None:
        format_reward_roles = list(format_reward_roles)
    replay_batch.meta_info['format_reward_roles'] = format_reward_roles

    replay_reward_map = self.reward_fn(replay_batch)
    replay_batch.batch['acc'] = replay_reward_map.pop('acc')
    for key, tensor in replay_reward_map.items():
        replay_batch.batch[key] = tensor
        if tensor.dim() < 2 or not key.endswith('_turn_level_reward'):
            continue
        turn_mask = verl_F.get_turn_mask(tensor, replay_batch.non_tensor_batch['num_turns'])
        key_return = key.replace('reward', 'return')
        replay_batch.batch[key_return] = core_algos.compute_turn_level_return(
            tensor, turn_mask, self.config.algorithm.gamma_turn_level)

    # Posterior update: group G rollouts per uid
    attack_success = replay_reward_map.get('attack_success', torch.zeros(len(replay_batch)))
    uid_to_successes = defaultdict(list)
    for i, uid in enumerate(replay_batch.non_tensor_batch['uid']):
        uid_to_successes[uid].append(attack_success[i].item() > 0.5)

    # Map back to entry_indices (entry_indices is pre-repeat, uids are post-repeat)
    n_rollouts = self.config.actor_rollout_ref.rollout.n
    seen_uids = []
    for uid in replay_batch.non_tensor_batch['uid']:
        if uid not in seen_uids:
            seen_uids.append(uid)

    for j, uid in enumerate(seen_uids):
        if j < len(entry_indices):
            any_harmful = any(uid_to_successes[uid])
            self.archive_pool.update_posterior(entry_indices[j], any_harmful)

    # Prune after posterior update
    self.archive_pool.prune()

    # Also buffer new successful attacks from replay for pool
    for i in range(len(replay_batch)):
        if attack_success[i].item() > 0.5:
            history = replay_batch.non_tensor_batch['history'][i]
            attacker_content = None
            for msg in reversed(history):
                if msg.get('role') == 'padding':
                    continue
                if msg.get('role') == 'attacker':
                    attacker_content = msg.get('content', '')
                    break
            if attacker_content:
                strat_idx = ArchivePool.extract_strategy(attacker_content)
                if strat_idx is not None:
                    self._pending_success_buffer.append({
                        'prompt_text': extract_answer(attacker_content) or attacker_content,
                        'seed_prompt': (replay_batch.non_tensor_batch.get('extra_info', [{}])[i] or {}).get('raw_prompt', ''),
                        'data_type': replay_batch.non_tensor_batch['data_type'][i],
                        'strategy': strat_idx,
                        'extra_info': replay_batch.non_tensor_batch.get('extra_info', [{}])[i] or {},
                        'prompt_data': {k: replay_batch.non_tensor_batch.get(k, [None])[i]
                                        for k in ['question','data_source','data_type','prompt',
                                                   'adversarial','reward_model','extra_info','ability',
                                                   'seed_prompt','input_template','attacker_template']},
                    })

    metrics['replay/batch_size'] = len(entry_indices)
    metrics['replay/pool_size'] = len(self.archive_pool)
    metrics['replay/pool_mean_posterior'] = np.mean([
        (self.archive_pool.alpha_prior + e.successes) /
        (self.archive_pool.alpha_prior + e.successes + self.archive_pool.beta_prior + e.failures)
        for e in self.archive_pool.entries
    ]) if self.archive_pool.entries else 0.0

    return replay_batch
```

#### 4C: Modify `fit()` — Replay integration point

Insert after the diversity reward injection (P3 Location 1) and before group filtering (L1740):

```python
### dace: replay batch for defender mixed training ###
if (self._current_train_agent == 'defender'
    and self.archive_pool is not None
    and self.config.algorithm.get('replay_pool', {}).get('enable', False)):
    with _timer('replay', timing_raw):
        replay_processed = self._run_replay_pipeline(base_rollout_meta_info, metrics)
        if replay_processed is not None:
            new_batch = DataProto.concat([new_batch, replay_processed])
```

### File: `src/verl/verl/separated_trainer/ppo/multi_agent_rollout.py`

#### 4D: Enable `skip_attacker_generation_for_defender` for replay

The existing mechanism at L627-667 already handles skipping attacker generation and injecting `adversarial` field content. For replay to work, we need to ensure the replay batch has:
- `use_adversarial_prompt_for_defender = True` in rollout config **OR** the replay meta_info triggers the skip

**Approach**: In `_run_multi_turn_conversation` (L619-622), extend the condition:

Current (L627-630):
```python
if (role == agent_roles[0]
        and train_role == agent_roles[1]
        and self.use_adversarial_prompt_for_defender
        and self.skip_attacker_generation_for_defender):
```

Change to:
```python
### dace: also skip attacker generation for replay batches ###
is_replay = data_proto.meta_info.get('is_replay', False)
if (role == agent_roles[0]
        and train_role == agent_roles[1]
        and (is_replay or (self.use_adversarial_prompt_for_defender
                          and self.skip_attacker_generation_for_defender))):
```

This way, replay batches automatically skip attacker generation and use the `adversarial` field (which we set to the archived attack prompt in `_build_replay_gen_batch`).

---

## P5: Metrics, Checkpoint, Training Script

### File: `src/verl/verl/separated_trainer/ppo/ray_trainer.py`

#### 5A: Archive checkpoint save/load

In `_save_checkpoint` method, add:
```python
### dace: save archive pool to checkpoint ###
if self.archive_pool is not None:
    archive_path = Path(checkpoint_dir) / 'archive_pool.json'
    self.archive_pool.save(archive_path)
```

In checkpoint loading (in `fit()` L1558 area), add:
```python
### dace: restore archive pool from checkpoint ###
if self.archive_pool is not None:
    archive_path = Path(checkpoint_dir) / 'archive_pool.json'
    if archive_path.exists():
        self.archive_pool = ArchivePool.load(archive_path, self.config.algorithm.get('replay_pool', {}))
```

#### 5B: Attack success rate metric

In `fit()` after reward computation (alongside diversity metrics):
```python
if 'attack_success' in reward_tensor_map:
    metrics['attack/success_rate'] = reward_tensor_map['attack_success'].mean().item()
```

### Training Script

Create `scripts/rl/separated/grpo_dace_diversity.sh` based on existing `grpo_dace.sh`, adding:
```bash
# DACE diversity + replay config
algorithm.diversity.enable=true \
algorithm.diversity.use_dace_format=true \
algorithm.diversity.lambda_success=1.0 \
algorithm.diversity.lambda_fail=0.5 \
algorithm.replay_pool.enable=true \
algorithm.replay_pool.replay_batch_size=32 \
algorithm.replay_pool.gamma_decay=0.97 \
algorithm.replay_pool.max_pool_size=5000 \
# Must enable skip for replay to work
actor_rollout_ref.rollout.use_adversarial_prompt_for_defender=false \
actor_rollout_ref.rollout.skip_attacker_generation_for_defender=false \
```

Note: For the main (non-replay) training flow, `use_adversarial_prompt_for_defender` and `skip_attacker_generation_for_defender` stay `false`. The replay path triggers skip via the `is_replay` meta_info flag (P4D change).

---

## Key Design Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Diversity reward location | trainer (`ray_trainer.py`), not reward manager | Needs global archive state; keeps reward manager stateless |
| Archive dedup | Exact text hash | Simple, O(1); semantic dedup adds complexity with marginal benefit |
| Replay rollout | Reuse `multi_turn_generate_sequences` + `is_replay` flag | Minimal code change; reuses existing `skip_attacker_generation` mechanism |
| Replay merge point | After reward computation, before group filtering | Replay has own reward pipeline; merging here allows joint GRPO advantage |
| Stage transition detection | Compare `_prev_train_agent` vs new agent | Simple; works with both ratio and metric switching modes |
| Pool insertion timing | Buffer during stage, flush at stage transition | Avoids modifying pool mid-step which could affect diversity reward consistency |
| UID namespace | `replay_` prefix for replay samples | Prevents GRPO group contamination; replay and new samples get separate advantage normalization |

---

## Verification Plan

1. **P0 unit test**: Create `tests/test_archive_pool.py` — test extract_strategy, add_entry, dedup, thompson_sample, diversity_reward, time_decay, prune, save/load
2. **P1 unit test**: Test `format_reward_func_dace` with valid/invalid 3-tag strings; test `extract_strategy_text`; test `attack_success` computation
3. **P3 integration test**: Run 1 epoch with `diversity.enable=true, replay_pool.enable=false` — verify diversity rewards appear in metrics, archive grows
4. **P4 integration test**: Run 1 epoch with both enabled — verify replay batches generated, posterior updates happen, pool prunes
5. **End-to-end**: Run `grpo_dace_diversity.sh` for ~50 steps, check wandb for: `diversity/coverage_entropy` increasing, `replay/pool_size` growing, `attack/success_rate` tracking, no NaN/crash
