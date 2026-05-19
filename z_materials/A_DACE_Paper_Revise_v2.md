# DACE 论文修订计划 v2 — Experiments 章节重构

## Context (why this revision)

用户要求在保持现有注释风格的前提下，**重构实验章节结构**，使其更贴近 MAGIC 论文的实验编排：主文专注 defender 主实验 + attacker 主实验 + 两张新图；multi-turn 与完整 ablation 下放到附录。当前 `neurips_2026.tex` 的 §5 有 6 个 RQ 但编排偏散、SSP 基线与用户新指令（对齐 MAGIC baseline）冲突；此外主表只放 Qwen2.5-7B 单 backbone，需要扩展到 Qwen+Llama 两个 backbone。为便于审稿人阅读，能和 MAGIC 对齐的表格要把 MAGIC 论文中已披露的数字直接填入 MAGIC 行（DACE 自身行仍用 `--` 占位）。

## 用户关键指令（Session 2 — 本次修订）

1. **主表模型覆盖**：Table 1/2/3 同时放 Qwen2.5-7B-Instruct + Llama3.1-8B-Instruct；其他表格/图表仅 Qwen2.5-7B。Qwen2.5-14B 放附录 F 扩展。
2. **Baseline 与 MAGIC 对齐**：从主表与附录中**完全移除 SSP**（包括 Ablation 中的 "SSP-style discrete-score replay" 行）。保留 Self-RedTeam / SmoothLLM / Self-Eval / MAGIC。
3. **实验结构 4 个主块**（参见 MAGIC）：
   - Defender main (Table 1/2/3 + 简化 case study)
   - Attacker main (Table 4 attacker ASR + Table 5 diversity-metrics + Figure 3 合并)
   - Appendix multi-turn (原 Table 4 下放)
   - Appendix full ablation (原 Table 5 下放，6 行: base/MAGIC/w/o SFT/w/o diversity/w/o replay/DACE)
4. **数据填充**：凡是表结构与 MAGIC 一致的单元格（MAGIC/Self-RedTeam/原模型 baseline 行），直接填入 MAGIC 数字；DACE 与 MAJIC 列 / DACE 行保持 `--`。
5. **附录补充**：加 Dataset 介绍（MAGIC 风格 `\paragraph{}` 体），包括新增 MAJIC 攻击的描述。
6. **Figure 3+4 合并**：一张 figure，左=co-evolution heatmap（MAGIC Fig 3 复刻），右=replay pool 12×10 strategy+harmfulness；caption 与分析段都要同时覆盖左右两侧。
7. **Table 5 diversity 指标**：包括 3 行对比（MAGIC 最后 15 步 8gpu-tp2、DACE 最后 15 步 sft-full、DACE 最终 replay pool max_pool=4000）；指标列：Coverage Rate / Shannon Entropy / QD-Score / SBERT cosine / Self-BLEU / Distinct-2 / n-gram entropy。
8. **Case study**：主文放"简化版"占位（简单 box，配 "to be supplemented" 说明）；附录 H 已有的详细版占位保留。
9. **Figure 4 数据源**：用户会自行选择合适的 step（250/200/300 或 early-vs-late 对比）作为底层数据；写作侧只写通用 intro / 分析，不锁死具体 step。
10. **分析文字口径**：沿用 "we evaluate / we expect / we study" 的 planned/evaluation framing，不要 premature 地宣称 SOTA。

## 主文 §5 实验章节的新结构（目标布局）

