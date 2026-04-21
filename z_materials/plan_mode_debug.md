# 训练日志深度分析：DACE 诊断与改进计划

## Context

本文档针对 `DACE-Diversity-Qwen2.5_7B_Instruct-wo_sft-2026-04-15_01-49-37.log` 训练日志进行深度分析。训练运行了 300 步（约 10 轮 attacker/defender 交替），pool 从 0 增长到 2451 条目。通过交叉对比日志数据、当前代码实现、研究方法与修改计划，定位了 6 个观察到的问题的根因，并按 "代码 bug / 计划漏洞 / 研究方法问题" 进行分类。

**核心关键数据**（来自日志）：
- 每轮 attacker→defender 转换：flush 数百条（418→229→328→247→180→208→222→222→187→209）
- 每轮 defender→attacker 转换：几乎都是 flush 0 条（例外：step 46829 flush 1 条）
- Pool 增长但从未触发 prune（pool_mean_posterior 稳定在 0.60-0.64）
- timing_s/step 从 ~165s 增长到 ~250-370s
- attacker format reward：attacker 训练时 0.98→0.93，defender 训练时 0.33→0.15

---

## 问题 1：初始档案为空 → Round 1 Stage 1 diversity reward 恒为 0

### 观察
- step 1（Round 1 Stage 1 attacker 训练）：`diversity/mean_reward=0.000, pool_size=0, coverage_entropy=0`
- 整个 Round 1 Stage 1 的 15 步内 attacker 没有任何 diversity 信号
- 这段时间相当于"attacker 自由探索 + 基础 effectiveness reward"，没有多样性压力

### 根因分析
这是 **研究方法（Coverage 公式本质）+ 实现方式（buffer-and-flush 模式）** 的共同问题：

1. **数学本质**：当 `|A|=0` 时，`slot_counts=0`，`H(p_A)=0`。加入任何样本 x，`slot_counts[x]=1`，新分布是单点分布，`H=0`。所以 `delta=0`，`delta_max=0`，`R_div=0/(0+eps)=0`。这是 Coverage 公式在空池下的数学必然结果，与实现无关。

2. **实现加剧**：当前 `_compute_and_inject_diversity_rewards` 内的 buffer-and-flush 机制导致：
   - Stage 1 内所有成功攻击被放入 `_pending_success_buffer`，不进入 `archive_pool.slot_counts`
   - 因此 Stage 1 内档案池始终为空，diversity reward 始终为 0
   - 直到 Stage 1 结束切换到 defender 时，`_handle_stage_transition` 才把 buffer 刷入 pool

### 解决方案（三选一或组合）
**方案 A（推荐）：改为 defender 先手训练**（Q2 修复后）
- `start_agent=defender`
- 前提：Q2 修复后，Stage 1 defender 训练期间，新攻击成功样本能被缓冲入池
- 效果：Round 1 Stage 1 defender 结束时 pool 已有数百条 → Round 1 Stage 2 attacker 开始就有非零 diversity reward
- 符合 MAGIC baseline 的 defender 先手顺序，改动最小

**方案 B：预填充 archive**
- 在训练前用已有攻击样本（如 `vanilla_harmful_dataset_origin.jsonl` 或 SFT 数据）提取 strategy，初始化 pool
- 需要在 `ArchivePool.__init__` 增加 `load_from_file` 参数
- 风险：预填充的策略分布可能与在线训练偏离，反而引入偏差

**方案 C：mid-stage 增量入池**
- 每步结束后立即把成功样本加入 pool（去掉 buffer）
- 但这会造成同一 Stage 内 archive 持续变化，diversity reward 失去"Stage 内稳定"的性质，也打破研究方法的 pseudocode 设计

**最终建议**：采用方案 A，结合 Q2 修复。

---

## 问题 2：Stage 2（defender 训练）结束后 flush 几乎为 0

### 观察
- defender→attacker 转换时，flush 的新样本数量：10 次转换中 9 次为 0，1 次为 1
- attacker→defender 转换时 flush 数量正常（数百条）

### 根因分析：**代码实现 bug + 计划漏洞**

当前代码中有两处 buffer 写入点：

