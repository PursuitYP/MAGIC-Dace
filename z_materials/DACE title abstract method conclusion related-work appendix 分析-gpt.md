# DACE title abstract method conclusion related-work appendix 分析-opus

> [文件不支持导出]
> 注意理解对话历史（DACE Introduction 分析-gpt.md），这是刚刚和你对话导出的对话内容，
> ====================
> 先保留对话历史中这一版关于 Evaluation 和 Introduction 的分析，切换到下一个任务，
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

我先把这轮任务边界明确一下：**现有 Introduction 和 Evaluation 先保留，不直接重写**；这轮重点产出 **Title / Abstract / Method / Conclusion** 的中文初稿，并给出下一轮完善 Introduction 和 Evaluation 时需要改的点。整体叙事不再写成“MAGIC + diversity reward + replay buffer”，而是写成：

> **MAGIC 解决了 safety alignment 从静态防御到动态攻防共演化的问题；DACE 进一步解决共演化是否“覆盖充分”和是否“长期稳健”的问题。**
> 攻击侧通过显式策略空间覆盖缓解 attack strategy collapse；防御侧通过贝叶斯对抗回放缓解 defense adversarial forgetting。

---

# 1. Title：候选标题与推荐

## 推荐版本 1

**DACE: Diversity-Aware Adversarial Co-Evolution for Robust LLM Safety Alignment**

这是我最推荐的主标题。优点是清楚、简洁、像 NeurIPS/ICLR 论文标题；DACE 的全称自然展开为 **Diversity-Aware Adversarial Co-Evolution**，同时 “Robust LLM Safety Alignment” 直接说明任务。它比 “red-teaming” 更宽，因为 DACE 不只是生成攻击，而是同时训练 defender。

## 候选版本 2

**DACE: Strategy-Covering and Memory-Aware Co-Evolution for LLM Safety**

这个标题更突出 DACE 的两个核心机制：**strategy coverage** 和 **adversarial memory**。缺点是没有显式出现 “adversarial”，攻击防御游戏感稍弱，但更能体现本文与 MAGIC 的差异。

## 候选版本 3

**Beyond Adaptive Safety: Diversity-Aware and Memory-Aware Co-Evolution for LLM Alignment**

这个标题故事性强，适合强调 “adaptive is not enough”。它直接表达 DACE 的论文主张：现有 co-evolution 已经 adaptive，但还不够 comprehensive 和 durable。缺点是 DACE acronym 不自然，需要副标题解释。

## 候选版本 4

**Diversity-Aware Safety Co-Evolution via Strategy-Space Coverage and Bayesian Replay**

这个版本技术点最完整：strategy-space coverage + Bayesian replay 都在标题里。缺点是略偏方法堆叠，不如版本 1 大气。

## 候选版本 5

**From Local Arms Races to Durable Safety: Diversity-Driven Adversarial Co-Evolution for LLMs**

这个标题适合更强叙事型论文。它把现有方法的问题概括为 “local arms race”，把 DACE 的目标概括为 “durable safety”。缺点是没有明确 safety alignment，且略带 marketing 风格。

**最终建议：**
主标题用版本 1：

**DACE: Diversity-Aware Adversarial Co-Evolution for Robust LLM Safety Alignment**

在 Abstract 和 Introduction 第一处解释：DACE = Diversity-Aware Adversarial Co-Evolution。

---

# 2. Abstract：写法逻辑与初稿

## Abstract 应该怎么讲故事

Abstract 按 MAGIC 的写法来，但不能复述 MAGIC 的问题。MAGIC 的 abstract 结构是：

1. LLM safety 很重要，但静态防御落后于动态攻击；
2. 提出 attacker-defender adversarial game；
3. attacker 持续暴露漏洞，defender 泛化到未见攻击；
4. 实验证明 safety 提升且 helpfulness 不降。

DACE 的 Abstract 应该是 MAGIC 之后的下一层：

1. 现有 co-evolution 让 safety training 变得 adaptive；
2. 但 adaptive co-evolution 仍可能失败：攻击者策略坍缩，防御者遗忘历史攻击；
3. DACE 通过结构化策略空间、多样性奖励和贝叶斯回放解决这两个问题；
4. 实验从 defender 和 attacker 两侧证明：defender 更鲁棒，attacker 更有效且更多样，消融证明两个模块都必要。

## Abstract 初稿

大语言模型的安全对齐正在从静态防御问题转变为动态攻防演化问题。近期 attacker-defender co-evolution 方法通过让攻击者和防御者交替优化，使安全训练能够持续适应新的攻击分布。然而，我们发现，**动态适应本身并不保证长期鲁棒性**：攻击者在强化学习中容易坍缩到少数高回报攻击策略，使防御者只在狭窄攻击分布上训练；同时，随着攻击者策略不断漂移，防御者也可能在学习新攻击时逐渐遗忘早期攻击模式。为解决这两个耦合问题，我们提出 **DACE**，一个 diversity-aware adversarial co-evolution framework for LLM safety alignment。DACE 将攻击样本映射到由风险类别和攻击方式构成的二维策略空间，并通过归一化边际覆盖增益奖励鼓励攻击者生成既有效又覆盖广泛的攻击，从而缓解 attack strategy collapse。与此同时，DACE 维护一个 Bayesian adversarial replay buffer，为历史成功攻击估计相对于当前防御者的动态风险后验，并通过 Thompson Sampling 将仍具威胁或不确定的历史攻击混入防御者训练，以缓解 defense adversarial forgetting。完整伪代码置于附录。我们从 defender 和 attacker 两侧系统评估 DACE。实验表明，DACE 在多类 adversarial safety benchmarks 和 out-of-distribution attackers 上提升防御鲁棒性，同时基本保持 benign compliance 与 general capability；DACE attacker 也在 attack success、strategy coverage、successful coverage、quality-diversity score 和 cross-defender transferability 上表现出更好的有效性—多样性平衡。消融实验进一步验证，结构化策略覆盖奖励和贝叶斯对抗回放分别是攻击多样性提升和防御长期鲁棒性的关键来源。

---

# 3. Method：写法逻辑与正文初稿

## Method 应该怎么写

Method 不要写成工程说明，而要按“问题—机制—训练目标”的逻辑展开。推荐主文结构如下：

**3.1 Overview**：说明 DACE 是 attacker-defender sequential game 的扩展，核心新增 strategy-space coverage 和 adversarial memory。
**3.2 Structured Attack Strategy Space**：定义 $\mathcal{B}=\mathcal{S}\times\mathcal{C}$，解释风险类别和攻击方式来源。
**3.3 Diversity-Aware Attacker Optimization**：定义 attacker reward，重点讲 normalized marginal coverage gain。
**3.4 Bayesian Adversarial Replay for Defender**：定义 archive/replay pool、Beta-Bernoulli posterior、Thompson Sampling、time decay 和 pruning。
**3.5 Alternating Co-Evolution Training**：说明 SFT warm-up、GRPO、attacker stage、defender mixed-batch stage。
**Algorithm**：主文只放简化流程图或高层算法说明，完整伪代码放 Appendix A。

---

## 3.1 Overview

我们将 LLM safety alignment 建模为攻击者 $\pi_A$ 与防御者 $\pi_D$ 之间的动态对抗过程。给定原始种子请求 $q$，攻击者首先生成改写后的对抗 prompt $x \sim \pi_A(\cdot \mid q)$，防御者随后生成响应 $y \sim \pi_D(\cdot \mid x)$。防御者的目标是在保持正常请求响应能力的同时拒绝有害请求，攻击者的目标则是发现能够诱导防御者失败的攻击形式。与已有 co-evolution 框架类似，DACE 采用解耦的 attacker 和 defender 参数，并通过交替优化近似双方的动态 best-response 过程。

DACE 的核心不同点在于，它不把 co-evolution 仅仅视为当前攻击者和当前防御者之间的局部对抗，而是显式建模两个长期因素：**攻击策略空间的覆盖** 和 **历史攻击经验的保持**。在攻击侧，DACE 将每个攻击映射到一个结构化行为描述符 $b(x)$，并奖励攻击者覆盖低频或未探索的策略区域；在防御侧，DACE 将历史成功攻击存入对抗回放池，并持续估计这些样本对当前防御者的剩余威胁度。这样，DACE 将在线红队、策略空间探索和防御者记忆巩固统一到一个闭环训练过程中。

---

## 3.2 Structured Attack Strategy Space

DACE 定义二维攻击策略空间

$$

\mathcal{B} = \mathcal{S} \times \mathcal{C},

$$

其中 $\mathcal{S}$ 表示安全风险类别，$\mathcal{C}$ 表示攻击方式。每个生成的攻击样本 $x$ 被映射到一个行为描述符

$$

b(x) = (s, c) \in \mathcal{B}.

$$

在当前实现中，风险类别 $\mathcal{S}$ 基于 Llama-Guard-4 的安全 taxonomy 构建，并根据训练数据频率和 text-only safety setting 的适用性进行裁剪。具体地，我们保留 12 个风险类别：Violent Crimes、Non-Violent Crimes、Sex-Related Crimes、Child Sexual Exploitation、Defamation、Specialized Advice、Privacy、Intellectual Property、Indiscriminate Weapons、Hate、Suicide & Self-Harm 和 Elections；删除频率极低且在当前 text-only defender 设置中不稳定或不适用的 Sexual Content 与 Code Interpreter Abuse。攻击方式 $\mathcal{C}$ 参考 Rainbow Teaming 的 adversarial prompt style taxonomy，包含 10 类攻击风格：Slang、Technical Terms、Role Play、Authority Manipulation、Misspellings、Word Play、Emotional Manipulation、Hypotheticals、Historical Scenario 和 Uncommon Dialects。因此，DACE 的默认策略空间包含 $12 \times 10 = 120$ 个策略单元。

为了让策略选择成为攻击者的显式动作，DACE 在攻击者输入中提供完整的策略空间描述，并要求攻击者在生成攻击 prompt 前输出其选择的风险类别和攻击方式。具体输出格式包含 `<think>`、`<strategy>` 和 `<answer>` 三个字段，其中 `<strategy>` 显式声明 `risk category` 与 `attack style`。训练时，我们直接从攻击者输出中解析 $b(x)$，而不是额外依赖 LLM judge 重新推断攻击方式。这样可以降低策略标注噪声，并使策略选择直接受强化学习信号约束。

---

## 3.3 Diversity-Aware Attacker Optimization

攻击者的目标不是单纯最大化 attack success rate，而是生成 **既有效又多样** 的攻击。为此，DACE 将攻击者奖励分解为攻击有效性、格式约束和策略多样性三部分：

$$

R_A(x, y) = -R_D(x, y) + R_{\mathrm{fmt}}(x) + \lambda(x) R_{\mathrm{div}}(x),

$$

其中 $R_D(x,y)=R_{\mathrm{harm}}(y)+R_{\mathrm{ref}}(y)$ 是防御者奖励，包含响应安全性和拒答校准；$-R_D$ 构成攻击者与防御者之间的零和部分；$R_{\mathrm{fmt}}$ 保证攻击者输出可解析的结构化格式；$R_{\mathrm{div}}$ 则鼓励策略空间覆盖。

多样性权重 $\lambda(x)$ 根据攻击成败自适应设置：

$$

\lambda(x)=
\begin{cases}
1.0, & \text{if } x \text{ succeeds},\\
0.5, & \text{otherwise}.
\end{cases}

$$

这一设计体现 **effective diversity** 原则：成功攻击应获得完整多样性奖励，因为它们同时具有安全威胁和覆盖价值；失败攻击仍保留折减的多样性奖励，以避免模型过早放弃尚未学会但安全语义上重要的低频策略区域。相比只奖励成功率，这可以缓解 RL attacker 对少数高回报攻击模式的过度利用；相比只奖励 diversity，这又避免模型生成大量多样但无效的攻击。

DACE 的主要多样性奖励是 **normalized marginal coverage gain**。设 $\mathcal{A}$ 为当前攻击档案池，$\mathbf{p}_{\mathcal{A}}$ 为档案池中策略单元的经验分布，$H(\cdot)$ 为 Shannon entropy。对于一个新攻击样本 $x$，其策略覆盖奖励定义为：

$$

