# Sec 4 实验部分精简计划（含可直接复制的精简后内容）

目标：从 ~9.5 页压缩到 9 页。每条分析下方给出**直接可复制的精简版本**（仅替换原段落正文，不动表/图/RQ 列表）。

---

## §4.1 Experimental Setup

### Models（L605-606）
**修改要点**：合并 judge 选择句，去 "subsequently/in subsequent"。

```latex
\textbf{Models.}\quad
We use instruction-tuned models from the Qwen2.5 and Llama3.1 families as defender backbones, with Qwen2.5-7B-Instruct~\citep{yang2025qwen25} and Llama3.1-8B-Instruct~\citep{touvron2023llama} reported in the main tables. Unless otherwise specified, Qwen3Guard~\citep{zhao2025qwen3guard} serves as the reward model during training and the in-distribution safety judge; GPT-4o~\citep{openai2024gpt} serves as an independent judge for OOD attacker evaluations.
```

### Training dataset（L610-611）
**修改要点**：合并 "harmful and benign 各 15K"，修复 typo "splitas"，把 uniform balancing 句并入。

```latex
\textbf{Training dataset.}\quad
For the SFT phase, we construct a strategy-conditioned CoT dataset in which every example requires the attacker to emit a reasoning trace, a strategy declaration $(s, c) \in \strategyspace$, and a rewritten prompt. The harmful subset draws its seeds from the training data of Jailbreak-R1~\citep{wang2025jailbreakr1}; the benign subset draws its seeds from the benign split of WildJailBreak~\citep{jiang2024wildteaming}. We employ Gemini-2.5-Pro~\citep{comanici2025gemini} to synthesize the three-part CoT rewrites under the prompts listed in Appendix~\ref{apdx:prompts}. For the RL phase, we sample 15{,}000 vanilla harmful and 15{,}000 vanilla benign prompts from WildJailBreak as seeds for attacker rewriting; uniform balancing across the $12\times10$ strategy grid is detailed in Appendix~\ref{apdx:space-design}.
\label{sec:exp-data}
```

### Baselines（L616-617）
**修改要点**：缩短 Self-RedTeam / MAGIC 修饰短语；删除 SmoothLLM/Self-Eval 后的赘述。

```latex
\textbf{Baselines.}\quad
We compare \method against the following baselines: (1) the original instruction-tuned Qwen2.5 and Llama3.1 models; (2) two co-evolution methods, \textbf{Self-RedTeam}~\citep{liu2025chasing}, an online self-play adversarial RL method with shared attacker--defender parameters, and \textbf{MAGIC}~\citep{magic2025}, an asymmetric sequential-game co-evolution baseline with an SPNE solution concept; and (3) inference-time defense baselines \textbf{SmoothLLM}~\citep{robey2023smoothllm} and \textbf{Self-Eval}~\citep{phute2023llm}. More experimental details are provided in Appendix~\ref{apdx:training-setup}.
```

## §4.2 Evaluation Protocol

### Safety evaluation（L634-635）
**修改要点**：合并末两句 judge 说明。

```latex
\textbf{Safety evaluation.}\quad
We evaluate harmful refusal on WildGuardTest~\citep{han2024wildguard}, the WildJailBreak adversarial-harm split~\citep{jiang2024wildteaming}, HarmBench~\citep{mazeika2024harmbench} vanilla and adversarial splits, DAN~\citep{shen2023doanythingnow}, OR-Bench-Toxic~\citep{cui2024orbench}, the XSTest contrast categories~\citep{rottger2023xstest}, and StrongREJECT~\citep{souly2024strongreject}; benign compliance is measured on the XSTest safe categories and the WildJailBreak adversarial-benign split. We use Qwen3Guard~\citep{zhao2025qwen3guard} as the in-distribution judge, and the OpenRT framework~\citep{OpenRT2026} with PAIR/TAP/AutoDAN/AutoDAN-Turbo plus a GPT-4o judge (Appendix~\ref{apdx:prompts}) for OOD robustness. Detailed benchmark descriptions are given in Appendix~\ref{apdx:bench-protocol}.
```

