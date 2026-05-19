# LLM Safety/Diversity 相关论文详细分析报告

本报告对五篇与 LLM 红队测试（Red Teaming）和多样性（Diversity）相关的重要论文进行深入分析，涵盖每篇论文的动机、目标、方法，并对涉及 diversity 考量的论文给出额外详细介绍。

---

## 目录
1. [Rainbow Teaming: Open-Ended Generation of Diverse Adversarial Prompts (NeurIPS 2024)](#1-rainbow-teaming)
2. [Curiosity-driven Red-teaming for Large Language Models (ICLR 2024)](#2-curiosity-driven-red-teaming)
3. [Jailbreak-R1: Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning](#3-jailbreak-r1)
4. [DiveR-CT: Diversity-enhanced Red Teaming with Relaxing Constraints (AAAI 2025)](#4-diver-ct)
5. [Evolving Diverse Red-team Language Models in Multi-round Multi-agent Games](#5-evolving-diverse-red-team)
6. [综合对比与总结](#6-综合对比)

---

## 1. Rainbow Teaming: Open-Ended Generation of Diverse Adversarial Prompts {#1-rainbow-teaming}

**会议/期刊**: NeurIPS 2024  
**作者**: Mikayel Samvelyan, Sharath Chandra Raparthy, Andrei Lupu 等 (Meta AI)

### 1.1 研究动机

随着大语言模型（LLMs）在各种实际应用中的广泛部署，理解和增强其对抗鲁棒性变得至关重要。现有的对抗提示识别方法存在以下关键局限：

- **领域特定性**：大多数方法只关注特定领域的攻击
- **缺乏多样性**：现有自动化红队方法在 attack success rate (ASR) 和多样性之间存在严重的权衡
- **人工标注依赖**：需要大量人工参与或预定义的攻击模板
- **模式崩溃**：基于目标优化的方法容易导致生成重复的攻击提示

### 1.2 研究目标

开发一种能够自动生成**既有效又多样化**的对抗提示的黑盒方法，用于：
1. 诊断 LLM 的安全漏洞
2. 生成高质量合成数据以增强模型鲁棒性
3. 实现开放式的自我改进机制

### 1.3 方法框架

Rainbow Teaming 将对抗提示生成问题转化为**质量-多样性（Quality-Diversity, QD）搜索问题**，基于 MAP-Elites 演化算法构建。

#### 核心组件

**1. Archive 结构**

定义一个 \(K\)-维离散网格（archive），每个维度对应一个预定义的**特征描述符（Feature Descriptor）**：

\[
z = \langle c_1, c_2, \ldots, c_K \rangle
\]

其中 \(c_i\) 表示第 \(i\) 个特征的类别。特征可以是：
- **分类特征**：如风险类别（Risk Category）、攻击风格（Attack Style）
- **数值特征**：如提示长度（Length），被离散化为区间

**2. 迭代搜索过程**

每次迭代包含以下步骤：

1. **选择（Selection）**：从 archive 中采样一个父提示 \(x\) 及其描述符 \(z\)，并选择目标描述符 \(z'\)
2. **变异（Mutation）**：使用 Mutator LLM \(\pi_M\) 生成新的候选提示：
   \[
   x' \sim \pi_M(\cdot | x, z')
   \]
   变异包含两阶段：
   - 风险变异：将提示改写为指定的风险类别
   - 风格变异：注入指定的攻击风格

3. **多样性过滤**：使用 BLEU 分数过滤与父提示过于相似的候选：
   \[
   \text{sim}(x, x') < \tau \quad (\text{默认} \tau = 0.6)
   \]

4. **目标查询**：将候选提示提交给目标 LLM \(\pi_T\) 获取响应

5. **评估**：使用 Judge LLM \(\pi_J\) 评估响应的有害性作为适应度函数 \(f\)

6. **Archive 更新**：如果新提示比当前单元格的提示表现更好，则替换

**3. 算法伪代码**

```
Algorithm: Rainbow Teaming
Input: Target π_T, Mutator π_M, Judge π_J, features, iterations
Output: Archive of adversarial prompts

Initialize archive with seed prompts
for i = 1 to iterations do
    Sample parent prompt x and descriptor z from archive
    Sample target descriptor z' (biased by fitness)
    Generate candidate x' = Mutate(x, z', π_M)
    if sim(x, x') < τ then
        response = π_T(x')
        fitness = π_J(x', response)
        if fitness > archive[z'].fitness then
            archive[z'] ← (x', fitness)
        end if
    end if
end for
return archive
```

### 1.4 Diversity 详细介绍 ⭐

Rainbow Teaming 的多样性机制是其核心创新，主要体现在以下几个方面：

#### 1.4.1 结构化多样性空间

通过预定义的特征维度显式构建多样性空间：

| 特征类型 | 示例 | 作用 |
|---------|------|------|
| **Risk Category** | Criminal Planning, Violence and Hate, Self-Harm, Sexual Content 等 | 覆盖不同类型的安全风险 |
| **Attack Style** | Authority Manipulation, Role Play, Hypothetical Scenarios, Emotional Appeal 等 | 覆盖不同的攻击策略 |
| **Prompt Length** | 离散化的字符数区间 | 覆盖不同复杂度的攻击 |

最终的 archive 大小为所有特征类别数的乘积。例如，使用 11 个风险类别和 11 个攻击风格，可生成 \(11 \times 11 = 121\) 个不同的对抗提示。

#### 1.4.2 QD 搜索的多样性优势

传统的最大化 ASR 方法容易陷入局部最优，而 QD 搜索有以下优势：

1. **显式多样性优化**：算法目标不仅是找到最有效的攻击，而是填充整个 archive
2. **Stepping Stones 效应**：某一类别的有效攻击可以作为"垫脚石"，通过小的修改发现其他类别的有效攻击
3. **避免模式崩溃**：每个单元格只保留一个最优解，防止重复

#### 1.4.3 多样性度量

论文使用多种指标评估生成提示的多样性：

\[
\text{Self-BLEU} = \frac{1}{n} \sum_{i=1}^{n} \text{BLEU}(x_i, X \setminus x_i)
\]

较低的 Self-BLEU 表示更高的多样性。此外还使用 BERTScore、ROUGE-L 和 gzip 压缩比等指标。

#### 1.4.4 实验结果

| 模型 | ASR (GPT-4) | ASR (Llama Guard) | 多样性保持 |
|------|-------------|-------------------|-----------|
| Llama 2-chat 7B | >90% | >90% | ✓ |
| Llama 2-chat 13B | >90% | >90% | ✓ |
| Llama 3-Instruct | >90% | >90% | ✓ |

---

## 2. Curiosity-driven Red-teaming for Large Language Models (CRT) {#2-curiosity-driven-red-teaming}

**会议/期刊**: ICLR 2024  
**作者**: Zhang-Wei Hong, Idan Shenfeld 等 (MIT, IBM Research)

### 2.1 研究动机

现有的基于强化学习的自动红队方法存在严重的**多样性问题**：

- RL 方法倾向于生成少量高效的测试用例，导致**覆盖率低**
- 一旦发现有效攻击，策略会反复利用相同的模式
- 无法充分探索可能引发不良响应的提示空间

### 2.2 研究目标

通过引入**好奇心驱动探索（Curiosity-driven Exploration）**机制，增加生成测试用例的覆盖率和多样性，同时保持或提升攻击效果。

### 2.3 方法框架

#### 核心思想

将红队测试中的覆盖率提升问题与 RL 中的好奇心驱动探索方法联系起来，通过优化新颖性来鼓励策略发现未见过的测试用例。

#### 训练目标

在标准的红队 RL 目标基础上，加入熵奖励和新颖性奖励：

\[
\mathcal{L}(\theta) = \mathbb{E}_{\pi_\theta}\left[ R_{\text{toxic}}(x, z) + \lambda_E \log \pi(x|z) + \sum_i \lambda_i B_i(x) \right] - \beta \text{KL}(\pi_\theta \| \pi_{\text{ref}})
\]

其中：
- \(R_{\text{toxic}}(x, z)\)：毒性奖励，评估目标模型响应的有害程度
- \(\log \pi(x|z)\)：熵奖励，鼓励生成多样化的输出
- \(B_i(x)\)：新颖性奖励，激励发现新的测试用例
- KL 惩罚：保持与参考策略的一致性

#### 新颖性奖励设计

CRT 提出多种新颖性奖励计算方式：

**1. 基于嵌入的新颖性**：计算新生成提示与历史嵌入的余弦相似度

\[
B_{\text{embed}}(x) = 1 - \max_{x' \in \mathcal{X}_{\text{history}}} \cos(\phi(x), \phi(x'))
\]

**2. 基于 N-gram 的新颖性**：使用 n-gram 统计衡量语言层面的新颖性

### 2.4 Diversity 详细介绍 ⭐

#### 2.4.1 好奇心驱动探索的理论基础

好奇心驱动探索源自 RL 中解决稀疏奖励问题的内在动机研究。核心思想是：

> 当外部奖励稀疏或信号不足时，通过内在奖励鼓励智能体探索新状态/行为。

在红队测试场景中：
- **外部奖励**：成功引发有害响应
- **内在奖励**：发现新颖的攻击提示

#### 2.4.2 与传统 RL 红队方法的对比

| 方法 | 多样性 | 有效性 | 覆盖率 |
|------|--------|--------|--------|
| 传统 RL (Perez et al.) | 低 | 高（但重复） | 低 |
| CRT | 高 | 高或更高 | 高 |

#### 2.4.3 关键发现

1. **多样性提升有效性**：好奇心驱动探索不仅增加多样性，还能发现更多有效的攻击（因为探索了更广的空间）
2. **可应用于已对齐模型**：即使对经过 RLHF 精调的 LLaMA2 模型，CRT 也能成功发现引发毒性响应的提示
3. **小模型攻击大模型**：仅用 137M 参数的 GPT-2 作为红队模型，就能成功攻击 LLaMA2-7B-chat

#### 2.4.4 局限性

- 随着历史嵌入库增长，基于全历史的语义距离计算会导致**新颖性停滞（Novelty Stagnation）**
- 这一问题在后续的 DiveR-CT 工作中得到解决

---

## 3. Jailbreak-R1: Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning {#3-jailbreak-r1}

**状态**: Preprint (arXiv 2506.00782)  
**作者**: Weiyang Guo 等

### 3.1 研究动机

现有的自动红队方法面临三个主要挑战：

1. **缺乏先验知识**：RL 难以从零开始发现有效的攻击提示
2. **陷入局部最优**：RL 倾向于过拟合奖励，反复生成几乎相同的成功攻击
3. **稀疏奖励信号**：越狱任务中的直接奖励信号稀缺，影响模型学习

### 3.2 研究目标

设计一个能够自动探索和生成**多样且有效**的越狱攻击的红队训练框架，同时平衡攻击成功率和多样性。

### 3.3 方法框架

Jailbreak-R1 采用**三阶段训练策略**：

#### 阶段一：冷启动（Cold Start）

通过模仿学习构建冷启动数据，将先验越狱知识注入模型：

1. 使用 GPT-4 对现有越狱提示进行改写和扩展
2. 对红队模型进行监督微调（SFT）

#### 阶段二：预热探索（Warm-up Exploration）

使用 GRPO（Group Relative Policy Optimization）算法训练，引入多样性和一致性奖励：

**一致性奖励**：确保生成的攻击与目标一致
\[
R_{\text{consis}} = \mathbb{I}[\text{Prompt}(y) \approx \text{Prompt}(x)]
\]

**多样性奖励**：鼓励组间多样性
\[
R_{\text{div}} = \frac{\text{Rank}(y, Y)}{|Y|}
\]

其中 \(\text{Rank}(y, Y)\) 根据 Self-BLEU 和嵌入相似度排序，多样性越高排名越靠前。

**组合奖励**：
\[
R = \alpha \cdot R_{\text{consis}} + \beta \cdot R_{\text{div}}
\]

#### 阶段三：增强越狱（Enhanced Jailbreak）

引入渐进式奖励（Progressive Rewards）解决稀疏奖励问题：

1. 通过逐步加入毒性数据，获得 \(n\) 个安全能力逐渐降低的中间目标模型：\(\pi_{tgt_1}, \pi_{tgt_2}, \ldots, \pi_{tgt_n}\)
2. 使用课程学习策略，从容易到困难逐步训练
3. 奖励信号稳定增长而非波动

### 3.4 Diversity 详细介绍 ⭐

#### 3.4.1 GRPO 中的多样性机制

Jailbreak-R1 巧妙地利用 GRPO 的组比较机制来促进多样性：

- 对每个攻击目标 \(x\)，生成一组攻击提示 \(\{y_1, y_2, \ldots, y_G\}\)
- 计算组内相似度，奖励与其他提示差异大的攻击

#### 3.4.2 多样性奖励的计算

\[
R_{\text{div}}(y) = \frac{\text{Rank}(y, Y)}{|Y|}
\]

排序标准：
\[
\text{Score}(y) = \frac{S_{\text{SelfBLEU}}(y) + S_{\text{embed}}(y)}{2}
\]

分数越低（与其他提示差异越大），排名越高，多样性奖励越大。

#### 3.4.3 实验效果

| 指标 | Jailbreak-R1 | 基线方法 |
|------|-------------|---------|
| 攻击成功率 | 最优 | 较低 |
| 多样性 | 最优 | 较低 |
| 效率 | 平均提升 28% | - |
| 成本 | 仅需 34% | 100% |

#### 3.4.4 消融研究

- **无冷启动**：ASR 降低 10.1%，多样性降低 10.7%
- **无预热阶段**：多样性略有下降，但一致性降低更多

---

## 4. DiveR-CT: Diversity-enhanced Red Teaming with Relaxing Constraints {#4-diver-ct}

**会议/期刊**: AAAI 2025 (Oral)  
**作者**: Andrew Zhao, Quentin Xu 等 (清华大学, BIGAI)

### 4.1 研究动机

现有自动红队方法存在两个关键问题：

1. **最大化偏差**：过度关注最大化 ASR，忽视了生成语义丰富的测试查询的重要性
2. **新颖性停滞**：CRT 等方法使用历史嵌入的余弦相似度作为语义多样性奖励，但随着历史增长，这种方法会导致新颖性停滞

### 4.2 研究目标

通过**放松约束（Relaxing Constraints）**的策略，在保持可控 ASR 的同时显著增强生成数据的多样性，从而：
1. 在不同 ASR 水平下都能生成更多样化的攻击
2. 通过生成的数据更好地增强蓝队模型的安全性
3. 实现可控的 ASR 动态调节
4. 减少奖励过优化问题

### 4.3 方法框架

#### 核心创新 1：约束优化框架

将传统的奖励最大化重新构建为**约束优化问题**：

**传统方法**：
\[
\max_\theta \mathbb{E}_{\pi_\theta}[R_{\text{unsafe}} + R_{\text{diversity}}]
\]

**DiveR-CT**：
\[
\max_\theta \mathbb{E}_{\pi_\theta}[R_{\text{diversity}}] \quad \text{s.t.} \quad R_{\text{unsafe}} \geq d_{\text{safe}}
\]

将 unsafe 奖励作为阈值约束而非最大化目标，赋予策略更大的自由度来优化多样性。

#### 核心创新 2：动态语义奖励（k-NN 奖励）

**CRT 的问题**：
\[
R_{\text{CRT}} = 1 - \cos(\phi(x_{t+1}), \phi(x_t))
\]

当新生成的提示与历史最后一个提示接近时，CRT 仍给予高奖励（因为只关注相邻差异）。

**DiveR-CT 的解决方案**：
\[
R_{\text{kNN}} = 1 - \frac{1}{k} \sum_{x' \in \mathcal{N}_{k,\phi}(x, \mathcal{X}_{\text{history}})} \cos(\phi(x), \phi(x'))
\]

其中 \(\mathcal{N}_{k,\phi}\) 表示在历史嵌入中找到的 \(k\) 个最近邻。

**关键优势**：
- 动态更新语义目标
- 防止智能体利用单个离群解
- 随着历史增长，奖励信号保持有效

#### 核心创新 3：乱码约束

将乱码惩罚（Gibberish Penalty）从奖励最大化改为约束：
\[
R_{\text{gibberish}} \geq d_{\text{gib}}
\]

这样策略有更多容量用于最大化新颖性奖励。

### 4.4 Diversity 详细介绍 ⭐

#### 4.4.1 CRT vs DiveR-CT 的多样性机制对比

| 方面 | CRT | DiveR-CT |
|------|-----|----------|
| 语义奖励计算 | 与上一个生成的相似度 | 与 k 个最近邻的平均相似度 |
| 目标更新 | 静态（相对于最后一个） | 动态（随历史更新） |
| 新颖性随时间 | 停滞 | 持续 |
| ASR 控制 | 通过系数平衡 | 通过阈值约束 |

#### 4.4.2 多样性度量指标

DiveR-CT 使用全面的多样性评估体系：

**1. 词汇多样性**
- Self-BLEU（越高越好）
- Distinct-k（k-gram 唯一性比例）
- Entropy-k（k-gram 分布熵）

**2. 语义多样性**
- Vendi-Ngram
- Vendi-Semantic
- Semantic Mean（平均语义距离）

**3. 分布相似性**
- BLEU-2/3/4（与人工红队数据集的相似度）
- MS-Jaccard（多集合 Jaccard 相似度）

#### 4.4.3 实验结果对比

在不同 ASR 水平下的多样性表现：

| 方法 | ASR | Self-BLEU ↑ | Vendi-Ngram ↑ | Distinct-1 ↑ |
|------|-----|-------------|---------------|--------------|
| RL (Perez) | ~0.88 | 0.037 | 0.148 | 0.004 |
| CRT | ~0.86 | 0.570 | 0.559 | 0.037 |
| **DiveR-CT** | ~0.86 | **0.746** | **0.964** | **0.103** |

#### 4.4.4 Safety Tuning 效果

使用 DiveR-CT 生成的数据进行安全微调，蓝队模型展现出：
- 更高的拒绝率（更安全）
- 不损害一般能力（OpenLLM 基准）
- 在多个红队测试基准上表现更好

---

## 5. Evolving Diverse Red-team Language Models in Multi-round Multi-agent Games {#5-evolving-diverse-red-team}

**状态**: arXiv 2310.00322 (多次修订)  
**作者**: Chengdong Ma, Zichen Wang 等 (北京大学)

### 5.1 研究动机

现有红队方法存在以下局限：

1. **静态攻防**：主要依赖单轮提示设计，针对固定蓝队进行单边优化
2. **缺乏理论基础**：没有严格的数学形式化，难以量化多样性或保证收敛
3. **模式崩溃**：在复杂的人机交互中难以发现潜在风险

### 5.2 研究目标

建立基于博弈论的红队测试框架，通过多轮多智能体博弈：
1. 分析红蓝队的动态攻防交互
2. 理论保证收敛到近似纳什均衡
3. 缓解模式崩溃，发现多样化攻击策略

### 5.3 方法框架

#### 红队博弈（Red Team Game, RTG）

将红队测试形式化为双人零和博弈：

- **红队语言模型（RLM）**：生成对抗提示
- **蓝队语言模型（BLM）**：生成（可能有害的）响应

目标是找到纳什均衡，双方都达到最优策略。

#### 博弈论形式化

**状态空间**：对话历史 \(H_t = (u_1, r_1, \ldots, u_t, r_t)\)

**动作空间**：
- RLM: 生成攻击提示 \(u_{t+1}\)
- BLM: 生成响应 \(r_{t+1}\)

**收益函数**：基于响应的毒性评分

#### Gamified Red-team Solver (GRTS)

GRTS 是一个迭代求解算法，包含以下关键组件：

**1. 策略优化**

使用 PPO 等算法优化 RLM 和 BLM 的策略

**2. 元博弈分析**

构建策略的响应矩阵，使用 \(\alpha\)-rank 或复制动态分析策略分布

**3. 语义多样性度量**

引入多样性度量来缓解模式崩溃：

\[
D(\pi) = \mathbb{E}_{x \sim \pi}[d(x, \mathcal{X}_{\text{history}})]
\]

**4. 收敛保证**

理论证明 GRTS 可以收敛到近似纳什均衡：
\[
\epsilon\text{-Nash Equilibrium}: \max_{\pi'} u(\pi', \pi^*) \leq u(\pi^*, \pi^*) + \epsilon
\]

### 5.4 Diversity 详细介绍 ⭐

#### 5.4.1 Spinning Top 假说

论文揭示了红队任务的几何结构符合"陀螺假说"：

> 多样化的 LLM 种群是异质人类红队专家的有效代理

这意味着：
- 单一攻击策略无法覆盖所有漏洞
- 需要构建多样化的攻击者种群
- 每个攻击者专注于不同的攻击维度

#### 5.4.2 多样性在博弈中的作用

**1. 策略多样性**

在博弈求解过程中，维护一个策略池而非单一策略：

\[
\Pi = \{\pi_1, \pi_2, \ldots, \pi_n\}
\]

**2. 攻击主题多样性**

实验显示 GRTS 能发现多种攻击主题：
- 政治敏感话题
- 暴力内容
- 个人隐私
- 等等

**3. 攻击形式多样性**

不同的攻击策略：
- 角色扮演
- 假设场景
- 情感操纵
- 等等

#### 5.4.3 多轮交互的多样性

多轮对话结构带来独特的多样性维度：

- **上下文多样性**：不同对话历史导致不同攻击路径
- **时序多样性**：攻击可以在后续轮次中成功（首轮失败后）
- **适应性多样性**：攻击者根据蓝队响应调整策略

#### 5.4.4 实验发现

随着 GRTS 迭代求解：
- 语义多样性会因上下文约束略有下降
- 但攻击深度和隐蔽性增加
- 发现的漏洞更加深层和难以检测

---

## 6. 综合对比与总结 {#6-综合对比}

### 6.1 方法对比表

| 论文 | 多样性机制 | 搜索范式 | 多轮支持 | 理论保证 |
|------|-----------|---------|---------|---------|
| Rainbow Teaming | MAP-Elites Archive | QD 演化搜索 | ❌ | QD 收敛 |
| CRT | 好奇心奖励 | RL 探索 | ❌ | ❌ |
| Jailbreak-R1 | GRPO 组多样性 | 三阶段 RL | ❌ | ❌ |
| DiveR-CT | k-NN 语义奖励 + 约束优化 | 约束 RL | ❌ | ❌ |
| RTG/GRTS | 博弈论 + 策略种群 | 博弈求解 | ✅ | Nash 均衡 |

### 6.2 多样性机制分类

**1. 结构化多样性（Rainbow Teaming）**
- 预定义特征空间
- 显式填充 archive
- 可控且可解释

**2. 探索驱动多样性（CRT, DiveR-CT）**
- 内在奖励驱动
- 语义空间探索
- 需要解决新颖性停滞

**3. 组相对多样性（Jailbreak-R1）**
- GRPO 组内比较
- 相对排序奖励
- 计算高效

**4. 博弈论多样性（RTG/GRTS）**
- 策略种群维护
- 均衡求解保证
- 自适应对抗

### 6.3 关键洞见

1. **多样性与有效性不矛盾**：多篇论文证明，提升多样性可以同时提升或维持攻击成功率

2. **Safety Tuning 需要多样性**：仅用高 ASR 但低多样性的数据进行安全微调效果有限

3. **新颖性停滞是关键挑战**：基于历史嵌入的方法需要动态目标更新机制

4. **多轮交互揭示更深层漏洞**：单轮攻击可能遗漏许多安全风险

### 6.4 未来方向

- 自动发现特征维度（而非预定义）
- 多模态红队测试
- 更高效的多样性度量
- 与人类红队的协同

---

*报告完成日期: 2026年1月21日*
