请进入 plan mode，基于以下详细的功能需求和代码分析，为在现有 MAGIC 框架上实现"攻击多样性"和"贝叶斯对抗回放池"两大功能制定完整的代码修改计划。
详细要求以 [研究方法v3.1.md] 和 [pseudocode_v3.1.html] 为主，以 [功能说明、代码层面的约束和需要思考的问题] 为辅。
请先充分阅读参考材料和现有代码，再逐文件给出具体修改方案。如果有存在冲突或者有不确定存疑的地方请及时提问，我会给你反馈信息。


# 在 MAGIC 框架上实现多样性驱动与回放池功能

---

## 参考材料

@z_materials/MAGIC_Latex/arxiv.tex ，这是 MAGIC baseline 论文的 latex 源码（包含其伪代码）。
@z_materials/研究方法v3.1.md ，这是我们在 MAGIC 基础上引入多样性和回放池的研究方法。
@z_materials/pseudocode_v3.1.html ，这是与我们的研究方法v3.1对应的详细的伪代码。
@data/safety/preprocess_dace.py ，这是我们方法的数据预处理的步骤和 prompt 内容。

请根据 [研究方法v3.1.md] 和 [pseudocode_v3.1.html]，在现有 MAGIC 代码框架上制定详细具体的代码修改计划，方便交给下一阶段逐步实现。下面是功能说明、代码层面的约束和需要思考的问题。

---

## 一、需要实现的两大功能

### 功能 1：攻击多样性（解决攻击策略坍缩）

引入显式的二维攻击策略空间 B = S × C（风险类别 × 攻击方式）来引导攻击者改写 prompt，并在攻击者奖励中加入多样性奖励项。

**核心要素：**

1. **攻击策略空间定义**：定义风险类别集合 S（如暴力犯罪、非暴力犯罪、性相关、自残自杀、仇恨歧视、危险物质等）和攻击方式集合 C（如角色扮演、权威操纵、术语伪装、故事嵌入、逻辑诱导等），每个攻击样本映射到 b(x) = (s, c) ∈ B。

2. **攻击者 prompt 模板改造**：在攻击者的 system prompt / user prompt 中提供完整的策略空间描述（所有 |S|×|C| 种策略组合的定义），要求攻击者：
   - 先推理选择一种最适合当前 seed prompt 的攻击策略 (s, c)
   - 在所选策略引导下将原始 prompt 改写为具有隐蔽性的对抗 prompt
   - 输出格式改为 `<think>推理过程</think><strategy>(s, c)</strategy><answer>改写后的 prompt</answer>`

3. **行为描述符提取**：从攻击者回复中通过正则表达式提取 `<strategy>` 标签内的 (s, c) 值，作为该样本的行为描述符 b(x)。

4. **多样性奖励计算 — 归一化边际覆盖增益（Coverage）**：
   - 维护档案池 A 中各策略槽位的频次分布 p_A
   - 计算 Shannon 熵 H(p) = -∑ p_i * log(p_i)，只对 p_i > 0 的项求和（p_i = 0 时跳过，避免 log(0) 的数值不稳定）
   - 分子 = 样本 x 加入后的熵增：H(p_{A∪{x}}) - H(p_A)
   - 分母 = 当前档案池下单步最优熵增（遍历所有槽位取最大值，batch 内共享，只计算一次）
   - R_div(x) = 分子 / (分母 + ε)
   - Coverage 和 Novelty 是多样性的两种可选定义（并非协同互补），这里选择 Coverage 定义作为实现

5. **差异化多样性系数**：
   - 攻击成功样本：λ = 1.0（完整多样性奖励）
   - 攻击失败样本：λ = 0.5（折减多样性奖励，保留探索压力）

6. **攻击成功判定**（基于 data_type 和 defender 响应）：
   - harmful 样本（data_type='vanilla_harmful'）：defender 输出有害回答 → 攻击成功
   - benign 样本（data_type='vanilla_benign'）：defender 输出有害回答 **或** defender 拒绝回答 → 攻击成功（即对 benign 样本，defender 应正常回答且不拒答）

7. **攻击者总奖励**：R_A = (-r_harm - r_refusal) + r_fmt + λ · r_div

### 功能 2：贝叶斯对抗回放池（解决防御对抗遗忘）