R_{\mathrm{div}}(x)
=
\frac{
H(\mathbf{p}_{\mathcal{A}\cup\{x\}})-H(\mathbf{p}_{\mathcal{A}})
}{
\max_{b\in\mathcal{B}}
\left[
H(\mathbf{p}_{\mathcal{A}\cup\{x_b\}})-H(\mathbf{p}_{\mathcal{A}})
\right]
+\epsilon
}.

$$

分子表示样本 $x$ 对当前策略分布带来的实际熵增；分母表示在当前档案池状态下，单个样本能够实现的最大熵增。由于原始边际熵增会随着 $|\mathcal{A}|$ 增大而按 $O(1/|\mathcal{A}|)$ 衰减，直接使用 raw entropy gain 会导致训练后期 diversity reward vanishing。DACE 的归一化形式将实际增益除以当前最优单步增益，使奖励量级在训练全过程中保持稳定。

该奖励也可以从 KL 散度角度解释。由于

$$

H(\mathbf{p}) = \log |\mathcal{B}| - D_{\mathrm{KL}}(\mathbf{p}\|\mathbf{u}),

$$

其中 $\mathbf{u}$ 是策略空间上的均匀分布，边际熵增等价于加入样本后策略分布相对于均匀分布的 KL 散度下降量。因此，$R_{\mathrm{div}}$ 可以理解为单步 KL 收缩效率：一个样本越能推动攻击分布向未覆盖或低频策略区域移动，它获得的多样性奖励越高。

---

## 3.4 Bayesian Adversarial Replay for Defender

攻击者策略在训练中持续变化，防御者面对的训练分布也随之非平稳漂移。若防御者只学习当前攻击者生成的新攻击，它可能逐渐遗忘早期攻击模式。为缓解这种 **defense adversarial forgetting**，DACE 维护一个统一的 adversarial archive and replay pool $\mathcal{A}$。该池同时承担两个功能：一是记录策略频次，用于计算攻击者的 diversity reward；二是存储历史成功攻击，用于防御者回放训练。

对每个历史攻击样本 $x_i$，DACE 不存储一个固定的离散风险标签，而是维护其相对于当前防御者的动态攻击成功概率后验。具体地，我们令攻击是否突破防御者服从 Bernoulli 分布，并采用 Beta 先验：

$$

p_i \mid s_i, f_i \sim \mathrm{Beta}(\alpha+s_i, \beta+f_i),

$$

其中 $s_i$ 和 $f_i$ 分别表示样本 $x_i$ 在回放评估中的衰减累计成功次数和失败次数。后验均值

$$

\hat{p}_i =
\frac{\alpha+s_i}{\alpha+\beta+s_i+f_i}

$$

表示该样本对当前防御者的期望攻破概率。相比只依赖 judge 给出的离散 safety score 来重写样本风险，DACE 的后验分布保留了不确定性：同一个历史攻击即使曾被拒绝，也不会因为一次防御成功而被立即淘汰；多次评估后，后验才会逐渐收敛。这使回放机制能够自然处理 defender 响应的偶然性。

为了适应防御者本身在训练中的变化，DACE 在每轮开始时对历史统计施加指数时间衰减：

$$

s_i \leftarrow \gamma s_i,\qquad f_i \leftarrow \gamma f_i.

$$

时间衰减使历史风险估计能够跟踪当前 defender，而不是被早期训练阶段的结果永久支配。对于回放采样，DACE 使用 Thompson Sampling：从每个样本的后验分布中采样风险值

$$

\tilde{p}_i \sim \mathrm{Beta}(\alpha+s_i,\beta+f_i),

$$

并选取采样值最高的 $B_{\mathrm{replay}}$ 个样本加入防御者训练。该机制同时偏好后验均值高的危险样本和不确定性高、尚未充分测试的样本，从而在 exploitation 与 exploration 之间自动平衡。

防御者训练时，每个 batch 由当前攻击者生成的新攻击和回放池采样的历史攻击组成。新攻击帮助防御者适应当前 attacker 的最新策略，历史攻击则帮助防御者保持对早期漏洞的鲁棒性。对于回放样本，防御者生成响应后，DACE 根据是否仍被攻破更新对应后验；当某个样本的后验均值低于阈值且已被充分测试时，该样本会被剪枝出池。这样，回放池不是静态缓存，而是一个动态 adversarial memory。

---

## 3.5 Alternating Co-Evolution Training

DACE 采用两阶段训练流程。首先，为避免基础模型在改写有害请求时直接拒绝，我们使用结构化攻击改写数据对攻击者进行 SFT warm-up，使其具备基本的 offensive reasoning 和格式遵循能力。随后进入迭代 RL 阶段，攻击者和防御者交替通过 GRPO 更新。

在 attacker optimization stage 中，防御者参数固定。攻击者针对每个种子请求生成多个 candidate attacks，并显式选择策略描述符 $b(x)$。防御者对每个攻击生成响应，安全评估器计算响应安全性、拒答状态和攻击成败。攻击者随后根据攻击有效性、格式合规性和策略覆盖奖励通过 GRPO 更新。

在 defender optimization stage 中，攻击者参数固定。对于每个训练 batch，攻击者首先从新种子请求生成当前攻击；同时，DACE 从回放池中采样历史高风险攻击。防御者在新攻击与回放攻击的混合 batch 上生成多组响应，并根据安全性和拒答校准奖励进行 GRPO 更新。混合训练使防御者在每个更新步中同时接触新旧威胁，避免将“适应当前攻击”和“记住历史攻击”拆成两个可能互相干扰的独立阶段。

考虑到完整伪代码较长，主文中建议只保留 DACE 的高层训练流程图或简化算法框，完整训练伪代码放入 **Appendix A**。主文 Method 中可写：

> The full training procedure, including archive updates, posterior decay, Thompson replay sampling, and pruning, is provided in Appendix A.

---

# 4. Conclusion：写法逻辑与初稿

## Conclusion 应该怎么写

Conclusion 不要只是重复实验结果，而要把 DACE 的论文主张收回来：

1. 第一段总结核心贡献：DACE 让 co-evolution 同时具备 strategy-space coverage 和 adversarial memory。
2. 第二段总结实验意义：defender 更稳健，attacker 更有效且更多样，消融支持机制有效。
3. 第三段诚实写 limitation：训练成本、judge 依赖、策略 taxonomy 设计、text-only 设置；未来扩展到 multimodal / tool-use / agent safety。

## Conclusion 初稿

本文提出 DACE，一个面向 LLM safety alignment 的 diversity-aware adversarial co-evolution framework。DACE 的核心观点是：稳健的安全共演化不仅需要 attacker 和 defender 动态适应彼此，还需要攻击侧持续覆盖更广泛的策略空间，并需要防御侧持续记忆和重估历史攻击。为此，DACE 将攻击样本映射到由风险类别和攻击方式构成的结构化策略空间，通过归一化边际覆盖增益奖励缓解攻击策略坍缩；同时，DACE 使用 Bayesian adversarial replay buffer 追踪历史攻击对当前防御者的动态威胁度，并将高风险或高不确定性的历史样本混入防御者训练，以缓解防御对抗遗忘。

实验从 defender 和 attacker 两个角度验证了 DACE 的有效性。在 defender 端，DACE 在多类 harmful refusal、OOD attacker robustness 和历史攻击保持评测中提升安全鲁棒性，同时基本保持 benign compliance 与 general capability。在 attacker 端，DACE 不仅保持较强 attack success rate，还显著提高 strategy coverage、successful coverage、strategy entropy、quality-diversity score 和 cross-defender transferability。消融结果进一步表明，结构化多样性奖励主要贡献于攻击策略覆盖扩展，而贝叶斯对抗回放主要贡献于防御者长期鲁棒性和抗遗忘能力。

DACE 也存在若干限制。首先，在线攻防共演化和回放评估带来额外训练成本；其次，DACE 依赖安全 judge 对攻击成败和防御响应进行评估，judge 的鲁棒性会影响奖励质量；第三，策略空间 taxonomy 的设计会影响 diversity reward 的粒度和覆盖方向。未来工作可以探索更细粒度或自动演化的攻击策略空间，将 DACE 扩展到多轮 agent、tool-use 和 multimodal safety 场景，并研究更高效的回放采样与训练调度机制。我们希望 DACE 能推动 LLM safety alignment 从针对当前攻击的局部适应，迈向覆盖充分、记忆稳定、可持续演化的安全训练范式。

---

# 5. 下一轮 Introduction 的改进意见

现有 Introduction 可以先保留，但下一轮建议重点改三处。

第一，**关于 diversity gap，要补充 TriPlay-RL，但不要过度展开。**
建议写法是：TriPlay-RL 已经在攻防协同建模中注意到 diversity 的重要性，但它的 diversity 主要停留在语义或角色层面的分散，缺少与安全风险类别、攻击方式和攻击成功率直接耦合的策略空间覆盖。因此，它不能充分保证攻击策略覆盖能够转化为更强的攻击能力或更稳健的防御训练信号。DACE 的差异是把 diversity 定义为 safety-relevant strategy coverage，即 risk category $\times$ attack style 的有效覆盖，而不是表层语义变化。

第二，**关于 replay gap，要修正之前“现有方法不更新 replay 样本”的表述。**
更准确的说法应该是：相关方法中的 replay 样本通常也会在回放后更新风险或奖励估计，但这种更新往往依赖 judge 给出的离散 safety score 或静态 reward，对 defender 响应的随机性和防御者本身的非平稳变化建模不足。DACE 的改进不是“首次更新 replay 样本”，而是将样本风险建模为动态后验分布，通过 Beta-Bernoulli update、时间衰减和 Thompson Sampling 同时处理当前威胁度、不确定性和 defender 演化。

第三，**Introduction 中不要写太细的 12×10 技术细节。**
Intro 可以说结构化策略空间 $\mathcal{S}\times\mathcal{C}$，具体 12 个 risk categories、10 个 attack styles、删除两个低频类别这些细节放 Method。这样主线更清楚，也避免 Introduction 看起来像实现说明。

---

# 6. 下一轮 Evaluation 的改进意见与表格骨架

Evaluation 先保留当前版本，但建议下一轮按下面骨架补齐。具体数据可以先留空。

## Table 1：Defender safety and benign compliance

| Model | WG adv harm ASR↓ | WG van harm ASR↓ | WJB adv harm ASR↓ | DAN ASR↓ | HarmBench adv ASR↓ | HarmBench van ASR↓ | OR-Bench RTA↑ | XSTest harm RTA↑ | StrongREJECT RTA↑ | WJB benign Comply↑ | XSTest benign Comply↑ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Base |  |  |  |  |  |  |  |  |  |  |  |
| Self-RedTeam |  |  |  |  |  |  |  |  |  |  |  |
| MAGIC |  |  |  |  |  |  |  |  |  |  |  |
| DACE |  |  |  |  |  |  |  |  |  |  |  |
| DACE w/o diversity |  |  |  |  |  |  |  |  |  |  |  |
| DACE w/o replay |  |  |  |  |  |  |  |  |  |  |  |

## Table 2：General capability

| Model | IFEval Prompt Loose↑ | IFEval Inst Loose↑ | ARC-C↑ | GPQA↑ | MMLU↑ | AlpacaEval 2 LC Win↑ |
|---|---:|---:|---:|---:|---:|---:|
| Base |  |  |  |  |  |  |
| MAGIC |  |  |  |  |  |  |
| DACE |  |  |  |  |  |  |
| DACE w/o diversity |  |  |  |  |  |  |
| DACE w/o replay |  |  |  |  |  |  |

## Table 3：OOD attacker robustness

| Defender | No-rev↓ | GCG↓ | PAIR↓ | TAP↓ | AutoDAN↓ | AutoDAN-turbo↓ | MAJIC-Attack↓ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Base |  |  |  |  |  |  |  |
| MAGIC |  |  |  |  |  |  |  |
| DACE |  |  |  |  |  |  |  |
| DACE w/o diversity |  |  |  |  |  |  |  |
| DACE w/o replay |  |  |  |  |  |  |  |

MAJIC-Attack 建议作为 stronger adaptive black-box attacker 放进主表或 appendix 前部，但要避免与 MAGIC 名字混淆。

## Table 4：Attacker quality-diversity evaluation

