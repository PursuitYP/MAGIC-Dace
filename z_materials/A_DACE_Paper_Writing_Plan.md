# DACE 论文写作计划（NeurIPS 2026）

## Context

### 任务背景
用户要基于已有研究方法（`研究方法v3.1.md`）、伪代码（`pseudocode_v3.1.html`）、实现细节（`dace_coding_v3.1.md` + `dace_coding_debug_v4.md`）、以及大量调研/分析材料，撰写 NeurIPS 2026 投稿论文 **DACE**。论文核心贡献：在 MAGIC 攻防协同框架基础上，引入 (1) 显式的二维攻击策略空间、(2) 归一化边际覆盖增益多样性奖励、(3) 基于 Beta-Bernoulli 后验 + 时间衰减 + Thompson Sampling 的贝叶斯对抗回放池，同时解决**攻击策略坍缩**（Attack Strategy Collapse）与**防御对抗遗忘**（Defense Adversarial Forgetting）两大协同演化痛点。

### 为什么现在做这件事
- 研究方法 v3.1 稳定；v4 全流水线（含 12×10 剪裁 + BENIGN_TEMPLATE 修复）已完成实现规划；下一步进入 PhD 级论文投稿写作阶段
- 已有 Opus / GPT-5.5 对 Intro / Evaluation / 其他章节的独立分析可参考，但需综合独立重写
- 用户已做 4 个写作风格决策：
  - **标题**：`DACE: Diversity-Driven Adversarial Co-Evolution for Robust LLM Safety Alignment`（并保留其他候选作为注释形式写入 LaTeX 供后续选择）
  - **Related Work**：正文保留极简版（约 0.5 页），完整版放附录
  - **Pseudocode**：正文放高度简化的算法框；完整多页版本放附录
  - **Tables**：先建表头 + 结构，数据用占位符

### 目标
完成可投稿的 DACE LaTeX 源码（`z_materials/DACE_NeurIPS_2026/neurips_2026.tex` + 分章节 .tex 文件），主文 9 页以内，附录无上限。每个英文段落上方用中文注释说明逻辑、上下文关系与中文对应内容；引用先用论文短名占位。

### 参考策略（关键原则）

**写作时主要基于本 plan 文件为准**——本 plan 已经整合了主对话的独立分析、opus/gpt 的精华观点、subagent 扩展调研，以及用户的关键修正（TriPlay-RL 批判维度、SSP replay 的三维度局限等）。本 plan 中的决策和框架应作为写作的**单一事实来源**（single source of truth）。

**当遇到具体章节细节需要展开时，可参考以下两份分析作为补充资料**（它们在某些细节上更详细具体，但可能存在事实错误，使用时以 plan 为准）：

- **Opus 系列分析**（全面、结构化）：
  - `z_materials/DACE Introduction 分析-opus.md`（Intro 4 段 + 3 贡献 bullet 的具体措辞建议）
  - `z_materials/DACE Evaluation 分析-opus.md`（9 benchmark × 3 backbone 表头、RQ 驱动细节）
  - `z_materials/DACE title abstract method conclusion related-work appendix 分析-opus.md`（Method 小节公式铺陈、Appendix 分区）

- **GPT-5.5 系列分析**（叙事更紧凑）：
  - `z_materials/DACE Introduction 分析-gpt.md`
  - `z_materials/DACE Evaluation 分析-gpt.md`
  - `z_materials/DACE title abstract method conclusion related-work appendix 分析-gpt.md`

**使用原则**：
1. 写某一段/小节时，先按本 plan 的结构指导完成骨架
2. 如需补充表述细节、具体例句、或细节格式，可查阅对应的 opus / gpt 分析作为风格参考
3. 两者若有冲突，以**本 plan 为准**（尤其是 SSP replay 分析、TriPlay-RL 定位这两处已经修正的内容）
4. 综合参考而非照抄——所有英文段落必须基于我们独立分析 + plan 结构重新撰写，并确保中文注释完整

---

## 一、整体 DACE 论文写作框架

### 1.1 论文核心叙事线

DACE 的论文故事必须围绕一条**单一主线**展开，避免"MAGIC + 多样性 + 回放"的分散感：

> **协同演化范式已被证明能让安全对齐追上演化攻击（MAGIC / Self-RedTeam），但现有协同演化框架仅保证攻击者和防御者"都在进步"，无法保证攻击覆盖广度和防御记忆持久度。当攻击者陷入策略坍缩时，防御者只在狭窄分布上被训练；当防御者对抗遗忘时，过去的安全能力持续退化。DACE 通过 (1) 显式 12×10 策略空间引导 + 归一化覆盖增益奖励使攻击探索结构化、(2) 贝叶斯后验回放池使防御记忆连续跟踪，使协同演化从"交替进步"升级为"全面且持久"。**

### 1.2 与 MAGIC 的差异化定位（避免被视为增量）

| 维度 | MAGIC | DACE |
|---|---|---|
| 攻击空间 | 隐式（策略涌现） | 显式 12×10（Llama-Guard-4 12类 × Rainbow Teaming 10风格） |
| 多样性信号 | RL 涌现 | 归一化边际覆盖增益 + λ 差异化激励 |
| 防御训练数据 | 仅当前攻击者 | 新攻击 + Bayesian Thompson 回放混合 batch |
| 回放风险估计 | 不涉及 | Beta-Bernoulli 后验 + 时间衰减 + Thompson Sampling |
| 策略输出 | 自由改写 | 显式三段输出 `<think><strategy><answer>` |

**关键表述**：DACE 继承 MAGIC 的 SPNE 安全保证（由非对称序贯博弈结构决定），并在其上增加 coverage 和 memory 两重机制。叙事基调应为"下一步"而非"增强版"。

### 1.3 主文 9 页篇幅分配（预估）

| 章节 | 页数 | 要点 |
|---|---:|---|
| Title + Abstract | 0.4 | 8 句摘要公式 |
| §1 Introduction | 1.5 | 4 段叙事 + 3 贡献 bullet |
| §2 Related Work（极简版） | 0.5 | 3 段落：攻击演化 / 协同演化 / 多样性 |
| §3 Preliminaries & Problem Formalization | 0.6 | 继承 MAGIC 博弈 + 两大病态形式化 |
| §4 Method | 3.2 | 4 子节 + 简版算法框 |
| §5 Experiments | 2.4 | RQ 驱动，3-5 表 + 2-3 图 |
| §6 Conclusion | 0.3 | 3 段落 |
| **合计** | ~9 页 | |

附录约 12-15 页：算法完整版、策略空间设计理由、prompts、训练细节、扩展结果、训练动态、攻击模式分析、Related Work 完整版。

---

## 二、章节写作详细计划

### §0 Title / Abstract

**目标**：标题明确定位，摘要 8 句完成"big picture → gap → DACE 提案 → 两核心组件 → 实验亮点 → 代码释出"。

**Title 区块**（在 `neurips_2026.tex` 中）：
- 主标题用 `Diversity-Driven Adversarial Co-Evolution` 版本
- 将其他 2 个候选作为 LaTeX 注释紧接写在主 `\title{}` 上方，供用户后续选择
- 英文标题对应的中文注释：`% 主标题 / 副候选 1 / 副候选 2，保留多样性便于最终选择`

**Abstract 8 句公式**（每句目标 20-30 词）：
1. Big picture: LLM 对齐落后于演化攻击
2. Gap1: 协同演化解决"追不上"但存在策略坍缩
3. Gap2: 同时存在对抗遗忘
4. 提案 DACE 一行定义（diversity + memory）
5. 组件 1: 12×10 策略空间 + 归一化覆盖增益
6. 组件 2: Beta-Bernoulli 后验回放
7. 实验结果一句话（留待补充具体数字）
8. 代码释出 + 呼吁