### General capability evaluation（L639-640）
**修改要点**：删除冗余目的陈述末句。

```latex
\textbf{General capability evaluation.}\quad
We evaluate general capability on five benchmarks covering instruction following, multi-task reasoning, and open-ended generation quality: IFEval~\citep{zhou2023ifeval}, ARC-Challenge~\citep{clark2018arc}, GPQA~\citep{rein2023gpqa}, MMLU~\citep{hendrycks2021mmlu}, and AlpacaEval~2~\citep{dubois2024alpacaeval2}, monitoring whether iterative safety-driven RL degrades downstream usefulness.
```

## §4.3 Main Results

### RQ1 段（L704）
**修改要点**：删括号内子集枚举；末句双机制归因压成一句。

```latex
\textbf{\method effectively improves defender safety without inducing over-refusal (RQ1).} As shown in Table~\ref{tab:evaluation_main}, on both \textit{Qwen2.5-7B-Instruct} and \textit{Llama3.1-8B-Instruct}, \method delivers consistent and substantial reductions in attack success rate across all harmful-refusal subsets compared to MAGIC and Self-RedTeam, while preserving benign compliance with only marginal differences from the strongest baseline. The defender therefore becomes strictly safer \emph{and} continues to comply with legitimate user requests. We attribute this dual gain to the two mechanisms in Section~\ref{sec:method}: the \emph{diversity-driven exploration} reward broadens the attack distribution while the \emph{Bayesian adversarial replay pool} prevents drift away from earlier attack modes once the attacker evolves.
```

### RQ2 段（L734）
**修改要点**：缩短末句对 prior work 的引用。

```latex
\textbf{\method preserves general capabilities after iterative RL training (RQ2).} Table~\ref{tab:general_cap} shows that on both backbones \method matches the original instruction-tuned model and the co-evolution baselines on IFEval, ARC-C, MMLU, and AlpacaEval~2 to within at most one point, and slightly improves AlpacaEval~2 LC win rate on Qwen2.5-7B-Instruct. This confirms that the diversity-driven attacker reward and the Bayesian replay mini-batch on the defender side---both safety-only signals layered on top of GRPO---do not interfere with instruction following or general knowledge, consistent with~\citet{magic2025}.
```

### RQ3 段（L761）
**修改要点**：合并迭代/组合 attacker 解释；末句两机制归因压成一句。

```latex
\textbf{\method-defender demonstrates robust generalisation to OOD attacks (RQ3).} Table~\ref{tab:harmbench_generalization} evaluates the defender against six unseen automated attackers on HarmBench. \method achieves the lowest ASR across every column---reducing AutoDAN-Turbo from $54.69\%$ (MAGIC) to $42.81\%$, PAIR from $25.31\%$ to $17.81\%$, and the no-rewrite baseline to $12.19\%$. The largest gains appear on iterative/composition-heavy attackers (AutoDAN-Turbo, TAP, PAIR), which match the strategy combinations emerging in late-training rollouts so the defender sees their neighbours during training. The strategy-level coverage reward exposes the defender to a wide cross-section of $(s,c)$ combinations, while the Bayesian replay pool prevents drift away from earlier modes that PAIR/TAP-style attacks tend to revisit.
```

### RQ4 段（L806）
**修改要点**：缩短两条修饰从句。

```latex
\textbf{\method-attacker exhibits strong transferability across unseen defenders (RQ4).} Table~\ref{tab:attacker-transfer} reports the cross-defender attack success rate of \method-attacker, MAGIC-attacker, and the base instruction-tuned attacker on 600 WildJailbreak vanilla harmful prompts. Across the four \emph{unseen} defenders---Qwen2.5-7B-IT, Llama3.1-8B-IT, Mistral-7B-IT, and Gemini-2.5-Flash---the \method attacker is expected to match or surpass MAGIC-attacker, showing that broader strategy coverage does not sacrifice single-shot attack strength. Conversely, on the matched \method-defender column, the \method attacker is sharply suppressed and produces a notably lower ASR than MAGIC-attacker faces on its own MAGIC-defender, indirect evidence that the \method defender's robustness stems from training against a stronger, more diverse adversary.
```

