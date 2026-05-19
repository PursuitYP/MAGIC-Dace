# DACE 实验和intro分析-gpt

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

## DACE Evaluation Survey：结论先行

我建议把 DACE 的 Evaluation 组织成 **两条主线**：

1. **Defender eval：证明 DACE 训练出的防御者更安全、不过拒、可泛化、不会遗忘。**
   主体直接沿用 MAGIC 的 Table 1/2/3/4 体系，再加入 PIA 的 persona-invariant/OOD persona eval，以及 DACE 特有的 replay/forgetting eval。MAGIC 已经把 defender eval 的基本故事讲清楚：harmful refusal、benign compliance、general capability、OOD attacker generalization、多轮攻击鲁棒性。DACE 的增量应该强调：显式策略空间 + 多样性奖励 + 贝叶斯回放池，让 defender 不只是“当轮变强”，而是在 **更广策略覆盖下变强，并保持历史攻击鲁棒性**。DACE 方法附件里已经明确了攻击策略空间 $\mathcal{B}=\mathcal{S}\times\mathcal{C}$、normalized marginal coverage gain、以及 Bayesian replay/Thompson sampling 混合防御训练机制，这正好支撑这条线。fileciteturn0file0 fileciteturn0file1

2. **Attacker eval：证明 DACE 训练出的攻击者不只是 ASR 高，而是“有效 + 多样 + 可迁移 + 能驱动 defender 学到更稳健的边界”。**
   这里不能只报 ASR。MAGIC 自己也指出“diversity alone does not necessarily reflect attack effectiveness”，因此 DACE attacker eval 要同时报 **effectiveness、diversity、quality-diversity、transferability、training dynamics**。MAGIC Figure 3/Table 10/Figure 4 是最重要参考：cross-evaluation heatmap、attacker transferability、fine-grained strategy distribution。DACE 应该在这些基础上加上策略空间覆盖、成功样本覆盖、QD-score、entropy/KL-to-uniform、hybrid/compositional strategy rate 等指标。fileciteturn0file2

---

## 1. 从已有初评结果看，DACE defender 的当前故事已经比较强

你给的三张初评图里，DACE 和 MAGIC 都是在 **Qwen2.5-7B-Instruct** 上对比。从结果看，DACE defender 的主叙事应是：

### 1.1 Safety / helpfulness 主表：DACE 在 harmful refusal 上整体优于 MAGIC，但要解释少数退化点

在 Table 1 对应的 11 个指标中，DACE 相比 MAGIC：

| 维度 | MAGIC | DACE | 判断 |
|---|---:|---:|---|
| WG:Test adv harm ASR↓ | 0.023 | **0.008** | DACE 更好 |
| WG:Test van harm ASR↓ | 0.002 | **0.002** | 持平 |
| WJB adv harm ASR↓ | 0.198 | **0.149** | DACE 更好 |
| DAN adv harm ASR↓ | 0.043 | **0.003** | DACE 明显更好 |
| HarmBench adv harm ASR↓ | 0.055 | **0.053** | 小幅更好 |
| HarmBench van harm ASR↓ | **0.019** | 0.075 | DACE 退化 |
| OR-Bench RTA↑ | 0.977 | **0.986** | DACE 更好 |
| XSTest harmful RTA↑ | **0.860** | **0.860** | 持平 |
| StrongREJECT RTA↑ | 0.988 | **0.998** | DACE 更好 |
| WJB adv benign ASR↑ | **0.968** | **0.968** | 持平 |
| XSTest benign Comply↑ | **0.945** | 0.920 | DACE 退化 |

推荐写法：**DACE 在更强 adversarial/strategy-driven safety benchmarks 上收益明显，尤其是 DAN、WJB adv harm、WG adv harm 和 StrongREJECT；但 HarmBench vanilla harmful 与 XSTest benign compliance 需要作为 trade-off 分析点。** 这很自然：DACE 的多样性和 replay 机制可能提高对隐蔽/对抗式 prompt 的覆盖，但也可能让模型对某些 vanilla harmful/benign boundary 更敏感，需要用 ablation 定位是 diversity reward、replay ratio、还是 reward/refusal calibration 造成的。

### 1.2 General capability：DACE 基本保留能力，但不是全面优于 MAGIC

Table 2 中 DACE 相比 MAGIC：IFEval Prompt Loose 0.736 vs 0.745、Instruct Loose 0.818 vs 0.821、ARC-C 0.579 vs 0.592、MMLU 0.733 vs 0.735、AlpacaEval 32.478% vs 33.224%，只有 GPQA 0.317 vs 0.308 更好。
推荐写法：**DACE 的 general capability degradation 较小，整体仍在 MAGIC 附近，但不能宣称全面无损；需要在最终论文里加 confidence interval 或重复运行，避免被审稿人抓住小幅差异。** MAGIC 的主表就是这样把 safety gain 和 general capability 保持放在一起讲的。fileciteturn0file2

### 1.3 Defender generalization：这是 DACE 当前最强的 defender 亮点

Table 3 中 DACE 在 HarmBench OOD attacker eval 上：

| Attacker | MAGIC ASR↓ | DACE ASR↓ | 判断 |
|---|---:|---:|---|
| no-rev | 13.44 | **13.12** | 小幅更好 |
| GCG | **11.25** | 12.18 | 小幅退化 |
| PAIR | 25.31 | **21.56** | 更好 |
| TAP | 35.63 | **31.87** | 更好 |
| AutoDAN | 24.38 | **23.44** | 更好 |
| AutoDAN turbo | 54.69 | **42.18** | 明显更好 |

推荐写法：**DACE 在 5/6 个 OOD attacker 上优于 MAGIC，尤其对 AutoDAN turbo、TAP、PAIR 的泛化更强，说明多样性驱动攻击训练和 replay 可能确实提升了 defender 对非训练攻击分布的覆盖。** 唯一 GCG 小退化建议后续补充 “white-box/gradient suffix attacks remain challenging” 的讨论。

---

## 2. Defender Evaluation：建议最终实验结构

### Table D1：Safety + benign compliance 主表，直接对齐 MAGIC Table 1

**目的：** 证明 DACE defender 的核心安全提升不是靠过拒获得的。
**数据集/指标：**

| 类别 | Benchmark | 指标 |
|---|---|---|
| Harmful refusal | WildGuardTest adv/van harm | ASR↓ |
| Harmful refusal | WildJailBreak adv harm | ASR↓ |
| Harmful refusal | DAN | ASR↓ |
| Harmful refusal | HarmBench adv/van | ASR↓ |
| Over-refusal robustness | OR-Bench-toxic | RTA↑ |
| Over-refusal robustness | XSTest contrast/harmful | RTA↑ |
| Hard refusal | StrongREJECT | RTA↑ |
| Benign compliance | WJB adv benign | ASR/compliance↑ |
| Benign compliance | XSTest safe | Comply↑ |

MAGIC 使用 Qwen3Guard 作为 reward model 和 evaluation judge，同时采用 Ai2 safety evaluation suite，包括 HarmBench、WildGuardTest、WildJailBreak、OR-Bench、XSTest、StrongREJECT、DAN，并用 XSTest/WJB benign 检查 benign compliance。这个 protocol 可以直接复用，方便横向对比。fileciteturn0file2 HarmBench 本身也是标准化 red-teaming/robust refusal evaluation framework，WildGuard 则覆盖 malicious intent、response safety risk、refusal detection 三类评估任务，适合作为自动评测 judge 的基础。

**推荐 baselines：**

| Baseline | 为什么需要 |
|---|---|
| Base Instruct | 证明安全起点 |
| Self-RedTeam | co-evolution/self-play 直接相关基线 |
| MAGIC | 最关键 baseline，DACE 需要证明改进点 |
| DACE-full | 主方法 |
| DACE w/o diversity reward | 证明多样性奖励有效 |
| DACE w/o Bayesian replay | 证明 replay/anti-forgetting 有效 |
| DACE w/o both | 证明不是训练轮数/数据量导致 |

Self-RedTeam 是 online self-play RL，用单模型交替扮演 attacker/defender；MAGIC 采用 decoupled attacker/defender asymmetric game 来避免共享参数目标冲突；AdvGame 则把 safety alignment 作为 non-zero-sum game，并用 pairwise preference reward 联合训练 attacker/defender。DACE 需要定位为：继承 MAGIC/AdvGame 的 co-evolution，但把 **策略覆盖和历史攻击记忆** 显式纳入训练目标。

### Table D2：General capability 主表，沿用 MAGIC Table 2

**目的：** 证明 DACE 没有通过“拒绝一切”换安全。
**推荐 benchmark：**

| 能力 | Benchmark |
|---|---|
| Instruction following | IFEval Prompt Loose / Instruct Loose |
| Reasoning / knowledge | ARC-C, GPQA, MMLU |
| Chat helpfulness | AlpacaEval 2 LC Win Rate |
| 可选 | MT-Bench / Arena-Hard / OpenCompass general suite |

MAGIC 的 Table 2 用 IFEval、ARC-C、GPQA、MMLU、AlpacaEval 2 评估 general capability，结果显示 safety training 后大体保持能力。DACE 应该完全复用，尤其你现在初评显示 DACE general capability 小幅低于 MAGIC，所以最终论文需要把这部分做扎实。fileciteturn0file2

### Table D3：Defender generalization to known attackers，沿用 MAGIC Table 3

**目的：** 证明 DACE defender 不只防住自己的 attacker，而能泛化到外部 attack families。
**推荐 attackers：**

| 攻击类型 | 方法 |
|---|---|
| No-revision/direct | HarmBench vanilla/no-rev |
| Gradient suffix | GCG |
| LLM iterative rewriting | PAIR |
| Tree search | TAP |
| Evolutionary attack | AutoDAN |
| Strong evolutionary attack | AutoDAN-turbo |
| 可选新 baselines | Auto-RT, RainbowPlus, QDRT, GFlowNet attacker |

MAGIC 在 Table 3 已经用 no-rev/GCG/PAIR/TAP/AutoDAN/AutoDAN-turbo 做 HarmBench ASR，并用 GPT-4o/OpenRT judge。DACE 现在在 5/6 个 attacker 上优于 MAGIC，这应作为最终 defender eval 的重点表。fileciteturn0file2 Auto-RT 强调自动探索复杂 jailbreak strategy，RainbowPlus/QDRT 强调 QD search 和高多样性攻击，因此可以作为更强的可选外部 attacker。

### Table D4：PIA-style persona-invariant/OOD persona eval

**目的：** 证明 DACE 对 persona/role-based jailbreak 也稳健，而不是只覆盖传统改写攻击。
PIA 的核心观点是：安全决策应该与 persona context 解耦，即相同 harmful intent 不应因为角色设定而从拒答变成有害响应。PIA 的 attack side 用 Persona Lineage Evolution，借助 lineage-based credit propagation 和 UCB exploration；defense side 用 Persona-Invariant Consistency Learning，把 persona-free output distribution 作为 teacher，通过 forward KL 约束 persona-based output。fileciteturn0file3 PIA 的 GitHub 也明确把它定义为针对 persona-based jailbreak 的 adversarial self-play / persona-invariant alignment 框架。

**推荐 eval：**

| Benchmark | 指标 |
|---|---|
| PIA OOD elite personas × StrongREJECT | ASR↓ |
| PIA OOD elite personas × WildGuardTest | ASR↓ |
| PIA OOD elite personas × XSTest-contrast | ASR↓ |
| PIA OOD elite personas × DAN | ASR↓ |
| PIA OOD elite personas × HarmBench | ASR↓ |
| PIA OOD elite personas × MaliciousInstruct | ASR↓ |
| PIA OOD elite personas × OR-Bench-toxic | ASR↓ |

PIA Table 2 就是这个结构：在 OOD elite personas 下，PICL 显著降低 StrongREJECT、WildGuardTest、XSTest-contrast、DAN、HarmBench、MaliciousInstruct、OR-Bench-toxic 的 ASR；同时 Table 3/4 检查 benign over-refusal 和 general capability。DACE 可以复用这个 protocol，比较 Base、MAGIC、DACE、DACE+PICL optional。fileciteturn0file3

### Figure D1：Defense adversarial forgetting / replay retention curve

**目的：** 这是 DACE 相比 MAGIC 最应该突出的新实验。
MAGIC 证明 co-evolution 有效，但 DACE 的方法附件明确指出了 “Defense Adversarial Forgetting”，并用 Bayesian replay pool + Thompson sampling 缓解历史攻击遗忘。fileciteturn0file0

**推荐做法：**

- 每轮 $k$ 保存 defender checkpoint $D_k$。
- 把攻击样本按产生轮次分成 archive buckets：early / middle / late。
- 对每个 $D_k$ 评估：
  - early attack ASR↓
  - middle attack ASR↓
  - latest attack ASR↓
  - external attack ASR↓
- 对比：
  - DACE-full
  - DACE w/o replay
  - uniform replay
  - FIFO replay
  - top-ASR replay
  - Thompson sampling replay

**理想现象：**
DACE-full 在 latest attacks 上不输 w/o replay，同时在 early attacks 上明显更低 ASR；这就能证明 replay 不是单纯增加数据量，而是缓解 adversarial forgetting。

---

## 3. Attacker Evaluation：建议最终实验结构

### Figure A1：Cross-evaluation heatmap，沿用 MAGIC Figure 3

**目的：** 证明 DACE attacker 随训练变强，同时 defender 也在适应，展示 co-evolution dynamics。
MAGIC Figure 3 用 attacker checkpoints × defender checkpoints 做 cross-evaluation heatmap，说明 attacker 早期能力提升、defender 快速适应，最终 game 逐渐稳定。fileciteturn0file2

**DACE 推荐设置：**

| 轴 | 内容 |
|---|---|
| rows | Attacker checkpoints：Base / SFT / RL iter1 / iter2 / iter3 / final |
| cols | Defender checkpoints：Base / RL iter1 / iter2 / iter3 / final |
| seed | HarmBench test 320 或 WJB harmful 600 |
| metric | ASR↓ for defender / ASR↑ for attacker |
| judge | GPT-4o + WildGuard/Qwen3Guard 双 judge subset |

**要点：**
单独看 final ASR 不够；heatmap 能体现 DACE 的 attacker 是否真的在不断发现 moving target，而不是只在固定 defender 上过拟合。

### Table A1：Attacker transferability，沿用 MAGIC Table 10

**目的：** 证明 DACE attacker 学到的是 transferable attack policy，而不是对 DACE defender 的局部 exploit。
MAGIC Table 10 用 600 个 WildJailBreak vanilla harmful seeds，比较 Base attacker 和 MAGIC-attacker 对 Qwen2.5、Llama3.1、Mistral、Gemini、MAGIC-defender 的 single-rollout ASR。MAGIC-attacker 对 base defenders 显著提高 ASR，但对 MAGIC-defender 不占优势，说明 defender co-trained 后对该攻击分布更稳。fileciteturn0file2

**DACE 推荐表：**

| Attacker \ Defender | Qwen2.5-7B | Llama3.1-8B | Mistral-7B | Gemini/closed | MAGIC-def | DACE-def |
|---|---:|---:|---:|---:|---:|---:|
| Base attacker |  |  |  |  |  |  |
| MAGIC-attacker |  |  |  |  |  |  |
| DACE-attacker |  |  |  |  |  |  |
| DACE-attacker w/o diversity |  |  |  |  |  |  |
| DACE-attacker w/o replay-aware training |  |  |  |  |  |  |

**必须报告：** single rollout / temperature / query budget。
这是为了公平对比 GCG、PAIR、TAP、AutoDAN 这类 test-time search 方法，因为它们通常需要多轮查询或迭代搜索，而 DACE/MAGIC attacker 是 single generation，更适合大规模 red-teaming。MAGIC Appendix E 也明确强调了这个区别。fileciteturn0file2

### Figure A2：Attack efficiency curve：query budget vs ASR

**目的：** 避免审稿人说 DACE attacker 只是采样更多。
推荐横轴是 query budget：1、2、4、8、16 rollouts；纵轴是 ASR。比较：

- Base attacker
- MAGIC-attacker
- DACE-attacker
- PAIR
- TAP
- AutoDAN / AutoDAN-turbo
- RainbowPlus / QDRT optional

RainbowPlus 报告其 QD/evolutionary framework 在 HarmBench 上对 12 个 LLM 取得高平均 ASR，并强调比 AutoDAN-Turbo 更快；QDRT 也强调通过 behavior-conditioned training 和 behavioral replay buffer 生成兼具高质量和多样性的 attackers。 所以 DACE 如果要进入 attacker eval，需要在同等预算下证明：**同样查询预算下 ASR 更高，或同样 ASR 下 diversity 更高。**

---

## 4. Attacker Diversity Evaluation：DACE 最应该新增的部分

### Table A2：Strategy-space coverage metrics

DACE 的核心方法是显式策略空间 $\mathcal{B}=\mathcal{S}\times\mathcal{C}$ 和 normalized marginal coverage gain，因此最终论文必须把这个空间的覆盖情况可视化/量化。附件方法中已经定义 coverage reward、frequency-inverse novelty、KL-to-uniform 视角和 Bayesian archive，这些都可以自然转成 eval metrics。fileciteturn0file0

推荐指标：

| 指标 | 定义 | 解释 |
|---|---|---|
| Cell Coverage | $|\{b:n(b)>0\}|/|\mathcal{B}|$ | 攻击策略槽位覆盖率 |
| Successful Cell Coverage | $|\{b:n_{succ}(b)>0\}|/|\mathcal{B}|$ | 有效攻击覆盖率，比普通 coverage 更重要 |
| Normalized Entropy | $H(p_B)/\log|\mathcal{B}|$ | 分布均匀性 |
| KL-to-uniform | $D_{KL}(p_B\|u)$ | 越低越接近均匀覆盖 |
| Effective #Strategies | $\exp(H(p_B))$ | 等效策略数 |
| Max Cell Share | $\max_b p(b)$ | mode collapse 指标 |
| Gini / Simpson / SEI | 多样性指数 | 和 Ruby/Rainbow 系列对齐 |
| QD-score | $\sum_b \max_{x\in b} quality(x)$ | quality-diversity 总质量 |
| Coverage@ASR threshold | ASR>τ 的槽位比例 | 有效且多样 |

Ruby Teaming 在 Rainbow Teaming 基础上加入 memory cache，并报告 ASR、Shannon’s Evenness Index、Simpson’s Diversity Index；Rainbow Teaming 把 adversarial prompt generation 明确建模成 quality-diversity problem；这些都支持 DACE 用 SEI/SDI/coverage/QD-score 作为 diversity 评估指标。

### Figure A3：2D strategy map / archive heatmap

**横轴：** attack method $\mathcal{C}$
**纵轴：** risk category $\mathcal{S}$
**颜色：** 每个 cell 的 best ASR、success count、或 reward-adjusted QD score。

建议画三张：

1. MAGIC-attacker archive heatmap
2. DACE-attacker w/o diversity heatmap
3. DACE-full archive heatmap

**理想现象：** DACE-full 的高质量成功样本分布更广，低频槽位不空，且不是靠填充大量无效攻击获得 coverage。

### Figure A4：Fine-grained attack pattern distribution，沿用 MAGIC Figure 4

MAGIC Appendix F 用 20 类 fine-grained attack strategy taxonomy，并跟踪 RL 训练过程中 strategy distribution 如何变化；结论是 RL 不只是放大 SFT template，而会产生复杂构造、多条件叠加、合法性借口等新组合。fileciteturn0file2

DACE 可以复用 MAGIC 的 20 类 taxonomy，但最好扩展成 DACE 的 $\mathcal{S}\times\mathcal{C}$：

| MAGIC-style category | DACE 对应 |
|---|---|
| Role-playing | attack method $c$ |
| Academic/Educational pretext | attack method $c$ |
| Concealment/key information hiding | attack method $c$ |
| Concept substitution | attack method $c$ |
| Legitimacy pretext | attack method $c$ |
| Multi-condition stacking | attack method $c$ |
| Encoding / translation / format manipulation | attack method $c$ |
| harmful risk category | risk category $s$ |

新增指标：

- Hybrid strategy rate：多策略组合比例。
- Novel combo rate：训练初始/SFT 数据中未出现过的组合比例。
- Success-weighted hybrid rate：成功攻击中组合策略比例。
- Strategy drift over rounds：每轮策略分布 JS divergence。
- Mode collapse score：top-1/top-3 strategy share。

### Table A3：Semantic diversity + textual diversity

为了和更多 red-teaming 文献对齐，建议同时报告文本层面和语义层面指标：

| 指标 | 用途 |
|---|---|
| Self-BLEU↓ | 表面形式多样性 |
| Distinct-1/2↑ | n-gram 多样性 |
| SBERT average pairwise distance↑ | 语义多样性 |
| Cluster coverage↑ | 语义簇覆盖 |
| Topic coverage↑ | topic/risk diversity |
| Embedding entropy↑ | 语义分布均匀性 |

CRT 使用 curiosity-driven exploration 来提高 test case coverage；DiveR-CT 指出普通 semantic novelty reward 随历史增长会 stagnate，并通过 relaxed constraints 和 kNN-style dynamic semantic reward 提升多样性；OpenAI 的 “Diverse and Effective Red Teaming” 把任务拆成 diverse goals + effective attacks，并用 multi-step RL 进一步提高 diversity。DACE 可以把这些作为 diversity eval 的外部依据。

---

## 5. DACE 最终实验推荐：优先级

### P0：必须放进主文

| 编号 | 实验 | 形式 | 作用 |
|---|---|---|---|
| D1 | Safety + benign compliance | Table | 对齐 MAGIC Table 1，证明安全且不过拒 |
| D2 | General capability | Table | 对齐 MAGIC Table 2，证明能力保留 |
| D3 | Defender OOD attacker generalization | Table | 对齐 MAGIC Table 3，展示当前 DACE 强项 |
| A1 | Attacker-defender cross-eval | Heatmap | 对齐 MAGIC Figure 3，证明 co-evolution |
| A2 | Attacker transferability | Table | 对齐 MAGIC Table 10，证明 attacker 可迁移 |
| A3 | Strategy coverage / QD metrics | Table + heatmap | DACE 核心贡献，必须有 |
| Ablation | w/o diversity, w/o replay | Table | 证明不是训练预算导致 |

### P1：强烈建议放主文或 appendix 前部

| 实验 | 为什么重要 |
|---|---|
| PIA-style OOD persona jailbreak | 覆盖 lijiajia PIA，证明 DACE 对 persona attack 有效 |
| Defense forgetting curve | DACE replay pool 的核心证据 |
| Query-budget efficiency curve | 避免与 test-time search attacker 不公平 |
| Judge robustness | Qwen3Guard/WildGuard/GPT-4o subset 交叉验证 |
| Multi-turn X-Teaming | MAGIC Table 4 方向，增强真实场景说服力 |

### P2：可放 appendix

| 实验 | 用途 |
|---|---|
| Hyperparameter sensitivity: $\lambda_{success/fail}$, replay ratio, $\gamma$, $\epsilon$, $n_{min}$ | 方法可信度 |
| Coverage vs novelty reward | 证明 normalized coverage 优于简单 novelty |
| Thompson vs uniform/FIFO/top-ASR replay | 证明 Bayesian replay 设计 |
| Human eval / sanitized qualitative cases | 增强可读性 |
| Agent safety benchmarks | 如果论文扩展到 agent/tool-use，再加入 |

---

## 6. 具体 ablation 设计

### Table B1：Diversity reward ablation

| Variant | 目的 |
|---|---|
| DACE-full | 主方法 |
| w/o diversity reward | 验证攻击策略是否坍缩 |
| raw marginal entropy gain | 验证 normalized reward 是否解决 reward vanishing |
| frequency-inverse novelty | 验证简单 novelty 是否足够 |
| semantic novelty only | 对比 CRT/DiveR-CT 类方法 |
| success-only diversity $\lambda_{fail}=0$ | 验证失败样本保留探索信号的价值 |
| equal diversity $\lambda_{success}=\lambda_{fail}=1$ | 验证有效性优先原则 |

报告：attacker ASR、successful coverage、entropy、QD-score、defender D1/D3 表现。

### Table B2：Replay ablation

| Variant | 目的 |
|---|---|
| no replay | 检查 forgetting |
| uniform replay | 检查 Thompson 是否必要 |
| FIFO replay | 检查只靠新样本是否够 |
| top posterior mean | 检查纯 exploitation 是否导致覆盖不足 |
| Thompson sampling | 主方法 |
| different replay ratio: 1/4, 1/2, 1 | 找安全/能力 trade-off |

报告：early/mid/late attacks ASR、OOD attacker ASR、benign compliance、general capability。

### Table B3：Strategy space ablation

| Variant | 问题 |
|---|---|
| risk category only $\mathcal{S}$ | 只有风险类别是否够 |
| attack method only $\mathcal{C}$ | 只有攻击方式是否够 |
| full $\mathcal{S}\times\mathcal{C}$ | 二维组合是否带来增益 |
| auto-extracted $b(x)$ vs LLM-judged $b(x)$ | 评估 descriptor extraction 稳定性 |

---

## 7. 推荐论文叙事

最终 DACE 的 evaluation story 可以这样写：

> MAGIC 证明了 attacker-defender co-evolution 能提升 defender safety，并保持 helpfulness；但 MAGIC 的 attacker diversity 主要是 emergent 的，缺少显式覆盖目标，且 defender 对历史 attack distribution 的保持能力没有被系统评估。PIA 证明 persona 维度会导致安全决策漂移，并用 lineage/UCB 与 persona-invariant consistency 解决 persona-specific jailbreak。DACE 进一步把 co-evolution 扩展为 diversity-driven and memory-aware safety game：attacker 通过显式 $\mathcal{S}\times\mathcal{C}$ 策略空间和 normalized coverage reward 扩大有效攻击覆盖；defender 通过 Bayesian replay pool 同时学习新攻击与历史高风险攻击，从而提升 OOD generalization 并缓解 adversarial forgetting。MAGIC、Self-RedTeam、AdvGame、SEAS 等工作共同支持从静态补丁式 safety tuning 转向 online co-evolution；Rainbow/Ruby/RainbowPlus/QDRT/CRT/DiveR-CT/GFlowNet 等工作则支持 DACE 必须从 effectiveness 和 diversity 两个维度评估 attacker。