### §1 Introduction（1.5 页，4 段 + 3 贡献 bullet）

#### 段落结构

**段 1：Hook — LLM 安全对齐面临"持续演化"挑战**
- 中文注释逻辑：以攻击演化（静态模板 → 自动化 → 组合多步 → agentic）开篇，类似 MAGIC 但不重复
- 关键 citations（占位）：`[shen2024anything]` (DAN), `[zou2023universal]` (GCG), `[chao2023pair]` (PAIR), `[liu2024autodan]` (AutoDAN), `[samvelyan2024rainbow]` (Rainbow), `[rahman2025xteaming]` (X-Teaming), `[majic2026]` (MAJIC)
- 结尾转折：静态对齐方法依赖预收集分布，无法应对这种动态威胁

**段 2：协同演化范式已证明可行，但存在"双病态"**
- 介绍 Self-RedTeam / MAGIC / AdvEvo-MARL / SEAS 协同演化线
- 明确指出**两个病态**（用加粗短语）：
  - **Attack Strategy Collapse**（攻击策略坍缩）：RL 过拟合少数高回报策略，攻击分布严重不均
  - **Defense Adversarial Forgetting**（防御对抗遗忘）：防御者学新攻击时遗忘旧攻击
- 强调两病态互相加强：坍缩的攻击分布训出偏科的防御者，偏科的防御者又进一步让攻击者巩固窄策略
- 关键 citations（占位）：`[liu2025chasing]` (Self-RedTeam), `[magic2025]` (MAGIC), `[advevomarl2025]` (AdvEvo-MARL), `[ssp2026]` (SSP)

**段 3：Gap 分析 — 现有方法"静态机制嫁接到动态系统"**

这一段是整个 Introduction 的**关键差异化段落**，需细分为两个子话题：

**3A（Diversity gap）**：
- QD / MAP-Elites 流派（Rainbow Teaming / QDRT / RainbowPlus / Ferret）：针对**静态目标**构造 archive，不适用于防御者持续演化的协同场景
- RL-diversity 流派（CRT / DiveR-CT / GFlowNet）：多样性信号停留在文本/语义层面（Self-BLEU, embedding distance），无法驱动**策略层面**的分散
- **特别指出 TriPlay-RL**：这是**协同演化中已注意到多样性**的最接近的先验工作，但其多样性机制仅基于 Self-BLEU 和 embedding cosine similarity，属于**纯语义/表层约束**，不对攻击策略空间做结构化划分。结果是：攻击者可以通过措辞变化骗过多样性惩罚，但实际策略仍然坍缩——"换皮不换招"
- 引出我们的方案：需要在**策略空间**（risk × style）而非文本空间做多样性优化

**3B（Replay gap — 修正 Opus 分析中的错误）**：
- 先肯定 SSP（Be Your Own Red Teamer）的贡献：它确实设置了经验回放池，并且**在回放之后实时更新样本的有害性估计**（这是 Opus/GPT 分析中错误表述的地方——SSP 的确在更新）
- 随后指出 SSP 的**真正局限**：更新机制依赖 judge 给出**离散的 safety score**（如 0/1 或少数等级）来更新样本后验风险，缺乏以下三个维度的建模能力：
  1. **无法表达估计不确定性**：离散分数不能反映"采样次数少、估计不可信"这一信息
  2. **不考虑防御者响应的偶然性**：单次防御成功可能因温度采样而发生，离散机制可能因一次偶然成功就过早淘汰有价值的攻击
  3. **不考虑防御者能力的动态性**：离散累计分数没有遗忘机制，旧的估计会"污染"当前防御者能力的判断
- 引出 DACE 的方案：连续值 Beta-Bernoulli 后验（均值 + 方差）+ 时间衰减 + Thompson Sampling，同时处理这三个维度

**段 4：DACE 提案 + "we observe" 钩子**
- 用 "In this paper, we propose DACE..." 作为转折
- 一句话总结：DACE 引入显式策略空间 + 归一化多样性奖励 + 贝叶斯回放池，使协同演化同时具备覆盖广度与记忆持久度
- "We observe" 一行：训练后期 attacker 涌现出组合式攻击（combinatorial attack emergence），即单个 prompt 中 seamless 融合多个 risk × style，这是 MAGIC/Self-RedTeam 未观察到的现象。此为强实验钩子，自然引出后续实验
- 视觉上 Figure 1 同步展示（MAGIC 攻击热力图 vs DACE 攻击热力图 + DACE 组合攻击示例）

**Contributions bullet（3 条，每条 3-4 句）**：
1. **Problem framing**: 首次系统地将协同演化中的"攻击策略坍缩"与"防御对抗遗忘"建模为一个需要联合优化覆盖广度与记忆持久度的整体问题
2. **Method**: 提出 DACE 框架，包含显式 12×10 策略空间 + 归一化边际覆盖增益奖励 + Beta-Bernoulli 贝叶斯回放池
3. **Empirical**: 在 WildGuardTest / HarmBench / X-Teaming / MAJIC / Auto-RT 等 9+ benchmark 上显著优于 MAGIC 与其他 SOTA，同时通用能力无退化，且攻击者生成的多样性覆盖率从 MAGIC 的 X% 提升至 Y%（占位）

#### 关键写作原则
- **不提 MAGIC 具体机制**（如 SPNE 定义）——留给 §3
- **不提具体方法实现**（如 λ 系数）——留给 §4
- 段 2-3 的 citation 密度要高（每句 1-2 个）
- 段 4 的"we observe" 钩子要有视觉预告

### §2 Related Work（极简版，0.5 页）

3 段落结构，每段约 3-4 句（共 12-15 句）：

**2.1 LLM Jailbreaks and Static Alignment**
- 简述攻击演化：human-crafted → GCG → PAIR/TAP/AutoDAN → multi-turn agentic
- 静态对齐（RLHF、guardrails）受限于预分布

**2.2 Co-Evolutionary Safety**
- Self-RedTeam、MAGIC、ACE-Safety、AdvEvo-MARL、SSP、TriPlay-RL、SEAS
- 转折：均缺乏对策略覆盖与记忆的系统机制

**2.3 Diversity in Red-Teaming**
- QD 流派（Rainbow/QDRT/RainbowPlus/Ferret）+ RL-diversity 流派（CRT/DiveR-CT/GFlowNet）
- 结尾：这些工作针对静态目标；我们将其迁移至动态协同演化

**附录完整版 Related Work**：
- 4 小节细分（LLM Safety Alignment / Automated Red-Teaming / Quality-Diversity Search / Experience Replay & Continual Learning），每节 1-2 段
- 含与 DACE 的具体对比表（可选）

### §3 Preliminaries & Problem Formalization（0.6 页）

**结构**：
- 继承 MAGIC 的非对称序贯博弈定义（简化复述一遍）
- 形式化定义两大病态：
  - **Strategy Collapse**：攻击者策略分布熵 \(H(\pi_A) \ll \log|\mathcal{B}|\)
  - **Adversarial Forgetting**：防御者对早期攻击 \(\mathcal{H}_t\) 的 ASR 随训练步衰退 \(\mathbb{E}_{x \in \mathcal{H}_t}[ASR_{\text{refuse}}(x)] \searrow\)
- 说明这两个病态是 co-evolutionary 协同演化的"共害现象"，需要联合优化

### §4 Method（3.2 页，4 子节 + 简版算法框）