```
§5 Experiments
├── §5.1 Experimental Setup
│   ├── Models & Baselines  (删除 SSP；主 backbones = Qwen2.5-7B + Llama3.1-8B；
│   │                        Self-RedTeam + MAGIC + SmoothLLM + Self-Eval)
│   ├── Training dataset    (保持)
│   ├── Training protocol   (保持 v4 脚本超参，仅微调语气)
│   └── Evaluation protocol (保持；引用附录 E.1–E.4)
│
├── §5.2 Defender Evaluation   — 三个 RQ，三张主表 + 1 简化 case study
│   ├── RQ1 Safety + Benign Compliance
│   │   → Table 1 (tab:evaluation_main)
│   │       Qwen2.5-7B block:  base / +Self-RedTeam / +MAGIC(数字) / +DACE(--)
│   │       Llama3.1-8B block: base / +Self-RedTeam / +MAGIC(数字) / +DACE(--)
│   │
│   ├── RQ2 General Capability
│   │   → Table 2 (tab:general_cap)
│   │       与 Table 1 同两 backbone 结构，数字填入 MAGIC 行
│   │
│   ├── RQ3 OOD Automated Red-Teaming (含 MAJIC)
│   │   → Table 3 (tab:harmbench_generalization)
│   │       Qwen2.5-7B block:  base / +Self-Eval / +SmoothLLM / +Self-RedTeam / +MAGIC / +DACE
│   │       Llama3.1-8B block: 同上
│   │       列： no-rev | GCG | PAIR | TAP | AutoDAN | AutoDAN-Turbo | MAJIC(新增)
│   │
│   └── Case Study (简化占位)
│       — 在 §5.2 末尾，1 个 attackerbox，写 "to be supplemented in camera-ready"
│
├── §5.3 Attacker Evaluation   — 两个 RQ，两张表 + 一张合并图
│   ├── RQ4 Attacker Transferability (MAGIC Table 10 style)
│   │   → Table 4 (tab:attacker-transfer)
│   │       行： Base / MAGIC-attacker(数字) / DACE-attacker(--)
│   │       列： Qwen2.5-7B-IT | Llama3.1-8B-IT | Mistral-7B-IT
│   │             | Gemini-2.5-Flash | MAGIC-defender | DACE-defender(新增)
│   │
│   ├── RQ5 Attacker Diversity: MAGIC vs DACE
│   │   → Table 5 (tab:attacker-diversity)
│   │       行 1 MAGIC last-15-steps (8gpu-tp2, ~64·4·15=3840 样本)
│   │       行 2 DACE  last-15-steps (sft-full, ~64·6·15=5760 样本)
│   │       行 3 DACE  final replay pool (~max_pool 4000 样本)
│   │       列： Coverage↑ | Shannon H↑ | QD-Score↑ | SBERT cos↓
│   │             | Self-BLEU↓ | Distinct-2↑ | n-gram entropy↑
│   │
│   └── Figure 3 (合并为单 figure, subfigure 左右)
│       左：DACE co-evolution heatmap (MAGIC Fig 3 等价)
│       右：DACE final replay pool 12×10 strategy-coverage heatmap
│            cell 颜色深浅 = 样本数；叠加数字 = 平均 posterior 有害性
│            (α+s)/(α+β+s+f)
│
└── (§5.4 Ablation 原位删除；整体下放到附录 F.2)
```

## 主文要删掉 / 下放 / 新增的片段

**删除**
- L620-642 Experimental Setup 内 SSP 相关句
- L692-693 Table 1 中 "+SSP" 行
- L725-726 Table 2 中 "+SSP" 行
- L767-768 Table 3 中 "+SSP" 行
- L782-800 当前 Table 4 (multi-turn) —— 整段下放到附录 §F.1
- L808-835 当前 Figure 3 + "tab:attacker-transfer" → 替换为新资产
- L849-874 当前 compact ablation table + §5.3 → 下放附录 §F.2（删 SSP-style 行）

**新增**
- 新 Table 4 attacker-transfer (MAGIC Table 10 style)
- 新 Table 5 diversity metrics (三行 × 七列)
- 新 Figure 3 (合并两张 subfigure)
- §5.2 末尾新增 1 个简化 case-study 占位 box

## 附录部分需新增 / 扩展的内容

**附录 E (Benchmark Protocols) — 扩展成 E.1–E.4 小节，MAGIC 风格 `\paragraph{}`**

```
§E.1 Safety Benchmarks
  \paragraph{WildGuardTest / WildJailBreak / HarmBench / DAN /
             OR-Bench-Toxic / XSTest / StrongREJECT}

§E.2 OOD Automated Red-Teaming Attackers
  \paragraph{PAIR / TAP / AutoDAN / AutoDAN-Turbo / MAJIC(新增)}
  — MAJIC: Markovian Adaptive Jailbreaking via Iterative Composition of
    Diverse Innovative Strategies. 960 迭代步内对 Qwen2.5-7B 达到 96.2% ASR。

§E.3 Multi-turn Red-Teaming
  \paragraph{X-Teaming}

§E.4 General Capability
  \paragraph{IFEval / ARC-C / GPQA / MMLU / AlpacaEval 2}
```

**附录 F (Expanded Results) — 重组为 F.1–F.6**

```
§F.1 Multi-turn Evaluation (MAGIC Table 4 style, 下放自主文旧 Table 4)
     行: base / +Self-RedTeam / +MAGIC(数字) / +DACE(--)

§F.2 Full Ablation Study (MAGIC Table 5 style, 6 行)
     行: base / +MAGIC(数字) / +DACE w/o SFT / +DACE w/o diversity
         / +DACE w/o replay / +DACE (full)
     列: WJB ASR↓ / StrongREJECT RTA↑ / WJB benign ASR↑ /
         XSTest Comply↑ / AlpacaEval 2 LC Win↑
     — SSP-style 行被用户明确要求删除

§F.3 14B Backbone Extended (Qwen2.5-14B 主表 1/2/3 复刻)

§F.4 Multi-level Diversity Full (Table 5 per-benchmark 完整版)

§F.5 Descriptor Faithfulness Audit + Judge Robustness Cross-Validation

§F.6 Per-seed Standard Deviations for Main Tables (camera-ready 填入)
```