---

## 8. 建议最终主文表图排布

**Main paper：**

1. **Table 1：Defender safety and benign compliance**
   Base / Self-RedTeam / MAGIC / DACE / ablations。

2. **Table 2：General capability**
   IFEval、ARC-C、GPQA、MMLU、AlpacaEval 2。

3. **Table 3：OOD attacker robustness**
   no-rev、GCG、PAIR、TAP、AutoDAN、AutoDAN-turbo。

4. **Figure 3：Attacker-defender cross-evaluation heatmap**
   展示 co-evolution dynamics。

5. **Table 4：Attacker transferability and efficiency**
   DACE-attacker vs MAGIC-attacker vs base attacker，single rollout + query budget。

6. **Figure 4：DACE strategy-space archive heatmap**
   $\mathcal{S}\times\mathcal{C}$ coverage，展示 DACE 的核心创新。

7. **Table 5：Quality-diversity metrics**
   successful coverage、entropy、KL-to-uniform、QD-score、Self-BLEU、SBERT diversity。

8. **Table 6：Ablation**
   w/o diversity、w/o replay、raw coverage、novelty、uniform replay、Thompson replay。

**Appendix：**

- PIA-style OOD persona eval。
- Multi-turn X-Teaming。
- Replay forgetting curves。
- Hyperparameter sensitivity。
- Judge robustness。
- Sanitized qualitative cases。

-----

> https://arxiv.org/abs/2508.13048
> MAJIC: Markovian Adaptive Jailbreaking via Iterative Composition of Diverse Innovative Strategies
> 这篇论文是不是可以补充table 3 oprenrt eval的stronger attacker，
> 你也可以调研其他论文，以及详细分析safety diversity和 auto automatic red teaming相关的论文，
>
> 接下来请按照实验章节来梳理所有Evaluation，可以参考magic论文的实验和附录的写法，【直接给出experiment章节内容】，一些描述可以简要说一下，主要写清楚每个图表分别想说明什么问题，考虑到论文的篇幅，请注意权衡选择最重要的几个实验，不重要的可以放在附录或者直接删除，注意实验的故事逻辑。

可以，**MAJIC 非常适合补充到 Table 3 / OpenRT defender generalization eval 里作为 stronger adaptive black-box attacker**。但建议在表里写成 **MAJIC-Attack**，避免和 MAGIC baseline 混淆。

MAJIC 的定位和 Table 3 很匹配：它不是固定模板攻击，而是把多种 disguise strategies 的 sequential composition 建模为 Markov chain，并根据攻击结果动态更新 strategy transition probability；论文报告在 GPT-4o、Gemini-2.0-flash 等模型上达到 90%+ ASR，平均每次攻击少于 15 queries。 官方代码也明确包含 10 类 obfuscation methods、Markov transition matrix、Q-learning-inspired dynamic optimization，并支持 GPT-4、Claude、Llama、Gemini 和多种 judge。

我建议 **主文 Table 3 加 MAJIC-Attack**，Appendix 再放 RainbowPlus / Auto-RT / Ferret / QDRT。原因是：MAJIC 与 DACE 的“策略组合、多样性、自适应攻击”关系最直接；RainbowPlus/QDRT 更适合作为 attacker diversity / quality-diversity eval 的对照，而不一定都塞进 defender generalization 主表。RainbowPlus、Ruby、Ferret、Auto-RT、QDRT、OpenAI diverse red teaming 共同说明：自动红队评估不能只看 ASR，还要看 diversity、coverage、quality-diversity 和 query efficiency。turn108460view2turn108460view3turn108460view4turn108460view5turn848505view7

下面是可以直接改写进论文的 **Experiments 章节草案**。

---

# 5. Experiments

## 5.1 Experimental Setup

We evaluate DACE from both the defender and attacker sides. The defender evaluation follows the safety–utility protocol of MAGIC, focusing on harmful refusal, benign compliance, general capability, and out-of-distribution attack robustness. The attacker evaluation is designed to capture both **effectiveness** and **diversity**, since a strong red-teamer should not only achieve high ASR but also cover a broad range of attack strategies and risk categories.

### Models

We conduct experiments on Qwen2.5-7B-Instruct as the main backbone. When compute allows, we additionally report results on Qwen2.5-14B-Instruct and Llama3.1-8B-Instruct to verify scalability across model families. For each backbone, DACE trains two decoupled agents: an attacker and a defender. The attacker is initialized with offensive rewriting data, while the defender starts from the original instruction-tuned model.

### Baselines

We compare DACE with the following baselines:

1. **Base Instruct Model**, the original aligned model without additional adversarial training.
2. **Self-RedTeam**, an online self-play baseline that alternates attack and defense roles.
3. **MAGIC**, the strongest co-evolution baseline and the most direct comparison.
4. **DACE variants**, including:
   - DACE w/o diversity reward;
   - DACE w/o Bayesian replay;
   - DACE w/ raw entropy gain;
   - DACE w/ frequency-inverse novelty;
   - DACE w/ uniform replay.

These ablations isolate the contribution of the two main designs in DACE: explicit diversity-driven attacker optimization and Bayesian adversarial replay for the defender.

### Judges and Metrics

For safety evaluation, we use automatic safety judges following MAGIC’s protocol. For the OpenRT/HarmBench generalization evaluation, we use GPT-4o as the judge, consistent with MAGIC Table 3. The primary safety metrics are:

- **ASR↓**: attack success rate on harmful prompts. Lower is better for defender evaluation.
- **RTA↑**: robustness to attacks or refusal-to-answer accuracy on harmful prompts.
- **Comply↑**: benign compliance rate on safe prompts.
- **LC Win↑**: length-controlled AlpacaEval 2 win rate for general helpfulness.

For attacker evaluation, we report:

- **ASR@1 / ASR@k↑**: attack success under one or k attack attempts.
- **Avg. Queries↓**: average query budget required for a successful attack.
- **Transfer ASR↑**: attack success on unseen defenders.
- **Successful Coverage↑**: fraction of strategy cells with at least one successful attack.
- **Normalized Entropy↑**: entropy of the attack strategy distribution normalized by the maximum entropy.
- **QD-Score↑**: quality-diversity score, computed as the sum of the best attack quality across strategy cells.
- **Max-Cell Share↓**: the largest fraction occupied by any single strategy cell, used to detect mode collapse.

The diversity metrics are motivated by quality-diversity red-teaming literature. Rainbow Teaming frames adversarial prompt generation as a quality-diversity search problem and shows that red-teaming data can improve safety without sacrificing general capability. Ruby Teaming further evaluates quality-diversity using Shannon’s Evenness Index and Simpson’s Diversity Index, while QDRT argues that simplistic diversity metrics such as word frequency or embedding similarity fail to capture meaningful strategy variation.turn108460view5

---

## 5.2 Main Defender Results: Safety without Over-Refusal

**Question 1: Does DACE improve harmful refusal while preserving benign compliance?**

We first evaluate DACE on harmful refusal and benign compliance benchmarks. This table follows the structure of MAGIC Table 1.

### Table 1: Safety evaluation on harmful refusal and benign compliance

**Purpose.**
Table 1 answers whether DACE improves safety without simply becoming over-conservative. The harmful side evaluates whether the defender refuses malicious or adversarially rewritten prompts. The benign side evaluates whether the defender still answers safe prompts.

**Benchmarks.**

- WildGuardTest adversarial harmful / vanilla harmful;
- WildJailBreak adversarial harmful;
- DAN;
- HarmBench adversarial / vanilla harmful;
- OR-Bench toxic;
- XSTest contrast;
- StrongREJECT;
- WildJailBreak adversarial benign;
- XSTest safe.

**Main text description.**

DACE achieves stronger harmful refusal than MAGIC on most adversarial safety benchmarks. On Qwen2.5-7B-Instruct, DACE reduces WildGuardTest adversarial harmful ASR from 0.023 to 0.008, WildJailBreak adversarial harmful ASR from 0.198 to 0.149, and DAN ASR from 0.043 to 0.003. It also improves StrongREJECT RTA from 0.988 to 0.998 while keeping WildJailBreak benign compliance comparable to MAGIC.

However, DACE slightly underperforms MAGIC on HarmBench vanilla harmful and XSTest benign compliance. This indicates that the diversity-driven attacker and replay-enhanced defender improve robustness to adversarially structured attacks, but may introduce a small trade-off on certain vanilla or benign boundary cases. We analyze this trade-off in the ablation section.

**Table layout.**

| Method | WG adv ASR↓ | WG van ASR↓ | WJB adv ASR↓ | DAN ASR↓ | HB adv ASR↓ | HB van ASR↓ | OR-Bench RTA↑ | XSTest RTA↑ | StrongREJECT RTA↑ | WJB benign↑ | XSTest Comply↑ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Base |  |  |  |  |  |  |  |  |  |  |  |
| Self-RedTeam |  |  |  |  |  |  |  |  |  |  |  |
| MAGIC | 0.023 | 0.002 | 0.198 | 0.043 | 0.055 | 0.019 | 0.977 | 0.860 | 0.988 | 0.968 | 0.945 |
| DACE | **0.008** | **0.002** | **0.149** | **0.003** | **0.053** | 0.075 | **0.986** | **0.860** | **0.998** | **0.968** | 0.920 |

**Why this table is important.**
This is the main safety table. It should stay in the main paper.

---

## 5.3 General Capability Evaluation

**Question 2: Does DACE degrade general capabilities?**

Following MAGIC Table 2, we evaluate whether safety training hurts instruction following, reasoning, and general helpfulness.

### Table 2: General capability evaluation

**Purpose.**
Table 2 shows whether DACE obtains safety gains by sacrificing general model capability. This is necessary because a model can appear safer by refusing too much or by becoming less capable overall.

**Benchmarks.**

- IFEval Prompt Loose;
- IFEval Instruct Loose;
- ARC-Challenge;
- GPQA;
- MMLU;
- AlpacaEval 2 LC Win Rate.

**Main text description.**

DACE largely preserves general capabilities. On Qwen2.5-7B-Instruct, DACE remains close to MAGIC on IFEval, MMLU, and AlpacaEval 2, while slightly improving GPQA. The small drops on IFEval and ARC-C suggest that diversity-driven safety training may introduce a mild instruction-following trade-off, but the overall degradation is limited compared with the safety gains observed in Table 1.

**Table layout.**

| Method | IFEval Prompt↑ | IFEval Instruct↑ | ARC-C↑ | GPQA↑ | MMLU↑ | AlpacaEval 2 LC Win↑ |
|---|---:|---:|---:|---:|---:|---:|
| Base |  |  |  |  |  |  |
| Self-RedTeam |  |  |  |  |  |  |
| MAGIC | 0.745 | 0.821 | 0.592 | 0.308 | 0.735 | 33.224% |
| DACE | 0.736 | 0.818 | 0.579 | **0.317** | 0.733 | 32.478% |

**Why this table is important.**
This table should stay in the main paper because it supports the safety–utility trade-off claim.

---

## 5.4 Defender Generalization to Stronger Out-of-Distribution Attackers

**Question 3: Does DACE generalize to unseen and stronger attack algorithms?**

We evaluate defender robustness on HarmBench using OpenRT with GPT-4o as the judge, following MAGIC Table 3. This evaluation tests whether DACE only overfits to its own attacker or generalizes to external attack families.

### Table 3: Defender generalization on HarmBench/OpenRT

**Purpose.**
Table 3 measures robustness against external attackers that were not used as DACE’s training attacker. This is the key table for proving defender generalization.

**Attackers.**

Main-paper attackers:

- no-revision;
- GCG;
- PAIR;
- TAP;
- AutoDAN;
- AutoDAN-turbo;
- **MAJIC-Attack**.

We add MAJIC-Attack because it is an adaptive black-box attacker that composes multiple disguise strategies through a dynamically updated Markov transition matrix. This makes it a stronger and more relevant stress test than fixed or single-strategy attacks.turn848505view1

**Main text description.**

DACE improves defender generalization to a broad set of OOD attackers. Compared with MAGIC, DACE achieves lower ASR on no-revision, PAIR, TAP, AutoDAN, and AutoDAN-turbo, with a particularly large reduction on AutoDAN-turbo. This suggests that DACE’s diversity-driven attacker exposes a broader set of vulnerabilities during training, enabling the defender to generalize better to unseen adaptive attacks.

We further include MAJIC-Attack as a stronger adaptive black-box attacker. Since MAJIC uses multiple queries per attack attempt, we report both ASR and average query budget. This prevents unfair comparison with single-query or fixed-budget attackers.

**Table layout.**

| Defender | no-rev↓ | GCG↓ | PAIR↓ | TAP↓ | AutoDAN↓ | AutoDAN-turbo↓ | MAJIC-Attack↓ | Avg. Queries↓ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Gemini-2.5-Flash |  |  |  |  |  |  |  |  |
| Qwen2.5-7B-Instruct |  |  |  |  |  |  |  |  |
| + Self-Eval |  |  |  |  |  |  |  |  |
| + SmoothLLM |  |  |  |  |  |  |  |  |
| + Self-RedTeam |  |  |  |  |  |  |  |  |
| + MAGIC | 13.44 | **11.25** | 25.31 | 35.63 | 24.38 | 54.69 | TBD | TBD |
| + DACE | **13.12** | 12.18 | **21.56** | **31.87** | **23.44** | **42.18** | TBD | TBD |

**Design note.**
MAJIC-Attack should be in the main table if we can run it reliably. RainbowPlus, Auto-RT, Ferret, and QDRT are better placed in the appendix because they add more evaluation dimensions and may require different budgets or archives. RainbowPlus is especially strong but its evaluation involves quality-diversity search and multi-element archives, which makes it less directly comparable to the standard OpenRT Table 3 setting.

**Why this table is important.**
This is the strongest defender-generalization evidence. It should stay in the main paper.

---

## 5.5 Attacker Effectiveness and Co-Evolution Dynamics

**Question 4: Does DACE train a stronger attacker during co-evolution?**

DACE is not only a defender-training method. Its attacker is explicitly optimized for both attack effectiveness and strategy diversity. We therefore evaluate the attacker separately.

### Figure 3: Cross-evaluation heatmap between attacker and defender checkpoints

**Purpose.**
Figure 3 follows MAGIC Figure 3. It visualizes the co-evolution process by evaluating attacker checkpoints against defender checkpoints from different training rounds.

**Setup.**

Rows are attacker checkpoints:

- Base attacker;
- SFT attacker;
- RL iter 1;
- RL iter 2;
- RL iter 3;
- final attacker.

Columns are defender checkpoints:

- Base defender;
- RL iter 1;
- RL iter 2;
- RL iter 3;
- final defender.

Each cell reports ASR on a fixed HarmBench or WildJailBreak harmful seed set.

**Expected observation.**

Early in training, later attacker checkpoints should achieve higher ASR against earlier defenders, indicating that DACE improves attacker capability. Later defenders should reduce ASR across most attacker checkpoints, indicating that the defender adapts to increasingly diverse attacks. A stable final block suggests that the co-evolution process approaches a more robust equilibrium.

**Why this figure is important.**
This figure explains the training story. It shows that DACE is not simply adding more adversarial data; it creates a moving-target interaction where attacker and defender both improve.

---

## 5.6 Attacker Transferability and Query Efficiency

**Question 5: Does the DACE attacker discover transferable attacks, or does it overfit to the DACE defender?**

### Table 4: Attacker transferability across unseen defenders

**Purpose.**
Table 4 evaluates whether the DACE attacker can transfer to other target models and defenses. This is the attacker-side counterpart of Table 3.

**Setup.**

We evaluate attacker checkpoints against multiple frozen defenders:

- Qwen2.5-7B-Instruct;
- Llama3.1-8B-Instruct;
- Mistral-7B-Instruct;
- Gemini-2.0/2.5;
- MAGIC defender;
- DACE defender.

**Metrics.**

- ASR@1;
- ASR@5;
- average queries to success;
- transfer ASR.

**Table layout.**

| Attacker | Qwen2.5 ASR@1↑ | Llama ASR@1↑ | Mistral ASR@1↑ | Gemini ASR@1↑ | MAGIC-def ASR@1↑ | DACE-def ASR@1↑ | Avg. Queries↓ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Base attacker |  |  |  |  |  |  |  |
| MAGIC attacker |  |  |  |  |  |  |  |
| DACE w/o diversity attacker |  |  |  |  |  |  |  |
| DACE attacker |  |  |  |  |  |  |  |

**Main text description.**

DACE attacker should achieve higher transfer ASR than MAGIC attacker and DACE w/o diversity attacker, especially under ASR@1 and ASR@5. This would indicate that explicit strategy coverage helps the attacker learn generalizable attack pathways rather than overfitting to one defender.

**Why this table is important.**
This table supports the claim that DACE improves the attacker, not only the defender.

---

## 5.7 Strategy Diversity and Quality-Diversity Analysis

**Question 6: Does DACE prevent attack strategy collapse?**

This is the most important DACE-specific evaluation. MAGIC shows that co-evolution can produce novel strategies, but DACE explicitly optimizes for strategy-space coverage. Therefore, we need to directly evaluate whether DACE produces attacks that are both successful and diverse.

### Figure 4: Strategy-space archive heatmap

**Purpose.**
Figure 4 visualizes the DACE attack archive over the two-dimensional strategy space $\mathcal{B}=\mathcal{S}\times\mathcal{C}$, where $\mathcal{S}$ is the risk category and $\mathcal{C}$ is the attack method.

**Setup.**

Rows are risk categories, columns are attack strategies. Each cell shows one of the following:

- number of successful attacks;
- best ASR in the cell;
- best attack reward in the cell;
- QD-score contribution.

We plot three heatmaps:

1. MAGIC attacker;
2. DACE w/o diversity reward;
3. DACE full.

**Expected observation.**

MAGIC and DACE w/o diversity may concentrate on a few high-reward strategies, such as role-play or authority manipulation. DACE full should cover more cells, especially successful cells, while maintaining high attack quality.

**Why this figure is important.**
This is the clearest visualization of DACE’s core contribution: diversity-driven strategy coverage.

---

### Table 5: Attacker quality-diversity metrics

**Purpose.**
Table 5 quantifies the diversity shown in Figure 4. It prevents the diversity claim from relying only on visualization.

**Metrics.**

| Metric | Meaning |
|---|---|
| ASR@1↑ | single-shot attack effectiveness |
| ASR@5↑ | low-budget attack effectiveness |
| Cell Coverage↑ | fraction of occupied strategy cells |
| Successful Coverage↑ | fraction of cells with at least one successful attack |
| Normalized Entropy↑ | strategy distribution uniformity |
| KL-to-Uniform↓ | distance from uniform coverage |
| QD-Score↑ | total best quality over occupied strategy cells |
| Max-Cell Share↓ | mode collapse indicator |
| Hybrid Strategy Rate↑ | fraction of attacks combining multiple strategies |
| Novel Combo Rate↑ | fraction of strategy combinations unseen in SFT data |

**Table layout.**

| Method | ASR@1↑ | ASR@5↑ | Cell Cov.↑ | Success Cov.↑ | Entropy↑ | KL↓ | QD-Score↑ | Max Share↓ | Hybrid Rate↑ | Novel Combo↑ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MAGIC attacker |  |  |  |  |  |  |  |  |  |  |
| DACE w/o diversity |  |  |  |  |  |  |  |  |  |  |
| DACE w/ novelty |  |  |  |  |  |  |  |  |  |  |
| DACE full |  |  |  |  |  |  |  |  |  |  |

**Main text description.**

DACE full should improve both ASR and successful coverage. This is crucial: higher diversity alone is insufficient if the generated attacks are ineffective. Conversely, higher ASR alone is insufficient if attacks collapse into a narrow strategy cluster. The QD-score captures this joint objective by rewarding high-quality attacks across many strategy cells.

This evaluation follows the broader automatic red-teaming literature. OpenAI’s diverse and effective red-teaming work explicitly separates the generation of diverse attack goals from the generation of effective attacks for those goals. QDRT similarly argues that meaningful diversity should reflect attack styles and risk categories rather than only surface-level text differences.

**Why this table is important.**
This table should be in the main paper because it directly validates the DACE attacker design.

---

## 5.8 Robustness to Persona-Based and Multi-Turn Attacks

**Question 7: Does DACE generalize to structured distribution shifts such as persona jailbreaks and multi-turn attacks?**

This section can be shortened in the main paper and expanded in the appendix. Since PIA is highly relevant to DACE, we include a compact persona-based evaluation in the main paper if space permits.

### Table 6: Structured robustness under multi-turn and persona attacks

**Purpose.**
Table 6 evaluates whether DACE generalizes beyond single-turn prompt rewriting. We include two stress tests:

1. **Multi-turn X-Teaming**, following MAGIC Table 4.
2. **OOD persona jailbreaks**, following PIA’s evaluation protocol.

PIA shows that safety decisions can become unstable under persona perturbations, and proposes persona-invariant consistency to decouple safety behavior from persona context. This motivates evaluating DACE under OOD persona-based jailbreaks, even if DACE is not specifically designed only for persona attacks.fileciteturn0file3

**Benchmarks.**

- X-Teaming multi-turn ASR;
- X-Teaming jailbreak rate;
- OOD persona × StrongREJECT;
- OOD persona × HarmBench;
- OOD persona × MaliciousInstruct;
- OOD persona × OR-Bench-toxic.

**Table layout.**

| Method | X-Teaming ASR↓ | X-Teaming JB Rate↓ | Persona StrongREJECT ASR↓ | Persona HarmBench ASR↓ | Persona MaliciousInstruct ASR↓ | Persona OR-toxic ASR↓ |
|---|---:|---:|---:|---:|---:|---:|
| Base |  |  |  |  |  |  |
| MAGIC |  |  |  |  |  |  |
| PIA/PICL |  |  |  |  |  |  |
| DACE |  |  |  |  |  |  |
| DACE + PICL optional |  |  |  |  |  |  |

**Main text description.**

DACE improves robustness under both multi-turn and persona-based attacks, indicating that diversity-driven co-evolution learns more transferable safety boundaries. However, if PICL remains stronger on pure persona-based jailbreaks, we present this honestly and position PICL as complementary: DACE improves broad attack diversity and adversarial replay, while PICL specifically enforces persona-invariant safety behavior.

**Placement recommendation.**

If page budget is tight, keep only one row summary in the main paper and move the full persona/multi-turn table to the appendix.

---

## 5.9 Ablation Studies

**Question 8: Which components of DACE are responsible for the gains?**

### Table 7: Main ablation on safety, diversity, and generalization

**Purpose.**
Table 7 identifies whether the improvements come from diversity reward, Bayesian replay, or simply additional training.

**Variants.**

- DACE full;
- DACE w/o diversity reward;
- DACE w/o Bayesian replay;
- DACE w/ raw marginal entropy gain;
- DACE w/ frequency-inverse novelty;
- DACE w/ uniform replay;
- DACE w/ top-risk replay;
- DACE w/ Thompson replay.

**Metrics.**

To keep the table compact, we report representative metrics:

- WJB harmful ASR↓;
- DAN ASR↓;
- AutoDAN-turbo ASR↓;
- XSTest benign compliance↑;
- Successful Coverage↑;
- QD-Score↑;
- Early-attack retention ASR↓.

**Table layout.**

| Variant | WJB ASR↓ | DAN ASR↓ | AutoDAN-turbo ASR↓ | XSTest Comply↑ | Success Cov.↑ | QD-Score↑ | Early Attack ASR↓ |
|---|---:|---:|---:|---:|---:|---:|---:|
| DACE full |  |  |  |  |  |  |  |
| w/o diversity |  |  |  |  |  |  |  |
| raw entropy gain |  |  |  |  |  |  |  |
| novelty reward |  |  |  |  |  |  |  |
| w/o replay |  |  |  |  |  |  |  |
| uniform replay |  |  |  |  |  |  |  |
| Thompson replay |  |  |  |  |  |  |  |

**Expected conclusion.**

Removing the diversity reward should reduce strategy coverage and QD-score, and may weaken OOD attacker generalization. Removing replay should increase early-attack ASR, showing adversarial forgetting. Raw entropy gain may underperform normalized coverage because the marginal reward vanishes as the archive grows. Frequency-inverse novelty may improve coverage but should be weaker than normalized coverage on QD-score and successful coverage.

---

### Figure 5: Defense adversarial forgetting curve

**Purpose.**
Figure 5 is the key evidence for Bayesian replay. It measures whether the defender forgets old attacks while adapting to new ones.

**Setup.**

We divide attacks by the round in which they were discovered:

- early attacks;
- middle attacks;
- latest attacks.

For each defender checkpoint, we evaluate ASR on each bucket.

**Expected observation.**

DACE w/o replay should adapt to latest attacks but gradually forget early attacks. DACE full should maintain low ASR on early attacks while still improving on latest attacks. This shows that Bayesian replay does not merely add more data; it stabilizes safety across the evolving attack distribution.

**Why this figure is important.**
This is a DACE-specific figure and should be in the main paper if space permits. If not, it should appear early in the appendix.

---

## 5.10 Appendix Experiments

To control main-paper length, we move the following experiments to the appendix.

### Appendix A: Stronger automatic red-teamers

We evaluate additional automatic red-teamers beyond MAJIC-Attack:

- RainbowPlus;
- Auto-RT;
- Ferret;
- QDRT.

RainbowPlus is included because it extends MAP-Elites-style quality-diversity search with a multi-element archive and reports strong ASR/diversity and faster runtime than AutoDAN-Turbo. Auto-RT is included because it uses reinforcement learning for automatic jailbreak strategy exploration with early-terminated exploration and progressive reward tracking. Ferret is included because it improves Rainbow Teaming with reward-based scoring and reports both higher ASR and better efficiency. QDRT is included because it explicitly targets high-quality and diverse attackers across attack styles and risk categories.

### Appendix B: Judge robustness

We repeat core safety evaluations with multiple judges:

- Qwen3Guard;
- WildGuard;
- GPT-4o;
- Llama Guard.

This ensures DACE’s gains are not artifacts of a single automatic judge.

### Appendix C: Hyperparameter sensitivity

