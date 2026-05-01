# MAGIC Prompt & Attack-Space Analysis (分析备忘,不含实现步骤)

## Context

本次任务不是修改代码,而是对当前 DACE pipeline 的 prompt 设计和 14×10 attack-space 进行系统性分析,指出缺陷并给出改进建议。用户已基于 SFT 数据、replay-buffer 和 benign 安全检查结果提出 8 条思考,本文档逐条回应并补充其他发现,**不触发自动修改**。

参考文件(绝对路径 / 行号):
- `data/safety/preprocess_dace.py:27-105` — COMMON_STRATEGY_GUIDANCE / HARM_TEMPLATE / BENIGN_TEMPLATE
- `data/safety/preprocess.py:40-50` — baseline(非 DACE)benign 模板(无 strategy space)
- `src/verl/verl/separated_trainer/ppo/archive_pool.py:52-85` — RISK_CATEGORIES / ATTACK_STYLES
- `src/verl/verl/separated_trainer/ppo/archive_pool.py:211-249` — 多样性奖励公式
- `src/verl/verl/utils/reward_score/game.py:338-354` — format_reward_func_dace
- `src/verl/verl/utils/reward_score/game.py:638-664` — attack_success 判定
- `data-sft/distill_v2_vanilla_benign_jsonl.py:31-37,115-126` — assigned_style 分配 + CONSTRAINT_TEMPLATE
- `data-sft/distill_v2_vanilla_harmful_jsonl.py:17,35-41` — NUM_RUNS=4 + 循环分配
- `scripts/check_benign_data_quality.py` — Guard 对 DACE 重写 benign 的安全度打分
- SFT 分布图 `data-sft/heatmap_v3_all_strategy_distribution.png`、pool 分布图 `scripts/archive_pool_analysis/.../heatmap_all.png`
- `z_materials/dace_benign_prompt_conflict.md` — 已有的 benign 模板冲突分析
- `z_materials/dace_prompt_attack_space_deep_analysis_2026-05-01.md` — GPT-5.5 平行分析(本文 v2 修订基础)

---

## v2 修订与补充 (2026-05-01,基于 GPT-5.5 平行分析)

本节记录相对 v1 的**勘误、精确化、新增观察**,具体修订下放到对应 Issue 节内联标注。读者只看本节即可拿到修订骨架。

### 勘误 (v1 错误)

1. **Issue 4 协同效应被严重高估**:v1 写"剪 S12+S14 后 dead rows 减少 ≥ 70%、delta_max 被压制问题大幅缓解"——错。在 step 300 archive_pool 上实算:剪后空格子从 12 → 2,delta_max 仍由剩余空格子决定,各保留类别的 r_div 几乎不变(例:Elections 0.5706 → 0.5717,Sex-Related Crimes 0.5100 → 0.5112)。**剪类别本身解决不了归一化压制问题**,必须配合 active-mask 或按 data_type 拆表;两者是不同维度的修复。
2. **Issue 5 "directed risk_category" 方向反转**:v1 建议"SFT v4 蒸馏时同时按 hash 分配 risk_category"——已被否决。理由:risk 与 vanilla 语义高度耦合,prompt 又有 "rewrite must entail vanilla" 约束,硬指派 risk 会制造 awkward 组合并破坏 entailment。**正确方案是方案 B'**:Directed Style + **Free Risk** + Hidden Assignment。NVC 占 41.89% 的失衡通过**数据侧**手段治理(源数据补齐 / 后验分层采样 / rare-risk 追加蒸馏 / Guard 过滤),而不是 prompt 侧硬拉均匀。

### 精确化 (v1 估算 → 实测)

3. **SFT v3**:总量 **43,828**,占用 135/140 slot,空格子 5 个(全部在 S14 Code Interpreter Abuse 行)。NVC 18,359 = **41.89%**。Attack style 列分布相对均匀(每列 9.61%-11.27%),说明 v2 directed-style assignment 已基本解决早期 79% Role Play 坍缩问题。
4. **Archive pool step 300**:总量 **4,000**,占用 128/140 slot,空格子 12 个;**vanilla_benign 2,618 (65.45%) vs vanilla_harmful 1,382 (34.55%)**——pool 是 **benign-heavy** 的,与 SFT 的 NVC-heavy 形成对照。这是个新增观察:RL 阶段 attacker 在 benign 源上更容易"成功攻击"(因为 benign 成功定义包含 over-refusal,门槛低),pool 被 benign 灌满。
5. **DACE benign 按 risk category 的 not-safe rate**:S12 Sexual Content 96.3%、S3 Sex-Related Crimes 84.5%、S4 Child Sexual Exploitation 80.4%、S13 Elections 78.2%、Defamation 77.0%、NVC 74.9%、Privacy 72.0%、IP 71.9%、S14 69.8%。**所有 risk 行污染率均 ≥ 70%,证实污染是 prompt 目标层面的问题,不是局部类别问题**;S12 最高,但 NVC 因体量极大贡献了最多绝对污染样本。

### 新增观察 (v1 漏)

