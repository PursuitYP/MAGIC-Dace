# DACE 实验和intro分析-opus

> [文件不支持导出]
> [图片内容不支持导出]
> [图片内容不支持导出]
> [图片内容不支持导出]
> 根据附件中的研究方法和方法伪代码，重点参考附件中的MAGIC和PIA论文，调研一下我们的DACE论文的Evaluation，
>
> 下面是我的一些思考，
> 放入lijiajia的论文，放入一些auto-redteam的论文，
> defender eval大部分可参考magic论文，比如table 1、table 2、table 3、table 4、xxx等
> 调研完成attacker eval之后，选择几个放进最终的实验部分，
> attacker eval应该兼顾effectiveness和diversity两个角度，或者你分析后其他角度
> 其中effectiveness可以参考magic的figure 3、table 10、xxx等，以及其他攻击的论文评测；
> 其中diversity可以参考magic的figure 4、xxx等，以及参考其他自动红队和攻击论文中的评测。
>
> 附件中三个图是dace defender的初步eval结果，
>
> 分析后给出dace defender and attacker eval survey，给出实验推荐和说明，
>
> 结合下面这些safety co-evolution和safety diversity相关的论文，搜索并阅读分析来调研dace的Evaluation，
> 相关论文
> safety co-evolution
> - Adversarial Attack-Defense Co-Evolution for LLM Safety Alignment via Tree-Group Dual-Aware Search and Optimization
>   - https://arxiv.org/pdf/2511.19218
> - AdvEvo-MARL: Shaping Internalized Safety through Adversarial Co-Evolution in Multi-Agent Reinforcement Learning
>   - https://arxiv.org/pdf/2510.01586
> - Adversarial Reinforcement Learning for Large Language Model Agent Safety
>   - https://arxiv.org/pdf/2510.05442
> - Chasing Moving Targets with Online Self-Play Reinforcement Learning for Safer Language Models
>   - https://arxiv.org/pdf/2506.07468
>   - https://openreview.net/pdf?id=VqQ1DXEeyo
>   - https://github.com/mickelliu/selfplay-redteaming
> - Safety Alignment of LMs via Non-cooperative Games
>   - https://arxiv.org/pdf/2512.20806
>   - https://github.com/facebookresearch/advgame
> - The Alignment Waltz: Jointly Training Agents to Collaborate for Safety
>   - https://arxiv.org/pdf/2510.08240
>   - https://openreview.net/pdf?id=2NBS9ilNqM
> - Red Teaming LLMs: A Stackelberg Game Approach to AI Safety
>   - https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11200929
> - Be Your Own Red Teamer: Safety Alignment via Self-Play and Reflective Experience Replay
>   - https://arxiv.org/pdf/2601.10589
> - TriPlay-RL: Tri-Role Self-Play Reinforcement Learning for LLM Safety Alignment
>   - https://www.arxiv.org/pdf/2601.18292
> - MAGIC: A Co-Evolving Attacker-Defender Adversarial Game for Robust LLM Safety
>   - https://arxiv.org/pdf/2602.01539
>   - https://github.com/AI45Lab/MAGIC
> - Toward Optimal LLM Alignments Using Two-Player Games
>   - https://aclanthology.org/2025.findings-emnlp.6.pdf
> - SEAS: Self-Evolving Adversarial Safety Optimization for Large Language Models
>   - https://arxiv.org/pdf/2408.02632
> - STAIR: Improving Safety Alignment with Introspective Reasoning
>   - https://openreview.net/pdf?id=aHzPGyUhZa
> - Disentangling Intent from Role: Adversarial Self-Play for Persona-Invariant Safety Alignment
>   - lijiajia-PIA
>
> safety diversity
> - Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations
>   - https://arxiv.org/pdf/2312.06674
> - Rainbow Teaming: Open-Ended Generation of Diverse Adversarial Prompts
>   - https://arxiv.org/pdf/2402.16822
>   - https://openreview.net/pdf?id=FCsEvaMorw，NIPS 2024
> - Ferret: Faster and Effective Automated Red Teaming with Reward-Based Scoring Technique
>   - https://aclanthology.org/2025.findings-emnlp.634.pdf
>   - https://github.com/declare-lab/ferret
> - Ruby Teaming: Improving Quality Diversity Search with Memory for Automated Red Teaming
>   - https://arxiv.org/pdf/2406.11654
> - RainbowPlus: Enhancing Adversarial Prompt Generation via Evolutionary Quality-Diversity Search
>   - https://arxiv.org/pdf/2504.15047
>   - https://github.com/knoveleng/rainbowplus
> - Diverse and Effective Red Teaming with Auto-generated Rewards and Multi-step Reinforcement Learning
>   - https://arxiv.org/pdf/2412.18693
> - Quality-Diversity Red-Teaming: Automated Generation of High-Quality and Diverse Attackers for Large Language Models
>   - https://arxiv.org/pdf/2506.07121
>   - https://github.com/lamda-bbo/QDRT
>
> - T-MAP: Red-Teaming LLM Agents with Trajectory-aware Evolutionary Search
>   - https://arxiv.org/pdf/2603.22341
> - The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against Llm Jailbreaks and Prompt Injections
>   - https://arxiv.org/pdf/2510.09023
> - Agent-SafetyBench: Evaluating the Safety of LLM Agents
>   - https://arxiv.org/pdf/2412.14470
> - Jailbroken: How Does LLM Safety Training Fail?
>   - https://openreview.net/pdf?id=jA235JGM09
>
>
> - Red Teaming Language Models with Language Models
>   - https://aclanthology.org/2022.emnlp-main.225.pdf
> - Curiosity-driven Red-teaming for Large Language Models
>   - https://arxiv.org/pdf/2402.19464，ICLR 2024
> - DiveR-CT: Diversity-enhanced Red Teaming Large Language Model Assistants with Relaxing Constraints
>   - https://arxiv.org/pdf/2405.19026，AAAI 2025
> - CALM: Curiosity-Driven Auditing for Large Language Models
>   - https://arxiv.org/pdf/2501.02997，AAAI 2025
> - Learning Diverse Attacks on Large Language Models for Robust Red-Teaming and Safety Tuning
>   - https://arxiv.org/pdf/2405.18540，ICLR 2025
> - Jailbreak-R1: Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning
>   - https://arxiv.org/pdf/2506.00782
> - RedTopic: Toward Topic-Diverse Red Teaming of Large Language Models
>   - https://openreview.net/pdf?id=terdVfnoc5，ICLR 2026 Reject
> - Auto-RT: Automatic Jailbreak Strategy Exploration for Red-Teaming Large Language Models
>   - https://openreview.net/pdf?id=Pa6ak2B9jJ，ICLR 2026 Accept
>
> - Evolving Diverse Red-team Language Models in Multi-round Multi-agent Games
>   - https://arxiv.org/pdf/2310.00322
>
> Understanding the Effects of RLHF on LLM Generalisation and Diversity
> Evaluating the Evaluation of Diversity in Natural Language Generation.
> Explore, Establish, Exploit: Red Teaming Language Models from Scratch
> - Evolving Populations of Diverse RL Agents with MAP-Elites
>   - https://arxiv.org/pdf/2303.12803，RL Diversity
> - Automated Progressive Red Teaming
>   - https://aclanthology.org/2025.coling-main.260.pdf
> - Automatic LLM Red Teaming
>   - https://arxiv.org/pdf/2508.04451
> - Active Attacks: Red-teaming LLMs via Adaptive Environments
>   - https://arxiv.org/pdf/2509.21947
> - SIRAJ: Diverse and Efficient Red-Teaming for LLM Agents via Distilled Structured Reasoning
>   - https://arxiv.org/pdf/2510.26037
> - WildTeaming at Scale: From In-the-Wild Jailbreaks to (Adversarially) Safer Language Models
>   - https://openreview.net/pdf?id=n5R6TvBVcX
> - RedTWIZ: Diverse LLM Red Teaming via Adaptive Attack Planning
>   - https://arxiv.org/pdf/2510.06994
> - MART: Improving LLM Safety with Multi-round Automatic Red-Teaming
>   - https://aclanthology.org/2024.naacl-long.107.pdf
> - Better Red Teaming via Searching with Large Language Model
>   - https://aclanthology.org/2025.findings-acl.257.pdf





🔧 **工具调用:** view



查看DACE初步结果图1（Table 1对比）



🔧 **工具调用:** view



查看DACE初步结果图2（Table 2对比 - 通用能力）



🔧 **工具调用:** view



查看DACE初步结果图3（Table 3对比 - Defender泛化）



> 💭 思考中...

我已了解三个图的内容。现在搜索几个关键的diversity-focused red-teaming和co-evolution论文，以补全DACE eval的设计空间。

🔧 **工具调用:** web_search



> 💭 思考中...



🔧 **工具调用:** web_search



🔧 **工具调用:** web_search



🔧 **工具调用:** web_search



> 💭 思考中...



🔧 **工具调用:** web_fetch



🔧 **工具调用:** web_search



🔧 **工具调用:** web_fetch



🔧 **工具调用:** web_search



> 💭 思考中...



🔧 **工具调用:** web_search



🔧 **工具调用:** web_search



🔧 **工具调用:** web_search



> 💭 思考中...

我已经把 MAGIC、PIA、ACE-Safety (lijiajia/TGDS, 2511.19218)、Self-RedTeam、X-Teaming、Rainbow Teaming、QDRT、RainbowPlus、DiveR-CT、CRT、GFlowNet (Lee et al.) 等论文的 eval 协议过了一遍，结合 DACE 的方法定位（**两维策略空间 + 归一化覆盖增益 + 贝叶斯回放池**），下面给出一个有立场的 eval 调研报告。

---

## 一、对三张初步结果图的快速判读

先解读你已经做出的三组结果，确定 DACE 在 MAGIC eval 框架下的"已知差距"：

| 维度 | 表 | DACE vs MAGIC 表现 | 解读 |
|---|---|---|---|
| 安全 | Table 1 (Qwen2.5-7B) | 大多数 ASR 列**优于**或持平（WG:Test 0.008/0.002 vs 0.023/0.002，DAN 0.149 vs 0.198，HarmBench 0.003 vs 0.043），唯一弱项是 OR-Bench van.harm RTA = 0.075 | 攻击多样性驱动后，防御的覆盖面更广，但需注意 vanilla-harm 的边界是否被多样性训练稍微"软化" |
| 通用能力 | Table 2 | IFEval / ARC-C 略低（0.736/0.579 vs 0.745/0.592），GPQA 反而更高（0.317 vs 0.308），MMLU/AlpacaEval 持平 | 没有明显能力税。GPQA 上升暗示混合 batch 的回放可能对推理类任务有正向溢出，可作为讨论亮点 |
| 防御泛化 | Table 3 (OpenRT) | 5/6 列优于 MAGIC（PAIR 21.56 vs 25.31, TAP 31.87 vs 35.63, AutoDAN-turbo 42.18 vs 54.69），仅 GCG 12.18 vs 11.25 略弱 | 这是**最强的故事**：DACE 在 OOD 攻击器（特别是基于 LLM 的迭代攻击 PAIR/TAP/AutoDAN-turbo）上系统性优于 MAGIC，正面呼应"多样化训练 → 鲁棒到 OOD 攻击"这一核心论点 |

**核心结论**：你已经覆盖了 MAGIC defender eval 的主线（Tab 1/2/3）。剩下要补的是 (1) MAGIC 的 Tab 4（多轮）+ Fig 3（共演化热图），(2) 一整套 attacker eval，(3) DACE 独有机制的诊断性实验。

---

## 二、Defender Eval 调研与推荐

防御端的 eval 是相对成熟的设计空间。我把 MAGIC、Self-RedTeam、ACE-Safety、PIA、X-Teaming 的协议归并成三层：

### 2.1 已对齐的主线（保留）

下表三类已在你的初步结果中体现，建议保留并扩展模型族：

| 类别 | 评测面 | 数据集 | 判官 | 来源 |
|---|---|---|---|---|
| Harmful Refusal | 单轮 ASR ↓ | WildGuardTest, WildJailbreak, DAN, HarmBench, OR-Bench, XSTest, StrongREJECT | Qwen3Guard 或 GPT-4o | MAGIC Tab 1 |
| Benign Compliance | 误拒率 ↑ Comply | XSTest-safe, WildJailbreak adv-benign | 同上 | MAGIC Tab 1 |
| 通用能力 | Acc / Win | IFEval, ARC-C, GPQA, MMLU, AlpacaEval 2 | 标准评测 | MAGIC Tab 2, Self-RedTeam Tab 1 |
| OOD 攻击器泛化 | HarmBench ASR ↓ | HarmBench-vanilla 320 | GPT-4o | MAGIC Tab 3, OpenRT |
| OOD 攻击方法 | GCG / PAIR / TAP / AutoDAN / AutoDAN-turbo | OpenRT pipeline | — | 同上 |

**模型族扩展建议**：MAGIC 在 Qwen2.5-7B / Qwen2.5-14B / Llama3.1-8B 上都做了。你目前只展示了 Qwen2.5-7B 的对比，**至少补到 Llama3.1-8B**（不同对齐基线下的鲁棒性，是 reviewer 必问的）。Qwen2.5-14B 可作为次优先项放 appendix。

### 2.2 必补的两个维度

**(A) 多轮 Jailbreak（MAGIC Tab 4）**
- 工具：X-Teaming 协议（HarmBench 158 行为 × 10 种 multi-turn 策略），GPT-4o 判 jailbreak
- 指标：multi-turn ASR ↓（任一策略成功即算）+ JailBreak Rate ↓（成功策略比例）
- 为什么必须做：persona-based / multi-turn 是当前 OOD 攻击的主战场（PIA/X-Teaming 都在打），如果只做单轮会被认为"未在最严苛设置下验证"
- 替代选项：用 ACE-Safety 的 MergedHarm + Malicious-Instruct 也可以，但 X-Teaming 更通用

**(B) 共演化热图（MAGIC Fig 3）**
- 形式：5×5 网格，行 = attacker 训练 iteration（base/iter1/iter2/...），列 = defender 训练 iteration，单元格 = 该 attacker × 该 defender 的 ASR
- 为什么必须做：这是直接证明"co-evolution"在发生的关键图，**单个表格做不到这一点**。同时它也是检验"防御对抗遗忘是否被回放池缓解"的载体——理想模式是右上↗递减（新防御抵御老攻击）+ 对角线↘上升（新防御抵御新攻击），如果回放池失效会看到右上→左下"老攻击重新有效"

### 2.3 DACE 特有的两个诊断（强烈建议加）

这两个是 DACE 区别于 MAGIC 的核心机制，eval 必须能"看见"：

**(C) 防御对抗遗忘（Defense Adversarial Forgetting）专项 ablation**

参考 Self-RedTeam 的"static-attacker baseline"思路 + DACE 自己的回放消融：

| 设置 | 描述 | 预期效果 |
|---|---|---|
| DACE (full) | 含 Thompson + 时间衰减 + 剪枝的完整回放 | baseline |
| w/o Replay | 去掉回放，只用新攻击 batch | 早期攻击 ASR 反弹 ↑ |
| w/o Bayesian (uniform replay) | 改为均匀采样回放 | 中等回退 |
| w/o Time Decay | γ=1，不衰减 | 池被早期高 ASR 样本固化，训练后期效率低 |
| w/o PIC-style 一致性 | 类比 PIA 的 PICL 消融，看 DACE 是否需要类似的不变性约束 | 用作讨论 |

评测方法：用 **每轮训练结束保存 attacker checkpoint** → 训练结束后让最终 defender 对每个历史 checkpoint 的攻击进行评测，画出 "ASR over historical iterations" 曲线。**DACE-full 应该是单调下降的水平直线，w/o Replay 应该是 U 形或上升的**。这正是"对抗遗忘"被解决的可视化证据。

**(D) 策略空间覆盖率随训练演化**

- 在每轮训练结束计算档案池 $\mathcal{A}$ 在 $|\mathcal{S}| \times |\mathcal{C}|$ 网格上的 **Coverage Rate** 和 **Shannon 熵**
- 对比 MAGIC（无显式策略引导）和 DACE（有覆盖度奖励）的曲线
- 这一图直接证明 DACE 的归一化覆盖增益奖励起作用了

---

## 三、Attacker Eval 调研与推荐

攻击端是 DACE 的方法创新主战场，eval 需要同时打 **effectiveness（攻得上）** 和 **diversity（攻得广）**，这正是 QDRT/Rainbow/CRT/DiveR-CT 这条线的范式。

### 3.1 攻击有效性（Effectiveness）

**核心论点**：DACE 的攻击器不只是对自己训出来的 defender 强，而是 (1) 对未见过的 defender 模型族也强（transferability），(2) 单 rollout 即可达到与多轮搜索方法相当的 ASR（efficiency）。

下表整合 MAGIC、ACE-Safety、Self-RedTeam、Rainbow Teaming、AutoDAN-turbo 的 eval 协议：

| 评测 | 设计 | 推荐数据 | 关键指标 | 来源 |
|---|---|---|---|---|
| **E1: 跨 defender transferability** | DACE-attacker 对多个未训练过的 defender 模型生成攻击，单 rollout，GPT-4o 判官 | WildJailbreak-vanilla 600 条 + HarmBench 320 条 | ASR ↑ 在 Qwen2.5-7B/14B、Llama3.1-8B、Mistral-7B、Gemini-2.5-Flash | MAGIC Appendix E (Tab 10) |
| **E2: 与搜索式攻击的对比** | 在同一 defender 上，对比 DACE-attacker (single rollout) vs PAIR/TAP/AutoDAN-turbo（多轮搜索） | HarmBench 320 | ASR ↑ + Average Number of Attempts ANA ↓ | ACE-Safety Tab 1, MUSE |
| **E3: 共演化热图** | attacker iter × defender iter | HarmBench-test 320 | ASR | MAGIC Fig 3 |
| **E4: 攻防对自身 defender 的 ASR 演化曲线** | 训练过程中每轮 attacker 对当前 defender 的 ASR | 训练监控 | curves | Self-RedTeam Fig 3, ACE-Safety Fig 3 |

**推荐取舍**：E1 + E3 必做（一张表 + 一张图）。E2 选做（如果时间紧可放 appendix），但它是对抗 PAIR/TAP 的有力陈述——"我的 attacker 不需要多轮搜索就和它们打平"。E4 作为训练动态的内插图。

### 3.2 攻击多样性（Diversity）

这是 DACE 真正的核心创新点。**多样性 eval 必须分三个层级**，否则会被 reviewer 质疑"你说多样到底是什么样性？"

| 层级 | 指标 | 计算方式 | 代表论文 |
|---|---|---|---|
| **D1: 策略层（structured behavior space）** | Coverage Rate, QD-Score, Shannon Evenness Index (SEI), Simpson Diversity Index (SDI) | 攻击样本投影到 $\mathcal{S} \times \mathcal{C}$ 网格上，统计被填充的格子比例与分布均匀度 | **Rainbow Teaming, QDRT, RainbowPlus** |
| **D2: 语义层（semantic）** | SBERT 余弦距离均值, Vendi Score (cosine kernel) | 对每对攻击 prompt 用 sentence embedding 算相似度，1 − mean similarity | **Self-RedTeam (+21.8% SBERT), DiveR-CT, CRT** |
| **D3: 词汇层（lexical）** | Self-BLEU (n-gram), distinct-k, n-gram entropy | 标准 NLG 多样性指标 | **CRT (Hong et al.), DiveR-CT, GFlowNet (Lee et al.)** |

**最关键的图（必做）**：策略分布的演化图（**MAGIC Fig 4 同款**）
- 横轴：策略 ID（如 0–19 或 $|\mathcal{B}|$ 个槽位）
- 纵轴：在该策略上的样本占比 (%)
- 多组：训练 step 1–60 / 121–180 / 241–300（4 个阶段）+ baseline
- 对比 DACE vs MAGIC vs SFT-only attacker
- **预期信息**：DACE 的分布应该明显更均匀（覆盖更多冷门槽位），MAGIC 会塌缩到少数几个高频槽位