We study:

- diversity coefficient $\lambda$;
- $\lambda_{\text{success}}$ vs. $\lambda_{\text{fail}}$;
- replay ratio $B_{\text{replay}}/B_{\text{train}}$;
- Beta prior $(\alpha,\beta)$;
- time decay $\gamma$;
- pruning threshold $\epsilon$;
- archive size.

### Appendix D: Qualitative strategy analysis

We provide sanitized examples of evolved attack strategies. We avoid including operationally harmful details and focus on the abstract strategy labels, such as role-play, translation, authority framing, hypothetical scenario, and multi-strategy composition.

### Appendix E: Full benchmark tables

We include full results for all model sizes and benchmark splits.

---

# 推荐最终主文图表顺序

考虑篇幅，我建议主文只放 **7 个核心图表**：

| Main paper item | 放置理由 |
|---|---|
| Table 1: Safety + benign compliance | 核心 defender safety 结果 |
| Table 2: General capability | 证明不是过拒或能力坍缩 |
| Table 3: OpenRT/HarmBench OOD attackers + MAJIC-Attack | 最强 defender generalization 证据 |
| Figure 3: Attacker–defender cross-eval heatmap | 讲清 co-evolution dynamics |
| Table 4: Attacker transferability | 证明 DACE attacker 有效且可迁移 |
| Figure 4: Strategy-space archive heatmap | DACE 核心创新：策略覆盖 |
| Table 5 or Table 7: QD metrics + ablation combined | 节省篇幅，同时证明 diversity/replay 有效 |

如果只能再压缩，优先保留 Table 1/2/3、Figure 4、Ablation Table；把 cross-eval heatmap、attacker transferability、persona/multi-turn 放 appendix。我的推荐是：**MAJIC-Attack 进主文 Table 3；RainbowPlus/Auto-RT/Ferret/QDRT 进 appendix；PIA-style persona eval 进 appendix 或主文短表。**

-----

> [文件不支持导出]
> 附件中四个文件依次是初次实现、第二轮的debug、第三轮的debug、第四轮的debug，请结合代码实现过程和改进辅助理解dace研究方法和细节，
>
> 以及根据下面写的再完善一下实验部分的写作和说明，实验章节先用中文梳理，
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

下面先把 DACE 的实现演进和实验设计逻辑串起来，然后给出一版**中文实验章节草案**。我会按论文实验章节的写法组织：每个实验回答什么问题、表/图放什么、为什么放主文或附录、预期说明什么。

---

# 一、从四轮实现与 debug 看 DACE 方法细节

DACE 的实验设计不能只按“方法设想”写，必须反映代码迭代中暴露出来的真实问题。四轮实现基本把 DACE 从“MAGIC + diversity idea”逐步推成了一个可解释的 **diversity-driven + replay-aware co-evolution system**。

## 1. 初始实现：DACE 的核心机制已经形成，但还停留在 14×10 策略空间

初始实现计划把 MAGIC 扩展为两部分：一是显式二维攻击策略空间与多样性奖励，二是 Bayesian replay pool 来缓解 defender 遗忘。Archive pool 同时存储攻击成功 prompt、策略槽位、Beta-Bernoulli posterior、step_added 和 replay 所需的数据字段；攻击策略空间最初采用 14 个 risk categories × 10 个 attack styles，即 140 个槽位。fileciteturn1file3

这一版已经确定了 DACE 最核心的实验命题：

1. **attacker 是否因为 diversity reward 覆盖更多策略槽位；**
2. **defender 是否因为 replay buffer 保持对历史攻击的鲁棒性；**
3. **最终 defender 是否比 MAGIC 更能泛化到 OOD attackers。**

因此，实验不能只复用 MAGIC Table 1/2/3，还必须新增 attacker-side 的 effectiveness/diversity 评测，以及 replay/forgetting 评测。

## 2. 第一轮 debug：发现 defender stage 没有把新成功攻击写入 pool

第一轮诊断发现一个关键实现漏洞：attacker stage 的成功攻击会进入 pending buffer，但 defender stage 中 new_batch 的成功攻击没有任何路径写入 replay pool，导致 defender→attacker 切换时几乎 flush 0 条。这违反了伪代码中“Stage 2 结束后将新攻击成功样本加入池中”的设计。fileciteturn1file2

这个 bug 对实验设计的启发是：**必须单独评测 replay buffer 的有效性和组成**，不能只看最终 ASR。否则 replay buffer 可能“看起来存在”，但真正进入池子的样本分布并没有覆盖训练过程中的关键攻击。

因此后续实验里要加入：

- replay buffer size / coverage / posterior distribution；
- replay buffer 中样本的 harmfulness；
- replay buffer 中样本在 12×10 attack space 上的分布；
- w/o replay buffer 的 ablation；
- early/mid/late attack retention curve。

## 3. 第二/第三轮 debug：发现 benign prompt 语义冲突和 format/strategy extraction 问题

第三轮诊断里最重要的两个发现：

第一，MAGIC-SFT attacker 格式通过率高，但 pool 只涨到 20 条，原因是 format reward 只检查 tag 结构，不检查 `<strategy>` 内部是否能被正则解析。于是攻击看起来“格式正确”，但无法抽取 risk category / attack style，最终不能入池。fileciteturn1file0

第二，DACE-SFT 变体的 benign refusal rate 飙到 0.3–0.5，根因是 BENIGN_TEMPLATE 中 “trick the language model into producing harmful responses” 和 “仍然被识别为 benign” 语义冲突，导致 benign rewrite 被蒸馏成带有 harmful 色彩的 adversarial prompt。fileciteturn1file0

这直接影响实验写法：DACE 的 benign compliance 不是附属指标，而是必须作为主线评测之一。否则审稿人会质疑 DACE 只是把 benign prompt 也推向 harmful-looking distribution，从而造成过拒。

所以主文必须保留：

- Table 1：harmful refusal + benign compliance；
- Table 2：general capability；
- ablation 中单独报告 benign compliance / XSTest safe / WJB benign；
- v4 中重新蒸馏 benign SFT data 后，要说明这是为了解决“benign adversarial rewrite must preserve benign intent”。

## 4. 第四轮 v4：12×10 attack space 更合理，也更适合实验叙事

v4 计划决定删除两个低频/不适合当前 text-only defender 的类别：Sexual Content 和 Code Interpreter Abuse，将策略空间从 14×10 改成 12×10。依据是：Sexual Content 在 SFT v3 中只有 0.80%，且 benign not-safe 率高达 96.3%；Code Interpreter Abuse 只有 0.11%，并且更适合 tool-use/code interpreter 场景，不适合当前 text-only defender。fileciteturn1file1

这个修改非常重要。它不只是工程清理，也应进入方法和实验说明：

- 12×10 让 diversity reward 的 denominator 不再被几乎永远空置的 dead rows 主导；
- 12×10 更符合当前 safety text benchmark 的风险覆盖；
- 删除的两个类别可以在 appendix 里说明“不参与训练空间，但 eval 仍可覆盖完整 safety taxonomy”。

v4 同时要求同步修改三条流水线：SFT 数据蒸馏、RL 数据预处理、RL 训练脚本，包括 distill_v4、preprocess_dace.py、archive_pool.py、analysis 常量、GRPO rollout.n=6 等。fileciteturn1file1

因此实验章节中应明确：**所有 v4 主结果均基于 12×10 attack space，旧 14×10 结果只作为开发诊断，不作为最终主实验。**

---

# 二、实验章节整体故事线

DACE 的实验故事建议写成三层：

1. **Defender side：DACE 是否训练出更鲁棒、不过拒、不掉能力的 defender？**
   对齐 MAGIC Table 1/2/3，并补充 MAJIC-Attack 作为 stronger adaptive attacker。

2. **Attacker side：DACE 是否训练出更有效、更可迁移、更有策略覆盖的 attacker？**
   参考 MAGIC Table 10，同时加入 replay buffer / online rewrite 的 attack space 分布与 harmfulness 评测。

3. **Mechanism side：DACE 的 diversity reward、SFT warm-up、replay buffer 是否真的有用？**
   通过 ablation 证明每个组件的作用。

主文建议保留 6–7 个核心图表，附录再放完整 attacker diversity、额外 automatic red-teaming、hyperparameter、v4 data quality 等结果。

---

# 三、Experiments 章节中文草案

## 5. Experiments

本节从 defender 和 attacker 两个角度系统评估 DACE。Defender 评测关注安全性、不过拒、通用能力保持和对外部攻击器的泛化；attacker 评测关注攻击有效性、跨模型迁移能力以及策略多样性。由于 DACE 的核心目标不是单纯提高 ASR，而是通过显式策略覆盖和历史攻击回放推动攻防双方共同演化，我们进一步设计 ablation 和 replay buffer 分析来验证各组件的作用。

### 5.1 Experimental Setup

#### Models

主实验使用 Qwen2.5-7B-Instruct 作为 backbone，并分别初始化 attacker 和 defender。Attacker 先经过 DACE-SFT v4 数据热启动，然后进入 RL co-evolution；defender 从原始 instruction-tuned checkpoint 开始训练。若计算资源允许，我们在 Qwen2.5-14B-Instruct 和 Llama3.1-8B-Instruct 上补充验证，以考察方法在不同模型规模和模型家族上的稳定性。

#### DACE v4 Attack Space

DACE v4 使用一个 12×10 的二维攻击策略空间：

$$

\mathcal{B} = \mathcal{S} \times \mathcal{C},

$$

其中 $\mathcal{S}$ 包含 12 个 risk categories，$\mathcal{C}$ 包含 10 个 attack styles。相比早期 14×10 版本，我们移除了 Sexual Content 和 Code Interpreter Abuse 两类。前者在 SFT 数据中极低频且 benign not-safe 率异常高，后者主要对应 tool/code-interpreter 场景，不适合当前 text-only defender。该剪裁避免 dead rows 长期占据 diversity reward 的最大边际增益，从而使 coverage reward 更稳定地鼓励有效策略覆盖。fileciteturn1file1

12 个 risk categories 为：

| 编号 | Risk Category |
|---:|---|
| 1 | Violent Crimes |
| 2 | Non-Violent Crimes |
| 3 | Sex-Related Crimes |
| 4 | Child Sexual Exploitation |
| 5 | Defamation |
| 6 | Specialized Advice |
| 7 | Privacy |
| 8 | Intellectual Property |
| 9 | Indiscriminate Weapons |
| 10 | Hate |
| 11 | Suicide & Self-Harm |
| 12 | Elections |

10 个 attack styles 保持不变：Slang、Technical Terms、Role Play、Authority Manipulation、Misspellings、Word Play、Emotional Manipulation、Hypotheticals、Historical Scenario、Uncommon Dialects。

#### Training Data

DACE 的训练数据包括 SFT 数据和 RL 数据两部分。

SFT 数据用于 attacker warm-up。我们基于 v4 版本重新蒸馏 harmful 和 benign rewrite 数据。对 harmful prompts，attacker 学习在指定 risk category 和 attack style 下生成隐蔽有害改写；对 benign prompts，v4 不再要求 “trick the model into harmful responses”，而是要求在保持 benign intent 的前提下生成容易诱发 false-positive / over-refusal 的复杂 prompt。这样可以避免早期版本中 benign rewrite 被错误蒸馏成 harmful-looking prompt 的问题。fileciteturn1file0

RL 数据同样采用 v4 的 12×10 attack space。每个样本在 prompt 中显式提供 risk category 和 attack style 选择空间，attacker 需要输出 `<think>`、`<strategy>`、`<answer>` 三段结构，其中 `<strategy>` 用于从模型输出中解析行为描述符 $b(x)$。

#### Baselines

我们比较以下方法：

| 方法 | 说明 |
|---|---|
| Base | 原始 instruction-tuned model |
| Self-RedTeam | 共享参数或自博弈式 safety baseline |
| MAGIC | 最直接的 co-evolution baseline |
| DACE | 完整方法 |
| DACE w/o SFT | 去掉 attacker SFT warm-up |
| DACE w/o diversity reward | 保留 DACE 格式和 replay，但不加 diversity reward |
| DACE w/o replay buffer | 保留 diversity reward，但 defender 不使用历史回放 |
| DACE w/o diversity design | 退化为 MAGIC-style co-evolution |

这里的 “w/o diversity design → MAGIC” 应谨慎表述。严格来说，它不是完全等同于 MAGIC 代码实现，而是 DACE 中去掉显式 strategy space、coverage reward 和 replay 之后的 MAGIC-style baseline。主文可以写成 “DACE w/o diversity design (MAGIC-style)” 或直接使用 MAGIC checkpoint 作为 baseline。

---

## 5.2 Main Defender Evaluation

### Question 1: DACE 是否提升 harmful refusal，同时避免过拒？

#### Table 1: Safety evaluation on harmful refusal and benign compliance

**表格目的。**
Table 1 是 defender 主结果，回答 DACE 是否在 harmful prompts 上更安全，同时在 benign prompts 上不过拒。它直接对齐 MAGIC Table 1，是主文必须保留的表。

**评测集。**

| 维度 | Benchmark | 指标 |
|---|---|---|
| Harmful refusal | WildGuardTest adv / vanilla harmful | ASR↓ |
| Harmful refusal | WildJailBreak adv harmful | ASR↓ |
| Harmful refusal | DAN | ASR↓ |
| Harmful refusal | HarmBench adv / vanilla harmful | ASR↓ |
| Over-refusal robustness | OR-Bench toxic | RTA↑ |
| Over-refusal robustness | XSTest contrast | RTA↑ |
| Strong refusal | StrongREJECT | RTA↑ |
| Benign compliance | WJB adv benign | Compliance / ASR↑ |
| Benign compliance | XSTest safe | Comply↑ |

**推荐写法。**

> DACE 在大多数 adversarial harmful benchmarks 上取得更强拒答能力。相比 MAGIC，DACE 在 WildGuardTest adversarial harmful、WildJailBreak adversarial harmful 和 DAN 上显著降低 ASR，说明显式策略覆盖能够暴露更广泛的训练攻击模式，从而提升 defender 对隐蔽改写攻击的鲁棒性。同时，我们在 WJB benign 和 XSTest safe 上评估 benign compliance，以验证 DACE 的收益不是来自简单的过度拒答。

**表格建议。**

| Method | WG adv ASR↓ | WG van ASR↓ | WJB adv ASR↓ | DAN ASR↓ | HB adv ASR↓ | HB van ASR↓ | OR-Bench RTA↑ | XSTest RTA↑ | StrongREJECT RTA↑ | WJB benign↑ | XSTest Comply↑ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Base |  |  |  |  |  |  |  |  |  |  |  |
| Self-RedTeam |  |  |  |  |  |  |  |  |  |  |  |
| MAGIC |  |  |  |  |  |  |  |  |  |  |  |
| DACE |  |  |  |  |  |  |  |  |  |  |  |

**主文保留。**
必须保留。

---

### Question 2: DACE 是否保持 general capability？

#### Table 2: General capability evaluation

**表格目的。**
证明 DACE 的 safety gain 不是通过能力退化或统一拒答获得的。该表直接对齐 MAGIC Table 2。

**评测集。**

| 能力 | Benchmark |
|---|---|
| Instruction following | IFEval Prompt Loose / Instruct Loose |
| Knowledge & reasoning | ARC-C, GPQA, MMLU |
| Helpfulness | AlpacaEval 2 LC Win Rate |

**推荐写法。**

> DACE 在显著提升 harmful refusal 的同时，基本保持 general capability。IFEval 和 AlpacaEval 2 用于检测 instruction-following 和 helpfulness 是否受损；ARC-C、GPQA 和 MMLU 用于验证 reasoning 和 knowledge capability。若 DACE 在少数能力指标上略低于 MAGIC，我们将其作为 safety–utility trade-off 讨论，并在 ablation 中分析是否由 replay ratio 或 benign prompt 质量导致。

**表格建议。**

| Method | IFEval Prompt↑ | IFEval Instruct↑ | ARC-C↑ | GPQA↑ | MMLU↑ | AlpacaEval 2 LC Win↑ |
|---|---:|---:|---:|---:|---:|---:|
| Base |  |  |  |  |  |  |
| Self-RedTeam |  |  |  |  |  |  |
| MAGIC |  |  |  |  |  |  |
| DACE |  |  |  |  |  |  |

**主文保留。**
必须保留。

---

### Question 3: DACE defender 是否能泛化到更强 OOD attackers？

#### Table 3: Defender generalization on HarmBench / OpenRT

**表格目的。**
这是 DACE defender 最关键的泛化实验。它回答 DACE 是否只是防住自己的训练 attacker，还是能防住外部攻击算法。

**攻击器。**

主文建议包含：

| Attacker | 类型 | 是否主文 |
|---|---|---|
| no-revision | direct harmful prompt | 主文 |
| GCG | gradient-based suffix attack | 主文 |
| PAIR | LLM iterative attack | 主文 |
| TAP | tree-search attack | 主文 |
| AutoDAN | evolutionary attack | 主文 |
| AutoDAN-turbo | stronger evolutionary attack | 主文 |
| MAJIC-Attack | adaptive Markovian strategy composition | 主文 |

MAJIC 很适合作为 Table 3 的 stronger attacker。它把多种 disguise strategies 的连续选择和组合建模为 Markov chain，并根据攻击结果动态调整 transition probability，论文报告在 GPT-4o、Gemini-2.0-flash 等模型上达到 90%+ ASR，平均每次攻击少于 15 queries。 这与 DACE 的“策略组合、多样性、自适应攻击”主题高度相关，适合放进主表作为更强压力测试。

**推荐写法。**

> We further evaluate defender generalization against external attackers under the OpenRT/HarmBench protocol. Besides standard attackers used in MAGIC, we include MAJIC-Attack, a stronger adaptive black-box attacker that composes diverse disguise strategies with a dynamically updated Markov transition matrix. This setting tests whether DACE learns a broadly robust safety boundary rather than overfitting to its own attacker distribution.

**表格建议。**

| Defender | no-rev ASR↓ | GCG ASR↓ | PAIR ASR↓ | TAP ASR↓ | AutoDAN ASR↓ | AutoDAN-turbo ASR↓ | MAJIC-Attack ASR↓ | MAJIC Avg. Queries↓ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Base |  |  |  |  |  |  |  |  |
| Self-Eval |  |  |  |  |  |  |  |  |
| SmoothLLM |  |  |  |  |  |  |  |  |
| Self-RedTeam |  |  |  |  |  |  |  |  |
| MAGIC |  |  |  |  |  |  |  |  |
| DACE |  |  |  |  |  |  |  |  |

**注意。**
MAJIC 是多 query adaptive attack，因此必须同时报告 Avg. Queries，避免与 single-shot attack 不公平比较。

**主文保留。**
必须保留。MAJIC-Attack 建议进入主文 Table 3。

---

## 5.3 Attacker Evaluation: Effectiveness

### Question 4: DACE attacker 是否比 MAGIC attacker 更强、更可迁移？

DACE 不是只训练 defender，也训练 attacker。因此 attacker 必须单独评测。否则 DACE 的 diversity reward 只会变成训练 trick，而不是可验证的 red-teaming 能力。

#### Table 4: Attacker transferability across target models

**表格目的。**
参考 MAGIC Table 10，用 DACE attacker 和 replay buffer 中的攻击样本去攻击不同 target models，评估 attacker 的 effectiveness 和 transferability。

**评测对象。**

| Attacker source | 说明 |
|---|---|
| Base attacker | 未经 DACE 训练的 attacker |
| MAGIC attacker | MAGIC 训练出的 attacker |
| DACE attacker | DACE final attacker online rewrite |
| DACE replay buffer | DACE archive 中保存的 successful attacks |
| DACE attacker w/o diversity reward | 检查 diversity reward 对 attack transfer 的影响 |
| DACE attacker w/o SFT | 检查 SFT warm-up 对 attack quality 的影响 |

**Target models.**

| Target | 目的 |
|---|---|
| Qwen2.5-7B-Instruct | 同族 base target |
| Llama3.1-8B-Instruct | 跨模型家族 |
| Mistral-7B-Instruct | 跨架构泛化 |
| Gemini / GPT-style API model | closed-source target |
| MAGIC defender | 是否能攻击 MAGIC defender |
| DACE defender | 是否能攻击自身 defender |

**指标。**

| 指标 | 含义 |
|---|---|
| ASR@1↑ | single-shot 攻击能力 |
| ASR@5↑ | low-budget 攻击能力 |
| Avg. Queries↓ | 平均攻击预算 |
| Transfer ASR↑ | 跨模型迁移能力 |
| Harmfulness rate↑ | 攻击 prompt 本身被 guard 判为 harmful 的比例 |
| Valid strategy rate↑ | 能成功解析出 `<strategy>` 的比例 |

**表格建议。**

| Attacker Source | Qwen ASR@1↑ | Llama ASR@1↑ | Mistral ASR@1↑ | Gemini ASR@1↑ | MAGIC-def ASR@1↑ | DACE-def ASR@1↑ | Avg. Queries↓ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Base attacker |  |  |  |  |  |  |  |
| MAGIC attacker |  |  |  |  |  |  |  |
| DACE w/o SFT |  |  |  |  |  |  |  |
| DACE w/o diversity reward |  |  |  |  |  |  |  |
| DACE attacker |  |  |  |  |  |  |  |
| DACE replay buffer |  |  |  |  |  |  |  |

**推荐写法。**

> We evaluate the attacker not only against the co-trained DACE defender, but also against unseen target models. DACE attacker achieves higher ASR@1 and ASR@5 than MAGIC attacker, indicating that explicit strategy-space optimization improves attack transferability rather than merely overfitting to the current defender. We also evaluate attacks stored in the replay buffer, which serves as a curated archive of historically successful and diverse attacks.

**主文/附录选择。**
建议主文保留一张简化 Table 4；完整 target model 结果放附录。

---

### Figure 3: Attacker–Defender cross-evaluation heatmap

**图目的。**
参考 MAGIC Figure 3，展示 co-evolution dynamics。横轴是 defender checkpoints，纵轴是 attacker checkpoints，每个 cell 是 ASR。

**设置。**

| 轴 | 内容 |
|---|---|
| Rows | SFT attacker, RL iter1, RL iter2, RL iter3, final attacker |
| Columns | base defender, iter1 defender, iter2 defender, iter3 defender, final defender |
| Metric | ASR on HarmBench / WJB harmful |
| Judge | GPT-4o / Qwen3Guard / WildGuard subset |

**推荐写法。**

> The heatmap reveals the moving-target nature of DACE training. Later attackers achieve higher ASR against earlier defenders, showing improved offensive capability. Meanwhile, later defenders reduce ASR against a broad range of attacker checkpoints, indicating that replay-enhanced co-evolution leads to a more stable safety boundary.

**主文/附录选择。**
如果主文篇幅紧张，可以放附录；但如果要强调 co-evolution 过程，建议主文保留。

---

## 5.4 Attacker Evaluation: Diversity

### Question 5: DACE attacker 是否避免 strategy collapse？

自动红队相关工作普遍指出，仅报告 ASR 不足以评价 attacker。Rainbow Teaming 将 adversarial prompt generation 明确建模为 quality-diversity problem，目标是同时生成有效且多样的攻击。 QDRT 进一步指出，word frequency 或 sentence embedding similarity 等简单指标不能充分刻画攻击策略差异，因此需要从 attack style 和 risk category 维度评测 diversity。 Ferret 也强调自动红队常面临 categorical diversity 和效率问题，并通过 reward-based scoring 提升搜索效率。

因此，DACE 的 attacker diversity 评测建议分成两层：**strategy-space diversity** 和 **semantic/textual diversity**。

---

### Figure 4: Attack-space distribution heatmap

**图目的。**
展示 DACE attacker / replay buffer 在 12×10 attack space 上的分布。这个图是 DACE 的核心创新展示，建议主文保留。

**绘制对象。**

画三张或四张 heatmap：

1. MAGIC attacker；
2. DACE w/o diversity reward；
3. DACE attacker；
4. DACE replay buffer。

**横纵轴。**

| 轴 | 内容 |
|---|---|
| Y-axis | 12 risk categories |
| X-axis | 10 attack styles |
| Cell color | success count / best ASR / QD-score contribution |

**推荐写法。**

> Compared with MAGIC and DACE without diversity reward, the full DACE attacker covers a broader region of the 12×10 strategy space. More importantly, the replay buffer preserves successful attacks across multiple risk-style combinations, suggesting that DACE does not simply increase surface-level diversity but maintains a diverse set of effective adversarial behaviors.

**主文保留。**
必须保留。这是 DACE 区别 MAGIC 的核心图。

---

### Table 5: Attacker diversity and quality-diversity metrics

**表格目的。**
量化 Figure 4，避免 diversity 只停留在可视化层面。

**指标建议。**

| 指标 | 含义 | 越大/越小 |
|---|---|---|
| ASR@1 | 单次攻击有效性 | ↑ |
| ASR@5 | 低预算攻击有效性 | ↑ |
| Cell Coverage | 覆盖的 12×10 槽位比例 | ↑ |
| Successful Coverage | 至少有一个成功攻击的槽位比例 | ↑ |
| Normalized Entropy | 策略分布均匀性 | ↑ |
| KL-to-Uniform | 与均匀分布距离 | ↓ |
| Max-Cell Share | 最大槽位占比，衡量 collapse | ↓ |
| QD-Score | 每个槽位 best quality 的总和 | ↑ |
| Cosine Similarity | embedding 平均相似度 | ↓ |
| Self-BLEU | 文本重复度 | ↓ |
| Distinct-1/2 | n-gram 多样性 | ↑ |

**表格建议。**

| Method | ASR@1↑ | ASR@5↑ | Cell Cov.↑ | Success Cov.↑ | Entropy↑ | KL↓ | Max Share↓ | QD-Score↑ | Cos Sim↓ | Self-BLEU↓ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MAGIC attacker |  |  |  |  |  |  |  |  |  |  |
| DACE w/o diversity reward |  |  |  |  |  |  |  |  |  |  |
| DACE w/ novelty reward |  |  |  |  |  |  |  |  |  |  |
| DACE full attacker |  |  |  |  |  |  |  |  |  |  |
| DACE replay buffer |  |  |  |  |  |  |  |  |  |  |