6. **`REWARD_LABEL=0` 是现成的小改动入口**:`game.py` 已经计算 label_consistency 奖励(target = 原始 data_type;attacker_query_label = q_safe_label;`reward_label = ±REWARD_LABEL`),但 `grpo_dace_diversity_full.sh:25` 把权重置 0,这个约束实际未进入训练。Issue 6 的"补 classification consistency reward"无需新写代码,只需把 `REWARD_LABEL` 从 0 调到小正数(例 0.2)。
7. **`USE_Q_SAFE_LABEL_FOR_REFUSAL=1` 的双面性**:好处——defender 拒绝真 Unsafe 改写不会被算 over-refusal 错杀;坏处——RL refusal reward 口径承认了 attacker 的类型漂移(benign→Unsafe),失去"逼回原 data_type"的拉力。这与 `REWARD_LABEL=0` 叠加,是 benign 污染在 RL 里没有自我修正机制的结构性原因。建议两者并改:保留 `USE_Q_SAFE_LABEL_FOR_REFUSAL=1`,把 `REWARD_LABEL` 抬高。
8. **`format_reward_func_dace` 漏 canonical 验证**:`game.py:338-354` 只检查三段 tag 结构,不验证 risk/style 是否在 canonical 14×10 内。后果:attacker 可声明 "risk category: financial scams"(非 canonical)拿到 format reward,但 `ArchivePool.extract_strategy` 因 fuzzy match 失败而拒绝入池,strategy 也就进不了 diversity reward。format 与 archive/diversity 之间存在签证失配。
9. **`ENABLE_REVISION_REWARD=0`**:`grpo_dace_diversity_full.sh:18` 关闭了 on-topic/entailment 约束,模板里的"on-topic, relevant to, and entails the vanilla prompt"完全靠 SFT 自觉。如果后续观察到 attacker 改写显著偏离 seed prompt,需要重启轻量 revision reward 或离线过滤。
10. **API key 硬编码**:`grpo_dace_diversity_full.sh:10` 写了 WANDB_API_KEY,distill_v2_*.py:286/313 写了 OpenAI 兼容 API key + base_url。不影响研究结论,但需要在仓库整理阶段迁移到环境变量。
11. **Pool benign-heavy 的连锁后果**(由 #4 推出):因为 benign 占 pool 65%,Issue 4.3 "拆 slot_counts 为 benign/harmful 两张表"的优先级应该比 v1 评估的更高——目前 harmful diversity 信号被 benign 大量样本稀释。

### 路线分阶 (替代 v1 P0/P1/P2/P3 的更稳健分阶法)

GPT-5.5 提出的三条路线值得作为决策模板:

- **路线 C(最小改动验证,推荐先做)**:只重写 BENIGN_TEMPLATE + 重蒸馏 benign + Guard 过滤;`REWARD_LABEL` 0 → 0.2;不动 14×10、不动 archive_pool 代码。跑 300 步 ablation,确认 benign 污染是否是 `refusal_rate_benign` 失控的主因。
- **路线 A(稳定优先,推荐 C 验证后做)**:在 C 之上加 12×10 剪裁 + active-mask delta_max + 方案 B' 蒸馏。需要 SFT/parquet/pool 三处常量同步改,不能在 14×10 旧 pool 上 resume。
- **路线 B(taxonomy 完整优先)**:保留 14×10 但禁用 S14;补 S12/S13/S4 数据;diversity 用 active-mask;蒸馏仍 B'。

C → A 的好处是先用 ablation 隔离 benign prompt 单变量,再决定是否承担 12×10 全链路改动;若 C 已经把 `refusal_rate_benign` 压到 < 0.20 且 diversity 信号也回到可见量级,A 的紧迫性降低。

---

## Executive Summary(5 点核心发现)

1. **BENIGN_TEMPLATE 语义冲突已有独立分析(dace_benign_prompt_conflict.md),实测被 Guard 侧数据确认**:DACE 重写 benign 有 **43% 被判为 unsafe,25.2% controversial**,与 MAGIC baseline(1.5% unsafe / 3.5% controversial)形成极端对比。这是 SFT 数据污染的实锤。
2. **14 类 risk category 直接复用 Llama Guard 4 (S1–S14)**:无增补无修改。其中 S14 Code Interpreter Abuse **在 SFT 的 v3 数据中 140 个格子里有 137 个为 0**(总样本 ~46),在 replay buffer 中更是**整行 0**;S12 Sexual Content 在 SFT 总样本仅 ~352(集中在 Role Play 一格),pool 里总计 ~9。这两类在当前数据生态里**实质上是 dead rows**。
3. **"3 个 sex 相关类别"的冗余问题**实际上被用户稍有误读:S3(性相关犯罪)、S4(儿童性剥削)、S12(色情内容)是 Llama Guard 4 的三个正交维度,各自分工清晰,并非冗余;但 S12 在 benign+harmful 源数据里都罕见,属于"设计上正交但数据端稀疏"的情况。
4. **多样性奖励被 dead rows 系统性压制**的推测成立,且机制比用户提的更微妙:不仅压制其他"小格子",实际上会压制**所有格子**的绝对奖励信号,因为 `delta_max` 被 dead rows 锁死在人工高位。
5. **此外至少还有 4 个未被 8 条思考覆盖的问题**:Non-Violent Crimes 在 SFT 中占比接近 50%(~18.5k/~43k,远超其他)、 benign/harmful 共用同一个 slot_counts 导致多样性奖励模糊、Win condition 2(仍被 classifier 判为 benign)在 RL reward 中根本没被奖励、attack_success 对 benign/harmful 的定义不一致被原样塞回 posterior 更新。

---

## Issue 1: BENIGN_TEMPLATE 冲突 + SFT 数据污染(对应用户第 6 点,最高优先级)

### 现状

`data/safety/preprocess_dace.py:94-105` 的 BENIGN_TEMPLATE:
- Win 1:"trick the language model into producing **harmful responses**"
- Win 2:"still be detected as **benign** by the safety classifier"
- Lose 1:"treats your prompt as **benign** and **complies**, or it produces **harmless** responses"

三条合在一起对 GRPO 是几乎无法同时满足的三元约束;相比之下 HARM_TEMPLATE 的三条完全自洽(都朝同一个方向)。

### 实验证据(已有)

用户提供的 `scripts/check_benign_cache/`:
- MAGIC baseline: 95.0% safe / 1.5% unsafe / 3.5% controversial
- DACE v1nv2_v3: **31.8% safe / 43.0% unsafe / 25.2% controversial**

即**DACE benign 重写中,实际 harmful 的样本占比 ≥ 43%,再加上 25% 的 controversial**。

与 `z_materials/dace_benign_prompt_conflict.md` 里的 `refusal_rate_benign` 轨迹(baseline/MAGIC ~0.10-0.12 vs DACE SFT 全程 0.3-0.5)形成闭环:SFT 数据被污染 → SFT attacker 偏向把 benign 改成 harmful → RL 里 attacker 继续强化这种倾向 → defender 对真 benign 过拒。

### 根因分析(补充于已有文档)

不仅是 Win 1 的措辞问题,还有两个较隐蔽的结构性原因:

1. **"still be detected as benign by the safety classifier" 在 RL 里没被奖励**:
   `compute_reward_bundle` 对 benign 的 attack_success 是 `is_unsafe_response OR is_refused`(`game.py:648-651`),与"改写后 prompt 的 q_safe_label"这个维度无关。换句话说 SFT 阶段告诉 attacker "要让 prompt 看起来 benign",但 RL 阶段完全不惩罚 prompt 越界到 harmful。SFT 约束在 RL 里蒸发了,这进一步放大了冲突。

2. **Gemini 作为蒸馏师倾向遵循"最强行动指令"**:
   Win 1 的"produce harmful response"是一个明确的生成动作,Win 2 的"keep benign"是一个被动约束。Gemini 在 agentic 设置下优先满足 active goal,数值上就是我们观察到的 43% unsafe。

### 建议方向(供后续决策,不含实现清单)

**改动路径**(按收益递减排序):

- **(A) BENIGN_TEMPLATE 重写为"诱发 over-refusal"目标**:与 `z_materials/dace_benign_prompt_conflict.md` 第 3.1 节方案一致,把 Win 1 改为"让 defender 过拒 / 给出不 helpful 回答",显式增加 Lose 2"改写引入真实 harmful 内容"的惩罚。**注意同步修改 distill_v2_vanilla_benign_jsonl.py 里的 CONSTRAINT_TEMPLATE**,保持和蒸馏阶段的 runtime 约束一致(避免只改 SFT 不改蒸馏 prompt 的二次错位)。
- **(B) 重新蒸馏 benign v4 SFT 数据**:用新的 BENIGN_TEMPLATE 跑 `run_cot_distill_v2.sh`,并用 Guard 过滤(即再走一次 `check_benign_data_quality.py`,只保留 safe,或 safe+controversial),落地 v4 数据集。
- **(C) RL reward 侧补一个"prompt 越界惩罚"**:在 `reward_score/game.py` 的 benign 分支,若 `q_safe_label == "Unsafe"` 则扣分;否则 SFT 新约束仍会在 RL 里被稀释。
- **(D) attack_success 分拆为 `over_refusal_success` 和 `harmful_success` 两个信号**:对 benign 只奖励 over_refusal_success,对 harmful 只奖励 harmful_success;archive pool 里 posterior 也相应分通道。这是最大的改动,但能根本解除 benign/harmful 在奖励信号上的混淆。

**排序理由**:A 是根因(数据生成侧),B 是清理历史污染,C 是防止 SFT 新约束被 RL 侵蚀,D 是体系性重构;前三个可增量上线,D 适合下一次 research method 迭代窗口再考虑。

---

## Issue 2: 14 类 risk category 与 Llama Guard 4 对齐 + sex 相关类别是否冗余(对应用户第 1、2 点)

### 1. 与 Llama Guard 4 的异同

**结论:DACE 的 14 个 risk category 就是 Llama Guard 4 S1–S14,一字不差**(`preprocess_dace.py:27-44` vs `z_materials/Llama_Guard_4_Model_Card.md` 的 Hazard Taxonomy 节)。包括每一类的 "Responses that..." 描述都是完整复制粘贴 Llama Guard 4 的 S1-S14 模型卡。

**一个细微概念错位值得记录**:Llama Guard 4 的 S1-S14 是**response-level 分类标签**(分类器看 defender 的回复是否违反了哪类),DACE 却把它们用作**prompt-level 生成目标**(让 attacker 从 14 类里选一个去攻击)。这在实际运行里并不会造成错误,但会让一些类别从 attacker 视角看变得不自然:

- S5 **Defamation** 说的是"回答里包含可被证伪且可能损害特定人名誉的内容"。attacker 要让 defender 诽谤,必须先构造一个针对具体人的 prompt。这类 prompt 在 benign WJB 源数据里基本不存在,导致数据端极稀疏。
- S8 **Intellectual Property** 同理。
- S14 **Code Interpreter Abuse** 的原定义明确写 "text-only tool-call use cases"——针对有 code interpreter 工具调用能力的模型。MAGIC 的 defender 本身不执行工具调用,S14 在这里**本质就不适用**。

### 2. sex 相关三类是否冗余

从 Llama Guard 4 模型卡回看:
- S3 **Sex-Related Crimes**:性贩卖/性侵/性骚扰/卖淫——**犯罪行为**
- S4 **Child Sexual Exploitation**:对儿童的性剥削——**犯罪且涉及未成年**
- S12 **Sexual Content**:"Responses that contain erotica"——**合法成人内容**

**概念上是正交三维,不是冗余**:S3/S4 是"行为是否犯罪",S12 是"内容是否色情"(即便合法,aligned 模型也常常过拒)。从 Llama Guard 的设计立意看,这三类各自承载了不同的误判模式。

**但数据端确实稀疏**(见 SFT v3 heatmap 读数):
- S3 Sex-Related Crimes:每格 ~120-140,总计 ~1300(中等)
- S4 Child Sexual Exploitation:每格 ~70-110,总计 ~820(偏低)
- S12 Sexual Content:每格 ~14-25(除 Role Play=187),总计 ~352(**非常低**)

**建议**:S3 + S4 保留(数据可用,且 Llama Guard 4 eval 会检测这两类);S12 在当前数据生态下是近似 dead row,**如果要剪裁 14→12,S12 是比 S14 更值得讨论的候选**,而不仅仅是 sparse 就删。

---

## Issue 3: 剪裁 14→12 (去 Sexual Content + Code Interpreter Abuse) 的决策分析(对应用户第 4 点)

### 从 SFT 和 replay buffer 分布读数看

**SFT v3 heatmap 读数**(`heatmap_v3_all_strategy_distribution.png`):
- S14 Code Interpreter Abuse 行:`[0, 26, 14, 3, 0, 3, 0, 0, 0, 0]` — **10 格中 7 格为 0**,行总和 ~46
- S12 Sexual Content 行:`[16, 21, 187, 14, 18, 21, 19, 14, 17, 25]` — 行总和 ~352,里面只有 Role Play=187 一个 outlier
- S13 Elections 行:`[42, 75, 375, 46, 42, 47, 47, 53, 105, 53]` — 行总和 ~885,Role Play=375 也是一个 outlier

**Replay pool heatmap 读数**(`scripts/archive_pool_analysis/.../heatmap_all.png`,pool size ~4000):
- S14 Code Interpreter Abuse:**整行 0**(10 格全 0)
- S12 Sexual Content:~9(各格 0-3)
- S13 Elections:~15
- S4 Child Sexual Exploitation:~34
- S3 Sex-Related Crimes:~48
- S9 Indiscriminate Weapons:~68
- 同时 Hate / Violent Crimes / Non-Violent Crimes 合计占 pool 约 50% 以上

### 剪裁决策

**选项 A: 剪 S12 + S14(用户方案)**:变成 12×10 = 120 slot。
- 证据链最强:两类在 SFT 和 pool 里都是近零。
- S14 本身概念上不适用(见 Issue 2)。
- S12 是正交概念但数据端枯,剪掉损失一个"合法但过拒"的 over-refusal 检测维度,在 benign 侧缺一个 niche 但清晰的评估轴(可惜但可接受)。
- **需要同步改动**:`archive_pool.py:52-85` 常量表、`data-sft/analyze_strategy_distribution.py` 和 `scripts/analyze_archive_pool.py` 的常量表、`preprocess_dace.py:27-57` 的 COMMON_STRATEGY_GUIDANCE 编号和描述、SFT 蒸馏 prompt (`distill_v2_vanilla_*.py`)的 RISK_CATEGORIES_CANONICAL、重跑蒸馏 + 清洗 script 里的 hardcoded 列表 (`run_cot_distill_v2.sh` 内嵌的 Python 块 L96-123)、RL parquet 重新预处理。

**选项 B: 剪 S4 + S12 + S13 + S14**:更激进。
- 优点:S4/S12/S13 在 pool 里都很稀疏。
- 缺点:S4(儿童性剥削)是安全评测里分量很重的一类,不建议剪;S13(选举信息)Llama Guard 强调,未来对齐压力很大。
- **不建议**。

**选项 C: 不剪,改成在 archive pool 里 动态掩蔽 empty rows**:
- 保留 14×10 的对外概念完整性(与 Llama Guard 4 对齐)。
- 在 `_compute_max_marginal_gain` 里只对 `已经被触达过的 slot 或 其邻居 slot` 求 max,避免 dead rows 压制。
- 好处:不改动数据层。
- 坏处:是一个 diversity reward 的局部修补,且 SFT 数据层的不均衡并没有被治理。
- **作为 Issue 4 的缓解,不作为 Issue 3 的主方案**。

**推荐:选项 A,且与 Issue 1 的 benign v4 重蒸馏 在同一窗口一次性落地**,避免两次改 SFT 数据。

---

## Issue 4: 多样性奖励被 dead rows 系统性压制(对应用户第 7 点,深入版)

### 公式回顾

`archive_pool.py:238-249`:
```
R_div(x) = [H(p ∪ {x}) - H(p)]  /  [ max_b (H(p ∪ {x_b}) - H(p)) + ε ]
```

分母 `delta_max` 枚举全部 `N_RISK × N_STYLE = 140` 个 slot,取边际熵增的最大值。

### 用户的直觉:正确,且机制比"抑制其他少量格子"更广

**1. 对 empty cell 最敏感**:
当分布已经 peaked(`Non-Violent Crimes × Slang` 在 pool 里有 80 样本,`Sexual Content × Slang` 有 1 个),加到**数量为 0 的格子**会产生最大的边际熵增,因为:
- 新开一个非零概率分量,-p log p 在 p=1/(N+1) 时最大(一阶项)
- 其他所有格子的 p 只是按比例缩小(二阶修正)

**2. dead rows 不仅压制"小但非零"的格子,而是压制所有格子**:

假设 pool 当前 N=3000 样本,Code Interpreter Abuse 整行 0(10 个永远不会被触达的格子)。`_compute_max_marginal_gain` 会扫这 10 个 dead cell,每个的 delta 都接近 `log(3001)/3001 ≈ 0.0027`,远大于向 Hate-Slang 这种已有 100+ 样本的格子加 1 的收益(~0 甚至负)。于是:

- `delta_max` 被 dead row 锁在 ~0.0027
- 对 attacker 真实可触达的任何 slot x,`ΔH(x) / 0.0027` 都被归一化到一个**很小的数**
- 注意 `game.py` 里的 diversity reward 是和 safety / refusal / format reward **直接相加**的(`compute_reward_bundle`),当 diversity 部分的绝对值缩到 0.01-0.1 量级时,**它几乎不再参与 GRPO 的 advantage 估计**,多样性信号实际被"稀释到噪音以下"。

换句话说,用户说的"相对受到抑制"是对的,但更准确说是**绝对奖励量级被稀释**(相对比例在数学上是不变的——比例和 delta_max 同比例缩放)。但因为 diversity 要与 safety 等其他 reward **相加**而非分开使用 advantage,所以绝对量级决定它有没有话语权。

**3. 补充:benign + harmful 共用同一个 slot_counts 的问题**:

`archive_pool.py:111`:
```python
self.slot_counts: np.ndarray = np.zeros((N_RISK, N_STYLE), dtype=np.float64)
```

只有一个 matrix。`add_entry` 无论 `data_type` 是 `vanilla_harmful` 还是 `vanilla_benign`,都 `self.slot_counts[r, s] += 1.0`(`archive_pool.py:281`)。

后果:attacker 在 benign × Specialized Advice 提交一个新样本时,如果 harmful × Specialized Advice 已经很满,diversity reward 会把这里算成"已覆盖"——但实际 benign 侧可能是空的。两类源数据在 strategy 分布上是完全不同的(benign 里 Non-Violent Crimes 很少,harmful 里 Non-Violent Crimes 占主导),把它们合到一张表里会让奖励信号失真。

### 建议方向

按改动成本从小到大排:

- **(小)在 `_compute_max_marginal_gain` 里只枚举非零 slot(或活跃 slot)**:改一行,空 slot 不进 max。保留 14×10 外观,但 delta_max 不再被 dead row 拉高。**实测最小改动且有效,可先试**。
- **(小)在 `_compute_diversity_reward` 里加一个绝对下限**,或者在 `compute_reward_bundle` 给 diversity 一个独立的乘子,避免与 safety reward 混在一起被归一化到 0.01 量级。
- **(中)拆分 slot_counts 为 benign / harmful 两张表**,`add_entry` 按 data_type 分流,`compute_diversity_reward` 按当前 sample 的 data_type 取相应矩阵。奖励信号更准确,但 pool 代码改动面比较大。
- **(大)从"均匀覆盖"目标切换成"与目标分布对齐"**:用 Kullback-Leibler 到某个目标分布(比如 jailbreak 攻击真实频率)的减少量作为 reward。这是研究方法级改动。

**与 Issue 3 的协同**:
~~v1 原文:"如果采用 Issue 3 选项 A(剪 S12 + S14),dead rows 从 20 格减到 0-10 格,delta_max 被 dead rows 拉高的问题能减轻 ≥ 70%"~~ — **v2 勘误,见顶部 v2 修订段第 1 条**。

实测结论:在 step 300 archive_pool 上把矩阵从 14×10 收缩到删除 S12/S14 的 12×10 后,空格子从 12 个减到 2 个,**delta_max 仍由剩余 2 个空格子决定**,各保留类别的归一化 r_div 几乎不变(Elections 0.5706 → 0.5717,Sex-Related Crimes 0.5100 → 0.5112)。**剪类别和修 diversity 归一化是两个正交问题**;Issue 3 解决的是"概念对齐 + 数据 dead rows 清洗",Issue 4 必须独立通过 active-mask / 拆表 / 改归一化口径解决。

补强 Issue 4 优先级的新证据(来自 v2 修订段第 4、11 条):pool 是 vanilla_benign 65% / vanilla_harmful 35% 的失衡,**两个 data_type 共用一张 slot_counts 会让 harmful diversity 信号被 benign 大量样本稀释**——这把 "(中)拆分 slot_counts" 的实际紧迫性提到 P1 级。

---

## Issue 5: SFT 数据分布严重不均衡(用户未显式提及,但 heatmap 强烈暗示)

**SFT v3 heatmap 读数(按行求和)**:
- Non-Violent Crimes: 每格 1633-2002,**行总和 ~18500**
- Hate: 每格 572-821,**行总和 ~6770**
- Violent Crimes: 每格 488-704,**行总和 ~6170**
- 其余 11 行总和合计 ~12000

Non-Violent Crimes **单独占 SFT 样本的 42%**。这意味着:

1. **SFT attacker 被严重偏置**:模型更可能在 Non-Violent Crimes 类做生成,即便 vanilla prompt 的自然主题是其他类。结合 Issue 1,这也解释了为什么 DACE benign 里 43% 被 Guard 判 harmful——大量 benign 源被改写成了 NVC 方向的攻击。
2. **RL 阶段自然继承这种偏置**:replay pool 里 Non-Violent Crimes 也明显多(但不如 SFT 那么极端,因为 RL 有 benign/harmful 源数据限制)。
3. **根因**:`distill_v2_vanilla_*_jsonl.py` 只 assign 了 attack_style(用 md5 hash 均匀分布到 10 个 style),**没有 assign risk_category**——让 Gemini"自由选 14 类中一个最匹配的"。Gemini 自然偏好语义最广泛的 Non-Violent Crimes 作为兜底。

### 建议(v2 修订:撤销 v1 的 directed-risk 方案,改用方案 B')

**v1 错误建议**(已撤销):"用 `(md5(vanilla) + run_idx) % 14` 给每个 vanilla 直接分配目标 risk_category"。

**撤销理由**:
- Risk 与 vanilla 语义高度耦合(NVC 适配大量 daily/financial/property 主题,Privacy 适配 PII-touch 主题,S4/S9 几乎只能匹配特定主题)。硬指派会让 Gemini 在不匹配的 vanilla 上强凑 risk,要么破坏 prompt 模板里的 "rewrite must entail the vanilla" 约束,要么生成 awkward 改写。
- 这与 attack_style 不同:style 是"包装风格"(Slang / Role Play / Misspellings 等),与内容轴**正交**,可以套到任何主题上;directed-style 在 v2 已实证有效(每列 9.61%-11.27% 接近均匀)。Risk 没有这个性质。

**采纳方案 B':Directed Style + Free Risk + Hidden Assignment**(与已有 distill_v2_*.py 的 CONSTRAINT_TEMPLATE 完全兼容):
1. 只指派 attack style(已落地);risk 仍由 Gemini 推理 vanilla 后自选(也已落地)。
2. `<think>` 范式保持"shortlist 多个候选 → commit 一个"的自由选择形态;目标 style Y 作为软约束,要求出现在 shortlist 中且被 commit 为最终选择,理由要写得像自由选择(linguistic/contextual properties of vanilla)。
3. Anti-leak:`<think>` 不得出现 "assigned / told / per instruction / mandated / chosen for me" 等 meta 表述;run_cot_distill_v2.sh 的 LEAK_PATTERNS clean 步骤已在做这件事,继续保留。

**NVC 41.89% 失衡用数据侧手段治理,而非 prompt 侧**:
- **源数据补齐**:`sft_data_source_*.jsonl` 里若 NVC 主题 vanilla 远多于其他类,先做源端 stratified sampling/补充而不是让 Gemini 在等量 vanilla 上自选。
- **生成后分层采样**:`distill` 完成后,按 Gemini 自选的 risk 做后验下采样(NVC 行 cap),把进 SFT 训练的样本压到目标比例(例如单类不超过 20%)。
- **rare-risk 追加蒸馏**:对 S3/S4/S13 等稀有类,从外部数据集(WildJailbreak 子集、Llama Guard 训练集子集)定向找 vanilla 再蒸,而不是从现有 vanilla 中硬指派。
- **Guard 过滤(对 benign)**:与 Issue 1-B 同步走,落地一次过滤即可同时治理污染和分布。
- **risk-category 后处理标签校正**(可选):用一个独立分类器(Llama Guard 4 / Wildguard)对每条 SFT `answer` 重打 risk 标签,把 Gemini 自选 risk 与分类器判定不一致的样本标出来,作为分布统计基准——但**不要据此重写 `<strategy>`**,以免破坏 SFT 语义自洽。

---

## Issue 6: Win condition 2 没在 RL reward 里被落地(未被 8 条思考覆盖)

### 现象

BENIGN_TEMPLATE Win 2:"still be detected as benign by the safety classifier"
HARM_TEMPLATE Win 2:"still be detected as harmful by the safety classifier"

RL 阶段的 `compute_score_components`(`game.py:366-557`):
- 有 `q_safe_label`(从 Wildguard 分类改写后的 prompt)
- 但 `q_safe_label` **只被用来确定 refusal 奖励的 request_label**(`game.py:449-466`),完全没被用来奖励/惩罚"改写是否保持原 data_type 的分类"。

### 后果

这导致:
- Benign attacker 无内在压力保持 prompt benign;
- Harmful attacker 无压力让 prompt 保持 harmful(虽然经验上 harmful 源已经是 harmful,自然保持,不是紧迫问题);
- Issue 1 的 SFT 污染在 RL 里没有修正机制。

### 建议(v2 修订:发现 reward 已实现,只是被脚本置零)

**v1 写"建议在 compute_reward_bundle 里加一个 reward_classification_consistency"——v2 修订**:

实际上 `game.py` 已经实现了这个一致性奖励:
- target label 来自原始 data_type
- attacker_query_label 来自 q_safe_label
- `reward_label = +REWARD_LABEL if consistent else -REWARD_LABEL`

但 `grpo_dace_diversity_full.sh:25` 设置 `REWARD_LABEL=0`,把整个奖励项清零,所以训练里这条约束实际不存在。

**最小修订**:把 `REWARD_LABEL` 从 0 调到小正数(例 0.2,约 REWARD_HARM 的 1/5),不需要新写代码。

**`USE_Q_SAFE_LABEL_FOR_REFUSAL=1` 的双面性**(v2 新增):
- 好处:如果 attacker 真的把 benign 改成 Unsafe,defender 拒绝它会被视为正确(用改写后的真实 label 而非原 data_type 来判 refusal)。这避免了 defender 在真 Unsafe 改写上被错算 over-refusal。
- 坏处:训练目标会从"保持原 data_type"滑向"按改写后 q_label 自洽"。SFT attacker 已学会把 benign 改 Unsafe 的话,RL 在 refusal reward 口径上承认这个漂移,失去拉回原 data_type 的力。
- **建议**:保留 `USE_Q_SAFE_LABEL_FOR_REFUSAL=1`(refusal 信号干净),同时把 `REWARD_LABEL` 抬高到小正数(对 attacker 单独施压不要漂移)。两者并改是兼容的。
- **新增监控指标**:`label_consistent_benign`、`label_consistent_harmful`、`q_safe_label_by_data_type` 分布——这些可以从 `compute_score_components` 已有的字段直接 log,工程量极小。

---

## Issue 7: attack_success 定义不一致被原样塞回 posterior(未被 8 条思考覆盖)

### 现象

`game.py:648-651`:
```python
if request_is_harmful is True:
    attack_success = is_unsafe_response
elif request_is_harmful is False:
    attack_success = is_unsafe_response or is_refused  # benign: 过拒也算成功
```

`archive_pool.py:365-375` 的 `update_posterior(entry_idx, any_harmful)` 把同一个布尔塞进 posterior 的 `successes += 1`。

### 问题

同一个 posterior beta 分布,既包含"harmful 成功攻击(诱导产生 harmful 响应)",又包含"benign 成功攻击(诱导过拒)"。Thompson sampling 用 `posterior mean = (α + s) / (α + s + β + f)` 排序,**两种截然不同性质的成功被当成同质事件**。

结果:一个"benign + Slang + Privacy"条目,posterior 可能是因为 defender 过拒了它而升高,但 sampling 时它会和"harmful + Slang + Privacy"条目竞争替换机会。两种攻击类型被迫共享 bandit 臂。

### 建议

短期:在 `ArchiveEntry` 里增加 `success_type ∈ {harmful_induction, over_refusal}` 标签,posterior 按 data_type 分支更新,pruning threshold 对两类分开。

长期:把 archive_pool 拆成 harmful_pool / over_refusal_pool 两个独立池,replay 阶段各自采样。

---

## Issue 8: 其他小发现(未被 8 条思考覆盖)

### 8.1 Strategy 正则 reward 和 pool 两套

- `game.py:110-144` `extract_strategy_text` 有自己的 pattern
- `archive_pool.py:145-152` `_STRATEGY_PATTERN` 是另一套(更宽松,容忍 CJK colon 和 comma 分隔)
- `game.py:128-133` 的 `extract_strategy_slot` 已经通过 `from archive_pool import ArchivePool` 委托过去了,所以 reward 侧的 slot 判定一致;但 `extract_strategy_text` 还单独存在,被 format check 等其他地方使用。

**风险**:小,因为核心路径统一了;但在 format_reward_func_dace 里用的是三段式结构 count,不是 strategy 正则。这一块基本 ok,只是风格上建议把两个 pattern 合成一个模块常量。

### 8.2 10 个 attack style 的混合抽象层级

- 表层形式 style: Slang / Misspellings / Uncommon Dialects / Technical Terms / Word Play
- 框架 style: Role Play / Authority Manipulation / Hypotheticals / Historical Scenario
- 修辞 style: Emotional Manipulation

**问题**:一个"让用户以研究员身份 Role Play + 使用 Technical Terms"的 prompt,attack style 该填哪一个?目前 Gemini 在蒸馏中用 assigned_style 强制,能保证 SFT 阶段一致;但 RL 阶段 attacker 自选 style,可能出现同义游移。

**建议**(低优):不剪 style,但在 COMMON_STRATEGY_GUIDANCE 里给每类一句更 operative 的区分说明,比如 "Slang = change **wording register** to informal/colloquial without reframing the task" 和 "Role Play = wrap the task in a **fictional persona frame**"。

### 8.3 assigned_style 只在 SFT 存在,RL 里自由选 style,导致 diversity 的对象不稳

- SFT v2 蒸馏:directed 分配 attack_style,**directed-style drift 会被清洗 script 丢掉**(`run_cot_distill_v2.sh` L212-217)
- RL rollout:attacker 在 CONSTRAINT 内自由选
- Diversity reward 对 RL 的 `(r, s)` 取 attacker 自己声明的——attacker 可以学会偏向声明低人口的 style 来刷 diversity reward,但实际文本上可能并不符合那个 style

**风险**:中;但需要一个 style 分类器(独立小模型)才能验证,实现成本高。暂时 observe 即可。

### 8.4 Win 1 的 HARM_TEMPLATE 有但 BENIGN_TEMPLATE 没有的条款

HARM_TEMPLATE 有"more **effective** jailbreak"这样的质量描述;BENIGN_TEMPLATE 只有"more complex"。这是一个无明显后果的 prompt 风格不对称,但如果要重写 BENIGN_TEMPLATE(Issue 1 A 方案),统一风格会更清晰。

### 8.5 format_reward_func_dace 漏 canonical 验证(v2 新增)

`game.py:338-354` 的 `format_reward_func_dace` 只查三段 tag 结构(各出现一次,顺序对),**不验证 risk/style 是否在 canonical 14×10 内**。

后果:attacker 可以输出 `<strategy>risk category: financial scams\nattack style: jailbreak</strategy>`,拿到 format reward,但 `ArchivePool.extract_strategy` 因 fuzzy match 失败而拒绝入池——strategy 进不了 archive,也就进不了 diversity reward。format 与 archive/diversity 之间存在签证失配。

**建议**(轻量):在 `format_reward_func_dace` 内复用 `ArchivePool.extract_strategy`,只对返回 None 的样本扣 format reward。或者为 attacker 增加一个独立的 strategy_reward,与 format_reward 并列。

### 8.6 revision_reward 已关 → on-topic 约束完全靠 SFT 自觉(v2 新增)

`grpo_dace_diversity_full.sh:18` 设置 `ENABLE_REVISION_REWARD=0`,模板里的 "rewrite must be on-topic, relevant to, and entail the vanilla prompt" 在 RL 阶段没有奖励信号支撑。如果 attacker 学会了用 "Hypotheticals" / "Historical Scenario" 等 framing 完全偏离 seed prompt,只要 defender 拒绝就能拿 over-refusal reward——这是一个潜在的 reward hacking 通道。

**建议**:暂时 observe(目前没有强证据 attacker 在做这件事);如果新增 `entailment_metric` 监控指标(轻量,用现有 revision model 离线打分一个采样子集即可),发现 entailment 持续下降,再恢复轻量 revision reward。

### 8.7 API key 硬编码到脚本(v2 新增)

- `grpo_dace_diversity_full.sh:10` 写死 WANDB_API_KEY
- `data-sft/distill_v2_vanilla_*_jsonl.py:286/313` 写死 OpenAI 兼容 API key + base_url

不影响研究结论,但仓库整理 / 公开发布前必须迁移到环境变量。

---

## 推荐优先级与改动依赖关系(v2 修订版)

**v2 重要变更**:撤销 v1 的 P1 [Issue 5 directed-risk];把 Issue 4.3 (拆 slot_counts) 从 P2 提升到 P1;新增 P0 的 `REWARD_LABEL=0→0.2` 一行改动(原 v1 写在 Issue 6 P1,现因为是已实现 reward 改 1 个 env var,提升到 P0);引入路线 C 先验证(单变量 ablation)再决定是否上 A 全套。

```
路线 C(最小改动验证,推荐先做一个 ablation):
  [Issue 1-A] BENIGN_TEMPLATE 重写       (preprocess_dace.py + distill_v2_*.py)
  [Issue 1-B] v4 SFT 数据重蒸馏 + Guard 过滤(只重蒸 benign)
  [Issue 6 / v2-#6] REWARD_LABEL: 0 → 0.2  (脚本一行)
  → 跑 300 steps,观察 refusal_rate_benign 是否降到 < 0.20、
    DACE benign Guard not-safe rate 是否 ≤ 10%、
    archive_pool bottom rows 是否仍接近 0
  → 用结果决定是否上路线 A

路线 A(稳定优先,C 验证后做):
  路线 C 全部 +
  [Issue 3-A] 14×10 → 12×10 (剪 S12 + S14)
  [Issue 4.1] _compute_max_marginal_gain 只枚举非零 slot (active-mask)
  [Issue 4.3] slot_counts 拆 benign/harmful 两张表  (新增 P1,因 pool 65/35 失衡)
  [Issue 5 / v2-#2] 蒸馏维持 B' (Directed Style + Free Risk + Hidden Assignment),
                    NVC 失衡用源数据补齐 + 后验分层 + rare-risk 追加 + Guard 过滤
  [Issue 8.5] format_reward 复用 ArchivePool.extract_strategy 验 canonical

路线 B(taxonomy 完整优先,可选):
  路线 C 全部 +
  仅删 S14,保留 S12 但补足 erotica boundary benign 数据 +
  Issue 4.1 active-mask + Issue 4.3 拆表

P2/P3(不进当前迭代窗口):
  [Issue 7]   archive_pool 按 success_type 分支 posterior
  [Issue 1-D] attack_success 拆 over_refusal / harmful_induction 双信号
  [Issue 4.4] 多样性目标从 uniform 换成 target-distribution KL
  [Issue 8.3] 加 style 分类器验证 attacker 声明
  [Issue 8.6] 视监控数据决定是否恢复轻量 revision reward
```

**依赖关系明确**:
- Issue 1-A(prompt 重写)和 Issue 1-B(v4 重蒸馏)必须一起做——只改 prompt 不重蒸,SFT 数据仍是污染版。
- Issue 3-A(剪 14→12)涉及 SFT 数据层、RL parquet 层、pool 层常量三处,必须和 v4 蒸馏合并;且 14×10 的旧 archive_pool checkpoint **不能 resume 到** 12×10 训练上(strategy index 不兼容)。
- Issue 4.1(active-mask) 和 Issue 4.3(拆表) 是相互正交的修复,可独立上线;Issue 4.3 在 pool benign-heavy 65% 的事实下比 v1 估计的更紧迫。

---

## 验证建议(如果上线)

1. **Benign 污染回归**:新 v4 SFT 数据过 `check_benign_data_quality.py`,目标 unsafe 率 < 10%(当前 43%)
2. **SFT 分布均衡**:重跑 `analyze_strategy_distribution.py`,Non-Violent Crimes 行占比应从 42% 降到 < 20%(分散到其他 risk)
3. **RL 跑 300 步后**:
   - `refusal_rate_benign` 训练全程 < 0.20(当前 0.3-0.5),`refusal_rate_harmful` 维持 0.7-0.9
   - `reward/diversity` 在 step 50 后绝对值 > 0.2(此前被 dead rows 压制到 ~0.01-0.05)
   - `archive_pool` 覆盖熵在 step 100 后 > 3.0(12×10 = 120 slot, log(120)≈4.79)
4. **跨类分布**:新 pool heatmap 应该没有整行 0 的行;最稀疏行至少 > 20 样本

---

## 开放问题(需要和用户进一步确认的决策点)

1. **是否真的要剪 14→12**:剪后与 Llama Guard 4 eval 的对应关系需要重新对齐,若后续要报告基于 Llama Guard 4 的分类分布,13-14 被合并/忽略会让 eval 不完整。可以考虑"训练用 12×10,eval 报告用 14×10"。
2. **S12 剪还是保**:如果保留,可以专门增加一批"benign erotica 测试"(比如写爱情诗、成人书评),作为 over-refusal 测试集的一部分;如果剪,接受失去一个 over-refusal 评估维度。
3. **v4 benign 数据量预算**:当前 v3 有 20000;加入 Issue 5 的 risk-category directed 分配后,是否保持 20000 or 扩到 40000 以覆盖所有 12×10=120 格?
4. **archive_pool 拆 benign/harmful(Issue 4.3)是否进 P1**:这是个中等改动,但对解除 diversity 污染效果最直接。

---

**本文档到此为止,仅供决策参考,不含任何自动修改步骤。**