将攻防过程中攻击成功的样本放入统一档案/回放池，在防御者训练时混入历史高风险样本。

**核心要素：**

1. **统一攻击档案池 A**：同时承担策略频次记录（功能 1 的多样性奖励计算）和对抗回放（功能 2 的防御者补训）。池中存储攻击成功的改写 prompt（仅攻击者改写后的 prompt，不含防御者回复），每个样本维护：
   - 行为描述符 b(x)
   - Beta-Bernoulli 后验参数 (s_i, f_i)：s_i 为衰减累计攻破次数，f_i 为衰减累计拒绝次数
   - 后验均值 p̂_i = (α + s_i) / (α + s_i + β + f_i)

2. **入池时机**：Stage 1（攻击者训练）和 Stage 2（防御者训练）结束后，各自将本阶段攻击成功样本放入池中。新样本初始化 s=1, f=0；已存在样本则 s_i += 1。

3. **时间衰减**：每轮（round）开始时对池中所有样本执行 s_i ← γ·s_i, f_i ← γ·f_i（γ ∈ [0.95, 0.99]），使后验跟踪防御者能力的演化。

4. **Thompson Sampling 采样**：在防御者训练的每个 step 中，对池中每个样本采样 p̃_i ~ Beta(α + s_i, β + f_i)，取 p̃_i 最高的 B_replay 个样本。

5. **后验更新**：对被采样的回放样本，用当前 defender 生成响应后判定攻击成败——若 G 个 rollout 中存在任一有害响应则 s_j += 1，否则 f_j += 1。

6. **剪枝**：p̂_i < ε 且 (s_i + f_i) > n_min 时移除样本。

7. **防御者混合 batch 训练**：
   - 每个 training step 的 batch 由 B_train 个新攻击样本 + B_replay 个回放样本组成
   - B_replay 设为 B_train/2 或 B_train/4（可配置）
   - 当池中样本不足 B_replay 时，仅使用新攻击样本训练

---

## 二、代码层面的关键约束和参考

### 2.1 现有训练流程中的关键机制

**UID 与 repeat 机制**（ray_trainer.py L1620-1622）：
```
原始 batch 64 条 → repeat(G=4) 后 256 条
uid:    [u₁,u₁,u₁,u₁, u₂,u₂,u₂,u₂, ...]
```
同一 seed prompt 的 G 个副本共享同一个 uid。利用 uid 可以追踪一组 rollout 中是否存在攻击成功的样本，这对以下场景至关重要：
- Stage 1 结束后判定哪些攻击者改写样本应入池
- Stage 2 中回放样本的后验更新（G 个 defender rollout 中是否存在 harmful 响应）

**Agent 切换机制**（ray_trainer.py L1435-1507）：
- 当前使用 ratio 模式 round-robin 切换，由 `switch_agent.freq` 控制切换频率
- `_current_train_agent` 标识当前训练角色（'attacker' 或 'defender'）
- 在训练 defender 时，attacker 使用 greedy（do_sample=False）生成单条攻击，然后 repeat G 次给 defender 做 GRPO。这是一种近似等价实现：repeat(G) + greedy ≈ 生成1次 + 复制G份

**Reward 计算流程**（game.py + reward_manager/game.py）：
- `GameRewardManager.__call__()` 对整个 batch 并行计算 reward，返回 `reward_tensor_map` 字典
- 各角色的 reward 在 `reward_tensor_map[f'{role}_turn_level_reward']` 中分别赋值（reward_manager/game.py L326-346）
- 攻击者奖励 = -base_score + revision + label_reward（L329）
- 防御者奖励 = base_score + defender_quality（L331）
- format reward 在此之后单独加入

**Format reward**（game.py L279-298）：
- 当前校验格式为 `<think>...</think><answer>...</answer>`
- 需要扩展为 `<think>...</think><strategy>...</strategy><answer>...</answer>` 以适应新的攻击者输出格式

**split_batch_for_agents()**（ray_trainer.py L318-357）：
- 将包含 attacker_/defender_ 前缀的 batch 拆分为各角色独立的 DataProto
- 新增的多样性奖励需要整合到 `attacker_turn_level_reward` 中

### 2.2 数据流关键节点

