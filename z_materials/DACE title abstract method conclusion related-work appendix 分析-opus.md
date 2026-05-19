# DACE title abstract method conclusion related-work appendix 分析-opus


> 先保留这一版关于 Evaluation 和 Introduction 的分析，切换到下一个任务，
>
> 结合最初的研究方法（研究方法v3.1.md）和伪代码（pseudocode_v3.1.html）文件，
> 参考 MAIGC 论文的写法、样式和风格（见之前上传过的附件 MAGIC.pdf），
>
> 现在帮忙梳理 title abstract method 和 conclusion 的初稿，用中文梳理，先简要介绍 dace 的这些部分怎么写，是什么讲故事逻辑以及为什么要怎么写，再给出具体的每一部分的每一段的内容，要求达到 NeurIPS 投稿水准，
>
> 下面是一些补充的内容和纠正，现有的 evaluation 和 introduction 先不改了，但是请说明改进意见，方便下一轮完善这两个部分，这一轮以 title abstract method 和 conclusion 为主，
> 另外，对于 title，可以先给几个版本的候选，并给出每个版本 title 的推荐理由和具体说明，
> ultrathink，深入思考，深入分析，多想一会儿分析清楚，
> ==========================
> 补充一下关于 introduction 中现有方法的不足和 gap：对于 diversity，除了分析自动红队中 quality-diversity 和 RL-based diversity 的相关工作的局限性，额外提一下 TriPlay-RL 这篇论文，它在攻防协同建模中关注到了 diversity，但只是语义层面比较 superficial，不能带来攻击策略的提升；对于 replay，在现有的 opus 和 gpt 的分析中有误，样本的有害性/奖励也会在 replay 之后实时更新，但是依赖 judge 给出离散的 safety score 来更新样本后验风险，不够灵活，并且没有考虑 defender 的偶然性和动态性，（这两点这个是我们的 dace 框架需要解决并且可以解决的问题，所以建议额外说明一下，可以适当分析并润色）
> 在方法中注意说明二维攻击策略空间（risk category * attack style）的来源，其中 risk category 来自 llama-guard4 分类但调整删除了两个频率很低的类别，attack style 来自 RainbowTeaming 的分类，
> 实验表格先做好，但具体数据可以先留白，内容等评测完成再补上去，实验分析和结论先按照预期的理想情况来写，
> 鉴于文章篇幅和伪代码长度，考虑将本文 DACE 的伪代码放到附录，同时在方法中说明伪代码见附录xxx，

下面我先把"现在该写什么、为什么这么写"讲清楚，再给出具体内容。在内心先把每部分的可能写法过一遍，避开 MAGIC 已经覆盖的角度。最后把改进意见集中放在末尾。

---

## 一、整体写作哲学（先想清楚 DACE 的"identity"）

DACE 在 NeurIPS 投稿语境下要回答一个根本问题：**为什么社区需要在 MAGIC 之上再读一篇 LLM safety co-evolution 论文？** 答案必须在 title、abstract、method 和 conclusion 中保持一致：

> DACE 把"动态适应"推进为"持续覆盖与历史记忆共同驱动的安全演化"——通过显式策略空间上的归一化覆盖奖励解决 attack collapse，通过贝叶斯威胁度感知回放解决 defense forgetting，二者闭环互锁。

这一句话在四部分中的折射：

| 部分 | 应该传达的信息 |
|---|---|
| Title | "diversity-driven" + "co-evolution" + "LLM safety"，最好再点一个 technical hook |
| Abstract | 双 pathology → 三组件解决方案 → 实证亮点（4 句压缩） |
| Method | 把"为什么是归一化覆盖增益、为什么是贝叶斯而不是 UCB、为什么是 12×10"讲透；伪代码进附录 |
| Conclusion | 不只重述贡献，要回到 §1 提出的"持续演化"愿景，并指出 limitation + future work |

---

## 二、Title 候选（5 版 + 推荐理由）

### V1（推荐 ★★★★★，对标 MAGIC 命名风格）

> **DACE: Diversity-Driven Adversarial Co-Evolution for Robust LLM Safety Alignment**

- **优势**：与 MAGIC 同款"acronym + 核心机制 + 应用域"三段式（"DACE: ... for Robust LLM Safety Alignment"），形式上完美对仗 MAGIC ("MAGIC: A Co-Evolving Attacker–Defender Adversarial Game for Robust LLM Safety")，便于读者在引用列表中快速建立映射；
- **"Diversity-Driven"** 把 DACE 的核心 hook（vs MAGIC 的 "Co-Evolving"）放在最前面；
- **"Co-Evolution"** 而非 "Co-Evolutionary Game" / "Multi-Agent RL"——既覆盖 framing 又不冗长；
- **"Robust"** 与 MAGIC title 完全对齐，强化 "next step of MAGIC" 的定位；
- 长度 11 词，符合 NeurIPS title 习惯（10–14 词）。

### V2（推荐 ★★★★，强调技术 novelty）

> **DACE: Co-Evolving LLM Safety with Strategy-Space Coverage and Bayesian Adversarial Replay**

- **优势**：直接把两个技术贡献名字写进 title，对 reviewer 友好；
- **劣势**："Strategy-Space Coverage"和"Bayesian Adversarial Replay"两个长术语并列，读起来略重，超过 13 词；与 MAGIC 风格相比偏 method-heavy。

### V3（推荐 ★★★★，强调 conceptual shift）

> **From Adaptive to Comprehensive: Diversity-Driven Co-Evolution for LLM Safety Alignment**

- **优势**：用 "From X to Y" 的对照把 DACE 相对 MAGIC 的 conceptual leap 直接讲出来，narrative 感强；
- **劣势**：缺少 acronym，引用时不够 catchy；NeurIPS 中 "From X to Y" 风格的 title 偶尔被认为 cliché。

### V4（推荐 ★★★，emphasis on identity）

> **Beyond Reactive Patching: Diversity-Driven Adversarial Co-Evolution for LLM Safety**

- **优势**：开门见山指明 DACE 是要超越 reactive paradigm，主张性强；
- **劣势**："Beyond X"风格在近两年 NeurIPS 略有审美疲劳；与 MAGIC 风格不对仗。

### V5（recovery option，方法名更亲切）

> **DACE: Diversity-Aware Co-Evolution for Robust and Memory-Stable LLM Safety**

- **优势**：把 collapse + forgetting 双 pathology 直接折射在 "Robust and Memory-Stable" 中；
- **劣势**："Memory-Stable" 是新创术语，对读者首次阅读时不直观，可能需要在 abstract 中再解释一次。

**最终建议**：选 **V1**。它在引用一致性、长度控制、与 MAGIC 风格对照三方面都是最优。如果你担心 "Diversity-Driven" 听起来不够有 punch，可以在 abstract 第一句紧接着展开 "diversity here means structured coverage over a 12×10 strategy space, not surface-level textual variation"，把 V1 的简洁与 V2 的技术 specificity 在 abstract 里一并取得。

---

## 三、Abstract 写作思路与初稿

### 3.1 Abstract 怎么写

参考 MAGIC abstract（约 180 词）的结构，DACE abstract 应严格遵守：

| 句 | 功能 | 限制 |
|---|---|---|
| 1 | Big picture（safety alignment 落后于演化攻击） | 1 句 |
| 2 | 当前 co-evolution 范式的限制（双 pathology） | 1 句 |
| 3 | DACE 是什么（一句话主张） | 1 句 |
| 4-5 | 两个核心组件（覆盖奖励 + 贝叶斯回放） | 2 句 |
| 6 | We observe hook（multi-strategy combinatorial attacks） | 1 句 |
| 7 | 实验结论（量化领先） | 1 句 |
| 8 | Code release | 1 句 |

总长目标 180–230 词。下面是中文初稿对应的英文版（中英对照，便于你后续直接用英文版投稿）。

### 3.2 Abstract 中文初稿