1. **`_compute_and_inject_diversity_rewards`（attacker stage only）**：
```python
if (... and self._current_train_agent == 'attacker'):
    self._compute_and_inject_diversity_rewards(...)
```
仅在 attacker 训练阶段运行。

2. **`_run_replay_pipeline` 的末尾部分**：
```python
# Buffer new successful attacks from replay for pool
for i in range(len(replay_batch)):
    if attack_success[i].item() > 0.5:
        ...
        self._pending_success_buffer.append({...})
```
只遍历 **replay_batch**，即从 pool 采样回来的历史样本。这些样本已经在 pool 中，`add_entry` 因 hash 匹配而返回 `False`，`n_added` 不递增。

**致命漏洞**：defender 训练阶段的 **new_batch**（即 B_train=64 条新种子、由当前 attacker 实时生成的攻击）中的成功样本，**没有任何代码路径将它们缓冲入池**。这直接违反了 pseudocode v3.1 第 43-45 行的要求：

```
43. for each 本阶段新攻击成功样本 x（∃ g: J(y^(g)) = harmful）do
44. if x ∉ A then A ← A ∪ {(x, b(x), s=1, f=0)}
45. else s_x ← s_x + 1
```

偶尔出现的 "Flushed 1" 可能源于 replay 样本经 `extract_answer` 后与原存储 prompt_text 有细微差异（如空白字符、tokenizer 重编码差异），导致 hash miss → 被当作新样本入池。

### 解决方案
**新增 `_buffer_new_successes_during_defender` 方法**，在 defender 训练阶段的 `fit()` 循环中，对 new_batch（不含 replay）执行：
- 提取每个样本的 attacker message 内容
- 通过 `ArchivePool.extract_strategy` 提取策略
- 判定 attack_success（使用 reward_tensor_map 中的 attack_success）
- 成功的样本构造 `prompt_data` 并 append 到 `_pending_success_buffer`

调用位置：在 defender 训练时 reward 计算完成后、filter_groups 之前（与 attacker stage 的 diversity injection 对称）。

同时，`_run_replay_pipeline` 末尾对 replay_batch 的 buffer 代码可以删除（因为它缓冲的都是重复条目），避免无意义的处理开销。

---

## 问题 3：attacker format reward 在 defender 训练时 ≈ 0.33 的成因

### 观察
- attacker 训练阶段：attacker format reward ≈ 0.98-0.95
- defender 训练阶段：attacker format reward ≈ 0.33
- 训练后期二者都下降：0.93 / 0.15

### 根因分析：**代码实现问题（metric 污染）**

**数学验证**：
- new_batch 大小 = B_train × G = 64 × 4 = 256 样本
- replay_batch 大小 = B_replay × G = 32 × 4 = 128 样本
- 合并后 total = 384 样本

对于 replay 样本，在 `_run_multi_turn_conversation` 的 skip 路径中（multi_agent_rollout.py L627-669）：
- 跳过 attacker 生成
- 将 archive 中的 `prompt_text`（即通过 `extract_answer` 提取的**纯答案文本，不含 tag**）作为 `current_outputs` 写入 history
- 该 history 条目 `role='attacker', content=archived_text, attacker_gen_skipped=True`

在 `GameRewardManager` 计算 format reward 时：
```python
format_r = compute_format_r(data_source, role, last_role_msg['content'], use_dace_format=True)
```
这里 `last_role_msg['content']` = 纯答案文本，不含 `<think>`、`<strategy>`、`<answer>` 标签。
`format_reward_func_dace` 检查三个 tag 的 counts（应为 `(1,1,1,1,1,1)`），实际全为 0 → 返回 **-FORMAT_REWARD_VALUE = -1.0**。

**期望公式**：
```
mean_attacker_format = (256 × new_format + 128 × (-1.0)) / 384
```

早期：new_format ≈ 0.98 → `(256×0.98 + 128×(-1))/384 = (250.9 - 128)/384 = 0.320` ≈ 0.33 ✓
晚期：observed mean = 0.15 → 反解 new_format = (0.15×384 + 128)/256 = 185.6/256 = **0.725**