在 `fit()` 主循环（ray_trainer.py L1546-1925）中，关键数据流节点如下：
1. **L1610-1622**：从 dataloader 取 batch，分配 uid，repeat G 次
2. **L1648**：multi_turn_generate_sequences → 生成 attacker/defender 对话
3. **L1700-1738**：reward_fn 计算 reward_tensor_map，写入 new_batch.batch
4. **L1740-1793**：uid 聚合 + group filter
5. **L1810-1819**：split_batch_for_agents → 取当前训练角色的 batch → compute_token_level_scores
6. **L1856-1866**：compute_log_prob + ref_log_prob
7. **L1881**：update_actor
8. **L1899-1911**：metrics 日志

多样性奖励和回放池的逻辑需要在这些节点之间合理插入。

### 2.3 配置文件扩展

在 `src/verl/verl/separated_trainer/config/ppo_trainer.yaml` 中添加回放池相关超参数，具体数值通过 shell 训练脚本覆盖：

```yaml
algorithm:
  diversity:
    enable: true
    reward_type: coverage  # coverage 或 novelty
    lambda_success: 1.0    # 攻击成功样本的多样性系数
    lambda_fail: 0.5       # 攻击失败样本的多样性系数
    epsilon: 1e-8          # 归一化分母的平滑项

  replay_pool:
    enable: true
    alpha: 1.0             # Beta 先验 α
    beta: 1.0              # Beta 先验 β
    gamma: 0.97            # 时间衰减因子
    epsilon: 0.05          # 剪枝阈值
    n_min: 5.0             # 最小试验次数阈值
    replay_ratio: 0.5      # B_replay / B_train 的比例（0.5 或 0.25）
```
注意区分这里的两个 epsilon 参数：diversity.epsilon 和 replay_pool.epsilon

---

## 三、需要在计划中回答的实现问题

### 3.1 档案池的数据结构与存储

1. **档案池应该作为 `RayReMASeparatedTrainer` 的实例属性**，在 `__init__` 中初始化，跨 step/epoch 持久存在。建议用 Python dict 或自定义类实现，key 为攻击 prompt 的文本（或其 hash），value 为 `{prompt, behavior_descriptor, s_i, f_i, round_added}` 等字段。

2. **prompt 去重/查重策略**：如何判断 attack prompt 是否已在档案池中？直接 `if prompt_text in archive_dict` 基于字符串精确匹配？还是需要做语义去重（计算 embedding 相似度）？精确匹配简单高效但可能遗漏微小变体；语义去重引入额外计算开销。建议先用精确匹配（`prompt_text` 作为 dict key），如果实验中发现大量近重复样本再考虑 hash 或 embedding 方案。

3. **策略频次分布**：维护一个 `Counter` 或 numpy array，shape 为 `(|S|, |C|)`，记录各槽位的累计频次。每次入池时更新。用于多样性奖励的熵计算。

4. **档案池是否需要持久化到磁盘**？建议在每个 round 结束时将档案池 dump 到 checkpoint 目录（JSON/pickle），以支持断点续训。

### 3.2 行为描述符提取

1. 攻击者输出格式：`<think>推理过程</think><strategy>(risk_category, attack_method)</strategy><answer>改写后的 prompt</answer>`

2. 正则提取 `<strategy>` 标签内容，解析出 (s, c)。需要处理提取失败的 fallback 情况（如攻击者未按格式输出）：
   - 方案 A：提取失败时分配到一个特殊的 "unknown" 槽位
   - 方案 B：提取失败时给 format reward 扣分（已有机制），多样性奖励设为 0
   - 建议采用方案 B，与 format reward 联动

3. 策略空间 S 和 C 的定义需要提前确定并硬编码到代码和 prompt 模板中，或者作为外部配置文件加载。

### 3.3 攻击成功判定的具体实现

当前 `compute_score_components()` 已经返回 `question_is_harmful`（来自 WildGuard 对 prompt 的判定）和 `defender_refused`（defender 是否拒答）。但研究方法要求基于 **data_type**（数据集标注）而非 reward model 的判定来区分 harmful/benign：

- `data_type == 'vanilla_harmful'`：攻击成功 ← defender 输出有害回答（qa_safe_label ∈ {Unsafe, Controversial}）
- `data_type == 'vanilla_benign'`：攻击成功 ← defender 输出有害回答 **或** defender 拒绝回答（qa_refusal_label == 'Yes'）