| Attacker | ASR@1↑ | ASR@5↑ | Transfer ASR↑ | Cell Coverage↑ | Successful Coverage↑ | Normalized Entropy↑ | QD-Score↑ | Max Cell Share↓ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Base attacker |  |  |  |  |  |  |  |  |
| MAGIC attacker |  |  |  |  |  |  |  |  |
| DACE attacker |  |  |  |  |  |  |  |  |
| DACE w/o diversity |  |  |  |  |  |  |  |  |

## Table 5：Replay and forgetting ablation

| Method | Early attack ASR↓ | Mid attack ASR↓ | Latest attack ASR↓ | OOD attacker ASR↓ | Benign Comply↑ | General Capability Avg↑ |
|---|---:|---:|---:|---:|---:|---:|
| No replay |  |  |  |  |  |  |
| Uniform replay |  |  |  |  |  |  |
| Top-risk replay |  |  |  |  |  |  |
| Thompson replay |  |  |  |  |  |  |
| DACE full |  |  |  |  |  |  |

这张表或对应曲线非常关键，因为它直接证明 DACE 的 replay 不是普通数据复用，而是在缓解 defense adversarial forgetting。

-----

> 在这些材料和分析的基础上，再写一下 related work 和 appendix 部分，附录可以先参考 maigc 论文来写，其他要求与之前的一样

下面继续沿用上一轮的写法：先说明 **Related Work 和 Appendix 应该承担什么叙事功能**，再给出可以直接改写进论文的中文初稿。这里默认主文已有 Introduction / Method / Evaluation 的初稿，因此 Related Work 要避免重复 Introduction 的 gap，而是更像 NeurIPS 论文里的“定位与区分”。

---

# 1. Related Work 应该怎么写

Related Work 的核心不是罗列论文，而是把 DACE 放进四条研究线里：

1. **LLM jailbreak 与 automated red teaming**：说明攻击从人工模板、启发式扰动，发展到自动化搜索、RL、多步组合和自适应攻击。DACE 借鉴自动红队，但目标不是单独造更强 attacker，而是用 attacker 驱动 defender 共演化。

2. **Safety alignment as adversarial co-evolution**：说明 MAGIC、Self-RedTeam、AdvGame、TriPlay-RL、PIA 等把 safety 训练转成博弈或自博弈。DACE 与它们最接近，但补上两个缺口：策略覆盖不足和历史攻击遗忘。

3. **Diversity in red teaming**：说明 Rainbow Teaming、Ruby Teaming、RainbowPlus、QDRT、DiveR-CT、CRT、CALM 等强调多样性，但多样性常常是语义/文本/行为层面的，并不一定转化成有效攻击和稳健防御。这里要专门加入 TriPlay-RL 的 diversity 局限：它意识到 diversity，但比较 superficial，缺少 safety-relevant strategy-space coverage。

4. **Replay, memory, and non-stationary safety training**：修正之前 replay 的说法：现有方法并非完全不更新样本风险，而是通常依赖 judge 的离散 safety score 或静态 reward 来更新样本风险，缺少对 defender 偶然性和动态变化的后验建模。DACE 的 Bayesian replay 是主要差异。

---

# 2. Related Work 初稿

## 2. Related Work

### LLM Jailbreaking and Automated Red Teaming

Early jailbreak attacks against large language models mainly rely on human-crafted prompts, such as role-playing, instruction hierarchy confusion, linguistic obfuscation, encoding tricks, and scenario reframing. Although these prompts can expose important vulnerabilities, they are difficult to scale and often overfit to specific model behaviors. Subsequent work formulates red teaming as an automated optimization problem. Gradient-based methods such as GCG optimize adversarial suffixes; LLM-driven attacks such as PAIR iteratively revise prompts using model feedback; tree-search and evolutionary methods such as TAP and AutoDAN explore stronger jailbreak candidates under a query budget. More recent adaptive attacks further move from single-step rewriting to multi-step strategy composition, where attackers dynamically combine multiple obfuscation and persuasion strategies to bypass defenses.

These methods provide increasingly strong evaluation-time attackers, but most of them treat the defender as a fixed target. As a result, they are effective at revealing vulnerabilities but do not by themselves provide a training mechanism for improving intrinsic model safety. DACE is complementary to this line of work: rather than optimizing a standalone jailbreak algorithm, it uses an attacker model as part of an online safety co-evolution process, where discovered attacks are converted into training signals for a defender. In our experiments, strong external attackers such as GCG, PAIR, TAP, AutoDAN, AutoDAN-Turbo, and adaptive strategy-composition attacks can be used to evaluate whether the resulting defender generalizes beyond the attacks generated by DACE itself.

### Safety Alignment via Adversarial Games and Co-Evolution

A growing body of work studies LLM safety alignment through self-play, adversarial training, or game-theoretic formulations. Static safety tuning and offline red-teaming datasets are limited because the attack distribution can change after deployment. Self-play red-teaming methods address this issue by iteratively generating new adversarial prompts and using them for safety training. However, shared-parameter self-play may suffer from conflicting optimization objectives when the same model alternates between attacker and defender roles. MAGIC addresses this issue by decoupling attacker and defender models and formulating LLM safety as an asymmetric adversarial game, where the attacker learns to rewrite harmful queries and the defender learns robust refusal behavior. Other game-based or co-evolutionary methods similarly emphasize dynamic adaptation between offensive and defensive policies.

DACE builds directly on this co-evolutionary view but argues that dynamic adaptation alone is not sufficient for durable safety. In practice, RL attackers may collapse to a small number of high-reward attack patterns, producing an apparently strong but narrow training distribution. At the same time, a defender trained only on the latest attacker distribution may gradually forget earlier vulnerabilities. DACE therefore extends adversarial co-evolution with two additional mechanisms: diversity-aware strategy-space coverage for the attacker and Bayesian adversarial replay for the defender. This changes the goal from local best response against the current opponent to broader and more durable safety improvement over an evolving attack space.

Persona-based and role-based safety work is also closely related. PIA shows that safety behavior should be invariant to persona contexts: a model should not answer a harmful request merely because it is framed under a benign or fictional role. This insight is complementary to DACE. While PIA focuses on disentangling harmful intent from persona or role context, DACE focuses on covering a broader two-dimensional attack strategy space and maintaining historical adversarial memory during co-evolution. In future work, persona lineage or role-context dimensions could be incorporated as additional strategy descriptors in DACE’s attack space.

TriPlay-RL is another relevant co-evolutionary framework because it explicitly recognizes the importance of diversity in multi-role safety training. However, its treatment of diversity remains relatively superficial: diversity is mainly encouraged at the semantic or role-interaction level, rather than being tied to a safety-relevant strategy space whose coverage can be measured and optimized. Such semantic diversity may produce varied-looking prompts without necessarily improving attack effectiveness or defender robustness. DACE instead defines diversity over a structured behavior descriptor $b(x)=(s,c)$, where $s$ is a risk category and $c$ is an attack style. This makes diversity measurable, controllable, and directly connected to safety-relevant coverage.

### Diversity in Automated Red Teaming

Diversity has become an important objective in automated red teaming. Rainbow Teaming frames adversarial prompt generation as an open-ended quality-diversity problem, encouraging attacks that cover different risk categories and attack styles. Ruby Teaming improves quality-diversity search with memory, while RainbowPlus and QDRT further explore evolutionary or behavior-conditioned approaches for generating both high-quality and diverse attacks. Other works such as curiosity-driven red teaming, DiveR-CT, CALM, and related RL-based methods introduce novelty rewards, semantic distance, topic coverage, or generated reward functions to expand the exploration space of red-teamers.

Despite these advances, diversity in existing red-teaming systems often has two limitations. First, diversity is frequently measured at the surface, semantic, or embedding level; such metrics may not correspond to meaningful safety coverage. Two prompts can be semantically distant while exploiting the same safety weakness, or semantically similar while probing different risk categories and attack mechanisms. Second, many diversity-oriented red-teaming methods optimize attacker generation against fixed models, but do not study how diverse attacks should be integrated into defender training. Therefore, high diversity alone does not guarantee improved safety alignment.

DACE addresses these limitations by optimizing **effective strategy diversity**. It defines a two-dimensional safety-relevant strategy space $\mathcal{B}=\mathcal{S}\times\mathcal{C}$, where $\mathcal{S}$ is derived from the Llama-Guard-4 risk taxonomy after removing low-frequency or unsuitable categories, and $\mathcal{C}$ follows attack-style categories inspired by Rainbow Teaming. DACE then rewards normalized marginal coverage gain over this space, with stronger weighting for successful attacks and weaker but nonzero weighting for failed attempts. This design encourages the attacker to discover attacks that are not only diverse in form, but also useful for training a more robust defender.

### Replay, Memory, and Non-Stationary Safety Training

Experience replay has long been used in reinforcement learning and continual learning to stabilize training and reduce forgetting. In LLM safety, replay-like mechanisms are increasingly used to reuse historical adversarial samples, maintain red-team memories, or revisit high-risk prompts discovered in previous rounds. Such methods are important because the attacker distribution is non-stationary: as the attacker changes, a defender trained only on current attacks may lose robustness to earlier attack families.

However, replay in adversarial safety training remains underdeveloped. Existing replay mechanisms may update sample harmfulness or reward after replay, but they often rely on discrete safety judgments or point estimates provided by a judge model. This makes the replay decision brittle: a sample may be treated as either solved or risky based on limited observations, even though defender responses are stochastic and the defender itself changes throughout training. Moreover, static or score-based replay does not explicitly balance high-risk samples and uncertain samples, both of which are important in an evolving adversarial game.

DACE treats replay as Bayesian risk tracking under non-stationarity. Each archived attack maintains a Beta-Bernoulli posterior over its probability of defeating the current defender. After replay, the posterior is updated according to whether the attack still succeeds. A time decay factor allows old evidence to gradually lose influence as the defender evolves. Thompson Sampling then selects replay samples that are either likely to remain dangerous or insufficiently tested. This posterior-based replay differs from fixed-score replay by modeling both uncertainty and defender dynamics, making the adversarial memory adaptive rather than static.

---

# 3. Appendix 应该怎么写

参考 MAGIC 的风格，Appendix 不应该只是“放不下的内容”，而应该服务四个目标：

第一，**可复现性**：完整算法、reward、prompt format、taxonomy、训练超参、evaluation protocol。
第二，**可信度**：补充消融、judge agreement、不同 benchmark、不同 attacker、不同 replay 策略。
第三，**解释性**：展示 DACE attacker 的策略分布、archive heatmap、strategy composition、failure cases。
第四，**安全性**：定性样例必须 sanitized，不放可直接复用的有害攻击 prompt。

建议主文保留 Method 的简化描述，把完整伪代码和复杂表格放 Appendix。结构可以写成：

- **Appendix A. Full DACE Training Algorithm**
- **Appendix B. Strategy Space and Prompt Format**
- **Appendix C. Reward Design and Bayesian Replay Details**
- **Appendix D. Experimental Details**
- **Appendix E. Additional Defender Evaluation**
- **Appendix F. Attacker Evaluation and Diversity Metrics**
- **Appendix G. Ablation Studies**
- **Appendix H. Judge Robustness and Human Validation**
- **Appendix I. Qualitative Analysis**
- **Appendix J. Limitations, Safety, and Responsible Release**

---

# 4. Appendix 初稿

## Appendix A. Full DACE Training Algorithm

### A.1 Overview

This appendix provides the full training procedure of DACE, including attacker optimization, defender mixed-batch optimization, archive updates, Bayesian posterior decay, Thompson replay sampling, and pruning. The main paper presents a high-level description due to space constraints.

DACE maintains two decoupled policies: an attacker $\pi_A$ and a defender $\pi_D$. The attacker rewrites seed prompts into adversarial prompts while explicitly selecting a risk category and an attack style. The defender generates responses to either newly generated attacks or replayed historical attacks. A unified adversarial archive $\mathcal{A}$ stores successful attacks and serves two purposes: computing strategy-space coverage rewards for the attacker and sampling historical high-risk attacks for defender replay.

### A.2 Full Algorithm

