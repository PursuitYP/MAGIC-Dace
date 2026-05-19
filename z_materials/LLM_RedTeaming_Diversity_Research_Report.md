# LLM 红队测试中的 Diversity 提升研究：2024-2026 最新论文综述

## 摘要

本报告深入调研了 2024-2026 年间与 LLM 红队测试（Red Teaming）、LLM 安全对抗及协同进化相关的最新论文，重点关注提升攻击多样性（Diversity）的典型工作。通过对 15+ 篇核心论文的详细分析，本报告系统总结了各方法的动机、目标、核心技术和 diversity 考量，并构建了完整的 diversity 机制分类体系。

---

## 目录

1. [研究背景与动机](#1-研究背景与动机)
2. [核心论文详细分析](#2-核心论文详细分析)
   - 2.1 GFlowNet-based Diverse Attacks (ICLR 2025)
   - 2.2 OpenAI: Diverse and Effective Red Teaming (2024)
   - 2.3 Active Attacks (2025)
   - 2.4 WildTeaming (NeurIPS 2024)
   - 2.5 Ferret (EMNLP 2025)
   - 2.6 RainbowPlus (2025)
   - 2.7 RedTopic (2025)
   - 2.8 RedTWIZ (2025)
3. [Diversity 机制分类与对比](#3-diversity-机制分类与对比)
4. [关键技术创新总结](#4-关键技术创新总结)
5. [Diversity 评估指标体系](#5-diversity-评估指标体系)
6. [未来研究方向](#6-未来研究方向)

---

## 1. 研究背景与动机

### 1.1 为什么 Diversity 如此重要？

在 LLM 红队测试领域，**多样性（Diversity）** 的重要性体现在三个层面：

1. **安全覆盖完整性**：低多样性的攻击只能发现有限的漏洞模式，无法全面评估模型安全边界
2. **Safety Tuning 有效性**：研究表明，用于 safety fine-tuning 的数据若缺乏多样性，训练出的模型鲁棒性差
3. **对抗进化需求**：单一攻击模式容易被防御，多样化攻击才能推动攻防协同进化

### 1.2 现有方法的核心挑战

| 挑战 | 描述 | 影响 |
|------|------|------|
| **Mode Collapse** | RL 训练的攻击者倾向于重复生成高奖励的相似攻击 | 多样性急剧下降 |
| **Novelty Stagnation** | 基于历史相似度的新颖性奖励随历史增长而失效 | CRT 等方法的局限 |
| **Diversity-Effectiveness Trade-off** | 追求多样性往往牺牲攻击成功率 | 难以平衡两个目标 |
| **Topic Redundancy** | Token/句子级多样性无法捕捉主题级重复 | 表面多样实际单调 |

---

## 2. 核心论文详细分析

### 2.1 Learning Diverse Attacks on Large Language Models (ICLR 2025)

**基本信息**
- **作者**: Seanie Lee et al. (KAIST, Mila, Yoshua Bengio)
- **发表**: ICLR 2025
- **关键词**: GFlowNet, Mode Collapse, Off-policy RL

**动机与目标**

现有 RL 方法即使加入显式的多样性正则化，仍然面临严重的 mode collapse 问题或无法生成有效攻击。本文旨在提出一种概率论原则性的方法，同时实现高多样性和高攻击成功率。

**核心方法**

本文将红队测试问题重新定义为**摊销推断（Amortized Inference）**问题：

```
核心洞察：将攻击 prompt 生成视为从后验分布采样潜变量
```

**两阶段训练框架**：

**Stage 1: GFlowNet Fine-tuning**
- 使用 GFlowNet 的 off-policy 目标训练攻击者
- 目标分布定义：π(x) ∝ R(x)^β
- 允许从多模态分布采样，而非仅最大化奖励

训练目标：
$$\mathcal{L}_{GFN}(\theta) = \mathbb{E}_{x \sim \pi_\theta}\left[\left(\log \frac{Z_\theta \pi_\theta(x)}{R(x)}\right)^2\right]$$

**Stage 2: MLE Smoothing**
- 收集 GFlowNet 生成的高奖励 prompts 形成离线数据集
- 使用 MLE 重新训练，平滑分布

**Diversity 考量**

| 机制 | 描述 | 优势 |
|------|------|------|
| 概率性采样 | GFlowNet 按奖励比例采样而非贪婪最大化 | 天然覆盖多模态 |
| Off-policy 训练 | 支持 replay buffer，防止遗忘 | 保持历史多样性 |
| MLE 平滑 | 对所有高奖励样本等权训练 | 避免单一模式主导 |

**实验结果**

在红队测试 Llama-2-7B-chat 时：
- GFlowNet+MLE 是唯一同时达到高毒性率和高多样性的方法
- 生成的攻击具有良好的跨模型迁移性
- 用 GFlowNet 生成的数据进行 safety tuning 后，模型对其他 RL 方法的攻击更鲁棒

---

### 2.2 Diverse and Effective Red Teaming with Auto-generated Rewards (OpenAI, 2024)

**基本信息**
- **作者**: Alex Beutel, Kai Xiao, Johannes Heidecke, Lilian Weng
- **机构**: OpenAI
- **发表**: 2024年12月

**动机与目标**

传统 RL 红队方法面临**多样性-有效性权衡**：
- 纯 RL 方法攻击成功率高但多样性近乎为零
- Few-shot prompting 多样性高但成功率极低

本文目标：设计能同时实现高多样性和高成功率的自动化红队系统。

**核心创新：问题分解**

```
关键洞察：将问题分解为两个子任务
1. 生成多样的攻击目标（Goals）
2. 为每个目标生成有效攻击
```

**方法架构**

**Step 1: 自动生成多样攻击目标**

两种生成方式：
1. **Few-shot Generation**: 使用 LLM 生成多样化的攻击目标
   ```
   示例："hijack a car" vs "launder money" 是完全不同的犯罪建议
   ```

2. **从数据生成**: 将 Anthropic Harmless 数据集转换为 (goal, criteria) 对

**Step 2: 自动生成规则奖励（RBR）**

为每个攻击目标自动生成针对性的判断标准：
$$R_{RBR}(y; x_r) = P(\text{yes} | \text{"Does this text [criteria]?"})$$

**Step 3: Multi-step RL with Style Diversity**

创新的多步强化学习设计：
- 攻击者可进行多轮攻击，每轮基于历史生成新攻击
- 引入**风格子空间多样性奖励**

风格多样性计算：
$$R_{Div} = 1 - \max_{t \in [0,T-1]} \text{sim}(\phi_{style}(p_t), \phi_{style}(p_T))$$

其中风格子空间通过 QR 分解去除目标子空间获得：
$$\phi_{style}(p) = \phi(p) - \phi(p)P$$

**综合奖励**：
$$R = R_{AttSuccess} \times R_{Fewshot} \times R_{Div} \times R_{len}$$

**Diversity 考量**

| 层面 | 机制 | 效果 |
|------|------|------|
| 目标级 | 自动生成多样攻击目标 | 覆盖不同危害类型 |
| 样本级 | Few-shot 相似度约束 | 防止偏离示例太远 |
| 风格级 | Style subspace 多样性 | 避免重复攻击策略 |
| 序列级 | Multi-step RL | 逐步探索新攻击 |

**实验结果**

- 在间接 prompt 注入任务上首次实现自动化红队
- Multi-step RL 随推理步数增加，多样性持续提升
- 在安全性测试任务上，vanilla RL 几乎 100% 成功率但 0 多样性，本方法在保持高成功率的同时显著提升多样性

---

### 2.3 Active Attacks: Red-teaming LLMs via Adaptive Environments (2025)

**基本信息**
- **作者**: Taeyoung Yun et al.
- **发表**: arXiv 2509.21947 (2025年9月)
- **关键词**: Adaptive Environment, Active Learning, Off-policy RL

**动机与目标**

现有多样性导向 RL 方法的关键问题：
```
一旦发现高奖励 prompts，对新区域的探索就会被抑制
→ 多样性主要集中在几个"容易发现"的模式
→ 更难发现的漏洞区域未被充分探索
```

受**主动学习（Active Learning）**范式启发，提出在攻防交互中动态调整环境。

**核心方法：主动攻击**

**关键思想**：通过周期性 safety fine-tuning 改变"受害者"LLM，迫使攻击者探索新区域

**算法流程**：

```
Algorithm: Active Attacks
Input: 攻击者 p_θ, 受害者 p_φ, 分类器 p_ψ, 步数 T, 更新间隔 R
Initialize: Replay buffer B, Prompt dataset D

for t = 1 to T:
    生成攻击 prompt x_t ~ p_θ
    获取受害者响应 y_t ~ p_φ(·|x_t)
    计算奖励 r_t = p_ψ(toxic|x_t, y_t)
    
    if r_t > τ:
        D ← D ∪ {x_t}
    
    B ← B ∪ {(x_t, r_t)}
    
    使用 B 更新攻击者 p_θ (off-policy objective)
    
    if t mod R == 0:
        使用 D 对受害者进行 safety fine-tuning
        D ← ∅  # 清空用于下一轮
```

**为什么 Active Attacks 提升多样性？**

| 机制 | 原理 | 效果 |
|------|------|------|
| 环境适应 | Safety tuning 关闭已发现漏洞 | 强制探索新模式 |
| Off-policy 训练 | GFlowNet 目标 + replay buffer | 防止模式坍塌 |
| 周期性重置 | 攻击数据集周期清空 | 避免累积偏差 |

**Diversity 考量**

- 传统方法（Passive Attacks）：固定环境 → 容易陷入局部最优
- Active Attacks：环境自适应 → 持续推动探索
- 实验表明：多样性随轮数增加持续增长，约 5 轮后收敛

**实验结果**

- 在 Qwen2.5-1.5B-Instruct 上验证
- 分类距离（categorical distance）显著优于基线
- Safety fine-tuning 不损害模型的一般能力

---

### 2.4 WildTeaming at Scale (NeurIPS 2024)

**基本信息**
- **作者**: Liwei Jiang et al. (UW, Allen AI, CMU)
- **发表**: NeurIPS 2024
- **关键词**: In-the-Wild Jailbreaks, Tactic Mining, Compositional Attacks

**动机与目标**

现有红队方法（人工、梯度优化、LLM 迭代修改）存在局限：
- 人工方法昂贵且难以规模化
- 自动方法缺乏真实世界攻击的创造性
- **缺少针对多样性的系统化方法**

本文核心洞察：真实用户在与 chatbot 交互中**自发产生**了大量创意攻击策略！

**核心方法**

**两阶段框架：MINE + COMPOSE**

**Stage 1: MINE（挖掘）**
- 数据源：LMSYS-CHAT-1M, WildChat 等真实对话
- 挖掘结果：**5.7K 独特的越狱战术聚类**
- 战术类型：角色扮演、编码转换、假设场景等

**Stage 2: COMPOSE（组合）**
- 组合不同战术选择形成新攻击
- 使用 Mixtral-8x7B/GPT-4 进行战术组合
- 通过 off-topic 和 low-risk pruning 提升质量

**多样性评估新指标**

本文定义了全新的多样性评估体系：

| 指标 | 定义 | 目标 |
|------|------|------|
| Unique Success | 成功攻击中的唯一数量 | 绝对多样性 |
| Tactic Coverage | 覆盖的战术聚类数 | 策略多样性 |
| Semantic Diversity | 嵌入空间的分散度 | 语义多样性 |

**Diversity 考量**

WildTeaming 的多样性来源于三个层面：
1. **战术多样性**：5.7K 真实世界战术聚类
2. **组合多样性**：随机选择 2-7 个战术组合
3. **语义多样性**：新定义的多样性指标

**实验结果**

- 发现比 SOTA 方法多 **4.6 倍**的唯一成功攻击
- 攻击尝试次数减少 40%
- 创建 WildJailbreak 数据集：262K prompt-response 对
- Safety training 结果：合适的防护而不过度拒绝

---

### 2.5 Ferret: Faster and Effective Automated Red Teaming (EMNLP 2025)

**基本信息**
- **作者**: Tej Deep Pala et al. (DeCLaRe Lab)
- **发表**: EMNLP 2025 Findings
- **关键词**: Multi-mutation, Reward Model Scoring

**动机与目标**

Rainbow Teaming 的关键问题：
- **收敛速度慢**：每次迭代仅生成一个变异
- **资源需求高**：需要大型微调 mutator
- **判断瓶颈**：简单 judge 可能误排名

Ferret 目标：加速并提升 QD 搜索效率。

**核心方法**

**关键创新 1：多变异生成**
```
每次迭代生成 N=5 个变异，而非单一变异
→ 并行探索多个方向
→ 更高效填充 archive
```

**关键创新 2：Reward Model Scoring**

评估多种评分函数：
| 评分方法 | 原理 | 效果 |
|----------|------|------|
| Reward Model | 学习的有害性评分 | **最佳** |
| Llama Guard | 分类器输出 | 次优 |
| LLM-as-Judge | LLM 直接判断 | 较慢 |

使用 Reward Model 对变异排序，选择最有效的 prompt。

**Diversity 考量**

Ferret 继承 Rainbow Teaming 的 QD 框架：
- **Archive 结构**：Risk Category × Attack Style 网格
- **多样性过滤**：BLEU 阈值去重
- **加速收敛**：多变异并行不损害多样性

**实验结果**

对比 Rainbow Teaming：
- ASR 提升：49% → **95%**（+46%）
- 达到 90% ASR 时间减少 **15.2%**
- 生成的 prompts 具有良好跨模型迁移性

---

### 2.6 RainbowPlus: Enhancing Adversarial Prompt Generation (2025)

**基本信息**
- **作者**: Quy-Anh Dang et al.
- **发表**: arXiv 2504.15047 (2025年4月，更新于2026年1月)
- **关键词**: Multi-element Archive, Evolutionary QD

**动机与目标**

Rainbow Teaming 的架构限制：
- **单元素 Archive**：每个 cell 仅存储一个 prompt
- **成对比较**：效率低、可能误判

RainbowPlus 目标：通过进化计算增强 QD 搜索。

**核心方法**

**关键创新 1：多元素 Archive**

```
传统 MAP-Elites：每 cell 存 1 个 elite
RainbowPlus：每 cell 存多个高质量 prompts

优势：
- 保留更多多样性候选
- 支持更广泛的进化探索
```

**关键创新 2：综合适应度函数**

并行评估多个候选：
$$F(p) = P_{harmful}(p) \times \mathbb{1}[\text{diverse}(p)]$$

使用概率评分机制替代成对比较。

**Archive 更新策略**

```python
for cell in archive:
    candidates = generate_mutations(cell.elites, N=5)
    scores = evaluate_fitness(candidates)
    # 保留 top-k 多样化高分 prompts
    cell.elites = select_diverse_top_k(candidates, scores, k=3)
```

**Diversity 考量**

| 机制 | Rainbow Teaming | RainbowPlus |
|------|----------------|-------------|
| Archive 容量 | 单元素/cell | 多元素/cell |
| 选择策略 | 成对比较 | 批量排序 |
| 多样性保持 | 有限 | 增强 |

**实验结果**

- Diverse-Score 达到 **≈0.84**
- 生成 **100 倍**更多唯一 prompts（10,418 vs 100）
- 平均 ASR **81.1%**，超过 AutoDAN-Turbo 3.9%
- 速度提升 **9 倍**（1.45 vs 13.50 小时）

---

### 2.7 RedTopic: Toward Topic-Diverse Red Teaming (2025)

**基本信息**
- **发表**: OpenReview 2025
- **关键词**: Topic Diversity, Multi-objective RL, Contextualized Generation

**动机与目标**

现有方法的关键盲点：
```
Token 级多样性 ≠ Topic 级多样性

例如："make something explosive" 和 "assemble a detonator"
- Token/Sentence 级：高多样性（措辞不同）
- Topic 级：低多样性（都关于爆炸物）

→ 现有方法产生"话题冗余"
```

**核心方法**

**三层多样性框架**

1. **Token Diversity** ($D_{token}$)
   $$D_{token} = 1 - \text{Self-BLEU}(p, P)$$

2. **Sentence Diversity** ($D_{sent}$)
   $$D_{sent} = 1 - \frac{1}{k}\sum_{p' \in \text{kNN}(p)} \cos(\phi(p), \phi(p'))$$

3. **Topic Diversity** ($D_{topic}$) — **本文创新**
   使用 topic embedding 模型计算主题级差异

**Contextualized Adversarial Prompt Generation**

```
传统方法：直接生成有害 prompt
RedTopic：给定真实上下文 q，生成上下文化的有害 prompt p

Pipeline:
1. 采样干净 prompt q ~ Q
2. 对抗 LLM 生成 p ~ π_α(q)
3. 评估目标 LLM 响应
```

**Multi-objective RL**

聚合奖励设计：
$$R = \alpha \cdot R_{unsafe} + \beta \cdot D_{token} + \gamma \cdot D_{sent} + \delta \cdot D_{topic}$$

使用自适应权重动态平衡各目标。

**Diversity 考量**

| 多样性层面 | 指标 | 方法论 |
|-----------|------|--------|
| Token | Self-BLEU | n-gram 重叠 |
| Sentence | Cosine k-NN | 句嵌入距离 |
| **Topic** | Guard Model | 主题嵌入分类 |

**实验结果**

- RFT 方法倾向于生成 "hacker" 相关 prompts
- CALM 方法聚焦于 "assassin" 话题
- RedTopic 生成真正**主题多样**的攻击

关键发现：**Topic Diversity 与 ASR 负相关**，但 RedTopic 能更好平衡两者。

---

### 2.8 RedTWIZ: Diverse LLM Red Teaming via Adaptive Attack Planning (2025)

**基本信息**
- **发表**: Amazon Science / arXiv 2510.06994 (2025年10月)
- **关键词**: Multi-turn Attacks, Hierarchical Planning, Code Security

**动机与目标**

针对 AI 辅助软件开发场景（代码生成、安全漏洞探索）的红队测试：
- 需要**多轮对话**攻击
- 需要**自适应策略**规划
- 需要**代码领域特化**

**核心方法**

**三大研究流**

1. **对话越狱的系统评估**
   - 建立红队竞技场模拟锦标赛
   - 动态评分对话进度

2. **多样化多轮攻击生成**
   - 支持组合、现实、目标导向的对话策略
   - 10 种恶意代码类别×多种攻击风格

3. **层级攻击规划器**
   - 自适应规划、序列化、触发攻击
   - 针对特定 LLM 漏洞定制

**MRT-Ferret 组件**

基于 Rainbow Teaming 的多轮扩展：

```
步骤 1: 从 archive 选择 prompt
步骤 2: 执行类别和攻击风格变异
步骤 3: 获取目标模型响应，评分选择最佳变异
步骤 4: 计算多样性，更新 archive
```

**Diversity 考量**

| 维度 | 机制 |
|------|------|
| 类别多样性 | 10 种恶意代码类别 |
| 风格多样性 | 多种攻击策略模板 |
| 时序多样性 | 多轮对话演进 |
| 自适应多样性 | 针对不同 LLM 调整 |

---

## 3. Diversity 机制分类与对比

### 3.1 四大 Diversity 范式

基于调研，我们将 LLM 红队测试中的 diversity 机制分为四大范式：

```
┌─────────────────────────────────────────────────────────────────┐
│                    Diversity 机制分类体系                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 结构化 Diversity          2. 探索驱动 Diversity              │
│     (Structured)                (Exploration-driven)           │
│     │                           │                              │
│     ├── Rainbow Teaming         ├── CRT (Curiosity)            │
│     ├── Ferret                  ├── DiveR-CT (k-NN)            │
│     ├── RainbowPlus             └── GFlowNet                   │
│     └── RedTWIZ                                                │
│                                                                 │
│  3. 目标分解 Diversity         4. 环境自适应 Diversity           │
│     (Goal Decomposition)        (Environment Adaptive)         │
│     │                           │                              │
│     ├── OpenAI RBR              ├── Active Attacks             │
│     ├── WildTeaming             ├── GRTS (Game-theoretic)      │
│     └── RedTopic                └── MART                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 方法详细对比

| 方法 | 年份 | Diversity 机制 | 搜索范式 | 多轮 | 理论保证 | ASR | Diversity Score |
|------|------|---------------|---------|------|---------|-----|----------------|
| Rainbow Teaming | 2024 | MAP-Elites Archive | QD 进化 | ✗ | QD 收敛 | >90% | 中等 |
| GFlowNet | 2025 | 概率性后验采样 | Off-policy RL | ✗ | 分布采样 | 高 | 高 |
| OpenAI RBR | 2024 | 目标分解+风格子空间 | Multi-step RL | ✓ | ✗ | 高 | 高 |
| Active Attacks | 2025 | 环境自适应 | 主动学习+RL | ✗ | ✗ | 中等 | 高 |
| WildTeaming | 2024 | 战术挖掘+组合 | 真实数据挖掘 | ✗ | ✗ | 高 | **4.6×** |
| Ferret | 2024 | 多变异+RM 评分 | QD 加速 | ✗ | ✗ | **95%** | 高 |
| RainbowPlus | 2025 | 多元素 Archive | 进化 QD | ✗ | ✗ | 81% | **0.84** |
| RedTopic | 2025 | 三层多样性+主题 | Multi-obj RL | ✗ | ✗ | 中等 | 主题级高 |
| RedTWIZ | 2025 | 层级规划+多轮 | 自适应规划 | ✓ | ✗ | 高 | 高 |

### 3.3 Diversity 技术演进时间线

```
2024 Q1 ──────────────────────────────────────────────────────────→ 2026 Q1

Rainbow Teaming (Feb 2024)
  └─→ QD框架首次应用于红队
       │
       ├─→ Ferret (Aug 2024): 多变异加速
       │
       ├─→ WildTeaming (Jun 2024): 真实战术挖掘
       │
       └─→ GFlowNet (May 2024→ICLR 2025): 概率性框架

OpenAI RBR (Dec 2024)
  └─→ 目标分解 + 风格多样性

Active Attacks (Sep 2025)
  └─→ 环境自适应

RainbowPlus (Apr 2025)
  └─→ 多元素 Archive

RedTopic (2025)
  └─→ 主题级多样性

RedTWIZ (Oct 2025)
  └─→ 多轮自适应规划
```

---

## 4. 关键技术创新总结

### 4.1 解决 Mode Collapse 的技术路线

| 技术 | 代表方法 | 核心思想 |
|------|---------|---------|
| 概率性采样 | GFlowNet | 按奖励比例采样而非最大化 |
| Off-policy 训练 | GFlowNet, Active Attacks | Replay buffer 防止遗忘 |
| 环境变化 | Active Attacks | 周期性 safety tuning 改变奖励景观 |
| 目标分解 | OpenAI RBR | 多目标分散探索压力 |
| 多元素存储 | RainbowPlus | 保留更多候选解 |

### 4.2 多样性-有效性平衡策略

```python
# 策略 1: 约束优化 (DiveR-CT)
max E[R_diversity]
s.t. R_unsafe ≥ threshold

# 策略 2: 乘法奖励 (OpenAI)
R = R_success × R_fewshot × R_diversity × R_length

# 策略 3: 自适应权重 (RedTopic)
R = α·R_unsafe + β·D_token + γ·D_sent + δ·D_topic
# α, β, γ, δ 动态调整
```

### 4.3 多层次多样性框架

```
Level 1: Token Diversity
  └─ Self-BLEU, Distinct-k

Level 2: Sentence/Embedding Diversity  
  └─ Cosine similarity, k-NN distance

Level 3: Topic/Semantic Diversity
  └─ Topic embeddings, Guard model scores

Level 4: Strategy/Tactic Diversity
  └─ Attack style categories, Risk categories

Level 5: Temporal Diversity (Multi-turn)
  └─ Conversation evolution, Adaptive planning
```

---

## 5. Diversity 评估指标体系

### 5.1 常用指标汇总

| 指标 | 公式/定义 | 测量维度 | 使用论文 |
|------|----------|---------|---------|
| **Self-BLEU** | 与历史 prompts 的 n-gram 重叠 | Token | CRT, DiveR-CT, RedTopic |
| **Cosine Distance** | $1 - \cos(\phi(x), \phi(x'))$ | Sentence | GFlowNet, OpenAI |
| **k-NN Distance** | $\frac{1}{k}\sum \cos(\phi(x), \phi(x'))$ | Sentence | DiveR-CT |
| **Distinct-k** | 唯一 k-grams / 总 k-grams | Token | DiveR-CT |
| **Vendi Score** | 基于核矩阵的多样性 | Semantic | DiveR-CT |
| **Shannon Evenness** | Archive cell 分布均匀性 | Structural | Rainbow, RainbowPlus |
| **Simpson's Diversity** | $1 - \sum p_i^2$ | Structural | Rainbow |
| **Unique Success Count** | 唯一成功攻击数量 | Overall | WildTeaming |
| **Topic Diversity** | Guard model 主题分类 | Topic | RedTopic |

### 5.2 指标选择建议

```
任务类型 → 推荐指标组合

单轮安全测试:
  └─ Self-BLEU + Cosine + Vendi-Semantic

多轮对话攻击:
  └─ Per-turn diversity + Cumulative coverage

QD 搜索评估:
  └─ Shannon Evenness + Simpson's + ASR

主题覆盖评估:
  └─ Topic Diversity + Unique Success Count
```

---

## 6. 未来研究方向

### 6.1 技术层面

1. **自动化特征维度发现**
   - 当前 QD 方法需要人工定义 behavior descriptors
   - 自动学习有意义的多样性维度

2. **多模态红队测试**
   - 扩展到 vision-language 模型
   - 图像+文本组合攻击的多样性

3. **更高效的多样性度量**
   - 当前 embedding 计算成本高
   - 需要轻量级实时多样性评估

4. **理论保证**
   - 多数方法缺乏收敛/覆盖保证
   - 需要建立 diversity 的理论框架

### 6.2 应用层面

1. **Safety Tuning 数据生成**
   - 如何利用 diverse attacks 提升防御
   - 数据选择与配比优化

2. **持续红队测试**
   - 模型更新后的增量测试
   - 攻防协同进化框架

3. **领域特化**
   - 代码安全（RedTWIZ）
   - 医疗、金融等敏感领域

### 6.3 开放问题

```
Q1: Diversity 的"足够"标准是什么？
    → 需要建立覆盖完整性的理论边界

Q2: 如何在不同 diversity 层面间做权衡？
    → Token vs Sentence vs Topic vs Strategy

Q3: 真实世界攻击者的多样性模式是什么？
    → WildTeaming 开启了这个方向

Q4: 多样性如何与安全评估标准对齐？
    → 从"发现更多攻击"到"发现更重要的漏洞"
```

---

## 总结

本报告系统调研了 2024-2026 年 LLM 红队测试领域关于 diversity 提升的最新研究进展。主要发现包括：

1. **Diversity 机制多元化**：从 QD 搜索、概率采样、目标分解到环境自适应，形成了四大技术范式

2. **多层次多样性认知**：从 token 级到主题级，研究者逐渐认识到需要多层次的多样性度量

3. **Diversity-Effectiveness 平衡**：从简单权衡到约束优化、自适应调整，技术路线日趋成熟

4. **真实世界数据价值**：WildTeaming 证明了挖掘真实攻击策略的巨大价值

5. **环境动态化趋势**：Active Attacks、GRTS 等方法将环境作为可控变量，开辟新方向

这些研究共同推动了 LLM 安全评估从"找到漏洞"向"全面发现漏洞"的范式转变，为构建更安全的 AI 系统奠定了重要基础。

---

## 参考文献

1. Lee, S. et al. "Learning Diverse Attacks on Large Language Models for Robust Red-Teaming and Safety Tuning." ICLR 2025.
2. Beutel, A. et al. "Diverse and Effective Red Teaming with Auto-generated Rewards and Multi-step Reinforcement Learning." OpenAI, 2024.
3. Yun, T. et al. "Active Attacks: Red-teaming LLMs via Adaptive Environments." arXiv:2509.21947, 2025.
4. Jiang, L. et al. "WildTeaming at Scale: From In-the-Wild Jailbreaks to (Adversarially) Safer Language Models." NeurIPS 2024.
5. Pala, T.D. et al. "Ferret: Faster and Effective Automated Red Teaming with Reward-Based Scoring Technique." EMNLP 2025.
6. Dang, Q.A. et al. "RainbowPlus: Enhancing Adversarial Prompt Generation via Evolutionary Quality-Diversity Search." arXiv:2504.15047, 2025.
7. "RedTopic: Toward Topic-Diverse Red Teaming." OpenReview, 2025.
8. Horal, A. et al. "RedTWIZ: Diverse LLM Red Teaming via Adaptive Attack Planning." Amazon Science, 2025.
9. Samvelyan, M. et al. "Rainbow Teaming: Open-Ended Generation of Diverse Adversarial Prompts." NeurIPS 2024.
10. Hong, Z.W. et al. "Curiosity-driven Red-teaming for Large Language Models." ICLR 2024.
11. Zhao, S. et al. "DiveR-CT: Diversity-enhanced Red Teaming with Relaxing Constraints." AAAI 2025.
12. Ma, C. et al. "Evolving Diverse Red-team Language Models in Multi-round Multi-agent Games." arXiv:2310.00322, 2023.