这意味着 **defender 训练阶段的 new_batch attacker format 降到了 0.725**（attacker 训练阶段同期为 0.93）。差距来源：
- defender 训练时 attacker 以 `do_sample=False`（greedy）生成
- 由于 attacker 没在训练，其参数来自上一 attacker stage 的结尾
- 同时可能存在"greedy 输出的 format 质量低于 sampled 输出"的现象

### 解决方案

**A. 修正 metric 计算**（核心）
在 `compute_data_metrics` 或 reward_manager 中，让 attacker format reward 的统计**跳过 replay 样本**：
- 检查 `history[i]` 中 attacker message 是否有 `attacker_gen_skipped=True` 标记
- 或在 meta_info 中标注样本来源（new/replay），聚合时只对 new 求均值
- 新增两个独立 metric：`reward/format/attacker_new`（256 条）和 `reward/format/attacker_replay`（128 条，应始终为 -1）

**B. 分析 format 退化**
- 检查 timing 是否与格式退化相关：late stages 的 attacker pg_loss 是否偏离正常范围
- 可增大 `FORMAT_REWARD_VALUE`（当前 1，提高到 2 或 3）以加强格式训练信号
- 或者在训练后期加入 KL penalty 防止 attacker 漂移

**C. timing_s/step 增长的原因**
结合日志数据（165s→370s），可能成因：
- pool 增长到 2451 后，`_run_replay_pipeline` 中的 posterior update 循环（prune 遍历所有条目 O(|A|)）开销上升
- replay 时的 Thompson sampling 需要对 2451 个条目各采样一次 Beta → O(|A|)
- checkpoint 保存开销（JSON dump 大 pool）
- 建议添加细粒度 timing：`timing_s/thompson_sample`、`timing_s/prune`、`timing_s/archive_save`

---

## 问题 4：Diversity metrics 扩展 + mean_reward 的 stage 波动

### 观察
- 用户希望新增 `diversity/min_reward`、`diversity/max_reward`
- 观察到 mean_reward 在 attacker stage 逐步上升，在 defender stage 逐步下降
- Step 300 时 mean_reward = **-0.110**（负值！）

### 根因分析

**A. Metric 扩展的实现**（**代码实现层面，无障碍**）

当前 `_compute_and_inject_diversity_rewards` 只报告 mean。扩展为 min/max 非常简单：
```python
nonzero = div_rewards[div_rewards != 0]
metrics['diversity/min_reward'] = float(nonzero.min()) if len(nonzero) > 0 else 0.0
metrics['diversity/max_reward'] = float(div_rewards.max())
```
注意 `mean_reward` 是**当前 batch 内所有 256 个样本的 diversity reward 均值**（包含未提取到 strategy 的 0 值，以及 λ 折减后的值），不是 pool-level 的指标。需在文档/变量名中明确区分。

**B. 波动根因分析（多重因素复合）**

1. **Attacker stage 内"上升"**：
   - Stage 内 `slot_counts` 冻结（buffer-and-flush）
   - 随 attacker 训练更新，逐步学习选择**低频 slot**的策略以最大化 R_div
   - 表现为 mean_reward 单调上升

2. **Defender stage 期间的"下降"**：
   - `_compute_and_inject_diversity_rewards` 在 defender stage **根本不被调用**
   - 即 defender stage 内 `metrics['diversity/mean_reward']` 不被设置
   - WandB 图表中显示的是"插值/最后一次值的延续"，并非真实下降
   - **这是视觉误解**，实际上这段时间没有任何数据点

3. **Step 300 mean_reward = -0.110（负值）的解释**：
   - 意味着 attacker 选择的策略 slot 比平均频率高（处于饱和区）
   - 可能原因：attacker 在后期"收敛"到某些 effective 策略，即使这些策略已频繁出现
   - 数学上：`R_div = delta / (delta_max + eps)` 中 delta 为负（高频 slot）、delta_max 为正（低频 slot），比值为负
   - 表明训练后期**多样性压力失效**：effectiveness reward 主导，attacker 甘愿接受负 diversity reward

### 解决方案