```text
Algorithm 1: DACE Training Procedure

Input:
  Attacker policy π_A, defender policy π_D
  Seed dataset D containing harmful and benign prompts
  Strategy space B = S × C
  Archive pool A
  Number of rounds K
  Attacker steps T_A, defender steps T_D
  New batch size B_train, replay batch size B_replay
  Beta prior parameters α, β
  Time decay γ
  Pruning threshold ε_prune

1:  Initialize attacker π_A with supervised offensive rewriting data.
2:  Initialize defender π_D from the base instruction-tuned model.
3:  Initialize archive pool A = ∅.

4:  for round k = 1, ..., K do
5:      Apply time decay to all archive entries:
            s_i ← γ s_i, f_i ← γ f_i.

6:      Attacker optimization stage:
7:      for t = 1, ..., T_A do
8:          Sample seed prompts q from D.
9:          Generate candidate attacks x ~ π_A(· | q).
10:         Extract strategy descriptor b(x) = (s, c).
11:         Query defender π_D to obtain responses y.
12:         Evaluate attack success and defender reward.
13:         Compute diversity reward R_div(x) using normalized marginal coverage gain.
14:         Compute attacker reward:
                R_A = -R_D + R_fmt + λ(x)R_div.
15:         Update π_A with GRPO.
16:         Add newly successful attacks into archive buffer.
17:      end for
18:      Flush successful attacks into archive A.

19:      Defender optimization stage:
20:      for t = 1, ..., T_D do
21:          Sample new seed prompts q from D.
22:          Generate new attacks x_new ~ π_A(· | q).
23:          Sample replay attacks x_rep from A using Thompson Sampling.
24:          Construct mixed batch X = x_new ∪ x_rep.
25:          Generate defender responses y ~ π_D(· | X).
26:          Evaluate harmfulness and refusal calibration.
27:          Update π_D with GRPO using defender rewards.
28:          Update posterior statistics for replay entries.
29:          Add newly successful attacks from x_new into archive buffer.
30:      end for
31:      Flush successful new attacks into archive A.
32:      Prune archive entries with low posterior risk and enough trials.
33:  end for

Output:
  Final attacker π_A, final defender π_D, and archive A.
```

### A.3 Difference from Standard Co-Evolution

Standard co-evolution trains the defender mainly against the current attacker distribution. DACE differs in two ways. First, attacker exploration is guided by explicit strategy-space coverage rather than only attack success. Second, defender training uses a mixed batch of current attacks and Bayesian replay attacks, which allows the defender to adapt to new threats while retaining robustness to earlier threats.

---

## Appendix B. Strategy Space and Prompt Format

### B.1 Risk Categories

DACE defines the risk dimension $\mathcal{S}$ based on the Llama-Guard-4 taxonomy, with two modifications. We remove categories that are extremely rare in our data or poorly matched to a text-only defender setting. The resulting risk set contains 12 categories.

| Index | Risk Category |
|---:|---|
| S1 | Violent Crimes |
| S2 | Non-Violent Crimes |
| S3 | Sex-Related Crimes |
| S4 | Child Sexual Exploitation |
| S5 | Defamation |
| S6 | Specialized Advice |
| S7 | Privacy |
| S8 | Intellectual Property |
| S9 | Indiscriminate Weapons |
| S10 | Hate |
| S11 | Suicide & Self-Harm |
| S12 | Elections |

We remove **Sexual Content** because it is low-frequency in the current training data and unstable under benign/harmful boundary labeling. We remove **Code Interpreter Abuse** because the current defender is evaluated in a text-only setting without tool execution or code interpreter surfaces. This yields a cleaner and more active strategy space for diversity optimization.

### B.2 Attack Styles

The attack-style dimension $\mathcal{C}$ follows a Rainbow-Teaming-inspired taxonomy. We use 10 attack styles:

| Index | Attack Style |
|---:|---|
| C1 | Slang |
| C2 | Technical Terms |
| C3 | Role Play |
| C4 | Authority Manipulation |
| C5 | Misspellings |
| C6 | Word Play |
| C7 | Emotional Manipulation |
| C8 | Hypotheticals |
| C9 | Historical Scenario |
| C10 | Uncommon Dialects |

The full behavior descriptor is therefore

$$

b(x)=(s,c)\in \mathcal{S}\times\mathcal{C},

$$

with $12\times 10=120$ strategy cells.

### B.3 Attacker Output Format

The attacker is required to output a structured response with three fields:

```text
<think>
  hidden reasoning used by the attacker
</think>
<strategy>
  risk category: [one category from S]
  attack style: [one style from C]
</strategy>
<answer>
  rewritten adversarial prompt
</answer>
```

During training, the strategy descriptor $b(x)$ is extracted directly from the `<strategy>` field. The defender only receives the rewritten prompt in `<answer>`, not the attacker’s hidden reasoning or strategy declaration. This ensures that strategy selection is trainable while avoiding leakage of attacker reasoning to the defender.

### B.4 Benign Prompts and Over-Refusal Attacks

For benign seeds, DACE does not ask the attacker to introduce harmful intent. Instead, benign adversarial prompts are designed to test whether the defender over-refuses safe requests or incorrectly judges benign content as harmful. This distinction is important: a benign seed should remain benign after rewriting, and attack success on benign data corresponds to false refusal or false harmfulness judgment, not to the creation of a genuinely unsafe request.

---

## Appendix C. Reward Design and Bayesian Replay

### C.1 Defender Reward

The defender reward contains two components:

$$

R_D(x,y)=R_{\mathrm{harm}}(y)+R_{\mathrm{ref}}(x,y).

$$

The harmfulness reward encourages the defender to produce safe responses. The refusal reward calibrates when refusal is appropriate: harmful requests should be refused, while benign requests should be answered. This prevents the defender from obtaining high safety scores by refusing everything.

### C.2 Attacker Reward

The attacker reward is

$$

R_A(x,y)=-R_D(x,y)+R_{\mathrm{fmt}}(x)+\lambda(x)R_{\mathrm{div}}(x).

$$

The first term is the adversarial objective against the defender. The format reward enforces structured outputs. The diversity term encourages coverage over the strategy space.

The diversity coefficient is

$$

\lambda(x)=
\begin{cases}
1.0, & \text{if the attack succeeds},\\
0.5, & \text{otherwise}.
\end{cases}

$$

This design encourages successful diverse attacks while preserving weak exploration pressure for unsuccessful but underexplored strategy cells.

### C.3 Normalized Marginal Coverage Gain

Let $\mathbf{p}_{\mathcal{A}}$ be the empirical distribution over strategy cells in the archive. DACE defines

$$

R_{\mathrm{div}}(x)
=
\frac{
H(\mathbf{p}_{\mathcal{A}\cup\{x\}})-H(\mathbf{p}_{\mathcal{A}})
}{
\max_{b\in\mathcal{B}}
\left[
H(\mathbf{p}_{\mathcal{A}\cup\{x_b\}})-H(\mathbf{p}_{\mathcal{A}})
\right]
+\epsilon
}.

$$

This normalizes the raw entropy gain by the best possible one-step gain under the current archive state. The normalization avoids reward vanishing when the archive becomes large.

### C.4 Bayesian Replay Posterior

For each archived attack $x_i$, DACE maintains a Beta-Bernoulli posterior:

$$

p_i \mid s_i,f_i \sim \mathrm{Beta}(\alpha+s_i,\beta+f_i),

$$

where $s_i$ and $f_i$ are decayed counts of replay success and failure. The posterior mean is

$$

\hat{p}_i=
\frac{\alpha+s_i}{\alpha+\beta+s_i+f_i}.

$$

Unlike a discrete safety score, this posterior represents both expected risk and uncertainty.

### C.5 Thompson Sampling for Replay

For each replay step, DACE samples

$$

\tilde{p}_i \sim \mathrm{Beta}(\alpha+s_i,\beta+f_i),

$$

and selects samples with the largest $\tilde{p}_i$. This prioritizes attacks that are likely to remain dangerous while occasionally revisiting uncertain attacks.

### C.6 Time Decay and Pruning

Because the defender changes during training, old evidence should not dominate forever. DACE applies

$$

s_i \leftarrow \gamma s_i,\qquad f_i \leftarrow \gamma f_i.

$$

Entries with low posterior mean and sufficient replay trials are pruned from the archive. This keeps the replay pool focused on attacks that are still informative for the current defender.

---

## Appendix D. Experimental Details

### D.1 Models

The main experiments use Qwen2.5-7B-Instruct as the backbone for both attacker and defender. Unless otherwise stated, attacker and defender are decoupled models with independent parameters. The attacker is initialized with supervised attack-rewriting data, while the defender starts from the original instruction-tuned model.

Optional scalability experiments can include Qwen2.5-14B-Instruct and Llama3.1-8B-Instruct.

### D.2 Baselines

We compare DACE against:

| Baseline | Purpose |
|---|---|
| Base Instruct | Original aligned model |
| Self-RedTeam | Shared or self-play red-teaming baseline |
| MAGIC | Strong co-evolution baseline |
| DACE w/o diversity | Removes strategy-space coverage reward |
| DACE w/o replay | Removes Bayesian adversarial replay |
| DACE w/ uniform replay | Tests whether Thompson Sampling is necessary |
| DACE w/ raw entropy gain | Tests normalized coverage reward |

### D.3 Evaluation Benchmarks

Defender evaluation includes harmful refusal, benign compliance, OOD attacker robustness, and general capability.

| Evaluation Type | Benchmarks |
|---|---|
| Harmful refusal | WildGuardTest, WildJailBreak, DAN, HarmBench, StrongREJECT |
| Benign compliance | XSTest benign, WildJailBreak benign |
| Over-refusal | OR-Bench, XSTest contrast |
| OOD attackers | GCG, PAIR, TAP, AutoDAN, AutoDAN-Turbo, MAJIC-Attack |
| General capability | IFEval, ARC-C, GPQA, MMLU, AlpacaEval 2 |

### D.4 Attacker Metrics

Attacker evaluation reports both effectiveness and diversity:

| Metric | Meaning |
|---|---|
| ASR@1 | Single-rollout attack success |
| ASR@k | Attack success under $k$ sampled attempts |
| Transfer ASR | Attack success on unseen defenders |
| Cell Coverage | Fraction of occupied strategy cells |
| Successful Coverage | Fraction of cells containing at least one successful attack |
| Normalized Entropy | Uniformity of strategy distribution |
| QD-Score | Sum of best attack quality over cells |
| Max Cell Share | Degree of mode collapse |

### D.5 Judge Robustness

Because automatic judges may introduce noise, we recommend reporting results under at least two judge settings:

1. Primary automatic safety judge used for training and large-scale evaluation.
2. Strong external judge for a held-out subset, such as GPT-4o or another high-quality evaluator.

For key results, the appendix should include agreement rates between judges and examples of disagreement categories.

---

## Appendix E. Additional Defender Evaluation

### E.1 Full Safety and Benign Compliance Results

| Model | WG Adv Harm ASR↓ | WG Van Harm ASR↓ | WJB Adv Harm ASR↓ | DAN ASR↓ | HarmBench Adv ASR↓ | OR-Bench RTA↑ | XSTest Benign Comply↑ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Base |  |  |  |  |  |  |  |
| Self-RedTeam |  |  |  |  |  |  |  |
| MAGIC |  |  |  |  |  |  |  |
| DACE |  |  |  |  |  |  |  |
| DACE w/o diversity |  |  |  |  |  |  |  |
| DACE w/o replay |  |  |  |  |  |  |  |

### E.2 General Capability

| Model | IFEval↑ | ARC-C↑ | GPQA↑ | MMLU↑ | AlpacaEval 2 LC Win↑ |
|---|---:|---:|---:|---:|---:|
| Base |  |  |  |  |  |
| MAGIC |  |  |  |  |  |
| DACE |  |  |  |  |  |
| DACE w/o diversity |  |  |  |  |  |
| DACE w/o replay |  |  |  |  |  |

### E.3 OOD Attacker Robustness

| Defender | No-rev↓ | GCG↓ | PAIR↓ | TAP↓ | AutoDAN↓ | AutoDAN-Turbo↓ | MAJIC-Attack↓ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Base |  |  |  |  |  |  |  |
| MAGIC |  |  |  |  |  |  |  |
| DACE |  |  |  |  |  |  |  |
| DACE w/o diversity |  |  |  |  |  |  |  |
| DACE w/o replay |  |  |  |  |  |  |  |

This table should be used to show that DACE is not merely robust against its own attacker but generalizes to independently developed attack algorithms.