### RQ5 段（L837）
**修改要点**：删三轴重复定义；末长句改写。

```latex
\textbf{Broader strategy and textual diversity is achieved by the \method attacker (RQ5).} Table~\ref{tab:attacker-diversity} compares \method against MAGIC at strategy, semantic, and textual levels. \method delivers a substantial lead at the strategy level (Coverage $88.33\%$ vs.\ $45.83\%$, Shannon $3.457$ vs.\ $3.382$ in the last 15 training steps) while simultaneously \emph{improving} every textual-level metric (lower SBERT cosine, lower Self-BLEU, higher Distinct-2). This rules out the ``new skin, same trick'' failure mode~\citep{triplayrl2026} where a co-evolved attacker varies surface form without changing underlying strategy: the diversity-driven exploration reward forces strategy-level coverage, and the explicit two-dimensional strategy space ensures rewrites are also semantically and lexically distinct. The third row further shows that the final \method replay pool retains $100\%$ strategy coverage and the lowest textual redundancy in the table even after Beta--Bernoulli-driven pruning, consistent with the design of the diversity reward (\S\ref{sec:method-attacker}) and the Bayesian replay pool (\S\ref{sec:method-replay}).
```

## §4.4 Experimental Analysis

### 引子（L848）
保持不动。

### 协同演化分析段（L871，全文最长正文段）
**修改要点**：删坐标轴说明；浓缩 forgetting 与 collapse 两条形式化引用。

```latex
\textbf{Co-evolution proceeds without strategy collapse or adversarial forgetting.} The left panel of Fig.~\ref{fig:coevo-and-pool} plots the $N \times N$ cross-evaluation heatmap between \method attacker and defender checkpoints, reporting ASR on $320$ HarmBench seeds following MAGIC's Figure~3 protocol. The diagonal stays consistently low and tightens monotonically toward the final round, evidencing a stable joint co-evolution rather than the oscillation typical of zero-sum self-play. Upper-triangular columns---a fixed late-round defender against progressively older attacker checkpoints---remain uniformly dark, empirically realising bounded $F(t_0,t)$ (Definition~\ref{def:forgetting}) and confirming that the Bayesian replay pool of Section~\ref{sec:method-replay} keeps the defender from drifting away from earlier attack modes. The right panel encodes, for each $(s, c)$ cell, the number of archived attacks (cell colour) and their aggregated Beta--Bernoulli posterior mean $\hat p = (\alpha + s_i)/(\alpha + \beta + s_i + f_i)$ (cell annotation). \method spreads successful attacks broadly across the grid \emph{and} maintains high posterior harmfulness in each populated cell, the empirical signature of avoiding strategy collapse (Definition~\ref{def:collapse}) and confirming the synergy of the coverage-gain reward (\S\ref{sec:method-attacker}) and the replay pool (\S\ref{sec:method-replay}).
```

---

## 预计总节约

| 段落 | 节约行数 |
|---|---|
| Models | 1 |
| Training dataset | 1 |
| Baselines | 1 |
| Safety evaluation | 1 |
| General capability | 1 |
| RQ1 | 1–2 |
| RQ2 | 1 |
| RQ3 | 2 |
| RQ4 | 1 |
| RQ5 | 2 |
| Co-evolution analysis | 3 |
| **合计** | **~15–16 行 ≈ 0.4–0.5 页** |

足以把正文从 9.5 页压回 9 页内。若 PDF 实测仍略超，可再从 RQ5 / 协同演化段各砍 1 行余量。

## 不修改
- L589–594 RQ 列表段（用户明确要求）
- 所有表格、图、caption、数字
- §4 之外的内容