**A. Metric 扩展**：实现 min/max 只需加几行代码。

**B. 解决视觉误解**：在 defender stage 也记录当前 archive 的 metric 快照（即使不计算 per-sample 的 R_div）：
- `diversity/coverage_entropy` 和 `diversity/strategy_coverage` 都只依赖 pool 状态，可以在每步都报告
- 将这两个 metric 从 `_compute_and_inject_diversity_rewards` 中抽出，在 `fit()` 的每步结束时统一报告

**C. 解决 mean_reward 真实波动（负值问题）**：
- 增大 `lambda_success`（例如 2.0→3.0），让多样性压力更强
- 或者在多样性收益为负时**截断到 0**（只奖励高于平均的多样性选择）：`r_div = max(0, r_div)`
- 或改用更稳定的 Novelty 公式（`1 - n(b)/n_max`），始终在 [0,1] 范围，不会出现负值

---

## 问题 5：reward/refusal_rate_harmful 和 refusal_rate_benign 的波动

### 观察
- `reward/refusal_rate_harmful`：多次下降后回升
- `reward/refusal_rate_benign`：明显的 stage 振荡
- step 1: harmful=0.404, benign=0.021
- step 148: harmful=0.493, benign=0.221
- step 300: harmful=0.747, benign=0.192

### 根因分析：**训练动力学 + 采样差异**

**A. refusal_rate_harmful 下降 → 回升的循环**
- attacker 训练阶段：attacker 探索新型攻击（do_sample=True，温度=1.0），defender 未见过 → 拒绝率下降（攻击成功）
- defender 训练阶段：defender 学习应对 → 拒绝率上升
- 每轮周期性重复

**B. refusal_rate_benign 的 stage 振荡**
- 目标：benign 不应拒答，refusal_rate_benign 应低
- attacker 对 benign prompt 改写时，改写后的 prompt 可能看起来像 harmful → defender 选择拒答（over-refuse）→ 攻击"成功"（对 benign 而言 over-refuse 是我们希望攻击检测的）
- 但 defender 训练时学到"不要 over-refuse"，该指标下降

**C. step 148 附近出现特殊波动**
- 观察：refusal_rate_benign=0.221，较其他步显著升高
- 148 ≈ 10 轮中间，pool 大小 1403
- 可能原因：attacker 在某轮学到了对 benign prompt 改写的新手法（欺骗 defender over-refuse），使 refusal 瞬时升高

### 是否是问题？
**不是 bug，是训练动力学的正常表现**。这种 stage 振荡在 MAGIC baseline 中也会出现。

### 改善方案（可选）
- 使用 EMA（指数移动平均）smooth metrics 曲线
- 增加 metric `reward/refusal_rate_benign_trend`（last 10-step moving average）
- 研究方法层面：验证集评估（test parquet）应在每轮结束后运行，看端到端 ASR 是否在稳定下降

---

## 问题 6：Replay pool prune 从不触发 + metric 扩展

### 观察
- Pool_size 10 轮内从 418 增长到 2451，**从未触发 prune**（日志中未见 `[ArchivePool] Pruned X entries` 信息）
- pool_mean_posterior 稳定在 0.60-0.64
- 用户希望新增 `pool_min_posterior`、`pool_max_posterior`

### 根因分析：**研究方法参数 + 研究方法缺陷**

**A. Metric 扩展**：显然可行，与 Q4 一样简单：
```python
posteriors = [(pool.alpha_prior + e.successes) / 
              (pool.alpha_prior + e.successes + pool.beta_prior + e.failures)
              for e in pool.entries]
metrics['replay/pool_min_posterior'] = float(min(posteriors))
metrics['replay/pool_max_posterior'] = float(max(posteriors))
metrics['replay/pool_median_posterior'] = float(np.median(posteriors))
```

**B. Prune 从不触发的深层原因（三重复合）**：

1. **Prune 条件过严**：`p̂ < 0.20 AND (s+f) > 3`
   - 新入池样本 (s=1, f=0): p̂ = 2/3 = 0.667
   - 需要通过 posterior update 把 p̂ 压到 0.20 以下