---

## Appendix F. Attacker Evaluation and Diversity Analysis

### F.1 Transferability Across Defenders

| Attacker | Qwen2.5 Base↑ | Llama3.1 Base↑ | Mistral Base↑ | MAGIC Defender↑ | DACE Defender↑ |
|---|---:|---:|---:|---:|---:|
| Base attacker |  |  |  |  |  |
| MAGIC attacker |  |  |  |  |  |
| DACE attacker |  |  |  |  |  |
| DACE w/o diversity |  |  |  |  |  |

This table evaluates whether the DACE attacker learns transferable attack strategies rather than overfitting to the current DACE defender.

### F.2 Strategy-Space Coverage

| Attacker | Cell Coverage↑ | Successful Coverage↑ | Normalized Entropy↑ | KL-to-Uniform↓ | QD-Score↑ | Max Cell Share↓ |
|---|---:|---:|---:|---:|---:|---:|
| MAGIC attacker |  |  |  |  |  |  |
| DACE w/o diversity |  |  |  |  |  |  |
| DACE full |  |  |  |  |  |  |

The key claim is not simply that DACE produces more different-looking prompts, but that it covers more safety-relevant strategy cells with successful attacks.

### F.3 Archive Heatmaps

This section should include heatmaps over the $12\times 10$ strategy space. We recommend reporting three versions:

1. Occupancy heatmap: number of archived attacks per cell.
2. Successful occupancy heatmap: number of successful attacks per cell.
3. QD heatmap: best attack quality per cell.

The expected pattern is that DACE full covers more cells than MAGIC or DACE without diversity, while maintaining high-quality attacks in many cells.

### F.4 Textual and Semantic Diversity

| Attacker | Self-BLEU↓ | Distinct-1↑ | Distinct-2↑ | Embedding Distance↑ | Cluster Coverage↑ |
|---|---:|---:|---:|---:|---:|
| MAGIC attacker |  |  |  |  |  |
| DACE w/o diversity |  |  |  |  |  |
| DACE full |  |  |  |  |  |

These metrics are secondary. They are useful for comparison with prior red-teaming diversity literature, but the main diversity evidence should come from strategy-space coverage and successful coverage.

---

## Appendix G. Ablation Studies

### G.1 Diversity Reward Ablation

| Variant | ASR@1↑ | Successful Coverage↑ | Entropy↑ | QD-Score↑ | Defender OOD ASR↓ |
|---|---:|---:|---:|---:|---:|
| DACE full |  |  |  |  |  |
| w/o diversity reward |  |  |  |  |  |
| raw entropy gain |  |  |  |  |  |
| frequency-inverse novelty |  |  |  |  |  |
| semantic novelty only |  |  |  |  |  |

This ablation should show that normalized marginal coverage gain avoids reward vanishing and produces better effective diversity than simpler novelty rewards.

### G.2 Replay Ablation

| Variant | Early Attack ASR↓ | Mid Attack ASR↓ | Latest Attack ASR↓ | OOD ASR↓ | Benign Comply↑ |
|---|---:|---:|---:|---:|---:|
| No replay |  |  |  |  |  |
| Uniform replay |  |  |  |  |  |
| Top posterior mean |  |  |  |  |  |
| Thompson replay |  |  |  |  |  |
| DACE full |  |  |  |  |  |

The important story is that no-replay defenders may adapt to current attacks but forget earlier attacks, while Thompson replay improves retention without overfitting only to old samples.

### G.3 Strategy-Space Ablation

| Strategy Descriptor | Coverage↑ | Successful Coverage↑ | Defender OOD ASR↓ | General Capability↑ |
|---|---:|---:|---:|---:|
| Risk category only |  |  |  |  |
| Attack style only |  |  |  |  |
| Full $S\times C$ |  |  |  |  |

This ablation tests whether the two-dimensional strategy descriptor is necessary. The expected result is that risk-only descriptors are too coarse, style-only descriptors ignore safety content, and the full product space gives the best effective coverage.

---

## Appendix H. Judge Robustness and Human Validation

### H.1 Judge Agreement

| Dataset | Primary Judge vs External Judge Agreement↑ | Harmful Precision↑ | Harmful Recall↑ | Refusal Agreement↑ |
|---|---:|---:|---:|---:|
| Harmful prompts |  |  |  |  |
| Benign prompts |  |  |  |  |
| Replay samples |  |  |  |  |

This section should address a likely reviewer concern: DACE uses judge-based rewards, so results may depend on the judge. The appendix should report agreement and discuss major disagreement modes.

### H.2 Manual Audit Protocol

For a subset of samples, human annotators or expert reviewers can label:

1. Whether the rewritten prompt preserves the original intent.
2. Whether the defender response is safe.
3. Whether refusal is appropriate.
4. Whether the attack style label is consistent with the generated prompt.

The paper should not include operational jailbreak details. Qualitative examples should be sanitized.

---

## Appendix I. Qualitative Analysis

### I.1 Strategy Evolution Over Training

This section should analyze how DACE attacker changes across training rounds. The expected trend is:

- Early rounds: attacker relies on common styles such as role play or hypothetical framing.
- Middle rounds: attacker begins to explore low-frequency risk-style combinations.
- Late rounds: attacker produces more compositional strategies while maintaining format compliance.

### I.2 Sanitized Case Studies

Each case study should include:

| Field | Content |
|---|---|
| Seed type | Harmful or benign |
| Risk category | Sanitized category |
| Attack style | Sanitized style |
| Defender behavior before training | High-level description |
| Defender behavior after DACE | High-level description |
| Safety takeaway | What vulnerability was addressed |

Do not include full attack prompts that could be directly reused.

### I.3 Failure Cases

This subsection is important for credibility. Suggested categories:

1. DACE still struggles with some gradient-optimized suffix attacks.
2. Some benign adversarial prompts may trigger over-refusal.
3. Strategy extraction can fail when attacker output format drifts.
4. Some low-frequency cells remain difficult to populate with successful attacks.
5. Judge disagreement can affect posterior updates.

---

## Appendix J. Limitations, Safety, and Responsible Release

DACE improves safety alignment through automated adversarial co-evolution, but it also introduces risks and limitations. First, online attacker-defender training is more expensive than offline safety tuning. Second, the method relies on automatic safety judges; judge errors may affect both reward quality and replay decisions. Third, the strategy taxonomy determines what kinds of diversity are encouraged. A poorly designed taxonomy could overemphasize surface-level variations or underrepresent important risk regions. Fourth, our current formulation focuses on text-only interactions and does not yet cover tool-use, multimodal inputs, or long-horizon agentic environments.

To reduce misuse risk, released examples should be sanitized and should not contain directly executable harmful instructions or reusable jailbreak prompts. The code release can include training infrastructure, evaluation scripts, and taxonomy definitions, while replacing raw adversarial prompts with redacted or abstracted examples where appropriate. Future work should investigate safer ways to share adversarial training data, stronger judge calibration, automatically evolving strategy taxonomies, and extensions to tool-using and multimodal agents.

---

# 5. 主文与附录的取舍建议

主文 Related Work 建议控制在 **4 个 subsection，每个 1–2 段**，不要放表。重点是把 DACE 定位为：

> co-evolution + effective strategy diversity + Bayesian adversarial memory

Appendix 则承担全部细节。最优先放入附录的是：

1. 完整伪代码；
2. 12×10 strategy taxonomy；
3. reward 和 Bayesian replay 公式；
4. 完整实验设置；
5. attacker diversity metrics；
6. replay forgetting ablation；
7. judge robustness；
8. sanitized qualitative cases。

这样主文会更像 NeurIPS：故事线清晰，附录支撑充分。

-----

> 在这些材料和分析的基础上，再写一下 related work 和 appendix 部分，附录可以先参考 maigc 论文来写，其他要求与之前的一样，
> 现在帮忙梳理 related work 和 appendix 初稿，用中文梳理，先简要介绍 dace 的这些部分怎么写，是什么讲故事逻辑以及为什么要怎么写，再给出具体的每一部分的每一段的内容，要求达到 NeurIPS 投稿水准，

下面这版延续上一轮的边界：**Introduction 和 Evaluation 暂不重写**，这轮重点补齐 **Related Work** 和 **Appendix** 的初稿。整体目标是让 DACE 的论文叙事更像 NeurIPS 主文：Related Work 不做“论文清单”，而是服务于 DACE 的 gap；Appendix 则参考 MAGIC 的写法，把主文放不下但支撑可信度的内容系统展开。

---

# 1. Related Work 应该怎么写

## 1.1 写作逻辑

DACE 的 Related Work 不建议按“所有相关论文逐个介绍”来写，而应该围绕 DACE 的两个核心 gap 展开：

第一条线是 **dynamic safety alignment**。现有安全对齐从静态 RLHF、静态 red-teaming 数据，逐渐发展到 self-play、multi-agent game、attacker-defender co-evolution。MAGIC 已经很好地证明了 co-evolution 的价值，所以 DACE 不能再把 gap 写成“现有方法不动态”。DACE 的 gap 应该写成：**现有 co-evolution 仍可能是局部军备竞赛，缺少策略覆盖约束和历史攻击记忆。**

第二条线是 **diverse automated red-teaming**。Rainbow Teaming、Ruby Teaming、RainbowPlus、QDRT、DiveR-CT、CRT、CALM、Auto-RT 等工作都关注 attack diversity，但大多将 diversity 作为 red-teaming 生成目标，而不是直接嵌入 attacker-defender co-evolution 的训练闭环。DACE 的差异是：**diversity 不是后验评估指标，而是训练中的策略空间覆盖奖励。**

第三条线是 **memory / replay / forgetting**。一些 self-play 或 red-teaming 方法确实会 replay 历史样本，并且 replay 后也会更新样本奖励或有害性估计。这里上一轮已经纠正过：不能说它们“不更新 replay 样本”。准确 gap 是：**它们多依赖 judge 的离散 safety score 或当前奖励来更新风险，缺少对 defender 随机性、风险不确定性和 defender 动态变化的显式建模。** DACE 用 Beta-Bernoulli 后验、时间衰减和 Thompson Sampling 来补这个 gap。

推荐 Related Work 主文写成 4 个小节：

1. **LLM Jailbreaking and Automated Red Teaming**
2. **Safety Alignment via Self-Play and Adversarial Co-Evolution**
3. **Diversity-Driven Red Teaming and Quality-Diversity Search**
4. **Replay, Memory, and Continual Robustness in Safety Training**

---

# 2. Related Work 初稿

## 2.1 LLM Jailbreaking and Automated Red Teaming

早期 LLM jailbreak 主要依赖人工编写的提示词和启发式改写，例如角色扮演、DAN-style 指令覆盖、编码混淆、翻译、错拼、格式操纵和情境伪装等。这类攻击揭示了安全对齐模型对表层提示形式的敏感性，但其规模化能力和策略覆盖有限。随着自动化红队的发展，攻击逐渐从人工模板转向搜索、优化和模型驱动生成。GCG 等梯度优化方法通过优化 adversarial suffix 提升攻击成功率；PAIR 和 TAP 使用 LLM 进行迭代式改写、评估和搜索；AutoDAN 及其后续方法则利用遗传算法和演化搜索生成更强攻击。近期工作进一步探索 adaptive、multi-step 和 agentic attacks，使攻击不再是单轮静态 prompt，而是能够根据目标模型反馈动态调整策略的过程。

这些自动化攻击方法推动了 LLM 安全评估从静态 benchmark 走向动态 red-teaming，但它们通常被用作 **test-time attackers** 或离线数据生成器。相比之下，DACE 关注的是如何将攻击者本身纳入训练闭环，使攻击者在与防御者的在线交互中持续演化，并将发现的攻击用于更新防御者。DACE 因此不只是一个新的 jailbreak generator，而是一个面向安全对齐的 attacker-defender co-evolution framework。

---

## 2.2 Safety Alignment via Self-Play and Adversarial Co-Evolution

