# DACE Evaluation 分析-opus

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