2. **绝大多数样本从未被 replay**：
   - Pool size 2451，每步 replay 32 条 (top Thompson samples)
   - 每轮 15 个 defender 训练 step × 32 replay = 480 次/轮 replay 机会
   - 但 Thompson 采样偏向 p̂ 高的样本（经过多次 replay 的成功样本）
   - 绝大多数样本经历**纯时间衰减**而无 posterior update
   - 纯衰减下：s_k = 0.9^k × 1, f_k = 0 → p̂ → 0.5（趋近均匀先验均值）
   - 永远达不到 0.20 阈值

3. **即使被持续 replay 且 defender 全部拦截**：
   - 如前分析，需要 ~7+ 轮连续 replay 失败才能让 p̂ < 0.20
   - 但 10 轮内一个样本能被 replay 10 次的概率极低（参考 top-32 采样）

**C. 为什么 pool_mean_posterior 稳定在 0.60-0.64**
- 大部分条目 p̂ ≈ 0.5（趋近先验）
- 少数被 replay 成功的条目 p̂ 较高（0.7-0.9）
- 平均落在 0.6 附近

### 解决方案

**方案 1（推荐组合）**：放宽 prune 阈值 + 加入 age-based 剪枝
- `prune_threshold=0.35`（当前 0.20）：纯衰减趋近 0.5 时不会被剪；但 replay + 全拦截 3-4 轮就能达到
- `prune_min_trials=2.0`（当前 3.0）：尽早进入可剪状态
- **新增 idle-based prune**：如果条目 `(self.global_steps - entry.step_added) > K_steps AND trials == 0`，则剪除（永远没被 replay 过的僵尸样本）
- K_steps 可设为 `freq × 20 ~ 50`（对应 10-25 轮）

**方案 2：改为 asymmetric decay**
- 只衰减 s，不衰减 f：`s_i ← γ·s_i, f_i 不变`
- 这样成功记忆被"遗忘"，失败记忆被保留
- 更符合"过时成功不再威胁，失败证据持续"的直觉
- p̂ 单调下降，自然触发 prune

**方案 3：动态 pool size 限制**
- 当前 `max_pool_size=5000` 且实现了"超出时删除最低 p̂"逻辑，但 pool 才 2451 未触发
- 降低 `max_pool_size` 到 1500-2000，强制 FIFO 清理低价值条目

---

## 额外观察：模板演变与 format reward 起始高值

### 用户提到的"旧模板只有 2-tag"
但日志 step 1 的 attacker 输出（见 log agent 报告）清晰显示 3-tag 格式，且 `reward/format/attacker=0.984`。

**矛盾解释**：
- 可能用户回忆的"旧模板"是更早版本（训练本日志时模板已经更新为 3-tag）
- 或者 Qwen2.5-7B-Instruct 的 instruction-following 能力足够好，即使系统提示只要求 2-tag，在策略空间的其他指导下也能自动产生 `<strategy>` 标签（可能性较低）
- **实际影响**：不影响本次分析结论，因日志中 attacker 格式稳定。

---

## 分类汇总与改进优先级

| 问题 | 分类 | 严重度 | 优先级 |
|------|------|-------|--------|
| Q1: 初始 archive 空 → R1S1 diversity=0 | 研究方法 + 实现选择 | 中 | **P1** |
| Q2: defender stage 不缓冲新成功样本 | **代码 bug + 计划漏洞** | **高** | **P0** |
| Q3: attacker format metric 被 replay 污染 | **代码实现（metric 计算）** | 中（功能正常但误导） | **P1** |
| Q4: diversity metric 缺 min/max + 负值 | 实现（简单扩展）+ 研究方法（负值语义） | 中 | **P1** |
| Q5: reward refusal 波动 | 训练动力学（正常） | 低 | P2 |
| Q6: prune 从不触发 + metric 缺 min/max | 研究方法（参数）+ 实现扩展 | 中 | **P1** |

---

## 推荐行动计划（最终版 — 已经用户确认）

### 用户选定的设计决策
- **Q1**: Defender-first 训练顺序 + 修复 Q2
- **Q4**: 截断负 diversity reward 到 0
- **Q6**: 仅调整 prune 参数（不引入 idle-based 剪枝）
- **Metric 扩展**: 只加 min/max