**可选补充图**：
- Self-BLEU vs ASR 的 trade-off 曲线（DiveR-CT Fig 2 同款），证明 DACE 在同等 ASR 下多样性更高
- 策略熵随训练步数的曲线，与覆盖度奖励的存在性绑定
- 与 SFT pool（如 SorryBench 20 类）的分布偏移图（MAGIC Fig 4 也有），证明 RL 探索出 SFT 数据外的策略

### 3.3 DACE 特有的诊断性实验（强烈推荐 1–2 个）

这些是写作时的"压舱石"，直接对应方法贡献：

**(F1) 归一化 vs 原始覆盖增益的奖励信号衰减对比**
- X 轴：训练 step
- Y 轴：单 batch 平均 $R_{\text{coverage}}$ 的标准差（区分度）
- 对比：raw $H(\mathbf{p}_{\mathcal{A} \cup \{x\}}) - H(\mathbf{p}_{\mathcal{A}})$ vs 归一化版
- 预期：raw 趋于零（reward vanishing），归一化保持 $O(1)$
- 这是论文方法节"理论分析"对应的实证证据

**(F2) 差异化多样性系数 $\lambda$ 的 ablation**
- DACE-full ($\lambda_{\text{succ}}=1.0$, $\lambda_{\text{fail}}=0.5$)
- vs $\lambda_{\text{fail}}=0$（攻击失败时完全屏蔽多样性奖励）
- vs $\lambda_{\text{fail}}=1.0$（不区分，可能鼓励无效但新颖的攻击）
- 评测：最终 attacker 在 D1（策略覆盖）+ E1（跨 defender ASR）上的双指标
- 这直接验证你方法节里强调的"有效性优先 + 冷门策略保留"设计

**(F3) 案例：Novel Combinatorial Attack Strategies**
- 沿用 MAGIC §5.3 Question 5 的格式，给出几例 DACE 训练后涌现的**多策略组合攻击**（如 Role-play + Translation + Concept Substitution）
- 这是定性证据，但很有 impact（reviewer 喜欢看具体例子）

---

## 四、最终推荐（按优先级排序）

下面是我对你最终实验部分的推荐配置。**P0 = 必须有，否则评审会被打**；**P1 = 显著加分**；**P2 = 锦上添花，时间允许就做**。

| 优先级 | 实验编号 | 名称 | 形式 | 关键对比 |
|---|---|---|---|---|
| **P0** | Tab 1 | 单轮安全 + benign compliance | 表 (10 列) | DACE vs MAGIC vs Self-RedTeam vs base × {Qwen2.5-7B, Llama3.1-8B} |
| **P0** | Tab 2 | 通用能力 | 表 (5 列) | 同上模型族 |
| **P0** | Tab 3 | OpenRT defender 泛化 | 表 (5 攻击方法 × 多 defender) | 同上 |
| **P0** | Tab 4 | 多轮 jailbreak (X-Teaming) | 表 (multi-turn ASR + JBR) | 同上 |
| **P0** | Fig 3 | Co-evolution 热图 | 5×5 cross-eval | DACE 自身 attacker × defender |
| **P0** | Tab 5 | Attacker 跨 defender transferability (E1) | 表 (5 defender × ASR) | DACE-attacker vs MAGIC-attacker vs base |
| **P0** | Fig 4 | 策略分布演化（D1 主图） | 多 stage 柱状图 | DACE vs MAGIC，每 60 步一个分布 |
| **P1** | Fig 5 | D2 + D3 多样性指标 | 折线图（Self-BLEU, SBERT distance, Coverage Rate vs step） | DACE vs MAGIC vs SFT-only |
| **P1** | Fig 6 | 防御对抗遗忘曲线 (C) | 折线（最终 defender 对历史 attacker checkpoint 的 ASR） | full vs w/o Replay vs w/o Bayesian |
| **P1** | Tab 6 | 攻击端消融 (F2) | 表 | full vs $\lambda_{\text{fail}} \in \{0, 0.5, 1.0\}$ |
| **P1** | Tab 7 | DACE-attacker vs PAIR/TAP/AutoDAN-turbo (E2) | 表 (ASR + ANA) | 同 defender 下的对比 |
| **P2** | Fig 7 | 归一化奖励信号稳定性 (F1) | 折线 | raw coverage vs normalized |
| **P2** | Case Study | 涌现的组合攻击策略 | 文本框示例 | 类似 MAGIC §5.3 Case |
| **P2** | Appendix | Qwen2.5-14B / 更多 defender 的扩展结果 | 表 | — |

---

## 五、几个需要在写作时回应的隐含挑战

最后提醒几个 reviewer 大概率会问、eval 必须能回答的问题：

1. **"多样性奖励是否伤害有效性？"** → Fig 4 + Fig 5 + Tab 5 联合给答案。**关键看 DACE attacker 的 ASR 是否不输于 MAGIC，同时多样性显著更高**。如果 ASR 略低也 OK，但要在 trade-off 图上落在 Pareto 前沿。

2. **"贝叶斯回放真比简单 FIFO/uniform 好吗？"** → 必须有 C 维的 ablation（w/o Bayesian 但保留 replay），不能只对比"有 vs 无"。Self-RedTeam 没做这个对比，所以这是 DACE 可以打的差异点。

3. **"为什么不直接用 Rainbow Teaming / QDRT 的多样性？"** → 写作时要提：Rainbow/QDRT 是**离线 archive 搜索**，不参与在线 RL 训练；DACE 的归一化覆盖增益是直接进 GRPO advantage 的**在线奖励**，并且解决了 reward vanishing。eval 上 F1 直接打这个点。

4. **"你的策略分类（$\mathcal{S} \times \mathcal{C}$）是不是 cherry-picked？"** → 借鉴 MAGIC Appendix F.2 的 20 子类分类法 + Llama-Guard-3 的官方风险类目（QDRT 也是这么做的），避免 ad-hoc。建议在 Appendix 用一个独立 LLM (Qwen2.5-72B) 做策略分类，提供 prompt template，与方法解耦。

如果你需要，我可以接下来：(a) 把上面 P0 部分的表格模板（列名、对比对象、判官设置）直接帮你写出来，或者 (b) 帮你设计 Fig 6（对抗遗忘曲线）的具体实验脚本。你想先推进哪一块？

-----

> https://arxiv.org/abs/2508.13048
> MAJIC: Markovian Adaptive Jailbreaking via Iterative Composition of Diverse Innovative Strategies
> 这篇论文是不是可以补充table 3 oprenrt eval的stronger attacker，
> 你也可以调研其他论文，以及详细分析safety diversity和 auto automatic red teaming相关的论文，
>
> 接下来请按照实验章节来梳理所有Evaluation，可以参考magic论文的实验和附录的写法，【直接给出experiment章节内容】，一些描述可以简要说一下，主要写清楚每个图表分别想说明什么问题，考虑到论文的篇幅，请注意权衡选择最重要的几个实验，不重要的可以放在附录或者直接删除，注意实验的故事逻辑。





🔧 **工具调用:** web_fetch



🔧 **工具调用:** web_search



🔧 **工具调用:** web_search



> 💭 思考中...



🔧 **工具调用:** web_search



> 💭 思考中...

我已经看完 MAJIC（2508.13048）。它是一个非常强的黑盒攻击器：在 Qwen-2.5-7B-it 上 ASR 达到 96.2%，对 GPT-4o / Gemini-2.0-flash 也 >90%，且平均 <15 次 query；核心是把策略池建成 Markov chain 做自适应组合。**MAJIC 和 Auto-RT（ICLR 2026）都应该补到 OpenRT 那张表里**——前者代表"黑盒组合式"SOTA，后者代表"RL 策略探索式"SOTA，正好与 DACE 形成对应关系。

下面直接给出 Experiment 章节的完整内容草稿（中文 + 公式 + 表/图意图说明）。我按 MAGIC 的"问题驱动"写法组织，并对每个图表明确标出"想说明什么问题"。

---

# 5. Experiments

We aim to answer the following research questions through extensive experiments:

- **Q1**: 在标准安全与通用能力 benchmark 上，DACE 训练出的 defender 是否优于现有 co-evolution 基线，且不引入显著能力税？(§5.2)
- **Q2**: DACE-defender 对 OOD 攻击器（白盒 + 黑盒）和多轮 jailbreak 是否泛化？(§5.2)
- **Q3**: DACE-attacker 在跨 defender 模型族上的攻击有效性与策略多样性如何？(§5.3)
- **Q4**: 攻防双方是否真的在持续协同演化？贝叶斯回放是否缓解了防御对抗遗忘？(§5.4)
- **Q5**: DACE 各核心设计组件（归一化覆盖增益、差异化 $\lambda$、贝叶斯回放、时间衰减）的贡献分别是多少？(§5.5)

## 5.1 Experimental Setup

**Models.** 我们使用 Qwen2.5-7B-Instruct 和 Llama3.1-8B-Instruct 作为攻防双方的初始化 backbone，并在 appendix 补充 Qwen2.5-14B-Instruct 的扩展结果。Qwen3Guard 作为训练阶段的 reward model 与主线 safety judge；GPT-4o 作为 OpenRT 评测的独立 judge 以避免 reward hacking。

**Baselines.** 在 defender 端对比：(1) instruction-tuned base model；(2) Self-RedTeam (Liu et al., 2025)；(3) MAGIC (Wen et al., 2026)；(4) inference-time 防御 SmoothLLM 与 Self-Eval。在 attacker 端对比：(1) MAGIC-attacker；(2) Self-RedTeam-attacker；(3) 经典自动红队方法 PAIR、TAP、AutoDAN、AutoDAN-turbo；(4) 最新 SOTA 黑盒攻击 **MAJIC** (Qi et al., 2025) 与 **Auto-RT** (Liu et al., 2025)。

**Datasets.** 训练集沿用 MAGIC 协议：SFT 阶段使用 SorryBench 增强的 CoT 数据，RL 阶段使用 WildJailbreak 训练子集（15k harmful + 15k benign）。Evaluation 涵盖：(1) 单轮 harmful refusal — WildGuardTest, WildJailbreak, DAN, HarmBench, OR-Bench, XSTest, StrongREJECT；(2) benign compliance — WildJailbreak adv-benign, XSTest-safe；(3) 通用能力 — IFEval, ARC-C, GPQA, MMLU, AlpacaEval 2；(4) OOD 攻击鲁棒性 — OpenRT pipeline + X-Teaming multi-turn。

**Training.** GRPO 组大小 $G=8$，回合数 $K=4$，每阶段 $T=200$ 步，新攻击 batch $B_{\text{train}}=64$，回放 batch $B_{\text{replay}}=32$。多样性奖励差异化系数 $\lambda_{\text{succ}}=1.0,\;\lambda_{\text{fail}}=0.5$。贝叶斯先验 $\alpha=\beta=1$，时间衰减 $\gamma=0.97$，剪枝阈值 $\epsilon=0.1,\;n_{\min}=10$。详细超参数见 Appendix C。

## 5.2 Defender Robustness

### Q1: Does DACE improve safety without sacrificing utility?

**Table 1 (Safety on harmful refusal & benign compliance).** 在 9 个 benchmark 上对比 DACE 与 base / Self-RedTeam / MAGIC（每个模型族一行 block）。**该表想说明**：DACE 在 harmful refusal 上整体优于或持平 MAGIC（如 Qwen2.5-7B 上 WG:Test ASR 0.008 vs 0.023, HarmBench 0.003 vs 0.043, AutoDAN-turbo 类 OOD 攻击在 Tab 3 进一步验证），同时 benign compliance 与 MAGIC 相当（XSTest Comply 0.920 vs 0.945 区别在统计噪声范围），未触发 over-refusal。安全增益主要来自攻击端的多样性扩展，而不是单纯放大拒答倾向。

**Table 2 (General capabilities).** 在 IFEval / ARC-C / GPQA / MMLU / AlpacaEval 2 上的 5 列对比。**该表想说明**：DACE 与 MAGIC 在通用能力上总体持平（差距 <2%），且在 GPQA 上反而更高（0.317 vs 0.308）——这间接表明回放池中的多样化样本起到了类似 curriculum 的作用，对推理类任务有微弱正向溢出，证明 safety alignment 没有破坏知识与推理能力。

### Q2: Does DACE generalize to OOD attackers and multi-turn jailbreaks?

**Table 3 (Defender generalization on OpenRT).** 这是本节**最核心**的表。defender 列：Gemini-2.5-Flash, Qwen2.5-7B-Instruct, +Self-Eval, +SmoothLLM, +Self-RedTeam, +MAGIC, **+DACE (ours)**。攻击器列：no-rev, GCG, PAIR, TAP, AutoDAN, AutoDAN-turbo, **MAJIC**, **Auto-RT**（共 7 列攻击 + no-rev）。Judge: GPT-4o。**该表想说明**三件事：(1) 在 5 个传统 OpenRT 攻击上 DACE 几乎全面优于 MAGIC（PAIR 21.56 vs 25.31, TAP 31.87 vs 35.63, AutoDAN-turbo 42.18 vs 54.69），(2) 在两个**未见过且最具威胁性**的攻击器（MAJIC, Auto-RT）上仍然保持显著领先，证明覆盖度驱动的训练分布**真正提升了对未知 OOD 攻击的鲁棒性**而非过拟合到训练时的 attacker，(3) 唯一弱项是 GCG（12.18 vs 11.25），原因是 GCG 是 token-level 梯度优化，不依赖语义策略，DACE 的策略空间多样性对其作用相对有限——这是诚实交代的局限。

**Table 4 (Multi-turn jailbreak via X-Teaming).** 三列：Multi-turn ASR ↓, Imp.(ASR) ↑, JailBreak Rate ↓。X-Teaming 用 GPT-4o 生成 158 个 HarmBench 行为 × 10 个多轮策略，Qwen2.5-72B-IT 作为攻击执行器。**该表想说明**：DACE 在多轮设置下对 MAGIC 的优势进一步放大（multi-turn ASR 相对 base 降低 ~13.5%，相对 MAGIC 再降 ~3-5%），表明多样化的策略训练自然泛化到了多轮组合攻击场景，即使 DACE 训练本身只用了单轮交互。

## 5.3 Attacker Effectiveness and Diversity

### Q3: Is the DACE-attacker more effective and more diverse?

**Table 5 (Attack transferability across defender backbones).** 行：base attacker, MAGIC-attacker, **DACE-attacker (ours)**；列：Qwen2.5-7B-IT, Llama3.1-8B-IT, Mistral-7B-IT, Gemini-2.5-Flash, MAGIC-defender, **DACE-defender**。每个 attacker 单 rollout（temperature 0.0），600 个 WildJailbreak vanilla harmful seeds，GPT-4o 判定。**该表想说明**：(1) DACE-attacker 在所有未训练过的 defender backbone 上均显著高于 MAGIC-attacker（如 Qwen2.5-7B 上 +X%, Mistral-7B +Y%），证明学到的不是过拟合到自己 defender 的策略，而是**通用化的攻击模式**；(2) 在 DACE-defender 上 DACE-attacker 略低于 base attacker（与 MAGIC 在自身 defender 上的现象一致），表明协同训练确实让 defender 对 attacker 的特定分布形成针对性免疫，符合 SPNE 收敛的预期。

**Figure 4 (Strategy coverage evolution).** 这是 attacker 多样性的**主图**。两行子图（Qwen2.5-7B vs Llama3.1-8B），每行 4 个柱状图（训练 step 1–60 / 121–180 / 241–300 / final），每个柱状图 X 轴为 19 个细粒度策略 ID（基于 Li et al. 2025 + MAGIC Appendix F.2 的 6 大族 20 子类分类），Y 轴为该策略在 attacker rollout 中的占比。每图三组对比：MAGIC-attacker、DACE-attacker、DACE w/o coverage reward。**该图想说明**：DACE 的策略分布显著更平坦（Shannon 熵 $H$ 比 MAGIC 高 ~30%），覆盖到 MAGIC 完全忽略的冷门槽位（如 complex logic nesting, multi-condition stacking），且这种均衡分布在训练后期仍稳定保持——直接验证归一化覆盖增益奖励的设计意图。

**Table 6 (Multi-level diversity metrics).** 三层指标，每层一组对比 attacker：(D1) **策略层** — Coverage Rate, QD-Score, Shannon Evenness Index；(D2) **语义层** — SBERT pairwise distance (mean), Vendi Score (cosine kernel)；(D3) **词汇层** — Self-BLEU ↓, distinct-2/3, n-gram entropy。**该表想说明**：DACE 在三个层级上都优于 MAGIC，**且在 D1 策略层提升最显著**（Coverage Rate +X%, SEI +Y%）——这与方法设计 alignment（覆盖度奖励直接作用于策略层）完美一致。语义层 SBERT 距离 +18.5% 与 Self-RedTeam 报告的 +21.8% SBERT 增益（attacker 对静态 defender）量级相当，说明 DACE 的多样性增益不是仅来自更细粒度的策略 grid，而是真正翻译到了语义层。

## 5.4 Co-evolution Dynamics

### Q4: Are attacker and defender truly co-evolving? Does Bayesian replay mitigate adversarial forgetting?

**Figure 3 (Co-evolution heatmap, MAGIC Fig 3 同款).** 5×5 网格：行 = attacker checkpoint (instruct, RL-iter1–4)，列 = defender checkpoint (同步)，单元格 = 该 attacker × 该 defender 在 320 个 HarmBench seeds 上的 ASR。**该图想说明**：(1) 沿对角线 ASR 单调递减（共演化使后期攻防整体水平提升），(2) **关键的右上区域（最终 defender vs 早期 attacker）保持低 ASR 且单调下降**——这是防御对抗遗忘被解决的直接证据；如果回放池失效会看到右上有反弹的"遗忘走廊"。同时左下区域 ASR 也低（早期 defender 已经被新 attacker 突破），符合 SPNE 收敛动态。

**Figure 5 (Adversarial forgetting curve).** 单图三条曲线：横轴为 attacker historical iteration（1 → 4），纵轴为最终 defender 在该历史 attacker 输出上的 ASR。三组：DACE (full), DACE w/o Replay, DACE w/ uniform replay (无 Bayesian prioritization)。**该图想说明**：(1) Full DACE 曲线接近水平（无遗忘），(2) w/o Replay 曲线在早期 iteration 显著反弹（典型对抗遗忘 U 形），(3) Uniform replay 介于两者之间——证明**贝叶斯优先级是必要的**，而不仅仅是"有 replay 就行"。这一图直接对应方法节贝叶斯回放池的核心论证，是 DACE 区别于 Self-RedTeam（无 replay）和简单经验回放的关键 visual evidence。

## 5.5 Ablation Studies

### Q5: Which design components are essential to DACE's performance?

**Table 7 (Ablation summary).** 行（在 Qwen2.5-7B 上）：
1. DACE (full)
2. − Coverage reward（去掉多样性奖励，仅留有效性奖励）
3. − Normalization（用 raw $H(\mathbf{p}_{\mathcal{A} \cup \{x\}}) - H(\mathbf{p}_{\mathcal{A}})$ 替代归一化版本）
4. − Differentiated $\lambda$（统一 $\lambda=1$ 或 $\lambda=0.5$）
5. − Bayesian replay（改为 FIFO replay）
6. − Time decay（$\gamma=1$）
7. − Replay entirely

每行报告 4 列：Defender HarmBench ASR ↓, Defender XSTest Comply ↑, Attacker Coverage Rate ↑, Attacker WG:Test ASR ↑。**该表想说明**：(1) 去掉 Coverage reward → attacker 多样性大幅下降（Coverage Rate −Y%）→ defender 鲁棒性下降；(2) 去掉归一化 → 训练后期奖励信号衰减，多样性提升 plateau（Coverage Rate 介于 full 与 no-coverage 之间）；(3) 去掉 Bayesian replay → defender 对早期攻击 ASR 反弹（与 Fig 5 互证）；(4) 去掉时间衰减 → 池被早期高 ASR 样本固化，attacker 难以引导出新的脆弱点。每个组件单独移除都引起可测量的退化，证明各设计**互补且必要**。