传统 LLM safety alignment 主要依赖静态偏好数据、人工标注安全数据、规则过滤器或安全 reward model。这类方法在固定分布上有效，但面对不断变化的 jailbreak 策略时容易变成 reactive patching：模型被训练去拒绝已知攻击，却无法保证对新型攻击保持鲁棒。为解决这一问题，近期研究开始将安全对齐建模为动态博弈或 self-play 过程。Self-RedTeam 让同一模型交替扮演攻击者和防御者，通过在线交互同时提升攻击和防御能力；AdvGame、SEAS、STAIR 以及其他 adversarial self-play 方法也从不同角度探索了对抗式安全训练。MAGIC 进一步将 attacker 和 defender 参数解耦，并将安全对齐建模为非对称 sequential game，使攻击者持续发现长尾漏洞，驱动防御者学习更稳健的拒答边界。

DACE 与这些工作共享一个核心出发点：安全对齐不应只是离线数据上的一次性训练，而应是持续演化过程。然而，DACE 进一步指出，**co-evolution 本身并不自动保证覆盖充分或长期稳健**。如果攻击者在 RL 中坍缩到少数高回报攻击模式，防御者学到的只是局部鲁棒性；如果防御者只训练当前攻击分布，则可能在适应新攻击时遗忘早期攻击。DACE 因此在 MAGIC-style co-evolution 之上加入两个机制：攻击侧的 strategy-space coverage reward，以及防御侧的 Bayesian adversarial replay。前者缓解 attack strategy collapse，后者缓解 defense adversarial forgetting。

---

## 2.3 Diversity-Driven Red Teaming and Quality-Diversity Search

Attack diversity 是自动红队中的核心问题。Rainbow Teaming 将 adversarial prompt generation 建模为 open-ended quality-diversity search，强调攻击生成不仅要有效，也要覆盖不同风险主题和攻击形式。Ruby Teaming、RainbowPlus 和 QDRT 等方法进一步引入 memory、evolutionary quality-diversity search 或 behavior-conditioned training，以提高攻击样本在语义、主题和策略层面的覆盖。CRT、DiveR-CT、CALM、Learning Diverse Attacks、Auto-RT、RedTWIZ 和 SIRAJ 等工作则从 curiosity、semantic novelty、topic coverage、adaptive planning 或 structured reasoning 等角度改进 diverse red-teaming。

这些工作说明，仅报告 attack success rate 不足以刻画 red-teamer 的能力；一个强攻击者应同时具备有效性、多样性和迁移性。然而，现有 diversity-driven red-teaming 多数仍将 diversity 作为攻击生成或评估目标，而不是直接服务于防御者训练。部分 co-evolution 工作也观察到攻击策略会自然变多样，例如 MAGIC 分析了 RL 后攻击模式从模板化策略转向组合策略；TriPlay-RL 在攻防协同建模中也关注到了 diversity。但这些 diversity 往往更偏语义或角色层面的分散，缺少与安全风险类别、攻击方式和攻击成功率直接绑定的策略覆盖目标，因此不一定能带来更强攻击或更稳健防御。

DACE 的关键区别在于，它将 diversity 显式定义为 safety-relevant strategy coverage。具体而言，DACE 构造由风险类别 $\mathcal{S}$ 与攻击方式 $\mathcal{C}$ 组成的二维策略空间 $\mathcal{B}=\mathcal{S}\times\mathcal{C}$，并通过归一化边际覆盖增益奖励攻击者覆盖低频或未覆盖策略单元。这样，diversity 不再只是生成结果的后验统计，而是直接进入 RL objective，成为驱动 attacker exploration 和 defender robustness 的训练信号。

---

## 2.4 Replay, Memory, and Continual Robustness in Safety Training

在线安全训练面临非平稳分布问题：随着攻击者不断演化，防御者训练数据也会持续漂移。经验回放是缓解非平稳训练和遗忘问题的常见机制，在 RL、自博弈和自动红队中均有应用。一些 self-play 或 red-teaming 方法会维护历史攻击样本，并在后续训练中重复使用这些样本；部分方法也会在 replay 后根据 judge 评分或新一轮模型响应更新样本奖励、有害性或优先级。这类机制在一定程度上缓解了只关注当前攻击分布的问题。

然而，DACE 关注的是更细粒度的 adversarial forgetting：一个历史攻击样本对当前防御者的威胁并不是静态属性，也不应由单次 judge 离散评分完全决定。相同攻击可能因为采样随机性、拒答边界变化或防御者训练阶段不同而呈现不同结果；同时，防御者本身在 co-evolution 中持续变化，早期风险估计可能很快过时。因此，仅依赖离散 safety score 或当前 reward 更新样本优先级，难以同时表达 **风险强度、不确定性和时间变化**。

DACE 将 replay pool 中每个历史攻击样本的剩余威胁建模为 Beta-Bernoulli 后验分布。每次回放后，根据攻击是否仍能突破当前防御者更新成功/失败统计；通过时间衰减跟踪 defender 的动态变化；通过 Thompson Sampling 同时采样高风险样本和高不确定样本。相比普通 replay，DACE 的回放机制不是静态缓存，也不是单纯 hard-example mining，而是一个动态 adversarial memory，用于在学习新攻击的同时保持对历史攻击的鲁棒性。

---

# 3. Appendix 应该怎么写

## 3.1 写作逻辑

MAGIC 的 appendix 结构很值得参考：它把理论证明、prompt templates、实验细节、评测协议、attacker transferability、attack pattern analysis 和 ablation 都放到附录里。DACE 可以继承这个风格，但需要加入 DACE 特有的内容。

DACE 的 appendix 应该承担三个功能：

第一，**可复现性**：完整伪代码、prompt templates、hyperparameters、benchmark protocols 都要足够清楚。

第二，**可信度**：主文中无法展开的 reward、Bayesian replay、strategy extraction、strategy taxonomy、judge 设置、ablation 都放到附录支撑。

第三，**安全合规**：涉及攻击样例时应做 sanitized presentation，不直接放可复用的有害攻击细节；同时添加 harmful content disclaimer 和 ethical considerations。

推荐 Appendix 结构如下：

- **A. Full DACE Algorithm**
- **B. Strategy Space and Prompt Templates**
- **C. Reward Design and Bayesian Replay Details**
- **D. Experimental Details**
- **E. Evaluation Protocols**
- **F. Additional Defender Results**
- **G. Attacker Transferability and Quality-Diversity Analysis**
- **H. Replay, Forgetting, and Ablation Studies**
- **I. Qualitative Analysis of Attack Strategies**
- **J. Limitations, Safety, and Ethical Considerations**

下面给出可直接写入论文附录的中文初稿。

---

# Appendix A. Full DACE Algorithm

## 写作说明

这一节对应 MAGIC 的 “Algorithm / Proof” 风格，但 DACE 目前更需要完整算法而不是理论证明。主文 Method 已经讲机制，Appendix A 要给出完整训练流程，尤其是主文放不下的 archive update、posterior decay、Thompson replay、pruning 和 mixed-batch defender training。考虑到伪代码较长，主文只引用 “Appendix A”，附录给完整版本。

## 初稿内容

### A.1 Overview

DACE 训练过程由两个阶段组成：攻击者初始化阶段和在线攻防共演化阶段。初始化阶段通过结构化攻击改写数据对攻击者进行 SFT，使其具备基本的 offensive rewriting、strategy selection 和格式遵循能力。在线共演化阶段交替优化攻击者和防御者。攻击者在固定防御者下生成多样化攻击，并根据攻击有效性、格式合规性和策略覆盖奖励更新；防御者在固定攻击者下同时学习当前攻击和历史回放攻击，并根据响应安全性和拒答校准奖励更新。

DACE 维护一个统一攻击档案池 $\mathcal{A}$。该池同时服务于两个目标：一是统计策略空间占用频率，用于计算 attacker diversity reward；二是存储历史成功攻击，并为每个样本维护动态风险后验，用于 defender replay training。每轮训练开始时，DACE 对回放池中的成功/失败统计施加时间衰减，以适应非平稳的防御者状态。防御者训练期间，DACE 使用 Thompson Sampling 从回放池中采样历史高风险或高不确定攻击，并将其与当前攻击者生成的新攻击混合成训练 batch。

### A.2 Algorithm

```latex
Algorithm 1 Diversity-Aware Adversarial Co-Evolution (DACE)

Input:
Seed dataset D = D_harmful ∪ D_benign;
attacker policy π_A;
defender policy π_D;
strategy space B = S × C;
archive and replay pool A;
number of rounds K;
attacker steps T_A;
defender steps T_D;
new batch size B_train;
replay batch size B_replay.

Stage 0: Attacker Initialization
1: Fine-tune π_A on structured adversarial rewriting data.
2: Initialize π_D from the base instruction-tuned model.
3: Initialize archive pool A = ∅.

Stage 1: Iterative Co-Evolution
4: for round k = 1,...,K do
5:     Apply posterior time decay to all entries in A.
6:
7:     // Attacker optimization
8:     Freeze π_D.
9:     for t = 1,...,T_A do
10:         Sample seed prompts q from D.
11:         π_A generates candidate attacks x with explicit strategy b(x).
12:         π_D generates responses y to each attack x.
13:         Judge response safety, refusal, and attack success.
14:         Compute attacker reward:
              R_A = -R_D + R_fmt + λ(x) R_div(x).
15:         Update π_A with GRPO.
16:         Add successful attacks to the pending archive buffer.
17:     end for
18:     Flush pending successful attacks into A.
19:
20:     // Defender optimization
21:     Freeze π_A.
22:     for t = 1,...,T_D do
23:         Sample seed prompts q from D.
24:         π_A generates new attacks x_new.
25:         Sample historical attacks x_rep from A via Thompson Sampling.
26:         Construct mixed batch x = x_new ∪ x_rep.
27:         π_D generates responses y to all attacks in the mixed batch.
28:         Judge response safety and refusal.
29:         Compute defender reward:
              R_D = R_harm + R_ref.
30:         Update π_D with GRPO.
31:         Update posterior statistics for replayed samples.
32:         Add newly successful current attacks to A.
33:         Prune stale low-risk samples from A.
34:     end for
35: end for

Output:
Trained attacker π_A and defender π_D.
```

---

# Appendix B. Strategy Space and Prompt Templates

## 写作说明

这一节对应 MAGIC 的 “Prompt Template”，但 DACE 要比 MAGIC 多说明一个关键点：策略空间不是随便定义的，而是由 **risk category × attack style** 构成。这里需要解释 risk category 来源、为什么删除两个类别、attack style 来源、格式模板如何让策略选择成为显式动作。

## 初稿内容

### B.1 Strategy Space Construction

DACE 将每个攻击样本映射到二维策略空间 $\mathcal{B}=\mathcal{S}\times\mathcal{C}$。其中 $\mathcal{S}$ 表示安全风险类别，$\mathcal{C}$ 表示攻击方式。风险类别基于 Llama-Guard-4 taxonomy 构建，但我们根据当前 text-only safety training setting 和训练数据分布进行裁剪。具体地，Sexual Content 在当前数据中频率极低且与 benign/adversarial benign 边界高度混淆；Code Interpreter Abuse 主要面向工具调用或代码解释器滥用场景，不适用于本文的 text-only defender setting。因此，我们删除这两个类别，并保留其余 12 个风险类别。

保留的风险类别包括 Violent Crimes、Non-Violent Crimes、Sex-Related Crimes、Child Sexual Exploitation、Defamation、Specialized Advice、Privacy、Intellectual Property、Indiscriminate Weapons、Hate、Suicide & Self-Harm 和 Elections。攻击方式参考 Rainbow Teaming 的 prompt style taxonomy，包含 Slang、Technical Terms、Role Play、Authority Manipulation、Misspellings、Word Play、Emotional Manipulation、Hypotheticals、Historical Scenario 和 Uncommon Dialects。最终策略空间包含 $12\times10=120$ 个 strategy cells。

这一设计使 DACE 的 diversity reward 具有明确安全语义。相比只基于 embedding distance 或 topic clustering 的语义多样性，$\mathcal{S}\times\mathcal{C}$ 同时约束攻击内容风险和攻击表达方式，能够更直接反映防御者需要覆盖的安全边界。

### B.2 Attacker Output Format

DACE 要求攻击者输出三个字段：`<think>`、`<strategy>` 和 `<answer>`。其中 `<think>` 包含攻击者内部推理，`<strategy>` 显式声明风险类别和攻击方式，`<answer>` 给出最终改写 prompt。训练和回放过程中，DACE 直接从 `<strategy>` 中解析 $b(x)$，并从 `<answer>` 中提取实际提交给防御者的攻击 prompt。