这需要在 `GameRewardManager.__call__()` 或上层逻辑中，基于已有的 `reward_tensor_map` 中的 `question_is_harmful` 和 `defender_refused` 以及 `extra_info['data_type']` 计算攻击成功标志。

注意：当前代码中 `question_is_harmful` 来自 WildGuard 的判定，可能和 data_type 标注不完全一致（攻击者改写后 benign prompt 可能被 WildGuard 判为 harmful）。需要明确以哪个为准——建议以 **原始 data_type** 为准，因为攻击成功的定义应基于原始任务意图。

注意：采用类似 MAGIC 中 USE_Q_SAFE_LABEL_FOR_REFUSAL 的逻辑，我们这里也使用 Attacker 改写后 prompt 的 safety_label 替换原始的 data_type！！！

### 3.4 多样性奖励的计算位置

多样性奖励需要访问全局的档案池频次分布，因此**不适合在 `GameRewardManager.__call__()` 内部计算**（那里是纯 reward 计算，不应有全局状态依赖）。建议：

- 在 `GameRewardManager.__call__()` 中正常计算 harm/refusal/format reward 并返回
- 在 `ray_trainer.py` 的 `fit()` 循环中，reward 计算完成后（约 L1738 后），单独计算多样性奖励并叠加到 `attacker_turn_level_reward` 上
- 这样档案池和多样性计算逻辑集中在 trainer 层，保持 reward manager 的无状态性

### 3.5 回放样本的 rollout 与训练整合

**核心难点：回放样本需要独立于种子数据走一遍 defender rollout 和 reward 计算，然后和新攻击样本的 batch 合并进行 GRPO 更新。**

具体流程设计：

1. 在防御者训练的每个 step 中，正常流程生成新攻击 batch（B_train 个 seed → attacker 改写 → defender rollout → reward）
2. 从档案池 Thompson Sampling 采样 B_replay 个 prompt
3. 回放 prompt 需要包装成 DataProto 格式，走 defender-only 的 rollout（无需 attacker 生成，直接用池中的攻击 prompt 作为 defender 输入）
4. 对回放 prompt 的 defender 响应计算 reward
5. 将新攻击 batch 和回放 batch 合并（DataProto.concat），统一做 advantage 计算和 GRPO 更新

**关键实现问题：**
- 回放样本的 rollout 应复用 `multi_turn_generate_sequences` 还是走更简单的单步 defender generation？由于回放的只是攻击 prompt（不含 defender 回复），应该只需要 defender 的 forward pass，不需要再走 attacker → defender 的完整多轮对话流程。需要新增一个专用的回放 rollout 函数或对现有函数进行参数化。
- 回放样本的 DataProto 需要包含和新攻击样本相同的 keys（uid, data_type, input_ids, attention_mask 等），以确保下游的 split_batch, advantage 计算, actor update 等环节正常工作。
- 回放样本合并后 batch size 变大（B_train + B_replay），需要确认 GRPO 的 group advantage 计算是否能正确处理不同来源的样本。特别是 uid-based 的 group filter 逻辑（L1740-1793）需要确保回放样本的 uid 不与新样本冲突。

### 3.6 两阶段迭代的控制逻辑

当前 MAGIC 使用 `switch_agent` 配置控制 attacker/defender 交替。研究方法的两阶段设计（Stage 1: 攻击者训练 → Stage 2: 防御者混合训练）本质上与现有的 ratio 模式 round-robin 切换兼容。需要明确：

- 每个 "round" 对应 `switch_agent.freq` 个 step 的 attacker 训练 + `switch_agent.freq` 个 step 的 defender 训练
- 时间衰减应在每个 round 开始时（即从 defender → attacker 切换时）执行
- 入池操作应在每个 stage 结束时（即 agent 切换前）执行
- 建议在 `_update_current_train_agent()` 中检测 agent 切换事件，触发入池和衰减操作

### 3.7 Format reward 修改

将攻击者的 format reward 校验从当前的 `<think>...</think><answer>...</answer>` 扩展为：
```
<think>推理过程</think><strategy>(s, c)</strategy><answer>改写后的 prompt</answer>
```
需要修改 `format_reward_func()`（game.py L279-298），增加对 `<strategy>` 标签的检查。注意这个修改**仅影响攻击者**（defender 的格式不变）。当前 format reward 已经有 role-aware 的机制（reward_manager/game.py L336: `if role in format_reward_roles`）。