> 大语言模型的广泛部署使其安全对齐成为核心问题，但主流静态对齐范式（RLHF、外部 guardrail、静态红队数据集）天然滞后于持续演化的越狱攻击。近期攻防协同演化（co-evolution）框架（如 MAGIC、Self-RedTeam）通过在线 RL 让攻击者与防御者动态共演化，向打破"反应式补丁"循环迈出了实质一步——但深入分析其训练动态，我们发现两个互锁的内生 pathology：**攻击策略坍缩**（attacker 在 RL 奖励下过拟合到少数高回报模式）与**防御对抗遗忘**（defender 在追逐当前攻击者时遗忘对早期攻击的鲁棒性），二者构成 in-distribution 训练指标虚高、真实 OOD 鲁棒性下降的恶性平衡。我们提出 ***DACE（Diversity-driven Adversarial Co-Evolution）***，一个将策略空间覆盖与历史威胁度感知回放系统性集成到 co-evolution 的 RL 框架。在攻击者侧，DACE 在显式 $12 \times 10$ 攻击策略空间（基于 Llama-Guard-4 风险分类与 Rainbow Teaming 攻击模式分类）上引入归一化边际覆盖增益奖励，从根源上消除原始熵增量奖励在长周期训练中的 $O(1/|\mathcal{A}|)$ 信号衰减；KL 散度视角下该奖励等价于单步 KL 收缩效率。在防御者侧，DACE 维护贝叶斯对抗回放池，通过 Beta-Bernoulli 后验追踪每个历史样本对当前 defender 的实时威胁度，Thompson Sampling 实现探索-利用平衡的回放采样，配合时间衰减处理 defender 能力漂移。我们观察到 DACE-attacker 在迭代 RL 中自发演化出 SFT 数据中不存在的多策略组合攻击。在 Qwen2.5-7B-Instruct 与 Llama3.1-8B-Instruct 两个 backbone 上的广泛评测显示，DACE 在 9 个安全基准与 OpenRT 协议下的 5 类 OOD 攻击（含最新 SOTA 黑盒攻击 MAJIC）上系统性优于 MAGIC，同时不损失通用能力。代码与回放池数据集见 https://github.com/[anon]/DACE。
>
> *Disclaimer: This paper contains potentially offensive and harmful text.*

### 3.3 Abstract 写作要点

- 不放具体数字（与 MAGIC 风格一致，把数字留给 introduction contribution 第 3 条）；
- "MAGIC、Self-RedTeam 取得实质进展"必须先说，再切到 "but 双 pathology"——避免被读为 "MAGIC 失败了所以我们提出 DACE"；
- "归一化"和"贝叶斯"必须在 abstract 中出现，让 reviewer 第一眼看到 technical novelty；
- "12×10 攻击策略空间（基于 Llama-Guard-4 + Rainbow Teaming）"在 abstract 中必须 cite 来源，避免被指为 ad-hoc——这是你新提的要求，必须遵守；
- "We observe..."hook 与 introduction §4 末尾一致，强化阅读节奏。

---

## 四、Method 章节写作思路与初稿

### 4.1 Method 怎么写

MAGIC 的 method 章节是 "Problem Formalization (§3) + Methods (§4)"两节。DACE 的篇幅约束与 MAGIC 相近，但因为 DACE 在策略空间设计、覆盖奖励的归一化推导、贝叶斯回放等细节上都有原创内容，建议以 4 节展开：

| § | 标题 | 核心内容 | 篇幅 |
|---|---|---|---|
| 3 | Problem Formalization | 形式化双人非对称序贯博弈 + 双 pathology 的形式化定义 | 0.5 页 |
| 4 | Method Overview | 训练流程（两阶段交替）+ Figure 2 框架图 | 0.5 页 |
| 5 | Attacker: Explicit Strategy Space + Coverage Reward | 12×10 策略空间来源 + 归一化覆盖奖励 + KL 视角理论支撑 | 1.0 页 |
| 6 | Defender: Bayesian Adversarial Replay | Beta-Bernoulli 后验 + Thompson 采样 + 时间衰减 + 剪枝 | 0.6 页 |
| 7 | Reward Design and Training Objective | 复合奖励 + GRPO 目标 + 算法（伪代码进附录） | 0.4 页 |

总篇幅约 3.0 页，与 MAGIC §3-§4 持平。下面给出每节的内容初稿。

### 4.2 § 3 Problem Formalization（约 220 字 + 公式）

> 沿用 MAGIC (Wen et al., 2026) 的非对称序贯博弈范式，我们将 LLM 安全对齐建模为攻击者 $\pi_A$ 与防御者 $\pi_D$ 之间的两人博弈。给定种子 prompt $x \in \mathcal{X}$，攻击者首先采样改写后的对抗 prompt $y_A \sim \pi_A(\cdot \mid x)$；防御者在观测到 $y_A$ 后采样响应 $y_D \sim \pi_D(\cdot \mid y_A)$。攻击者获得奖励 $r_A(y_A, y_D)$，防御者获得奖励 $r_D(y_A, y_D)$。MAGIC 已证明该博弈在 Subgame Perfect Nash Equilibrium 下取得点态安全保证（$r_D(y_A, y_D) \geq 0$ 对任意 $y_A$ 成立），DACE 直接继承这一安全保证作为方法的理论 backbone。
>
> 然而 SPNE 仅保证 *equilibrium 下* 安全，**不保证训练过程中策略空间被充分覆盖、历史攻击不被遗忘**。具体地，将 $y_A$ 的策略描述符记为 $b(y_A) = (s, c) \in \mathcal{B} = \mathcal{S} \times \mathcal{C}$（详见 §5.1），训练过程中 attacker 输出在 $\mathcal{B}$ 上的分布 $P_t(\cdot)$ 可能塌缩到一个低熵子集——即 *attack strategy collapse*：$H(P_t) \ll \log |\mathcal{B}|$。同时，记 $\mathcal{H}_t$ 为 t 时刻历史成功攻击的集合，defender $\pi_D^{(t)}$ 对 $\mathcal{H}_t$ 中样本的拒绝率 $\mathbb{E}_{x \in \mathcal{H}_t}[\text{refused}(x)]$ 可能随 t 增大而下降——即 *defense adversarial forgetting*。DACE 通过两个互补机制同时缓解二者，详述于 §5–§6。

### 4.3 § 4 Method Overview（约 200 字 + Figure 2 引用）

> Figure 2 给出 DACE 的整体框架。训练分为两个交替阶段，每轮迭代记为 round $k = 1, \ldots, K$。
>
> **Stage 1（Attacker Optimization）：** 冻结 defender $\pi_D^{(k-1)}$，采样种子 $x \sim \mathcal{D}_{\text{seed}}$；attacker 输出三段式响应 $\langle\text{think}\rangle\langle\text{strategy}\rangle\langle\text{answer}\rangle$，其中 $\langle\text{strategy}\rangle$ 显式给出 $(s, c) \in \mathcal{B}$，$\langle\text{answer}\rangle$ 给出改写 $y_A$。Defender 对每个 $y_A$ 生成响应 $y_D$，由 Qwen3Guard 打分 attack 是否成功。Attacker 通过 GRPO 在复合奖励 $R_A = R_{\text{effective}} + \lambda(x) \cdot R_{\text{coverage}}$ 上更新（详见 §5）。攻击成功的样本进入贝叶斯回放池 $\mathcal{A}$。
>
> **Stage 2（Defender Optimization）：** 冻结 attacker $\pi_A^{(k)}$，defender 训练 batch 由两部分构成：当前 attacker 生成的新攻击 $B_{\text{train}}$ 条 + 从 $\mathcal{A}$ 通过 Thompson Sampling 抽取的 $B_{\text{replay}}$ 条历史攻击。Defender 通过 GRPO 在 $R_D = R_{\text{harm}} + R_{\text{ref}}$ 上更新（沿用 MAGIC 设计）；回放样本的响应结果用于更新其 Beta-Bernoulli 后验（详见 §6）。
>
> 完整算法见 Appendix A.