**推荐写法。**

> DACE improves diversity at both the strategy and semantic levels. The full model achieves higher successful coverage and lower max-cell share, indicating reduced strategy collapse. Meanwhile, lower cosine similarity and Self-BLEU show that DACE also improves surface and semantic diversity. However, we emphasize strategy-space metrics as the primary diversity evidence, since textual diversity alone may not correspond to meaningful variation in attack behavior.

**主文/附录选择。**
建议主文放简化版，只保留 ASR@1、Successful Coverage、Entropy、QD-Score、Cosine Similarity、Max-Cell Share。完整 Self-BLEU / Distinct / SBERT 指标放附录。

---

### Table 6: Harmfulness and distribution analysis of on-rewrite attacks and replay buffer

**表格目的。**
回答你提出的“统计 attack on-rewrite/replay buffer 在 attack space 的有害性和分布情况”。这个实验非常适合放在 attacker eval 中，证明 replay buffer 不是随机堆积，而是保留了有害、有效且分布广的攻击。

**评测对象。**

| Source | 含义 |
|---|---|
| Online rewrite | DACE attacker 当前生成的攻击 |
| Replay buffer | Archive 中保存的历史成功攻击 |
| High posterior replay | Thompson sampling 高风险样本 |
| Low posterior replay | 被 defender 学会、posterior 下降的样本 |

**指标。**

| 指标 | 含义 |
|---|---|
| Guard harmful rate | 攻击 prompt 被 judge 判为 harmful 的比例 |
| Defender ASR | 对当前 defender 的攻击成功率 |
| Cross-model ASR | 对其他 target model 的成功率 |
| Valid strategy rate | strategy 能否被解析 |
| Cell coverage | attack space 覆盖率 |
| Risk entropy | risk category 分布熵 |
| Style entropy | attack style 分布熵 |
| Mean posterior | replay 样本后验均值 |
| Mean age | replay 样本进入池后的平均步数 |

**表格建议。**

| Source | Harmful Rate↑ | Defender ASR↑ | Cross-model ASR↑ | Valid Strategy↑ | Cell Cov.↑ | Risk Entropy↑ | Style Entropy↑ | Mean Posterior |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Online rewrite |  |  |  |  |  |  |  |  |
| Full replay buffer |  |  |  |  |  |  |  |  |
| Thompson replay samples |  |  |  |  |  |  |  |  |
| Low-posterior samples |  |  |  |  |  |  |  |  |

**推荐写法。**

> We further analyze the attacks generated online and those stored in the replay buffer. The replay buffer maintains a high harmfulness rate and broad strategy coverage, while Thompson-sampled replay examples concentrate on samples with higher posterior risk. This indicates that the buffer does not merely store historical attacks, but acts as an adaptive memory of diverse and currently challenging vulnerabilities.

**主文/附录选择。**
如果篇幅允许，主文放；否则放附录。这个表对解释 replay buffer 很有帮助。

---

## 5.5 Replay Buffer and Forgetting Analysis

### Question 6: replay buffer 是否缓解 defender adversarial forgetting？

#### Figure 5: Early/Mid/Late attack retention curve

**图目的。**
证明 replay buffer 的作用不是增加训练样本数，而是防止 defender 忘记早期攻击。

**设置。**

将训练中产生的攻击按发现轮次划分：

| Bucket | 内容 |
|---|---|
| Early attacks | 前 1/3 训练轮发现的攻击 |
| Mid attacks | 中间 1/3 训练轮发现的攻击 |
| Late attacks | 最后 1/3 训练轮发现的攻击 |

对每个 defender checkpoint 评估三类攻击的 ASR。

**对比方法。**

| Method | 作用 |
|---|---|
| DACE full | 主方法 |
| DACE w/o replay buffer | 检查是否遗忘 |
| DACE uniform replay | 检查 Thompson sampling 是否必要 |
| DACE top-posterior replay | 检查纯 exploitation 是否过拟合高风险样本 |

**推荐写法。**

> Without replay, the defender adapts to recent attacks but gradually becomes vulnerable to early attack patterns. DACE with Bayesian replay maintains low ASR on early and mid-stage attacks while still improving against late-stage attacks. This shows that replay buffer mitigates adversarial forgetting under a non-stationary attacker distribution.

**主文/附录选择。**
建议主文保留。如果篇幅不够，至少在 ablation table 中保留 “Early Attack ASR”。

---

## 5.6 Ablation Studies

### Question 7: DACE 各组成部分分别起什么作用？

#### Table 7: Component ablation

**表格目的。**
证明 DACE 的收益来自 SFT warm-up、diversity reward、12×10 strategy design 和 replay buffer，而不是训练预算或随机波动。

**消融项。**

| Variant | 说明 | 预期现象 |
|---|---|---|
| DACE full | 完整方法 | 最优综合表现 |
| w/o diversity design | 退化为 MAGIC-style | diversity/coverage 大幅下降 |
| w/o SFT training | attacker 无 warm-up | early attacker 弱，pool 增长慢 |
| w/o diversity reward | 有 strategy 格式但无 coverage reward | ASR 可能高，但 strategy collapse |
| w/o replay buffer | defender 只学当前攻击 | early attack forgetting |
| w/ raw entropy gain | 不做 normalized coverage | 后期 reward vanishing |
| w/ novelty reward | 简化 diversity reward | coverage 有效但 QD-score 可能较低 |
| uniform replay | 不用 Thompson sampling | replay 风险选择较弱 |

**主表指标要少。**

建议只放 7 个代表指标：

| 指标 | 代表什么 |
|---|---|
| WJB harmful ASR↓ | 主安全性 |
| DAN ASR↓ | jailbreak robustness |
| AutoDAN-turbo ASR↓ | OOD attacker generalization |
| XSTest safe Comply↑ | benign compliance |
| Successful Coverage↑ | attacker diversity |
| QD-Score↑ | effectiveness + diversity |
| Early Attack ASR↓ | forgetting / replay |

**表格建议。**

| Variant | WJB ASR↓ | DAN ASR↓ | AutoDAN-turbo ASR↓ | XSTest Comply↑ | Success Cov.↑ | QD-Score↑ | Early Attack ASR↓ |
|---|---:|---:|---:|---:|---:|---:|---:|
| DACE full |  |  |  |  |  |  |  |
| w/o diversity design |  |  |  |  |  |  |  |
| w/o SFT |  |  |  |  |  |  |  |
| w/o diversity reward |  |  |  |  |  |  |  |
| w/o replay buffer |  |  |  |  |  |  |  |
| w/ novelty reward |  |  |  |  |  |  |  |
| uniform replay |  |  |  |  |  |  |  |

**推荐写法。**

> Removing the diversity reward leads to a clear drop in successful strategy coverage and QD-score, confirming that explicit coverage optimization is necessary to prevent attack strategy collapse. Removing replay buffer increases ASR on early attacks, demonstrating adversarial forgetting. Removing SFT warm-up weakens the attacker in early training and slows archive growth, indicating that offensive initialization remains important for stable co-evolution.

**主文保留。**
必须保留，但可以压缩，只放关键 variants。

---

## 5.7 Additional Strong Automatic Red-Teamers

这个部分建议放附录，不要挤占主文。

### Appendix Table A1: Evaluation against stronger automatic red-teamers

**候选攻击器。**

| Attacker | 放置建议 | 理由 |
|---|---|---|
| MAJIC-Attack | 主文 Table 3 | 与 DACE 策略组合最相关 |
| RainbowPlus | 附录 | quality-diversity search，适合 diversity stress test |
| Ferret | 附录 | reward-based scoring + efficient ART |
| QDRT | 附录 | style/risk category diversity，与 DACE 最相关但评测复杂 |
| Auto-RT | 附录 | automatic jailbreak strategy exploration |

Rainbow Teaming 和后续 RainbowPlus/QDRT/Ferret 都支持 DACE 的 attacker diversity 评测设计，但如果全部放主文，会造成实验主线发散。主文应聚焦 MAGIC 对齐评测 + MAJIC stronger attacker；更多 automatic red-teaming 放附录作为 stress tests。

---

# 四、论文篇幅权衡：最终主文建议放哪些图表

我建议主文最多放 7 个图表：

| 编号 | 图表 | 是否主文 | 作用 |
|---|---|---|---|
| Table 1 | Safety + benign compliance | 主文 | defender 核心安全性 |
| Table 2 | General capability | 主文 | 证明不过拒/不掉能力 |
| Table 3 | OpenRT OOD attackers + MAJIC-Attack | 主文 | defender 泛化 |
| Figure 3 | Attacker–defender cross-eval heatmap | 主文或附录 | co-evolution dynamics |
| Figure 4 | 12×10 attack-space heatmap | 主文 | DACE 核心贡献 |
| Table 5 | Attacker QD/diversity metrics | 主文 | 证明 attacker 不 collapse |
| Table 7 | Component ablation | 主文 | 证明各组件有效 |

如果页数非常紧张，删减顺序建议是：

1. 把 Figure 3 heatmap 移到 appendix；
2. 把 Table 6 replay buffer harmfulness/distribution 移到 appendix；
3. Table 5 只保留 5 个指标；
4. Table 7 只保留 4 个 variants：Full、w/o SFT、w/o diversity reward、w/o replay buffer。

主文必须保留的是：**Table 1、Table 2、Table 3、Figure 4、Table 7**。

---

# 五、v4 数据补充与实验前置 TODO

你提出的 v4 数据补充非常必要，建议作为实验前的 data quality pipeline，而不是主实验的一部分。

## TODO 1：重新统计 WJB last20k 的 risk category 分布

目标是确认 12 个 risk categories 中哪些在 SFT 数据中仍然低频。具体做法：

1. 部署 Llama-Guard-4；
2. 对 WJB harmful / WJB benign 的后 20k 样本跑 risk category classification；
3. 统计每类数量；
4. 找出 v4 SFT 中仍然低频的 risk categories；
5. 从 WJB last20k 中主动筛选这些类别；
6. 重新蒸馏补充到 sft-data-v4。

## TODO 2：补齐低频 risk category 的 SFT 数据

建议目标不是完全均匀，而是设置最低样本阈值：

| 类型 | 建议阈值 |
|---|---:|
| 每个 risk category harmful SFT | ≥ 1,000 |
| 每个 risk category benign false-positive SFT | ≥ 500 |
| 每个 attack style | ≥ 1,000 |
| 每个 risk-style cell | 不强制均匀，但不能长期为 0 |

因为 12×10 完全均匀会带来数据构造成本，也可能过度牺牲真实分布。更合理的是保证每个 risk category 和 attack style 有足够覆盖，同时让 diversity reward 在 RL 阶段继续推动 cell-level coverage。

## TODO 3：v4 SFT 数据质量检查

在正式 RL 前必须报告：

| 检查项 | 目标 |
|---|---|
| benign not-safe rate | ≤ 20%，越低越好 |
| harmful valid strategy rate | ≥ 95% |
| benign valid strategy rate | ≥ 95% |
| Sexual Content / Code Interpreter Abuse 出现次数 | 0 |
| 12 risk category coverage | 100% |
| 10 attack style coverage | 100% |
| `<think><strategy><answer>` format pass rate | ≥ 95% |

这些指标不一定放主文，可以放 appendix 的 data quality section。

---

# 六、最终实验章节的核心叙事

可以在实验章节开头用这段话作为总述：

> Our evaluation is designed around the two failure modes that motivate DACE: attack strategy collapse and defense adversarial forgetting. We first evaluate whether DACE improves defender robustness without inducing over-refusal or degrading general capabilities. We then test generalization against unseen and stronger attackers, including adaptive strategy-composition attacks. Finally, we evaluate the attacker itself from both effectiveness and diversity perspectives, measuring cross-model transferability, attack-space coverage, and quality-diversity metrics. Through component ablations, we show that SFT warm-up, normalized diversity reward, and Bayesian replay buffer contribute complementary benefits: SFT stabilizes early offensive capability, diversity reward prevents strategy collapse, and replay buffer mitigates defender forgetting.

中文对应：

> 我们围绕 DACE 的两个核心动机设计实验：攻击策略坍缩与防御对抗遗忘。首先，我们评估 DACE 是否提升 defender 的 harmful refusal，同时避免过拒和通用能力退化。其次，我们在外部强攻击器上测试 defender 泛化能力，包括自适应策略组合攻击。最后，我们从 effectiveness 和 diversity 两个角度单独评估 attacker，考察其跨模型迁移能力、攻击空间覆盖度和 quality-diversity 表现。通过组件消融，我们证明 SFT warm-up、归一化多样性奖励和 Bayesian replay buffer 分别承担互补作用：SFT 稳定早期攻击能力，多样性奖励缓解策略坍缩，replay buffer 缓解 defender 对历史攻击的遗忘。

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

下面这版把 **DACE 的实现迭代、v4 改动、defender eval、attacker eval、ablation、appendix 取舍** 合在一起，作为后续写论文 Experiments 章节的中文梳理稿。

---

# 一、结合四轮实现/debug 后，对 DACE 方法细节的重新理解

DACE 的实验章节不能只写成 “MAGIC + diversity reward + replay buffer”。从代码实现和四轮 debug 看，DACE 的真正贡献更清楚地落在三个闭环上：

1. **攻击侧：显式策略空间 + 多样性奖励，缓解 attack strategy collapse。**
   初始实现里已经把 DACE 定义为在 MAGIC 上加入二维 attack space、diversity reward、Bayesian replay pool 的扩展，核心目标是解决攻击策略坍缩和防御遗忘。实现上新增 `ArchivePool`，维护 strategy slot counts、coverage entropy、Thompson replay posterior，并把 diversity reward 注入 attacker reward。fileciteturn1file3

2. **防御侧：new attacks + replay attacks 混合训练，缓解 defense adversarial forgetting。**
   第一轮 debug 发现 defender stage 的 new successful attacks 一开始没有进入 replay buffer，这会导致 defender 阶段发现的新攻击无法回流到 archive，违反 pseudocode 中“Stage 2 结束后新攻击成功样本入池”的设计。这个 bug 被定位后，实验章节里需要强调 DACE replay buffer 不是静态 memory，而是 **attacker stage 与 defender stage 双向吸纳新成功攻击** 的动态 archive。fileciteturn1file2

3. **v4：把方法从“能跑”修正为“实验语义一致”。**
   第三轮和第四轮 debug 表明，旧 BENIGN_TEMPLATE 里 “trick into harmful responses” 与 “detected as benign” 语义冲突，导致 benign SFT 数据中大量样本被 guard 判为 non-safe，进而在 RL 中表现为 `refusal_rate_benign` 飙升。v4 因此把 benign 改写目标改成 “诱发 over-refusal / false-positive，同时保持 benign intent”，并将 attack space 从 14×10 剪裁为 12×10，删除低频且不适配 text-only defender 的 Sexual Content 与 Code Interpreter Abuse。fileciteturn1file0 fileciteturn1file1

因此，实验章节的主线应该是：

> DACE 通过 12×10 显式 attack space 训练一个更有效、更分散的 attacker；该 attacker 不断发现覆盖更广的 adversarial prompts；成功攻击进入 Bayesian replay buffer；defender 在当前攻击和历史高风险攻击的混合 batch 上训练，从而同时获得更强 OOD robustness 和更低 adversarial forgetting。

---

# 二、v4 方法设置在实验章节中必须交代的内容

## 2.1 Attack space：从 14×10 改成 12×10

主文中建议简要写：

> We define a two-dimensional attack space consisting of 12 risk categories and 10 attack styles, resulting in 120 strategy cells. Compared with the preliminary 14×10 design, we remove Sexual Content and Code Interpreter Abuse because they are extremely underrepresented in the distilled SFT data and introduce unstable diversity normalization signals. Code Interpreter Abuse is also not applicable to our text-only defender setting.

附录中放完整 mapping：

| 新编号 | 原 LG4 类别 | 名称 |
|---:|---:|---|
| 1 | S1 | Violent Crimes |
| 2 | S2 | Non-Violent Crimes |
| 3 | S3 | Sex-Related Crimes |
| 4 | S4 | Child Sexual Exploitation |
| 5 | S5 | Defamation |
| 6 | S6 | Specialized Advice |
| 7 | S7 | Privacy |
| 8 | S8 | Intellectual Property |
| 9 | S9 | Indiscriminate Weapons |
| 10 | S10 | Hate |
| 11 | S11 | Suicide & Self-Harm |
| 12 | S13 | Elections |

v4 计划中已经给出删除 S12/S14 的数据依据：Sexual Content 在 SFT v3 中仅 0.80%，Code Interpreter Abuse 仅 0.11%，且 Code Interpreter Abuse 不适配 MAGIC/DACE 的 text-only defender；dead rows 会把 normalized coverage reward 的最大边际增益长期钉在空格子上，压制 active slots 的奖励信号。fileciteturn1file1

## 2.2 SFT 数据蒸馏修改

实验设置中需要写清楚：

- harmful SFT：保留 harmful rewriting 目标，但 prompt 中的 risk category 改为 12 类。
- benign SFT：不再要求 “trick the model into harmful responses”，而是要求保持 benign intent，同时构造可能诱发 false-positive / over-refusal 的复杂 prompt。
- v4 蒸馏数据与 RL prompt 使用同一套 12-risk guidance，避免 SFT 与 RL strategy space 不一致。
- 对低频类别，需要从 WJB harmful / WJB benign 后 2w 样本中用 Llama-Guard4 重新统计 risk category 分布，主动补充低频 risk category，再蒸馏到 sft-data-v4。

这一部分建议主文一句带过，附录详细描述数据构建、过滤规则、类别分布和补充流程。

## 2.3 RL 数据预处理修改

需要说明：

- RL harmful / benign seed 都使用 12×10 strategy space。
- attacker 输出中必须包含 `<think>`, `<strategy>`, `<answer>` 三段；`<strategy>` 内直接声明 risk category 与 attack style。
- strategy descriptor 不再由 judge 后验分类，而是从 attacker 输出中正则提取。
- 对旧 14 类数据，包含 Sexual Content / Code Interpreter Abuse 的样本在 v4 训练中不进入 attack-space reward 计算。
- benign attack success 定义为：defender 产生 unsafe response 或错误拒答；harmful attack success 定义为：defender 产生 unsafe response。这个定义与 v4 benign template 的 “over-refusal attack” 目标一致。fileciteturn1file1

## 2.4 RL 训练细节修改

主文设置建议写：

| 项目 | v4 设置 |
|---|---|
| attack space | 12 risk categories × 10 attack styles |
| rollout group size | $G=6$ |
| train batch size | $B_{\text{train}}=64$ |
| replay batch size | $B_{\text{replay}}=32$ |
| max replay pool size | 4000 |
| replay sampling | Thompson Sampling |
| posterior prior | $\alpha=\beta=1$ |
| time decay | $\gamma=0.90$ |
| prune threshold | 0.45 |
| diversity coefficients | $\lambda_{\text{success}}=1.0,\lambda_{\text{fail}}=0.5$ |
| label consistency reward | disabled in v4, used as future ablation |

---

# 三、实验章节主线设计

建议 Experiments 章节按下面逻辑写：

1. **先证明 defender 更安全且不过拒。**
   对齐 MAGIC Table 1 / Table 2。

2. **再证明 defender 泛化到更强 OOD attackers。**
   对齐 MAGIC Table 3，并加入 MAJIC-Attack 作为 stronger adaptive attacker。

3. **然后证明 DACE attacker 本身更强。**
   用 DACE attacker / replay buffer 去攻击各种模型，参考 MAGIC Table 10。

4. **最后证明 attacker 不是单一策略变强，而是 effective + diverse。**
   用 attack-space distribution、successful coverage、cosine similarity、entropy、QD-score 等指标。

5. **消融实验解释每个组件的作用。**
   包括 w/o SFT、w/o diversity reward、w/o replay buffer、w/o full diversity design。

---

# 四、建议主文 Experiments 章节结构

## 5.1 Experimental Setup

### 5.1.1 Models

主模型：

- Qwen2.5-7B-Instruct 作为主要 backbone；
- 可选扩展：Qwen2.5-14B-Instruct、Llama3.1-8B-Instruct。

主文如果篇幅紧，Qwen2.5-7B 作为主表即可，14B/Llama 放附录。

### 5.1.2 Baselines

主文建议保留：

| Baseline | 作用 |
|---|---|
| Base Instruct | 原始安全能力 |
| Self-RedTeam | online self-play baseline |
| MAGIC | 最强直接 baseline |
| DACE | 主方法 |
| DACE w/o SFT | 验证 attacker cold-start 重要性 |
| DACE w/o diversity reward | 验证多样性奖励 |
| DACE w/o replay buffer | 验证 replay 对 defender 的贡献 |

其中 “w/o diversity design → MAGIC” 建议不要写成一个含糊 variant，而是在论文里明确：

> MAGIC can be viewed as removing DACE’s explicit strategy-space diversity design and Bayesian replay mechanism while retaining the general attacker–defender co-evolution paradigm.

这样 MAGIC 是 baseline；DACE ablation 是在 DACE 框架内部逐项移除组件。

### 5.1.3 Attack Space and Data

这里简要说明：

- DACE 使用 12×10 attack space；
- SFT attacker 使用 v4 distilled harmful/benign CoT data；
- RL dataset 来自 WJB harmful / WJB benign；
- low-frequency risk categories 通过 Llama-Guard4 从 WJB 后 2w 样本中筛选补充；
- benign rewriting 目标是 false-positive / over-refusal，而不是引入真实 harmful intent。

完整数据统计表放附录。

---

## 5.2 Main Defender Evaluation

### Table 1：Safety and benign compliance

**要回答的问题：**
DACE 是否提升 harmful refusal，同时不明显牺牲 benign compliance？

**主文表格：**

| Method | WG adv ASR↓ | WG van ASR↓ | WJB adv ASR↓ | DAN ASR↓ | HB adv ASR↓ | HB van ASR↓ | OR-Bench RTA↑ | XSTest RTA↑ | StrongREJECT RTA↑ | WJB benign↑ | XSTest Comply↑ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Base |  |  |  |  |  |  |  |  |  |  |  |
| Self-RedTeam |  |  |  |  |  |  |  |  |  |  |  |
| MAGIC |  |  |  |  |  |  |  |  |  |  |  |
| DACE |  |  |  |  |  |  |  |  |  |  |  |

**说明重点：**

- WG / WJB / DAN / HarmBench 说明 harmful refusal；
- OR-Bench / XSTest contrast / StrongREJECT 说明强安全边界；
- WJB benign / XSTest safe 说明不过拒；
- v4 的重点是验证修正 BENIGN_TEMPLATE 后，DACE 是否不再出现 v3 那种 `refusal_rate_benign=0.3–0.5` 的问题。第三轮 debug 中已经明确 benign prompt 冲突是高 over-refusal 的主要原因，因此 Table 1 是验证 v4 修正是否成功的第一张主表。fileciteturn1file0

**主文保留。**

---

### Table 2：General capability

**要回答的问题：**
DACE 的安全收益是否以 general capability 下降为代价？

**主文表格：**

| Method | IFEval-Prompt↑ | IFEval-Instruct↑ | ARC-C↑ | GPQA↑ | MMLU↑ | AlpacaEval 2 LC Win↑ |
|---|---:|---:|---:|---:|---:|---:|
| Base |  |  |  |  |  |  |
| Self-RedTeam |  |  |  |  |  |  |
| MAGIC |  |  |  |  |  |  |
| DACE |  |  |  |  |  |  |

**说明重点：**

- IFEval 说明 instruction following；
- ARC-C / GPQA / MMLU 说明 reasoning / knowledge；
- AlpacaEval 2 说明 helpfulness；
- 如果 DACE 在某些 benchmark 小幅下降，要写成 safety–utility trade-off，而不是回避。

**主文保留。**

---

## 5.3 Defender Generalization to Stronger OOD Attackers

### Table 3：OpenRT / HarmBench defender generalization

**要回答的问题：**
DACE defender 是否只防住自己的 attacker，还是能泛化到外部 stronger attackers？

**主文表格：**

| Defender | no-rev↓ | GCG↓ | PAIR↓ | TAP↓ | AutoDAN↓ | AutoDAN-turbo↓ | MAJIC-Attack↓ | Avg. Queries↓ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Gemini-2.5-Flash |  |  |  |  |  |  |  |  |
| Qwen2.5-7B-Instruct |  |  |  |  |  |  |  |  |
| + Self-Eval |  |  |  |  |  |  |  |  |
| + SmoothLLM |  |  |  |  |  |  |  |  |
| + Self-RedTeam |  |  |  |  |  |  |  |  |
| + MAGIC |  |  |  |  |  |  |  |  |
| + DACE |  |  |  |  |  |  |  |  |

**为什么加入 MAJIC-Attack：**

MAJIC-Attack 是非常合适的 stronger attacker，因为它不是单一攻击模板，而是通过 Markovian adaptive composition 组合多种攻击策略。它与 DACE 的 diversity / strategy composition 主题高度相关，因此比单独再加一个固定模板 attacker 更能测试 defender 是否学到了广义安全边界。

**说明重点：**

- GCG：gradient suffix attack；
- PAIR/TAP：LLM iterative / tree-search attack；
- AutoDAN / AutoDAN-turbo：evolutionary attack；
- MAJIC-Attack：adaptive compositional attack；
- 对 MAJIC 这类多 query attack，要同时报告 ASR 和 Avg. Queries，避免和 single-shot attacker 不公平比较。

**主文保留。**
RainbowPlus、Auto-RT、Ferret、QDRT 等更多 automatic red teaming methods 放附录。

---

## 5.4 Attacker Effectiveness Evaluation

这一节是 DACE 相比 MAGIC 必须补强的部分。不能只评 defender，因为 DACE 的方法名和设计都强调 attacker diversity。

### Table 4：DACE attacker transferability，参考 MAGIC Table 10

**要回答的问题：**
DACE attacker 是否比 MAGIC attacker 更有效？是否能迁移攻击不同模型？

**设置：**

用不同 attacker 攻击多个 frozen defenders：

