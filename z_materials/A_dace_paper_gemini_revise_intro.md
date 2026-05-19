### 📝 论文修改计划 (Modification Plan) v2

#### 1. Abstract (摘要) 逻辑分析与修改
* **当前逻辑评估：** 现有的 Abstract 采用了非常经典的 `背景 -> 问题 (双病态) -> 现有方法的Gap -> 我们的Solution (DACE) -> 实验结果` 的结构，逻辑严密，"Problem-Gap-Solution" 对齐得很好。
* **存在的问题：** 对现有工作缺陷（Existing remedies fall short...）的描述稍显冗长，占用了太多字数，导致 DACE 核心方法和实验结果的介绍空间被压缩。同时，原计划中提及了“组合式攻击”，但根据最新指示，DACE 并不强调这一点。
* **修改方案：**
  - **精简 Gap 描述：** 将对 QD、TriPlay-RL 和 SSP 的长句批判，凝练为强有力的陈述（例如："Existing remedies either rely on static targets, superficial textual diversity, or discrete safety scores that fail to capture the non-stationarity of the threat landscape."）。
  - **突出 DACE 核心机制：** 更加紧凑地描述 $12 \times 10$ 策略空间、归一化边际覆盖奖励（Normalized marginal coverage gain）和贝叶斯回放池（Bayesian replay pool）。
  - **移除不相关的声明：** 彻底移除关于“组合式攻击（combinatorial strategies）”的表述，确保与论文的实际设定（单一 risk category + 单一 attack style）一致。

#### 2. Introduction (引言) 逻辑与段落衔接完善
* **当前逻辑评估：**
  - P1: 攻击演化，静态对齐失效（Hook）。
  - P2: 协同演化的局限性，提出两大病态（策略坍缩与对抗遗忘）。
  - P3: 深入分析 Diversity gap 和 Replay gap。
  - P4: 提出 DACE 框架。
* **存在的问题与衔接调整：**
  - **P3 过于厚重（Dense）：** 包含了两大块相互独立的文献批判（多样性和回放），阅读负荷过高。
  - **现有方法的 Gap 分析不够准确/深入：** 原有的分析停留在表面，需要结合具体论文（QD 方法、TriPlay-RL、SSP）深入分析其在 target model (static vs. evolving)、diversity metric (semantic vs. behavioral) 和 replay mechanism (discrete vs. continuous/uncertainty-aware) 上的局限性。
  - **错误包含“组合式攻击”：** P4 中提及的 "combinatorial emergence" 必须删除。
* **修改方案：**
  - **细化 P3 为两段：**
    - **The Diversity Gap:** 对比 QD 方法（通常针对 static target）和 TriPlay-RL（虽然是 co-evolution，但只依赖 Self-BLEU/cosine 这种 semantic 约束，容易被 "new skin, same trick" 绕过）。强调 DACE 引入的是 *behavior-conditioned* diversity。
    - **The Replay Gap:** 分析 SSP（Be Your Own Red Teamer）。指出其虽然有 replay，但依赖离散的 safety score，无法表达估计的不确定性（estimation uncertainty），容易受单次偶然响应影响，且缺乏显式的非平稳性遗忘机制（non-stationarity）。
  - **修正 P4：** 介绍 DACE 的 $12 \times 10$ 策略空间和贝叶斯回放池，删除所有关于 combinatorial strategies 的描述。

#### 3. Introduction - Contribution (贡献) 凝练重写
* **当前问题：** 采用了三大段纯文本（*First*, *Second*, *Third*）描述，篇幅过长，不够醒目。同时包含了对组合式攻击的错误描述。
* **修改方案：** 严格对齐 MAGIC 论文的风格，使用 `\begin{itemize}` 列出三个精炼的 Bullet Points，并彻底移除组合式攻击的表述。
  * \textbf{Item 1 (Problem \& Framework):} 提出并形式化了协同演化中的两大耦合病态（攻击策略坍缩与防御对抗遗忘），并由此引入 \method，一个基于不对称博弈的多样性驱动协同演化框架。
  * \textbf{Item 2 (Core Mechanisms):} 提出了两大创新机制解决病态：攻击者端的显式策略空间与**归一化边际覆盖增益奖励**（确保持续的探索梯度）；防御者端的**贝叶斯对抗回放池**（结合 Beta-Bernoulli 后验、时间衰减与 Thompson 采样，解决非平稳性问题）。
  * \textbf{Item 3 (Empirical Findings):} 广泛的单轮/多轮实验证明，\method 在显著提升安全防御鲁棒性并有效抵御 OOD 攻击的同时，较好地保持了模型的通用能力，且攻击者实现了广泛的策略覆盖。

#### 4. Problem Formalization (问题形式化) 完善
* **当前逻辑评估：** 2.1 节继承了 MAGIC 的序贯博弈；2.2 节用文字描述+熵公式定义了 Collapse 和 Forgetting。
* **存在的问题：** 数学张力不足。仅仅定义了"什么是病态"，但没有明确给出 DACE **试图优化的数学目标形式**。现在的描述太像文字说明，缺乏严格的定义。
* **修改方案：**
  - **增强定义的严谨性：** 规范 Definition 1 和 Definition 2 中的数学符号。例如，使用具体的数学不等式（如 $H(\mathbf{p}_{\pi_A, t}) / \log|\mathcal{B}| < \tau_{collapse}$）来严格定义坍缩。
  - **新增一小节 "Joint Optimization Objective" (联合优化目标)：** 将 2.3 节的文字描述转化为公式。引入一个带约束的联合优化目标：
    - 攻击者最大化 Reward 的同时，受制于策略熵约束 $H(\mathbf{p}_{\pi_A}) \ge \tau$。
    - 防御者最小化当前损失的同时，最小化在历史攻击分布 $\mathcal{H}_{t_0}$ 上的性能退化惩罚。
  - **逻辑升华：** 明确指出直接求解该联合优化极其困难，从而引出第三章（Method）中提出的 *Coverage Reward* 和 *Bayesian Replay Pool* 是对这一理论目标的**优雅且可计算的工程近似**。

#### 5. Conclusion (结论) 逻辑分析与修改
* **当前逻辑评估：** 总结了贡献，并提及了局限性和未来工作，结构完整。
* **存在的问题：** 与 Abstract 和 Introduction 的修改不一致。特别是可能仍潜藏着对不相关特性（如组合式攻击）的强调，或者未充分对齐修改后的 Contribution。
* **修改方案：**
  - 确保 Conclusion 精确呼应修改后的 Abstract 和 Contribution 的三点内容（双病态 -> 两个核心机制 -> 实验结论）。
  - 检查并移除任何关于“组合式攻击（combinatorial attacks/strategies）”的遗留表述。
  - 保持对 Limitations 的客观陈述（如策略空间的离散性、仅在单轮文本设置下验证）。

#### 6. 整体审查与全局修改 (全局一致性)
* 搜索整个 `neurips_2026.tex`，查找并删除所有 `combinatorial`、`compositional` (在形容 attacker strategies 时)、`hybrid strategy` 等表述，因为 DACE 限定为单一 risk category + 单一 attack style。
* 确保提到的所有 baseline（特别是 QDRT、TriPlay-RL、SSP）在引用和对比时都是准确且一致的。