### 4.4 § 5 Attacker: Explicit Strategy Space and Coverage Reward（约 1.0 页）

#### § 5.1 12×10 攻击策略空间（约 220 字）

> 我们定义攻击策略空间 $\mathcal{B} = \mathcal{S} \times \mathcal{C}$，其中 $\mathcal{S}$ 为风险类别集合，$\mathcal{C}$ 为攻击模式集合。
>
> **$\mathcal{S}$ 的来源**：基于 Llama-Guard-4 (Llama Team, 2025) 的 14 类风险分类，我们移除两个低频且与 text-only defender 设定不匹配的类别——*Sexual Content*（在 SFT 蒸馏数据中占比 0.80%、benign refusal rate 96.3%）和 *Code Interpreter Abuse*（占比 0.11%，假设了工具调用接口）——保留剩余 12 类（Violent Crimes, Non-Violent Crimes, Sex-Related Crimes, Child Sexual Exploitation, Defamation, Specialized Advice, Privacy, Intellectual Property, Indiscriminate Weapons, Hate, Suicide & Self-Harm, Elections）。**$\mathcal{C}$ 的来源**：沿用 Rainbow Teaming (Samvelyan et al., 2024) 的 10 类攻击模式（Slang, Technical Terms, Role Play, Authority Manipulation, Misspellings, Word Play, Emotional Manipulation, Hypotheticals, Historical Scenario, Uncommon Dialects）。最终 $|\mathcal{B}| = 120$。
>
> Attacker 在每次改写前显式选择 $(s, c)$，将原本隐式的策略选择提升为可观测、可奖励的离散动作。我们通过 Gemini-2.5-Pro 蒸馏 ~43k 条带 $\langle\text{think}\rangle\langle\text{strategy}\rangle\langle\text{answer}\rangle$ 三段式 CoT 的 SFT 数据进行暖启动，赋予 attacker 策略推理能力，避免直接从 base instruct 模型起步导致的策略空间利用不充分。

#### § 5.2 Normalized Marginal Coverage Gain（约 280 字）

> **原始定义及其局限。** 自然的覆盖度奖励是边际 Shannon 熵增量：
>
> $$
R_{\text{coverage}}^{\text{raw}}(x) = H(P_{\mathcal{A} \cup \{x\}}) - H(P_{\mathcal{A}})
$$
>
> 其中 $P_{\mathcal{A}}$ 为档案池上策略分布的归一化频率。然而当 $|\mathcal{A}|$ 增大时，加入单个样本对分布的扰动为 $O(1/|\mathcal{A}|)$，对应熵增量也是 $O(1/|\mathcal{A}|)$，导致训练后期奖励信号持续衰减直至消失（**reward vanishing**）。
>
> **归一化设计。** 我们以当前 $\mathcal{A}$ 状态下单个样本可达到的最大熵增量作为归一化基准：
>
> $$
R_{\text{coverage}}(x) = \frac{H(P_{\mathcal{A} \cup \{x\}}) - H(P_{\mathcal{A}})}{\max_{b \in \mathcal{B}} \left[H(P_{\mathcal{A} \cup \{x_b\}}) - H(P_{\mathcal{A}})\right] + \epsilon}
$$
>
> 其中 $x_b$ 为一个落入槽位 $b$ 的假想样本。分子分母同为 $O(1/|\mathcal{A}|)$ 量级且同速衰减，比值始终保持 $O(1)$，**从根本上消除信号衰减**。落入当前最低频槽位的样本得分为 1，落入饱和槽位的样本得分接近 0，区分度在全训练周期内稳定。
>
> **计算复杂度**：$O(|\mathcal{B}|)$，且分母仅依赖 $\mathcal{A}$ 状态，同一 batch 内所有样本共享同一分母，每步只需计算一次。

#### § 5.3 KL Divergence Perspective（约 160 字）

> 利用 $H(P) = \log |\mathcal{B}| - D_{\text{KL}}(P \| U)$（$U$ 为 $\mathcal{B}$ 上均匀分布），边际熵增量等价改写为：
>
> $$
H(P_{\mathcal{A} \cup \{x\}}) - H(P_{\mathcal{A}}) = D_{\text{KL}}(P_{\mathcal{A}} \| U) - D_{\text{KL}}(P_{\mathcal{A} \cup \{x\}} \| U)
$$
>
> 即归一化覆盖增益等价于**单步 KL 收缩效率**——该样本使策略分布向均匀分布收缩的实际 KL 减少量，占单步最优 KL 减少量的比例。该视角提供两个理论支撑：(i) **梯度方向**：$\partial D_{\text{KL}}(P \| U) / \partial p_b = 1 + \log p_b - \log u_b$，$p_b$ 越小（越低频槽位）梯度越大，沿该方向更新带来的 KL 下降越大；(ii) **Zero-avoiding 特性**：前向 KL 在 $p_b \to 0$ 时趋于极大值，意味着归一化覆盖增益天然对空白槽位施加最强探索驱动，与"避免任何策略区域被遗漏"目标在理论上一致。

#### § 5.4 Differentiated Diversity Coefficient（约 130 字）

> 攻击者总奖励为 $R_A(x) = R_{\text{effective}}(x) + \lambda(x) \cdot R_{\text{coverage}}(x)$，其中差异化系数：
>
> $$
\lambda(x) = \begin{cases} \lambda_{\text{succ}} = 1.0 & \text{if attack succeeds} \\ \lambda_{\text{fail}} = 0.5 & \text{otherwise} \end{cases}
$$
>
> 设计动机：$\lambda_{\text{fail}} = 0$ 会让冷门策略一旦未学会有效攻击，探索梯度立即消失；保留折减奖励 $\lambda_{\text{fail}} = 0.5$ 在不过度激励无效攻击的前提下，为冷门策略方向维持基本探索压力。$\lambda_{\text{succ}} = 2 \lambda_{\text{fail}}$ 的比例确保 GRPO group 内 advantage 计算优先强化"既有效又新颖"的攻击。

### 4.5 § 6 Defender: Bayesian Adversarial Replay（约 0.6 页）

#### § 6.1 统一档案池设计（约 100 字）

> 档案池 $\mathcal{A}$ 同时承担两项功能：(i) 策略频次记录（用于 §5 的覆盖奖励计算），(ii) 对抗回放（用于 defender 训练混合 batch）。每轮攻防交互后，攻击成功的样本 $x$ 连同其策略描述符 $b(x)$ 加入 $\mathcal{A}$；池中每个样本 $x_i$ 维护成功次数 $s_i$ 与失败次数 $f_i$（在回放训练中累积）。

#### § 6.2 Beta-Bernoulli 后验追踪（约 200 字）

> 假设每次攻击成败服从伯努利分布，取共轭 Beta 先验 $\alpha = \beta = 1$（均匀先验），则后验为：
>
> $$
p_i \mid s_i, f_i \sim \text{Beta}(\alpha + s_i, \beta + f_i)
$$
>
> 后验均值 $\hat{p}_i = (\alpha + s_i)/(\alpha + \beta + s_i + f_i)$ 给出当前威胁度的点估计；后验方差则反映估计的不确定性，**实验次数越多方差越小，对 $\hat{p}_i$ 估计越有信心**。这一设计相对 SSP (Wang et al., 2026) 基于离散奖励高低的 UCB 优先级有三个结构性优势：(1) **抗偶然误判**——后验均值综合所有历史试验，单次防御成功不会导致样本被过早淘汰；(2) **不确定性建模**——后验方差天然区分"被反复验证为低威胁"与"试验次数少威胁度未知"两类样本；(3) **支持原则化采样**——后验分布同时支持 Thompson Sampling 等内建探索-利用平衡机制，无需额外调参。

#### § 6.3 时间衰减与 Thompson 采样（约 180 字）