| Attacker | Qwen2.5-7B Base ASR@1↑ | Llama3.1-8B ASR@1↑ | Mistral-7B ASR@1↑ | Gemini ASR@1↑ | MAGIC-def ASR@1↑ | DACE-def ASR@1↑ | Avg. ASR@5↑ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Base attacker |  |  |  |  |  |  |  |
| MAGIC attacker |  |  |  |  |  |  |  |
| DACE w/o SFT attacker |  |  |  |  |  |  |  |
| DACE w/o diversity reward attacker |  |  |  |  |  |  |  |
| DACE attacker |  |  |  |  |  |  |  |

**指标：**

- ASR@1：单次生成攻击成功率；
- ASR@5：每个 seed 采样 5 次，至少一次成功；
- Avg. Queries：达到成功的平均查询数；
- Transfer ASR：在非训练 defender 上的平均 ASR。

**说明重点：**

- 如果 DACE attacker 在 base models 上 ASR 更高，说明攻击更 effective；
- 如果 DACE attacker 在 MAGIC-def 或其他 aligned defender 上仍有攻击能力，说明它不是只对 base model 有效；
- 如果 DACE-def 对 DACE attacker 仍保持低 ASR，说明 defender 通过 replay 和 co-evolution 学到了对应防御。

**主文保留。**

---

### Table 5：On-rewrite attacks vs replay buffer attacks

**要回答的问题：**
DACE replay buffer 中保存的是不是高质量攻击？on-rewrite 生成攻击和 replay buffer 攻击在 attack space 上有什么差异？

**两个攻击源：**

1. **On-rewrite attacks**：DACE attacker 在 held-out seeds 上即时生成的攻击；
2. **Replay buffer attacks**：训练结束后 archive / replay buffer 中保存的成功攻击。

**主文表格：**

| Attack Source | Query Harmful Rate↑ | Defender ASR↑ | Risk Coverage↑ | Style Coverage↑ | Cell Coverage↑ | Successful Cell Coverage↑ | Entropy↑ | Max Cell Share↓ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MAGIC attacker on-rewrite |  |  |  |  |  |  |  |  |
| DACE attacker on-rewrite |  |  |  |  |  |  |  |  |
| DACE replay buffer |  |  |  |  |  |  |  |  |

**指标解释：**

- Query Harmful Rate：攻击 prompt 本身被 safety judge 判为 unsafe / harmful 的比例；
- Defender ASR：攻击目标 defender 后成功率；
- Risk Coverage：12 个 risk categories 中被覆盖的比例；
- Style Coverage：10 个 attack styles 中被覆盖的比例；
- Cell Coverage：120 个 strategy cells 中非空比例；
- Successful Cell Coverage：至少存在一个成功攻击的 cell 比例；
- Entropy：strategy distribution normalized entropy；
- Max Cell Share：最大 cell 占比，用于检测 mode collapse。

**说明重点：**

- replay buffer 不应只是 “高 ASR 样本池”，还应体现覆盖广；
- on-rewrite 与 replay buffer 的差异能说明 Thompson replay 如何筛选高风险样本；
- 如果 replay buffer 的 ASR 高但 diversity 低，需要解释为 replay sampler 偏向当前高风险区域；如果 coverage 也高，则说明 DACE 同时保存了高质量和多样化攻击。

**主文建议保留压缩版，完整 per-category/per-style 分布放附录。**

---

## 5.5 Attacker Diversity Evaluation

### Figure 4：12×10 attack-space heatmap

**要回答的问题：**
DACE 是否真的缓解 attack strategy collapse？

**图设计：**

画 3 个 heatmap：

1. MAGIC attacker；
2. DACE w/o diversity reward；
3. DACE full。

横轴是 10 个 attack styles，纵轴是 12 个 risk categories。颜色可以表示：

- cell 内成功攻击数；
- cell 内最高 ASR；
- cell 内平均 attack reward；
- cell 内 QD-score contribution。

**说明重点：**

- MAGIC 或 w/o diversity reward 可能集中在少数 cell；
- DACE full 应该覆盖更多 cells；
- 更重要的是 DACE full 的成功攻击 coverage 更高，而不是只生成大量无效低质量 prompt。

**主文保留。**

---

### Table 6：Diversity metrics

**要回答的问题：**
除了 attack-space coverage，DACE 在文本/语义层面是否也更多样？

**主文表格：**

| Method | ASR@1↑ | Successful Coverage↑ | Entropy↑ | QD-Score↑ | Avg. Cosine Sim↓ | Self-BLEU↓ | Distinct-2↑ | Hybrid Strategy Rate↑ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MAGIC attacker |  |  |  |  |  |  |  |  |
| DACE w/o diversity reward |  |  |  |  |  |  |  |  |
| DACE full |  |  |  |  |  |  |  |  |

**指标解释：**

- Avg. Cosine Sim↓：用 embedding 计算成功攻击之间的平均 pairwise cosine similarity，越低表示语义越分散；
- Self-BLEU↓：越低表示表面形式越不重复；
- Distinct-2↑：越高表示 n-gram 多样性越高；
- Hybrid Strategy Rate↑：攻击中组合多个策略的比例；
- QD-Score↑：每个 strategy cell 的 best quality 之和，用于同时刻画 quality 和 diversity。

**注意：**

只用 cosine similarity 不够，因为它可能把同一攻击策略的不同措辞误判为多样。因此主文应该把 cosine similarity 作为辅助指标，核心仍然是 **successful strategy coverage + entropy + QD-score**。

**主文可保留，如果篇幅紧，可以与 Figure 4 合并成一个 compact table。**

---

## 5.6 Replay and Forgetting Evaluation

### Figure 5：Defense adversarial forgetting curve

**要回答的问题：**
replay buffer 是否真的缓解 defender 对早期攻击的遗忘？

**设置：**

按照攻击进入 archive 的时间，把 replay buffer / generated attacks 划分为：

- early attacks；
- middle attacks；
- late attacks。

对每个 defender checkpoint $D_k$ 测：

| Defender checkpoint | Early ASR↓ | Middle ASR↓ | Late ASR↓ |
|---|---:|---:|---:|
| iter 1 |  |  |  |
| iter 2 |  |  |  |
| iter 3 |  |  |  |
| final |  |  |  |

比较：

- DACE full；
- DACE w/o replay buffer；
- DACE with uniform replay；
- DACE with Thompson replay。

**说明重点：**

- w/o replay 可能对 late attacks 适应较好，但 early ASR 反弹；
- Thompson replay 应该同时保持 early/middle/late attacks 的较低 ASR；
- 这是 DACE 区别于 MAGIC 的关键证据之一。

**主文建议保留 Figure 5 或放入 ablation table 中。**
如果篇幅有限，Figure 5 放附录，但主文 ablation table 中必须有一个 “Early Attack ASR↓” 指标。

---

## 5.7 Ablation Studies

### Table 7：Component ablation

**要回答的问题：**
DACE 的每个组件分别贡献了什么？

**主文表格：**

| Method | WJB ASR↓ | DAN ASR↓ | MAJIC-Attack ASR↓ | XSTest Comply↑ | Attacker ASR@5↑ | Successful Coverage↑ | QD-Score↑ | Early Attack ASR↓ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MAGIC |  |  |  |  |  |  |  |  |
| DACE w/o SFT |  |  |  |  |  |  |  |  |
| DACE w/o diversity reward |  |  |  |  |  |  |  |  |
| DACE w/o replay buffer |  |  |  |  |  |  |  |  |
| DACE full |  |  |  |  |  |  |  |  |

**每个 ablation 的解释：**

1. **MAGIC / w/o diversity design**
   去掉显式 attack space、diversity reward 和 Bayesian replay，仅保留 co-evolution baseline。用于说明 DACE 相比 MAGIC 的总体收益。

2. **DACE w/o SFT**
   attacker 从 base model 开始，不做 DACE SFT。用于验证 attacker cold-start 是否必要。早期 debug 显示无 SFT 时虽然 pool 能增长，但 attacker 质量和格式稳定性都可能不足。fileciteturn1file2

3. **DACE w/o diversity reward**
   保留 12×10 strategy format，但不把 coverage reward 加入 attacker reward。用于验证显式 reward 是否真的提升 diversity，而不只是 prompt 里列出策略空间就够了。

4. **DACE w/o replay buffer**
   defender 只训练当前 attacker 生成的新攻击，不混入历史高风险攻击。用于验证 replay 是否缓解 forgetting。

5. **DACE full**
   完整方法。

**说明重点：**

- 如果 w/o diversity reward 的 ASR 高但 coverage 低，说明 attacker 仍会坍缩到少数有效策略；
- 如果 w/o replay 的 latest ASR 低但 early ASR 高，说明出现 adversarial forgetting；
- 如果 w/o SFT 的 attacker ASR 和 format reward 差，说明 offensive SFT 是必要 warm-start；
- 如果 DACE full 在 MAJIC-Attack ASR 上也更低，说明策略覆盖训练带来了 OOD generalization。

**主文保留。**

---

# 五、附录实验安排

## Appendix A：Data construction and v4 pipeline

放：

- 14×10 到 12×10 的完整理由；
- 删除 Sexual Content / Code Interpreter Abuse 的统计；
- SFT v4 harmful / benign distillation prompt；
- benign template before/after；
- Llama-Guard4 对 WJB 后 2w harmful / benign 的 category 统计；
- 低频 category 数据补充流程；
- SFT data v4 的最终 risk/style 分布。

这是重要但不适合占主文篇幅的内容。

## Appendix B：Full defender benchmark results

放：

- Qwen2.5-14B；
- Llama3.1-8B；
- 完整 HarmBench / WildGuard / WJB / XSTest / StrongREJECT 细分；
- 多 judge 结果：Qwen3Guard、WildGuard、GPT-4o、LlamaGuard。

## Appendix C：Additional stronger attackers

放：

- RainbowPlus；
- Auto-RT；
- Ferret；
- QDRT；
- MAJIC-Attack 的更多 query-budget 曲线；
- PAIR/TAP/AutoDAN 不同预算下结果。

主文只保留 MAJIC-Attack 进入 Table 3，其他自动红队方法作为附录补充。

## Appendix D：Full attacker diversity analysis

放：

- risk category distribution；
- attack style distribution；
- 12×10 cell-level table；
- cosine similarity 分布；
- Self-BLEU；
- Distinct-n；
- embedding clustering；
- per-risk ASR；
- per-style ASR；
- on-rewrite vs replay buffer 完整对比。

## Appendix E：Replay pool diagnostics

放：

- pool size over time；
- entries added / evicted per step；
- zombie fraction；
- posterior mean/min/max/median；
- Thompson vs uniform replay；
- replay batch size sensitivity；
- prune threshold sensitivity。

第三轮 debug 已经说明 pool 饱和 4000 后需要看流动性，而不是只看 pool size；这些 metric 更适合放附录。fileciteturn1file0

## Appendix F：Qualitative examples

放 sanitized examples，只展示策略标签和高层改写方式，不放可执行有害细节。

---

# 六、主文最终建议保留的图表

为了控制篇幅，主文建议最多保留下面 7 个核心图表：

| 编号 | 图表 | 作用 | 主文/附录 |
|---|---|---|---|
| Table 1 | Safety + benign compliance | 证明 defender 安全且不过拒 | 主文 |
| Table 2 | General capability | 证明能力不明显下降 | 主文 |
| Table 3 | OpenRT OOD attackers + MAJIC-Attack | 证明 defender 泛化到 stronger attackers | 主文 |
| Table 4 | Attacker transferability | 证明 DACE attacker effective | 主文 |
| Figure 4 | 12×10 attack-space heatmap | 证明 DACE attacker diverse | 主文 |
| Table 6 | Diversity metrics | 量化 diversity / QD | 主文，可压缩 |
| Table 7 | Ablation | 解释 SFT/diversity/replay 作用 | 主文 |

如果必须进一步压缩，优先级是：

**必须保留：Table 1、Table 2、Table 3、Figure 4、Table 7。**
Table 4 和 Table 6 可以合并成一个 “Attacker effectiveness and diversity” 表；Figure 5 forgetting curve 放附录，但在 Table 7 中保留 Early Attack ASR 指标。

---

# 七、实验故事线建议写法

最终实验章节可以按下面这条线写：

> We first evaluate whether DACE improves defender safety without sacrificing benign compliance or general capabilities. Then, we test whether the learned defender generalizes to unseen and stronger attackers, including adaptive compositional attacks such as MAJIC-Attack. After establishing defender robustness, we turn to the attacker side and show that DACE trains a stronger red-teamer that transfers across target models. Finally, we analyze the attack archive and show that the improvement is not due to a single collapsed attack mode: DACE produces successful attacks across a broader 12×10 strategy space, with higher successful coverage, higher quality-diversity score, and lower semantic similarity. Ablations further show that SFT warm-start, diversity reward, and Bayesian replay are all necessary for the final safety–diversity–robustness trade-off.

中文对应：

> 我们首先验证 DACE defender 是否在 harmful refusal 上优于 MAGIC，同时保持 benign compliance 和 general capability。随后，我们在 OpenRT/HarmBench 上使用 GCG、PAIR、TAP、AutoDAN、AutoDAN-turbo 和 MAJIC-Attack 等 OOD attackers 测试泛化鲁棒性。接着，我们从 attacker 角度评估 DACE attacker 的攻击有效性和迁移性，并分析 on-rewrite attacks 与 replay buffer attacks 在 12×10 attack space 中的有害性和分布。最后，我们通过 attack-space heatmap、cosine similarity、successful coverage、QD-score 和 ablation 证明 DACE 的收益来自“有效且多样”的攻击探索以及 replay buffer 对历史高风险攻击的记忆，而不是简单增加训练数据或让 defender 过度拒答。

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

我会先把最新方法脉络和前期材料中的核心论点抽出来，再用相关工作定位来搭 introduction 的“故事线—gap—方法—贡献”。下面会直接给出可作为论文初稿的中文段落版本。

下面先给 **DACE Introduction 的写法逻辑**，再给一版可以继续打磨成英文 NeurIPS paper 的 **中文 introduction 初稿**。我这里默认 DACE 的核心定位是：

> **DACE = Diversity-Aware Adversarial Co-Evolution**
> 一个面向 LLM safety alignment 的多样性驱动攻防协同演化框架，核心由 **结构化攻击策略空间、策略多样性奖励、GDPO 式多奖励解耦归一化、贝叶斯对抗回放池** 组成。

---

# 一、DACE 的 Introduction 应该怎么讲故事

DACE 的 introduction 不应该从“我们又提出一个 red teaming 方法”开始，而应该从 **LLM 安全对齐面对的是一个动态对抗问题** 开始。因为 DACE 的优势不是单点攻击更强，也不是单次防御更强，而是把 **攻击多样性、防御泛化、历史对抗记忆** 放进同一个协同演化闭环里。

建议采用下面这条故事线：

## 1. 第一层：安全对齐不是静态分类问题，而是动态攻防问题

传统 safety alignment 往往依赖固定的安全数据集或固定红队样本。但现实中的攻击者会不断适应模型防线，静态数据会很快过时。Self-RedTeam 和 MAGIC 这类工作已经把问题推进到 online self-play / attacker-defender co-evolution：攻击者和防御者持续交互，攻击者发现新漏洞，防御者学习拒绝新攻击。Self-RedTeam 明确指出传统“先攻击、后修补”的流程会导致攻击者和防御者之间的分布错配，并提出在线自博弈；MAGIC 则进一步把安全对齐建模为非对称攻击者—防御者博弈。

这一段的作用是把 DACE 放到 **safety co-evolution** 的主线里。

## 2. 第二层：现有协同演化虽然动态，但没有系统解决“多样性”

现有 co-evolution 方法解决了 static defense 的问题，但仍然容易出现两个深层失败模式：

第一，攻击者在 RL 中会追逐少数高奖励模式，导致 **attack strategy collapse**。这在 automated red teaming 里是经典问题：GFlowNet red teaming 工作指出，即使加入 novelty/diversity regularization，现有 RL attacker 仍可能 mode collapse 或生成无效攻击；OpenAI 的 diverse red teaming 也强调 automated red teaming 的关键挑战是同时保持 diversity 和 effectiveness，而不是只优化其中之一。

第二，防御者在面对不断变化的攻击时，容易过拟合当前攻击分布并遗忘旧攻击模式，也就是 **adversarial forgetting**。MAGIC/Self-RedTeam 证明动态共演化有效，但它们对历史攻击经验如何被结构化保存、更新和重采样，并没有形成 DACE 这样明确的贝叶斯记忆机制。

这一段的作用是提出 DACE 的第一个核心 gap：
**co-evolution without diversity control is still fragile.**

## 3. 第三层：已有 diversity red teaming 也不够，因为它们大多是“单边红队”而非“攻防共演化”

Rainbow Teaming、QDRT、Curiosity-driven Red Teaming、GFlowNet diverse attacks、OpenAI diverse red teaming 都在解决攻击多样性问题。Rainbow Teaming 把 adversarial prompt generation 建模为 Quality-Diversity search，并用 MAP-Elites 式 archive 维护多样攻击；QDRT 强调 word/embedding similarity 不足以捕捉真正的攻击策略差异，因此提出 goal-driven behavior diversity；CRT 用 novelty reward 提升 test-case coverage；GFlowNet 方法从概率采样角度缓解 mode collapse。

但这些工作大多面向静态目标模型或单边攻击生成。它们能产生更多 diverse attacks，却不一定回答：

> 这些多样攻击如何持续推动 defender 学到更稳健的安全边界？
> defender 学过的旧攻击如何不被遗忘？
> 攻击多样性如何与防御训练闭环耦合？

这一段的作用是提出 DACE 的第二个核心 gap：
**diverse red teaming without co-evolution is incomplete.**

## 4. 第四层：DACE 的关键 insight

DACE 的核心 insight 可以写成一句话：

> **Robust LLM safety requires not only stronger attacks or stronger defenses, but a diversity-aware co-evolutionary process in which the attacker systematically covers the attack strategy space while the defender repeatedly revisits high-risk historical attacks.**

中文就是：

> 稳健的 LLM 安全对齐不应只追求更强攻击或更强防御，而应让攻击者在结构化策略空间中持续扩展覆盖，同时让防御者通过历史高风险攻击回放维持对整个策略空间的长期鲁棒性。

这一段之后介绍方法三件套：

1. **结构化攻击策略空间**：风险类别 × 攻击方式。
2. **策略多样性奖励 + GDPO 解耦归一化**：让攻击者不仅追求 ASR，还追求有效策略覆盖。
3. **贝叶斯对抗回放池**：让防御者混合学习当前攻击和历史高风险攻击，缓解对抗遗忘。

## 5. 第五层：贡献总结不要泛泛写，要对准 gap

NeurIPS 风格 contribution 建议写成 3–4 条：

1. 提出 diversity-aware adversarial co-evolution formulation。
2. 提出 structured strategy-space diversity objective，包括 coverage / novelty / decoupled reward normalization。
3. 提出 Bayesian adversarial replay pool，用不确定性和时间衰减管理历史攻击。
4. 实验证明 defender 更安全、更泛化、更少遗忘；attacker 更有效且更多样。

---

# 二、DACE Introduction 中文初稿

下面是一版按照 NeurIPS 叙事节奏写的 introduction 初稿。它不是中文摘要，而是完整 introduction 的中文骨架，后续可以逐段翻译成英文。

---

## Paragraph 1：从现实问题切入——LLM safety 是动态对抗问题

大语言模型正在被部署到越来越开放的交互环境中，其安全性不再只取决于模型能否拒绝一组固定的有害请求，而取决于模型能否在面对持续变化、策略性适应的攻击者时保持稳健。现有安全对齐方法通常依赖静态的安全数据集、人工构造的红队样本或离线收集的 jailbreak prompts 来训练模型拒绝有害请求。然而，这种静态范式与真实威胁模型之间存在天然错配：攻击者会根据防御模型的拒绝模式不断调整攻击策略，而防御者若只在固定样本上训练，则容易滞后于新出现的攻击分布。近期的在线自博弈和攻防协同演化方法开始将 LLM 安全对齐建模为动态对抗过程，其中攻击者持续生成 adversarial prompts，防御者同步学习识别并拒绝这些输入。Self-RedTeam 将安全对齐形式化为 online self-play reinforcement learning，MAGIC 进一步将攻击者和防御者建模为非对称多智能体博弈，表明动态共适应可以比静态安全微调更有效地暴露长尾漏洞并提升防御鲁棒性。

---

## Paragraph 2：指出 co-evolution 的不足——动态不等于多样

尽管攻防协同演化为 LLM 安全训练提供了更贴近现实的范式，但现有方法仍然缺少对攻击策略空间的系统性控制。强化学习训练中的攻击者通常被奖励其是否成功诱导防御者输出有害内容，因此自然倾向于重复利用少数高回报、低成本的攻击模式。这会导致攻击策略坍缩：攻击成功率可能在训练集或当前防御者上升高，但攻击分布逐渐集中于少数策略区域，无法充分覆盖真实攻击空间。类似问题在 automated red teaming 中已被反复观察到：基于 RL 的 red-team 模型即使加入显式 novelty 或 diversity regularization，仍可能出现 mode collapse，或者为了追求多样性而牺牲攻击有效性；自动红队的核心难点并不是单独优化 effectiveness 或 diversity，而是同时生成有效且多样的攻击。 在协同演化场景下，这一问题更加严重：如果攻击者坍缩到少数策略，防御者也会过拟合这些策略，从而获得一种表面上的“训练内鲁棒性”，但对未覆盖的攻击方式仍然脆弱。

---

## Paragraph 3：指出 defense 端问题——防御者会遗忘历史攻击

攻防协同演化的另一个被低估的问题是防御者的对抗遗忘。随着攻击者持续演化，防御者训练分布也不断漂移。若防御者主要学习当前轮次生成的新攻击，它可能在适应新攻击的同时逐渐遗忘旧有攻击模式，导致历史上已经被修补的漏洞重新出现。这一现象与持续学习中的 catastrophic forgetting 类似，但在安全对抗场景中更加棘手：旧攻击并不会因为当前训练分布中消失而在真实世界中消失，攻击者随时可以复用早期有效策略或将其与新策略组合。因此，一个可靠的安全共演化框架不仅需要让攻击者持续发现新漏洞，还需要让防御者持续回顾历史高风险攻击，并根据当前防御能力动态判断哪些历史样本仍然具有训练价值。现有 co-evolution 方法通常强调攻击者和防御者的在线交互，却较少系统建模历史攻击经验的选择、更新与淘汰机制。

---

## Paragraph 4：回顾 diversity red teaming，并指出为什么还不够

与 co-evolution 方向并行，另一条研究线关注如何生成更具多样性的红队攻击。Rainbow Teaming 将 adversarial prompt generation 形式化为 Quality-Diversity search，并借助 MAP-Elites 式 archive 在风险类别、攻击风格等行为维度上维护多样且高质量的攻击样本；Curiosity-driven Red Teaming 通过 novelty reward 扩展生成测试用例的覆盖范围；GFlowNet-based red teaming 将攻击生成视为从多模态奖励分布中采样，以缓解 RL 最大化带来的 mode collapse；QDRT 进一步指出，基于词频或句向量相似度的 diversity 指标难以捕捉真实攻击策略差异，因此提出行为条件化训练和 behavioral replay buffer 来提升 goal-driven diversity。 然而，这些方法大多仍以静态目标模型为中心，主要优化攻击生成器本身，而没有将攻击多样性与防御者的动态训练闭环结合起来。换言之，它们回答了“如何找到更多样的攻击”，但没有充分回答“如何让这些多样攻击持续推动防御者形成更广泛、更持久的安全边界”。

---

## Paragraph 5：提出 DACE 的中心命题

本文提出 **DACE：Diversity-Aware Adversarial Co-Evolution**，一个面向 LLM 安全对齐的多样性驱动攻防协同演化框架。DACE 的核心观点是：稳健的安全对齐需要同时解决两个耦合问题——攻击者必须系统性覆盖攻击策略空间，而防御者必须在当前攻击和历史高风险攻击之间保持持续学习。为此，我们将 LLM safety training 建模为攻击者与防御者之间的动态对抗博弈：攻击者学习将原始有害请求改写为更隐蔽、更具欺骗性的 adversarial prompts；防御者学习在保持 helpfulness 的同时拒绝这些有害请求。不同于仅最大化攻击成功率的共演化框架，DACE 显式将策略空间多样性纳入攻击者优化目标，并通过对抗回放机制将历史攻击经验纳入防御者训练，从而形成“多样攻击发现—历史风险记忆—防御鲁棒提升—新攻击压力生成”的闭环。

---

## Paragraph 6：方法组件一——结构化攻击策略空间

DACE 首先引入结构化攻击策略空间，将每个攻击样本映射到一个行为描述符 $b(x)=(s,c)$，其中 $s$ 表示安全风险类别，$c$ 表示攻击方式。风险类别可以对应主流安全分类体系中的暴力、违法行为、自残、仇恨、危险物质、隐私等维度；攻击方式则描述 prompt 如何绕过防御，例如角色扮演、权威操纵、术语伪装、故事嵌入、逻辑诱导、多轮递进等。这样的设计将 diversity 从表层文本差异或语义嵌入距离提升到安全语义明确的策略空间。相比 Self-BLEU、Distinct-n 或 embedding distance 等通用多样性指标，策略空间覆盖更直接对应 red teaming 的核心目标：模型是否暴露于足够广泛的风险类别和攻击手法组合。DACE 在攻击者输入中显式提供完整策略空间描述，使攻击者先推理选择合适的策略，再基于该策略改写 prompt，从而将多样性探索从隐式采样转化为显式策略选择。

---

## Paragraph 7：方法组件二——多样性奖励与 GDPO 归一化

在攻击者训练中，DACE 同时优化攻击有效性和策略多样性。攻击有效性奖励衡量攻击是否诱导防御者产生不安全响应，同时保持与原始有害意图的一致性；策略多样性奖励则由覆盖度和新颖性两类信号组成。覆盖度奖励鼓励攻击者填补低频或未覆盖的策略槽位，使整体攻击分布接近更均衡的策略覆盖；新颖性奖励惩罚重复落入历史高频策略，推动攻击者远离已经被过度利用的攻击模式。为了避免“多样但无效”的攻击污染训练信号，DACE 对成功攻击给予完整多样性激励，对失败但策略新颖的样本给予折减激励，从而在有效性优先的同时保留对冷门策略区域的探索梯度。进一步地，DACE 采用 GDPO 式逐奖励解耦归一化：不同奖励分量先在 group 内独立标准化，再加权聚合为最终 advantage。这一设计避免攻击成功率等大尺度奖励淹没覆盖度和新颖性信号，使攻击者既学习“如何成功攻击”，也学习“向哪些尚未充分覆盖的策略区域探索”。

