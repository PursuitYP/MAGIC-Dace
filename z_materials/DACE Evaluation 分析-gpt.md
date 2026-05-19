# DACE Evaluation 分析-gpt

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