#### §4.1 Overview（0.4 页 + Figure 2）
- 两阶段交替迭代（Attacker → Defender），核心循环叙述
- Figure 2: DACE 训练流程图
  - 左：Stage 1 attacker RL（新攻击 + λ-weighted diversity reward）
  - 中：统一攻击档案池（策略频次 + Beta-Bernoulli 后验双重功能）
  - 右：Stage 2 defender RL（新攻击 + Thompson 采样回放混合）
- 一句话引用附录：详细伪代码见附录 Algorithm A.1

#### §4.2 Explicit Attack Strategy Space（0.6 页）

**核心内容**：
- 定义 \(\mathcal{B} = \mathcal{S} \times \mathcal{C}\)，\(|\mathcal{S}| \times |\mathcal{C}| = 12 \times 10 = 120\) 单元
- \(\mathcal{S}\)：来自 Llama-Guard-4 taxonomy 的 **12 个风险类别**
  - 原始 LG4 有 14 类，删除两个不适用类别：S12 Sexual Content（频率 0.80%，benign Guard not-safe 率 96.3% 不可靠），S14 Code Interpreter Abuse（频率 0.11%，text-only 防御器概念不适用）
  - 保留编号 1-12，paper 说明引用 LG4 S1-S11 + S13
- \(\mathcal{C}\)：来自 **Rainbow Teaming** 的 10 种攻击风格（Slang / Technical Terms / Role Play / Authority Manipulation / Misspellings / Word Play / Emotional Manipulation / Hypotheticals / Historical Scenario / Uncommon Dialects）
- 攻击者输出三段式：`<think>推理</think><strategy>risk category: ... attack style: ...</strategy><answer>改写后 prompt</answer>`
- 正则提取策略描述符 \(b(x)\)，而非 LLM judge 评估（降低噪声，直接监督策略选择）
- SFT 热启动：用 Gemini-2.5-Pro 蒸馏约 43k 三段式 CoT 样本（详见附录 B）

#### §4.3 Diversity-Aware Attacker Optimization（0.9 页）

**4.3.1 Composite Reward**
\[
R_A(x) = -R_D(x, y_D) + R_{\text{fmt}}(x) + \lambda(x) \cdot R_{\text{div}}(x)
\]
其中 \(-R_D\) 保持零和结构。

**4.3.2 Normalized Marginal Coverage Gain**（核心创新）
\[
R_{\text{div}}(x) = \frac{H(\mathbf{p}_{\mathcal{A} \cup \{x\}}) - H(\mathbf{p}_{\mathcal{A}})}{\max_{b \in \mathcal{B}}[H(\mathbf{p}_{\mathcal{A} \cup \{x_b\}}) - H(\mathbf{p}_{\mathcal{A}})] + \epsilon}
\]
- 解释 reward vanishing 问题：raw marginal entropy 衰减为 \(O(1/|\mathcal{A}|)\)
- 归一化后：分子分母同阶，比值 \(O(1)\) 稳定
- 计算复杂度 \(O(|\mathcal{B}|)\)，batch 内共享分母

**4.3.3 KL Divergence Perspective**
\[
H(\mathbf{p}_{\mathcal{A} \cup \{x\}}) - H(\mathbf{p}_{\mathcal{A}}) = D_{\text{KL}}(\mathbf{p}_{\mathcal{A}} \| \mathbf{u}) - D_{\text{KL}}(\mathbf{p}_{\mathcal{A} \cup \{x\}} \| \mathbf{u})
\]
- 单步 KL 收缩效率的语义
- Zero-avoiding 性质：低频槽位获得最强梯度

**4.3.4 Differentiated Diversity Coefficient**
\[
\lambda(x) = \begin{cases} 1.0 & \text{if success} \\ 0.5 & \text{otherwise} \end{cases}
\]
- 理由：成功样本已验证威胁；失败样本保留折减激励避免冷门策略方向探索信号完全消失

#### §4.4 Bayesian Adversarial Replay for Defender（0.9 页）

**4.4.1 Unified Archive Pool**
- 统一档案池 \(\mathcal{A}\) 双重功能：策略频次（支撑覆盖度奖励）+ 回放缓冲
- 仅存攻击 prompt（不含 defender 响应），每样本维护 \((s_i, f_i)\)

**4.4.2 Beta-Bernoulli Posterior Threat Tracking**
\[
p_i \mid s_i, f_i \sim \text{Beta}(\alpha + s_i, \beta + f_i)
\]
- 后验均值 \(\hat{p}_i\) 和后验方差 \(\text{Var}(p_i)\) 提供**点估计 + 不确定性**
- 强调与 SSP 离散更新的对比（正文用一两句话；完整对比在附录）：
  - SSP 以离散 safety score 累加/递减 → 无法表达不确定性、易被偶然性误判、无遗忘机制
  - DACE 以连续值 Beta 后验 → 均值聚合所有历史试验、方差量化估计不确定性、支持时间衰减

**4.4.3 Time Decay for Non-Stationarity**
\[
s_i \leftarrow \gamma \cdot s_i, \quad f_i \leftarrow \gamma \cdot f_i \quad (\gamma \in [0.9, 0.99])
\]
- 每轮开始执行，将估计缓慢"遗忘"回先验
- 自然追踪防御者能力漂移

**4.4.4 Thompson Sampling for Replay**
\[
\tilde{p}_i \sim \text{Beta}(\alpha + s_i, \beta + f_i), \quad \text{select top-}B_{\text{replay}}
\]
- 自适应 exploration-exploitation 平衡
- 高后验均值+低方差 → 稳定威胁（exploit）；高方差 → 需要验证（explore）

**4.4.5 Pruning**
\[
\text{remove if } \hat{p}_i < \epsilon \text{ AND } (s_i + f_i) > n_{\min}
\]

#### §4.5 Training Algorithm (Simplified)
- 主文放一个 10-15 行的**简化算法框**，显示两阶段主循环
- 完整带变量、数据结构、边界条件的多页伪代码放附录 A
- 简版伪代码样式：
```
Algorithm 1: DACE (simplified)
for round k = 1 to K:
  [Stage 1 – Attacker RL]
    sample seeds; attacker rollouts with strategy selection
    evaluate; compute R_A including normalized coverage gain
    GRPO update π_A; flush successful attacks to A
  [Stage 2 – Defender RL w/ mixed batch]
    decay (s,f); Thompson sample D_replay from A
    combine new attacks + D_replay
    GRPO update π_D; Bayesian posterior update + prune
return π_A, π_D
```

### §5 Experiments（2.4 页）

#### §5.1 Experimental Setup
- Models: Qwen2.5-7B-Instruct (primary), Llama3.1-8B-Instruct (secondary)
- Baselines: Base / Self-RedTeam / MAGIC / SSP / (optionally SEAS, AdvEvo-MARL if comparable checkpoints available)
- Benchmarks: 见 RQ 下分布
- 训练细节指向附录 D

#### §5.2 Main Results — 以 RQ 驱动

**RQ1: Does DACE improve defender safety without over-refusal tax?**
- Table 1: 9 benchmark × 3 backbone（WildGuardTest, WJB adv, HarmBench adv/van, DAN, XSTest safe/unsafe RTA, OR-Bench, StrongREJECT）
- 解读模板：DACE 在 adversarial 场景显著降低 ASR（e.g., "WG Test ASR X% → Y%"），在 benign 场景 comply rate 与 MAGIC 持平

**RQ2: Is DACE's safety gain free of general capability cost?**
- Table 2: IFEval, ARC-C, GPQA, MMLU, AlpacaEval 2（5 capabilities × backbone）
- 解读模板：差距 < 2%，GPQA 可能小幅提升