---

### P0 — 立即修复（代码 bug 必须修复）

**P0.1 修复 Q2：defender 阶段缓冲新攻击成功样本**

新增 `_buffer_new_successes_during_defender` 方法到 `ray_trainer.py`，包含：
- 遍历 new_batch 的每个样本（不含 replay）
- 通过 `ArchivePool.extract_strategy` 提取策略
- 如果 attack_success=True，构造 prompt_data 并 append 到 `_pending_success_buffer`
- 同时提供 metric: `diversity/pending_buffer_size_new`

调用位置：在 defender 训练时、reward 计算完成后、filter_groups 之前（与 attacker stage 的 diversity injection 位置对称）。

同时删除 `_run_replay_pipeline` 末尾冗余的 replay 样本 buffer 逻辑（因为 replay 样本都是 pool 内重复条目）。

**P0.2 修正 Q3：attacker format reward metric 不被 replay 污染**

在 reward_manager 或 metric_utils 层面，让 `reward/format/attacker` 的均值计算：
- 跳过 `attacker_gen_skipped=True` 的样本（replay 样本）
- 或利用 `is_replay` meta_info 标记
- 额外记录 `reward/format/attacker_new`（仅 new_batch）和 `reward/format/attacker_replay`（仅 replay，预期恒为 -1）

修改涉及：
- `src/verl/verl/workers/reward_manager/game.py`：在 `role_format_rewards` 赋值时根据 skip 状态区分
- 或 `src/verl/verl/separated_trainer/ppo/metric_utils.py`：在聚合时过滤

---

### P1 — 建议改进

**P1.1 改为 Defender 先手（Q1）**

修改训练脚本 `scripts/rl/separated/grpo_dace_diversity.sh`：
```bash
algorithm.switch_agent.start_agent=defender  # 从 attacker 改为 defender
```

**P1.2 截断 diversity reward 负值（Q4）**

修改 `src/verl/verl/separated_trainer/ppo/archive_pool.py` 的 `compute_diversity_reward`：
```python
def compute_diversity_reward(self, strategy: Tuple[int, int]) -> float:
    delta = self._compute_marginal_entropy_gain(strategy)
    delta_max = self._compute_max_marginal_gain()
    r_div = delta / (delta_max + self.epsilon)
    ### dace: clip negative diversity reward to 0 ###
    return max(0.0, r_div)
```

可选：新增配置项 `algorithm.diversity.clip_negative: true`，控制是否启用该截断。

**P1.3 调整 prune 参数（Q6，仅调参）**

在 `ppo_trainer.yaml` 和 `grpo_dace_diversity.sh` 中调整：
```yaml
replay_pool:
  prune_threshold: 0.35   # was 0.20, 放宽以应对 zombie 条目
  prune_min_trials: 2.0   # was 3.0, 尽早允许剪枝
```

注意：此方案不引入 idle-based 剪枝，保持代码简洁。zombie 条目问题仅通过 `max_pool_size=5000` 的硬上限 + 最低 p̂ 驱逐机制约束。可以适当调小 `max_pool_size` 到 2000-3000 以更早触发硬上限。

**P1.4 Metrics 扩展 — 只加 min/max**

修改 `_compute_and_inject_diversity_rewards`，添加：
```python
nonzero = div_rewards[div_rewards != 0]
metrics['diversity/min_reward'] = float(nonzero.min()) if len(nonzero) > 0 else 0.0
metrics['diversity/max_reward'] = float(div_rewards.max())
```

修改 `_run_replay_pipeline`，添加：
```python
if self.archive_pool.entries:
    posteriors = [(self.archive_pool.alpha_prior + e.successes)
                   / (self.archive_pool.alpha_prior + e.successes 
                      + self.archive_pool.beta_prior + e.failures)
                   for e in self.archive_pool.entries]
    metrics['replay/pool_min_posterior'] = float(min(posteriors))
    metrics['replay/pool_max_posterior'] = float(max(posteriors))
```