> **时间衰减处理非平稳性**：defender 持续训练时其能力会漂移，历史样本的实时威胁度随之变化。每轮训练开始时对所有样本执行：$s_i \leftarrow \gamma s_i, f_i \leftarrow \gamma f_i$（$\gamma \in [0.9, 0.99]$）。该衰减将后验缓慢"遗忘"回先验，使 $\hat{p}_i$ 自然跟踪 defender 能力的演化，避免历史记录与当前状态相互"污染"。
>
> **Thompson 采样采样回放 batch**：每次 defender 训练 batch 中需从 $\mathcal{A}$ 抽取 $B_{\text{replay}}$ 个回放样本时：(1) 对每个 $x_i$ 从其后验抽样 $\tilde{p}_i \sim \text{Beta}(\alpha + s_i, \beta + f_i)$；(2) 按 $\tilde{p}_i$ 降序取前 $B_{\text{replay}}$。**后验均值高且方差小的样本（多次验证确实危险）大概率抽到高 $\tilde{p}_i$——利用；试验次数少、方差大的样本也有机会恰好抽到高值——探索**。这一探索-利用平衡通过后验采样自然实现，**无需额外调参**。

#### § 6.4 剪枝策略（约 80 字）

> 移除后验均值极低且已被充分测试的样本：
>
> $$
\text{remove } x_i \quad \text{if } \hat{p}_i < \epsilon \text{ and } (s_i + f_i) > n_{\min}
$$
>
> 仅当样本被充分测试（试验次数超过阈值）**且**威胁度估计极低时，才确信其已无威胁价值。高不确定性的样本（试验次数少）不会被过早剪枝。

### 4.6 § 7 Reward Design and Training Objective（约 0.4 页）

#### § 7.1 复合奖励设计（约 130 字）

> 沿用 MAGIC 的奖励结构，attacker 与 defender 的总奖励分别为：
>
> $$
R_D = R_{\text{harm}}(y_D) + R_{\text{ref}}(y_D), \quad R_A = R_{\text{effective}}(x) + \lambda(x) R_{\text{coverage}}(x) + R_{\text{fmt}}(y_A)
$$
>
> 其中 $R_{\text{harm}}$ 基于 Qwen3Guard 判定（unsafe/controversial 计 $-r_{\text{harm}}$，safe 计 $+r_{\text{harm}}$），$R_{\text{ref}}$ 防止 over-refusal 坍缩，$R_{\text{fmt}}$ 强制 attacker 三段式格式。$R_{\text{effective}} = -R_D$ 体现攻防零和性质。

#### § 7.2 GRPO 训练目标（约 100 字）

> 我们用 Group Relative Policy Optimization (Guo et al., 2025) 训练，每个样本的 advantage 通过组内归一化得到：
>
> $$
A_i = \frac{r_i - \text{mean}(\{r_1, \ldots, r_G\})}{\text{std}(\{r_1, \ldots, r_G\})}
$$
>
> 完整 surrogate loss 与 KL 约束沿用标准 GRPO 形式（细节见 Appendix A）。

#### § 7.3 算法（一句话指引）

> DACE 完整训练算法（含两阶段 GRPO 更新、贝叶斯后验更新、Thompson 采样、时间衰减与剪枝调用）见 **Appendix A**（伪代码与超参数说明）。

### 4.7 Method 章节的几个关键写作决策

1. **§5 占整章一半篇幅，且最 detail-heavy**——这是 DACE 的主要 technical novelty 所在，必须给足空间；而 §6 的贝叶斯回放虽然也是 novelty，但数学上是经典 Beta-Bernoulli + Thompson Sampling，不需要从头推导。
2. **§5.3 KL Perspective 单独成节而非埋在 §5.2**——MAGIC 在 §3.2 给出 SPNE 的 stronger pointwise safety guarantee 时也是单独成节，这种 theoretical depth 段落能显著提升 NeurIPS reviewer 评分。
3. **伪代码进 Appendix A**——MAGIC 的 Algorithm 1（约 1/3 页）放在主文 §4 末尾，但 DACE 因 §5–§6 篇幅扩展，主文已紧张，伪代码进附录更稳妥。
4. **§7.1 复合奖励刻意写得简短**——重复 MAGIC §4.2 已有的部分越短越好，避免"自抄 MAGIC"质疑；只在 $R_{\text{coverage}}$ 处展开。
5. **没有"Comparison with Related Methods"**——这部分在 introduction §3 已经讨论过，method 章节不重复，避免冗余。

---

## 五、Conclusion 章节写作思路与初稿

### 5.1 Conclusion 怎么写

参考 MAGIC §6 conclusion（约 180 词，1 个段落），DACE conclusion 应包含：

| 句 | 功能 |
|---|---|
| 1 | 重述 DACE 是什么（一句话主张） |
| 2-3 | 重述两个核心贡献（覆盖奖励 + 贝叶斯回放） |
| 4 | 实证总结（一句话） |
| 5-6 | Limitations |
| 7 | Future work + 愿景 |

总长目标 200–250 词。**避免重复 introduction 已说过的话**——conclusion 的角色是 reflect 而非 announce。

### 5.2 Conclusion 中文初稿

> 在本文中，我们提出 DACE，一个将策略空间多样性与历史威胁度感知回放系统性集成到 LLM 安全协同演化的 RL 框架。通过显式 $12 \times 10$ 攻击策略空间上的归一化边际覆盖增益奖励，DACE 从根源上消除原始熵增量奖励的 reward vanishing 问题，并提供单步 KL 收缩效率的理论可解释性；通过贝叶斯对抗回放池追踪每个历史样本对当前 defender 的实时威胁度，DACE 在原则化的探索-利用平衡下解决防御对抗遗忘。我们的理论分析与广泛实证支持核心论点：**协同演化中的安全鲁棒性应被视为对策略空间的覆盖问题与对历史漏洞的记忆问题的联合优化**，而非单纯对当前对手的最优响应。
>
> 本工作存在若干 limitation。首先，DACE 的策略空间是基于 Llama-Guard-4 与 Rainbow Teaming 的离散分类构造，无法处理跨类别的细粒度风险（如同时涉及 hate 与 specialized advice 的攻击）；其次，attacker 的多策略组合涌现高度依赖 SFT 暖启动质量，base 模型直接 RL 时性能下降明显；最后，本工作仅在 text-only 单轮设定下验证，多模态与长程 agentic 场景下的 co-evolution 仍是开放问题。
>
> Future work 包括：将策略空间从离散网格推广到连续语义嵌入；将贝叶斯回放扩展为 lifelong adversarial memory，支持跨多个 RL 训练 run 的持久化；以及探索 DACE 与 inference-time safety reasoning（如 Reasoned Safety Alignment）的正交结合。我们希望本工作能推动社区将"安全对齐作为持续演化过程"视为 LLM safety 的下一阶段范式。

### 5.3 Conclusion 写作要点

- **Limitation 必须诚实**——MAGIC §6 也明确指出 "the attacker's exploration is highly sensitive to the SFT initialization"，DACE 应该同样诚实承认这一点；
- **Future work 三条**——分别对应方法层面（连续策略空间）、系统层面（lifelong memory）、范式层面（与 reasoning 结合），avoiding 全部 future work 都堆在一个方向；
- **末句"安全对齐作为持续演化过程"** 与 MAGIC §6 末尾"safety alignment as a evolving process"对仗呼应，形成与 MAGIC 的 conceptual lineage。

---

## 六、对此前 Evaluation 与 Introduction 的改进意见（下一轮处理）

### 6.1 Evaluation 改进点