**RQ3: How robust is DACE defender to SOTA automatic red-teaming?**
- Table 3: GCG / PAIR / TAP / AutoDAN / AutoDAN-turbo / MAJIC / Auto-RT
- 解读模板：MAJIC 和 AutoDAN-turbo 是最强 OOD，DACE 相较 MAGIC 保持更低 ASR

**RQ4: Does DACE attacker exhibit coverage-aware diverse attack behavior?**
- Figure 3: 12×10 strategy heatmap（MAGIC vs DACE w/o diversity vs DACE full）
- Table 4: Multi-level diversity metrics (Strategy coverage rate / Shannon entropy / Max-cell share / QD-Score + 补充文本级 Self-BLEU / Distinct-2 / SBERT cosine)
- Figure 4 (optional): Combinatorial attack emergence case study (sanitized)

**RQ5: Does Bayesian replay prevent defense adversarial forgetting?**
- Figure 5: 不同训练阶段攻击样本 ASR 曲线（early / middle / late × 不同 replay 策略）
- 展示 w/o replay 呈 U 型遗忘；uniform replay 部分缓解；DACE full 最平缓

#### §5.3 Ablation Study
- Table 5: DACE full vs w/o diversity vs w/o SFT vs w/o coverage reward vs w/o replay vs w/ novelty reward (替代 coverage) vs w/ uniform replay (替代 Thompson)
- 列指标：WJB ASR / DAN ASR / AutoDAN-turbo ASR / XSTest Comply / Strategy Coverage / Forgetting (early attack ASR)
- 解读：每个组件缺失都会在至少两列上劣化

#### §5.4 Cross-Evaluation of Co-Evolution Dynamics（若篇幅允许）
- Figure 6: 5×5 attacker-defender checkpoint ASR heatmap，验证双方同步演化、无 OOD 攻击者反弹

### §6 Conclusion（0.3 页，3 段）

1. **核心贡献重述**：将"覆盖广度"与"记忆持久度"作为协同演化的两个新维度，并通过归一化覆盖奖励 + Bayesian 回放机制系统求解
2. **局限**：策略空间离散性、组合涌现对 SFT 质量敏感、仅文本单轮验证
3. **未来方向**：连续策略空间 / 多模态 / agent 协同 / lifelong 记忆 / 与 inference-time 推理安全对齐正交组合

### Appendix（12-15 页）

| 附录 | 内容 | 页数 |
|---|---|---:|
| A | 完整训练伪代码 + 超参表 | 1.5 |
| B | 策略空间设计：12×10 剪裁数据证据、LG4 映射、Rainbow Teaming attack styles、SFT 蒸馏 prompt 模板 | 2 |
| C | Prompts: attacker template / defender template / judge templates | 1.5 |
| D | Training setup 详情（硬件、超参、curricula） | 1 |
| E | Benchmark protocols（包括 MAJIC/Auto-RT/X-Teaming 接入细节） | 1.5 |
| F | 扩展结果：多 backbone (Llama/Qwen-14B)、多 judge 交叉验证 | 2 |
| G | 训练动态：pool size 曲线、entropy 演化、reward 稳定性、forgetting curve 放大 | 1.5 |
| H | Attack pattern qualitative analysis（组合攻击案例，sanitized） | 1.5 |
| I | Related Work 完整版（4 小节） | 1 |
| J | Limitations + Broader Impact + Ethical considerations | 0.5 |
| K | NeurIPS Checklist 回答（见 checklist.tex） | N/A |

---

## 三、LaTeX 文件组织与修改清单

### 3.1 目标文件结构（遵循 NeurIPS 模板极简原则）

**用户明确指示**：整体遵循 NeurIPS 模板，一般**不动 `neurips_2026.sty`**，主要**修改 `neurips_2026.tex`**，可适当添加其他文件。

因此采用"主文集中、辅文最小化"策略：

```
z_materials/DACE_NeurIPS_2026/
├── neurips_2026.tex          # 【主文件】所有论文内容写在这里（含正文 + 附录）
├── neurips_2026.sty          # 【不动】NeurIPS 官方样式
├── checklist.tex             # 【最终填答】保持文件名/路径不变
├── references.bib            # 【新增，必需】占位 bibtex 条目，供 \bibliography{} 使用
└── figures/                  # 【新增，必需】论文插图目录
    ├── dace_pipeline.pdf     # Figure 2: DACE 训练流程图（初稿用 \fbox 占位）
    ├── motivation.pdf        # Figure 1: Motivation（MAGIC 坍缩 vs DACE 热力图 + 组合攻击示例）
    ├── coevolution_heatmap.pdf  # Figure 5/6: 5×5 attacker-defender 协同热力图
    ├── strategy_space.pdf    # Figure 3: 12×10 策略热力图对比
    └── forgetting_curve.pdf  # Figure 5: 回放池对遗忘的缓解
```

**关键原则**：
- 所有章节内容（abstract / intro / related / preliminaries / method / experiments / conclusion / appendix）都在 `neurips_2026.tex` 单文件内组织
- **不新建 `sections/` 子目录**（避免过度工程化，符合 NeurIPS 模板惯例）
- 章节之间用大块 `% === SECTION: ... ===` 注释分隔，便于浏览与导航
- 如果后续 `neurips_2026.tex` 变得过长（> 2000 行）难以维护，再考虑切分

### 3.2 模板保留策略（关键约束）

- `neurips_2026.tex` 中**所有原内容**（L61-509，包括 title/author/abstract/正文 demo/checklist/references 等 placeholder）都用 `%` 注释化，**不删除**，方便写作时查看模板原示例
- 新内容在每个 section 原位置**下方**写入（先注释原占位内容，再写新内容）
- 例：
```latex
% \title{Formatting Instructions For NeurIPS 2026}  % 原模板，保留作参考

\title{DACE: Diversity-Driven Adversarial Co-Evolution for Robust LLM Safety Alignment}
% Alternative candidates (for final selection; keep commented):
% \title{DACE: Diversity-Aware Adversarial Co-Evolution for Robust LLM Safety Alignment}
% \title{DACE: Diversity-Aware Co-Evolution with Bayesian Adversarial Replay for LLM Safety}
```
- `neurips_2026.sty` **完全不改动**
- `checklist.tex` 最后阶段填答（含 14 项 NeurIPS checklist questions）

### 3.3 写作约定

**每个英文段落必需的中文注释头**：
```latex
% [段 N] 大意：...
% 撰写逻辑：（与上段的衔接）...（本段核心论点）...（与下段的引出）...
% 中文对应内容：...（用中文先复述英文段落内容）...

\textbf{DACE}~\citep{dace2026} is the first framework to...
```

**占位引用**：
- 所有 citation 用 `\citep{paper_short_name}` 或 `\cite{paper_short_name}`
- 短名统一风格：`authorYYYYkeyword`（与 MAGIC.bib 对齐，见 §11.3）
- `references.bib` 先用占位条目，每条含 `note={To be filled}`

**表格**：
- 所有表头、列/行结构、方法名、benchmark 名齐全
- 数据格子统一用 `--` 或 `TODO` 占位
- 表下分析段落以"预期"口吻（"DACE is expected to..."）先写，便于真实数据出来后精修

**伪代码**：
- 主文用 `algorithm2e` 或 `algorithm + algorithmic` 包的简版框（10-15 行）
- 附录用完整版（可 2-3 页，对应 `pseudocode_v3.1.html` 详细内容）