**附录 H (Attack Patterns / Case Study) — 增补**

```
- 保留 Case H.1 占位
- 新增 Case H.2、H.3 占位（共 3 个 sanitized cases）
- 每个 case 字段：Raw Prompt / Declared (s,c) / Secondary Strategies
  / <think>/<strategy>/<answer> / Defender Verdict
```

## 写作风格与分析段落口径

- **planned tone**：所有主表分析段以 "we evaluate / we expect / we study / we anticipate / we hypothesize" 开头；不允许 "DACE achieves X" / "DACE outperforms Y"。
- **中文注释头**：沿用现有格式 `% [段 · RQk 分析] 大意 / 中文对应内容`。
- **每段段首 1 句话要点化**：MAGIC 风格。
- **表注（caption）一致性**：所有主表以 `\textbf{...}` 开头。
- **RQ 编号**：主文保留 5 个 RQ（RQ1 safety / RQ2 capability / RQ3 OOD / RQ4 attacker transfer / RQ5 diversity）。multi-turn 与 ablation 在附录用 `\paragraph{}` 表述。

## opus vs gpt 分析的采纳策略

**采纳 opus**：紧凑型主文（5 个主要可视资产）、Question-driven 段落、D1/D2/D3 三层多样性划分。

**局部借鉴 gpt**：Dataset & Attacker 描述更细致的 `\paragraph{}` 体 → 附录 E.1–E.4；多指标对比表 → 主文 Table 5；Judge robustness → 附录 F.5。

**不采纳**：PIA persona-invariant 表、query-efficiency 曲线、Ferret/RainbowPlus/QDRT 对比（超出主文空间且与 MAGIC 对齐原则冲突）。

## MAGIC 数字清单速查（直接填入 MAGIC 对应行）

**Table 1 — Qwen2.5-7B-Instruct**
```
base:          0.365, 0.038, 0.701, 0.327, 0.363, 0.250, 0.892, 0.800, 0.964, 0.992, 0.940
+Self-RedTeam: 0.255, 0.017, 0.442, 0.323, 0.237, 0.047, 0.973, 0.825, 0.988, 0.980, 0.904
+MAGIC:        0.023, 0.002, 0.198, 0.043, 0.055, 0.019, 0.977, 0.860, 0.988, 0.968, 0.945
```

**Table 1 — Llama3.1-8B-Instruct**
```
base:          0.187, 0.046, 0.659, 0.517, 0.213, 0.094, 0.881, 0.950, 0.983, 0.992, 0.908
+Self-RedTeam: 0.094, 0.003, 0.214, 0.239, 0.144, 0.044, 0.942, 0.943, 0.958, 0.936, 0.949
+MAGIC:        0.012, 0.002, 0.147, 0.050, 0.017, 0.000, 0.945, 0.960, 0.989, 0.968, 0.932
```
(列顺序: WG-Test adv, WG-Test van, WJB adv, DAN, HarmBench adv, HarmBench van, OR-Bench, XSTest RTA, StrongREJECT, WJB benign, XSTest benign)

**Table 2 — Qwen2.5-7B-Instruct**
```
base:          0.749, 0.824, 0.592, 0.342, 0.733, 33.733%
+Self-RedTeam: 0.728, 0.805, 0.592, 0.301, 0.735, 34.252%
+MAGIC:        0.745, 0.821, 0.592, 0.308, 0.735, 33.224%
```

**Table 2 — Llama3.1-8B-Instruct**
```
base:          0.736, 0.794, 0.561, 0.234, 0.684, 24.223%
+Self-RedTeam: 0.693, 0.777, 0.516, 0.286, 0.676, 21.406%
+MAGIC:        0.762, 0.835, 0.565, 0.239, 0.670, 24.122%
```

**Table 3 — Qwen2.5-7B-Instruct** (no-rev | GCG | PAIR | TAP | AutoDAN | AutoDAN-Turbo | MAJIC)
```
base:          25.62, 43.90, 44.38, 63.75, 47.81, 75.00, --
+Self-Eval:    24.06, 28.75, 37.19, 50.00, 42.81, 89.06, --
+SmoothLLM:    19.38, 20.00, 30.63, 61.25, 62.19, 70.31, --
+Self-RedTeam: 19.38, 22.50, 31.88, 40.00, 30.31, 66.88, --
+MAGIC:        13.44, 11.25, 25.31, 35.63, 24.38, 54.69, --
```
Table 3 Llama3.1-8B 所有行 = 全部 `--`（MAGIC 未公开 Llama3.1-8B OpenRT 数字）。