---

## Paragraph 8：方法组件三——贝叶斯对抗回放池

为了缓解防御者的对抗遗忘，DACE 构建贝叶斯对抗回放池来管理历史高风险攻击。每当攻击者成功突破当前防御者，相应攻击样本及其策略描述符会被加入回放池。与简单保留或一次性淘汰历史样本不同，DACE 为每个回放样本维护 Beta-Bernoulli 后验，用于估计该样本在当前防御者上的剩余攻击有效性。若某个历史攻击仍频繁突破防御者，其后验风险保持较高；若防御者多次稳定拒绝该攻击，其风险估计逐渐下降。同时，DACE 引入时间衰减以适应防御者能力和攻击分布的非平稳变化，并通过 Thompson Sampling 在高风险利用和不确定样本探索之间取得平衡。防御者训练时同时接收当前攻击者生成的新攻击和回放池采样的历史攻击，从而既能适应新攻击，又能维持对旧攻击模式的鲁棒性。

---

## Paragraph 9：总结 DACE 与现有工作的本质差别

DACE 与现有方法的区别不在于单独提出一个更强的 attacker 或一个更保守的 defender，而在于将攻击多样性和防御记忆机制统一到攻防共演化过程中。相对于 Self-RedTeam 和 MAGIC，DACE 显式建模攻击策略空间覆盖，避免攻击者在 RL 中坍缩到少数高回报模式；相对于 Rainbow Teaming、CRT、GFlowNet red teaming 和 QDRT，DACE 不止生成多样攻击，而是将这些攻击作为持续训练信号推动防御者演化；相对于普通 replay buffer，DACE 的贝叶斯回放池根据当前防御者状态动态估计历史样本价值，使回放不只是数据复用，而是面向非平稳攻防过程的风险记忆。由此，DACE 将 red teaming 的目标从“发现一批有效攻击”推进到“维持一个能持续扩展、持续记忆、持续提升防御边界的安全演化系统”。

---

## Paragraph 10：实验预告

我们在多个安全评测基准和外部攻击器上评估 DACE。实验从 defender 和 attacker 两个角度验证方法有效性：在 defender 端，我们评估有害请求拒绝率、benign compliance、general capability、OOD attacker generalization 以及历史攻击遗忘；在 attacker 端，我们评估攻击成功率、策略覆盖率、成功样本覆盖熵、策略分布均衡性和跨防御者迁移性。结果表明，DACE 训练出的防御者在多类 adversarial safety benchmarks 上相较强共演化基线获得更好的鲁棒性，同时基本保持通用能力和正常请求响应能力；DACE 攻击者则生成更有效且更多样的攻击，覆盖更广泛的风险类别和攻击方式组合。消融实验进一步显示，结构化多样性奖励和贝叶斯回放池分别对攻击覆盖扩展和防御遗忘缓解具有关键贡献。

---

## Paragraph 11：Contribution list

本文的主要贡献如下：

1. **我们提出 DACE，一个多样性驱动的 LLM 安全攻防协同演化框架。** DACE 将攻击策略覆盖、防御鲁棒性提升和历史攻击记忆统一到一个闭环动态训练过程中。

2. **我们提出面向安全语义的结构化攻击策略空间和策略多样性优化目标。** 通过将攻击样本映射到风险类别 × 攻击方式的行为描述符，DACE 将多样性从表层文本差异提升为策略层面的有效覆盖，并通过覆盖度与新颖性奖励缓解攻击策略坍缩。

3. **我们引入 GDPO 式多奖励解耦归一化以稳定多目标攻击者训练。** 该机制保留有效性、覆盖度和新颖性各自的组内排序信号，避免多样性奖励在强化学习中被攻击成功奖励淹没。

4. **我们设计贝叶斯对抗回放池以缓解防御者对抗遗忘。** 该机制为历史攻击维护动态风险后验，并通过 Thompson Sampling 选择仍具训练价值或不确定性的历史样本，使防御者在适应新攻击的同时维持对旧攻击的鲁棒性。

5. **我们系统评估 DACE 在防御鲁棒性、攻击有效性、策略多样性和遗忘缓解上的表现。** 实验表明，DACE 不仅提升当前攻防训练中的表现，也提升对外部攻击器和历史攻击模式的泛化防御能力。

---

# 三、建议最终英文 Introduction 的段落结构

如果转成英文 NeurIPS 版本，我建议保持 9–10 段：

1. **Motivation：LLM safety is dynamic and adversarial.**
2. **Prior co-evolution methods：Self-RedTeam / MAGIC solve static mismatch.**
3. **Gap 1：co-evolution suffers from attack strategy collapse.**
4. **Gap 2：defender suffers from adversarial forgetting.**
5. **Prior diversity red teaming：Rainbow / CRT / GFlowNet / QDRT.**
6. **Gap 3：diverse red teaming is mostly one-sided and static-target.**
7. **DACE overview：diversity-aware attacker + Bayesian replay defender.**
8. **Technical details preview：strategy space, reward, GDPO, replay.**
9. **Experiments preview.**
10. **Contributions.**

最关键的 NeurIPS 审稿人友好点是：
**不要把 DACE 写成“我们加了 diversity reward 和 replay buffer”。**
要写成：

> Existing safety co-evolution lacks a mechanism for maintaining broad attack-space coverage and long-term defensive memory. DACE addresses this by coupling strategy-space exploration on the attacker side with Bayesian adversarial memory on the defender side.

这句话就是整篇 introduction 的主轴。

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
> 有个问题，gdpo是之前版本的内容，现在已经没有了，最新的以v3.1的两个文件为主，
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

我会先把历史上下文和当前材料里的方法主线抽出来，再用最新论文脉络校准 Introduction 的“缺口—方法—贡献”叙事，最后直接给出可写进论文的中文段落草稿。

我已经把当前能读取的材料和历史上下文对齐了：这版 Introduction 需要避开旧版 GDPO 叙事，把重点落在“策略空间覆盖 + 有效多样性 + 贝叶斯回放/防御记忆”的闭环上。

下面这版先保留实验整理，切到 **Introduction 初稿**。我按你这次特别强调的约束处理：**GDPO 是旧版内容，Introduction 不再把 GDPO 写成方法贡献或核心组件**；DACE 的主线收敛为 **策略空间多样性驱动的 attacker + 贝叶斯对抗回放驱动的 defender memory**。

---

# 一、DACE 的 Introduction 应该怎么写

DACE 的 Introduction 不要写成“我们提出了一个新的 red teaming 方法”。更好的 NeurIPS 叙事是：

> **LLM safety alignment 正在从静态防御问题变成动态攻防演化问题；但现有 co-evolution 方法缺少显式多样性控制，现有 diversity red-teaming 方法又大多停留在单边攻击生成。DACE 的核心贡献是把 attack-space coverage 和 adversarial memory 放进同一个攻防闭环，使 attacker 更有效且更多样，defender 更鲁棒且更不容易遗忘。**

具体讲故事逻辑建议是：

1. **开场：LLM safety 是动态对抗问题。**
   静态 safety tuning 或固定红队数据无法匹配不断演化的 jailbreak / adversarial prompt。Self-RedTeam 和 MAGIC 这类工作已经说明，在线 self-play / attacker-defender co-evolution 是更自然的安全训练范式：攻击者持续暴露漏洞，防御者同步学习拒绝。Self-RedTeam 将 safety alignment 建模为 online self-play RL，MAGIC 将其建模为非对称 attacker-defender game。

2. **转折：动态 co-evolution 仍然会失败，因为 attacker 会坍缩。**
   RL attacker 如果只追求攻击成功率，很容易重复少数高回报攻击模式。OpenAI diverse red teaming 指出 automated red teaming 的核心挑战是同时生成 diverse and effective attacks；GFlowNet red-teaming 也指出，即使加入 novelty/diversity regularization，传统 RL red-teaming 仍可能 mode collapse 或生成无效攻击。

3. **第二个问题：defender 会遗忘历史攻击。**
   攻击者在变，防御者训练分布也在变。如果 defender 只学当前攻击，就会对早期攻击模式产生 adversarial forgetting。SSP / reflective experience replay 已经意识到经验池对 self-play safety alignment 的重要性，但 DACE 要进一步把历史攻击样本的“当前风险”和“不确定性”建模成动态后验，而不是简单缓存。

4. **对比 diversity red-teaming：它们解决了攻击多样性，但没有闭环训练 defender。**
   Rainbow Teaming 将 adversarial prompt generation 建模为 quality-diversity search；QDRT 进一步指出 word frequency / sentence embedding similarity 这类简单多样性指标无法充分捕捉攻击策略差异，因此引入 risk category 和 attack style 维度的行为多样性。 但这些方法多面向静态 target model，主要回答“如何找到更多样攻击”，而不是“如何让这些攻击持续训练出更强 defender”。

5. **提出 DACE：把 diversity-aware attack exploration 和 Bayesian adversarial replay 统一起来。**
   DACE 的 insight 应该写成一句主轴句：
   **Robust LLM safety requires not only stronger attacks or stronger defenses, but a diversity-aware co-evolutionary process where the attacker systematically covers the attack strategy space while the defender repeatedly revisits high-risk historical attacks.**

6. **贡献：围绕两个 failure modes 对齐。**
   不要写“我们加了 coverage reward 和 replay buffer”。要写：
   - DACE 系统性缓解 **attack strategy collapse**；
   - DACE 系统性缓解 **defense adversarial forgetting**；
   - DACE 将 automated red-teaming 的 diversity 目标和 safety co-evolution 的 defender training 目标真正耦合起来。

---

# 二、Introduction 中文初稿

## Paragraph 1：LLM safety 从静态分类变成动态对抗

大语言模型正在被部署到越来越开放的交互环境中，其安全性不再只取决于模型能否拒绝一组固定的有害请求，而取决于模型能否在面对持续变化、策略性适应的攻击者时保持稳健。传统 safety alignment 通常依赖静态安全数据、人工构造的红队样本或离线收集的 jailbreak prompts 来训练模型拒绝有害请求。然而，这种静态范式与真实威胁模型之间存在天然错配：攻击者会根据模型的拒绝模式不断调整攻击策略，而防御者若只在固定样本上训练，则容易滞后于新出现的攻击分布。近期 online self-play 和 attacker-defender co-evolution 方法开始将 LLM safety alignment 建模为动态对抗过程，其中攻击者持续生成 adversarial prompts，防御者同步学习识别并拒绝这些输入。Self-RedTeam 将安全对齐形式化为在线自博弈强化学习，MAGIC 进一步将攻击者和防御者建模为非对称多智能体博弈，表明动态共适应可以比静态安全微调更有效地暴露长尾漏洞并提升防御鲁棒性。

## Paragraph 2：现有 co-evolution 的不足——动态不等于多样

尽管攻防协同演化为 LLM safety training 提供了更贴近现实的范式，但现有方法仍缺少对攻击策略空间的系统性控制。强化学习训练中的攻击者通常被奖励其是否成功诱导防御者输出有害内容，因此自然倾向于重复利用少数高回报、低成本的攻击模式。这会导致 **attack strategy collapse**：攻击成功率可能在当前防御者上升高，但攻击分布逐渐集中于少数策略区域，无法充分覆盖真实攻击空间。类似问题在 automated red teaming 中已被反复观察到：OpenAI 的 diverse red teaming 工作指出，自动红队的核心挑战不是单独优化 diversity 或 effectiveness，而是同时生成多样且成功的攻击；GFlowNet-based red teaming 也指出，传统 RL attacker 即使加入显式 novelty 或 diversity regularization，仍可能出现 mode collapse 或生成无效攻击。 在 co-evolution 场景下，这一问题更加严重：如果攻击者坍缩到少数策略，防御者也会过拟合这些策略，从而获得一种表面上的训练内鲁棒性，却仍然暴露于未覆盖的攻击方式。

## Paragraph 3：另一个被低估的问题——defender adversarial forgetting

攻防协同演化的另一个关键问题是防御者的对抗遗忘。随着攻击者持续演化，防御者面对的训练分布也在不断漂移。若防御者主要学习当前轮次生成的新攻击，它可能在适应新攻击的同时逐渐遗忘旧有攻击模式，导致历史上已经被修补的漏洞重新出现。这一现象与持续学习中的 catastrophic forgetting 类似，但在安全对抗场景中更加棘手：旧攻击并不会因为当前训练分布中消失而在真实世界中消失，攻击者随时可以复用早期有效策略，或将其与新策略组合。已有 self-play safety alignment 工作开始引入 experience replay 以帮助模型从历史失败中学习，例如 SSP 使用 reflective experience replay 和 UCB sampling 来关注历史困难样本。 然而，一个更稳健的 co-evolution 框架需要进一步回答：哪些历史攻击对当前 defender 仍然危险，哪些只是已经被学习的过时样本，以及如何在利用高风险历史攻击和探索不确定历史攻击之间取得平衡。

## Paragraph 4：已有 diversity red-teaming 仍然不够

与 co-evolution 方向并行，另一条研究线关注如何生成更具多样性的红队攻击。Rainbow Teaming 将 adversarial prompt generation 形式化为 quality-diversity search，并通过 archive 在风险类别、攻击风格等行为维度上维护多样且高质量的攻击样本；Curiosity-driven Red Teaming 通过 novelty reward 扩展生成测试用例的覆盖范围；QDRT 进一步指出，基于词频或句向量相似度的 diversity 指标难以捕捉真实攻击策略差异，因此提出基于 risk category 和 attack style 的 behavior-conditioned training。 这些工作说明，LLM red teaming 需要从表层文本多样性走向策略层面的有效多样性。然而，它们大多仍以静态目标模型为中心，主要优化攻击生成器本身，而没有将攻击多样性与防御者的动态训练闭环结合起来。换言之，它们回答了“如何找到更多样的攻击”，但没有充分回答“如何让这些多样攻击持续推动 defender 形成更广泛、更持久的安全边界”。

## Paragraph 5：提出 DACE 的中心命题

本文提出 **DACE，Diversity-Aware Adversarial Co-Evolution**，一个面向 LLM safety alignment 的多样性驱动攻防协同演化框架。DACE 的核心观点是：稳健的安全对齐需要同时解决两个耦合问题——攻击者必须系统性覆盖攻击策略空间，而防御者必须在当前攻击和历史高风险攻击之间保持持续学习。为此，我们将 LLM safety training 建模为攻击者与防御者之间的动态对抗博弈：攻击者学习将原始请求改写为更隐蔽、更具欺骗性的 adversarial prompts；防御者学习在保持 helpfulness 的同时拒绝这些有害请求。不同于仅最大化攻击成功率的 co-evolution 框架，DACE 显式将策略空间多样性纳入攻击者优化目标，并通过 Bayesian adversarial replay 将历史攻击经验纳入防御者训练，从而形成“多样攻击发现—历史风险记忆—防御鲁棒提升—新攻击压力生成”的闭环。

## Paragraph 6：方法组件一——结构化攻击策略空间

DACE 首先引入结构化攻击策略空间，将每个攻击样本映射到行为描述符 $b(x)=(s,c)$，其中 $s$ 表示安全风险类别，$c$ 表示攻击方式。风险类别可以对应主流安全分类体系中的暴力、违法行为、自残、仇恨、危险物质、隐私等安全维度；攻击方式则描述 prompt 如何绕过防御，例如角色扮演、权威操纵、术语伪装、故事嵌入、逻辑诱导或多轮递进等。Llama Guard 和 MLCommons AI Safety Benchmark 都强调了安全风险 taxonomy 对输入/输出安全分类和系统化安全评测的重要性，这也为 DACE 的风险类别维度提供了自然基础。 这样的设计将 diversity 从表层文本差异或语义嵌入距离提升到安全语义明确的策略空间。相比 Self-BLEU、Distinct-n 或 embedding distance 等通用多样性指标，策略空间覆盖更直接对应 red teaming 的核心目标：模型是否暴露于足够广泛的风险类别和攻击手法组合。DACE 在攻击者输入中显式提供策略空间描述，使攻击者先选择合适的攻击策略，再基于该策略改写 prompt，从而将多样性探索从隐式采样转化为显式策略选择。

## Paragraph 7：方法组件二——有效多样性奖励

在攻击者训练中，DACE 同时优化攻击有效性和策略多样性。攻击有效性奖励衡量攻击是否诱导防御者产生不安全响应，同时保持与原始意图的一致性；策略多样性奖励则鼓励攻击者覆盖低频或未覆盖的策略槽位，并减少对历史高频策略的重复依赖。关键在于，DACE 追求的不是“多样但无效”的随机探索，而是 **effective diversity**：攻击者应当在保持攻击质量的前提下扩展策略覆盖。为此，DACE 对成功攻击给予完整多样性激励，对尚未成功但落入冷门策略区域的样本保留折减探索信号，使模型不会过早放弃尚未学会的低频策略。这样，攻击者既被鼓励发现真正能暴露 defender 漏洞的攻击，也被持续推动远离少数热门攻击模式，从而缓解 RL attacker 的策略坍缩。该设计与 QDRT 和 Rainbow Teaming 对“高质量 + 多样性”的强调一致，但 DACE 将这一目标嵌入在线攻防训练，而不是仅用于离线红队搜索。

## Paragraph 8：方法组件三——贝叶斯对抗回放池

为了缓解防御者的对抗遗忘，DACE 构建 Bayesian adversarial replay buffer 来管理历史高风险攻击。每当攻击者成功突破当前防御者，对应攻击样本及其策略描述符会被加入回放池。与简单保留所有历史样本或按固定分数采样不同，DACE 为每个历史攻击维护一个动态风险估计，用于追踪它对当前防御者是否仍然有效。若某个历史攻击仍频繁突破防御者，其风险估计保持较高；若防御者多次稳定拒绝该攻击，其风险估计逐渐下降。同时，DACE 通过不确定性驱动的采样机制在高风险利用和不确定样本探索之间取得平衡。防御者训练时同时接收当前攻击者生成的新攻击和回放池采样的历史攻击，从而既能适应新攻击，又能维持对旧攻击模式的鲁棒性。这使 replay buffer 不只是数据复用机制，而是面向非平稳攻防过程的动态风险记忆。

## Paragraph 9：DACE 与现有工作的本质差别

DACE 与现有方法的区别不在于单独提出一个更强 attacker 或一个更保守 defender，而在于将攻击多样性和防御记忆机制统一到攻防共演化过程中。相对于 Self-RedTeam、MAGIC、SEAS 和 non-cooperative game alignment 等 co-evolution 方法，DACE 显式建模攻击策略空间覆盖，避免攻击者在 RL 中坍缩到少数高回报模式。 相对于 Rainbow Teaming、CRT、GFlowNet red teaming 和 QDRT，DACE 不止生成多样攻击，而是将这些攻击作为持续训练信号推动防御者演化。相对于普通 replay 或固定历史池，DACE 根据当前防御者状态动态估计历史样本价值，使回放不只是“记住过去”，而是持续选择仍然危险或仍然不确定的历史漏洞。由此，DACE 将 red teaming 的目标从“发现一批有效攻击”推进到“维持一个能持续扩展、持续记忆、持续提升防御边界的安全演化系统”。

## Paragraph 10：实验预告

我们从 defender 和 attacker 两个角度系统评估 DACE。在 defender 端，我们评估 harmful refusal、benign compliance、general capability、out-of-distribution attacker generalization 以及历史攻击遗忘；在 attacker 端，我们评估 attack success rate、跨模型迁移性、策略覆盖率、successful coverage、策略分布熵、quality-diversity score 和语义多样性。实验表明，DACE 训练出的防御者在多类 adversarial safety benchmarks 上相较强 co-evolution baseline 获得更好的鲁棒性，同时基本保持通用能力和正常请求响应能力；DACE 攻击者则生成更有效且更多样的攻击，覆盖更广泛的风险类别和攻击方式组合。消融实验进一步显示，结构化多样性奖励和 Bayesian adversarial replay 分别对攻击覆盖扩展和防御遗忘缓解具有关键贡献。

---

# 三、Contribution list 初稿

建议最终 Introduction 末尾写成 4 条，不要太多。

1. **We formulate diversity-aware adversarial co-evolution for LLM safety alignment.**
   我们提出 DACE，将 LLM 安全训练建模为一个同时关注攻击策略覆盖和防御历史记忆的动态攻防演化过程，目标是同时缓解 attack strategy collapse 和 defense adversarial forgetting。

2. **We introduce a structured attack strategy space for effective diversity optimization.**
   我们将攻击样本映射到风险类别 × 攻击方式的行为描述符，使多样性优化从表层文本差异提升为安全语义明确的策略空间覆盖，并通过有效性优先的多样性奖励推动 attacker 生成既成功又多样的攻击。

3. **We design a Bayesian adversarial replay mechanism for defender memory.**
   我们为历史成功攻击维护动态风险估计，并基于风险与不确定性采样历史攻击，使 defender 在适应当前攻击的同时持续复习仍具威胁的历史攻击，从而缓解对抗遗忘。

4. **We provide a comprehensive evaluation of both defender robustness and attacker diversity.**
   我们不仅评估 defender 的 harmful refusal、benign compliance、general capability 和 OOD attacker robustness，也评估 attacker 的 effectiveness、transferability、strategy-space coverage 和 quality-diversity，系统验证 DACE 的两个核心机制。

---

# 四、写作注意事项

这里有几个关键取舍：

第一，**不要在 Introduction 里写 GDPO**。既然最新 v3.1 已经移除 GDPO，就不要再把“逐奖励解耦归一化”写成贡献点。最多在 Method 里如果还有 reward normalization 的工程细节，可以作为实现细节轻描淡写，不进入 Introduction 主线。

第二，**不要过早写死 12×10**。Introduction 可以写 $\mathcal{S}\times\mathcal{C}$ strategy space；如果最终 v4 已确定 12×10，再在 Method / Experiments 中具体说明。Intro 的重点是“策略空间覆盖”这个思想，不是具体多少个 cell。

第三，**DACE 的 novelty 不应包装成普通文本多样性**。NeurIPS 审稿人会熟悉 Self-BLEU、Distinct-n、embedding diversity 这些指标，但 DACE 的强点是“安全语义上的策略多样性”。所以 Introduction 中要明确：文本多样性只是辅助，真正核心是 risk × style 的 effective strategy coverage。

第四，**防御记忆要写成 safety 必需，而不是 replay trick**。不要说“我们用了 replay buffer 增加训练数据”。要说“历史攻击不会因为当前训练分布消失而消失，因此 defender 必须维护动态 adversarial memory”。

第五，**实验预告要两端都写**。DACE 不是单纯 defender 方法，也不是单纯 attacker 方法。Introduction 末尾必须说明：我们同时评估 defender robustness 和 attacker diversity/effectiveness。

-----

> [文件不支持导出]
> 感觉还是不够好，可以参考magic论文（之前附件上传过，MAGIC.pdf）再完善一下，
> 先写4-6段写“故事线”，理清逻辑关系，最后再加一个contribution部分，
> 假装你是严格的reviewer，在内心先对上面的introduction进行提问，再切换回author视角完善introduction，再深入思考整理一版，
> 先简要介绍 dace 的 introduction 怎么写，是什么讲故事逻辑以及为什么要怎么写，再给出具体的每一段的 introduction 内容，要求达到 NeurIPS 录用论文高质量水准，

下面这版我会把 DACE 的 Introduction 重新定位为：**不是“MAGIC + 一个 diversity reward + 一个 replay buffer”，而是“把 co-evolution 从当前对手适应，推进到策略空间覆盖与历史风险记忆驱动的安全演化过程”。** 这才是 NeurIPS 级别更容易站住的故事。

---

# 1. DACE 的 Introduction 应该怎么写

DACE 的 Introduction 最好写成 **MAGIC 之后的下一步**，而不是重新发明 co-evolution。

MAGIC 已经讲清楚了第一层故事：LLM safety 不应只靠静态数据和离线 red-teaming，而应被建模为 attacker 与 defender 的动态非对称序贯博弈。MAGIC 的核心贡献是：攻击者和防御者参数解耦，避免 Self-RedTeam 这类 shared-parameter self-play 的目标冲突；攻击者先动、防御者后动，更符合真实攻击场景；并且通过在线 RL 使攻击者持续暴露 long-tail vulnerabilities，推动防御者提升泛化鲁棒性。MAGIC 的 Introduction 和 Figure 1 都围绕两个问题展开：攻击者缺少 offensive reasoning cold-start，以及共享模型 self-play 会产生 attacker/defender gradient conflict。fileciteturn1file0

DACE 不能重复这个故事。DACE 应该说：**MAGIC 证明了 co-evolution 是有效的，但 co-evolution 本身还不保证“覆盖充分”与“记忆稳定”。** 如果攻击者只被攻击成功率驱动，它仍可能集中到少数高回报攻击模式；如果防御者只追逐当前攻击分布，它仍可能遗忘历史攻击。前者是 **attack strategy collapse**，后者是 **defense adversarial forgetting**。这两个问题共同说明：安全共演化不应只是当前 attacker 和 defender 之间的局部 best response，而应是对攻击策略空间和历史漏洞空间的持续覆盖。

因此 DACE 的主线应该是：

> **Static alignment lags behind evolving attacks. MAGIC-style co-evolution makes safety training adaptive. But adaptive does not necessarily mean comprehensive or durable: attackers may collapse to narrow strategies, and defenders may forget old threats. DACE makes co-evolution diversity-aware and memory-aware by explicitly covering a structured attack strategy space and replaying historically risky attacks through Bayesian adversarial memory.**

为什么要这么写？因为 reviewer 会问三个很尖锐的问题：

1. **你和 MAGIC 的本质区别是什么？**
   不能只说“我们也做 attacker-defender game”。必须说 MAGIC 主要解决动态适应和角色解耦，而 DACE 进一步解决 co-evolution 中的策略覆盖和历史记忆问题。