**数学符号一致性**（跨章节）：
- 攻击者策略 \(\pi_A\)，防御者策略 \(\pi_D\)
- 攻击 prompt \(x\)（重写后），原始 seed prompt \(q\)
- 策略描述符 \(b(x) = (s, c) \in \mathcal{B} = \mathcal{S} \times \mathcal{C}\)
- 档案池 \(\mathcal{A}\)；Beta 后验参数 \(\alpha, \beta\)；成功/失败计数 \(s_i, f_i\)
- 奖励 \(R_A, R_D, R_{\text{fmt}}, R_{\text{harm}}, R_{\text{ref}}, R_{\text{div}}\)；多样性系数 \(\lambda(x)\)
- 策略分布 \(\mathbf{p}_{\mathcal{A}}\)；均匀分布 \(\mathbf{u}\)；Shannon 熵 \(H(\cdot)\)；KL 散度 \(D_{\text{KL}}(\cdot \| \cdot)\)

### 3.4 关键文件修改列表（按依赖顺序）

| Step | 文件 | 动作 |
|---|---|---|
| 1 | `neurips_2026.tex` | 顶部改 title/author；`\begin{abstract}` 块替换；依序写入各 section |
| 1.1 | `neurips_2026.tex` § Abstract | 8 句摘要（含 3 个标题候选注释） |
| 1.2 | `neurips_2026.tex` § 1 Introduction | 4 段 + 3 contributions bullet |
| 1.3 | `neurips_2026.tex` § 2 Related Work | 极简 0.5 页版 |
| 1.4 | `neurips_2026.tex` § 3 Preliminaries | 博弈形式化 + 双病态定义 |
| 1.5 | `neurips_2026.tex` § 4 Method | 4.1-4.5（含公式与简版算法框） |
| 1.6 | `neurips_2026.tex` § 5 Experiments | 5 RQ + ablation + 表格结构占位 |
| 1.7 | `neurips_2026.tex` § 6 Conclusion | 3 段 |
| 1.8 | `neurips_2026.tex` § Appendix | A-J 附录（完整伪代码、策略空间设计、prompts 等） |
| 2 | `references.bib` | 占位条目（约 50-80 条，含 §11.3 列出的所有 key） |
| 3 | `checklist.tex` | 按论文内容逐条回答 14 个 NeurIPS checklist questions |
| 4 | `figures/` | 占位图表（用 `\fbox{\rule{...}{...}}` 占位；实际图在实验完成后替换） |

---

## 四、写作顺序建议

为了保证前后段落一致性（符合用户"写完一个部分同时回顾上一个部分并完善"的要求）：

1. **先写整体骨架**：title + abstract + intro + conclusion（四大叙事锚点）
2. **回顾 + 写方法**：method §4（核心技术铺陈）
3. **回顾 intro + method + 写实验**：experiments §5（含 RQ 驱动，与 intro 的贡献 bullet 对齐）
4. **回顾全局 + 写 preliminaries + related work**：§3 §2（作为"胶水"章节）
5. **整理 appendix**：完整版伪代码、设计细节、扩展结果
6. **最终 pass**：
   - 所有中文注释是否齐全
   - 所有 citation 占位是否完整
   - 所有表/图引用 `\ref{}` 是否正确
   - 所有数学符号前后一致
   - 页数是否 ≤ 9

---

## 五、关键参考来源（写作时主要参考）

| 写作需求 | 主要参考 |
|---|---|
| 总体叙事 / 章节 / 写作风格 | MAGIC `arxiv.tex`（已分析） |
| 摘要句式 / Contribution bullet 格式 | MAGIC abstract + intro 最后段 |
| 方法章节数学组织 | MAGIC §3-§4 + SIE §2-§3 |
| 实验 RQ box 格式 | MAGIC `rqbox` 环境 |
| 相关工作密度 | MAGIC §2（两小节） |
| 附录组织 | ReMA `sections/appendix.tex` |
| Case study 彩色 box | MAGIC `tcolorbox` |
| DACE 核心技术细节 | `研究方法v3.1.md` + `pseudocode_v3.1.html` + `dace_coding_v3.1.md` |
| 剪裁设计证据（12×10） | `dace_coding_debug_v4.md` + `dace_v4_rebuild_decisions.md` |
| Intro 三个贡献的表述 | Opus `Introduction 分析` + GPT `Introduction 分析` |
| 实验表格与 RQ 设计 | Opus `Evaluation 分析` + GPT `Evaluation 分析` |
| TriPlay-RL 批判点 | 已由 Explore agent 提取关键引文 |

---

## 六、Critical Files（实现写作时需阅读的关键文件）

### 必须参考（实现时优先阅读）
- `/mnt/shared-storage-user/yupeng/MAGIC/z_materials/DACE_NeurIPS_2026/neurips_2026.tex` — 目标模板
- `/mnt/shared-storage-user/yupeng/MAGIC/z_materials/DACE_NeurIPS_2026/checklist.tex` — 待填答
- `/mnt/shared-storage-user/yupeng/MAGIC/z_materials/研究方法v3.1.md` — 方法正文依据
- `/mnt/shared-storage-user/yupeng/MAGIC/z_materials/pseudocode_v3.1.html` — 附录伪代码依据
- `/mnt/shared-storage-user/yupeng/MAGIC/z_materials/arXiv-MAGIC/arxiv.tex` — 风格最主要参考
- `/mnt/shared-storage-user/yupeng/MAGIC/z_materials/arXiv-MAGIC/arxiv.bib` — 引用占位对照

### 重要背景（已读，仅需回溯）
- `/mnt/shared-storage-user/yupeng/MAGIC/z_materials/DACE Introduction 分析-opus.md` + `-gpt.md`
- `/mnt/shared-storage-user/yupeng/MAGIC/z_materials/DACE Evaluation 分析-opus.md` + `-gpt.md`
- `/mnt/shared-storage-user/yupeng/MAGIC/z_materials/DACE title abstract method conclusion related-work appendix 分析-opus.md` + `-gpt.md`
- `/mnt/shared-storage-user/yupeng/MAGIC/z_materials/研究方法v2.1.md`（设计迭代上下文）
- `/mnt/shared-storage-user/yupeng/MAGIC/z_materials/覆盖度熵变体分析与推荐.md`（KL 视角理论来源）
- `/mnt/shared-storage-user/yupeng/MAGIC/z_materials/可选定义对比分析与推荐组合.md`（设计选择推理）
- `/mnt/shared-storage-user/yupeng/MAGIC/z_materials/dace_coding_v3.1.md` + `dace_coding_debug_v3/v4.md`（实现细节）
- `/mnt/shared-storage-user/yupeng/MAGIC/z_materials/dace_v4_rebuild_decisions.md`（12×10 剪裁决策）
- `/mnt/shared-storage-user/yupeng/MAGIC/z_materials/dace_benign_prompt_conflict.md`（BENIGN_TEMPLATE 修正）

### 风格借鉴
- `/mnt/shared-storage-user/yupeng/MAGIC/z_materials/arXiv-ReMA/sections/` — 分章节组织模式
- `/mnt/shared-storage-user/yupeng/MAGIC/z_materials/arXiv-SIE/iclr2026_conference.tex` — RQ 驱动实验

### 相关论文 PDF / LaTeX（按需子代理查阅）
- `/mnt/shared-storage-user/yupeng/MAGIC/z_materials/safety_papers_pdf_latex_package/papers/safety_co-evolution/`
- `/mnt/shared-storage-user/yupeng/MAGIC/z_materials/safety_papers_pdf_latex_package/papers/safety_diversity/`

---

## 七、Verification（验证方案）

每完成一节后：

1. **编译验证**：
   ```bash
   cd /mnt/shared-storage-user/yupeng/MAGIC/z_materials/DACE_NeurIPS_2026
   pdflatex neurips_2026.tex
   # 预期：无 fatal 错误，warning 可接受（如 undefined references 在占位阶段正常）
   ```