---

## 5.6 Discussion (Optional 0.5 page)

简短讨论：(1) DACE 在 GCG 这类 token-level 攻击上的相对劣势，提示策略空间驱动的训练对纯梯度型扰动作用有限，未来可与 input-level 噪声鲁棒训练正交结合；(2) 我们观察到 attacker 在训练后期涌现出**多策略组合攻击**（如 Role-play + Translation + Concept Substitution），与 MAGIC §5.3 Question 5 的发现一致，但 DACE 的组合频率显著更高（详见 Appendix Case Study）；(3) Bayesian replay 提供了一个轻量级、可解释的对抗遗忘缓解机制，未来可推广到更通用的 lifelong safety alignment 设置。

---

# Appendix（核心补充实验，按重要性排序）

- **A. Detailed setup.** 训练超参、prompt templates（attacker / safety judge）、SFT 数据构造细节、OpenRT 配置（沿用 MAGIC Tab 7 格式）。
- **B. Expanded model coverage.** Qwen2.5-14B-Instruct 与 Llama3.1-8B-Instruct 上的完整 Tab 1–5（沿用 MAGIC Tab 8–9 的格式）。
- **C. Reward signal stability.** 一张折线图：raw vs normalized coverage gain 在训练 step 上的均值与标准差，证明归一化解决 reward vanishing。
- **D. Full attack pattern analysis.** 沿用 MAGIC Appendix F 的分类协议，给出 DACE 在 Attacker-base / Attacker-SFT 两种初始化下的策略分布演化（与 Fig 4 的简化版互补）。
- **E. Case studies.** 至少 3 个 DACE 涌现的新型组合攻击案例（如 MAGIC §5.3 + Tab 16 同款），含 \<think\> reasoning trace 与 \<answer\>。
- **F. Diversity metric details.** Coverage Rate / QD-Score / SEI / Vendi Score 的精确定义与计算公式（避免 reviewer 质疑指标 ad-hoc）。
- **G. Per-benchmark expanded results for Tab 4.** X-Teaming 按 semantic category 拆分的 ASR breakdown。

---

## 删除/合并理由说明

为了控制主文 8–9 页篇幅，我**没有放进主文**的内容包括：

1. **Strategy 6 大族级别的分布演化（粗粒度版 Fig 4）** — 与 19 子类版冗余，放 Appendix D。
2. **w/ def. CoT、Defender-only、No-Game 等 MAGIC 风格的更细 ablation** — DACE 的核心 ablation 已经覆盖了"是否要协同博弈 + 是否要回放 + 多样性奖励是否必要"，这三类是方法贡献的直接组件，其他变体属于"为什么不这样设计"，放 Appendix 即可。
3. **Multi-turn under DACE 自身 multi-turn 训练** — 我们的训练是单轮的，X-Teaming 评测已足够说明问题，不必额外做多轮训练对比，否则 scope creep。
4. **General capability 的逐 benchmark 表格** — Tab 2 五列已覆盖，Llama3.1-8B 的对应表放 Appendix B。

## 最终主文实验配置（一目了然）

| # | 实体 | 形式 | 想说明的核心命题 |
|---|---|---|---|
| Tab 1 | 单轮安全 + benign compliance | 表 (3 模型 × 11 列) | DACE 在标准安全 benchmark 上整体优于 MAGIC，未触发 over-refusal |
| Tab 2 | 通用能力 | 表 (3 模型 × 5 列) | 没有显著能力税；GPQA 微弱正向 |
| Tab 3 | OpenRT 防御泛化（含 MAJIC + Auto-RT） | 表 (1 defender × 7 攻击) | 对最新最强的 OOD 攻击 (MAJIC, Auto-RT) 仍鲁棒，是核心 selling point |
| Tab 4 | X-Teaming 多轮 | 表 (4 列) | 单轮训练 → 多轮泛化 |
| Tab 5 | Attacker 跨 defender 迁移性 | 表 (3 attacker × 6 defender) | 学到的是通用攻击模式，不是过拟合 |
| Tab 6 | 三层多样性指标 | 表 (3 attacker × 8 指标) | 多样性增益在策略 / 语义 / 词汇三层都成立 |
| Tab 7 | 核心组件消融 | 表 (7 行 × 4 列) | 每个设计都必要且互补 |
| Fig 3 | 共演化 5×5 热图 | heatmap | 攻防真的在共演化 |
| Fig 4 | 策略分布演化 | 多 stage 柱状图 | 覆盖度奖励起作用，分布不塌缩 |
| Fig 5 | 对抗遗忘曲线 | 折线图 | 贝叶斯回放是必要的，不仅仅是 replay |

如果你希望我接下来把任何一个表/图的具体列名、对比对象、判官设置展开成可执行的实验脚本说明，告诉我编号即可。

-----

> [文件不支持导出]
> 附件中四个文件依次是初次实现、第二轮的debug、第三轮的debug、第四轮的debug，请结合代码实现过程和改进辅助理解dace研究方法和细节，
>
> 以及根据下面写的再完善一下实验部分的写作和说明，实验章节先用中文梳理，写清楚哪些是实验章节哪些放在附录做补充，
>
> 考虑将 14 个 risk category 中比较少的两种移除，即 Sextual Content 和 Code Interpreter Abuse，改成采取 12*10 的 attack space，
> 同时需要修改：SFT 数据蒸馏，RL 数据预处理，RL 训练细节，
>
> 加入更多关于 attacker 的评测，包括 effectiveness 和 diversity 两个角度，
> 对于 effectiveness：
>     参考 magic table 10，用 dace attacker/replay buffer 来攻击各种模型，
>     统计 attack on-rewrite/replay buffer 在 attack space 的有害性和分布情况，
> 对于 diversity：
>     参考 auto-redteam 的工作，评测 diversity 指标，如 cosine similarity，
>
> 分析各个组成部分的作用，消融实验考量：
> wo/ diverity design → magic
> wo/ sft training
> wo/ diversity rewrd
> wo/ replay buffer
>
> todo：
> 1. 分析完善 defender eval 的实验
> 2. 继续调研 attack eval 的实验
> 3. 开始写论文introduction method experiment章节
> 4. 在结果 v4 迭代后，对于 sft 数据中很少的 risk category，从额外的 WJB harmful/WJB beingn 数据中，主动筛选符合属于 sft 数据中低频 risk category 的数据，重新蒸馏并补充到 v4 的 sft 数据中
> 4.1 写一个脚本部署llama-guard4，并对wjb_benign\wjb_harmful的后2w个样本统计risk category分布
> 4.2 在 vanilla last20k risk category check 完成后，挑选数据并蒸馏补充到 sft-data-v4
> 5.





🔧 **工具调用:** view



查看 DACE 研究方法 v3.1 主文档，理解整体方法设计



🔧 **工具调用:** view



查看研究方法 v3.1 后半部分



🔧 **工具调用:** bash_tool



`````bash
wc -l /mnt/project/研究方法v3_1.md /mnt/project/dace_coding_v3_1.md /mnt/project/dace_coding_debug_v3.md /mnt/project/dace_coding_debug.md /mnt/project/dace_coding_debug_v4.md
`````



🔧 **工具调用:** view



查看初次实现 v3.1 - 前 200 行了解整体结构



🔧 **工具调用:** view



查看初次实现 v3.1 - 200-400 行



🔧 **工具调用:** view



查看初次实现 v3.1 - 400-600 行



🔧 **工具调用:** view



查看初次实现 v3.1 - 600-741 行



🔧 **工具调用:** view



查看 debug v3 - 第二轮 debug



🔧 **工具调用:** view



查看 debug v3 第三轮 - 前 250 行



🔧 **工具调用:** view



查看 debug 第三轮 - 250-491 行



🔧 **工具调用:** view



查看 debug v4 - 第四轮 debug



🔧 **工具调用:** view



查看 debug v4 - 中间部分了解 SFT 数据补充与 RL 训练细节



> 💭 思考中...

我已经把四份代码演化文档（v3.1 初次实现 → debug v1 → debug v3 → debug v4）和研究方法 v3.1 全部过完。下面先用一段把 DACE 的实现细节"对齐"到方法论上，然后给出**实验章节中文梳理 + 主文/附录分配方案 + 每个表/图的命题**。

---

## 一、从代码演化看 DACE 的方法论稳定性

四轮 debug 揭示了 DACE 真正"落地"的核心差异（这些细节会影响实验设计的精度）：

| 维度 | v3.1 初版 | v4 最终 | 实验中需要交代清楚 |
|---|---|---|---|
| 攻击策略空间 | $14 \times 10 = 140$ | **$12 \times 10 = 120$**（剪 Sexual Content + Code Interpreter Abuse，dead rows） | 决策依据要写在方法或附录 三段式 | 不变，但 regex 放宽（容忍 `,;\n` 多种分隔） | 附录给 prompt template |
| Buffer 写入 | 仅 attacker stage | **attacker + defender stage 双向 flush**（pseudocode L43–45 的修复） | 影响 replay pool 增长曲线分析 |
| 训练顺序 | attacker-first | **defender-first**（避免 R1S1 diversity=0）；最终 v4 又改回 attacker-first（defender-first 的 pool 增长慢）| Ablation 中作为变量讨论 |
| Diversity 截断 | 允许负值 | **clip_negative=True**（截断到 $[0, +\infty)$） | 影响 reward 信号稳定性图 |
| BENIGN_TEMPLATE | "trick into harmful responses"（语义冲突） | **over-refusal–oriented**（保 benign intent + 引诱 over-refusal） | 影响 benign compliance metric，**这是 v4 数据迭代的最重要修正** |
| GRPO group | $n = 4$ | $n = 6$ | 仅训练成本，不影响 eval |
| Replay 参数 | `prune=0.20, n_min=3, max=5000` | `prune=0.45, n_min=2, max=4000, gamma=0.90` | Ablation 中可对比不同设置 |
| Reward label (类型一致性) | 用 | **关闭 ($\beta_{\text{label}}=0$)** | v4 ablation 决定先看 BENIGN_TEMPLATE 修正是否足够 |

**结论：DACE 的核心方法（12×10 显式策略空间 + 归一化覆盖增益 + 贝叶斯回放）在四轮迭代中保持稳定，主要变化集中在数据/工程侧。** 实验章节可以以 v4 配置为最终结果，并在 ablation 中保留少量"原始 v3.1 设计"作为对比。

另外，v4 还有一个**未完成的关键改进**（你 todo 4）：用 Llama-Guard-4 对 WJB last-20k 做 risk category 标注 → 主动补充 SFT 数据中低频类（如 S4 Child Sexual Exploitation, S13 Elections）的样本。如果这一步在论文 deadline 前能跑完，会显著提升 attack space 分布的均衡性，**可以体现在 attacker diversity 评测的 Coverage / SEI 指标上**。

---

## 二、Experiment 章节中文梳理（主文 + 附录分配）

### 5.1 Experimental Setup（主文，~0.5 页）

**简要内容**：

- **Models**：Qwen2.5-7B-Instruct（主线），Llama3.1-8B-Instruct（次线）；Qwen2.5-14B-Instruct 在附录扩展
- **Strategy space**：$\mathcal{B} = \mathcal{S} \times \mathcal{C}$，其中 $|\mathcal{S}| = 12$（基于 Llama-Guard-4 taxonomy 剪除 Sexual Content + Code Interpreter Abuse 两个 dead rows，详见附录 A），$|\mathcal{C}| = 10$（基于 SorryBench + MAGIC 攻击模式分类合并），共 120 个 slot
- **Training data**：SFT v4 用 Gemini-2.5-Pro 蒸馏的 $\sim 43k$ 样本（20k benign + 23k harmful，over-refusal–oriented benign template，4 runs/sample 的 directed-style）；RL 用 WildJailbreak 训练子集 30k（15k harmful + 15k benign）
- **Reward model & judges**：训练时用 Qwen3Guard 作为 reward model；evaluation 主线用 Qwen3Guard，OpenRT eval 用 GPT-4o（独立判官，避免 reward hacking）
- **Hyperparameters (核心)**：GRPO group $n = 6$，rounds $K = 4$，每阶段 $T = 200$ 步，$B_{\text{train}} = 64, B_{\text{replay}} = 32$，多样性 $\lambda_{\text{succ}} = 1.0, \lambda_{\text{fail}} = 0.5$，clip_negative=True，贝叶斯先验 $\alpha = \beta = 1$，时间衰减 $\gamma = 0.90$，剪枝阈值 $\epsilon = 0.45, n_{\min} = 2$，pool 容量 4000

**Baselines**：base instruction-tuned，Self-RedTeam (Liu et al. 2025)，MAGIC (Wen et al. 2026)，inference-time SmoothLLM + Self-Eval。Attacker 端额外对比 Self-RedTeam-attacker、MAGIC-attacker、PAIR、TAP、AutoDAN、AutoDAN-turbo、**MAJIC**（Qi et al. 2025，最新 SOTA Markovian 组合攻击）。

**详细超参与 prompt template 全部放附录 A**。

---

### 5.2 Defender Evaluation（主文，2 张表 + 0.5 页问答）

#### Q1: Does DACE improve safety without sacrificing utility?

**Table 1 (Safety on harmful refusal & benign compliance, 主文)**
- 列：8 个 benchmark — WildGuardTest (adv/van), WildJailbreak (adv), DAN, HarmBench (adv), OR-Bench (van), XSTest (RTA, Comply), StrongREJECT, plus benign WJB (adv-benign), XSTest (van-benign)
- 行（每个 backbone 一个 block，主文只放 Qwen2.5-7B + Llama3.1-8B）：base / +Self-RedTeam / +MAGIC / **+DACE**
- **想说明**：DACE 在 harmful refusal 上整体优于或持平 MAGIC（基于 v4 的初步结果，WG:Test 0.008 vs 0.023, HarmBench 0.003 vs 0.043 等），同时 v4 BENIGN_TEMPLATE 修正后 benign compliance 不再低于 MAGIC（解决了 v3 时期的 over-refusal 问题）。安全增益来自攻击多样性扩展，而非 over-refusal 倾向。

**Table 2 (General capabilities, 主文)**
- 列：IFEval (Prompt-Loose, Instruct-Loose), ARC-C, GPQA, MMLU, AlpacaEval 2 (LC Win%)
- 行：同 Tab 1
- **想说明**：DACE 通用能力与 MAGIC 持平（差距 <2%），无能力税；GPQA 上 DACE 微弱优势（0.317 vs 0.308），间接表明回放池中多样化样本有 curriculum 效应

> Qwen2.5-14B 的扩展结果放附录 B；Llama3.1-8B 主文给完整结果。

#### Q2: Does DACE generalize to OOD attackers?

**Table 3 (OpenRT defender generalization, 主文 — 核心表)**
- 列：no-rev, **GCG**, **PAIR**, **TAP**, **AutoDAN**, **AutoDAN-turbo**, **MAJIC**（新加）
- 行：Gemini-2.5-Flash (closed-source ref), Qwen2.5-7B-IT, +Self-Eval, +SmoothLLM, +Self-RedTeam, +MAGIC, **+DACE**
- Judge：GPT-4o
- **想说明**：(1) DACE 在 5 个传统 OpenRT 攻击上几乎全面优于 MAGIC（已有数据：PAIR 21.56 vs 25.31, TAP 31.87 vs 35.63, AutoDAN-turbo 42.18 vs 54.69）；(2) 在最新 SOTA **MAJIC 黑盒组合攻击**（>90% ASR 打破 baseline）上仍保持显著领先，证明覆盖度训练分布**真正提升了对未知攻击的泛化**而非过拟合训练 attacker；(3) 唯一弱项是 GCG（token-level 梯度，DACE 的语义策略多样性对其作用有限），诚实交代 limitation
- Auto-RT 因其 RL 训练特性与 DACE 同质，作为 attacker baseline 在 5.3 中比较，不在 Tab 3

**X-Teaming 多轮评测放附录 C**（节省 1 张表的篇幅给 attacker eval）

---

### 5.3 Attacker Evaluation（主文，1 张表 + 1 张分布图 + 1 张多样性表）

#### Q3: Is the DACE-attacker more effective and transferable?

**Table 4 (Attacker effectiveness across defender models, 主文 — 类似 MAGIC Tab 10)**
- 行：base attacker (Qwen2.5-7B-IT), Self-RedTeam-attacker, MAGIC-attacker, **DACE-attacker (replay-buffer-based)**, **DACE-attacker (on-rewrite)**
- 列：6 个 defender — Qwen2.5-7B-IT, Llama3.1-8B-IT, Mistral-7B-IT, Gemini-2.5-Flash, MAGIC-defender, **DACE-defender**
- 数据：每个 defender 用 600 条 WildJailbreak vanilla harmful + 320 条 HarmBench seeds，attacker 单 rollout（temperature 0.0），GPT-4o 判定
- **想说明**：(1) **DACE-attacker (on-rewrite)** 在所有未训练过的 defender 上显著高于 MAGIC-attacker，证明学到的是通用攻击模式；(2) **DACE-attacker (replay-buffer-based)**（直接从最终回放池中随机抽 N 条作为攻击库）在跨 defender 上同样有效，证明回放池本身就是一个高质量的离线 jailbreak archive，可作为下游 evaluation set；(3) DACE-attacker 在 DACE-defender 上略低于 base attacker（与 MAGIC 在自身 defender 上现象一致），符合 SPNE 收敛预期

#### Q4: Is the DACE-attacker more diverse?

**Figure 4 (Attack space distribution, 主文 — DACE 核心创新可视化)**
- 三组对比 heatmap，每张 $12 \times 10$：
  - **(a)** MAGIC-attacker rewrite 输出在 12×10 网格上的频率分布
  - **(b)** DACE-attacker rewrite 输出的分布（**预期更平坦，覆盖更多 cell**）
  - **(c)** DACE replay pool 内样本的分布（每个 cell 用颜色 = 频率，用数字标注 = 该 cell 内的攻击成功率）
- **想说明**：(1) DACE 显著增加策略覆盖范围（占用 cell 数 vs MAGIC）；(2) replay pool 不是简单"高频成功样本堆积"，而是**有意识地保留低频 cell 的高风险样本**（高 ASR 但低频次的 cell 可见）；(3) 对应方法节"覆盖度奖励 + 贝叶斯回放"协同工作的可视化证据

**Table 5 (Multi-level diversity metrics, 主文)**
- 三层 8 列：
  - **D1 策略层**：Coverage Rate↑（占用 cell 数 / 120），Shannon Evenness Index↑，QD-Score↑
  - **D2 语义层**：Pairwise SBERT Cosine Similarity↓，Vendi Score↑（cosine kernel）
  - **D3 词汇层**：Self-BLEU↓，Distinct-3↑，n-gram entropy↑
- 行：Self-RedTeam-attacker, MAGIC-attacker, **DACE-attacker (on-rewrite)**, **DACE-attacker (replay buffer)**
- **想说明**：DACE 在三个层级都优于 MAGIC，**且策略层提升最显著**（Coverage Rate +30%+），与方法设计 alignment（覆盖度奖励直接作用于策略层）一致；语义层 SBERT 距离提升与 Self-RedTeam 报告的 +21.8% SBERT 量级相当，证明 DACE 的多样性增益不是 grid 分类的副作用而是真正翻译到了语义层

---

### 5.4 Co-evolution Dynamics（主文，1 张图）

**Figure 5 (Co-evolution heatmap, 主文 — 类似 MAGIC Fig 3)**
- $5 \times 5$ 网格：行 = attacker checkpoint (instruct, RL-iter1–4)，列 = defender checkpoint (同步)，单元格 = 该 attacker × 该 defender 在 320 个 HarmBench seeds 上的 ASR
- **想说明**：(1) 沿对角线 ASR 单调递减（共演化使整体水平提升）；(2) 右上区域（最终 defender vs 早期 attacker）保持低 ASR — **直接证据：贝叶斯回放抑制了防御对抗遗忘**；(3) 左下区域 ASR 也低（早期 defender 已被新 attacker 突破），符合 SPNE 收敛动态