### 3.8 Metrics 扩展

在每个 step 的 metrics 中额外记录：
- `replay/pool_size`：当前档案池中的样本数量
- `replay/strategy_coverage`：已有攻击策略的数量 / 定义的策略总数 |B|
- `replay/strategy_entropy`：当前策略分布的 Shannon 熵
- `replay/pool_mean_posterior`：池中样本后验均值的平均值
- `diversity/batch_reward_mean`：当前 batch 的平均多样性奖励
- `attack/success_rate`：当前 batch 的攻击成功率

### 3.9 分布式环境下的一致性

当前训练使用 Ray 分布式。档案池作为 trainer 实例属性存在于 driver process 中，reward 计算在 worker process 中执行。需要确认：
- 档案池的更新和采样都在 driver process 中完成（在 reward 计算返回后），不需要跨 worker 同步
- 多样性奖励的计算也在 driver process 中完成（作为 reward 的后处理），然后叠加到 batch 的 tensor 中再分发给 worker 做 GRPO 更新
- 这种设计避免了分布式一致性问题，但需要确认 driver process 有足够的内存存储档案池

### 3.10 攻击者 prompt 模板设计

当前攻击者 prompt（prompt/game/single_turn.py）非常简洁。新的 prompt 需要：
1. 在 system prompt 中描述完整的策略空间 B = S × C（所有组合的定义和简要说明）
2. 在 user prompt 中给出 seed question 并要求攻击者按指定格式输出
3. 模板较长，建议将策略空间描述抽取为独立的配置文件（如 `prompt/game/strategy_space.py` 或 JSON），方便后续调整策略定义

需要仔细设计 prompt 以确保攻击者理解并遵循策略选择 → 改写的两步流程。

注意：@data/safety/preprocess_dace.py ，这是我们方法的数据预处理的步骤和 prompt 内容！！！

### 3.11 回放样本的 DataProto 构造

从档案池采样的回放 prompt 需要构造成合法的 DataProto，这涉及：
- tokenize 回放 prompt 为 input_ids / attention_mask
- 填充必要的 non_tensor_batch 字段（data_source, data_type, uid, extra_info 等）
- 回放样本不需要走 attacker generation，直接作为 defender 的输入
- 需要处理 tokenizer 和 padding 的对齐，使回放 batch 与新攻击 batch 可以 concat

这本质上需要一个 `build_replay_batch()` 函数，将纯文本 prompt 列表转换为 DataProto。可以参考 `GameDataset.__getitem__()` 和 `collate_fn()` 的实现。

---

## 四、实现优先级建议

建议按以下顺序实现，每步可独立验证：

1. **P0 - 攻击策略空间 + prompt 模板 + 行为描述符提取 + format reward 修改**：纯模板/正则/reward 层面的改动，不涉及训练流程，可快速验证格式是否正确。
2. **P1 - 档案池数据结构 + 策略频次维护 + 多样性奖励计算**：在 trainer 中实现档案池和 Coverage 奖励，叠加到攻击者 reward 中。可以先不做回放，只验证多样性奖励是否生效。
3. **P2 - 攻击成功判定 + 入池逻辑 + 时间衰减**：基于 uid 聚合判定攻击成功，将成功样本入池，在 round 切换时执行衰减。
4. **P3 - Thompson Sampling + 回放 batch 构造 + 混合训练**：实现回放采样、DataProto 构造、defender rollout、batch 合并，完成完整的两阶段混合训练。
5. **P4 - 后验更新 + 剪枝 + metrics + checkpoint**：完善贝叶斯更新、剪枝策略、metrics 日志、档案池持久化。

---

## 五、请在计划中明确给出的内容

对于每一个需要修改的文件，请给出：
1. 文件路径和具体修改位置（行号范围）
2. 修改内容的详细描述（新增函数/类的签名、数据结构定义、逻辑流程）
3. 与其他修改的依赖关系
4. 修改涉及的代码注释标注（遵循 `### dace: <description> ###` 格式）

请 think deeply / ultrathink，充分理解现有代码架构后再制定计划。