2. **中文注释完整性自检**：每个 `\section{}` / `\subsection{}` 下的段落前是否都有 `% [段 N]` 注释头

3. **Placeholder 扫描**：
   ```bash
   grep -n "TODO\|占位\|--\|\\\\citep{[a-z]*YYYY" sections/*.tex
   ```

4. **篇幅校验**：每节完成后查看 pdf 页数

5. **风格对齐**：对比 MAGIC `arxiv.tex` 段落开头句式，确保叙事节奏一致

6. **关键贡献对齐**：
   - abstract / intro 最后 bullet / conclusion 首段 / experiments RQ 描述 — 四处必须表述一致
   - 方法章节 4.3.3 KL 视角的理论推导需严格对应 `覆盖度熵变体分析与推荐.md` §4

7. **技术正确性**：
   - 公式 \(R_A = -R_D + R_{\text{fmt}} + \lambda R_{\text{div}}\) 与 `pseudocode_v3.1.html` Def 3 完全一致
   - 贝叶斯更新 \(s_i \leftarrow s_i + 1\) / \(f_i \leftarrow f_i + 1\) 与 `pseudocode_v3.1.html` Def 2 一致
   - 简版算法框与附录完整版主循环一致

---

## 八、Open Questions / 延后决策

以下在写作过程中若遇到，暂按 DEFAULT 执行，待用户复核：

1. **论文签名**：作者与机构以用户实际情况填写（初稿可先保持 `Anonymous Author(s)`）
2. **Figure 1 (Motivation) 和 Figure 2 (DACE Pipeline)**：**用户将后续补充这两张关键图**。初稿用 `\fbox{\rule[-3cm]{0cm}{6cm}\rule[-3cm]{\linewidth}{0cm}}` 占位 + 完整 caption（caption 可以先写好），等用户提供 PDF 后替换 `\includegraphics{}` 路径即可
3. **Figure 3 (12×10 strategy heatmap)、Figure 5 (co-evolution heatmap)、Figure 5/6 (forgetting curve)**：等实验完成后用脚本生成 PDF
4. **是否保留 §5.4 Cross-Evaluation Heatmap**：若主文溢出 9 页则移至附录
5. **Broader Impact / Limitations**：按 NeurIPS 模板放 appendix 或 conclusion 内，初稿同时写两处（择一）
6. **是否公开 replay pool 作为数据集贡献**：若不确定暂不声明，保留作为 future work 可能性
7. **实验表格实际数据格式**：等 evaluation 流水线跑完后统一填入（均值 ± 标准差 / 单点数 + boldface winner 等），初稿统一用占位

遇到以上 1-6 的任何一个、或发现新的技术细节冲突，暂停写作并通过 AskUserQuestion 询问。

---

## 九、潜在风险

1. **Opus/GPT 分析对 SSP 的表述不准**（用户已指出）：写作时必须以用户修正版为准——SSP 确实实时更新回放样本风险，但用离散 judge 分数 + 无不确定性 + 无遗忘机制，这是 DACE 要改进的三个维度
2. **TriPlay-RL 的主张轻重**：不要过度贬低，保持学术尊重——肯定它在协同演化中注意到了 diversity（确实是最接近的先验工作），但指出其多样性限于文本/embedding 层面（已由 Explore agent 提取具体引文作证）
3. **12×10 剪裁的说服力**：论文中必须清晰说明剪裁理由（附录 B 完整证据链），避免被审稿人误解为 ad-hoc
4. **避免与 MAGIC 重复表述**：尤其是 §3 博弈形式化，应简洁引用 MAGIC 然后聚焦 DACE 新增的 coverage / memory 概念
5. **实验数据占位的表述**：分析段落用"is expected to"句式，避免未来实际数据与预期偏离时需要大改写
6. **中文注释的信息量**：避免注释过于机械（只说"This paragraph introduces X"），应包含**与上下段的衔接逻辑**和**段内核心论点**，成为完整的中文平行稿

---

## 十、原始任务提示（供实现时参考）

以下为用户原始 prompt 的完整存档，用于实现阶段回顾需求：