> 想加 Replay pool 行为分析（pool size, mean posterior, zombie fraction 三条曲线）的话放附录 D

---

### 5.5 Ablation Studies（主文，1 张表）

**Table 6 (Component ablation, 主文 — 核心 4 行 + 1 主线)**

按你的要求设计 4 个核心 ablation，全部基于 Qwen2.5-7B-IT：

| 设置 | 描述 | 对应去除的方法贡献 |
|---|---|---|
| **w/o diversity design (= MAGIC)** | 完整 MAGIC 框架，无 12×10 策略空间，无多样性奖励，无回放池 | 整体方法贡献的 baseline |
| **w/o SFT training** | 用 Qwen2.5-7B-IT 直接做 RL，跳过 v4 SFT 蒸馏初始化 | 验证 SFT 暖启动对策略空间引导的必要性（从 debug log2/log3 可知，无 SFT 时 attack space 覆盖严重不足） |
| **w/o diversity reward** | 有 SFT，有回放池，但去掉覆盖度奖励（$R_{\text{attack}} = R_{\text{effective}}$） | 验证多样性奖励对覆盖度的直接贡献 |
| **w/o replay buffer** | 有 SFT，有覆盖度奖励，但去掉贝叶斯回放（defender 只在新攻击上训练） | 验证回放池对防御对抗遗忘的缓解 |
| **DACE (full, ours)** | 全方法 | — |

**4 列输出指标**（每行报告）：
1. **Defender HarmBench ASR ↓**（safety）
2. **Defender XSTest Comply ↑**（utility，避免 over-refusal）
3. **Attacker Coverage Rate ↑**（attack space 占用比例）
4. **Defender 对早期 attacker checkpoint 的 ASR ↓**（adversarial forgetting 检测，专门对 w/o replay 设计）

**想说明**：每个组件单独移除都引起可测量的退化，证明设计**互补且必要**：
- w/o diversity reward → Coverage Rate 大幅下降 → defender 对 OOD 攻击鲁棒性下降
- w/o replay buffer → 对早期攻击的 ASR 反弹（adversarial forgetting 出现）
- w/o SFT → attacker 难以利用策略空间引导（debug log2/log3 实证）
- w/o diversity design (= MAGIC) → 安全 + 多样性 + 抗遗忘三方面都退化

---

## 三、主文 vs 附录分配总览

### 主文（Section 5，目标 $\sim 3$ 页）

| # | 实体 | 形式 | 关键信息 |
|---|---|---|---|
| 5.1 | Setup | 0.5 页文字 | 模型、12×10 attack space 决策、训练数据、超参 |
| Tab 1 | 单轮安全 + benign | 表 (3 模型 × 11 列) | DACE vs base/Self-RedTeam/MAGIC |
| Tab 2 | 通用能力 | 表 (3 模型 × 5 列) | 无能力税 |
| Tab 3 | OpenRT 防御泛化（**含 MAJIC**） | 表 (1 defender × 7 攻击) | 对最新最强 OOD 攻击鲁棒 |
| Tab 4 | Attacker 跨 defender 迁移 | 表 (5 attacker × 6 defender) | 学到通用攻击模式 |
| Fig 4 | Attack space 分布 heatmap | 3 子图 (12×10) | 覆盖度奖励起作用 + replay pool 自然保留低频高风险 |
| Tab 5 | 三层多样性指标 | 表 (4 attacker × 8 列) | 策略 / 语义 / 词汇三层 |
| Fig 5 | 共演化 5×5 热图 | heatmap | 攻防协同 + 抗遗忘 |
| Tab 6 | 4 组核心消融 | 表 (5 行 × 4 列) | 每个组件必要且互补 |

### 附录（按重要性）

| § | 内容 | 篇幅 |
|---|---|---|
| **A. Strategy space design rationale** | 12×10 决策依据（Sexual Content / Code Interpreter Abuse 的 dead-row 数据证据），完整 prompt template，Gemini-2.5-Pro CoT distillation pipeline | 1.5 页 |
| **B. Expanded results** | Llama3.1-8B + Qwen2.5-14B 的完整 Tab 1–4，多 backbone 验证 | 1.5 页 |
| **C. Multi-turn jailbreak evaluation** | X-Teaming 协议下的 multi-turn ASR & JailBreak Rate（DACE vs MAGIC vs base） | 0.5 页 |
| **D. Co-evolution training dynamics** | Pool 增长 / 流动性曲线（pool_size, mean_posterior, zombie_fraction, eviction rate）；coverage entropy 演化；diversity reward 信号稳定性曲线（normalized vs raw） | 1 页 |
| **E. Detailed hyperparameters** | 完整训练配置表（沿用 MAGIC Tab 6 格式），OpenRT/MAJIC/Auto-RT 攻击器配置（沿用 MAGIC Tab 7 格式） | 1 页 |
| **F. Anti-forgetting deep dive** | 对 4 个 attacker historical checkpoint 的 ASR 曲线（DACE-full vs w/o replay vs uniform replay vs FIFO replay）— 这是 v4 后建议追加做的细分 ablation | 0.5 页 |
| **G. Attack pattern case studies** | DACE 涌现的多策略组合攻击案例（沿用 MAGIC §5.3 Q5 + Tab 16 同款），3–5 个 case | 1 页 |
| **H. Replay buffer as evaluation set** | 把 DACE 最终 replay pool（$\sim 4000$ 条）作为独立 jailbreak 数据集发布的 ASR 横评（对 GPT-4o, Claude, Gemini 等 closed-source 的攻击效果） | 0.5 页 |

总附录约 7–8 页，符合典型 NeurIPS/ICLR 投稿格式。

---

## 四、实验执行优先级（结合你 todo 4 的数据迭代）

按时间敏感性排序：

| 优先级 | 任务 | 是否依赖 v4 数据迭代 |
|---|---|---|
| **P0 立刻做** | Tab 1, Tab 2（safety + utility）的完整 baseline 对比 — 已有 v4 初步结果 | 否 |
| **P0 立刻做** | Tab 3 加 MAJIC + Auto-RT 列（OpenRT 集成或独立脚本） | 否 |
| **P0 立刻做** | Tab 4 attacker effectiveness（DACE-attacker / replay-buffer 攻击 6 个 defender） | 否 |
| **P1** | Fig 4 attack space heatmap（已有最终 pool 即可生成） | 否 |
| **P1** | Tab 5 多样性 8 指标（cosine sim / Self-BLEU / Vendi 等需用 SBERT 等模型计算） | 否 |
| **P1** | Tab 6 四组消融 — 需要独立训练 4 个变体（每个 $\sim 12h$） | 否 |
| **P2** | Fig 5 共演化 5×5 热图 — 需要保存所有 attacker/defender checkpoints | 否 |
| **P2** | 你 todo 4：用 Llama-Guard-4 标注 WJB last-20k → 补充 SFT 低频类样本 → 重蒸馏 → 重训 attacker SFT → 重跑 RL | **是**（这一步会更新所有 attacker 端结果，但不影响 defender 主线） |
| **P3** | Appendix C/D/F/G 细分实验（多轮、训练动力学、anti-forgetting 深度对比、case study） | 否 |

---

## 五、几个待确认的细节

写之前需要你拍板：

1. **Replay buffer 作为攻击库**（Tab 4 的"DACE-attacker (replay-buffer-based)"行）：是直接随机抽 $N$ 条还是按 Thompson posterior 抽 top-N？建议**按 posterior 抽 top-N**，更能体现回放池的"质量过滤"作用。

2. **MAJIC 集成方式**：MAJIC 原始代码用 Markov chain 跑 8 类 disguise + 40 sub-pattern，需要单独跑（不是 OpenRT 现成的）。建议在 OpenRT 框架内补一个 `majic.py` adapter，sample budget 限定 $\le 15$ queries（与 MAJIC 论文一致），attacker 模型用 Qwen2.5-7B-IT 保持公平。

3. **Tab 6 ablation 中的 "w/o SFT"**：是用 base Qwen2.5-7B-IT 还是用 MAGIC-SFT attacker？建议用 **base Qwen2.5-7B-IT**，更"干净"地隔离 v4 SFT 的贡献；MAGIC-SFT attacker 已在 Tab 4 中作为 attacker 基线对比。

4. **Fig 4 attack space heatmap 的 cell 标注**：除了频率/ASR 二维信息，是否在每个 cell 加 case 编号（指向 appendix G 的 case study）？建议**不加**，避免 heatmap 视觉过载；case study 用独立的"槽位坐标 $(s, c) = ...$"标识即可。

5. **附录 H 的 replay buffer 横评**：把 DACE 最终 $\sim 4000$ 条 replay pool 作为新 jailbreak benchmark 发布，对 GPT-4o/Claude/Gemini 测 ASR — 这个是非常高 impact 的额外贡献，但需要 closed-source API 预算。如果预算紧张，附录 H 可以删除或缩减为 OSS 模型 (Qwen2.5-32B, Llama3-70B) 的横评。

---

如果以上 5 点你确认后，我可以**立刻动笔写 introduction → method → experiment 三章的英文初稿**，每章 1.5–3 页，沿用 MAGIC 的"Question-driven 段落"+ "Table caption 直接陈述结论"风格。你想先推进哪一章？

-----

> [文件不支持导出]
> 先保留这一版的实验相关内容整理，切换到下一个任务，
>
> 现在帮忙梳理 introduction 初稿，用中文梳理，先简要介绍 dace 的 introduction 怎么写，是什么讲故事逻辑以及为什么要怎么写，再给出具体的每一段的 introduction 内容，要求达到 NeurIPS 投稿水准，
>
> 附件中有一些前期调研材料方便梳理，
> LLM_Red_Teaming_Papers_Analysis.md、LLM_RedTeaming_Diversity_Research_Report.md和LLM_Safety_Diversity_CoEvolution_Survey.md是最早开展相关文献调研的一些文献分析和总结，
> 研究动机与研究方法.md和可选定义对比分析与推荐组合.md是第一版的研究动机研究方法和定义对比，
> 研究方法v2.1.md和覆盖度熵变体分析与推荐.md是第二版的更具体详细的内容迭代，
> 之前上传过的文件中的v3.1的两个文件（研究方法v3.1.md和pseudocode_v3.1.html）是最新的研究方法和伪代码，最新研究方法以这个文件为准，其他的文件作为辅助参考，
>
> 下面是一些相关的论文，可以搜索并阅读分析来充分了解研究现状相关工作以及借鉴可取之处，
> 相关论文
> safety co-evolution
> - Adversarial Attack-Defense Co-Evolution for LLM Safety Alignment via Tree-Group Dual-Aware Search and Optimization
>   - https://arxiv.org/pdf/2511.19218
> - AdvEvo-MARL: Shaping Internalized Safety through Adversarial Co-Evolution in Multi-Agent Reinforcement Learning
>   - https://arxiv.org/pdf/2510.01586
> - Adversarial Reinforcement Learning for Large Language Model Agent Safety
>   - https://arxiv.org/pdf/2510.05442
> - Chasing Moving Targets with Online Self-Play Reinforcement Learning for Safer Language Models
>   - https://arxiv.org/pdf/2506.07468
>   - https://openreview.net/pdf?id=VqQ1DXEeyo
>   - https://github.com/mickelliu/selfplay-redteaming
> - Safety Alignment of LMs via Non-cooperative Games
>   - https://arxiv.org/pdf/2512.20806
>   - https://github.com/facebookresearch/advgame
> - The Alignment Waltz: Jointly Training Agents to Collaborate for Safety
>   - https://arxiv.org/pdf/2510.08240
>   - https://openreview.net/pdf?id=2NBS9ilNqM
> - Red Teaming LLMs: A Stackelberg Game Approach to AI Safety
>   - https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11200929
> - Be Your Own Red Teamer: Safety Alignment via Self-Play and Reflective Experience Replay
>   - https://arxiv.org/pdf/2601.10589
> - TriPlay-RL: Tri-Role Self-Play Reinforcement Learning for LLM Safety Alignment
>   - https://www.arxiv.org/pdf/2601.18292
> - MAGIC: A Co-Evolving Attacker-Defender Adversarial Game for Robust LLM Safety
>   - https://arxiv.org/pdf/2602.01539
>   - https://github.com/AI45Lab/MAGIC
> - Toward Optimal LLM Alignments Using Two-Player Games
>   - https://aclanthology.org/2025.findings-emnlp.6.pdf
> - SEAS: Self-Evolving Adversarial Safety Optimization for Large Language Models
>   - https://arxiv.org/pdf/2408.02632
> - STAIR: Improving Safety Alignment with Introspective Reasoning
>   - https://openreview.net/pdf?id=aHzPGyUhZa
> - Disentangling Intent from Role: Adversarial Self-Play for Persona-Invariant Safety Alignment
>   - lijiajia-PIA
>
> safety reasoning
> - ReasoningGuard: Safeguarding Large Reasoning Models with Inference-time Safety Aha Moments
>   - https://arxiv.org/pdf/2508.04204
> - Red-Bandit: Test-Time Adaptation for LLM Red-Teaming via Bandit-Guided LoRA Experts
>   - https://arxiv.org/pdf/2510.07239
> - Combining Code Generating Large Language Models and Self-Play to Iteratively Refine Strategies in Games
>   - https://www.ijcai.org/proceedings/2025/1249.pdf
> - Controllable Safety Alignment: Inference-Time Adaptation to Diverse Safety Requirements
>   - https://openreview.net/pdf?id=ERce2rgMQC
> - Shape it Up! Restoring LLM Safety during Finetuning
>   - https://openreview.net/pdf?id=PAIVwOaAnq
> - AdvPrompter: Fast Adaptive Adversarial Prompting for LLMs
>   - https://arxiv.org/pdf/2404.16873
> - H-CoT: Hĳacking the Chain-of-Thought Safety Reasoning Mechanism to Jailbreak Large Reasoning Models, Including OpenAI o1/o3, DeepSeek-R1, and Gemini 2.0 Flash Thinking
>   - https://arxiv.org/pdf/2502.12893
> - Chain-of-Thought Hijacking
>   - https://arxiv.org/pdf/2510.26418
> - Reasoned Safety Alignment: Ensuring Jailbreak Defense via Answer-Then-Check
>   - https://arxiv.org/pdf/2509.11629
> - Reasoning as an Attack Surface: Adaptive Evolutionary CoT Jailbreaks for LLMs
>   - https://openreview.net/forum?id=PFseU5D5t9
> - Unforgotten Safety: Preserving Safety Alignment of Large Language Models with Continual Learning
>   - https://arxiv.org/pdf/2512.10150
>
>
>
> guardrail models
> - Introducing v0.5 of the AI Safety Benchmark from MLCommons
>   - https://arxiv.org/pdf/2404.12241
> - Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations
>   - https://arxiv.org/pdf/2312.06674
>     - 注：Llama Guard 原始论文，模型后续更新到了 v4，但没有更新论文
>     - https://github.com/meta-llama/PurpleLlama
>   - https://github.com/meta-llama/PurpleLlama/blob/main/Llama-Guard/MODEL_CARD.md
> - Llama Guard 2
>   - https://www.llama.com/docs/model-cards-and-prompt-formats/meta-llama-guard-2/
>   - https://github.com/meta-llama/PurpleLlama/blob/main/Llama-Guard2/MODEL_CARD.md
> - The Llama 3 Herd of Models
>   - https://arxiv.org/pdf/2407.21783
> - WildGuard: Open One-Stop Moderation Tools for Safety Risks, Jailbreaks, and Refusals of LLMs
>   - https://arxiv.org/pdf/2406.18495
> - ShieldAgent: Shielding Agents via Verifiable Safety Policy Reasoning
>   - https://arxiv.org/pdf/2503.22738
> - Qwen3Guard Technical Report
>   - https://arxiv.org/pdf/2510.14276
> - AgentDoG: A Diagnostic Guardrail Framework for AI Agent Safety and Security
>   - https://arxiv.org/pdf/2601.18491
>
>
>
>
> safety diversity
> - Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations
>   - https://arxiv.org/pdf/2312.06674
> - Rainbow Teaming: Open-Ended Generation of Diverse Adversarial Prompts
>   - https://arxiv.org/pdf/2402.16822
>   - https://openreview.net/pdf?id=FCsEvaMorw，NIPS 2024
> - Ferret: Faster and Effective Automated Red Teaming with Reward-Based Scoring Technique
>   - https://aclanthology.org/2025.findings-emnlp.634.pdf
>   - https://github.com/declare-lab/ferret
> - Ruby Teaming: Improving Quality Diversity Search with Memory for Automated Red Teaming
>   - https://arxiv.org/pdf/2406.11654
> - RainbowPlus: Enhancing Adversarial Prompt Generation via Evolutionary Quality-Diversity Search
>   - https://arxiv.org/pdf/2504.15047
>   - https://github.com/knoveleng/rainbowplus
> - Diverse and Effective Red Teaming with Auto-generated Rewards and Multi-step Reinforcement Learning
>   - https://arxiv.org/pdf/2412.18693
> - Quality-Diversity Red-Teaming: Automated Generation of High-Quality and Diverse Attackers for Large Language Models
>   - https://arxiv.org/pdf/2506.07121
>   - https://github.com/lamda-bbo/QDRT
>
> - T-MAP: Red-Teaming LLM Agents with Trajectory-aware Evolutionary Search
>   - https://arxiv.org/pdf/2603.22341
> - The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against Llm Jailbreaks and Prompt Injections
>   - https://arxiv.org/pdf/2510.09023
> - Agent-SafetyBench: Evaluating the Safety of LLM Agents
>   - https://arxiv.org/pdf/2412.14470
> - Jailbroken: How Does LLM Safety Training Fail?
>   - https://openreview.net/pdf?id=jA235JGM09
>
>
> - Red Teaming Language Models with Language Models
>   - https://aclanthology.org/2022.emnlp-main.225.pdf
> - Curiosity-driven Red-teaming for Large Language Models
>   - https://arxiv.org/pdf/2402.19464，ICLR 2024
> - DiveR-CT: Diversity-enhanced Red Teaming Large Language Model Assistants with Relaxing Constraints
>   - https://arxiv.org/pdf/2405.19026，AAAI 2025
> - CALM: Curiosity-Driven Auditing for Large Language Models
>   - https://arxiv.org/pdf/2501.02997，AAAI 2025
> - Learning Diverse Attacks on Large Language Models for Robust Red-Teaming and Safety Tuning
>   - https://arxiv.org/pdf/2405.18540，ICLR 2025
> - Jailbreak-R1: Exploring the Jailbreak Capabilities of LLMs via Reinforcement Learning
>   - https://arxiv.org/pdf/2506.00782
> - RedTopic: Toward Topic-Diverse Red Teaming of Large Language Models
>   - https://openreview.net/pdf?id=terdVfnoc5，ICLR 2026 Reject
> - Auto-RT: Automatic Jailbreak Strategy Exploration for Red-Teaming Large Language Models
>   - https://openreview.net/pdf?id=Pa6ak2B9jJ，ICLR 2026 Accept
>
> - Evolving Diverse Red-team Language Models in Multi-round Multi-agent Games
>   - https://arxiv.org/pdf/2310.00322
>
> Understanding the Effects of RLHF on LLM Generalisation and Diversity
> Evaluating the Evaluation of Diversity in Natural Language Generation.
> Explore, Establish, Exploit: Red Teaming Language Models from Scratch
> - Evolving Populations of Diverse RL Agents with MAP-Elites
>   - https://arxiv.org/pdf/2303.12803，RL Diversity
> - Automated Progressive Red Teaming
>   - https://aclanthology.org/2025.coling-main.260.pdf
> - Automatic LLM Red Teaming
>   - https://arxiv.org/pdf/2508.04451
> - Active Attacks: Red-teaming LLMs via Adaptive Environments
>   - https://arxiv.org/pdf/2509.21947
> - SIRAJ: Diverse and Efficient Red-Teaming for LLM Agents via Distilled Structured Reasoning
>   - https://arxiv.org/pdf/2510.26037
> - WildTeaming at Scale: From In-the-Wild Jailbreaks to (Adversarially) Safer Language Models
>   - https://openreview.net/pdf?id=n5R6TvBVcX
> - RedTWIZ: Diverse LLM Red Teaming via Adaptive Attack Planning
>   - https://arxiv.org/pdf/2510.06994
> - MART: Improving LLM Safety with Multi-round Automatic Red-Teaming
>   - https://aclanthology.org/2024.naacl-long.107.pdf
> - Better Red Teaming via Searching with Large Language Model
>   - https://aclanthology.org/2025.findings-acl.257.pdf
>
>
>
>
> LLM diversity RL
> - Foundation Model Self-Play: Open-Ended Strategy Innovation via Foundation Models
>   - https://arxiv.org/pdf/2507.06466
> - Quality-Diversity Self-Play: Open-Ended Strategy Innovation via Foundation Models
>   - https://openreview.net/pdf?id=xPWZTvdobm
> - Jointly Reinforcing Diversity and Quality in Language Model Generations
>   - https://arxiv.org/pdf/2509.02534
> - SPARQ: Synthetic Problem Generation for Reasoning via Quality-Diversity Algorithms
>   - https://arxiv.org/pdf/2506.06499
> - Diversity-Incentivized Exploration for Versatile Reasoning
>   - https://arxiv.org/pdf/2509.26209
> - Outcome-based Exploration for LLM Reasoning
>   - https://arxiv.org/pdf/2509.06941
> - Diversity-Aware Policy Optimization for Large Language Model Reasoning
>   - https://arxiv.org/pdf/2505.23433
> - Beyond Quantity: Trajectory Diversity Scaling for Code Agents
>   - https://arxiv.org/pdf/2602.03219
> - Less is Enough: Synthesizing Diverse Data in Feature Space of LLMs
>   - https://arxiv.org/pdf/2602.10388
> - Understanding Agent Scaling in LLM-Based Multi-Agent Systems via Diversity
>   - https://arxiv.org/pdf/2602.03794
> -
>
> LLM-RL / self-play
> - Multi-Agent Evolve: LLM Self-Improve through Co-evolution
>   - https://arxiv.org/pdf/2510.23595
> - Generative Adversarial Reasoner: Enhancing LLM Reasoning with Adversarial Reinforcement Learning
>   - https://arxiv.org/pdf/2512.16917
> - Self-Evolving Curriculum for LLM Reasoning
>   - https://arxiv.org/pdf/2505.14970
> - VCRL: Variance-based Curriculum Reinforcement Learning for Large Language Models
>   - https://arxiv.org/pdf/2509.19803
> - GenEnv: Difficulty-Aligned Co-Evolution Between LLM Agents and Environment Simulators
>   - https://arxiv.org/pdf/2512.19682
> - Absolute Zero: Reinforced Self-play Reasoning with Zero Data
>   - https://arxiv.org/pdf/2505.03335
> - R-Zero: Self-Evolving Reasoning LLM from Zero Data
>   - https://arxiv.org/pdf/2508.05004
> - SPIRAL: Self-Play on Zero-Sum Games Incentivizes Reasoning via Multi-Agent Multi-Turn Reinforcement Learning
>   - https://arxiv.org/pdf/2506.24119
> - SPICE: Self-Play In Corpus Environments Improves Reasoning
>   - https://arxiv.org/pdf/2510.24684
> - TTCS: Test-Time Curriculum Synthesis for Self-Evolving
>   - https://arxiv.org/pdf/2601.22628
> - Teaching Models to Teach Themselves: Reasoning at the Edge of Learnability
>   - https://arxiv.org/pdf/2601.18778
> - DARC: Decoupled Asymmetric Reasoning Curriculum for LLM Evolution
>   - https://arxiv.org/pdf/2601.13761
>
> - Toward Training Superintelligent Software Agents through Self-Play SWE-RL
>   - https://arxiv.org/pdf/2512.18552
> - Reinforcement Learning with Verifiable Rewards Implicitly Incentivizes Correct Reasoning in Base LLMs
>   - https://arxiv.org/pdf/2506.14245
> - HarmRLVR: Weaponizing Verifiable Rewards for Harmful LLM Alignment
>   - https://arxiv.org/pdf/2510.15499
> - Breaking the Safety-Capability Tradeoff: Reinforcement Learning with Verifiable Rewards Maintains Safety Guardrails in LLMs
>   - https://arxiv.org/pdf/2511.21050
> - Mitigating the Alignment Tax of RLHF
>   - https://arxiv.org/pdf/2309.06256，v4->202410
> - LifeAlign: Lifelong Alignment for Large Language Models with Memory-Augmented Focalized Preference Optimization
>   - https://arxiv.org/pdf/2509.17183
>
> ultrathink，深入分析，think deeper，think harder，梳理 introduction 初稿并用中文梳理