1. **Tab 4 (Attacker effectiveness) 的"on-rewrite vs replay-buffer"两行**：你之前提到要看 replay buffer 作为攻击库的有效性，建议在 Tab 4 加一列 **"Attack Space Distribution Coverage"**，显示该 attacker 在 12×10 grid 上的占用 cell 数——这能让 Tab 4 同时讲 effectiveness + diversity 两个故事，避免再单独做 Tab 5。
2. **Fig 4 attack space heatmap**：根据你最新要求"统计 attack on-rewrite/replay buffer 在 attack space 的分布"，建议把 Fig 4 改为 $2 \times 2$ 子图：(a) MAGIC on-rewrite, (b) DACE on-rewrite, (c) DACE replay buffer (frequency), (d) DACE replay buffer (per-cell ASR)——比原 $1 \times 3$ 设计更全面。
3. **Tab 6 ablation 第 2 行"w/o SFT training"** 的 baseline 选择：上一轮我建议用 base Qwen2.5-7B-IT，但根据 v3 debug log2/log3 的实际证据，base 起步会遭遇严重的 strategy 提取失败问题。建议在 Tab 6 中用 **"MAGIC-SFT attacker（即 MAGIC 自己的 SFT 暖启动）"** 作为 w/o DACE-SFT 的对照，这样消融的就是"DACE 蒸馏 prompt 设计"而非"是否有 SFT"，结论更 actionable。
4. **MAJIC 集成方式**：上一轮已说明，但 v4 阶段未确认是否进入 OpenRT。建议在 evaluation 章节明确写一段"OpenRT extension"，说明如何把 MAJIC 的 Markov chain 接入 OpenRT 的 attacker 接口——这能让 Tab 3 的 MAJIC 列站住脚。

### 6.2 Introduction 改进点（结合你本轮新提的"TriPlay-RL + 离散 safety score 不灵活"）

1. **§3 现有 RL diversity 部分**：在 CRT、DiveR-CT、GFlowNet 红队之后，加一句 **TriPlay-RL (作者, 2026) 在 attacker-defender-judge 三方 self-play 中引入 attacker semantic diversity，但其多样性度量仍停留在 sentence-level 嵌入距离，无法识别策略层"换皮不换招"的伪多样性**。这一句让 §3 多样性方法的 case 覆盖更全。

2. **§3 现有 replay 部分**：把"SSP 的优先级仅基于历史奖励"这句修正为**"现有 replay 机制（如 SSP、CRT 经验回放）的样本优先级依赖 judge 给出的离散 safety score 实时更新，但离散 score 缺乏对 defender 偶然性（同一样本不同 rollout 结果不一致）与动态性（defender 能力随训练漂移）的建模——一个早期被某次 rollout 突破的样本，可能因 judge 的离散评分浮动被反复回放或过早淘汰"**。这一段定位更准确，把"为什么需要贝叶斯后验 + 时间衰减"的 motivation 直接植入 §3。

3. **§4 三组件介绍中**：在介绍贝叶斯回放时，建议添加一句 **"相对现有 replay 机制依赖离散 safety score 更新，DACE 的 Beta-Bernoulli 后验自然将 defender 偶然性建模为后验方差、将能力漂移建模为时间衰减，提供原则化的不确定性量化"**——直接呼应 §3 的 motivation。

4. **Figure 1 设计微调**：(a) 子图加上 "MAGIC attacker 频率塌缩到 5/120 cells" 的具体注解；(b) 子图加上 "early-iter attacks ASR rebound under SSP-style replay" 的注解，让 Fig 1 既视觉直观又有 quantitative 锚点。

---

## 七、最后几个待你拍板的细节

1. **Title V1 vs V2**：是 catchy 优先（V1）还是 technical specificity 优先（V2）？我推荐 V1，但 V2 在 reviewer 第一眼看到时更能传达 "本文有真技术贡献"。
2. **Abstract 是否包含 GitHub URL**：MAGIC abstract 末尾给了代码链接，DACE 是否同样给？注意盲审时需要 anonymize。
3. **§5.3 KL 视角是否上 NeurIPS 主文**：这是相对小众但漂亮的理论分析，能让 reviewer 觉得"作者懂 information theory"。如果空间紧可放 Appendix，但建议主文保留——它是 differentiation 之一。
4. **Method §6 中是否对比 SSP 的 UCB priority**：上面我在 §6.2 加了一句对比，但有人会觉得 method 章节不应做 related work。如果改为 "introduction §3 已说明，method §6 不重复"，可以删掉；如果想强化 differentiation，保留即可。我建议**保留**——method 章节里讲清楚"为什么是贝叶斯不是 UCB"是核心 selling point。
5. **Limitations 措辞**：当前 conclusion 里 limitation 写得相对直接。是否要软化为 "we leave to future work" 风格？NeurIPS 通常欢迎诚实的 limitation 列表（甚至有 ethics/limitation section），建议保持当前的诚实直接风格。

---

如果你确认这一轮 OK，下一轮我可以：(a) 把 introduction §3 / §4 按本节 6.2 的改进意见重写并与本轮 method 衔接；或者 (b) 把 abstract / method / conclusion 全部翻译为正式英文版本，控制总篇幅在 5–6 页 NeurIPS 排版。你想先推进哪个？

-----

> 在这些材料和分析的基础上，再写一下 related work 和 appendix 部分，附录可以先参考 maigc 论文来写，其他要求与之前的一样

下面我先讲清楚 related work 和 appendix 的写作哲学（DACE 的特殊定位决定了这两部分要怎么取舍），再给出具体内容。

---

## 一、Related Work 写作思路

### 1.1 整体哲学

DACE 的 related work 必须**避免成为 "introduction §3 的扩展版"**——MAGIC 的 §2 只用了 1 页，分两个子节（"LLM Jailbreaking" + "LLM Safety Alignment and Multi-Agent Games"），DACE 应同样紧凑。但 DACE 的 conceptual lineage 比 MAGIC 复杂——既继承 MAGIC 的 co-evolution，又借鉴 Quality-Diversity 的 archive 思想，又引入持续学习的 replay 概念——所以分类必须比 MAGIC 更细。

我建议**3 个子节**：

| § | 标题 | 核心信息 | 篇幅 |
|---|---|---|---|
| 2.1 | Adversarial Attacks and Static Safety Alignment | 攻击演化谱系（cite MAGIC §2.1） + 静态对齐的局限 | 0.4 页 |
| 2.2 | Co-Evolutionary Safety Alignment | MAGIC、Self-RedTeam、ACE-Safety、PIA、TriPlay-RL 等 + 它们的 diversity / replay 不足 | 0.4 页 |
| 2.3 | Diversity in Automated Red-Teaming | Quality-Diversity (Rainbow/QDRT) + RL diversity (CRT/DiveR-CT/GFlowNet) + 它们都不在 co-evolution | 0.3 页 |

### 1.2 写作上的几个关键决策

1. **不重复 introduction §3 的具体批判**——related work 应"陈述已有工作的方法本质"，introduction §3 才是"指出它们为什么不够"。两处避免重复 wording。
2. **§2.1 篇幅最大但密度最高**——把 MAGIC §2.1 的攻击演化清单浓缩为一段，留出空间专门讨论 RLHF / safety RLVR / guardrail 等静态对齐范式的局限——这是 introduction §1 的延伸，把"为什么需要 dynamic"讲深。
3. **§2.2 必须把 PIA 与 TriPlay-RL 区分对待**：PIA 是 ICML 2026 持续投稿，与 DACE 同期；TriPlay-RL 是 arXiv 2601 但已可引用。两者代表了 "MAGIC 之后" 的两个不同改进方向（persona-invariant vs. tri-role），DACE 的 differentiation 要明示。
4. **§2.3 不展开技术细节**——把 Rainbow / QDRT / CRT / DiveR-CT / GFlowNet 红队作为一个聚类提及，重点是"它们都把 attacker 当作离线优化器，不参与 co-evolution"。
5. **加一句 continual learning 与 experience replay 的桥接**——DACE 的贝叶斯回放本质上是 continual learning 的 replay 思路在 adversarial 设定下的特化。这种跨域 connection 能显著提升 reviewer 的 perceived contribution。

### 1.3 Related Work 中文初稿

#### § 2 Related Work（开头一句）

> 我们将 DACE 置于三条研究主线的交汇处：演化中的对抗攻击与静态安全对齐的张力 (§2.1)、攻防协同演化范式 (§2.2)、以及自动化红队中的多样性研究 (§2.3)。