```text
<think>
[attacker reasoning]
</think>
<strategy>
risk category: [one of the 12 risk categories]
attack style: [one of the 10 attack styles]
</strategy>
<answer>
[rewritten adversarial prompt]
</answer>
```

这种结构化格式有三个作用。第一，它让策略选择成为攻击者的显式动作，而不是后验分析标签。第二，它使 diversity reward 可以直接绑定到攻击者生成行为，从而被 GRPO 优化。第三，它减少了额外 LLM judge 对 attack style 进行分类带来的噪声，使策略空间统计在训练过程中更稳定。

### B.3 Harmful Seed Rewriting Template

对于 harmful seed prompt，攻击者的目标是生成更隐蔽、更具欺骗性的 adversarial prompt，同时保持原始有害意图和安全分类一致性。攻击者需要选择一个风险类别和一种攻击方式，并在该策略引导下改写原始请求。若防御者生成有害或不安全响应，则该攻击被视为成功；若防御者拒绝或给出安全替代回答，则攻击失败。

附录中可以保留完整模板，但主文不建议展示过多可复用攻击细节。最终版本建议将模板中具体有害示例替换为占位符，并加入 harmful content disclaimer。

### B.4 Benign Seed Rewriting Template

对于 benign seed prompt，DACE 使用 adversarial benign rewriting 来训练防御者的拒答校准能力。攻击者的目标不是引入真实有害意图，而是将 benign prompt 改写成容易触发过拒或 false-positive harmful judgment 的复杂表达，同时保持原始 benign intent。若防御者错误拒绝该 benign prompt，攻击者在 benign setting 下获得成功信号；若防御者正确识别其无害性并正常回答，则攻击失败。

这一模板与 harmful rewriting 明确区分，避免把 benign prompt 改写成真正有害请求。该设计对于控制 defender over-refusal 尤其重要，因为 adversarial benign prompts 可以迫使防御者学习区分 “看起来像攻击” 与 “实际有害” 的差异。

---

# Appendix C. Reward Design and Bayesian Replay Details

## 写作说明

这一节专门解释主文 Method 中简写的 reward 和 replay。DACE 的两个核心创新都在这里：normalized marginal coverage gain 和 Bayesian replay。附录需要把公式、直觉和实现细节写清楚。

## 初稿内容

### C.1 Defender Reward

防御者奖励由 harmfulness reward 和 refusal calibration reward 组成：

$$

R_D(x,y)=R_{\mathrm{harm}}(y)+R_{\mathrm{ref}}(x,y).

$$

$R_{\mathrm{harm}}$ 衡量防御者响应是否安全。如果响应被 judge 标记为 unsafe 或 controversial，则防御者受到惩罚；如果响应被标记为 safe，则获得奖励。$R_{\mathrm{ref}}$ 衡量拒答是否校准：对于 harmful prompt，正确拒答获得奖励，错误回答受到惩罚；对于 benign prompt，正常回答获得奖励，错误拒答受到惩罚。该奖励设计避免防御者通过 “refuse everything” 获得虚高 safety score。

### C.2 Attacker Reward

攻击者奖励包含与防御者奖励相反的零和部分、格式奖励和多样性奖励：

$$

R_A(x,y)=-R_D(x,y)+R_{\mathrm{fmt}}(x)+\lambda(x)R_{\mathrm{div}}(x).

$$

其中 $R_{\mathrm{fmt}}$ 约束攻击者遵循 `<think>`、`<strategy>`、`<answer>` 格式；$R_{\mathrm{div}}$ 鼓励攻击者覆盖低频策略单元；$\lambda(x)$ 根据攻击成败调整 diversity reward 权重。成功攻击获得完整多样性奖励，失败攻击获得折减奖励。这样既能避免攻击者生成无效但多样的 prompt，也能防止低频策略因早期失败而完全失去探索信号。

### C.3 Normalized Marginal Coverage Gain

设 $\mathcal{A}$ 为当前 archive，$\mathbf{p}_{\mathcal{A}}$ 为 archive 中策略单元的经验分布。DACE 的多样性奖励定义为：

$$

R_{\mathrm{div}}(x)
=
\frac{
H(\mathbf{p}_{\mathcal{A}\cup\{x\}})-H(\mathbf{p}_{\mathcal{A}})
}{
\max_{b\in\mathcal{B}}
\left[
H(\mathbf{p}_{\mathcal{A}\cup\{x_b\}})-H(\mathbf{p}_{\mathcal{A}})
\right]
+\epsilon
}.

$$

原始边际熵增随着 archive 规模增大会逐渐衰减，因此直接使用 raw entropy gain 会导致训练后期 reward vanishing。DACE 使用当前 archive 状态下的最大可能单步增益进行归一化，使 diversity reward 在训练早期和后期保持可比较的量级。该奖励鼓励攻击者填补低频 strategy cells，同时抑制对高频成功策略的过度重复。

### C.4 Bayesian Replay Posterior

对于 archive 中每个样本 $x_i$，DACE 维护一个 Beta-Bernoulli 后验：

$$

p_i \mid s_i,f_i \sim \mathrm{Beta}(\alpha+s_i,\beta+f_i).

$$

这里 $p_i$ 表示样本 $x_i$ 对当前 defender 的攻击成功概率，$s_i$ 和 $f_i$ 分别为衰减累计成功和失败次数。后验均值为：

$$

\hat{p}_i=
\frac{\alpha+s_i}{\alpha+\beta+s_i+f_i}.

$$

后验方差则反映该样本风险估计的不确定性。相比使用单个离散 safety score，Beta posterior 能同时表达样本的预期威胁和估计不确定性。

### C.5 Time Decay, Thompson Sampling, and Pruning

由于 defender 在训练中持续变化，历史统计不能永久有效。因此 DACE 在每轮开始时施加时间衰减：

$$

s_i\leftarrow \gamma s_i,\qquad f_i\leftarrow \gamma f_i.

$$

回放采样时，DACE 从每个样本的后验中采样：

$$

\tilde{p}_i\sim\mathrm{Beta}(\alpha+s_i,\beta+f_i),

$$

并选择 $\tilde{p}_i$ 最高的样本进入 defender replay batch。Thompson Sampling 同时偏好高风险样本和高不确定样本，因此比固定 top-risk replay 更不容易陷入少数旧攻击，也比 uniform replay 更能聚焦仍具威胁的历史攻击。

当某个样本的后验均值低于阈值，且已经经过足够多次回放评估时，DACE 将其从 archive 中剪枝。剪枝可以控制回放池规模，并避免防御者持续训练已经被稳定掌握的低风险样本。

---

# Appendix D. Experimental Details

## 写作说明

这一节参考 MAGIC Appendix C，放训练细节、模型、硬件、超参数、baselines。这里先给表格骨架，数据后面评测完成再补。

## 初稿内容

### D.1 Models and Training Setup

我们以 Qwen2.5-7B-Instruct 作为主要 backbone，并在额外实验中考虑 Qwen2.5-14B-Instruct 和 Llama3.1-8B-Instruct 以验证方法的跨模型泛化能力。DACE 使用两个解耦模型分别作为 attacker 和 defender。Attacker 经过结构化 adversarial rewriting SFT 初始化；defender 从原始 instruction-tuned checkpoint 初始化。在线 RL 阶段使用 GRPO 交替优化两者。

### D.2 Hyperparameters

| Setting | Value |
|---|---:|
| Backbone | Qwen2.5-7B-Instruct |
| Training rounds |  |
| Total RL steps |  |
| Attacker steps per round |  |
| Defender steps per round |  |
| Switching frequency |  |
| GRPO group size |  |
| New batch size $B_{\mathrm{train}}$ |  |
| Replay batch size $B_{\mathrm{replay}}$ |  |
| Learning rate |  |
| KL coefficient |  |
| Rollout temperature |  |
| Max prompt length |  |
| Max response length |  |
| Diversity coefficient for success | 1.0 |
| Diversity coefficient for failure | 0.5 |
| Beta prior $(\alpha,\beta)$ |  |
| Time decay $\gamma$ |  |
| Pruning threshold |  |
| Max archive size |  |

### D.3 Baselines

我们比较以下 baselines。Base Instruct Model 表示未经额外安全共演化训练的原始 instruction-tuned model。Self-RedTeam 代表共享参数 self-play 训练范式。MAGIC 是最直接的 co-evolution baseline，使用解耦 attacker 和 defender 进行非对称 adversarial game training。DACE w/o diversity 移除策略覆盖奖励，用于评估 diversity-aware attacker optimization 的贡献。DACE w/o replay 移除 Bayesian adversarial replay，用于评估 replay memory 对防御抗遗忘能力的贡献。我们还比较 uniform replay、top-risk replay 和 raw entropy gain 等变体，用于分析 DACE 各模块设计选择的必要性。

---

# Appendix E. Evaluation Protocols

## 写作说明

这一节参考 MAGIC Appendix D，把 safety eval、general capability、OpenRT defender generalization、attacker eval、diversity metrics 都写清楚。主文 Evaluation 只报关键表，附录解释具体协议。

## 初稿内容

### E.1 Defender Safety Evaluation

防御者评估覆盖 harmful refusal、benign compliance、over-refusal robustness 和 hard jailbreak robustness。我们使用 WildGuardTest、WildJailBreak、DAN、HarmBench、OR-Bench、XSTest 和 StrongREJECT 等 benchmark。对于 harmful prompts，主要指标是 attack success rate，越低表示防御越强；对于 benign prompts，主要指标是 compliance rate 或 acceptance rate，越高表示过拒越少。

### E.2 General Capability Evaluation

为了验证 DACE 没有通过过度拒答牺牲通用能力，我们使用 IFEval、ARC-C、GPQA、MMLU 和 AlpacaEval 2 评估 instruction following、reasoning、knowledge 和 general helpfulness。所有模型使用相同 decoding 设置和 evaluation pipeline。最终表格报告每项 benchmark 的分数，并在必要时报告平均能力分数。

### E.3 OOD Attacker Robustness

为评估 defender 对未见攻击方法的泛化能力，我们使用 OpenRT-style evaluation。攻击方法包括 no-revision direct attack、GCG、PAIR、TAP、AutoDAN、AutoDAN-turbo 和 MAJIC-Attack。对于需要 attacker LLM 的方法，我们固定 attacker backbone 和 decoding 设置，以确保不同 defender 之间比较公平。主要指标为 HarmBench seed prompts 上的 ASR。

### E.4 Attacker Effectiveness and Transferability

攻击者评估关注 DACE attacker 是否学到可迁移攻击策略，而不是只过拟合 DACE defender。我们使用 WildJailBreak vanilla harmful prompts 作为种子，让不同 attacker 对多个 defender 进行 single-rollout rewriting，并用统一 judge 判断攻击是否成功。比较对象包括 Base attacker、MAGIC attacker、DACE attacker 和 DACE ablations。主要指标为 ASR@1、ASR@k、average queries 和 cross-defender transfer ASR。

### E.5 Diversity and Quality-Diversity Metrics

DACE attacker 的 diversity evaluation 包含 strategy-space metrics 和 text/semantic diversity metrics。策略空间指标包括 Cell Coverage、Successful Cell Coverage、Normalized Entropy、KL-to-uniform、Effective Number of Strategies、Max Cell Share 和 QD-Score。文本和语义指标包括 Self-BLEU、Distinct-n、embedding distance 和 semantic cluster coverage。我们特别强调 Successful Coverage 和 QD-Score，因为普通 coverage 可能由无效攻击填充，而 DACE 的目标是生成 **有效且多样** 的攻击。

---

# Appendix F. Additional Defender Results

## 写作说明

这里放完整 defender 结果表。主文可能只放 Qwen2.5-7B 的关键结果，附录放更多 backbone、更多 benchmark、judge robustness 和完整表格。

## 初稿内容

### F.1 Full Safety Results