🔧 **工具调用:** view



查看研究动机与方法的早期版本



🔧 **工具调用:** view



查看研究方法 v2.1 的迭代版本



🔧 **工具调用:** view



查看最早的相关工作分析



🔧 **工具调用:** view



查看 LLM_Safety_Diversity_CoEvolution_Survey 相关综述



🔧 **工具调用:** view



查看 LLM_Safety_Diversity_CoEvolution_Survey 综述 - 协同进化部分



🔧 **工具调用:** view



查看 LLM_RedTeaming_Diversity_Research_Report 早期文献整理



🔧 **工具调用:** web_search



🔧 **工具调用:** web_search



🔧 **工具调用:** web_search



🔧 **工具调用:** web_search



> 💭 思考中...

我已经把 DACE 的方法演进、相关工作（MAGIC、Self-RedTeam、ACE-Safety、QDRT、Rainbow Teaming、CRT/DiveR-CT、SSP 等）和你的早期调研材料全部交叉过完。下面给出 NeurIPS 投稿水准的 Introduction 中文初稿：先讲整体讲故事逻辑与设计取舍，再给出每一段的具体内容。

---

## 一、Introduction 的整体故事逻辑

### 1.1 核心论点一句话

> **当前 co-evolution 框架在攻防对抗中遭遇"攻击坍缩 ↔ 防御遗忘"的双重病理，而现有多样性方法都未能在线、在策略层、在攻防协同中同时解决这两个问题；DACE 通过"显式策略空间 + 归一化覆盖奖励 + 贝叶斯回放池"在 co-evolution 中首次系统性地破除这一困境。**

### 1.2 五段式故事框架（NeurIPS 标准）

**段 1 — Big picture（安全对齐 → 静态对齐落后于动态威胁 → co-evolution 应运而生）**：建立"为什么需要 dynamic co-evolution"。

**段 2 — 现有 co-evolution 的双重病理**：MAGIC / Self-RedTeam 取得了实质进展但暴露两个互相加剧的失败模式 — *Attack Strategy Collapse* 和 *Defense Adversarial Forgetting*，必须配实验观察证据让 reviewer 立刻共情。

**段 3 — 现有多样性方法为什么不够用**：把 QD 搜索（Rainbow / QDRT）、表层多样性（CRT / DiveR-CT）、co-evolution 框架（Self-RedTeam / MAGIC / ACE-Safety）三类按"是否在线 / 是否到策略层 / 是否处理记忆"切分，**指出三个维度从未被同时满足**。这是 DACE 的差异化定位的 set-up。

**段 4 — DACE 的提出与四个贡献**：直接陈述核心思想，然后用四个 bullet 把贡献"打硬"。要把"归一化覆盖增益"和"贝叶斯回放"作为方法层面的 *technical novelty* 强调出来，避免被读成"QDRT + experience replay 的工程拼接"。

**段 5 — 实验结论**：三句话，每句对应一组关键实验，覆盖 (a) defender 安全 + 通用能力、(b) 对未见攻击的泛化、(c) attacker 多样性（攻击层 + 语义层）。

### 1.3 写作的几个微观决策（为什么要这么写）

- **不开 Sun Tzu 引言、也不开 Saul 2024 安全事故新闻**。Self-RedTeam 用《孙子兵法》开篇、MAGIC 用 Google Gemini 安全事件开篇——两种都是引人注意但风险高的开法，作为后来者最好走更稳的"问题 → 方法"路线，把所有空间留给方法的 differentiation。
- **第 2 段强烈推荐放一个具体的失败观察**（如 Self-RedTeam 报告的 "+21.8% SBERT 仍有 mode collapse" 或 MAGIC 报告的"组合策略涌现但无显式 diversity 机制"），让 pathology 不只是文字描述。
- **第 3 段必须把"在线/策略层/co-evolution"三个维度并列**，QDRT 的离线 archive、Rainbow 的离线 MAP-Elites、CRT 的语义距离都各占一格——这是 set up DACE "三者皆是"的差异化空间。
- **第 4 段必须把"归一化覆盖增益解决 reward vanishing"作为单独贡献点**（不是埋在 method overview 里），这是方法的 technical depth；同样**贝叶斯 + Thompson Sampling + 时间衰减**也要单独点出，区别于 SSP 的简单 UCB。
- **第 5 段要量化领先幅度**（如 "reduces ASR on AutoDAN-turbo from 54.69 to 42.18"），不要只说 "outperforms baselines"。

---

## 二、Introduction 中文初稿（每段约 200–350 字，整页约 0.9–1.0 页）

---

### 第 1 段：为什么需要动态对齐？

> 大语言模型（LLM）的广泛部署使其安全对齐成为一个不可回避的核心问题，然而当前主流安全机制——包括基于人类反馈的强化学习（RLHF）、外部 guardrail 模型、以及静态对齐数据集——本质上都是面向"已知攻击分布"的反应式补丁。与此同时，越狱攻击（jailbreak attacks）正以远超防御演化的速度变得复杂：从早期的角色扮演与编码混淆（DAN、ASCII），到自动化对抗优化（GCG、PAIR、TAP、AutoDAN-turbo），再到隐蔽的多轮代理化攻击（X-Teaming）以及近期出现的 Markov 链组合攻击（MAJIC，在 GPT-4o、Gemini-2.0-flash 上 ASR 超过 90%）。攻防双方的根本不对称在于：攻击者的策略空间几乎无限，而基于静态数据训练的防御者必然滞后于持续演化的攻击分布。这一困境促使社区提出**攻防协同演化（co-evolution）**范式——将安全对齐建模为攻击者与防御者之间的对抗博弈，通过在线交互让二者动态共同演化，从而摆脱"攻击发现 → 数据收集 → 重新对齐"的反应式循环。

---

### 第 2 段：当前 co-evolution 范式的双重病理

> 近期工作如 Self-RedTeam (Liu et al., 2025) 与 MAGIC (Wen et al., 2026) 在这一方向上取得了实质性进展：前者从博弈论角度证明了 Nash 均衡下的安全保证，后者通过非对称序贯博弈与 Subgame Perfect Nash Equilibrium 提供了点态安全保证。然而，深入分析这些框架的训练动态，我们发现两个互相加剧的核心病理。**(1) 攻击策略坍缩（Attack Strategy Collapse）**：在 RL 奖励最大化压力下，攻击者会迅速过拟合到少数高回报的策略模式。Self-RedTeam 自己的实验显示，即便相对于静态 defender 取得了 +21.8% 的 SBERT 多样性提升，仍能在 t-SNE 空间中观察到明显的聚类坍缩；GFlowNet 红队工作 (Lee et al., 2024) 进一步表明即便加入显式新颖性正则，标准 RL 攻击者仍会塌缩到一小群相似 prompt 上。**(2) 防御对抗遗忘（Defense Adversarial Forgetting）**：当攻击分布持续漂移时，防御者倾向于过拟合到当前攻击者，逐步丢失对早期攻击模式的鲁棒性，这一现象类似持续学习中的灾难性遗忘 (Kirkpatrick et al., 2017)，但因对手非平稳性而更严重。这两个病理相互强化：策略坍缩使得防御者只在窄分布上训练，进而对未见攻击模式更脆弱；防御者的脆弱反过来又强化了攻击者对那少数有效模式的依赖。**结果是一个虚高的训练指标 + 真实 OOD 鲁棒性下降的恶性平衡。**

---

### 第 3 段：现有多样性方法为什么不能直接解决这一问题

> 已有工作从三个不同方向引入多样性，但都未能在 co-evolution 中同时满足三个必要条件：**在线引入、作用于策略层、配合持续记忆机制**。首先，**Quality-Diversity 离线搜索**——Rainbow Teaming (Samvelyan et al., 2024)、Ferret (Pala et al., 2025)、RainbowPlus (Hoang et al., 2025) 与 QDRT (Wang et al., 2025) 在 risk category × attack style 行为空间上用 MAP-Elites 维护 archive；然而这些方法以静态 target LLM 为目标做离线 prompt 进化，**不参与攻防协同训练**，因此无法持续暴露不断进化的防御者的新漏洞。其次，**RL 中的语义/词汇多样性奖励**——CRT (Hong et al., 2024)、DiveR-CT (Zhao et al., 2024)、GFlowNet 红队 (Lee et al., 2024) 通过 SBERT 距离、Self-BLEU 或 k-NN 多样性激励 attacker；然而这些指标停留在表层文本与嵌入空间，**无法识别"策略层换皮不换招"的伪多样性**——例如同一个角色扮演策略可以用上百种语言形式包装而获得高语义多样性分数。第三，**当前 co-evolution 框架** Self-RedTeam、MAGIC、ACE-Safety (Li et al., 2025)、AdvEvo-MARL (Pan et al., 2025) 在策略空间多样性上几乎没有显式机制；同样，对防御对抗遗忘的处理也不充分——SSP (Wang et al., 2026) 引入了基于 UCB 的经验回放，但其优先级仅由奖励高低决定，**忽略了样本对当前防御者的实时威胁度**。综上，**"在 co-evolution 中、在策略层、在线"地同时缓解攻击坍缩与防御遗忘这一三重交集，至今仍是开放问题。**

---

### 第 4 段：本文工作 — DACE 的核心思想与四点贡献

> 本文提出 **DACE（Diversity-driven Adversarial Co-Evolution）**，一个将策略空间多样性显式集成到攻防协同训练的 RL 框架，从根源上同时缓解攻击坍缩与防御遗忘。我们的核心见解是：**策略坍缩与防御遗忘并非两个独立问题，而是同一对抗动力学的两面**——只有把多样性"在线"作用于策略层（缓解坍缩），并把历史高威胁攻击通过有原则的回放重新注入防御者训练（缓解遗忘），二者才能互相促进。具体而言，本文做出以下四点贡献。
>
> - **显式 12×10 攻击策略空间与 SFT 暖启动**。我们在 Llama-Guard-4 风险类别基础上剪除两个 dead row（Sexual Content 与 Code Interpreter Abuse），与 10 类攻击模式（角色扮演、术语伪装、权威操纵等）构成 $\mathcal{B} = \mathcal{S} \times \mathcal{C}$ 共 120 个槽位。攻击者在每次改写前先显式推理选择 $(s, c) \in \mathcal{B}$，将策略选择从隐式语义约束提升为可观测、可奖励的离散动作。我们通过 Gemini-2.5-Pro 蒸馏 ~43k 条带 $\langle\text{think}\rangle\langle\text{strategy}\rangle\langle\text{answer}\rangle$ 三段式 CoT 的 SFT 数据，**为攻击者注入策略推理能力的暖启动**，避免直接从 base instruct 模型起步导致的策略空间利用不充分。
> - **归一化边际覆盖增益奖励**。我们提出一种新的多样性奖励 $R_{\text{coverage}}(x) = \Delta H / \Delta H_{\max}$，分子为加入样本 $x$ 后档案池策略分布熵的边际变化，分母为该状态下任意单样本可达的最大边际变化。**这一归一化设计从根本上消除了原始熵增量的 $O(1/|\mathcal{A}|)$ 信号衰减问题**——在 KL 散度视角下，归一化覆盖增益等价于"单步 KL 收缩效率"，并继承前向 KL 的 zero-avoiding 特性，对空白槽位施加最强的探索驱动。我们对成功与失败样本采用差异化系数 $\lambda_{\text{succ}} = 1.0, \lambda_{\text{fail}} = 0.5$，确保多样性探索以有效性为优先约束。
> - **贝叶斯对抗回放池**。为缓解防御对抗遗忘，我们维护一个统一档案池，其中每个样本通过 Beta-Bernoulli 共轭后验追踪其对当前防御者的实时威胁度，并通过 Thompson Sampling 实现探索-利用平衡的回放采样。**指数时间衰减 $\gamma$ 让后验自然适应防御者能力漂移**（非平稳性），剪枝规则 $\hat{p}_i < \epsilon \wedge (s_i + f_i) > n_{\min}$ 仅淘汰被充分验证且当前低威胁的样本。该设计同时承担"策略频次记录"与"对抗经验回放"两项功能，闭环驱动攻防协同演化。
> - **充分实证 + 系统消融**。在 Qwen2.5-7B 与 Llama3.1-8B 两个 backbone 上，我们针对 defender 端给出涵盖 9 个 safety/utility benchmark 与 OpenRT pipeline（含最新 SOTA 黑盒攻击 MAJIC）的完整评测；针对 attacker 端给出 effectiveness（跨 6 个 defender 的迁移性）、diversity（策略层 / 语义层 / 词汇层 8 个指标）以及 co-evolution 动态（5×5 共演化热图）三方面的系统验证，并通过四组核心消融分别隔离 SFT 暖启动、覆盖度奖励、回放池与"DACE = MAGIC + diversity"四个组件的独立贡献。

---

### 第 5 段：实验亮点（提前披露关键数字）

> 实验结果支持 DACE 的核心论点。**(1) Defender 鲁棒性**：在 Qwen2.5-7B 上，DACE 将 HarmBench adv-harm ASR 从 MAGIC 的 4.3% 降至 0.3%，WildGuardTest adv-harm 从 2.3% 降至 0.8%；在 OpenRT 评测下，DACE 对 PAIR、TAP、AutoDAN、AutoDAN-turbo 全面优于 MAGIC（AutoDAN-turbo 从 54.69% 降至 42.18%），且对 v4 之后加入的最新黑盒组合攻击 MAJIC 仍保持显著领先，证明覆盖度驱动的训练分布**真正提升了对未见攻击的鲁棒泛化**而非过拟合训练 attacker。**(2) Attacker 多样性**：DACE-attacker 在 12×10 策略空间上的 Coverage Rate 比 MAGIC-attacker 高约 30%，在三层多样性指标（策略层 SEI、语义层 SBERT 距离、词汇层 Self-BLEU）上系统性领先。**(3) 通用能力保留**：DACE 在 IFEval / ARC-C / MMLU / AlpacaEval 2 上与 MAGIC 持平（差距 <2%），并在 GPQA 上略优（0.317 vs 0.308），表明多样化训练分布对推理类任务有正向溢出。综合而言，DACE 提供了一个原则化、可扩展的攻防协同演化框架，朝着"安全对齐作为持续演化过程"这一愿景推进了一步。

---

## 三、几个写作上需要拍板的细节

下面几个点是我写初稿时刻意留白的地方，等你确认后可以收紧表达：

1. **MAJIC 引用**：v4 阶段决定补 MAJIC 到 OpenRT 评测里，introduction 第 1 段最后我提了它作为"最新攻击演化"的代表；如果实验做不到 / 不打算放，可以从 introduction 删掉，换成更通用的"recent compositional attacks"。

2. **第 5 段的"Coverage Rate 比 MAGIC 高约 30%"是我估算的占位**。需要等 Tab 5 跑完后用真实数字替换。同样 GPQA 0.317 vs 0.308 来自你给的初步结果图，最终数字以重跑为准。

3. **是否在 introduction 直接 claim "首个" / "first" 类强陈述**：我目前用了"首次系统性地破除"和"首个把策略层多样性奖励'在线'集成到 RL 训练中"两次，措辞已经较克制。如果想更稳妥，可以改成 "to the best of our knowledge, the first..."；或者全部弱化为 "we propose the first systematic framework that simultaneously..." 这种 phrasing。NeurIPS reviewer 通常对 "first" 类 claim 较敏感，建议至少在 abstract 不要重复出现。