#### § 2.1 Adversarial Attacks and Static Safety Alignment（约 320 字）

> **Adversarial attacks against aligned LLMs.** LLM 越狱攻击的演化呈现清晰的复杂度递增谱系：早期人工 jailbreak 模板（DAN (Shen et al., 2023)、ASCII art (Jiang et al., 2024a)、低资源语言翻译 (Yong et al., 2023)）→ 自动化对抗优化（GCG (Zou et al., 2023) 及其改进 (Jia et al., 2024; Liao & Sun, 2024)、PAIR (Chao et al., 2023)、TAP (Mehrotra et al., 2024)、AutoDAN (Liu et al., 2023, 2024a)）→ 隐蔽组合攻击（FlipAttack (Liu et al., 2024c)、scenario shifting (Wu et al., 2025)、persona modulation (Shah et al., 2023)、many-shot jailbreak (Anil et al., 2024)）→ 多轮代理化攻击 (X-Teaming (Rahman et al., 2025)) → 最新的 Markov 链组合攻击 (MAJIC (Qi et al., 2025)，在 GPT-4o 上 ASR 超过 90%)。这一谱系揭示了攻击者策略空间的指数级扩张趋势。
>
> **Static safety alignment.** 主流对齐范式包括 RLHF (Ouyang et al., 2022)、Safe RLHF (Dai et al., 2023)、Constitutional AI (Bai et al., 2022)、外部 guardrail 模型 (Llama Guard (Inan et al., 2023)、WildGuard (Han et al., 2024)、Qwen3Guard (Zhao et al., 2025)、ShieldAgent (Chen et al., 2025))，以及 inference-time 防御（SmoothLLM (Robey et al., 2023)、Self-Eval (Phute et al., 2023)、Reasoned Safety Alignment (Liu et al., 2025c)）。然而这些方法都依赖**预先收集的对抗分布**——一旦攻击者发现 OOD 模式，静态对齐立即失效 (Wei et al., 2023; Ren et al., 2025)。这种范式与攻击演化速度的根本性不对称促使社区转向动态对抗训练。

#### § 2.2 Co-Evolutionary Safety Alignment（约 300 字）

> 早期工作通过迭代红队 + 离线对齐近似 co-evolution：MART (Ge et al., 2024)、PAT (Mo et al., 2024)、RPO (Zhou et al., 2024) 在每轮训练中部分固定攻击者，未达到真正在线协同。MTSA (Guo et al., 2025) 引入多轮安全对齐但仅针对 multi-turn jailbreak。
>
> **Online co-evolution** 由 Self-RedTeam (Liu et al., 2025) 与 MAGIC (Wen et al., 2026) 系统性奠基：前者通过 zero-sum self-play 在共享参数下取得 Nash 均衡安全保证；后者通过非对称序贯博弈与参数解耦取得 Subgame Perfect Nash Equilibrium 的点态保证。其后续工作沿不同方向延伸：ACE-Safety (Li et al., 2025) 将 GS-MCTS 与课程 RL 结合；AdvEvo-MARL (Pan et al., 2025) 拓展到多智能体设定；AdvGame (Paulus et al., 2025) 用非合作博弈论形式化；Alignment Waltz (Lin et al., 2025) 引入协作训练；PIA (Li et al., 2026) 关注 persona-invariant safety；TriPlay-RL (作者, 2026) 引入 attacker-defender-judge 三方 self-play。
>
> 然而这些工作都未系统性处理两个 co-evolution 内生的训练 pathology：**attack strategy collapse** 在所有上述工作中均未引入显式策略层多样性奖励——TriPlay-RL 是其中最接近的，但其多样性度量停留在 sentence-level 嵌入距离，无法识别策略层"换皮不换招"；**defense adversarial forgetting** 在所有上述工作中亦未配套 principled replay 机制——SSP (Wang et al., 2026) 是少数引入 experience replay 的，但其优先级基于历史奖励，依赖 judge 离散 safety score 实时更新，未对 defender 偶然性与动态性建模。DACE 的设计正面针对这两个 gap。

#### § 2.3 Diversity in Automated Red-Teaming（约 240 字）

> **Quality-Diversity 离线搜索**：Rainbow Teaming (Samvelyan et al., 2024) 首次将红队建模为 MAP-Elites 在 risk × style 行为空间上的 archive 搜索；Ruby Teaming (Jiang et al., 2024b) 加入记忆缓存维度；Ferret (Pala et al., 2025)、RainbowPlus (Hoang et al., 2025) 与 QDRT (Wang et al., 2025) 进一步增强变异质量与多 attacker 模型设计。这类方法以**静态 target LLM** 为目标做 prompt 进化，不参与攻防协同训练。
>
> **RL-based diversity rewards**：CRT (Hong et al., 2024) 引入新颖性奖励；DiveR-CT (Zhao et al., 2024) 用 k-NN 距离与放松约束；GFlowNet 红队 (Lee et al., 2024) 用摊销推断采样多模分布；CALM (Yu et al., 2025) 引入 token 稀疏性；Jailbreak-R1 (Wang et al., 2025) 用 GRPO 组相对多样性。这些方法依赖词频、嵌入距离等表层指标，**无法识别策略层差异**。
>
> **Continual learning 与 experience replay**：经验回放是缓解灾难性遗忘的经典思路 (Lin, 1992; Robins, 1995)，近期在 LLM continual fine-tuning 中重新受到关注 (Du et al., 2024; FOREVER (Liu et al., 2026))。DACE 的贝叶斯回放可视为这一思路在对抗安全训练下的特化——通过 Beta-Bernoulli 后验对 defender 非平稳性建模。

---

## 二、Appendix 写作思路

### 2.1 整体哲学

参考 MAGIC 的 9 个 appendix（A. Proof + B. Prompts + C. Setup + D. Eval + E. Transferability + F. Attack Patterns + G. Ablations）共约 22 页。DACE 因有原创 archive pool 实现、新的 attack space 设计、独有的贝叶斯后验更新等额外细节，appendix 篇幅会略大，但结构应保持类似。

我建议 **9 个 appendix 子节**：

| § | 标题 | 内容 | 篇幅 |
|---|---|---|---|
| A | Algorithm Pseudocode | DACE 完整训练算法（attacker stage + defender stage + posterior update + 时间衰减 + 剪枝） | 1.5 页 |
| B | Strategy Space Design Rationale | 12×10 决策依据 + 删除 S12/S14 的数据证据 + 攻击模式分类来源 | 1.5 页 |
| C | Prompt Templates | CoT distillation prompt + attacker prompt + defender prompt + safety judge prompt | 2.0 页 |
| D | Experimental Setup Details | 训练超参 + GRPO 配置 + 数据集构建 + baseline 实现细节 | 1.5 页 |
| E | Evaluation Benchmarks | 9 个 safety benchmark + 5 个通用能力 benchmark + OpenRT 配置 + MAJIC 集成 | 1.5 页 |
| F | Expanded Results | Llama3.1-8B / Qwen2.5-14B 的完整 Tab 1–5；多 backbone 验证 | 2.0 页 |
| G | Co-Evolution Training Dynamics | Pool 流动性曲线 + Coverage entropy 演化 + Reward signal 稳定性 + Anti-forgetting 深度对比 | 1.5 页 |
| H | Attack Pattern Analysis | DACE 涌现的多策略组合攻击分类 + 案例研究（沿用 MAGIC §F 风格） | 2.0 页 |
| I | Replay Buffer as Jailbreak Dataset | 把 DACE 最终 ~4000 条 replay pool 作为独立 jailbreak benchmark 横评 closed-source models | 1.0 页 |

总附录约 14 页，合理范围（NeurIPS 上限通常无硬限制，但建议 ≤ 20 页）。

### 2.2 各 appendix 内容初稿

#### Appendix A: Algorithm Pseudocode（1.5 页）

**写作目标**：完整、自包含的伪代码，让 reviewer 可以独立 reproduce。沿用 MAGIC Algorithm 1 的"输入-阶段-子流程"格式。