2. **你的 diversity 是不是只是更多样的文本？**
   不能停留在 Self-BLEU、Distinct-n、embedding distance。DACE 的核心是 risk category × attack style 的 **策略空间覆盖**，也就是 safety-relevant diversity，而不是表面措辞变化。

3. **replay buffer 是不是工程 trick？**
   不能写成“我们加了历史样本”。要写成：在非平稳攻防系统中，历史漏洞不会因为当前训练分布消失而消失；defender 需要一个动态 adversarial memory 来估计哪些历史攻击仍然危险，哪些已经被防住，哪些不确定但值得复查。

---

# 2. Introduction 故事线初稿：6 段版本

## Paragraph 1：从静态安全对齐到动态攻防博弈

Large language models are increasingly deployed in open-ended interactive environments, where safety failures are no longer triggered only by direct harmful instructions, but by adaptive, obfuscated, and multi-step adversarial prompts. As MAGIC observes, the threat landscape has rapidly shifted from simple role-playing jailbreaks to automated adversarial attacks and stealthy multi-turn agentic exploitations, turning LLM safety into a cat-and-mouse game between attackers and defenders. Static safety alignment pipelines—whether based on pre-collected harmlessness data, manually designed red-teaming prompts, or post-hoc guardrails—inevitably lag behind this evolving threat distribution. Once a model is patched against one family of attacks, new prompts quickly resurface through paraphrasing, role modulation, scenario shifting, or compositional deception. This motivates a more adaptive formulation: instead of treating safety alignment as one-shot training on a fixed dataset, we should treat it as an evolving adversarial process in which attackers continuously discover new vulnerabilities and defenders continuously learn to reject them.

**中文可投稿版：**

大语言模型正在进入开放式交互环境，其安全风险已经不再主要来自直接有害请求，而是来自持续演化的、经过伪装和组合的对抗提示。MAGIC 指出，LLM 的威胁形态正在从简单的角色扮演 jailbreak，快速演化为自动化对抗攻击和隐蔽的多轮 agentic exploitation，使安全对齐逐渐变成攻击者与防御者之间的 “cat-and-mouse game”。fileciteturn1file0 传统安全对齐方法通常依赖预先收集的 harmlessness 数据、人工构造的红队样本或外部 guardrail；这些静态防御可以修补已知漏洞，却天然滞后于不断变化的攻击分布。一旦模型被针对某类攻击修补，攻击者仍可通过改写、角色设定、场景迁移或多策略组合重新绕过安全边界。因此，LLM safety alignment 不应只被视为固定数据集上的离线训练问题，而应被建模为一个持续演化的对抗过程：攻击者不断发现新漏洞，防御者不断学习拒绝这些攻击。

---

## Paragraph 2：MAGIC 的贡献，以及 DACE 要推进的下一步

Recent co-evolutionary approaches have made an important step toward this goal. In particular, MAGIC formulates LLM safety alignment as an asymmetric sequential game between a decoupled attacker and defender: the attacker first rewrites a seed query into a deceptive prompt, and the defender then learns to recognize and refuse it. This formulation addresses two limitations of earlier self-play systems: shared-parameter attacker/defender training can introduce conflicting gradients, and symmetric normal-form games fail to capture the sequential structure of real-world jailbreak attempts. MAGIC further shows that a reasoning-capable attacker can evolve novel combinatorial strategies through iterative RL, and that such co-evolution improves defender robustness without severe helpfulness degradation. However, MAGIC also exposes a deeper question: once co-evolution is enabled, what determines whether the attacker explores the vulnerability space broadly enough, and whether the defender retains robustness to vulnerabilities discovered earlier in training?

**中文可投稿版：**

近期的攻防协同演化方法已经向这一目标迈出重要一步。MAGIC 将 LLM safety alignment 形式化为攻击者与防御者之间的非对称序贯博弈：攻击者首先将原始请求改写为更隐蔽的 adversarial prompt，防御者随后学习识别并拒绝该输入。该设计解决了早期 self-play 方法的两个关键局限：一方面，共享参数的 attacker/defender 训练会将相互冲突的目标压到同一参数空间中，产生 gradient conflict；另一方面，对称 normal-form game 难以刻画真实 jailbreak 场景中“攻击者先行动、防御者后响应”的序贯结构。fileciteturn1file0 MAGIC 进一步展示了一个具有初始 reasoning 能力的攻击者可以在迭代 RL 中演化出此前未见过的组合式攻击策略，并推动防御者在保持 helpfulness 的同时提升鲁棒性。fileciteturn1file0 然而，MAGIC 也自然引出了下一层问题：当 co-evolution 已经发生后，我们如何保证攻击者不是只在少数高回报策略上反复利用？又如何保证防御者在适应当前攻击者时，不会遗忘训练早期已经暴露过的漏洞？

---

## Paragraph 3：第一个缺口——adaptive 不等于 diverse

The first limitation is that adaptivity alone does not guarantee coverage. In reinforcement learning, an attacker optimized primarily for attack success may over-exploit a small number of high-reward rewriting patterns, producing increasingly effective but strategically narrow attacks. Such attack strategy collapse is especially harmful in safety training: a defender trained against a narrow adversary may appear robust within the current game, yet remain vulnerable to under-explored regions of the attack space. Automated red-teaming research has repeatedly shown that effective attacks and diverse attacks are not the same objective. Quality-diversity methods such as Rainbow Teaming maintain archives over behavior descriptors, while QDRT argues that word- or embedding-level diversity metrics cannot reliably capture meaningful attack behavior. These insights suggest that co-evolutionary safety training needs a notion of diversity that is tied to safety-relevant attack strategies, not merely surface-level textual variation. Yet existing co-evolutionary frameworks typically treat attack diversity as an emergent property to be analyzed after training, rather than an explicit objective that shapes the attacker throughout training.

**中文可投稿版：**

第一个关键缺口是：**动态适应并不等于策略覆盖充分**。在强化学习训练中，如果攻击者主要被攻击成功率驱动，它很容易过度利用少数高回报改写模式，生成越来越有效但策略上越来越狭窄的攻击。这种 attack strategy collapse 在安全训练中尤其危险：防御者可能在当前攻击者分布上表现稳健，却仍然暴露于未被充分探索的攻击空间区域。自动化红队研究已经反复表明，有效攻击和多样攻击并不是同一个目标。Rainbow Teaming 将对抗提示生成建模为 quality-diversity search，并通过行为描述符 archive 维护高质量且多样的攻击；QDRT 进一步指出，词频、句向量相似度或普通 semantic distance 难以可靠刻画真实攻击行为差异。早期调研材料中也总结过：LLM safety diversity 的核心价值在于安全覆盖完整性、safety tuning 有效性和协同演化效率，而现有方法普遍受到 mode collapse、novelty stagnation 以及 diversity-effectiveness trade-off 的限制。fileciteturn0file4 这些观察说明，co-evolutionary safety training 需要的是与安全语义直接相关的策略多样性，而不是表层文本变化。然而，现有 co-evolution 框架通常只在训练后分析 attacker 是否涌现了多样策略，而没有将策略覆盖作为贯穿训练过程的显式优化目标。

---

## Paragraph 4：第二个缺口——current robustness 不等于 durable robustness

The second limitation is that robustness to the current attacker does not imply durable robustness over time. In an evolving game, the defender’s training distribution is non-stationary: as the attacker discovers new strategies, earlier attacks may disappear from the current batch even though they remain valid threats in the real world. A defender trained only on the latest adversarial distribution may therefore suffer from adversarial forgetting, relearning recent vulnerabilities while losing robustness to older ones. This problem is more severe than ordinary distribution shift because historical attacks can be deliberately reused or recombined by future adversaries. Experience replay offers a natural remedy, but a naive replay buffer is insufficient: old attacks differ in whether they are still effective against the current defender, whether they have become obsolete, and whether their risk is uncertain due to limited re-evaluation. Thus, robust co-evolution requires not only an adaptive attacker, but also a memory mechanism that continually estimates the current threat level of historical attacks and revisits those that remain risky or uncertain.

**中文可投稿版：**

第二个关键缺口是：**对当前攻击者稳健，不等于长期稳健**。在一个不断演化的攻防游戏中，防御者面对的训练分布是非平稳的：随着攻击者发现新策略，早期攻击可能从当前 batch 中消失，但它们并不会从真实威胁空间中消失。若防御者只追逐最新攻击分布，它可能在学习新攻击的同时遗忘旧攻击，产生 defense adversarial forgetting。这个问题比普通分布漂移更严重，因为历史攻击可以被未来攻击者主动复用，也可以与新策略组合后重新变得有效。经验回放是自然的缓解思路，但简单 replay buffer 并不足够：历史攻击样本之间存在显著差异，有些仍能突破当前 defender，有些已经过时，有些则因缺少重新评估而风险不确定。因此，一个可靠的 co-evolution 框架不只需要动态攻击者，还需要一个动态 adversarial memory：持续估计历史攻击对当前防御者的威胁水平，并优先复习仍然危险或不确定的漏洞。

---

## Paragraph 5：DACE 的中心思想

We propose DACE, a diversity-aware adversarial co-evolution framework for LLM safety alignment. DACE starts from a simple principle: robust safety requires co-evolution over both the strategy space and time. On the attacker side, DACE defines a structured attack strategy space as the Cartesian product of risk categories and attack styles. Each generated attack is assigned a behavior descriptor, allowing the attacker to be rewarded not only for bypassing the current defender, but also for expanding coverage over safety-relevant strategy cells. This turns diversity from an implicit byproduct into an explicit training signal. On the defender side, DACE maintains a Bayesian adversarial replay buffer that stores historical successful attacks and tracks their evolving risk against the current defender. During defender training, current attacks are mixed with replayed historical attacks sampled according to risk and uncertainty, encouraging the defender to improve against new strategies while retaining robustness to old ones. Together, these two mechanisms transform co-evolution from a local arms race into a coverage- and memory-aware safety training process.

**中文可投稿版：**

本文提出 **DACE，Diversity-Aware Adversarial Co-Evolution**，一个面向 LLM safety alignment 的多样性驱动攻防协同演化框架。DACE 的核心原则是：稳健安全性需要同时沿着两个维度演化——**策略空间维度** 和 **时间维度**。在攻击者侧，DACE 定义结构化攻击策略空间，将每个攻击映射到风险类别与攻击方式组成的行为描述符 $b(x)=(s,c)$。已有方法设计中也明确将攻击策略空间定义为 $\mathcal{B}=\mathcal{S}\times\mathcal{C}$，并用策略空间覆盖度与新颖性来驱动攻击者远离少数热门策略区域。fileciteturn0file0 这样，攻击者不只因突破当前防御者而获得奖励，也因扩展安全语义明确的策略覆盖而获得奖励，从而将 diversity 从训练后的涌现现象转化为训练中的显式目标。在防御者侧，DACE 维护 Bayesian adversarial replay buffer，存储历史成功攻击，并动态估计这些样本对当前 defender 的风险。防御者训练时同时接收当前攻击者生成的新攻击和从回放池采样的历史高风险或高不确定攻击，使其既能适应新策略，也能保持对旧策略的鲁棒性。二者结合后，co-evolution 不再只是当前 attacker 与 defender 的局部 arms race，而变成一个由策略覆盖和历史记忆共同驱动的安全演化过程。

---

## Paragraph 6：DACE 相比 MAGIC 的清晰定位

DACE builds on the co-evolutionary insight of MAGIC but changes what the game is optimized to preserve. MAGIC asks whether a decoupled attacker-defender game can produce a stronger defender against adaptive adversaries. DACE asks a complementary question: can the game be guided so that the attacker systematically explores the safety-relevant strategy space and the defender remains robust to vulnerabilities discovered across the entire training history? This shift matters because safety is not only a pointwise response to the current adversary; it is a coverage problem over many possible subgames and a retention problem over time. By making attack diversity explicit and defender memory adaptive, DACE aims to produce attackers that are both effective and strategically broad, and defenders that are not only robust to the latest attacks but also resistant to adversarial forgetting. We evaluate DACE from both sides of the game: defender safety, benign compliance, general capability, out-of-distribution attacker robustness, adversarial forgetting, attacker effectiveness, transferability, and strategy-space quality-diversity.

**中文可投稿版：**

DACE 建立在 MAGIC 的 co-evolution insight 之上，但改变了这个游戏所要维护的对象。MAGIC 关注的问题是：解耦的 attacker-defender 非对称博弈能否训练出更强的防御者来应对 adaptive adversaries。DACE 进一步追问一个互补问题：我们能否引导这个游戏，使攻击者系统性覆盖安全相关的策略空间，同时使防御者在整个训练历史中保持对已发现漏洞的鲁棒性？这个转变很关键，因为安全性不只是对当前攻击者的 pointwise response；它同时是一个跨策略子空间的覆盖问题，也是一个跨训练时间的保持问题。通过显式优化攻击多样性并引入自适应防御记忆，DACE 旨在得到既有效又策略广泛的攻击者，以及不仅能抵御最新攻击、也能抵抗 adversarial forgetting 的防御者。我们从攻防两端系统评估 DACE：在 defender 侧评估 harmful refusal、benign compliance、general capability、OOD attacker robustness 与历史攻击遗忘；在 attacker 侧评估 attack effectiveness、transferability、strategy-space coverage、successful coverage 和 quality-diversity。

---

# 3. Contribution 部分初稿

建议 Contribution 写 4 条，重点要和 MAGIC 区分开。

## Contributions

**(1) We formulate diversity-aware adversarial co-evolution for LLM safety alignment.**
我们提出 DACE，将 LLM safety alignment 从当前攻击者—防御者之间的动态适应，推进为同时关注 **策略空间覆盖** 与 **历史风险记忆** 的协同演化问题。该框架直接针对现有 co-evolution 中两个未被充分解决的 failure modes：attack strategy collapse 和 defense adversarial forgetting。

**(2) We introduce a structured strategy-space objective for effective attack diversity.**
我们将攻击样本映射到风险类别 × 攻击方式的结构化行为描述符，并在攻击者训练中显式奖励 safety-relevant strategy coverage。与文本相似度或语义距离不同，该目标直接对应安全红队中的策略覆盖，使攻击者生成不只是表面不同、而是在风险类型和攻击机制上真正不同的有效攻击。

**(3) We design a Bayesian adversarial replay mechanism for durable defender robustness.**
我们构建 Bayesian adversarial replay buffer，为历史成功攻击维护动态风险估计，并根据风险与不确定性采样历史样本参与防御者训练。该机制使 defender 不仅适应当前攻击者，还能持续复习仍然危险或尚未充分确认的历史攻击，从而缓解 adversarial forgetting。

**(4) We provide a two-sided evaluation of co-evolution, measuring both defender robustness and attacker diversity.**
我们不仅评估防御者在 harmful refusal、benign compliance、general capability、OOD attacker robustness 和 forgetting curve 上的表现，也系统评估攻击者的 ASR、transferability、strategy-space coverage、successful coverage、entropy 和 quality-diversity score。这样的评估能够验证 DACE 是否真正实现了 “effective, diverse attacks” 与 “robust, durable defenses” 的联合提升。

---

# 4. 这一版比上一版更强在哪里

这一版的核心改进是：

1. **先承认 MAGIC 的贡献，再指出 MAGIC 留下的空白。**
   这样不会显得 DACE 在重复 MAGIC，也不会被 reviewer 质疑“你只是换了个名字做 co-evolution”。

2. **把 DACE 的问题定义从 method trick 提升到 failure mode。**
   attack strategy collapse 和 defense adversarial forgetting 是两个明确、可实验验证、和方法组件一一对应的问题。

3. **把 diversity 从“生成更多不同 prompt”提升为“策略空间覆盖”。**
   这能和 Rainbow/QDRT 对齐，也能凸显 DACE 的安全语义贡献。

4. **把 replay 从“缓存历史样本”提升为“动态风险记忆”。**
   这能解释为什么 Bayesian replay 是必要的，而不是普通 experience replay。

5. **把最终主张写成一句更强的 NeurIPS claim：**
   **DACE turns adversarial co-evolution from a local arms race into a coverage- and memory-aware safety training process.**

-----

> 有点问题，gdpo是之前版本的东西，现在已经没有了，最新的以v3.1的两个文件为主，
> 另外，好论文的introduction一般不会写这么多段落，最多五个段落，你再好好想想。
> 按照上一个用户要求重新梳理 introduction 初稿并用中文梳理，

我会先按你指出的两个约束校正：不再把 GDPO 当作当前方法核心，Introduction 压缩成论文常见的 4–5 段结构，并以 v3.1 两个文件中的方法设定为主。

对，你这个反馈是对的。之前版本的问题主要有两个：

1. **技术主线偏旧**：不应该再把 GDPO 写成核心贡献；现在应以 v3.1 的两个文件为准，主线是 **策略空间多样性驱动的攻击者 + UCB 对抗回放驱动的防御者**。
2. **Introduction 太像 proposal / related work 展开**：顶会论文的 Introduction 通常不会拆很多小节或写成综述，最好控制在 **4–5 个自然段**，每段承担清晰功能：背景 → 缺口 → 方法 → 贡献 → 结果/总结。

下面我按这个思路重新梳理一个 **中文 Introduction 初稿**。为了方便后续转英文，我会尽量保持论文式表达，不写得太散。

---

# Introduction 初稿（中文，5 段版）

大语言模型的安全对齐通常依赖静态安全数据、人工红队样本或自动化攻击生成器来提升模型对有害请求的拒答能力。然而，现实中的越狱攻击并不是静态分布：攻击者会持续调整攻击方式，组合角色扮演、语义伪装、任务转写、上下文诱导等策略，以绕过不断更新的防御模型。因此，近期研究开始将 LLM 安全训练建模为攻击者与防御者之间的动态对抗过程，通过 self-play 或 co-evolution 让攻击者持续发现新漏洞，同时让防御者在对抗交互中提升鲁棒性。代表性方法如 Self-RedTeam 和 MAGIC 已经表明，攻防协同训练能够比单轮安全微调更有效地提升模型安全性，并在一定程度上保留模型的通用能力。

尽管如此，现有攻防协同框架仍然存在两个关键局限。首先，攻击者在强化学习中往往倾向于利用少数高回报攻击模式，导致 **attack strategy collapse**：模型可能在攻击成功率上提升，但生成的攻击集中在有限策略区域，无法充分覆盖真实世界中多样化的风险类别和攻击方式。已有自动红队和 quality-diversity red teaming 工作试图通过语义距离、n-gram 差异或 MAP-Elites archive 提升攻击多样性，但这些方法大多面向静态目标模型，且多样性度量常停留在文本或语义层面，难以保证攻击策略层面的有效覆盖。其次，防御者在持续学习新攻击时可能产生 **adversarial forgetting**：当训练分布不断向最新攻击者偏移时，模型可能逐渐遗忘对历史攻击模式的防御能力，从而在长期攻防演化中出现安全性能震荡或旧漏洞复现。

为解决上述问题，我们提出 **DACE**，一个 diversity-aware attacker-defender co-evolution framework for LLM safety alignment。DACE 的核心思想是将攻击多样性从隐式的文本差异提升为显式的策略空间覆盖。具体而言，我们定义二维攻击策略空间 $\mathcal{B}=\mathcal{S}\times\mathcal{C}$，其中 $\mathcal{S}$ 表示安全风险类别，$\mathcal{C}$ 表示攻击方式；攻击者在生成对抗 prompt 时被显式引导到不同的策略单元，并通过攻击有效性、策略空间覆盖度和组内新颖性共同优化。与仅奖励攻击成功不同，DACE 鼓励攻击者生成既能突破当前防御者、又能扩展策略覆盖的高价值攻击，从而缓解强化学习中的模式坍缩问题，并为防御者提供更全面的对抗训练信号。

同时，DACE 为防御者引入动态对抗回放机制，以缓解攻防演化过程中的遗忘问题。每轮攻击成功的样本会被加入对抗回放池，并记录其策略描述符和有害性状态；防御者训练时不仅学习当前攻击者生成的新攻击，也会通过 UCB 采样从历史回放池中选取仍具威胁或较少被复查的攻击样本。回放池中的样本根据防御者当前响应进行多级有害性更新：反复突破防御者的样本被保留并提高优先级，已被稳定防住的样本逐步降权或淘汰。这样，DACE 将攻击者的策略探索、防御者的鲁棒学习和历史攻击记忆连接成一个闭环，使防御者在适应新攻击的同时维持对旧攻击的防御能力。

我们的实验从防御者和攻击者两个角度验证 DACE 的有效性。防御者侧，我们评估 harmful refusal、benign compliance、general capability 以及对 OOD attackers 的泛化鲁棒性，证明 DACE 能在保持模型有用性的同时提升对多样化攻击的防御能力。攻击者侧，我们不仅报告 attack success rate，还进一步评估 strategy coverage、successful coverage、strategy entropy 和 transferability，以验证 DACE 生成的攻击是否真正兼具有效性和多样性。总体而言，DACE 表明，在 LLM 安全攻防协同训练中，显式建模攻击策略多样性并维护历史对抗经验，是提升长期安全鲁棒性和缓解对抗遗忘的关键。

---

# 这版 Introduction 的段落功能

| 段落 | 作用 | 重点 |
|---|---|---|
| 第 1 段 | 背景与问题场景 | LLM safety 从静态安全微调走向动态攻防协同 |
| 第 2 段 | 现有方法缺口 | attack strategy collapse + adversarial forgetting |
| 第 3 段 | DACE 攻击者侧方法 | 显式策略空间、coverage、group novelty、有效多样性 |
| 第 4 段 | DACE 防御者侧方法 | UCB adversarial replay、多级有害性更新、缓解遗忘 |
| 第 5 段 | 实验与贡献总结 | defender eval + attacker eval，强调 effective diversity 和 robust defense |

---

# 需要注意的修改点

这一版我刻意做了三件事：

第一，**完全删掉 GDPO 主线**。现在只保留 “通过强化学习优化攻击者/防御者” 的表述，不把某个旧优化算法写成贡献。

第二，**不再把 Introduction 写成综述**。Rainbow、QDRT、MAGIC、Self-RedTeam 这些工作只作为背景支撑，不展开逐篇分析；详细比较应该放 Related Work。

第三，**把 DACE 的 novelty 放在一句话里说清楚**：
> 攻击者侧解决策略坍缩，防御者侧解决对抗遗忘，二者通过回放池闭环连接。

这个故事比“我们加了很多 diversity 指标”更像论文主线。

-----