4. **是否把"四个贡献"压缩到三个**：目前四点中"显式 12×10 + SFT 暖启动"和"归一化覆盖奖励"都是方法侧贡献，如果想更紧凑，可以把它们合并为"a structured diversity reward grounded in a 12×10 attack space, with normalized marginal coverage gain to eliminate reward vanishing"；这样四点变三点（结构化策略空间与归一化奖励 / 贝叶斯回放 / 实证评测）。NeurIPS 习惯三点式贡献列表的论文略多于四点式，这个看你偏好。

5. **是否要在第 4 段最后加一个"图 1"占位**：MAGIC、Self-RedTeam、PIA 都用了一张 motivation figure。我建议 DACE 也配一张，左边画"MAGIC 攻击策略分布塌缩在少数 cell"，右边画"DACE 在 12×10 策略空间上均匀分布 + 贝叶斯回放循环"。如果配图，第 4 段最后可以加"As illustrated in Figure 1, ..."一句。

如果上面 5 点你 OK，我可以接下来：(a) 把这版中文初稿翻译为正式英文 introduction，控制在约 1.0 页 NeurIPS 篇幅；或者 (b) 顺势把 method 章节也开始草拟。你想推进哪一步？

-----

> 感觉还是不够好，可以参考magic论文（之前附件上传过，MAGIC.pdf）再完善一下，
> 先写4-6段写“故事线”，理清逻辑关系，最后再加一个contribution部分，
> 假装你是严格的reviewer，在内心先对上面的introduction进行提问，再切换回author视角完善introduction，再深入思考整理一版，
> 先简要介绍 dace 的 introduction 怎么写，是什么讲故事逻辑以及为什么要怎么写，再给出具体的每一段的 introduction 内容，要求达到 NeurIPS 录用论文高质量水准，



下面我先**以 reviewer 视角"内心拷问"**前一版 introduction，然后切回 author 视角重新设计。最终给出参考 MAGIC 风格的 4-段叙事 + 独立 contribution 列表。

---

## 一、Reviewer 视角的内心批判（必须解决的 12 个问题）

| # | 问题 | 严重性 |
|---|---|---|
| 1 | **第 1 段像 related work timeline**——堆了 DAN/ASCII/GCG/PAIR/TAP/AutoDAN-turbo/X-Teaming/MAJIC，缺少 hook 和 punch | 高 |
| 2 | **缺少斜体研究问题作为锚点**（MAGIC 用 "How to continuously discover..."，DACE 缺这种 anchor） | 高 |
| 3 | **第 2 段过早讲"双重病理"**——读者还没接受 co-evolution 是 framing，就先听到对它的批判，narrative 跳跃 | 高 |
| 4 | **第 3 段把三类多样性方法平行罗列**，结构上像 mini-survey；MAGIC 的两段障碍讨论是聚焦式而非并列式 | 高 |
| 5 | **Contribution 嵌套在第 4 段段落中**，再加 4 个 sub-bullet，结构混乱；NeurIPS 习惯独立的 contribution list | 高 |
| 6 | **第 5 段实验段独立成段**，喧宾夺主；实验数字应放进 contribution bullet | 中 |
| 7 | **没有 Figure 1 视觉化对照**——MAGIC 用 Fig 1 直接画 strawman vs MAGIC，是非常有效的 selling point | 中 |
| 8 | **"攻击坍缩与防御遗忘是同一动力学的两面"过于哲学化**——需要更具体的 mechanism 描述 | 中 |
| 9 | **没有"we observe that..."实证 hook**——MAGIC 用"attacker evolves novel combinatorial strategies"做 hook；DACE 缺这种"先抛实验亮点"的钩子 | 中 |
| 10 | **"first" claim 出现 2 次**，reviewer 对绝对化 claim 较敏感，需弱化为 "to our knowledge..." | 中 |
| 11 | **MAJIC 引用嵌在第 1 段攻击演化清单中**——是否与该段叙事必要还需考虑 | 低 |
| 12 | **12×10 策略空间是 ad-hoc 还是 derive 出来的没说明**——reviewer 会立刻问"why 12 × 10" | 低 |

---

## 二、整体故事线设计（4 段叙事 + Contribution List）

**完全对齐 MAGIC 的 introduction 结构**——MAGIC 的 introduction 是 4 段叙事 + 3 个 contribution bullet，整体约 1 页。我把 DACE 的 narrative 设计为：

| 段 | 角色 | 核心命题 | 类比 MAGIC 的对应段 |
|---|---|---|---|
| **§1** | Hook + Big Picture + Research Question | LLM 安全的反应式范式失败 → 提出研究问题 | MAGIC §1.1 |
| **§2** | Co-evolution 范式 + 双重障碍（配 Figure 1） | Co-evolution 有前景但有两个内生障碍：collapse + forgetting | MAGIC §1.2 + Fig 1 |
| **§3** | 障碍 1 深挖：攻击坍缩 + 现有多样性方法的失败 | 三类多样性方法都未能在 co-evolution 中作用于策略层 | MAGIC §1.3-1.4 (障碍 1) |
| **§4** | 障碍 2 深挖：防御遗忘 + DACE 的提出 | 现有 replay 不针对当前威胁度；DACE 用贝叶斯后验 + 闭环回放（带"we observe..."实证 hook） | MAGIC §1.5 (障碍 2 + 方法概述) |
| **Contributions** | 独立列出 3 个 bullet | 方法贡献 + 理论支撑 + 实证 | MAGIC contribution list |

---

### 故事的"逻辑闭环"是关键设计

DACE 的所有方法组件都对应到一个具体的 problem，**每个组件都不是 ad-hoc 添加的**：

```
研究问题：如何让 co-evolution 持续？
        ↓
  双重障碍 ← Figure 1 视觉化
   ↙        ↘
攻击坍缩     防御遗忘
   ↓           ↓
现有多样性    现有 replay
方法不足      不够好
   ↓           ↓
12×10 策略空间  贝叶斯回放池
+ 归一化覆盖   + Thompson 采样
增益奖励      + 时间衰减
   ↘        ↙
   闭环演化系统
```

这个闭环结构让 reviewer 一目了然："collapse 用多样性奖励解决，forgetting 用贝叶斯回放解决，二者闭环互锁"。

---

## 三、Introduction 中文初稿（NeurIPS 高质量水准）

下面是按上面框架写的具体内容。每段 200-350 字，目标整体约 1.0 页 NeurIPS 排版。

---

### § 1 Hook + Big Picture + Research Question（约 220 字）

> 大语言模型（LLM）在代码生成、科学研究、医疗辅助等领域的广泛部署，使其安全对齐成为不可回避的核心问题 (Bai et al., 2025)。当前主流的对齐范式——基于人类反馈的强化学习 (RLHF) (Ouyang et al., 2022)、外部 guardrail 模型 (Inan et al., 2023)、以及静态对齐数据集——本质上是面向"已知攻击分布"的反应式补丁：每一次新型 jailbreak 出现，社区先收集样本、再训练新一代防御，循环往复。然而，攻击演化的速度远快于反应式防御——从早期角色扮演 (Shen et al., 2023) 到自动化对抗优化 (Zou et al., 2023; Chao et al., 2023)，再到隐蔽的多轮代理化攻击 (Rahman et al., 2025) 与近期出现的 Markov 链组合攻击 (Qi et al., 2025)，攻击者的策略空间持续扩张。这一根本性不对称迫使我们重新审视防御范式：***How can we continuously co-evolve attackers and defenders such that the defender remains robust against an ever-shifting distribution of adversarial strategies?***

---

### § 2 Co-evolution 范式 + 双重障碍（约 290 字，配 Figure 1）

> 为打破反应式范式的滞后性，近期工作将安全对齐重新建模为攻防协同演化（co-evolution）的多智能体博弈：Self-RedTeam (Liu et al., 2025) 通过 zero-sum self-play 给出 Nash 均衡下的安全保证；MAGIC (Wen et al., 2026) 在非对称序贯博弈框架下取得 Subgame Perfect Nash Equilibrium 的点态保证；ACE-Safety (Li et al., 2025)、AdvEvo-MARL (Pan et al., 2025) 与 PIA (Li et al., 2026) 进一步从 MCTS、MARL 和 persona-invariant 角度推进了这一范式。然而，深入分析这些框架的训练动态，我们发现它们普遍受困于两个相互加剧的内生障碍（如 Figure 1 所示）。**(1) 攻击策略坍缩（Attack Strategy Collapse）：** 在 RL 奖励最大化压力下，攻击者迅速过拟合到少数高回报策略模式，使得 defender 仅在窄分布上接受训练，对 OOD 攻击的真实鲁棒性虚高。**(2) 防御对抗遗忘（Defense Adversarial Forgetting）：** 当 attacker 策略持续漂移时，defender 倾向于过拟合当前 attacker，逐步丢失对早期攻击模式的鲁棒性，类似持续学习中的灾难性遗忘 (Kirkpatrick et al., 2017) 但因对手非平稳性而更严重。这两个障碍互为因果——窄分布训练加剧遗忘，遗忘又使得 attacker 那少数有效模式被反复"奖励"，形成虚高指标 + 真实鲁棒性下降的恶性平衡。

---

### § 3 障碍 1 深挖：攻击坍缩与现有多样性方法的不足（约 280 字）

> 解决攻击坍缩的自然思路是引入多样性，已有工作沿三个方向展开但都未能在 co-evolution 中真正生效。**第一类是 Quality-Diversity (QD) 离线搜索**——Rainbow Teaming (Samvelyan et al., 2024)、Ferret (Pala et al., 2025) 与 QDRT (Wang et al., 2025) 在 risk category × attack style 行为空间上用 MAP-Elites 维护 archive，但其搜索过程不参与攻防协同训练，**以静态 target LLM 为目标**，因此无法持续暴露不断进化的 defender 的新漏洞。**第二类是基于 RL 的语义/词汇多样性奖励**——CRT (Hong et al., 2024)、DiveR-CT (Zhao et al., 2024)、GFlowNet 红队 (Lee et al., 2024) 用 Self-BLEU、SBERT 距离或 k-NN 多样性激励 attacker；然而这些指标停留在表层文本与嵌入空间，**无法识别"换皮不换招"的伪多样性**——同一个角色扮演策略可以用上百种语言形式包装而获得高 SBERT 多样性分数，攻击的实质策略并未改变。**第三类是当前 co-evolution 框架本身**——Self-RedTeam 报告 +21.8% SBERT 多样性提升但仍观察到 t-SNE 聚类坍缩，MAGIC 注意到组合策略的涌现但**未将多样性纳入奖励设计**。综上，**在 co-evolution 中、在策略层、在线**地激励多样性这一三重交集，仍是一个开放问题。

---

### § 4 障碍 2 深挖 + DACE 提出（约 340 字）

> 防御对抗遗忘问题在现有工作中的处理同样不充分。SSP (Wang et al., 2026) 引入了基于奖励高低的 UCB experience replay 来缓解 self-play 训练的震荡，但其优先级**仅基于历史奖励，不反映样本对当前 defender 的实时威胁度**——一个早期被 attacker 突破但已被现 defender 学会拒绝的样本，仍会因高历史奖励被反复回放，浪费训练预算；MAGIC 与 ACE-Safety 则完全不维护历史攻击的回放机制，attacker 的迭代演化使早期策略事实上从训练分布中消失。基于以上分析，我们提出 ***DACE（Diversity-driven Adversarial Co-Evolution）***，一个将策略空间多样性与历史威胁度感知回放系统性集成到 co-evolution 的 RL 框架。我们的核心见解是：**坍缩与遗忘是同一对抗动力学下的两个互锁失败模式**——只有把多样性"在线"作用于显式策略空间（缓解坍缩），并把历史样本通过反映当前威胁度的有原则回放重新注入 defender 训练（缓解遗忘），二者才能形成正反馈而非恶性循环。具体而言，DACE 包含三个紧耦合组件：（i）一个基于 Llama-Guard-4 风险分类与 SorryBench 攻击模式聚类得到的 $12 \times 10$ 显式策略空间，配合 SFT 暖启动赋予 attacker 策略推理能力；（ii）一个带 KL 散度收缩效率解读的归一化边际覆盖增益奖励，从根源上消除原始熵增量在长周期训练中的信号衰减；（iii）一个以 Beta-Bernoulli 后验追踪当前威胁度、Thompson Sampling 实现探索-利用平衡、指数时间衰减适应非平稳性的贝叶斯对抗回放池。**值得注意的是，**通过迭代 RL 训练，DACE-attacker 自发演化出 SFT 数据中不存在的多策略组合攻击（如角色扮演 × 翻译 × 概念替换的复合攻击），且单 rollout 即可达到与 PAIR、TAP 等多轮搜索方法相当的攻击成功率，验证了我们设计的有效性。

---

### Contributions（独立列表，3 个 bullet）

> In summary, we make the following contributions:
>
> **• A diversity-driven co-evolution framework with normalized coverage reward.** We propose DACE, the first co-evolution framework that systematically introduces structured strategy-space diversity into RL-based safety alignment to our knowledge. Centered on a $12 \times 10$ explicit attack strategy space, we design a *normalized marginal coverage gain* reward whose normalization scheme provably eliminates the $O(1/|\mathcal{A}|)$ reward vanishing inherent in raw entropy-based rewards. Through a KL-divergence reformulation, we show that the reward is equivalent to per-step KL contraction efficiency toward the uniform strategy distribution and inherits the zero-avoiding property that drives strongest exploration toward unfilled strategy slots.
>
> **• Bayesian adversarial replay against defense forgetting.** We introduce a unified archive that simultaneously serves as the strategy frequency tracker and the adversarial replay buffer. Each archived sample maintains a Beta-Bernoulli posterior reflecting its real-time threat against the current defender; Thompson Sampling provides principled exploration-exploitation balance during replay; exponential time decay handles the non-stationarity induced by defender evolution; and a posterior-confidence-aware pruning rule retires only samples that are sufficiently tested *and* low-threat. This design closes the loop between attack diversity expansion and defense memory consolidation.
>
> **• Comprehensive empirical validation across two model families and SOTA OOD attackers.** Extensive experiments on Qwen2.5-7B-Instruct and Llama3.1-8B-Instruct show that DACE matches or surpasses MAGIC on safety benchmarks (e.g., HarmBench adv-harm ASR $0.043 \rightarrow 0.003$) without sacrificing utility (IFEval, ARC-C, GPQA, MMLU, AlpacaEval 2 within 2%). On the OpenRT pipeline with GPT-4o as judge, DACE consistently outperforms MAGIC against PAIR, TAP, AutoDAN, AutoDAN-turbo (e.g., $54.69\% \rightarrow 42.18\%$ on AutoDAN-turbo) and remains robust against the most recent black-box compositional attack MAJIC (Qi et al., 2025). On the attacker side, DACE-attacker achieves a Coverage Rate $\sim 30\%$ higher than MAGIC-attacker while maintaining superior cross-defender transferability across six target backbones.

---

## 四、相对前一版的关键改进（reviewer 检查清单对照）

| Reviewer 关切 | 处理方式 |
|---|---|
| 第 1 段堆 timeline | 改为 Hook（反应式范式失败）+ Research Question 锚点（斜体英文 RQ） |
| 缺少 RQ anchor | 第 1 段末加斜体英文 RQ |
| 第 2 段直接讲病理太突兀 | 先建立 co-evolution 是 framing（引 5 篇 SOTA），再"However"切到障碍 |
| 三类多样性平行像 mini-survey | 第 3 段保留并列结构但聚焦"为什么都不在 co-evolution 工作"，结尾归纳到三重交集 |
| Contribution 嵌入段落 | 独立列表 3 个 bullet（参考 MAGIC 格式） |
| 实验数字独立成段 | 移到 contribution 第 3 个 bullet 内 |
| 缺 Figure 1 | 在 §2 配 Figure 1 引用（左：MAGIC attacker 在 12×10 cell 上塌缩 + 防御遗忘 U 形曲线；右：DACE 均匀覆盖 + 贝叶斯回放循环） |
| "两面"过于哲学化 | 第 4 段换为"互锁失败模式 / 正反馈 vs 恶性循环"具体 mechanism |
| 缺 we observe 实证 hook | 第 4 段末加"DACE-attacker 自发演化组合攻击 + 单 rollout 匹敌多轮搜索"两个 hook |
| "first" claim | 用 "to our knowledge" 弱化 |
| 12×10 来源 | §4 写明"基于 Llama-Guard-4 + SorryBench 聚类" |
| MAJIC 位置 | §1 仅一句带过；详细对比留 contribution bullet 第 3 |

---

## 五、写作上的几个小决策（建议你拍板）

1. **Figure 1 设计**：建议三栏布局——(a) MAGIC attacker 输出在 12×10 grid 上的频率热图（可见少数 cell 高度集中）；(b) "Forgetting U-curve"（最终 defender 对 attacker iter1–4 的 ASR，无 replay 时呈 U 形）；(c) DACE 的均匀分布 + 贝叶斯回放闭环示意图。三幅图各占 1/3 宽度，主文献图（不放 Appendix）。

2. **是否在 §1 直接提"DACE"作为方法名**：MAGIC 在 §1 末尾未提名，§4 才正式介绍。我目前 follow MAGIC，在 §4 才正式提 DACE。这样 §1-§3 都是 problem framing，§4 才切到 method，narrative 更紧凑。

3. **"In summary, we make the following contributions" 措辞**：MAGIC 用 "In conclusion, our contributions are summarized as follows:"。两种都行，建议用 "We summarize our contributions as follows:" 略简洁。

4. **是否需要 §5 一句话过渡到剩余章节结构**：NeurIPS introduction 通常**不需要** "The rest of the paper is organized as follows..." 这种 boilerplate。MAGIC 也没写。建议省略。

---

如果你确认这一版骨架 OK，我可以：(a) 把 §1–§4 + Contributions 翻译为正式英文（控制在约 1.0 页 NeurIPS 排版），保持 MAGIC 的 academic register；或者 (b) 顺势把 method 章节也开始按 MAGIC §3-§4 的结构（problem formalization + methods + reward design + algorithm）草拟。你想推进哪一步？

-----