**内容草拟**：

> **Algorithm 1**: DACE Training Algorithm
> **Require**: Initial attacker $\pi_A$, defender $\pi_D$, Strategy space $\mathcal{B} = \mathcal{S} \times \mathcal{C}$ with $|\mathcal{B}| = 120$, Seed dataset $\mathcal{D}_{\text{seed}}$, Rounds $K$, Steps per stage $T$, GRPO group size $G$, Replay parameters ($\gamma, \alpha, \beta, \epsilon, n_{\min}, B_{\text{train}}, B_{\text{replay}}$)
>
> 1: **Phase 1: SFT Warm-Start**
> 2: $\pi_A \leftarrow \text{SFT}(\pi_A, \mathcal{D}_{\text{sft}})$ on Gemini-distilled 12×10 strategy CoT data
> 3: Initialize archive pool $\mathcal{A} \leftarrow \emptyset$, strategy frequency counts $N_b \leftarrow 0$ for all $b \in \mathcal{B}$
> 4: **Phase 2: Co-Evolution**
> 5: **for** $k = 1$ to $K$ **do**
> 6: &nbsp;&nbsp;&nbsp; **# Stage 1: Attacker Optimization (fix $\pi_D$)**
> 7: &nbsp;&nbsp;&nbsp; **for** $t = 1$ to $T$ **do**
> 8: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Sample seed batch $\{x_i\}_{i=1}^{B} \sim \mathcal{D}_{\text{seed}}$
> 9: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **for each** $x_i$ **do**
> 10: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Attacker generates $G$ candidates $\{(b_i^{(g)}, y_A^{(g)})\}_{g=1}^G \sim \pi_A(\cdot \mid x_i)$
> 11: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Defender responds $y_D^{(g)} \sim \pi_D(\cdot \mid y_A^{(g)})$ for each $g$
> 12: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Compute $R_{\text{effective}}^{(g)}, R_{\text{coverage}}^{(g)}, R_{\text{fmt}}^{(g)}$  // see §5–§7
> 13: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $R_A^{(g)} \leftarrow R_{\text{effective}}^{(g)} + \lambda(g) R_{\text{coverage}}^{(g)} + R_{\text{fmt}}^{(g)}$
> 14: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **end for**
> 15: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Update $\pi_A$ via GRPO using group advantages
> 16: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **for each** successful attack $(x, b, y_A)$ **do**
> 17: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **if** $y_A \notin \mathcal{A}$ **then** add $(y_A, b, s=1, f=0)$ to $\mathcal{A}$; $N_b \mathrel{+}= 1$
> 18: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **end for**
> 19: &nbsp;&nbsp;&nbsp; **end for**
> 20: &nbsp;&nbsp;&nbsp; **# Round transition: time decay + prune**
> 21: &nbsp;&nbsp;&nbsp; **for each** $x_i \in \mathcal{A}$ **do** $s_i \leftarrow \gamma s_i, f_i \leftarrow \gamma f_i$
> 22: &nbsp;&nbsp;&nbsp; Remove $x_i$ from $\mathcal{A}$ if $\hat{p}_i < \epsilon \wedge (s_i + f_i) > n_{\min}$
> 23: &nbsp;&nbsp;&nbsp; **# Stage 2: Defender Optimization (fix $\pi_A$)**
> 24: &nbsp;&nbsp;&nbsp; **for** $t = 1$ to $T$ **do**
> 25: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Sample seed batch $\{x_i\}_{i=1}^{B_{\text{train}}} \sim \mathcal{D}_{\text{seed}}$
> 26: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Generate new attacks via $\pi_A$  // $B_{\text{train}}$ samples
> 27: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **# Thompson Sampling from archive**
> 28: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **for each** $x_i \in \mathcal{A}$ **do** $\tilde{p}_i \sim \text{Beta}(\alpha + s_i, \beta + f_i)$
> 29: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Take top $B_{\text{replay}}$ samples by $\tilde{p}_i$ → replay batch
> 30: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Mixed batch $=$ new attacks $\cup$ replay batch
> 31: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Defender generates $G$ responses per sample, computes $R_D$
> 32: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Update $\pi_D$ via GRPO
> 33: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **for each** replay sample $x_i$ **do**
> 34: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **if** any of $G$ responses unsafe **then** $s_i \mathrel{+}= 1$ **else** $f_i \mathrel{+}= 1$
> 35: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **end for**
> 36: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **# Add new successful attacks to archive (mirroring Stage 1)**
> 37: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ...
> 38: &nbsp;&nbsp;&nbsp; **end for**
> 39: **end for**
> 40: **return** $\pi_A, \pi_D, \mathcal{A}$

伪代码后紧跟一个 0.3 页的 **超参表**（沿用 MAGIC Tab 6 风格）：

> **Table A.1**: Hyperparameters for DACE training. Values follow MAGIC defaults unless noted.
>
> | Setting | Value |
> |---|---|
> | Training order | Attacker → Defender |
> | Rounds $K$ | 4 |
> | Steps per stage $T$ | 200 |
> | GRPO group size $G$ | 6 |
> | Train batch $B_{\text{train}}$ | 64 |
> | Replay batch $B_{\text{replay}}$ | 32 |
> | KL coefficient $\beta$ | 0 |
> | Learning rate | $1 \times 10^{-6}$ |
> | Time decay $\gamma$ | 0.90 |
> | Beta prior $\alpha = \beta$ | 1.0 |
> | Pruning threshold $\epsilon$ | 0.45 |
> | Pruning min trials $n_{\min}$ | 2.0 |
> | Max archive size | 4000 |
> | $\lambda_{\text{succ}}, \lambda_{\text{fail}}$ | 1.0, 0.5 |
> | Reward weights | $r_{\text{harm}} = 1.0, r_{\text{ref}} = 0.5, r_{\text{fmt}} = 0.5$ |

#### Appendix B: Strategy Space Design Rationale（1.5 页）

**写作目标**：让 reviewer 信服 12×10 不是 ad-hoc，而是基于明确数据证据剪裁的设计。

**内容草拟**：

> **B.1 Risk Categories**: Sourced from Llama Guard 4 (Llama Team, 2025), which extends Llama Guard 3 with refined risk taxonomy of 14 categories (S1–S14). We retain 12 categories and remove S12 (Sexual Content) and S14 (Code Interpreter Abuse) based on the following data-driven analysis.
>
> **B.2 Removal of S12 and S14 — empirical justification**:
>
> Table B.1 reports the distribution of these categories in our SFT distillation corpus and replay pool, along with their behavioral characteristics:
>
> | Category | SFT corpus count (%) | Pool@step 300 | DACE benign not-safe rate | LG4 semantic | text-only defender applicability |
> |---|---|---|---|---|---|
> | S12 Sexual Content | 352 (0.80%) | 9 (0.23%) | 96.3% (highest) | legitimate erotica | applicable but lacks adult benign data |
> | S14 Code Interpreter Abuse | 47 (0.11%) | 5 (0.12%) | 69.8% | text-only tool-call attacks | ❌ defender has no tool surface |
>
> Both categories exhibit (i) <1% representation in the SFT corpus, (ii) excessive false-positive rates on benign rewriting, and (iii) conceptual mismatch with text-only single-turn defenders. Their inclusion creates "dead rows" in the strategy grid that pin the maximum marginal entropy gain (denominator of $R_{\text{coverage}}$) to "filling an empty slot," which suppresses the normalized signal for all active slots. Removing them yields a balanced 12×10 grid with all 120 slots semantically meaningful and empirically populated.
>
> **B.3 Renumbering scheme**: For attacker prompt clarity we renumber S1–S11 + S13 as S1–S12; for internal Python indexing we use 0–11. The mapping is documented in code release.
>
> **B.4 Attack Styles**: Sourced from Rainbow Teaming (Samvelyan et al., 2024) augmented with Ruby Teaming (Jiang et al., 2024b) extensions. We retain 10 styles that satisfy three criteria: (a) cover qualitatively distinct attack mechanisms (linguistic obfuscation, persona shift, persuasion, etc.); (b) are common in real-world jailbreak collections (DAN, WildJailbreak, SorryBench); (c) are operationalizable as discrete categorical decisions (vs. continuous severity scales). The final 10 styles are: Slang, Technical Terms, Role Play, Authority Manipulation, Misspellings, Word Play, Emotional Manipulation, Hypotheticals, Historical Scenario, and Uncommon Dialects.