额外建议：将 `diversity/coverage_entropy` 和 `diversity/strategy_coverage` 从 `_compute_and_inject_diversity_rewards` 抽出，在 `fit()` 每步结束时都报告一次，避免 defender stage 的 metric gap。

---

### 修改文件清单

| 文件路径 | 修改内容 | 优先级 |
|---------|---------|-------|
| `src/verl/verl/separated_trainer/ppo/ray_trainer.py` | 新增 `_buffer_new_successes_during_defender` 方法；在 defender stage 调用；删除 `_run_replay_pipeline` 末尾冗余 buffer；扩展 metrics；抽 coverage metric 到每步 | P0 + P1 |
| `src/verl/verl/separated_trainer/ppo/archive_pool.py` | `compute_diversity_reward` 截断负值 | P1 |
| `src/verl/verl/workers/reward_manager/game.py` | attacker format reward metric 过滤 replay 样本 | P0 |
| `src/verl/verl/separated_trainer/config/ppo_trainer.yaml` | prune_threshold=0.35, prune_min_trials=2.0, max_pool_size=2000 | P1 |
| `scripts/rl/separated/grpo_dace_diversity.sh` | start_agent=defender, prune_threshold=0.35, prune_min_trials=2.0 | P1 |

所有新增代码加上 `### dace: <description> ###` 标注。

---

## 验证方法

修复后重新运行 `grpo_dace_diversity.sh`，检查：

1. **Q1 + Q2 修复验证**：
   - 日志应显示 `Training switching to attacker` 后紧跟 `[DACE] Flushed X ... (total: Y)`，X > 0（至少几十条）
   - Round 1 Stage 2 attacker 开始（步 16-30 附近）应有 `diversity/mean_reward > 0`，而不再全零

2. **Q3 修复验证**：
   - `reward/format/attacker` 在 defender stage 应接近 `reward/format/attacker` 在 attacker stage（都接近 1.0）
   - 或者新增的 `reward/format/attacker_new` 在所有 stage 均在 0.9+ 附近
   - `reward/format/attacker_replay`（如添加）恒为 -1

3. **Q4 修复验证**：
   - `diversity/min_reward ≥ 0` 始终成立
   - 后期训练 `diversity/mean_reward` 不再出现负值

4. **Q6 修复验证**：
   - 日志中应出现 `[ArchivePool] Pruned X entries` 消息，X > 0
   - `replay/pool_size` 不再单调增长，某些时刻应下降或趋稳
   - `replay/pool_mean_posterior` 分布更健康（可对比调整前后的 pool_min/max/mean）

5. **P2 Timing 稳定性**：
   - `timing_s/step` 不应随 pool 增长呈线性爆炸
   - 若问题持续，再考虑添加细粒度 timing profiling 定位瓶颈

---

## 与研究方法 (v3.1) 的一致性检查

| 研究方法要点 | 当前实现状态 | 修复后状态 |
|-------------|------------|-----------|
| pseudocode L3-4：round 开始 decay | ✓ 已在 `_handle_stage_transition` 实现 | ✓ 保持 |
| pseudocode L19-21：Stage 1 结束成功样本入池 | ✓ attacker stage 已实现 | ✓ 保持 |
| pseudocode L43-45：Stage 2 结束新攻击成功样本入池 | ✗ **未实现（bug）** | ✓ P0.1 修复 |
| pseudocode L28-30：Thompson Sampling 取 top B_replay | ✓ 已实现 | ✓ 保持 |
| pseudocode L34-35：replay 样本 posterior 更新 | ✓ 已实现 | ✓ 保持 |
| pseudocode L41-42：每 batch 后 prune | ✓ 已实现，但触发率极低 | ✓ 参数调优解决 |
| 研究方法 2.2：lambda_success=1.0, lambda_fail=0.5 | ✓ 已实现 | ✓ 保持 |
| 研究方法 2.3：Normalized Marginal Coverage Gain | ✓ 已实现 | 🟡 加截断（方法轻微改动） |

整体上，本次修复主要补齐 pseudocode L43-45 缺失的实现，并通过参数调优和截断处理对齐训练实际行为，不涉及研究方法的本质修改。