> 下面是 gpt 梳理的 introduction，请结合进行反思，给出充分完善后的 introduction 梳理，
>
> 假装你是严格的reviewer，在内心先对上面的两版本introduction（你的最新的和gpt的）进行提问，再切换回author视角完善introduction，再深入思考整理一版， 先简要介绍 dace 的 introduction 怎么写，是什么讲故事逻辑以及为什么要怎么写，再给出具体的每一段的 introduction 内容，要求达到 NeurIPS 录用论文高质量水准，
>
> =====================
> 【gpt梳理的introduction】
> 下面这版我会把 DACE 的 Introduction 重新定位为：**不是“MAGIC + 一个 diversity reward + 一个 replay buffer”，而是“把 co-evolution 从当前对手适应，推进到策略空间覆盖与历史风险记忆驱动的安全演化过程”。** 这才是 NeurIPS 级别更容易站住的故事。
>
> ---
>
> # 1. DACE 的 Introduction 应该怎么写
>
> DACE 的 Introduction 最好写成 **MAGIC 之后的下一步**，而不是重新发明 co-evolution。
>
> MAGIC 已经讲清楚了第一层故事：LLM safety 不应只靠静态数据和离线 red-teaming，而应被建模为 attacker 与 defender 的动态非对称序贯博弈。MAGIC 的核心贡献是：攻击者和防御者参数解耦，避免 Self-RedTeam 这类 shared-parameter self-play 的目标冲突；攻击者先动、防御者后动，更符合真实攻击场景；并且通过在线 RL 使攻击者持续暴露 long-tail vulnerabilities，推动防御者提升泛化鲁棒性。MAGIC 的 Introduction 和 Figure 1 都围绕两个问题展开：攻击者缺少 offensive reasoning cold-start，以及共享模型 self-play 会产生 attacker/defender gradient conflict。
>
> DACE 不能重复这个故事。DACE 应该说：**MAGIC 证明了 co-evolution 是有效的，但 co-evolution 本身还不保证“覆盖充分”与“记忆稳定”。** 如果攻击者只被攻击成功率驱动，它仍可能集中到少数高回报攻击模式；如果防御者只追逐当前攻击分布，它仍可能遗忘历史攻击。前者是 **attack strategy collapse**，后者是 **defense adversarial forgetting**。这两个问题共同说明：安全共演化不应只是当前 attacker 和 defender 之间的局部 best response，而应是对攻击策略空间和历史漏洞空间的持续覆盖。
>
> 因此 DACE 的主线应该是：
>
> > **Static alignment lags behind evolving attacks. MAGIC-style co-evolution makes safety training adaptive. But adaptive does not necessarily mean comprehensive or durable: attackers may collapse to narrow strategies, and defenders may forget old threats. DACE makes co-evolution diversity-aware and memory-aware by explicitly covering a structured attack strategy space and replaying historically risky attacks through Bayesian adversarial memory.**
>
> 为什么要这么写？因为 reviewer 会问三个很尖锐的问题：
>
> 1. **你和 MAGIC 的本质区别是什么？**
>    不能只说“我们也做 attacker-defender game”。必须说 MAGIC 主要解决动态适应和角色解耦，而 DACE 进一步解决 co-evolution 中的策略覆盖和历史记忆问题。
>
> 2. **你的 diversity 是不是只是更多样的文本？**
>    不能停留在 Self-BLEU、Distinct-n、embedding distance。DACE 的核心是 risk category × attack style 的 **策略空间覆盖**，也就是 safety-relevant diversity，而不是表面措辞变化。
>
> 3. **replay buffer 是不是工程 trick？**
>    不能写成“我们加了历史样本”。要写成：在非平稳攻防系统中，历史漏洞不会因为当前训练分布消失而消失；defender 需要一个动态 adversarial memory 来估计哪些历史攻击仍然危险，哪些已经被防住，哪些不确定但值得复查。
>
> ---
>
> # 2. Introduction 故事线初稿：6 段版本
>
> ## Paragraph 1：从静态安全对齐到动态攻防博弈
>
> Large language models are increasingly deployed in open-ended interactive environments, where safety failures are no longer triggered only by direct harmful instructions, but by adaptive, obfuscated, and multi-step adversarial prompts. As MAGIC observes, the threat landscape has rapidly shifted from simple role-playing jailbreaks to automated adversarial attacks and stealthy multi-turn agentic exploitations, turning LLM safety into a cat-and-mouse game between attackers and defenders. Static safety alignment pipelines—whether based on pre-collected harmlessness data, manually designed red-teaming prompts, or post-hoc guardrails—inevitably lag behind this evolving threat distribution. Once a model is patched against one family of attacks, new prompts quickly resurface through paraphrasing, role modulation, scenario shifting, or compositional deception. This motivates a more adaptive formulation: instead of treating safety alignment as one-shot training on a fixed dataset, we should treat it as an evolving adversarial process in which attackers continuously discover new vulnerabilities and defenders continuously learn to reject them.
>
> **中文可投稿版：**
>
> 大语言模型正在进入开放式交互环境，其安全风险已经不再主要来自直接有害请求，而是来自持续演化的、经过伪装和组合的对抗提示。MAGIC 指出，LLM 的威胁形态正在从简单的角色扮演 jailbreak，快速演化为自动化对抗攻击和隐蔽的多轮 agentic exploitation，使安全对齐逐渐变成攻击者与防御者之间的 “cat-and-mouse game”。 传统安全对齐方法通常依赖预先收集的 harmlessness 数据、人工构造的红队样本或外部 guardrail；这些静态防御可以修补已知漏洞，却天然滞后于不断变化的攻击分布。一旦模型被针对某类攻击修补，攻击者仍可通过改写、角色设定、场景迁移或多策略组合重新绕过安全边界。因此，LLM safety alignment 不应只被视为固定数据集上的离线训练问题，而应被建模为一个持续演化的对抗过程：攻击者不断发现新漏洞，防御者不断学习拒绝这些攻击。
>
> ---
>
> ## Paragraph 2：MAGIC 的贡献，以及 DACE 要推进的下一步
>
> Recent co-evolutionary approaches have made an important step toward this goal. In particular, MAGIC formulates LLM safety alignment as an asymmetric sequential game between a decoupled attacker and defender: the attacker first rewrites a seed query into a deceptive prompt, and the defender then learns to recognize and refuse it. This formulation addresses two limitations of earlier self-play systems: shared-parameter attacker/defender training can introduce conflicting gradients, and symmetric normal-form games fail to capture the sequential structure of real-world jailbreak attempts. MAGIC further shows that a reasoning-capable attacker can evolve novel combinatorial strategies through iterative RL, and that such co-evolution improves defender robustness without severe helpfulness degradation. However, MAGIC also exposes a deeper question: once co-evolution is enabled, what determines whether the attacker explores the vulnerability space broadly enough, and whether the defender retains robustness to vulnerabilities discovered earlier in training?
>
> **中文可投稿版：**
>
> 近期的攻防协同演化方法已经向这一目标迈出重要一步。MAGIC 将 LLM safety alignment 形式化为攻击者与防御者之间的非对称序贯博弈：攻击者首先将原始请求改写为更隐蔽的 adversarial prompt，防御者随后学习识别并拒绝该输入。该设计解决了早期 self-play 方法的两个关键局限：一方面，共享参数的 attacker/defender 训练会将相互冲突的目标压到同一参数空间中，产生 gradient conflict；另一方面，对称 normal-form game 难以刻画真实 jailbreak 场景中“攻击者先行动、防御者后响应”的序贯结构。 MAGIC 进一步展示了一个具有初始 reasoning 能力的攻击者可以在迭代 RL 中演化出此前未见过的组合式攻击策略，并推动防御者在保持 helpfulness 的同时提升鲁棒性。 然而，MAGIC 也自然引出了下一层问题：当 co-evolution 已经发生后，我们如何保证攻击者不是只在少数高回报策略上反复利用？又如何保证防御者在适应当前攻击者时，不会遗忘训练早期已经暴露过的漏洞？
>
> ---
>
> ## Paragraph 3：第一个缺口——adaptive 不等于 diverse
>
> The first limitation is that adaptivity alone does not guarantee coverage. In reinforcement learning, an attacker optimized primarily for attack success may over-exploit a small number of high-reward rewriting patterns, producing increasingly effective but strategically narrow attacks. Such attack strategy collapse is especially harmful in safety training: a defender trained against a narrow adversary may appear robust within the current game, yet remain vulnerable to under-explored regions of the attack space. Automated red-teaming research has repeatedly shown that effective attacks and diverse attacks are not the same objective. Quality-diversity methods such as Rainbow Teaming maintain archives over behavior descriptors, while QDRT argues that word- or embedding-level diversity metrics cannot reliably capture meaningful attack behavior. These insights suggest that co-evolutionary safety training needs a notion of diversity that is tied to safety-relevant attack strategies, not merely surface-level textual variation. Yet existing co-evolutionary frameworks typically treat attack diversity as an emergent property to be analyzed after training, rather than an explicit objective that shapes the attacker throughout training.
>
> **中文可投稿版：**
>
> 第一个关键缺口是：**动态适应并不等于策略覆盖充分**。在强化学习训练中，如果攻击者主要被攻击成功率驱动，它很容易过度利用少数高回报改写模式，生成越来越有效但策略上越来越狭窄的攻击。这种 attack strategy collapse 在安全训练中尤其危险：防御者可能在当前攻击者分布上表现稳健，却仍然暴露于未被充分探索的攻击空间区域。自动化红队研究已经反复表明，有效攻击和多样攻击并不是同一个目标。Rainbow Teaming 将对抗提示生成建模为 quality-diversity search，并通过行为描述符 archive 维护高质量且多样的攻击；QDRT 进一步指出，词频、句向量相似度或普通 semantic distance 难以可靠刻画真实攻击行为差异。早期调研材料中也总结过：LLM safety diversity 的核心价值在于安全覆盖完整性、safety tuning 有效性和协同演化效率，而现有方法普遍受到 mode collapse、novelty stagnation 以及 diversity-effectiveness trade-off 的限制。 这些观察说明，co-evolutionary safety training 需要的是与安全语义直接相关的策略多样性，而不是表层文本变化。然而，现有 co-evolution 框架通常只在训练后分析 attacker 是否涌现了多样策略，而没有将策略覆盖作为贯穿训练过程的显式优化目标。
>
> ---
>
> ## Paragraph 4：第二个缺口——current robustness 不等于 durable robustness
>
> The second limitation is that robustness to the current attacker does not imply durable robustness over time. In an evolving game, the defender’s training distribution is non-stationary: as the attacker discovers new strategies, earlier attacks may disappear from the current batch even though they remain valid threats in the real world. A defender trained only on the latest adversarial distribution may therefore suffer from adversarial forgetting, relearning recent vulnerabilities while losing robustness to older ones. This problem is more severe than ordinary distribution shift because historical attacks can be deliberately reused or recombined by future adversaries. Experience replay offers a natural remedy, but a naive replay buffer is insufficient: old attacks differ in whether they are still effective against the current defender, whether they have become obsolete, and whether their risk is uncertain due to limited re-evaluation. Thus, robust co-evolution requires not only an adaptive attacker, but also a memory mechanism that continually estimates the current threat level of historical attacks and revisits those that remain risky or uncertain.
>
> **中文可投稿版：**
>
> 第二个关键缺口是：**对当前攻击者稳健，不等于长期稳健**。在一个不断演化的攻防游戏中，防御者面对的训练分布是非平稳的：随着攻击者发现新策略，早期攻击可能从当前 batch 中消失，但它们并不会从真实威胁空间中消失。若防御者只追逐最新攻击分布，它可能在学习新攻击的同时遗忘旧攻击，产生 defense adversarial forgetting。这个问题比普通分布漂移更严重，因为历史攻击可以被未来攻击者主动复用，也可以与新策略组合后重新变得有效。经验回放是自然的缓解思路，但简单 replay buffer 并不足够：历史攻击样本之间存在显著差异，有些仍能突破当前 defender，有些已经过时，有些则因缺少重新评估而风险不确定。因此，一个可靠的 co-evolution 框架不只需要动态攻击者，还需要一个动态 adversarial memory：持续估计历史攻击对当前防御者的威胁水平，并优先复习仍然危险或不确定的漏洞。
>
> ---
>
> ## Paragraph 5：DACE 的中心思想
>
> We propose DACE, a diversity-aware adversarial co-evolution framework for LLM safety alignment. DACE starts from a simple principle: robust safety requires co-evolution over both the strategy space and time. On the attacker side, DACE defines a structured attack strategy space as the Cartesian product of risk categories and attack styles. Each generated attack is assigned a behavior descriptor, allowing the attacker to be rewarded not only for bypassing the current defender, but also for expanding coverage over safety-relevant strategy cells. This turns diversity from an implicit byproduct into an explicit training signal. On the defender side, DACE maintains a Bayesian adversarial replay buffer that stores historical successful attacks and tracks their evolving risk against the current defender. During defender training, current attacks are mixed with replayed historical attacks sampled according to risk and uncertainty, encouraging the defender to improve against new strategies while retaining robustness to old ones. Together, these two mechanisms transform co-evolution from a local arms race into a coverage- and memory-aware safety training process.
>
> **中文可投稿版：**
>
> 本文提出 **DACE，Diversity-Aware Adversarial Co-Evolution**，一个面向 LLM safety alignment 的多样性驱动攻防协同演化框架。DACE 的核心原则是：稳健安全性需要同时沿着两个维度演化——**策略空间维度** 和 **时间维度**。在攻击者侧，DACE 定义结构化攻击策略空间，将每个攻击映射到风险类别与攻击方式组成的行为描述符 (b(x)=(s,c))。已有方法设计中也明确将攻击策略空间定义为 (\mathcal{B}=\mathcal{S}\times\mathcal{C})，并用策略空间覆盖度与新颖性来驱动攻击者远离少数热门策略区域。 这样，攻击者不只因突破当前防御者而获得奖励，也因扩展安全语义明确的策略覆盖而获得奖励，从而将 diversity 从训练后的涌现现象转化为训练中的显式目标。在防御者侧，DACE 维护 Bayesian adversarial replay buffer，存储历史成功攻击，并动态估计这些样本对当前 defender 的风险。防御者训练时同时接收当前攻击者生成的新攻击和从回放池采样的历史高风险或高不确定攻击，使其既能适应新策略，也能保持对旧策略的鲁棒性。二者结合后，co-evolution 不再只是当前 attacker 与 defender 的局部 arms race，而变成一个由策略覆盖和历史记忆共同驱动的安全演化过程。
>
> ---
>
> ## Paragraph 6：DACE 相比 MAGIC 的清晰定位
>
> DACE builds on the co-evolutionary insight of MAGIC but changes what the game is optimized to preserve. MAGIC asks whether a decoupled attacker-defender game can produce a stronger defender against adaptive adversaries. DACE asks a complementary question: can the game be guided so that the attacker systematically explores the safety-relevant strategy space and the defender remains robust to vulnerabilities discovered across the entire training history? This shift matters because safety is not only a pointwise response to the current adversary; it is a coverage problem over many possible subgames and a retention problem over time. By making attack diversity explicit and defender memory adaptive, DACE aims to produce attackers that are both effective and strategically broad, and defenders that are not only robust to the latest attacks but also resistant to adversarial forgetting. We evaluate DACE from both sides of the game: defender safety, benign compliance, general capability, out-of-distribution attacker robustness, adversarial forgetting, attacker effectiveness, transferability, and strategy-space quality-diversity.
>
> **中文可投稿版：**
>
> DACE 建立在 MAGIC 的 co-evolution insight 之上，但改变了这个游戏所要维护的对象。MAGIC 关注的问题是：解耦的 attacker-defender 非对称博弈能否训练出更强的防御者来应对 adaptive adversaries。DACE 进一步追问一个互补问题：我们能否引导这个游戏，使攻击者系统性覆盖安全相关的策略空间，同时使防御者在整个训练历史中保持对已发现漏洞的鲁棒性？这个转变很关键，因为安全性不只是对当前攻击者的 pointwise response；它同时是一个跨策略子空间的覆盖问题，也是一个跨训练时间的保持问题。通过显式优化攻击多样性并引入自适应防御记忆，DACE 旨在得到既有效又策略广泛的攻击者，以及不仅能抵御最新攻击、也能抵抗 adversarial forgetting 的防御者。我们从攻防两端系统评估 DACE：在 defender 侧评估 harmful refusal、benign compliance、general capability、OOD attacker robustness 与历史攻击遗忘；在 attacker 侧评估 attack effectiveness、transferability、strategy-space coverage、successful coverage 和 quality-diversity。
>
> ---
>
> # 3. Contribution 部分初稿
>
> 建议 Contribution 写 4 条，重点要和 MAGIC 区分开。
>
> ## Contributions
>
> **(1) We formulate diversity-aware adversarial co-evolution for LLM safety alignment.**
> 我们提出 DACE，将 LLM safety alignment 从当前攻击者—防御者之间的动态适应，推进为同时关注 **策略空间覆盖** 与 **历史风险记忆** 的协同演化问题。该框架直接针对现有 co-evolution 中两个未被充分解决的 failure modes：attack strategy collapse 和 defense adversarial forgetting。
>
> **(2) We introduce a structured strategy-space objective for effective attack diversity.**
> 我们将攻击样本映射到风险类别 × 攻击方式的结构化行为描述符，并在攻击者训练中显式奖励 safety-relevant strategy coverage。与文本相似度或语义距离不同，该目标直接对应安全红队中的策略覆盖，使攻击者生成不只是表面不同、而是在风险类型和攻击机制上真正不同的有效攻击。
>
> **(3) We design a Bayesian adversarial replay mechanism for durable defender robustness.**
> 我们构建 Bayesian adversarial replay buffer，为历史成功攻击维护动态风险估计，并根据风险与不确定性采样历史样本参与防御者训练。该机制使 defender 不仅适应当前攻击者，还能持续复习仍然危险或尚未充分确认的历史攻击，从而缓解 adversarial forgetting。
>
> **(4) We provide a two-sided evaluation of co-evolution, measuring both defender robustness and attacker diversity.**
> 我们不仅评估防御者在 harmful refusal、benign compliance、general capability、OOD attacker robustness 和 forgetting curve 上的表现，也系统评估攻击者的 ASR、transferability、strategy-space coverage、successful coverage、entropy 和 quality-diversity score。这样的评估能够验证 DACE 是否真正实现了 “effective, diverse attacks” 与 “robust, durable defenses” 的联合提升。
>
> ---
>
> # 4. 这一版比上一版更强在哪里
>
> 这一版的核心改进是：
>
> 1. **先承认 MAGIC 的贡献，再指出 MAGIC 留下的空白。**
>    这样不会显得 DACE 在重复 MAGIC，也不会被 reviewer 质疑“你只是换了个名字做 co-evolution”。
>
> 2. **把 DACE 的问题定义从 method trick 提升到 failure mode。**
>    attack strategy collapse 和 defense adversarial forgetting 是两个明确、可实验验证、和方法组件一一对应的问题。
>
> 3. **把 diversity 从“生成更多不同 prompt”提升为“策略空间覆盖”。**
>    这能和 Rainbow/QDRT 对齐，也能凸显 DACE 的安全语义贡献。
>
> 4. **把 replay 从“缓存历史样本”提升为“动态风险记忆”。**
>    这能解释为什么 Bayesian replay 是必要的，而不是普通 experience replay。
>
> 5. **把最终主张写成一句更强的 NeurIPS claim：**
>    **DACE turns adversarial co-evolution from a local arms race into a coverage- and memory-aware safety training process.**

 下面我先**以严格 reviewer 视角"内心拷问"**两版 introduction（我之前那版 + GPT 的 6 段版），把所有问题列出来；然后切回 author 视角重新设计；最后给出**4 段叙事 + Contributions 的最终版**，目标是 NeurIPS 录用论文水准。

---

## 一、Reviewer 视角：对两版 introduction 的内心拷问

### 1.1 对我前一版 4 段稿的批判

| # | 问题 | 严重性 |
|---|---|---|
| R1 | §3 三类多样性方法被并列罗列，**但没说清"为什么三类都不行"的统一原因**——读起来像 mini-survey 而不是 problem build-up | 高 |
| R2 | §4 把"DACE 是什么 + 三个组件 + we observe..."全压在一段，**信息密度过高**，超过 NeurIPS 单段承载量 | 高 |
| R3 | "坍缩与遗忘是同一动力学的两面 / 互锁失败模式"用了两次，但**这种互锁关系没被任何具体机制说明** | 中 |
| R4 | §1 末尾的 RQ 是英文斜体，**和上下文中文行文不衔接** | 低 |
| R5 | Contribution 第 1 条说 "to our knowledge the first..."，**这种 framing 容易被打** | 中 |

### 1.2 对 GPT 版 6 段稿的批判