**Table 4 (attacker ASR, 600 WJB vanilla harmful, GPT-4o judge)**
```
Base-attacker:  @ Qwen2.5-7B-IT = 37.33, Llama3.1-8B-IT = 25.00,
                  Mistral-7B-IT  = 46.83, Gemini-2.5-Flash = 24.67,
                  MAGIC-defender = 10.50, DACE-defender = --
MAGIC-attacker: 58.00, 35.83, 64.17, 31.33, 9.00, --
DACE-attacker:  --, --, --, --, --, --
```

**附录 F.1 (Multi-turn X-Teaming)**
```
base Qwen2.5-7B: 0.949, --, 0.507, --
+Self-RedTeam:   0.899, 5.27%, 0.504, 0.6%
+MAGIC:          0.854, 10.1%, 0.430, 15.2%
```

**附录 F.2 (Full Ablation)** — WJB ASR↓ / StrongREJECT RTA↑ / WJB benign ASR↑ / XSTest Comply↑ / AlpacaEval 2
```
base:     0.701, 0.964, 0.992, 0.940, 33.733%
+MAGIC:   0.198, 0.988, 0.968, 0.945, 33.224%
其余 (w/o SFT / w/o diversity / w/o replay / DACE-full) 全部 `--`
```

## 文件修改清单（按序执行）

| Step | 文件 | 操作 |
|---|---|---|
| 1 | `neurips_2026.tex` §5.1 | 删除 SSP baseline 句；dataset/protocol 微调 |
| 2 | `neurips_2026.tex` Table 1 | 改两 backbone 版；MAGIC/base/Self-RedTeam 行填数字；删 SSP 行 |
| 3 | `neurips_2026.tex` Table 2 | 同 Step 2 |
| 4 | `neurips_2026.tex` Table 3 | 同 Step 2（Llama 块全 `--`）；保留 MAJIC 列 |
| 5 | `neurips_2026.tex` §5.2 末尾 | 插入简化 case study 占位 box |
| 6 | `neurips_2026.tex` 原 Table 4 (multi-turn) | 整体下放至附录 §F.1 |
| 7 | `neurips_2026.tex` 原 Figure 3 + "tab:attacker-transfer" | 替换为新 Table 4 + 新 Table 5 + 合并 Figure 3 |
| 8 | `neurips_2026.tex` §5.3 (Ablation) | 整节下放至附录 §F.2；删 SSP-style 行 |
| 9 | `neurips_2026.tex` 附录 E | 扩展为 E.1–E.4 |
| 10 | `neurips_2026.tex` 附录 F | 重组为 F.1–F.6 |
| 11 | `neurips_2026.tex` 附录 H | 增加 Case H.2 / H.3 占位 |

## Verification（实现结束后自检）

1. `pdflatex neurips_2026.tex` 编译无致命错误
2. 主文 + 附录 F 中 SSP 相关行全删（附录 I Table I.1 的 SSP 行保留作为 Related Work 讨论）
3. Table 1/2/3 各有 Qwen2.5-7B + Llama3.1-8B 两个 backbone block
4. 新 Figure 3 的 caption 同时提及 co-evolution heatmap 与 replay pool strategy distribution
5. 附录 E 有 `\paragraph{MAJIC}` 段
6. 附录 F 有 F.1 multi-turn、F.2 full ablation（6 行，无 SSP-style）、F.3 14B 扩展
7. 中文注释头风格一致；`rqbox` 编号连续 RQ1→RQ5
8. 与 MAGIC 一致的单元格数字已填入；DACE 行和 MAJIC 列仍为 `--`

## Open Questions（实现时处理）

1. **Llama3.1-8B 在 Table 3 全 `--`** — 默认保留两 backbone 结构（按用户指令），加 footnote "Llama3.1-8B OpenRT 结果在 camera-ready 补全"。
2. **Table 4 DACE-defender 列全 `--`** — 正确，等 DACE 评测完成。
3. **Table 5 MAGIC diversity 样本** — 实现阶段需跑 MAGIC 评测脚本；写作阶段按 `--` 处理。
4. **Figure 3 co-evolution checkpoint 数** — 写作阶段只写 "N×N cross-evaluation"，N 待定。
5. **简化 case vs 附录详细 case** — 主文用 1-sentence 预告 + 引用 App. H.1；附录 3 个 case 独立。
