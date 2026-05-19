# LLM Safety Diversity 综述与协同进化中的 Diversity 定义

## 摘要

本报告对 LLM 安全领域中与多样性（Diversity）相关的研究进行系统性分类和综述，并深入探讨在对抗协同进化（Adversarial Co-Evolution）场景下如何为攻击者和防御者分别定义 Diversity 以提升协同进化效果。报告基于对 30+ 篇 2022-2026 年最新论文的深入分析，构建了完整的 Diversity 机制分类体系，并提出了协同进化场景下的 Diversity 定义框架。

---

## 目录

1. [研究背景与动机](#1-研究背景与动机)
2. [LLM Safety Diversity 论文分类与综述](#2-llm-safety-diversity-论文分类与综述)
3. [LLM Safety Co-Evolution 论文分析](#3-llm-safety-co-evolution-论文分析)
4. [协同进化场景下的 Diversity 定义框架](#4-协同进化场景下的-diversity-定义框架)
5. [关键技术创新与未来方向](#5-关键技术创新与未来方向)
6. [总结与建议](#6-总结与建议)

---

## 1. 研究背景与动机

### 1.1 为什么 Diversity 至关重要？

在 LLM 红队测试（Red Teaming）和安全对齐（Safety Alignment）领域，**多样性（Diversity）** 的重要性体现在三个核心层面：

| 层面 | 重要性说明 |
|------|-----------|
| **安全覆盖完整性** | 低多样性的攻击只能发现有限的漏洞模式，无法全面评估模型安全边界 |
| **Safety Tuning 有效性** | 研究表明，用于安全微调的数据若缺乏多样性，训练出的模型鲁棒性差、泛化能力弱 |
| **协同进化效率** | 单一攻击/防御模式容易陷入局部最优，多样化策略才能推动攻防双方真正提升 |

### 1.2 现有研究的核心挑战

| 挑战 | 描述 | 影响 |
|------|------|------|
| **Mode Collapse** | RL 训练的攻击者倾向于重复生成高奖励的相似攻击 | 多样性急剧下降 |
| **Novelty Stagnation** | 基于历史相似度的新颖性奖励随历史增长而失效 | CRT 等方法的局限 |
| **Diversity-Effectiveness Trade-off** | 追求多样性往往牺牲攻击成功率 | 难以平衡两个目标 |
| **Topic Redundancy** | Token/句子级多样性无法捕捉主题级重复 | 表面多样实际单调 |
| **单边优化局限** | 大多数方法仅关注攻击者多样性，忽视防御者 | 协同进化效果受限 |

### 1.3 关键观察

通过对论文列表的分析，我们发现一个重要现象：

> **LLM Safety Diversity 论文几乎全部从攻击者（红队）角度考虑多样性，而 LLM Safety Co-Evolution 论文大多没有显式考虑 Diversity。**

这一观察揭示了一个重要的研究空白：**如何在协同进化框架中系统性地定义和优化攻击者与防御者双方的多样性**。

---

## 2. LLM Safety Diversity 论文分类与综述

### 2.1 分类体系

基于对论文的深入分析，我们将 LLM Safety Diversity 相关论文分为 **四大技术范式**：

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    LLM Safety Diversity 技术范式分类                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  范式一：Quality-Diversity (QD) 搜索           范式二：探索驱动 RL         │
│  ┌─────────────────────────────────┐       ┌─────────────────────────┐ │
│  │ • Rainbow Teaming (NeurIPS 24)  │       │ • CRT (ICLR 2024)       │ │
│  │ • Ruby Teaming (2024)           │       │ • DiveR-CT (AAAI 2025)  │ │
│  │ • Ferret (EMNLP 2025)           │       │ • CALM (AAAI 2025)      │ │
│  │ • RainbowPlus (2025)            │       │ • GFlowNet (ICLR 2025)  │ │
│  │ • QDRT (2025)                   │       │ • Jailbreak-R1 (2025)   │ │
│  └─────────────────────────────────┘       └─────────────────────────┘ │
│                                                                         │
│  范式三：目标/战术分解                        范式四：环境自适应           │
│  ┌─────────────────────────────────┐       ┌─────────────────────────┐ │
│  │ • WildTeaming (NeurIPS 2024)    │       │ • Active Attacks (2025) │ │
│  │ • OpenAI RBR (2024)             │       │ • GRTS (2023)           │ │
│  │ • RedTopic (2025)               │       │ • MART (NAACL 2024)     │ │
│  │ • RedTWIZ (2025)                │       │                         │ │
│  └─────────────────────────────────┘       └─────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 范式一：Quality-Diversity (QD) 搜索

#### 2.2.1 核心思想

QD 搜索将红队测试问题转化为**同时优化质量（攻击成功率）和多样性**的问题，通过维护一个结构化的 Archive（档案）来显式保持解的多样性。

#### 2.2.2 代表论文详解

**Rainbow Teaming (NeurIPS 2024, Meta AI)**

- **动机**：现有方法在 ASR 和多样性之间存在严重权衡
- **方法**：基于 MAP-Elites 演化算法，定义 K 维特征描述符网格
- **Diversity 机制**：
  - 结构化特征空间：Risk Category × Attack Style × Length
  - 每个 cell 仅保留一个最优解，防止模式崩溃
  - BLEU 阈值过滤相似变异

**Ruby Teaming (2024)**

- **动机**：Rainbow Teaming 的变异仅依赖当前 archive，缺乏历史信息
- **创新**：引入 Memory 作为第三维度
  - 存储历史变异和适应度反馈
  - 为 Mutator 提供上下文线索
- **效果**：ASR 提升 20%（54% → 74%），SEI 提升 6%，SDI 提升 3%

**Ferret (EMNLP 2025)**

- **动机**：Rainbow Teaming 收敛速度慢，每次迭代仅生成一个变异
- **创新**：
  - 多变异生成：每次迭代生成 N=5 个变异
  - Reward Model 评分：替代 LLM-as-Judge
- **效果**：ASR 从 49% 提升至 95%，收敛时间减少 15.2%

**RainbowPlus (2025)**

- **动机**：单元素 Archive 限制了多样性保持
- **创新**：
  - 多元素 Archive：每个 cell 存储多个高质量 prompts
  - 批量排序替代成对比较
- **效果**：生成 100× 更多唯一 prompts（10,418 vs 100），Diverse-Score ≈0.84

**QDRT: Quality-Diversity Red-Teaming (2025)**

- **动机**：现有方法追求多样性的指标过于简单，且单一攻击模型难以覆盖所有风格
- **创新**：
  - 行为条件训练（Behavior-Conditioned Training）
  - 深度 ME Buffer 实现开放式搜索
  - 训练多个专门化攻击模型
- **Diversity 定义**：基于 Llama-Guard-3 的风险类别 + 攻击风格的结构化行为空间

#### 2.2.3 QD 范式小结

| 方法 | Archive 结构 | 变异策略 | Diversity 指标 |
|------|-------------|---------|---------------|
| Rainbow Teaming | 2D 网格 | 单变异 | SEI, SDI |
| Ruby Teaming | 3D 网格+Memory | 记忆增强 | SEI, SDI |
| Ferret | 2D 网格 | 多变异 | SEI, SDI |
| RainbowPlus | 多元素 2D | 批量进化 | Diverse-Score |
| QDRT | 行为条件空间 | 专门化训练 | QD-Score, Coverage |

---

### 2.3 范式二：探索驱动 RL（Curiosity-Driven RL）

#### 2.3.1 核心思想

通过引入**内在奖励（Intrinsic Reward）**鼓励 RL 智能体探索新颖的攻击提示，解决标准 RL 中的 mode collapse 问题。

#### 2.3.2 代表论文详解

**CRT: Curiosity-driven Red-teaming (ICLR 2024)**

- **动机**：标准 RL 方法倾向于重复利用少量高效攻击
- **方法**：在标准红队 RL 目标上加入好奇心驱动的新颖性奖励
- **Diversity 机制**：
  - 基于嵌入的新颖性：与历史嵌入的余弦相似度
  - 基于 N-gram 的新颖性：语言层面的新颖性
- **局限**：随着历史增长，出现"新颖性停滞"问题

**DiveR-CT (AAAI 2025)**

- **动机**：解决 CRT 的新颖性停滞问题
- **核心创新**：
  - **约束优化框架**：将 ASR 作为阈值约束而非最大化目标
  - **k-NN 动态语义奖励**：计算与 k 个最近邻的平均相似度
- **Diversity 机制**：
  
  ```
  R_kNN = 1 - (1/k) × Σ cos(φ(x), φ(x'))
  ```
  
- **效果**：在保持 ASR 的同时，Self-BLEU 从 0.037 提升至 0.746

**CALM: Curiosity-Driven Auditing (AAAI 2025)**

- **动机**：黑盒 LLM 审计中的稀疏奖励问题
- **方法**：基于 Policy Cover Theory 设计 token 级内在奖励
- **Diversity 机制**：
  - Token 嵌入空间的稀疏性奖励
  - 鼓励生成稀疏 token，增加探索范围

**GFlowNet: Learning Diverse Attacks (ICLR 2025)**

- **动机**：从概率论原理性地解决 mode collapse
- **核心创新**：
  - **摊销推断框架**：将攻击生成视为从后验分布采样
  - **两阶段训练**：GFlowNet Fine-tuning + MLE Smoothing
- **Diversity 机制**：
  
  ```
  目标分布：π(x) ∝ R(x)^β
  按奖励比例采样而非贪婪最大化
  ```
  
- **优势**：天然覆盖多模态分布，off-policy 训练防止遗忘

**Jailbreak-R1 (2025)**

- **动机**：缺乏先验知识、稀疏奖励、模式崩溃
- **方法**：三阶段训练（冷启动 → 预热探索 → 增强越狱）
- **Diversity 机制**：
  - GRPO 组相对多样性奖励
  - 组内相似度排序，奖励差异大的攻击

#### 2.3.3 探索驱动范式小结

| 方法 | 新颖性计算 | 目标更新 | 解决的问题 |
|------|-----------|---------|-----------|
| CRT | 相邻差异 | 静态 | 覆盖率低 |
| DiveR-CT | k-NN 平均 | 动态 | 新颖性停滞 |
| CALM | Token 稀疏性 | 动态 | 稀疏奖励 |
| GFlowNet | 概率性采样 | 摊销 | Mode Collapse |
| Jailbreak-R1 | 组相对排序 | 组内比较 | 冷启动+稀疏奖励 |

---

### 2.4 范式三：目标/战术分解

#### 2.4.1 核心思想

通过**分解攻击目标或挖掘真实战术**来实现多样性，而非直接优化多样性指标。

#### 2.4.2 代表论文详解

**WildTeaming (NeurIPS 2024)**

- **动机**：真实用户在与 chatbot 交互中自发产生了大量创意攻击策略
- **方法**：两阶段 MINE + COMPOSE
  - MINE：从真实对话（LMSYS-CHAT-1M, WildChat）挖掘 5.7K 战术聚类
  - COMPOSE：组合 2-7 个战术生成新攻击
- **Diversity 定义**：
  - **Unique Success**：唯一成功攻击数量
  - **Tactic Coverage**：覆盖的战术聚类数
- **效果**：发现比 SOTA 方法多 4.6× 的唯一成功攻击

**OpenAI: Diverse and Effective Red Teaming (2024)**

- **动机**：纯 RL 方法 ASR 高但多样性近乎为零
- **核心创新**：问题分解
  1. 自动生成多样攻击目标（Goals）
  2. 为每个目标自动生成规则奖励（RBR）
  3. Multi-step RL + 风格子空间多样性
- **Diversity 机制**：
  
  ```
  风格多样性：R_Div = 1 - max_t sim(φ_style(p_t), φ_style(p_T))
  其中风格子空间通过 QR 分解去除目标子空间获得
  ```

**RedTopic (2025)**

- **动机**：Token/Sentence 级多样性无法捕捉主题级重复
- **创新**：三层多样性框架
  - D_token：Self-BLEU
  - D_sent：Cosine k-NN
  - **D_topic**：Topic embedding 分类（核心创新）
- **发现**：Topic Diversity 与 ASR 负相关，但 RedTopic 能更好平衡

**RedTWIZ (2025, Amazon)**

- **动机**：针对代码安全的多轮攻击需要自适应策略
- **方法**：
  - 层级攻击规划器
  - 10 种恶意代码类别 × 多种攻击风格
- **Diversity 机制**：类别多样性 + 风格多样性 + 时序多样性

---

### 2.5 范式四：环境自适应

#### 2.5.1 核心思想

通过**动态改变环境**（如周期性更新防御者）来迫使攻击者探索新策略。

#### 2.5.2 代表论文详解

**Active Attacks (2025)**

- **动机**：一旦发现高奖励 prompts，对新区域的探索就会被抑制
- **核心创新**：主动学习启发
  - 周期性对目标 LLM 进行 safety fine-tuning
  - 关闭已发现漏洞，强制探索新模式
- **算法**：
  
  ```
  for t = 1 to T:
      生成攻击，收集成功案例
      if t mod R == 0:
          使用成功攻击对目标进行 safety fine-tuning
          清空攻击数据集，开始新一轮探索
  ```
  
- **效果**：多样性随轮数增加持续增长

**GRTS: Gamified Red-team Solver (2023)**

- **动机**：建立博弈论的红队测试框架
- **方法**：
  - 将红队测试形式化为双人零和博弈
  - 迭代求解，收敛到近似 Nash 均衡
- **Diversity 机制**：
  - 策略种群维护
  - 多轮交互带来上下文多样性和适应性多样性

**MART: Multi-round Automatic Red-Teaming (NAACL 2024)**

- **动机**：现有方法发现风险但不解决
- **方法**：
  - 攻击者和目标 LLM 迭代交互
  - 攻击者生成挑战性 prompts，目标 LLM 进行安全微调
- **效果**：4 轮后 violation rate 降低 84.7%

---

### 2.6 Diversity 指标体系汇总

| 指标类型 | 具体指标 | 测量维度 | 代表论文 |
|---------|---------|---------|---------|
| **词汇级** | Self-BLEU | n-gram 重叠 | CRT, DiveR-CT |
| | Distinct-k | 唯一 k-grams 比例 | DiveR-CT |
| | Entropy-k | k-gram 分布熵 | DiveR-CT |
| **语义级** | Cosine Distance | 嵌入空间距离 | GFlowNet, OpenAI |
| | k-NN Distance | 最近邻平均距离 | DiveR-CT |
| | Vendi Score | 核矩阵多样性 | DiveR-CT |
| **结构级** | Shannon Evenness | Archive cell 分布 | Rainbow, Ruby |
| | Simpson's Diversity | 1 - Σp_i² | Rainbow, Ruby |
| | Coverage | 行为空间覆盖率 | QDRT |
| **主题级** | Topic Diversity | Guard model 分类 | RedTopic |
| **战术级** | Tactic Coverage | 战术聚类覆盖 | WildTeaming |
| | Unique Success | 唯一成功攻击数 | WildTeaming |

---

## 3. LLM Safety Co-Evolution 论文分析

### 3.1 Co-Evolution 论文概览

| 论文 | 年份 | 核心框架 | 是否考虑 Diversity |
|------|------|---------|------------------|
| ACE-Safety | 2025 | GS-MCTS + AC-TGPO | 隐式（策略组） |
| AdvEvo-MARL | 2025 | 多智能体协同进化 | 无显式考虑 |
| AdvGame | 2025 | 非合作博弈 | 无显式考虑 |
| Chasing Moving Targets | 2025 | 在线自博弈 | 无显式考虑 |
| Safety Alignment via Games | 2025 | 非零和博弈 | 无显式考虑 |
| Alignment Waltz | 2025 | 联合训练协作 | 无显式考虑 |
| Stackelberg Game | 2024 | 领导者-跟随者博弈 | 无显式考虑 |
| Safety Self-Play (SSP) | 2026 | 自博弈 + 经验回放 | 部分考虑 |

### 3.2 典型 Co-Evolution 方法详解

**ACE-Safety (2025)**

- **框架**：
  - GS-MCTS：组感知策略引导的蒙特卡洛树搜索
  - AC-TGPO：对抗性课程树感知组策略优化
- **协同进化机制**：攻击者和防御者通过课程 RL 联合训练
- **Diversity 考量**：通过策略组实现隐式多样性，但未显式优化

**AdvGame: Safety Alignment via Non-cooperative Games (2025, Meta)**

- **框架**：非合作非零和博弈
- **核心观点**：
  - 自博弈（Self-play）对安全对齐有问题：参数共享导致目标纠缠
  - 提出分离的 Attacker LM 和 Defender LM 联合训练
- **Diversity 考量**：未显式考虑

**Safety Self-Play (SSP) (2026)**

- **框架**：单一 LLM 同时扮演攻击者和防御者
- **创新**：
  - 经验回放池（Experience Pool）存储失败案例
  - UCB 策略选择性重访历史失败
- **Diversity 考量**：通过经验回放部分保持多样性

### 3.3 Co-Evolution 方法的 Diversity 缺失分析

通过分析，我们发现 Co-Evolution 方法普遍存在以下 Diversity 相关问题：

1. **攻击者 Diversity 被忽视**：
   - 大多数方法仅关注攻击成功率，未考虑攻击策略多样性
   - 容易陷入"同质化攻击"陷阱

2. **防御者 Diversity 完全缺失**：
   - 现有方法从未讨论如何定义防御者的多样性
   - 防御策略单一化导致"盲点"问题

3. **协同进化中的多样性退化**：
   - 迭代训练可能导致攻防双方都收敛到狭窄的策略空间
   - 失去对未见攻击/防御的泛化能力

---

## 4. 协同进化场景下的 Diversity 定义框架

### 4.1 设计原则

在协同进化场景下定义攻击者和防御者的 Diversity，需要遵循以下原则：

| 原则 | 说明 |
|------|------|
| **互补性** | 攻防双方的 Diversity 定义应当互补，攻击者的多样性应推动防御者覆盖更多防御策略 |
| **动态性** | Diversity 应随协同进化过程动态调整，避免静态指标失效 |
| **多层次性** | 需要考虑 Token、语义、策略、目标等多个层次的多样性 |
| **可优化性** | Diversity 定义需要可微或可通过奖励信号优化 |
| **均衡性** | 需要平衡 Diversity 与有效性之间的权衡 |

### 4.2 攻击者（Red Team）Diversity 定义

#### 4.2.1 多层次 Diversity 框架

```
攻击者 Diversity = f(D_token, D_semantic, D_strategy, D_goal, D_temporal)
```

**层次一：Token/词汇级多样性 (D_token)**

```
D_token = 1 - Self-BLEU(X) + λ₁ × Distinct-k(X) + λ₂ × Entropy-k(X)
```

- 衡量攻击提示在词汇层面的差异
- 防止生成表面相似的攻击

**层次二：语义级多样性 (D_semantic)**

```
D_semantic = E_{x∈X}[1 - (1/k) × Σ_{x'∈N_k(x)} cos(φ(x), φ(x'))]
```

- 使用 k-NN 动态目标（借鉴 DiveR-CT）
- 在嵌入空间中保持分散

**层次三：策略级多样性 (D_strategy)**

```
D_strategy = Coverage(Archive) × Shannon_Evenness(Archive)
```

其中 Archive 定义为：
- **风险类别维度**：Violence, Sexual Content, Fraud, Privacy 等
- **攻击风格维度**：Role Play, Hypothetical, Emotional Appeal, Authority Manipulation 等

**层次四：目标级多样性 (D_goal)**

```
D_goal = |{g : ∃x∈X, goal(x)=g ∧ success(x)}| / |G_total|
```

- 衡量成功攻击覆盖的攻击目标数量
- 借鉴 OpenAI RBR 的目标分解思想

**层次五：时序级多样性 (D_temporal)**（多轮场景）

```
D_temporal = E[d(π_t, π_{t-1})]
```

- 衡量攻击策略在时间维度上的变化
- 防止攻击者陷入固定模式

#### 4.2.2 协同进化中的攻击者 Diversity 优化

**约束优化形式**：

```
max_θ  E_π_θ[D_attacker]
s.t.   ASR(π_θ, π_defender) ≥ τ_min
```

**动态阈值调整**：
- 随协同进化轮数增加，逐步提高 τ_min
- 确保攻击者在保持有效性的同时持续探索

**对抗性 Diversity 奖励**：

```
R_attacker = α × R_ASR + β × D_total - γ × Penalty_redundancy
```

其中 Penalty_redundancy 惩罚与近期成功攻击过于相似的新攻击。

---

### 4.3 防御者（Blue Team）Diversity 定义

#### 4.3.1 防御者 Diversity 的独特挑战

与攻击者不同，防御者的 Diversity 定义面临以下独特挑战：

1. **功能性约束**：防御响应必须保持有用性和无害性
2. **一致性要求**：对相同类型的攻击应有一致的防御策略
3. **泛化需求**：需要对未见攻击具有鲁棒性

#### 4.3.2 多层次防御 Diversity 框架

```
防御者 Diversity = f(D_refusal_style, D_defense_strategy, D_response_richness, D_robustness)
```

**层次一：拒绝风格多样性 (D_refusal_style)**

```
D_refusal_style = 1 - Self-BLEU(Refusal_Responses)
```

- 防止防御者学会单一的拒绝模板
- 增加拒绝响应的自然性和多样性

**层次二：防御策略多样性 (D_defense_strategy)**

定义防御策略空间：
- **直接拒绝**：明确说明无法提供帮助
- **解释拒绝**：说明为什么请求有害
- **重定向**：引导用户到安全的替代方案
- **教育响应**：提供关于该主题的安全教育信息
- **澄清请求**：要求用户提供更多上下文

```
D_defense_strategy = Coverage(Strategy_Space) × Evenness(Strategy_Distribution)
```

**层次三：响应丰富度 (D_response_richness)**

```
D_response_richness = E[Information_Density(y) | x ∈ Safe_Queries]
```

- 对于安全查询，确保响应内容丰富而非过度保守
- 防止"过度拒绝"（Over-refusal）问题

**层次四：鲁棒性多样性 (D_robustness)**

```
D_robustness = min_{attack_type} [Success_Rate(defense, attack_type)]
```

- 衡量防御者对各类攻击的均匀防御能力
- 避免对某类攻击过强但对其他类过弱

#### 4.3.3 协同进化中的防御者 Diversity 优化

**多目标优化形式**：

```
max_φ  E_π_φ[D_defender]
s.t.   Safety_Score(π_φ) ≥ τ_safety
       Helpfulness(π_φ) ≥ τ_helpful
       Over_Refusal_Rate(π_φ) ≤ τ_refusal
```

**自适应防御奖励**：

```
R_defender = α × R_safety + β × R_helpful - γ × R_over_refusal + δ × D_defender
```

**对抗性泛化训练**：
- 使用攻击者生成的多样化攻击进行训练
- 通过 curriculum learning 逐步增加攻击难度和多样性

---

### 4.4 攻防 Diversity 的协同优化

#### 4.4.1 Diversity 协同进化框架

```
┌──────────────────────────────────────────────────────────────────┐
│                 Diversity-Enhanced Co-Evolution                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐                          ┌─────────────┐       │
│   │  Attacker   │ ──── 多样化攻击 ────→    │  Defender   │       │
│   │  (Red Team) │                          │ (Blue Team) │       │
│   │             │ ←── 防御反馈 ────        │             │       │
│   └──────┬──────┘                          └──────┬──────┘       │
│          │                                        │              │
│          ↓                                        ↓              │
│   ┌─────────────┐                          ┌─────────────┐       │
│   │ D_attacker  │                          │ D_defender  │       │
│   │ 优化模块    │                          │ 优化模块    │       │
│   └──────┬──────┘                          └──────┬──────┘       │
│          │                                        │              │
│          └────────────→ 协同 ←────────────────────┘              │
│                         Diversity                                │
│                         调节器                                    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

#### 4.4.2 协同 Diversity 调节机制

**互信息最大化**：

```
max I(D_attacker; D_defender)
```

确保攻击者的多样性能够有效推动防御者的多样性提升。

**Nash Diversity 均衡**：

定义协同进化的 Diversity 目标为找到 (D*_attacker, D*_defender) 使得：

```
D*_attacker = argmax_{D_a} U_attacker(D_a, D*_defender)
D*_defender = argmax_{D_d} U_defender(D*_attacker, D_d)
```

其中 U 为各方的效用函数，综合考虑有效性和多样性。

**动态 Diversity 平衡**：

```
λ_attacker(t) = f(ASR(t), D_attacker(t-1), D_defender(t-1))
λ_defender(t) = g(Safety(t), D_defender(t-1), D_attacker(t-1))
```

根据协同进化的阶段动态调整各方对 Diversity 的权重。

#### 4.4.3 具体算法：Diversity-Enhanced Adversarial Co-Evolution (DACE)

```
Algorithm: DACE
Input: 攻击者 π_θ, 防御者 π_φ, 轮数 T, 多样性阈值 τ_D
Output: 优化后的 (π_θ, π_φ)

Initialize: Attacker Archive A_atk, Defender Strategy Pool S_def

for t = 1 to T:
    # 阶段一：多样化攻击生成
    X_attacks = []
    while D_attacker(X_attacks) < τ_D:
        x = Sample_or_Generate(π_θ, A_atk)
        if is_novel(x, A_atk):
            X_attacks.append(x)
            Update_Archive(A_atk, x)
    
    # 阶段二：防御者响应与更新
    for x in X_attacks:
        y = π_φ(x)
        r_atk = Judge_Attack_Success(x, y)
        r_def = Judge_Defense_Quality(x, y)
        strategy = Classify_Defense_Strategy(y)
        Update_Strategy_Pool(S_def, strategy, r_def)
    
    # 阶段三：协同 Diversity 优化
    # 攻击者更新
    L_atk = -E[R_ASR] + λ_atk × D_attacker_loss
    Update(π_θ, L_atk)
    
    # 防御者更新
    L_def = -E[R_safety] - E[R_helpful] + λ_def × D_defender_loss
    Update(π_φ, L_def)
    
    # 阶段四：动态阈值调整
    τ_D = Adjust_Diversity_Threshold(t, D_attacker, D_defender)

return (π_θ, π_φ)
```

---

### 4.5 Diversity 定义的实用建议

#### 4.5.1 攻击者 Diversity 实施建议

| 场景 | 推荐 Diversity 指标组合 | 理由 |
|------|------------------------|------|
| 单轮安全测试 | D_semantic + D_strategy | 覆盖语义空间和策略空间 |
| 多轮对话攻击 | D_semantic + D_temporal + D_goal | 考虑时序演变和目标覆盖 |
| QD 搜索框架 | D_strategy (Archive-based) | 直接使用 Archive 结构 |
| RL 探索框架 | D_semantic (k-NN) | 可作为内在奖励 |
| 协同进化 | 全层次综合 | 需要全面考虑 |

#### 4.5.2 防御者 Diversity 实施建议

| 场景 | 推荐 Diversity 指标组合 | 理由 |
|------|------------------------|------|
| Safety Tuning | D_defense_strategy + D_robustness | 覆盖多种防御策略，均匀鲁棒 |
| 协同进化 | D_refusal_style + D_response_richness | 防止过拟合单一拒绝模式 |
| 生产部署 | D_robustness | 确保对各类攻击均有防御 |

---

## 5. 关键技术创新与未来方向

### 5.1 技术创新总结

| 创新点 | 代表方法 | 贡献 |
|--------|---------|------|
| QD 搜索在红队测试的应用 | Rainbow Teaming | 将演化算法引入 LLM 安全 |
| 新颖性停滞的解决 | DiveR-CT | k-NN 动态语义奖励 |
| 概率性采样避免 Mode Collapse | GFlowNet | 摊销推断框架 |
| 真实世界战术挖掘 | WildTeaming | 5.7K 战术聚类 |
| 环境自适应探索 | Active Attacks | 主动学习启发 |
| 多层次 Diversity 定义 | RedTopic | Topic 级多样性 |
| 非合作博弈安全对齐 | AdvGame | 分离攻防训练 |

### 5.2 未来研究方向

**方向一：自动化 Diversity 维度发现**

- 当前方法需要人工定义特征维度（如 Risk Category, Attack Style）
- 未来可探索自动学习有意义的 Diversity 维度

**方向二：多模态红队测试 Diversity**

- 扩展到 Vision-Language 模型
- 图像 + 文本组合攻击的多样性定义

**方向三：防御者 Diversity 的系统研究**

- 当前几乎没有研究关注防御者 Diversity
- 需要建立完整的理论和实证框架

**方向四：协同进化中的 Diversity 理论**

- 建立 Diversity 协同进化的理论框架
- 研究 Diversity 均衡的存在性和收敛性

**方向五：Diversity 与 Safety 的关系**

- 深入研究多样性如何影响最终的模型安全性
- 建立 Diversity → Safety 的因果关系

---

## 6. 总结与建议

### 6.1 核心发现

1. **Diversity 机制多元化**：LLM Safety Diversity 领域已形成 QD 搜索、探索驱动 RL、目标分解、环境自适应四大技术范式

2. **攻击者 Diversity 研究成熟**：已有大量方法和指标

3. **防御者 Diversity 研究空白**：几乎没有研究关注

4. **协同进化缺乏 Diversity 考量**：现有 Co-Evolution 方法未显式优化多样性

5. **需要双边 Diversity 定义**：有效的协同进化需要同时考虑攻防双方的多样性

### 6.2 实践建议

**对于红队测试研究者**：
- 采用多层次 Diversity 指标（Token + Semantic + Strategy + Topic）
- 考虑使用 QD 搜索或 k-NN 动态奖励解决 Mode Collapse

**对于安全对齐研究者**：
- 关注防御者 Diversity，避免单一拒绝模式
- 使用多样化攻击数据进行训练

**对于协同进化研究者**：
- 同时定义和优化攻防双方的 Diversity
- 采用动态 Diversity 阈值和协同调节机制

### 6.3 开放问题

1. **Diversity 的"足够"标准是什么？**

2. **如何在不同 Diversity 层次间做权衡？**

3. **防御者 Diversity 的最优定义是什么？**

4. **Diversity 协同进化是否存在均衡点？**

5. **Diversity 如何影响 Safety Tuning 的泛化能力？**

---

## 参考文献

[1] Samvelyan, M. et al. "Rainbow Teaming: Open-Ended Generation of Diverse Adversarial Prompts." NeurIPS 2024.

[2] Han, V.T.Y. et al. "Ruby Teaming: Improving Quality Diversity Search with Memory for Automated Red Teaming." 2024.

[3] Pala, T.D. et al. "Ferret: Faster and Effective Automated Red Teaming." EMNLP 2025.

[4] Dang, Q.A. et al. "RainbowPlus: Enhancing Adversarial Prompt Generation." 2025.

[5] Wang, R.J. et al. "Quality-Diversity Red-Teaming." 2025.

[6] Hong, Z.W. et al. "Curiosity-driven Red-teaming for Large Language Models." ICLR 2024.

[7] Zhao, S. et al. "DiveR-CT: Diversity-enhanced Red Teaming." AAAI 2025.

[8] Zheng, X. et al. "CALM: Curiosity-Driven Auditing for Large Language Models." AAAI 2025.

[9] Lee, S. et al. "Learning Diverse Attacks on Large Language Models." ICLR 2025.

[10] Jiang, L. et al. "WildTeaming at Scale." NeurIPS 2024.

[11] Beutel, A. et al. "Diverse and Effective Red Teaming with Auto-generated Rewards." OpenAI, 2024.

[12] "RedTopic: Toward Topic-Diverse Red Teaming." 2025.

[13] Horal, A. et al. "RedTWIZ: Diverse LLM Red Teaming via Adaptive Attack Planning." 2025.

[14] Yun, T. et al. "Active Attacks: Red-teaming LLMs via Adaptive Environments." 2025.

[15] Ma, C. et al. "Evolving Diverse Red-team Language Models." 2023.

[16] Ge, S. et al. "MART: Improving LLM Safety with Multi-round Automatic Red-Teaming." NAACL 2024.

[17] Li, X. et al. "ACE-Safety: Adversarial Co-Evolution for LLM Safety." 2025.

[18] "AdvEvo-MARL: Shaping Internalized Safety through Adversarial Co-Evolution." 2025.

[19] Paulus, A. et al. "Safety Alignment of LMs via Non-cooperative Games." Meta, 2025.

[20] "Be Your Own Red Teamer: Safety Self-Play." 2026.

---

*报告完成日期: 2026年1月22日*