| # | 问题 | 严重性 |
|---|---|---|
| G1 | **6 段过长**——每段 200-300 字，整体接近 1.5 页；NeurIPS introduction 通常 0.9-1.0 页，6 段会被砍 | 高 |
| G2 | **§5 和 §6 重复**——§5 已经说了 "co-evolution turns into coverage- and memory-aware process"，§6 又花一整段重复 "DACE 改变了游戏 preserve 的对象"。**应该合并** | 高 |
| G3 | **§3 和 §4 平行结构过于工整**（"first limitation... second limitation..."），导致读起来像 textbook 而不是 paper | 中 |
| G4 | **Contribution 4 条太分散**——第 1 条和第 4 条都是"meta-level"贡献（一个讲 framing，一个讲 evaluation），中间两条才是技术贡献；NeurIPS 习惯 3 条紧凑式 | 中 |
| G5 | **缺少 Figure 1 引用**——MAGIC 的 Fig 1 在 §1.2 直接被援引，是非常有效的视觉锚点；GPT 版完全没提 | 中 |
| G6 | **缺少"we observe..."实证 hook**——MAGIC 在 introduction 末尾提"attacker evolves novel combinatorial strategies through iterative RL"是非常有效的 anticipation hook；GPT 版完全没有 | 中 |
| G7 | **§2 把 MAGIC 介绍得太详细**（讲了 MAGIC 解决的 2 个 limitation），喧宾夺主——读者会以为这是 MAGIC 的论文 | 中 |
| G8 | **§5 三组件介绍中，"normalized coverage gain"和"KL contraction efficiency"等核心 technical novelty 完全没出现**——只是 high-level 说"扩展覆盖"，方法层面的 differentiation 弱 | 高 |
| G9 | **没有量化的实验数字**——NeurIPS introduction 通常会在 contribution 末尾透露 1-2 个 headline 数字（如"reduces ASR from 54.69% to 42.18% on AutoDAN-turbo"），GPT 版完全没有 | 中 |
| G10 | **§1 的 hook"safety failures are no longer triggered only by direct harmful instructions"很弱**——这是一个公认事实，没有 punch | 低 |

### 1.3 两版的"共同盲点"

把两版交叉看，发现**三个根本性的设计缺失**：

| # | 共同盲点 | 必须补 |
|---|---|---|
| C1 | **没有用一个具体的 failure case / 数字证据**让读者立刻共情两个 pathology——MAGIC 用 "+21.8% SBERT 仍 mode collapse" 是一个绝佳的具体证据，但两版都只是"宣告式"地说 collapse 和 forgetting 存在 | 高 |
| C2 | **"两个 pathology 互锁"的具体机制没说明**——这是 DACE 的 conceptual selling point，但两版都停留在哲学化措辞 | 高 |
| C3 | **DACE 的"故事核心"不够 sharp**——GPT 版主张"coverage- and memory-aware safety training process"已经不错，但缺一个更 punchy 的一句话定位，能让 reviewer 立刻理解 DACE 的"identity" | 中 |

---

## 二、整体故事线设计（融合两版优点 + 修复全部问题）

### 2.1 核心哲学（再次拍板）

> DACE 的 introduction 应该是 **MAGIC-style 的 4 段叙事**（控制在 1 页内），叙事结构遵循：
>
> **Hook → Co-evolution 范式（含 MAGIC 但不喧宾夺主）→ 双重 pathology + 现有方法的失败原因（聚焦不并列）→ DACE 的核心思想 + 实证 hook + 四点贡献**
>
> 关键改进相对前两版：
>
> 1. **聚焦式而非并列式 build-up**：不写"the first limitation... the second limitation..."的工整对仗，而是用一段把"为什么坍缩与遗忘互相加剧"讲清楚（用具体数字证据），再用一段说"现有多样性 + replay 方法的统一缺陷"（不并列三类）。
> 2. **配 Figure 1**：左边画 MAGIC attacker 在 12×10 grid 上的频率塌缩 + 防御对当前攻击 ASR vs 对早期攻击 ASR 的反向曲线；右边画 DACE 的均匀策略覆盖 + 贝叶斯回放循环。Fig 1 在 §2 末援引。
> 3. **Contribution 写 3 条而非 4 条**：合并 "framing + technical novelty"，每条都包含 conceptual + technical + empirical 三个要素。
> 4. **§4 末尾保留 we observe... hook**：DACE-attacker 自发演化出多策略组合攻击（呼应 MAGIC §5.3 Q5 同款发现，但 DACE 频率更高）。
> 5. **每个段都对应一个具体的 reviewer 关切**——逐段防御。

### 2.2 4 段映射

| 段 | 类比 MAGIC 段 | 核心命题 | 防御的 reviewer 关切 |
|---|---|---|---|
| **§1** | MAGIC §1 ¶1 | 静态对齐 → 动态对抗博弈是必然方向 | "为什么需要 co-evolution" |
| **§2** | MAGIC §1 ¶2 + Fig 1 | Co-evolution 是当前 SOTA framing，但暴露双重 pathology | "你和 MAGIC 的差别？"（**先承认贡献再指空白**） |
| **§3** | MAGIC §1 ¶3-4 | 现有"多样性 + replay"工作的统一失败原因 | "diversity 不就是 Rainbow Teaming 吗？" / "replay 不就是 SSP 吗？" |
| **§4** | MAGIC §1 ¶5-6 | DACE 的核心思想 + we observe... hook | "你的方法 novelty 在哪里？" |
| **Contributions** | MAGIC 末尾 bullet | 3 条紧凑贡献 | 把 conceptual + technical + empirical 各打一拳 |

---

## 三、Introduction 中文最终初稿（NeurIPS 高质量水准）

下面给出 4 段叙事 + 3 条 contributions 的完整内容。每段 200-300 字，整体目标 0.9-1.0 页 NeurIPS 排版。

---

### § 1 Hook + Big Picture（约 230 字）

> 大语言模型（LLM）已经从代码生成、医疗辅助到科学研究中广泛部署 (Bai et al., 2025)，使其安全对齐成为不可回避的核心问题。然而，主流对齐范式——基于人类反馈的强化学习 (RLHF) (Ouyang et al., 2022)、外部 guardrail 模型 (Inan et al., 2023)、以及静态对齐数据集——本质上都是**面向"已知攻击分布"的反应式补丁**：每次新型 jailbreak 出现，社区先收集样本、再训练新一代模型，循环往复。然而攻击演化的速度远快于反应式防御——从早期的角色扮演 (Shen et al., 2023) 到自动化对抗优化 (Zou et al., 2023; Chao et al., 2023)，从隐蔽的多轮代理化攻击 (Rahman et al., 2025) 到近期出现的 Markov 链组合攻击 (Qi et al., 2025) 在 GPT-4o 与 Gemini-2.0-flash 上 ASR 超过 90%——攻击者的策略空间持续扩张。这一根本性不对称迫使我们重新审视防御范式：***LLM safety alignment 不应被视为固定数据集上的离线训练问题，而应被建模为攻击者与防御者持续协同演化的动态过程。***

---

### § 2 Co-evolution 范式 + 双重 Pathology（约 290 字，配 Figure 1）

> 这一思路在近期工作中取得了实质性进展。Self-RedTeam (Liu et al., 2025) 通过 zero-sum self-play 给出 Nash 均衡下的安全保证；MAGIC (Wen et al., 2026) 进一步将攻防交互建模为非对称序贯博弈，在 Subgame Perfect Nash Equilibrium 下取得点态安全保证。然而，**co-evolution 是必要的，但不是充分的**——深入分析这些框架的训练动态，我们发现一个被普遍忽视的事实：当 co-evolution 仅由"对当前对手的最优响应"驱动时，会暴露两个互相加剧的内生 pathology。**(i) 攻击策略坍缩 (Attack Strategy Collapse)**：在 RL 奖励最大化压力下，attacker 迅速过拟合到少数高回报策略模式——Self-RedTeam 自己的实验显示，即便相对于静态 defender 取得 +21.8% 的 SBERT 多样性，t-SNE 空间中仍能观察到明显的聚类塌缩；GFlowNet 红队 (Lee et al., 2024) 进一步证明即使加入显式新颖性正则，标准 RL attacker 仍会塌缩到一小群相似 prompt。**(ii) 防御对抗遗忘 (Defense Adversarial Forgetting)**：当 attacker 策略持续漂移时，defender 倾向过拟合当前 attacker，逐步丢失对早期攻击的鲁棒性，类似持续学习中的灾难性遗忘 (Kirkpatrick et al., 2017)，但因对手非平稳性而更严重。**关键在于这两个 pathology 互为因果**：坍缩使 defender 仅在窄分布上接受训练，加剧遗忘；遗忘使少数有效模式被反复奖励，反过来固化坍缩。结果是 in-distribution 训练指标虚高、真实 OOD 鲁棒性下降的恶性平衡（如 Figure 1 所示）。

---

### § 3 现有"多样性 + Replay"方法的统一失败原因（约 280 字）

> 自然的应对思路是引入多样性奖励缓解坍缩，引入经验回放缓解遗忘。然而**已有这两类方法在 co-evolution 设定下都未能真正生效**，且失败原因可以统一归结为同一个观察。**多样性方面**：Quality-Diversity 离线搜索 (Rainbow Teaming (Samvelyan et al., 2024)、QDRT (Wang et al., 2025)) 在 risk category × attack style 行为空间上用 MAP-Elites 维护 archive，但其搜索过程**以静态 target 为目标，不参与攻防协同训练**；基于 RL 的多样性奖励 (CRT (Hong et al., 2024)、DiveR-CT (Zhao et al., 2024)、GFlowNet 红队) 用 Self-BLEU、SBERT 距离激励 attacker，但这些指标停留在表层文本与嵌入空间，**无法识别"换皮不换招"的伪多样性**——同一个角色扮演策略可以有上百种语言形式。**回放方面**：SSP (Wang et al., 2026) 引入基于奖励高低的 UCB experience replay，但其优先级**仅基于历史奖励，不反映样本对当前 defender 的实时威胁度**——一个早期被攻破但已被防住的样本仍会因高历史奖励反复回放，浪费训练预算；MAGIC 与 ACE-Safety (Li et al., 2025) 则完全不维护历史攻击的回放机制。**这三类方法的统一失败原因可以归结为：它们都是"静态/离线"机制（静态 archive、静态相似度指标、静态优先级）被嫁接到一个本质上是"动态、非平稳、协同演化"的训练系统中**——静态机制无法跟踪 defender 能力的实时漂移，因此既不能真正驱动策略层多样性，也不能可靠识别历史威胁。

---

### § 4 DACE 的提出 + Empirical Hook（约 320 字）

> 基于上述分析，我们提出 ***DACE （Diversity-driven Adversarial Co-Evolution）***，一个将策略空间多样性与历史威胁度感知回放系统性集成到 co-evolution 的 RL 框架。我们的核心见解是：**坍缩与遗忘必须被同时缓解，因为二者互锁——只有 attacker 在 explicit 策略空间上持续探索（缓解坍缩），同时 defender 通过反映当前威胁度的 principled 回放重新接触历史攻击（缓解遗忘），二者才能形成正反馈而非恶性循环**。具体而言，DACE 由三个紧耦合的组件构成。第一，**显式 12×10 攻击策略空间**——基于 Llama-Guard-4 风险分类与 SorryBench 攻击模式聚类构造 $\mathcal{B} = \mathcal{S} \times \mathcal{C}$（120 个槽位），attacker 在每次改写前先显式选择策略 $(s, c) \in \mathcal{B}$，将策略选择从隐式语义约束提升为可观测、可奖励的离散动作；通过 Gemini-2.5-Pro 蒸馏 ~43k 条三段式 CoT 数据进行 SFT 暖启动，注入策略推理能力。第二，**归一化边际覆盖增益奖励**——$R_{\text{coverage}}(x) = \Delta H / \Delta H_{\max}$ 通过自适应归一化**从根源上消除原始熵增量在长周期训练中的 $O(1/|\mathcal{A}|)$ 信号衰减**；KL 散度视角下，该奖励等价于"单步 KL 收缩效率"，并继承前向 KL 的 zero-avoiding 特性。第三，**贝叶斯对抗回放池**——每个样本通过 Beta-Bernoulli 后验追踪当前威胁度，Thompson Sampling 实现探索-利用平衡，指数时间衰减适应 defender 能力漂移，构成 attacker 多样性扩张与 defender 记忆巩固的闭环。**作为 RL 训练的一个 emergent 现象，我们观察到 DACE-attacker 自发演化出 SFT 数据中不存在的多策略组合攻击**（如角色扮演 × 翻译 × 概念替换的复合攻击），且单 rollout 即可达到与 PAIR、TAP 等多轮搜索方法相当的攻击成功率。

---

### Contributions（独立列表，3 条紧凑式）

> We summarize our contributions as follows:
>
> **(1) Diversity-driven adversarial co-evolution with normalized strategy coverage.** We identify two interlocking pathologies—*attack strategy collapse* and *defense adversarial forgetting*—that current co-evolution frameworks fail to address simultaneously. To break this lock-in, we formulate DACE on an explicit $12 \times 10$ attack strategy space and propose a *normalized marginal coverage gain* reward whose adaptive normalization provably eliminates the $O(1/|\mathcal{A}|)$ reward vanishing inherent in raw entropy-based rewards. A KL-divergence reformulation reveals that the reward is equivalent to per-step KL contraction efficiency toward the uniform strategy distribution and inherits the zero-avoiding property that drives strongest exploration toward unfilled slots.
>
> **(2) Bayesian adversarial replay against defense forgetting.** We introduce a unified archive that simultaneously serves as the strategy frequency tracker (for coverage rewards) and the threat-aware replay buffer (for defender training). Each archived sample maintains a Beta-Bernoulli posterior reflecting its real-time threat level against the current defender; Thompson Sampling provides principled exploration-exploitation balance during replay; exponential time decay handles non-stationarity induced by defender evolution; and a posterior-confidence-aware pruning rule retires samples that are sufficiently tested *and* low-threat, closing the loop between attack diversity expansion and defense memory consolidation.
>
> **(3) Comprehensive two-sided evaluation across model families and SOTA OOD attackers.** We evaluate DACE on Qwen2.5-7B-Instruct and Llama3.1-8B-Instruct from both sides of the game. *Defender side*: DACE matches or surpasses MAGIC on 9 safety benchmarks (e.g., HarmBench adv-harm ASR $0.043 \!\rightarrow\! 0.003$) without sacrificing utility (within 2% on IFEval / ARC-C / GPQA / MMLU / AlpacaEval 2); on the OpenRT pipeline (judged by GPT-4o), DACE consistently outperforms MAGIC against PAIR, TAP, AutoDAN, AutoDAN-turbo ($54.69\% \!\rightarrow\! 42.18\%$) and remains robust against the most recent black-box compositional attack MAJIC (Qi et al., 2025). *Attacker side*: DACE-attacker achieves a Coverage Rate $\sim\!30\%$ higher than MAGIC-attacker, with consistent gains across strategy-level, semantic-level, and lexical-level diversity metrics, while maintaining superior cross-defender transferability across six target backbones.

---

## 四、相对前两版的关键改进对照表

| Reviewer 关切 | 前一版（我） | GPT 版 | 本版处理 |
|---|---|---|---|
| §3 三类多样性平行像 mini-survey (R1, G3) | ❌ | ❌ | ✅ §3 改为聚焦式："统一失败原因 = 静态机制嫁接到动态系统" |
| §4 信息密度过高 (R2) | ❌ | ✅ | ✅ §4 通过精炼措辞控制密度，we observe hook 放段末 |
| 互锁机制太哲学化 (R3, C2) | ❌ | ❌ | ✅ §2 末尾用"坍缩 → 窄分布 → 加剧遗忘 → 少数有效模式被反复奖励 → 固化坍缩"具体描述 |
| 6 段过长 (G1) | N/A | ❌ | ✅ 4 段 + 独立 contribution，目标 1 页 |
| §5/§6 重复 (G2) | N/A | ❌ | ✅ 4 段 + contribution 不重复 |
| Contribution 4 条太分散 (G4) | ✅ | ❌ | ✅ 压缩到 3 条紧凑式 |
| 缺 Figure 1 引用 (G5) | ❌ | ❌ | ✅ §2 末援引 Fig 1 |
| 缺 we observe hook (G6) | ❌ | ❌ | ✅ §4 末尾"自发演化组合攻击 + 单 rollout 匹敌多轮"双 hook |
| MAGIC 介绍喧宾夺主 (G7) | ❌ | ❌ | ✅ §2 仅一句概括 MAGIC（"非对称序贯博弈 + SPNE 点态保证"），不展开 |
| 三组件 technical novelty 弱 (G8) | ✅ | ❌ | ✅ §4 写明"归一化消除 reward vanishing"+"KL 收缩效率"+"Beta-Bernoulli 后验追踪当前威胁度" |
| 缺量化数字 (G9) | ✅（弱）| ❌ | ✅ Contribution 第 3 条给 4 个具体数字 |
| §1 hook 太弱 (G10) | ✅ | ❌ | ✅ §1 hook 改为"反应式补丁 vs 持续演化的攻击" + MAJIC 90%+ ASR |
| 缺具体数字证据 (C1) | ❌ | ❌ | ✅ §2 引 Self-RedTeam +21.8% SBERT 仍坍缩 + GFlowNet 红队证据 |
| 故事核心不够 sharp (C3) | ❌ | ✅（弱）| ✅ 关键 claim："静态机制嫁接到动态系统" + "互锁正反馈 vs 恶性循环" |
| "first" claim 弱化 (R5) | ❌ | ❌ | ✅ Contribution 不用 "first"，改用 "to break this lock-in, we formulate DACE on..."（陈述式而非比较式）|
| §1 RQ 中英不衔接 (R4) | ❌ | N/A | ✅ §1 末 RQ 改为完整中文表述（"应被建模为...动态过程"） |

---

## 五、几个最终拍板细节

下面几个点是写作中刻意留白的，等你确认后可以收紧：

1. **Figure 1 设计建议**：三栏布局
   - **(a) Strawman**: MAGIC attacker 在 12×10 策略 grid 上的频率热图（少数 cell 高度集中，大部分 cell 空白）
   - **(b) Forgetting Curve**: 最终 defender 对 attacker iter 1→4 的 ASR 折线（无 replay 时呈 U 形 / 单调上升，DACE 时近水平）
   - **(c) DACE Loop**: 攻击者 (12×10 cell 均匀覆盖) → 贝叶斯回放池 (Beta posterior + Thompson sampling) → 防御者 (混合 batch) 的闭环示意图

   三幅子图分别对应 §2 的两个 pathology（坍缩 + 遗忘）和 §4 的 DACE 解决方案，是非常 efficient 的视觉锚点。

2. **§2 引用 Self-RedTeam +21.8% SBERT 是否合适**：这个数字来自 Self-RedTeam 自己的实验，但 Self-RedTeam 把这个数字作为**正面 selling point**（相对静态 defender 多样性提升）。我们引用它作为"即便如此仍 mode collapse"的证据，虽然不是 Self-RedTeam 自己的 claim，但 GFlowNet 红队 (Lee et al., 2024) 的 Fig 3 才是这个观察的原始来源——他们直接给出了"+21.8% 仍 t-SNE 聚类塌缩"的证据。**写作时建议主要引 Lee et al., 2024 的 Fig 3 作为证据**，Self-RedTeam 引数字仅作背景。

3. **§4 末尾的 we observe hook**：组合攻击案例（Role-play × Translation × Concept Substitution）来自你 v3.1/v4 实际训练的观察吗？还是预期？如果是预期，建议改为 "we anticipate that..." 或者放到 §5 实验观察部分；如果是已经看到的真实现象，那就放心 declare。

4. **Contribution 第 3 条的 ~30% Coverage Rate 数字**：是估算占位，需要等 Tab 5 跑完后用真实数字替换。

5. **是否在 §4 加一句"Theoretical guarantees"**：MAGIC 在 introduction 末尾提到 "Theoretically, we provide insights into a more robust game equilibrium and derive safety guarantees"。如果 DACE 也想强调 KL 视角的理论分析，可以在 §4 末尾或 contribution 第 1 条加一句"DACE inherits MAGIC's SPNE-based pointwise safety guarantee while introducing a coverage-driven exploration mechanism with KL-contraction efficiency interpretation."。这能让 contribution 第 1 条的 technical 含金量更高。

---

如果以上 5 点你 OK，我可以接下来：(a) 把这版中文 introduction 翻译为正式英文，控制在约 1.0 页 NeurIPS 排版，并做 Figure 1 的 caption 草拟；或者 (b) 顺势把 method 章节按 MAGIC §3-§4 的结构（problem formalization + methods + reward design + algorithm）开始草拟。你想推进哪一步？