> 下面是 claude 梳理的 introduction，请结合进行反思，给出充分完善后的 introduction 梳理，
>
> 假装你是严格的reviewer，在内心先对上面的两版本introduction（你的最新的和claude的）进行提问，再切换回author视角完善introduction，再深入思考整理一版， 先简要介绍 dace 的 introduction 怎么写，是什么讲故事逻辑以及为什么要怎么写，再给出具体的每一段的 introduction 内容，要求达到 NeurIPS 录用论文高质量水准，
>
>
> =====================
> 【gpt梳理的introduction】
> 下面我先**以 reviewer 视角"内心拷问"**前一版 introduction，然后切回 author 视角重新设计。最终给出参考 MAGIC 风格的 4-段叙事 + 独立 contribution 列表。
>
> ---
>
> ## 一、Reviewer 视角的内心批判（必须解决的 12 个问题）
>
> | #  | 问题                                                                                                                    | 严重性 |
> | -- | --------------------------------------------------------------------------------------------------------------------- | --- |
> | 1  | **第 1 段像 related work timeline**——堆了 DAN/ASCII/GCG/PAIR/TAP/AutoDAN-turbo/X-Teaming/MAJIC，缺少 hook 和 punch             | 高   |
> | 2  | **缺少斜体研究问题作为锚点**（MAGIC 用 "How to continuously discover..."，DACE 缺这种 anchor）                                           | 高   |
> | 3  | **第 2 段过早讲"双重病理"**——读者还没接受 co-evolution 是 framing，就先听到对它的批判，narrative 跳跃                                              | 高   |
> | 4  | **第 3 段把三类多样性方法平行罗列**，结构上像 mini-survey；MAGIC 的两段障碍讨论是聚焦式而非并列式                                                         | 高   |
> | 5  | **Contribution 嵌套在第 4 段段落中**，再加 4 个 sub-bullet，结构混乱；NeurIPS 习惯独立的 contribution list                                   | 高   |
> | 6  | **第 5 段实验段独立成段**，喧宾夺主；实验数字应放进 contribution bullet                                                                     | 中   |
> | 7  | **没有 Figure 1 视觉化对照**——MAGIC 用 Fig 1 直接画 strawman vs MAGIC，是非常有效的 selling point                                       | 中   |
> | 8  | **"攻击坍缩与防御遗忘是同一动力学的两面"过于哲学化**——需要更具体的 mechanism 描述                                                                    | 中   |
> | 9  | **没有"we observe that..."实证 hook**——MAGIC 用"attacker evolves novel combinatorial strategies"做 hook；DACE 缺这种"先抛实验亮点"的钩子 | 中   |
> | 10 | **"first" claim 出现 2 次**，reviewer 对绝对化 claim 较敏感，需弱化为 "to our knowledge..."                                           | 中   |
> | 11 | **MAJIC 引用嵌在第 1 段攻击演化清单中**——是否与该段叙事必要还需考虑                                                                             | 低   |
> | 12 | **12×10 策略空间是 ad-hoc 还是 derive 出来的没说明**——reviewer 会立刻问"why 12 × 10"                                                   | 低   |
>
> ---
>
> ## 二、整体故事线设计（4 段叙事 + Contribution List）
>
> **完全对齐 MAGIC 的 introduction 结构**——MAGIC 的 introduction 是 4 段叙事 + 3 个 contribution bullet，整体约 1 页。我把 DACE 的 narrative 设计为：
>
> | 段                 | 角色                                     | 核心命题                                                           | 类比 MAGIC 的对应段            |
> | ----------------- | -------------------------------------- | -------------------------------------------------------------- | ------------------------ |
> | **§1**            | Hook + Big Picture + Research Question | LLM 安全的反应式范式失败 → 提出研究问题                                        | MAGIC §1.1               |
> | **§2**            | Co-evolution 范式 + 双重障碍（配 Figure 1）     | Co-evolution 有前景但有两个内生障碍：collapse + forgetting                 | MAGIC §1.2 + Fig 1       |
> | **§3**            | 障碍 1 深挖：攻击坍缩 + 现有多样性方法的失败              | 三类多样性方法都未能在 co-evolution 中作用于策略层                               | MAGIC §1.3-1.4 (障碍 1)    |
> | **§4**            | 障碍 2 深挖：防御遗忘 + DACE 的提出                | 现有 replay 不针对当前威胁度；DACE 用贝叶斯后验 + 闭环回放（带"we observe..."实证 hook） | MAGIC §1.5 (障碍 2 + 方法概述) |
> | **Contributions** | 独立列出 3 个 bullet                        | 方法贡献 + 理论支撑 + 实证                                               | MAGIC contribution list  |
>
> ---
>
> ### 故事的"逻辑闭环"是关键设计
>
> DACE 的所有方法组件都对应到一个具体的 problem，**每个组件都不是 ad-hoc 添加的**：
>
> ```
> 研究问题：如何让 co-evolution 持续？
>         ↓
>   双重障碍 ← Figure 1 视觉化
>    ↙        ↘
> 攻击坍缩     防御遗忘
>    ↓           ↓
> 现有多样性    现有 replay
> 方法不足      不够好
>    ↓           ↓
> 12×10 策略空间  贝叶斯回放池
> + 归一化覆盖   + Thompson 采样
> 增益奖励      + 时间衰减
>    ↘        ↙
>    闭环演化系统
> ```
>
> 这个闭环结构让 reviewer 一目了然："collapse 用多样性奖励解决，forgetting 用贝叶斯回放解决，二者闭环互锁"。
>
> ---
>
> ## 三、Introduction 中文初稿（NeurIPS 高质量水准）
>
> 下面是按上面框架写的具体内容。每段 200-350 字，目标整体约 1.0 页 NeurIPS 排版。
>
> ---
>
> ### § 1 Hook + Big Picture + Research Question（约 220 字）
>
> > 大语言模型（LLM）在代码生成、科学研究、医疗辅助等领域的广泛部署，使其安全对齐成为不可回避的核心问题 (Bai et al., 2025)。当前主流的对齐范式——基于人类反馈的强化学习 (RLHF) (Ouyang et al., 2022)、外部 guardrail 模型 (Inan et al., 2023)、以及静态对齐数据集——本质上是面向"已知攻击分布"的反应式补丁：每一次新型 jailbreak 出现，社区先收集样本、再训练新一代防御，循环往复。然而，攻击演化的速度远快于反应式防御——从早期角色扮演 (Shen et al., 2023) 到自动化对抗优化 (Zou et al., 2023; Chao et al., 2023)，再到隐蔽的多轮代理化攻击 (Rahman et al., 2025) 与近期出现的 Markov 链组合攻击 (Qi et al., 2025)，攻击者的策略空间持续扩张。这一根本性不对称迫使我们重新审视防御范式：***How can we continuously co-evolve attackers and defenders such that the defender remains robust against an ever-shifting distribution of adversarial strategies?***
>
> ---
>
> ### § 2 Co-evolution 范式 + 双重障碍（约 290 字，配 Figure 1）
>
> > 为打破反应式范式的滞后性，近期工作将安全对齐重新建模为攻防协同演化（co-evolution）的多智能体博弈：Self-RedTeam (Liu et al., 2025) 通过 zero-sum self-play 给出 Nash 均衡下的安全保证；MAGIC (Wen et al., 2026) 在非对称序贯博弈框架下取得 Subgame Perfect Nash Equilibrium 的点态保证；ACE-Safety (Li et al., 2025)、AdvEvo-MARL (Pan et al., 2025) 与 PIA (Li et al., 2026) 进一步从 MCTS、MARL 和 persona-invariant 角度推进了这一范式。然而，深入分析这些框架的训练动态，我们发现它们普遍受困于两个相互加剧的内生障碍（如 Figure 1 所示）。**(1) 攻击策略坍缩（Attack Strategy Collapse）：** 在 RL 奖励最大化压力下，攻击者迅速过拟合到少数高回报策略模式，使得 defender 仅在窄分布上接受训练，对 OOD 攻击的真实鲁棒性虚高。**(2) 防御对抗遗忘（Defense Adversarial Forgetting）：** 当 attacker 策略持续漂移时，defender 倾向于过拟合当前 attacker，逐步丢失对早期攻击模式的鲁棒性，类似持续学习中的灾难性遗忘 (Kirkpatrick et al., 2017) 但因对手非平稳性而更严重。这两个障碍互为因果——窄分布训练加剧遗忘，遗忘又使得 attacker 那少数有效模式被反复"奖励"，形成虚高指标 + 真实鲁棒性下降的恶性平衡。
>
> ---
>
> ### § 3 障碍 1 深挖：攻击坍缩与现有多样性方法的不足（约 280 字）
>
> > 解决攻击坍缩的自然思路是引入多样性，已有工作沿三个方向展开但都未能在 co-evolution 中真正生效。**第一类是 Quality-Diversity (QD) 离线搜索**——Rainbow Teaming (Samvelyan et al., 2024)、Ferret (Pala et al., 2025) 与 QDRT (Wang et al., 2025) 在 risk category × attack style 行为空间上用 MAP-Elites 维护 archive，但其搜索过程不参与攻防协同训练，**以静态 target LLM 为目标**，因此无法持续暴露不断进化的 defender 的新漏洞。**第二类是基于 RL 的语义/词汇多样性奖励**——CRT (Hong et al., 2024)、DiveR-CT (Zhao et al., 2024)、GFlowNet 红队 (Lee et al., 2024) 用 Self-BLEU、SBERT 距离或 k-NN 多样性激励 attacker；然而这些指标停留在表层文本与嵌入空间，**无法识别"换皮不换招"的伪多样性**——同一个角色扮演策略可以用上百种语言形式包装而获得高 SBERT 多样性分数，攻击的实质策略并未改变。**第三类是当前 co-evolution 框架本身**——Self-RedTeam 报告 +21.8% SBERT 多样性提升但仍观察到 t-SNE 聚类坍缩，MAGIC 注意到组合策略的涌现但**未将多样性纳入奖励设计**。综上，**在 co-evolution 中、在策略层、在线**地激励多样性这一三重交集，仍是一个开放问题。
>
> ---
>
> ### § 4 障碍 2 深挖 + DACE 提出（约 340 字）
>
> > 防御对抗遗忘问题在现有工作中的处理同样不充分。SSP (Wang et al., 2026) 引入了基于奖励高低的 UCB experience replay 来缓解 self-play 训练的震荡，但其优先级**仅基于历史奖励，不反映样本对当前 defender 的实时威胁度**——一个早期被 attacker 突破但已被现 defender 学会拒绝的样本，仍会因高历史奖励被反复回放，浪费训练预算；MAGIC 与 ACE-Safety 则完全不维护历史攻击的回放机制，attacker 的迭代演化使早期策略事实上从训练分布中消失。基于以上分析，我们提出 ***DACE（Diversity-driven Adversarial Co-Evolution）***，一个将策略空间多样性与历史威胁度感知回放系统性集成到 co-evolution 的 RL 框架。我们的核心见解是：**坍缩与遗忘是同一对抗动力学下的两个互锁失败模式**——只有把多样性"在线"作用于显式策略空间（缓解坍缩），并把历史样本通过反映当前威胁度的有原则回放重新注入 defender 训练（缓解遗忘），二者才能形成正反馈而非恶性循环。具体而言，DACE 包含三个紧耦合组件：（i）一个基于 Llama-Guard-4 风险分类与 SorryBench 攻击模式聚类得到的 (12 \times 10) 显式策略空间，配合 SFT 暖启动赋予 attacker 策略推理能力；（ii）一个带 KL 散度收缩效率解读的归一化边际覆盖增益奖励，从根源上消除原始熵增量在长周期训练中的信号衰减；（iii）一个以 Beta-Bernoulli 后验追踪当前威胁度、Thompson Sampling 实现探索-利用平衡、指数时间衰减适应非平稳性的贝叶斯对抗回放池。**值得注意的是，**通过迭代 RL 训练，DACE-attacker 自发演化出 SFT 数据中不存在的多策略组合攻击（如角色扮演 × 翻译 × 概念替换的复合攻击），且单 rollout 即可达到与 PAIR、TAP 等多轮搜索方法相当的攻击成功率，验证了我们设计的有效性。
>
> ---
>
> ### Contributions（独立列表，3 个 bullet）
>
> > In summary, we make the following contributions:
> >
> > **• A diversity-driven co-evolution framework with normalized coverage reward.** We propose DACE, the first co-evolution framework that systematically introduces structured strategy-space diversity into RL-based safety alignment to our knowledge. Centered on a (12 \times 10) explicit attack strategy space, we design a *normalized marginal coverage gain* reward whose normalization scheme provably eliminates the (O(1/|\mathcal{A}|)) reward vanishing inherent in raw entropy-based rewards. Through a KL-divergence reformulation, we show that the reward is equivalent to per-step KL contraction efficiency toward the uniform strategy distribution and inherits the zero-avoiding property that drives strongest exploration toward unfilled strategy slots.
> >
> > **• Bayesian adversarial replay against defense forgetting.** We introduce a unified archive that simultaneously serves as the strategy frequency tracker and the adversarial replay buffer. Each archived sample maintains a Beta-Bernoulli posterior reflecting its real-time threat against the current defender; Thompson Sampling provides principled exploration-exploitation balance during replay; exponential time decay handles the non-stationarity induced by defender evolution; and a posterior-confidence-aware pruning rule retires only samples that are sufficiently tested *and* low-threat. This design closes the loop between attack diversity expansion and defense memory consolidation.
> >
> > **• Comprehensive empirical validation across two model families and SOTA OOD attackers.** Extensive experiments on Qwen2.5-7B-Instruct and Llama3.1-8B-Instruct show that DACE matches or surpasses MAGIC on safety benchmarks (e.g., HarmBench adv-harm ASR (0.043 \rightarrow 0.003)) without sacrificing utility (IFEval, ARC-C, GPQA, MMLU, AlpacaEval 2 within 2%). On the OpenRT pipeline with GPT-4o as judge, DACE consistently outperforms MAGIC against PAIR, TAP, AutoDAN, AutoDAN-turbo (e.g., (54.69% \rightarrow 42.18%) on AutoDAN-turbo) and remains robust against the most recent black-box compositional attack MAJIC (Qi et al., 2025). On the attacker side, DACE-attacker achieves a Coverage Rate (\sim 30%) higher than MAGIC-attacker while maintaining superior cross-defender transferability across six target backbones.
>
> ---
>
> ## 四、相对前一版的关键改进（reviewer 检查清单对照）
>
> | Reviewer 关切          | 处理方式                                                                                     |
> | -------------------- | ---------------------------------------------------------------------------------------- |
> | 第 1 段堆 timeline      | 改为 Hook（反应式范式失败）+ Research Question 锚点（斜体英文 RQ）                                          |
> | 缺少 RQ anchor         | 第 1 段末加斜体英文 RQ                                                                           |
> | 第 2 段直接讲病理太突兀        | 先建立 co-evolution 是 framing（引 5 篇 SOTA），再"However"切到障碍                                    |
> | 三类多样性平行像 mini-survey | 第 3 段保留并列结构但聚焦"为什么都不在 co-evolution 工作"，结尾归纳到三重交集                                         |
> | Contribution 嵌入段落    | 独立列表 3 个 bullet（参考 MAGIC 格式）                                                             |
> | 实验数字独立成段             | 移到 contribution 第 3 个 bullet 内                                                           |
> | 缺 Figure 1           | 在 §2 配 Figure 1 引用（左：MAGIC attacker 在 12×10 cell 上塌缩 + 防御遗忘 U 形曲线；右：DACE 均匀覆盖 + 贝叶斯回放循环） |
> | "两面"过于哲学化            | 第 4 段换为"互锁失败模式 / 正反馈 vs 恶性循环"具体 mechanism                                                |
> | 缺 we observe 实证 hook | 第 4 段末加"DACE-attacker 自发演化组合攻击 + 单 rollout 匹敌多轮搜索"两个 hook                                |
> | "first" claim        | 用 "to our knowledge" 弱化                                                                  |
> | 12×10 来源             | §4 写明"基于 Llama-Guard-4 + SorryBench 聚类"                                                  |
> | MAJIC 位置             | §1 仅一句带过；详细对比留 contribution bullet 第 3                                                   |
>
> ---
>
> ## 五、写作上的几个小决策（建议你拍板）
>
> 1. **Figure 1 设计**：建议三栏布局——(a) MAGIC attacker 输出在 12×10 grid 上的频率热图（可见少数 cell 高度集中）；(b) "Forgetting U-curve"（最终 defender 对 attacker iter1–4 的 ASR，无 replay 时呈 U 形）；(c) DACE 的均匀分布 + 贝叶斯回放闭环示意图。三幅图各占 1/3 宽度，主文献图（不放 Appendix）。
>
> 2. **是否在 §1 直接提"DACE"作为方法名**：MAGIC 在 §1 末尾未提名，§4 才正式介绍。我目前 follow MAGIC，在 §4 才正式提 DACE。这样 §1-§3 都是 problem framing，§4 才切到 method，narrative 更紧凑。
>
> 3. **"In summary, we make the following contributions" 措辞**：MAGIC 用 "In conclusion, our contributions are summarized as follows:"。两种都行，建议用 "We summarize our contributions as follows:" 略简洁。
>
> 4. **是否需要 §5 一句话过渡到剩余章节结构**：NeurIPS introduction 通常**不需要** "The rest of the paper is organized as follows..." 这种 boilerplate。MAGIC 也没写。建议省略。
>
> ---
>
> 如果你确认这一版骨架 OK，我可以：(a) 把 §1–§4 + Contributions 翻译为正式英文（控制在约 1.0 页 NeurIPS 排版），保持 MAGIC 的 academic register；或者 (b) 顺势把 method 章节也开始按 MAGIC §3-§4 的结构（problem formalization + methods + reward design + algorithm）草拟。你想推进哪一步？

我会把 Claude 版当成一个强 baseline 来“挑错再重写”：保留它的 4–5 段结构和 Figure 1 意识，但会删掉过强 claim、过多 related-work 堆叠，以及任何不符合 v3.1 的旧方法表述。

你给的 Claude 版比我上一版更接近论文 Introduction 的形态：它有 **research question、双重 failure mode、Figure 1、contribution list**。但它仍有几个需要修正的点：

1. **还是偏“综述式”**：第 1–3 段堆了太多工作，容易像 Related Work。
2. **方法细节过早过密**：12×10、Llama-Guard-4、SorryBench、Beta-Bernoulli、Thompson、KL contraction 全塞进 Introduction，会让主线变重。
3. **claim 过强**：比如 “first co-evolution framework” 这类说法 reviewer 会敏感，建议改成 “to our knowledge, among the first...”
4. **实验数字不要写太满**：Introduction 可以给概括性结果，具体数字放 abstract 或 experiment。
5. **最重要的是**：DACE 的故事不应写成“加了 diversity reward 和 replay buffer”，而应写成 **co-evolution 要长期有效，必须同时解决 attack-space coverage 和 defensive memory**。

---

# 一、DACE Introduction 应该怎么写

DACE 的 Introduction 最好采用 **4 段主叙事 + 1 段实验总结 + contribution list**。

核心故事逻辑是：

> LLM safety 不是静态分类问题，而是动态攻防问题。
> Co-evolution 是正确方向，但现有 co-evolution 会出现两个内生失败：攻击者策略坍缩，防御者对抗遗忘。
> 现有 diversity red-teaming 能提升攻击多样性，但大多是静态 target、单边 red team，不能解决防御者长期鲁棒性。
> DACE 的关键是把 **显式策略空间探索** 和 **历史威胁记忆** 放进同一个攻防闭环：攻击者持续覆盖策略空间，防御者持续回放仍具威胁的历史攻击，从而推动长期鲁棒安全对齐。

这个写法的好处是：
**每个方法组件都对应一个 reviewer 能理解的必要问题**。

| DACE 组件 | 对应问题 | Introduction 中的功能 |
|---|---|---|
| 结构化攻击策略空间 | 多样性不能只靠文本/语义距离 | 说明 DACE 的 diversity 是策略层面的 |
| 归一化覆盖奖励 / 新颖性奖励 | RL attacker 容易策略坍缩 | 说明 DACE 如何保持有效攻击覆盖 |
| 对抗回放池 | Defender 会遗忘旧攻击 | 说明 DACE 如何维持长期鲁棒性 |
| 当前攻击 + 历史攻击混合训练 | 新攻击适应与旧攻击记忆冲突 | 说明 DACE 是闭环演化系统 |
| defender + attacker 双侧 eval | 不能只证明安全，也要证明攻击多样性 | 对应实验章节主线 |

---

# 二、推荐 Introduction 段落结构

我建议控制为下面这 5 段：

| 段落 | 任务 | 核心句 |
|---|---|---|
| Paragraph 1 | 背景与 research question | LLM safety 是动态攻防问题，静态 safety tuning 滞后 |
| Paragraph 2 | Co-evolution 的前景与内生失败 | Co-evolution 有希望，但会出现 attack collapse 与 defense forgetting |
| Paragraph 3 | 为什么现有 diversity red-teaming 不够 | 多样攻击生成≠能持续训练出长期鲁棒 defender |
| Paragraph 4 | 提出 DACE | DACE 用策略空间探索 + 对抗记忆闭环解决上述问题 |
| Paragraph 5 | 实验总结 | DACE 同时提升 defender 鲁棒性、attacker 多样性和遗忘缓解 |

然后接一个 **Contribution list**，最多 3–4 条，不要 5 条以上。

---

# 三、Introduction 中文初稿

下面这版是我认为更适合 NeurIPS 投稿水准的中文骨架。它比 Claude 版更收敛，避免过多 related work 堆叠，也避免把方法细节提前讲成 Method section。

---

## Paragraph 1：从动态安全问题切入

大语言模型正被部署到越来越开放的交互环境中，其安全性不再只取决于能否拒绝一组固定的有害请求，而取决于能否在面对持续变化、策略性适应的攻击者时保持稳健。传统安全对齐方法通常依赖静态安全数据、人工红队样本或离线收集的 jailbreak prompts 来训练模型拒绝有害请求；然而，这种反应式范式天然滞后于真实威胁模型，因为攻击者会根据模型的拒绝模式不断调整攻击策略、组合新的伪装方式，并复用历史上曾经有效的攻击模式。近期的 self-play 和 attacker-defender co-evolution 方法开始将 LLM safety alignment 重新建模为动态攻防过程：攻击者持续生成 adversarial prompts，防御者同步学习识别并拒绝这些输入。这一方向表明，安全对齐不应只是静态补丁，而应是持续演化的对抗学习过程。本文关注的核心问题是：**如何让攻防协同演化长期有效，使防御者不仅适应当前攻击者，而且对不断扩展的攻击策略空间保持稳健？**

---

## Paragraph 2：指出 co-evolution 的两个内生失败

尽管攻防协同演化为 LLM 安全训练提供了更贴近现实的范式，现有方法仍然缺少维持长期鲁棒性的机制。我们认为，其关键瓶颈来自两个相互耦合的失败模式。第一，**攻击策略坍缩**：在强化学习奖励最大化压力下，攻击者容易过拟合到少数高回报、低成本的攻击模式。此时，训练中的 attack success rate 可能持续上升，但攻击分布逐渐集中于少数策略区域，无法覆盖真实世界中更加多样的风险类别和攻击方式。第二，**防御对抗遗忘**：当攻击者策略持续漂移时，防御者的训练分布也随之移动。如果防御者主要学习当前轮次的新攻击，它可能在适应新攻击的同时逐渐遗忘旧攻击模式，使历史漏洞在后续阶段重新出现。这两个问题并非独立存在：攻击者坍缩会使防御者只在窄分布上训练，而防御者遗忘又会让少数历史有效策略反复变得有利，最终形成表面共演化、实则覆盖不足的脆弱循环。

---

## Paragraph 3：解释为什么现有 diversity red-teaming 不足以解决 DACE 的问题

与 co-evolution 方向并行，自动红队和 diversity red-teaming 工作已经尝试生成更有效且更多样的攻击。例如，quality-diversity search 通过行为网格和 archive 维护高质量攻击样本，curiosity-driven 或 GFlowNet-based 方法通过新颖性奖励或概率采样缓解 mode collapse，近期的 goal-driven diversity 方法也指出，简单的词汇差异或 embedding 距离难以捕捉真实攻击策略差异。这些工作为攻击多样性提供了重要基础，但它们大多面向静态 target model，主要优化 red-team generator 本身，而没有回答 co-evolution 中更关键的问题：**多样攻击如何持续推动防御者形成更广泛的安全边界？防御者已经学过的历史攻击如何被保留、重估和重新采样？** 换言之，现有 diversity red-teaming 解决的是“如何找到更多样的攻击”，而 DACE 需要解决的是“如何让多样攻击与防御训练形成长期闭环”。

---

## Paragraph 4：提出 DACE 的中心思想和方法概览

为此，我们提出 **DACE，Diversity-Aware Adversarial Co-Evolution**，一个面向 LLM safety alignment 的多样性驱动攻防协同演化框架。DACE 的核心观点是：稳健的安全共演化需要同时具备 **攻击侧的策略空间覆盖** 和 **防御侧的历史威胁记忆**。在攻击侧，DACE 将每个攻击样本映射到结构化行为描述符 $b(x)=(s,c)$，其中 $s$ 表示安全风险类别，$c$ 表示攻击方式，从而把多样性从表层文本差异提升到具有安全语义的策略空间。攻击者不仅被奖励攻击成功，还被鼓励覆盖低频或尚未充分探索的策略区域，生成既有效又多样的攻击。在防御侧，DACE 维护对抗回放池，记录历史成功攻击及其策略描述符，并根据当前防御者的响应动态估计这些样本的剩余威胁度。防御者训练时同时学习当前攻击者生成的新攻击和从回放池中采样的历史高风险攻击，从而在适应新攻击的同时维持对旧攻击模式的鲁棒性。通过这一闭环，DACE 将 red teaming 从一次性漏洞发现推进为持续的策略覆盖扩展与防御记忆巩固过程。

---

## Paragraph 5：实验总结与论文承诺

我们从 defender 和 attacker 两个角度系统评估 DACE。Defender 端，我们考察 harmful refusal、benign compliance、general capability、对外部 OOD attackers 的泛化鲁棒性，以及对历史攻击的遗忘程度，以验证 DACE 是否真正提升安全性而不是简单提高过拒率。Attacker 端，我们不仅报告 attack success rate，还进一步评估 strategy coverage、successful coverage、strategy entropy、quality-diversity score 和 cross-defender transferability，以检验攻击者是否真正产生有效且多样的攻击。实验结果表明，DACE 能在保持模型通用能力和正常请求响应能力的同时，提升防御者对多类 adversarial benchmarks 和外部攻击器的鲁棒性；同时，DACE attacker 覆盖更广泛的风险类别和攻击方式组合，生成的攻击具有更强的迁移性和更低的策略坍缩倾向。消融实验进一步表明，结构化多样性奖励和对抗回放机制分别对攻击覆盖扩展和防御遗忘缓解起到关键作用。

---

# 四、Contribution list 建议版本

Contribution list 不要太长，建议 3 条即可。

## Contributions

本文的主要贡献可以写成：

1. **我们提出 DACE，一个多样性驱动的 LLM 安全攻防协同演化框架。**
   DACE 将攻击策略探索、防御鲁棒学习和历史攻击记忆统一到一个闭环训练过程中，使 co-evolution 不仅适应当前攻击者，也持续覆盖更广泛的攻击策略空间。

2. **我们提出策略空间层面的攻击多样性建模与优化目标。**
   DACE 将攻击样本映射到风险类别 × 攻击方式的结构化策略空间，并通过覆盖度和新颖性奖励鼓励攻击者生成既有效又多样的攻击，从而缓解 RL-based red teaming 中常见的策略坍缩问题。

3. **我们设计对抗回放机制以缓解防御者遗忘。**
   DACE 维护历史高风险攻击的动态回放池，并根据当前防御者状态重估样本威胁度，使防御者在学习新攻击的同时持续复习仍具训练价值的历史攻击。

4. **我们进行双侧评估，验证 DACE 同时提升防御鲁棒性和攻击多样性。**
   在 defender 端，DACE 提升 harmful refusal、OOD attacker robustness 和历史攻击保持能力，同时基本保持 benign compliance 与 general capability；在 attacker 端，DACE 在 attack success、strategy coverage、successful coverage 和 transferability 上表现出更好的有效性—多样性平衡。

---

# 五、相对 Claude 版我建议保留与修改的点

**保留：**

- 保留 4–5 段 Introduction，而不是之前 10 段式写法。
- 保留 research question。
- 保留 “attack strategy collapse + defense adversarial forgetting” 作为核心 gap。
- 保留 Figure 1 的想法：左边画现有 co-evolution 的坍缩与遗忘，右边画 DACE 的策略覆盖和回放闭环。
- 保留 contribution list，而不是把贡献埋在正文里。

**修改：**

- 不在 Introduction 里展开过多论文清单，把 detailed survey 放 Related Work。
- 不把方法细节写得像 Method section，诸如具体 posterior、采样公式、时间衰减、KL 解释，可以在 Method 里展开。
- 不再写 GDPO，因为它已经不是当前 v3.1 主线。
- 弱化 “first” claim，改成 “we propose” 或 “to our knowledge, among the first”。
- 实验段只写结论性承诺，不写过多可能后续变动的具体数值。

最终最关键的一句话可以作为整篇 Introduction 的 spine：

> **DACE argues that robust LLM safety co-evolution requires coupling strategy-space exploration on the attacker side with adversarial memory consolidation on the defender side.**

中文就是：

> **DACE 的核心主张是：稳健的 LLM 安全共演化必须把攻击侧的策略空间探索与防御侧的对抗记忆巩固耦合起来。**