> 帮忙分析并整理 DACE 论文写作，下面分别是相关材料和写作要求，
>
> ================================================
> 【相关材料和资料】
> @z_materials/safety_papers_pdf_latex_package/
> @z_materials/safety_papers_pdf_latex_package/papers/safety_co-evolution/
> @z_materials/safety_papers_pdf_latex_package/papers/safety_diversity/
> 这里是 oups 和 gpt 对话历史中附件中的相关论文，包含 safety_co-evolution 和 safety_diversity，可以在 subagent 中阅读，可以找 pdf 阅读工具来阅读这些论文内容，方便写相关工作和 introduction，
>
> @z_materials/LLM_Red_Teaming_Papers_Analysis.md
> @z_materials/LLM_RedTeaming_Diversity_Research_Report.md
> @z_materials/LLM_Safety_Diversity_CoEvolution_Survey.md
> @z_materials/研究动机与研究方法.md
> @z_materials/研究方法v2.1.md
> @z_materials/覆盖度熵变体分析与推荐.md
> @z_materials/可选定义对比分析与推荐组合.md
> 这是 dace 之前的历史调研和历史研究方法，可以大概阅读来方便理解，可以在 subagent 中阅读，
>
> @z_materials/ ，请认真分析并理解这个文件夹下的重要材料，
> @z_materials/DACE Evaluation 分析-opus.md ，这是 claude opus 对实验章节的分析，
> @z_materials/DACE Introduction 分析-opus.md ，这是 opus 对 introduction 章节的分析，
> @z_materials/DACE title abstract method conclusion related-work appendix 分析-opus.md，这是 opus 对其他章节的详细分析，
> @z_materials/DACE Evaluation 分析-gpt.md ，这是 gpt 5.5 对实验章节的分析，
> @z_materials/DACE Introduction 分析-gpt.md ，这是 gpt 对 introduction 章节的分析，
> @z_materials/DACE title abstract method conclusion related-work appendix 分析-gpt.md ，这是 gpt 对其他章节的详细分析，
> 这是一些 claude opus 和 gpt 5.5 整理的分析，
>
> @z_materials/dace_coding_v3.1.md
> z_materials/dace_coding_debug.md
> @z_materials/dace_coding_debug_v3.md
> @z_materials/dace_coding_debug_v4.md
> 这是 dace 实现和完善的 coding 和 debug 文档，方便查看更了解实现细节，
>
> @z_materials/MAGIC.pdf @z_materials/arXiv-MAGIC/arxiv.tex ，magic 论文的 pdf 和 latex，
> @z_materials/ReMA.pdf @z_materials/arXiv-ReMA/neurips_2025_conference.tex @z_materials/arXiv-ReMA/sections/ ，这是 ReMA 论文的 pdf 和 latex，
> @z_materials/SIE.pdf @z_materials/arXiv-SIE/iclr2026_conference.tex ，这是 SIE 论文的 pdf 和 latex，
> 这是一些优秀的写作 pdf 和 latex，可以学习参考，
>
> @z_materials/研究方法v3.1.md
> @z_materials/pseudocode_v3.1.html
> @z_materials/DACE_NeurIPS_2026/
> 这是 dace 最新版的研究方法和伪代码，以及 latex 文档模板，需要重点参考来写作，
>
> ================================================
> 【写作要求和建议】
> 帮忙根据相关材料和资料写一下 DACE 论文的 latex 文档，请深入分析相关材料，保持专业性和清晰性，
>
> 重点参考 MAGIC 论文的、写法样式和风格，同时可以参考优秀论文 ReMA 和 SIE 的写法，学习写作经验，
>
> 注意，neurips_2026 模板原始内容已经注释但没有删除，请保持注释状态也不要删除方便参考写法，
> 对于模板中暂未注释的东西，不要删除，比如 title 和 abstract 等，你在写的时候注释掉原内容再写，
> @z_materials/DACE_NeurIPS_2026/ ，DACE 论文模板在这里，参考 sty 和 tex 文件进行论文写作，
>
> 在撰写和修改时，对于每个段落，段落内容请用英文书写，但每个段落上面都务必用中文写上注释，说明该段的大概意思、撰写逻辑关系、与上下段落的关系和与英文内容对应的中文段落内容，中文段落内容可以先忽略引用等标记，
>
> 对于参考文献，不用在浏览器搜索 bibtext，先用占位符替代，比如使用论文简称，我后面单独查具体的引用条目，
>
> 你可以参考 claude opus 和 gpt 5.5 整理的分析，借鉴这两个分析过的不错的内容，但是也需要参考它们对话历史中的 prompt，来自己独立进行一轮的论文各个部分写作分析和整理，最后对于论文每个部分，综合你的分析、opus 分析和 gpt 分析来写作，最终对论文整体已经论文的每个部分，详细的写出写作分析和计划；为了使论文写作质量更高，可以先整体分析 DACE 写作框架，然后逐个部分进行写作，写完一个部分同时回顾上一个部分并完善，
>
> 补充一下关于 introduction 中现有方法的不足和 gap：对于 diversity，除了分析自动红队中 quality-diversity 和 RL-based diversity 的相关工作的局限性，额外提一下 TriPlay-RL 这篇论文，它在攻防协同建模中关注到了 diversity，但只是语义层面比较 superficial，不能带来攻击策略的提升；对于 replay，在现有的 opus 和 gpt 的分析中有误，样本的有害性/奖励也会在 replay 之后实时更新，但是依赖 judge 给出离散的 safety score 来更新样本后验风险，不够灵活，并且没有考虑 defender 的偶然性和动态性，
> （这两点这个是我们的 dace 框架需要解决并且可以解决的问题，所以建议额外说明一下，可以适当分析并润色）
>
> 在方法中注意说明二维攻击策略空间（risk category * attack style）的来源，其中 risk category 来自 llama-guard4 分类但调整删除了两个频率很低的类别，attack style 来自 RainbowTeaming 的分类，
>
> 实验表格先做好，但具体数据可以先留白，内容等评测完成再补上去，实验分析和结论先按照预期的理想情况来写，
>
> 鉴于文章篇幅和伪代码长度，考虑将本文 DACE 的伪代码放到附录，同时在方法中说明伪代码见附录xxx，
> 同样的，对于 related work，如果正文太长了就放到附录，估计 related work 直接放到附录就好，
>
> 相关材料和资料比较多，可以先分类制定阅读计划，然后开始有计划的阅读，以便更好的理解并制定写作计划，
> 你可以使用 subagent 来分析一些不那么 critic 但也需要熟悉理解的文件和材料，以便保持主对话上下文必要，
>
> 分析完成准备写 plan 文件的时候，记得在最后加一个章节，把现在这个 prompt 加进去，方便实现的时候参考，
>
> 如果有存在冲突或者有不确定存疑的地方请及时提问，我会给你反馈信息。
>
> 整体需要遵循 NeurIPS 模板，一般不动 neurips_2026.sty，修改 neurips_2026.tex，可适当添加其他文件


### 用户后续补充（关键修正）

> 对于 prompt 中的这部分，刚刚缺失了，补充一下补充一下关于 introduction 中现有方法的不足和 gap：对于 diversity，除了分析自动红队中 quality-diversity 和 RL-based diversity 的相关工作的局限性，额外提一下 TriPlay-RL 这篇论文，它在攻防协同建模中关注到了 diversity，但只是语义层面比较 superficial，不能带来攻击策略的提升；对于 replay，在现有的 opus 和 gpt 的分析中有误，在 SSP 中样本的有害性/奖励也会在 replay 之后实时更新，但是依赖 judge 给出离散的 safety score 来更新样本后验风险，不够灵活，并且没有考虑 defender 的偶然性和动态性，
> （这两点这个是我们的 dace 框架需要解决并且可以解决的问题，所以建议额外说明一下，可以适当分析并润色）
> 对于 replay 分析，opus 的现有分析理解有误，讲的是对 SSP 论文（Be Your Own Red Teamer）的分析，

### 用户决策（经 AskUserQuestion 确认）

1. **Title**: 以 `DACE: Diversity-Driven Adversarial Co-Evolution for Robust LLM Safety Alignment` 为主，其他候选以 LaTeX 注释形式一并写入
2. **Related Work**: 正文保留极简版（0.5 页），完整版放附录
3. **Pseudocode**: 正文简版 + 附录完整版
4. **Tables**: 表头 + 结构 + 占位符（数据等评测完成后填入）

---

## 十一、补充调研发现（来自 subagent 扩展阅读）

以下为本轮 4 个 haiku subagent 并行阅读的关键增量发现，可直接指导具体章节写作。

### 11.1 Diversity 相关工作扩展清单（用于 §2.3 / Appendix I Related Work）

每条格式：`paper_key` — 方法一句话 + 对 DACE 的局限点。

| Paper | 一句话方法 | DACE-相对局限 |
|---|---|---|
| Ferret | 多攻击者 ensemble + reward 评分的 QD 加速 | 静态目标，文本级多样性 |
| Ruby Teaming | QD search + memory cache | 离线 archive，不随防御者演化 |
| RainbowPlus | 多策略 prompting 增强 Rainbow 进化 | 静态 QD |
| OpenAI RBR | 自动生成 reward + multi-step RL | 单攻击者 RL，无显式覆盖机制 |
| QDRT | 基于行为空间的 MAP-Elites QD | 离线优化，不适应动态防御者 |
| T-MAP | 轨迹感知进化 | QD on trajectory features，但非 risk × style 结构 |
| CALM | 基于 token 稀疏性的好奇心驱动 | 表层 token 多样性，忽略策略空间 |
| Jailbreak-R1 | GRPO 组相对多样性 | 文本嵌入多样性，无策略级冗余检测 |
| RedTopic | 语义聚类驱动主题多样性 | 话题多样 ≠ 策略多样 |
| Auto-RT | RL 探索越狱策略 | 无 principled coverage reward，无回放 |
| GRTS | 多攻击者博弈 | 缺 risk-category coverage，无 Bayesian replay |
| Active Attacks | 自适应环境红队 | 聚焦环境 feedback，非防御者协同 |
| WildTeaming | 从 in-the-wild 越狱扩展 | 大规模但非 principled coverage |
| RedTWIZ | 自适应攻击规划 | 无结构化策略空间 |
| **TriPlay-RL**（重点批判） | 三角色 self-play + Self-BLEU + embedding cosine 多样性惩罚 | **已分析**：属纯语义表层约束，换皮不换招 |

**Llama Guard / Agent-SafetyBench / Jailbroken / SIRAJ / Attacker-Moves-Second** 可作为 context 一句话提及。

### 11.2 Co-Evolution 相关工作清单补充（用于 §2.2 / Appendix I）