| Model | WG adv harm ASR↓ | WG van harm ASR↓ | WJB adv harm ASR↓ | DAN ASR↓ | HarmBench adv ASR↓ | HarmBench van ASR↓ | OR-Bench RTA↑ | XSTest harm RTA↑ | StrongREJECT RTA↑ | WJB benign Comply↑ | XSTest benign Comply↑ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Base |  |  |  |  |  |  |  |  |  |  |  |
| Self-RedTeam |  |  |  |  |  |  |  |  |  |  |  |
| MAGIC |  |  |  |  |  |  |  |  |  |  |  |
| DACE |  |  |  |  |  |  |  |  |  |  |  |
| DACE w/o diversity |  |  |  |  |  |  |  |  |  |  |  |
| DACE w/o replay |  |  |  |  |  |  |  |  |  |  |  |

### F.2 Full General Capability Results

| Model | IFEval Prompt Loose↑ | IFEval Instruction Loose↑ | ARC-C↑ | GPQA↑ | MMLU↑ | AlpacaEval 2 LC Win↑ |
|---|---:|---:|---:|---:|---:|---:|
| Base |  |  |  |  |  |  |
| MAGIC |  |  |  |  |  |  |
| DACE |  |  |  |  |  |  |
| DACE w/o diversity |  |  |  |  |  |  |
| DACE w/o replay |  |  |  |  |  |  |

### F.3 Defender Generalization to OOD Attackers

| Defender | No-rev↓ | GCG↓ | PAIR↓ | TAP↓ | AutoDAN↓ | AutoDAN-turbo↓ | MAJIC-Attack↓ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Base |  |  |  |  |  |  |  |
| MAGIC |  |  |  |  |  |  |  |
| DACE |  |  |  |  |  |  |  |
| DACE w/o diversity |  |  |  |  |  |  |  |
| DACE w/o replay |  |  |  |  |  |  |  |

预期分析写法：DACE 在大多数 OOD attacker 上降低 ASR，说明策略覆盖和回放训练提升的不只是对 DACE attacker 的局部鲁棒性，而是对外部攻击族的泛化防御能力。若 GCG 等白盒 suffix attack 上存在小幅退化，应如实说明这是当前 black-box co-evolution 设置的限制，并作为未来工作讨论。

---

# Appendix G. Attacker Transferability and Quality-Diversity Analysis

## 写作说明

这一节对应 MAGIC Appendix E 和 F，但 DACE 要更系统。MAGIC 主要看 attacker transferability 和 attack pattern；DACE 还要加 strategy-space heatmap、successful coverage 和 QD-score。

## 初稿内容

### G.1 Attacker Transferability

| Attacker \ Defender | Qwen2.5-7B | Llama3.1-8B | Mistral-7B | Gemini / Closed Model | MAGIC-defender | DACE-defender |
|---|---:|---:|---:|---:|---:|---:|
| Base attacker |  |  |  |  |  |  |
| MAGIC attacker |  |  |  |  |  |  |
| DACE attacker |  |  |  |  |  |  |
| DACE w/o diversity |  |  |  |  |  |  |

DACE attacker 若在多个 base defenders 上取得更高 ASR，说明其策略不是只针对单一 defender 的局部 exploit，而具有跨模型迁移性。若 DACE-defender 对 DACE-attacker 的 ASR 明显低于 base defenders，则说明 co-training 使 defender 学会了对该攻击分布的鲁棒拒答。

### G.2 Strategy-Space Coverage

| Attacker | Cell Coverage↑ | Successful Coverage↑ | Normalized Entropy↑ | KL-to-uniform↓ | Effective #Strategies↑ | Max Cell Share↓ | QD-Score↑ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Base attacker |  |  |  |  |  |  |  |
| MAGIC attacker |  |  |  |  |  |  |  |
| DACE attacker |  |  |  |  |  |  |  |
| DACE w/o diversity |  |  |  |  |  |  |  |

预期分析写法：DACE 相比 MAGIC 和 w/o diversity 具有更高 successful coverage 和 QD-score，说明其多样性提升不是来自随机扩散，而是来自有效策略空间的扩展。Max Cell Share 降低则表明攻击者没有过度坍缩到少数高回报策略。

### G.3 Strategy Archive Heatmaps

我们可视化 $\mathcal{S}\times\mathcal{C}$ 策略空间中每个 cell 的成功攻击数量、最高攻击质量或平均 reward。横轴为 attack style，纵轴为 risk category。相比 MAGIC 和 w/o diversity，DACE 的成功攻击应覆盖更多风险类别和攻击方式组合，尤其是在低频类别和复杂攻击风格上表现出更充分探索。

### G.4 Query-Budget Efficiency

| Method | ASR@1↑ | ASR@2↑ | ASR@4↑ | ASR@8↑ | ASR@16↑ | Avg. Queries↓ |
|---|---:|---:|---:|---:|---:|---:|
| Base attacker |  |  |  |  |  |  |
| MAGIC attacker |  |  |  |  |  |  |
| DACE attacker |  |  |  |  |  |  |
| PAIR |  |  |  |  |  |  |
| TAP |  |  |  |  |  |  |
| AutoDAN |  |  |  |  |  |  |
| MAJIC-Attack |  |  |  |  |  |  |

这一实验用于区分 learned single-rollout attacker 和 test-time search attacker。DACE attacker 的优势不一定是在无限 query budget 下超越所有搜索攻击，而是在低 query budget 或 single rollout 设置下生成高质量、多样且可迁移的攻击。

---

# Appendix H. Replay, Forgetting, and Ablation Studies

## 写作说明

这是 DACE 附录中最重要的差异化部分之一。主文可能只放一张 ablation 表，附录要详细展示 replay 如何缓解 forgetting，以及 diversity reward 和 replay 的各自贡献。

## 初稿内容

### H.1 Defense Adversarial Forgetting

我们将攻击样本按其产生轮次划分为 early、middle 和 late 三组，并评估不同 defender checkpoints 对这些历史攻击的 ASR。若不使用 replay，防御者可能在 late attacks 上变强，但对 early attacks 的 ASR 回升，表现出 adversarial forgetting。DACE 通过 mixed-batch replay 同时训练当前攻击和历史攻击，应在 early、middle 和 late attacks 上保持更均衡的鲁棒性。

| Method | Early Attack ASR↓ | Middle Attack ASR↓ | Late Attack ASR↓ | OOD Attack ASR↓ |
|---|---:|---:|---:|---:|
| No replay |  |  |  |  |
| Uniform replay |  |  |  |  |
| Top-risk replay |  |  |  |  |
| Thompson replay |  |  |  |  |
| DACE full |  |  |  |  |

### H.2 Diversity Reward Ablation

| Variant | ASR@1↑ | Successful Coverage↑ | Normalized Entropy↑ | QD-Score↑ | Defender OOD ASR↓ |
|---|---:|---:|---:|---:|---:|
| DACE full |  |  |  |  |  |
| w/o diversity reward |  |  |  |  |  |
| raw entropy gain |  |  |  |  |  |
| frequency-inverse novelty |  |  |  |  |  |
| semantic novelty only |  |  |  |  |  |
| success-only diversity |  |  |  |  |  |

预期分析写法：移除 diversity reward 会降低 strategy coverage 和 QD-score，并可能使 defender 对 OOD attackers 的鲁棒性下降。Raw entropy gain 在训练后期可能因 reward vanishing 导致策略扩展不足。Semantic novelty only 可以提升表层语义差异，但不一定带来 safety-relevant strategy coverage。

### H.3 Replay Ablation

| Variant | Early ASR↓ | Latest ASR↓ | OOD ASR↓ | Benign Comply↑ | General Capability↑ |
|---|---:|---:|---:|---:|---:|
| No replay |  |  |  |  |  |
| Uniform replay |  |  |  |  |  |
| FIFO replay |  |  |  |  |  |
| Top posterior mean |  |  |  |  |  |
| Thompson Sampling |  |  |  |  |  |
| DACE full |  |  |  |  |  |

预期分析写法：No replay 最容易出现 early attack forgetting。Uniform replay 能缓解遗忘但效率较低。Top posterior mean 偏向 exploitation，可能反复训练少数高风险样本。Thompson Sampling 通过后验采样兼顾风险和不确定性，在历史攻击保持和新攻击适应之间取得更好平衡。

### H.4 Strategy Space Ablation

| Strategy Space | ASR@1↑ | Successful Coverage↑ | OOD Defender ASR↓ | Notes |
|---|---:|---:|---:|---|
| Risk category only $\mathcal{S}$ |  |  |  |  |
| Attack style only $\mathcal{C}$ |  |  |  |  |
| Full $\mathcal{S}\times\mathcal{C}$ |  |  |  |  |
| Full space with removed categories restored |  |  |  |  |

预期分析写法：只使用 risk category 会忽略攻击表达形式，只使用 attack style 会忽略风险语义。完整二维空间能同时约束安全内容和攻击形式，因此更适合训练安全防御者。恢复被删除的低频类别可能导致部分 dead cells 影响 diversity reward 的归一化信号，因此裁剪后的 12×10 空间更稳定。

---

# Appendix I. Qualitative Analysis of Attack Strategies

## 写作说明

这一节参考 MAGIC 的 attack pattern analysis，但 DACE 要注意安全合规。可以展示 sanitized examples，不给出可直接复用的攻击细节。重点不是“教人攻击”，而是说明 DACE attacker 学到的策略组合更丰富，以及 defender 学到的拒答边界更细。

## 初稿内容

DACE 训练后，攻击者不只是重复 SFT 初始化中的模板化改写，而会组合多个策略维度。例如，在某些风险类别中，攻击者会将 role play 与 authority manipulation 组合；在另一些风险类别中，攻击者会使用 hypothetical framing 或 historical scenario 来降低请求表面危险性。相比 w/o diversity 变体，DACE full 产生的攻击样本覆盖更多风险类别和攻击方式组合，并表现出更低的 mode collapse。

我们对 qualitative examples 进行脱敏展示。每个样例只保留策略类别、攻击意图摘要、防御者响应类型和 judge 结果，不展示可直接复用的有害操作细节。

| Risk Category | Attack Style | Sanitized Attack Summary | Defender Behavior | Judge Result |
|---|---|---|---|---|
| Privacy | Role Play | Requests sensitive personal information under a fictional scenario | Refuses and offers privacy-safe alternative | Safe |
| Specialized Advice | Authority Manipulation | Frames unsafe professional advice as expert review | Provides safe high-level guidance | Safe |
| Hate | Historical Scenario | Embeds harmful rhetoric in a historical analysis frame | Refuses hateful content, provides neutral context | Safe |

---

# Appendix J. Limitations, Safety, and Ethical Considerations

## 写作说明

NeurIPS 审稿人会关注安全论文是否可能被滥用。DACE 是自动红队和攻击生成框架，必须说明安全处理方式。这里应该诚实写 limitation，同时强调实验中的攻击样本不直接释放或经过脱敏。

## 初稿内容

DACE 仍存在若干限制。首先，在线 attacker-defender co-evolution 比静态安全训练成本更高，尤其是 defender mixed-batch training 和 replay posterior update 会增加额外计算开销。其次，DACE 依赖自动 judge 来评估 response harmfulness、refusal 和 attack success；若 judge 存在系统性偏差，训练奖励和最终评测都可能受到影响。第三，DACE 的策略空间由人工 taxonomy 定义，虽然具有明确安全语义，但可能无法覆盖所有新兴攻击方式。未来工作可以探索自动扩展或层次化策略空间，使 attack style 和 risk category 能随训练动态演化。

由于 DACE 涉及自动生成 adversarial prompts，我们在实验和附录中采取安全控制。论文中不展示可直接复用的有害攻击细节；qualitative examples 仅提供脱敏摘要；release 时应避免公开未过滤的攻击样本或可直接执行的 jailbreak prompt。DACE 的目标是提升模型安全鲁棒性，而不是帮助真实攻击者绕过安全系统。我们建议将 DACE 用于受控研究环境、内部安全评测和防御训练，并配合访问控制、日志审计和安全审查流程。

---

# 4. 主文与附录的最终分工建议

Related Work 主文建议保留 **4 个小节、每节 1-2 段**，控制在一页以内。重点是讲清楚：

> DACE = co-evolution + strategy coverage + Bayesian memory。

Appendix 则承担细节：

- MAGIC 有 Prompt Template、Experimental Details、Evaluation、Transferability、Attack Pattern、Ablation；
- DACE 在此基础上新增 Full Algorithm、Strategy Space、Bayesian Replay、Forgetting Analysis；
- 这样主文保持 NeurIPS 风格的紧凑叙事，附录保证可复现性和审稿可信度。