#### Appendix C: Prompt Templates（2.0 页）

包含 4 个 box：

> **C.1 Attacker SFT Distillation Prompt** (input to Gemini-2.5-Pro)
> [完整 prompt template，含 12 个 risk category 定义、10 个 attack style 定义、CoT 三段式格式要求、in-context examples]
>
> **C.2 Attacker Inference Prompt** (used during RL training)
> [简化版本，删除 in-context examples，保留策略空间描述与三段式格式]
>
> **C.3 Defender Prompt**
> [沿用 model 的 default system prompt + "Question: {attacker_prompt}" 用户输入]
>
> **C.4 Safety Judge Prompt** (Qwen3Guard / WildGuard / GPT-4o)
> [沿用各 judge 的 official template，DACE 不修改]

格式参考 MAGIC §B（box 包裹 + 各色 highlight）。

#### Appendix D: Experimental Setup Details（1.5 页）

**D.1 Training Pipeline**：基于 ReMA (Wan et al., 2025) 与 verl，4 GPU × ~50h。
**D.2 SFT Phase**：Gemini-2.5-Pro 蒸馏 ~43k 样本（20k benign + 23k harmful），LLaMA-Factory full SFT 3 epochs。
**D.3 RL Phase**：详细 Hydra config 截图。
**D.4 Baseline Implementation**：Self-RedTeam / MAGIC 重训详情、SmoothLLM / Self-Eval 推理时配置。

#### Appendix E: Evaluation Benchmarks（1.5 页）

**E.1 Safety Benchmarks**: 详细描述 9 个 benchmark（HarmBench / WildGuardTest / WildJailbreak / DAN / OR-Bench / XSTest / StrongREJECT 等）的样本数、风险分布、判官设置。
**E.2 General Capability Benchmarks**: 5 个 benchmark 的具体配置。
**E.3 OpenRT Configuration**: 沿用 MAGIC Tab 7 风格，给出 GCG / PAIR / TAP / AutoDAN / AutoDAN-turbo + **MAJIC** 与 Auto-RT 的攻击器超参表。
**E.4 X-Teaming Multi-Turn Setup**: 158 HarmBench seeds × 10 strategies × Qwen2.5-72B-IT executor。

#### Appendix F: Expanded Results（2.0 页）

包含 5 张表：

> **F.1 Llama3.1-8B-Instruct full safety table** (类比主文 Tab 1)
> **F.2 Qwen2.5-14B-Instruct full safety table** (additional scale)
> **F.3 Llama3.1-8B / Qwen2.5-14B general capability** (类比主文 Tab 2)
> **F.4 Cross-defender attacker effectiveness on additional backbones** (Mistral-7B, Phi-3, Gemini-2.5-Flash)
> **F.5 Attacker diversity metrics across all 8 dimensions**

#### Appendix G: Co-Evolution Training Dynamics（1.5 页）

**写作目标**：用 4 张 figure 把 DACE 训练动态讲透——这部分是审稿人最容易"看图理解 method 工作"的入口。

> **G.1 Pool flow metrics** (3 子图: pool size, mean posterior, zombie fraction over training steps)
> **G.2 Coverage entropy evolution** (1 图: Shannon entropy of attacker output distribution over 12×10 grid, comparing DACE / DACE w/o coverage / MAGIC)
> **G.3 Reward signal stability** (1 图: raw vs normalized coverage gain reward magnitude over training, showing no signal vanishing in normalized version)
> **G.4 Adversarial forgetting curve** (1 图: final defender ASR on attacker checkpoints from iter 1–4, comparing DACE-full / DACE w/o replay / DACE w/ uniform replay)

#### Appendix H: Attack Pattern Analysis（2.0 页）

沿用 MAGIC §F 风格：

> **H.1 Classification methodology**: 用 Qwen2.5-72B-IT 作为分类器，在 19 个 fine-grained 攻击模式子类（基于 MAGIC Appendix F.2 的 6 大族 20 子类，去除"None of these"后保留 19）上对 DACE 与 MAGIC 的 attacker 输出进行分类。
> **H.2 Strategy distribution evolution**: 4 个柱状图（步 1–60 / 121–180 / 241–300 / final），对比 DACE-attacker、MAGIC-attacker、DACE w/o coverage 三组。
> **H.3 Case studies of emergent combinatorial attacks**: 3–5 个具体案例（每个含 \<think\>+\<strategy\>+\<answer\>），展示 DACE-attacker 涌现的多策略组合（如 Role-play × Translation × Concept Substitution）。沿用 MAGIC Tab 16 的 box 格式。

#### Appendix I: Replay Buffer as Independent Jailbreak Dataset（1.0 页，可选）

**写作目标**：把 DACE 最终 ~4000 条 replay pool 作为独立的 jailbreak benchmark 公开发布——这是一个高 impact 的额外贡献。

> **I.1 Dataset statistics**: 4000 条样本 × 120 cells 分布、平均长度、posterior mean 分布。
> **I.2 Attacks against closed-source LLMs**: GPT-4o, Claude 3.5 Sonnet, Gemini 2.0 Flash 在该 dataset 上的 ASR（对比直接用 HarmBench / AdvBench 的 ASR）。
> **I.3 Public release**: dataset 与 reproduction script 链接（盲审 anonymize）。

如果预算紧张，I.2 可以缩减为 OSS 模型横评（Qwen2.5-72B / Llama3-70B / DeepSeek-V3）。

---

## 三、最后几个待你拍板的细节

1. **§2 引用的 PIA 和 TriPlay-RL 论文**：PIA 是你附件里 lijiajia 的 ICML 2026 投稿（arXiv 还没正式 ID）；TriPlay-RL 是 arXiv 2601.18292。两者都需要确认引用稳定性——若 PIA 还在投稿可能需要标 "concurrent work"。

2. **Appendix B 的剪裁数据证据**：Tab B.1 的"DACE benign not-safe rate 96.3%"等数字是 v3 阶段实测；但 v4 数据迭代后这些数字可能变化。建议在 v4 跑完后用最终数字替换，目前用占位符。

3. **Appendix I 是否保留**：把 replay buffer 作为独立 jailbreak dataset 发布是一个非常吸引人但需要额外 closed-source API 预算的选项。如果预算有限，可以 (a) 删除 Appendix I；或 (b) 改为 OSS 模型横评；或 (c) 移到 future work 提及。**建议保留 + OSS-only 横评**，能让 paper 多一个 dataset contribution 卖点而成本不增。

4. **Appendix 总篇幅 14 页是否过多**：MAGIC 是 22 页，DACE 14 页其实保守。如果 reviewer 期待更多 figures，G 与 H 各加一张图扩展到 16 页也合理。NeurIPS 2024-2025 的录用论文 appendix 中位数约 15 页。

5. **算法伪代码中是否要包含"multi-turn extension"**：MAGIC 在主文 §5.3 多轮评估时提到 attacker 可加一个 multi-turn system prompt 实现多轮。DACE 当前算法是单轮 + appendix G 的多轮 X-Teaming 评测沿用 MAGIC pattern，建议**算法伪代码保持单轮**（清晰），多轮变体在 appendix E.4 单独描述。

---

如果这一轮 OK，下一轮我可以把 abstract / introduction / method / related work / conclusion / appendix 全部翻译为正式英文版本，控制总篇幅在 9 页主文 + 14 页 appendix（NeurIPS 标准），并按 MAGIC 风格统一 section heading、citation format、figure caption 风格。你想推进吗？