| Paper | 定位 | DACE-相对局限 |
|---|---|---|
| Self-RedTeam | 在线自博弈 RL，零和 Nash | 单边参数共享，未解决坍缩/遗忘 |
| MAGIC | 非对称序贯博弈，SPNE | 无策略覆盖 + 无记忆 |
| ACE-Safety | 树组双感知 MCTS + 课程 RL | 缺 principled diversity signal |
| AdvEvo-MARL | 多智能体协同 + SFT seed pool | 种子池启动，训练中无 diversity |
| SSP | 自博弈 + reflective experience replay + UCB | **离散** safety score 更新，无不确定性建模 |
| AdvGame | 非合作非零和博弈 | 分离 attacker/defender，但无 diversity/replay |
| SEAS | 自演化对抗安全优化 | 典型 mutual evolve，未显式 coverage |
| STAIR | 反思推理提升安全对齐 | 非协同演化 |
| Two-Player Games | Stackelberg 领导者-跟随者 | 博弈论优化，未处理坍缩/遗忘 |
| Alignment Waltz | Agent 协作训练 | 协作视角，非对抗 |
| Chasing Moving Targets | 同 Self-RedTeam | — |
| MART | 多轮自动红队 | 防御者进化，但回放策略简陋 |

### 11.3 MAGIC.bib 中的关键引用键（供 DACE 直接复用以保一致性）

建议在 `references.bib` 中直接复用以下 key（确保与 MAGIC 投稿一致）：

**Attacks**:
- `zou2023universal`（GCG）
- `chao2023twentyqueries`（PAIR）
- `liu2023autodan`（AutoDAN）
- `liu2024autodan`（AutoDAN-turbo）
- `qi2025majic`（MAJIC）
- `rahman2025xteaming`（X-Teaming）
- `shen2023doanythingnow`（DAN）

**Co-evolution**:
- `liu2025chasing`（Self-RedTeam）
- `pan2025advevo`（AdvEvo-MARL）

**Safety benchmarks**:
- `jiang2024wildteaming`（WildJailbreak / WildGuardTest）
- `mazeika2024harmbench`（HarmBench）
- `rottger2023xstest`（XSTest）
- `cui2024orbench`（OR-Bench）
- `souly2024strongreject`（StrongREJECT）
- `xie2024sorry`（Sorry-Bench）

**Alignment**:
- `ouyang2022training`（RLHF InstructGPT）
- `bai2022constitutional`（Constitutional AI）
- `dai2023safe`（Safe RLHF）

**Judges**:
- `inan2023llamaguard`（Llama Guard）
- `han2024wildguard`（WildGuard）
- `zhao2025qwen3guard`（Qwen3Guard）

**Foundation Models**:
- `touvron2023llama`（Llama 2）
- `qwen25max_blog`（Qwen2.5-Max）
- `comanici2025gemini`（Gemini 2.5）
- `guo2025deepseek`（DeepSeek-R1 / GRPO）

**Capability**:
- `zhou2023ifeval`（IFEval）
- `clark2018arc`（ARC-C）
- `rein2023gpqa`（GPQA）
- `hendrycks2021mmlu`（MMLU）
- `dubois2024alpacaeval2`（AlpacaEval 2）

**DACE 独有新增**（MAGIC 未引用）：
- `samvelyan2024rainbow`（Rainbow Teaming — 策略空间 attack style 来源）
- `llamaguard4_2026` 或 `llama2024guard4`（Llama Guard 4 — risk category 来源；需确认 MAGIC.bib 中是否已有）
- `triplayrl2026`（TriPlay-RL — 重点批判对象）
- `pala2025ferret`、`hoang2025rainbowplus`、`diverct2025aaai` 等 diversity 论文
- `ssp2026`（SSP / Be Your Own Red Teamer — replay gap 批判对象）

### 11.4 ReMA 写作风格洞察（可迁移到 DACE）

- **Subsection 命名**：method section 用**动名词祈使式**（"Deploying...", "Training...", "Scaling..."）；experiment section 用**问题式**（"Does X outperform?"）
- **引用密度**：method 段平均每段 2-3 citations
- **过渡结构**：问题-解法-收益，每节前先点出一个 prior work 的 concrete limitation
- **表格设计**：用 `\definecolor` 赋予语义（in-distribution vs out-of-distribution），`\textcolor{red}{}` 标注 gain，`\textcolor{green}{}` 标 loss
- **复杂方程**：用 `\begin{align}` 带颜色高亮关键组件；简单定义用 `equation*`
- **附录 TOC**：ReMA 附录用显式 mini TOC，DACE 附录可以模仿这一做法

### 11.5 §4.2 Strategy Space 的关键数据支撑（用于 Appendix B）

**SFT v3 策略分布（43.8k 样本）**（说明 Rainbow Teaming 风格 + LG4 风险交叉后的自然分布）：
- Non-Violent Crimes 41.89%（18.3k）最大
- Hate 15.45%，Violent Crimes 14.09%，依次递减
- S12 Sexual Content 0.80%（352），S14 Code Interpreter Abuse 0.11%（47）—— 两项 dead rows

**Archive pool step 300（4k samples）**（说明 RL 训练过程中的策略分布漂移）：
- Hate 21.9%，Violent 18.5%，NVC 18.0%（RL 主动重新平衡）
- S12/S14 几乎为空（9 / 5 samples）

**12×10 剪裁关键数据证据**：
- S12 benign "not-safe" 率 96.3%（benign prompt 被 Guard 误判为 unsafe 最高）
- S14 text-only defender 场景不适用（需工具/代码执行表面）
- 剪裁后 12×10 = 120 个有效策略槽位

### 11.6 §5 实验章节关键补充

**OOD attacker 评估必须包含**：
- MAJIC：96.2% ASR on Qwen2.5-7B with <15 queries，最新黑盒 SOTA，代表"unseen 组合式威胁"
- Auto-RT：RL 自动探索越狱，测试 OOD 泛化

**Judge 验证策略**：
- Qwen3Guard：训练 + in-distribution 评估
- GPT-4o：OpenRT 独立判官（避免 reward hacking）
- LG4：在 S1-S14 的风险分类上交叉验证（附录）

**多层次多样性指标**（Table 4/5）：
- D1 策略层：Coverage Rate / Shannon Evenness / QD-Score
- D2 语义层：SBERT pairwise / Vendi Score
- D3 词汇层：Self-BLEU / Distinct-k / n-gram entropy

**Fig 5 协同演化热力图（5×5）**：attacker iter × defender iter 网格，直观展示"无对抗遗忘"——上三角 ASR 保持低位；对角线单调递减。这是 DACE 的 *visual smoking gun*。

### 11.7 V4 数据侧修复的写作含义

**Benign Template 冲突**（v3 43% benign 被 Guard 判 unsafe → v4 目标 ≤ 10%）：
- 旧版"trick into harmful responses" vs 新版"induce over-refusal while preserving benign intent"
- 这个修复不必在正文强调（会显得过于依赖 data engineering），但**附录 B（Strategy Space）必须简要提及** benign 部分的设计考量，以证明 DACE 评估的 benign refusal rate 健康（而不是因为 benign data pollution 虚高）

**SFT 热启动重要性**：
- v4 SFT 蒸馏用 Gemini-2.5-Pro
- 12×10 策略分布定向（directed style via md5 seed）保证 SFT 对冷门策略也有监督
- 没有 SFT 的 ablation（w/o SFT）会显著降低 pool 增长速度，这是 ablation §5.3 的一行重要发现

### 11.8 引用 key 占位风格统一

在 `references.bib` 中使用以下占位模板：
```bibtex
@article{magic2025,
  title={MAGIC: Multi-Agent Adversarial Game for Robust LLM Safety},
  author={Placeholder},
  year={2025},
  note={To be filled}
}
```
所有占位条目都加 `note={To be filled}` 方便后续批量替换为真实 bibtex 条目。
