# DACE 论文审查与分析报告

审查对象：

- 用户原始写作要求：`z_materials/paper_writing_prompt.txt`
- Claude 写作计划：`z_materials/A_DACE_Paper_Writing_Plan.md`
- Claude 论文实现：`z_materials/DACE_NeurIPS_2026/`
- DACE 方法与实现材料：`z_materials/研究方法v3.1.md`、`z_materials/dace_coding_v3.1.md`、`z_materials/dace_coding_debug_v4.md`
- 关键实现对照：`src/verl/verl/separated_trainer/ppo/archive_pool.py`、`src/verl/verl/separated_trainer/config/ppo_trainer.yaml`、`scripts/rl/separated/grpo_dace_diversity_v4.sh`

## 1. 总体判断

当前 DACE 论文源码是一个结构完整、叙事方向正确的高质量草稿，但还不能被视为可投稿成稿。它基本遵循了用户给 Claude 的大部分写作要求：参考 MAGIC 风格、保留 NeurIPS 模板注释、分章节组织、每个英文段落上方添加中文注释、使用 citation 占位符、将 related work 和完整伪代码放到附录，并围绕 DACE 的两个核心痛点（attack strategy collapse、defense adversarial forgetting）构建主线。

但从审查角度看，当前版本存在三类严重问题：

1. **事实性和实现一致性问题**：论文中多个超参数、机制描述和当前 v4 代码/脚本不一致。例如论文写默认 `gamma=0.97`、`n_min=8`、剪枝阈值 `0.05`，但 v4 脚本实际使用 `gamma_decay=0.90`、`prune_min_trials=2.0`、`prune_threshold=0.45`；论文正文还强调 over-saturated cell 产生 signed negative gradient，但实现默认 `clip_negative=True`。
2. **实验章节仍是计划稿，不是结果稿**：所有主表、图和 ablation 都是 `--` 或 placeholder，正文大量使用 “is expected to”。这与 introduction、abstract、conclusion 中已经用完成时宣称 DACE “attains lower ASR / improves safety / preserves utility” 直接冲突。
3. **理论与 reviewer 风险**：论文声称 “DACE leaves the game structure untouched, so all SPNE properties are inherited”，但 DACE 添加了多样性奖励、格式奖励和 replay 训练分布，严格来说已经改变了训练目标和有效 payoff；除非补充证明或降格表述，否则 reviewer 很容易质疑这是未经证明的理论继承。

建议定位为：**当前是 PhD-level paper scaffold + strong narrative draft，而不是 final paper**。下一步应先做“事实对齐”和“实验结果落地”，再做语言压缩与 reviewer-proofing。

## 2. 与用户原始要求的符合度

### 做得好的地方

- **论文主线符合用户要求**：论文围绕 DACE 的显式二维攻击策略空间、归一化覆盖奖励、Beta-Bernoulli replay pool 展开，和 `研究方法v3.1.md`、Claude plan 中的核心框架一致。
- **重点 gap 被纳入 introduction**：用户特别强调的 TriPlay-RL 和 SSP 两点都被写入了 introduction。TriPlay-RL 被定位为语义/表层多样性不足，SSP 被修正为“确实更新 replay 后验，但依赖离散 safety score”。
- **12×10 策略空间被正确使用**：论文正文与附录都说明了 Llama-Guard-4 原 14 类中剪掉 S12 Sexual Content 与 S14 Code Interpreter Abuse，保留 S1-S11 + S13；这与 v4 重建计划一致。
- **模板保留基本合规**：`neurips_2026.tex` 保留了大量原始 NeurIPS 模板注释，符合用户“不要删除模板注释”的要求。
- **中文注释要求基本满足**：各英文段落上方都有中文注释，说明大意、写作逻辑和中文对应内容。注释质量总体较高。
- **Related Work 和 pseudocode 放置符合计划**：正文 related work 很短，完整版本在 appendix；正文 algorithm 简化，完整 algorithm 放附录。

### 没完全做到或有风险的地方

- **“实验表格先做好，具体数据留白”被过度延伸到主结论**：用户允许表格数据留白，但不等于可以在 abstract、introduction contribution、conclusion 中提前宣称已经显著优于 baselines。当前主结论的语气比证据状态更强。
- **“实验分析和结论先按照预期理想情况写”需要显式标记为 draft**：当前文稿混合了 expected language 和 completed-results language，容易造成读者和 reviewer 误解。
- **参考文献占位符数量过多且年份含 2026**：这是用户允许的，但如果当前版本给外部读者看，会显得像大量未核验文献堆砌。尤其是 `llamaguard4_2026`、`triplayrl2026`、`ssp2026` 等必须后续逐条核验。
- **没有真正形成“审稿式保守 claims”**：很多地方用 “first”、“provably”、“absent in prior baselines”、“confirms” 等强词，当前证据支撑不足。

## 3. Author 视角：内容是否符合实际

### A1. 论文超参数与实现不一致

这是最需要立即修复的问题。论文实验设置写：

- `sections/experiments.tex:26`：`gamma=0.97`、`pruning thresholds epsilon=0.05 and n_min=8`
- `sections/appendix.tex:69-71`：附录超参表同样写 `gamma=0.97`、`0.05, 8`

但当前实现与 v4 脚本是：

- `src/verl/verl/separated_trainer/config/ppo_trainer.yaml`：默认 `gamma_decay=0.90`、`prune_threshold=0.35`、`prune_min_trials=2.0`、`max_pool_size=2000`
- `scripts/rl/separated/grpo_dace_diversity_v4.sh`：实际运行覆盖为 `gamma_decay=0.90`、`prune_threshold=0.45`、`prune_min_trials=2.0`、`max_pool_size=4000`
- `src/verl/verl/separated_trainer/ppo/archive_pool.py`：类默认 `gamma_decay=0.90`、`prune_threshold=0.35`、`prune_min_trials=2.0`、`max_pool_size=2000`

建议：

- 如果论文描述的是 v4 主实验，应把正文和附录统一改为 `gamma=0.90`、`n_min=2`、主脚本 `prune_threshold=0.45`、`max_pool_size=4000`。
- 如果最终想用更保守的 `gamma=0.97`、`n_min=8`，需要同步训练脚本并重跑实验，不能只在论文中写。
- 附录超参表应区分 “config default” 和 “main experiment override”，否则会继续混乱。

### A2. 负 diversity reward 的描述与实现不一致

论文方法写：

- `sections/method.tex:90`：over-saturated cell “is pushed toward or below zero, providing a strong, signed gradient”
- 中文注释也说负值可提供 signed gradient

但实现默认：

- `archive_pool.py` 中 `clip_negative=True`
- `scripts/rl/separated/grpo_dace_diversity_v4.sh` 显式传入 `algorithm.replay_pool.clip_negative=True`
- 实际 `compute_diversity_reward` 会 `return max(0.0, r_div)`

这意味着主实验默认没有 negative/signed penalty，最多是不给多样性奖励。当前论文的 signed-gradient 说法是不符合实现的。

建议改法：

- 方法正文改为：“By default we clip negative gains to zero for stability; ablations can disable clipping to study signed penalties.”
- 不要把 “strong signed gradient” 当成主方法优势，除非最终实验确实关闭 `clip_negative`。
- 公式后补一句实现细节：`R_div <- max(0, R_div)` in main experiments。

### A3. DACE 是否“继承 MAGIC 的 SPNE 保证”表述过强

`sections/preliminaries.tex` 写 DACE “leaves the game structure untouched---so all SPNE properties are inherited”。但 DACE 实际做了：

- attacker reward 增加 `R_fmt` 和 `lambda R_div`
- defender training batch 加入 replay distribution
- archive posterior 和 Thompson sampling 改变训练数据分布

这些不会简单地保持 MAGIC 的原始零和/序贯博弈 payoff。最多可以说 DACE 继承 MAGIC 的 attacker-defender interaction order 和 effectiveness component 的零和结构；多样性和 replay 是训练-time regularization / data selection mechanisms，不应直接宣称继承理论保证。

建议：

- 把 “all SPNE properties are inherited” 降格为 “we build on the same asymmetric sequential interaction; our additions are training-time mechanisms rather than a new interaction protocol.”
- 如果要保留 SPNE 说法，需要增加 proposition，明确 augmented payoff 下的 equilibrium 是什么，以及 diversity regularizer 是否进入 attacker utility。
- 否则 reviewer 会抓住 “additional reward breaks zero-sum” 这一点。

### A4. “combinatorial attack emergence” 目前是强 claim，但证据为空

论文多处宣称组合式攻击涌现：

- `sections/intro.tex:12` figure caption 说 prior co-evolution baselines 未观察到
- `sections/intro.tex:34` 说 mid-to-late training 观察到 MAGIC/Self-RedTeam 未报告的新行为
- `sections/experiments.tex:162-166` 有 case study placeholder
- `sections/appendix.tex:220-239` 组合攻击案例表仍为空

如果当前没有日志、案例、标注协议和 baseline 对比，这个 claim 过强。

建议：

- 在实验完成前，abstract/conclusion 中不要把 combinatorial emergence 写成已证实结果。
- 最少需要：若干 sanitized examples、post-hoc multi-label strategy annotation、和 MAGIC/TriPlay/SSP 同 seed prompt 的对比。
- 需要定义 emergence 的判据：单 prompt 涉及多个 risk？多个 style？自声明策略与实际文本策略不一致是否也算？

### A5. SFT 数据和 benign 模板统计要核验来源

论文附录写：

- `~43K` Gemini-2.5-Pro distilled CoT samples
- v3 benign unsafe rate `43%`
- revised template brings benign not-safe rate to `<=10%`

但 v4 debug 文档写的是：

- v3 benign 数据 Guard non-safe `68.2%`
- 目标 not-safe rate `<=20%`

论文中的 `43%` 和 `<=10%` 与 `dace_coding_debug_v4.md` 不一致，除非另有实验记录支撑。这里尤其敏感，因为它用于证明 v4 benign 数据清洗有效。

建议：

- 从实际 `check_benign_data_quality.py` 输出日志确认最终数值。
- 未确认前写成 “we reduced the benign not-safe rate substantially; exact statistics are reported in Table X”，不要写具体百分比。
- 如果保留具体数值，附录应注明数据版本、样本数、judge、日期和脚本。

### A6. 训练与评估资源声明可能不实

`sections/appendix.tex` 写 “trained under identical compute budgets on an 8xH100 node”、“mean across three independent seeds”。如果当前没有实际完成三种子训练，这就是不符合实际的 claim。

建议：

- 草稿阶段可写 “Our planned protocol uses...”
- 成稿阶段必须用实际训练记录替换，包括 GPU 型号、数量、训练步数、总 token、wall-clock、seed 数。

### A7. “release code / archive / defender weights” 需要与真实发布策略一致

论文 abstract、intro、appendix 都提到 release code、strategy-indexed adversarial replay pool、defender weights、不发布 attacker weights。若团队尚未决定发布范围，这会引发 reproducibility 和 safety release policy 问题。

建议：

- 投稿前统一改成实际 release plan。
- 如果双盲投稿，不要写会暴露身份的 repo 信息；可以写 “We will release...” 但不要过度承诺 archive 全量 release。

## 4. Reader 视角：哪里读不懂或体验不好

### R1. Introduction 信息密度过高

Introduction 四段结构是对的，但每段都很长，citation 密度很高，读者需要同时处理：

- jailbreak 演化线
- co-evolution / SPNE / Nash
- diversity 两大流派
- TriPlay-RL 的细节批判
- SSP replay 的三维局限
- DACE 的两个组件
- combinatorial emergence

问题不是内容错，而是 reader 的认知负荷太高。尤其第 3 段（`sections/intro.tex:29`）长到几乎变成 related work + 方法动机混合段。

建议：

- Introduction 第 3 段拆成两个英文段落：Diversity gap 和 Replay gap。
- 每个 gap 用 “Why not existing diversity?”、“Why not existing replay?” 两句 topic sentence 开头。
- 把部分 citation 列表移到 related work，intro 只保留最关键的 2-3 个对比。

### R2. “risk category”和“attack style”的关系需要更直观解释

方法中定义了 `B = S x C`，但普通读者可能不清楚一个 prompt 为什么只能落入一个 risk 和一个 style。现实攻击可能天然 multi-risk/multi-style，而论文又宣称后期出现 combinatorial emergence，二者之间存在张力。

建议：

- 在 `Explicit Attack Strategy Space` 中加入一句：训练奖励使用 attacker self-declared primary descriptor；post-hoc analysis 可多标签标注 secondary descriptors。
- 明确 primary strategy descriptor 是训练控制变量，不是声称攻击真实语义只有一个类别。
- 这能缓解 reader 对 “组合攻击为何还能用单 cell coverage 训练” 的困惑。

### R3. Replay posterior 中 success/failure 定义不够清楚

方法写 “attack broke through / attack refused”，但 DACE 同时处理 harmful seed 和 benign seed。实现中 `attack_success` 对 harmful 和 benign 的定义不同：

- harmful prompt：defender unsafe response 算 success
- benign prompt：defender unsafe response 或 refusal 算 success（即诱导过拒也算攻击成功）

论文方法没有清楚说明这个双定义，reader 会疑惑 benign replay 的 posterior 表示什么威胁。

建议：

- 在 replay posterior 段落补一句：for harmful seeds, success means unsafe compliance; for benign seeds, success means unsafe response or over-refusal, following the dual safety objective.
- 表格中把 harmful ASR 和 benign over-refusal 明确分开。

### R4. 实验章节读起来像 proposal，不像 paper

实验表格都是 `--`，图都是 `\fbox` placeholder，解释段都是 “expected to”。这对内部 draft 可以接受，但外部 reader 会认为论文尚未完成。

建议：

- 如果短期内没有结果，就把 `Experiments` 改名为 `Planned Evaluation` 并不要放到投稿版。
- 如果要投稿，必须填入真实数值、图和统计显著性，所有 expected 语句改为 observed result。
- Abstract、intro contribution 和 conclusion 必须与结果同步降格或更新。

### R5. NeurIPS page budget 风险

主文当前包括大量中文注释、placeholder figures 和长实验表，编译后几乎必然超过 9 页。虽然中文注释在 LaTeX 中是注释不会显示，但占位图和表会占页。正文 related work 虽短，method + experiments 已经很长。

建议：

- 投稿版保留中文注释在源码没问题，但最终编译需要确保不会影响；注释本身不会显示。
- Figure 1 和 Figure 2 若都为大图，experiments 中的 Figure 3/4/5/6 至少要移 2-3 个到 appendix。
- 主文 experiments 最多保留：main safety table、OOD robustness table、strategy heatmap、forgetting curve、one compact ablation table。

## 5. Reviewer 视角：逻辑、证据和可攻击点

### V1. Novelty 可能被质疑为“MAGIC + diversity reward + replay”

论文已经努力把主线提升为 “coverage x memory”，这是正确方向。但 reviewer 仍可能认为：

- 显式 strategy grid 类似 QD descriptor archive
- normalized entropy gain 是 coverage shaping
- Beta-Bernoulli Thompson replay 是 bandit/replay 的标准组合
- 在 MAGIC 上拼接这些模块是否足够 NeurIPS novelty？

建议强化 novelty 的边界：

- 明确 DACE 的新意不是任一单个模块，而是 dynamic co-evolution 下将 strategy-level coverage 和 posterior threat memory 联合建模。
- 实验必须证明单模块拼接不够：`w/o coverage`、`uniform replay`、`SSP-style discrete replay`、`textual diversity reward` 都应显著弱于 full DACE。
- 方法中避免把标准 Beta/Thompson 写成“核心理论创新”，应写成“principled adaptation to defender non-stationarity”。

### V2. 强 baseline 可复现性和公平性会被审查

论文计划比较 Self-RedTeam、MAGIC、SSP、TriPlay-RL、SEAS、AdvEvo-MARL、Rainbow Teaming 等，但很多可能没有公开代码或训练成本不同。Reviewer 会问：

- 是否真的复现了所有 baselines？
- 是否使用相同 attacker SFT seed set？
- 是否每个 baseline 都调参充分？
- 如果 SSP 是 2026 论文，是否能复现其 reflective replay？

建议：

- 主文只保留能真实、可靠复现的 baselines。
- 对难以复现的 baselines 标为 “reported result” 或移到 appendix。
- 必须有 compute parity table：训练 steps、tokens、rollout.n、judge、seed、defender base。

### V3. Strategy descriptor 由 attacker 自声明，可能被 reward hacking

DACE 直接从 `<strategy>` 中 regex 提取 `(risk, style)`。这降低 judge 噪声，但也引入新风险：attacker 可能声明冷门策略以拿 diversity reward，但实际文本并没有使用该策略。

论文现在说 “self-consistent” 和 “removes circular dependency”，但没有充分处理 misdeclaration/reward hacking。

建议：

- 增加 descriptor faithfulness audit：随机抽样 N 条，由 independent judge 或规则模型判断 declared strategy 是否与实际 rewrite 匹配。
- 报告 `strategy declaration accuracy` 或 `descriptor consistency rate`。
- 在方法中承认 self-declared descriptor 是 noisy control signal，并说明 format reward + SFT warm start + audit 如何缓解。

### V4. 归一化 coverage reward 的理论解释有数学细节风险

当前 KL 解释方向基本正确，但 `sections/method.tex:102` 中 “forward KL is zero-avoiding, so empty cells exert strongest pull” 需要谨慎。对于离散 empirical distribution，`D_KL(p || u)` 中 `p_b=0` 的项是 `0 log 0/u = 0`，不是发散；发散的是反向 KL `D_KL(u || p)` 或涉及 log p 的梯度在边界附近问题。当前 “p_b -> 0 时 forward KL 发散” 的中文 plan/注释逻辑不严谨，英文虽然没有直接写 “diverges”，但 “zero-avoiding” 说法仍容易被理论 reviewer 抓住。

建议：

- 删除 “zero-avoiding” 或改成更准确的经验分布/边际熵增益说明：adding a sample to an empty or low-count cell yields the largest marginal entropy gain under the current count vector。
- KL 视角只保留恒等式和 “entropy maximization equals KL reduction to uniform”。
- 如果要讨论梯度，避免在 simplex boundary 上做不严谨陈述。

### V5. “i.i.d. Bernoulli” 与 non-stationary defender 有内在矛盾

方法中写每个 entry 的 success/failure history 是 i.i.d. Bernoulli trials，但下一段又说 defender continuously trained, older evidence less informative。严格来说，在 defender drift 下这些 trial 不是 i.i.d。

建议：

- 改为 “We use a Beta-Bernoulli filtering approximation, treating recent decayed outcomes as pseudo-counts for the current threat probability.”
- 不要声称 i.i.d.，只说 conjugate update is used before decay / with exponentially discounted pseudo-counts。

### V6. “SSP 离散 score 不能表达不确定性”表述需要更精确

SSP 如果保存 replay 次数和 score history，也可能间接表达 confidence。当前论文把 SSP 说成 “a sample tried once and a sample verified a hundred times contribute identically”，这可能过强，除非 SSP 原文确实如此。

建议：

- 核验 SSP 论文原文后再定稿。
- 更稳妥说法：SSP's replay priority is based on a discrete point estimate rather than an explicit posterior distribution; it does not expose uncertainty in the sampling rule in the way Thompson sampling does。
- 避免 “identically” 这种绝对词，除非有源码/公式支撑。

### V7. Empirical claims 不能前置

`sections/intro.tex:43` 和 conclusion 明确写 DACE 已经优于 MAGIC/Self-RedTeam/SSP。当前没有结果，reviewer 会直接判定为 unsupported claims。

建议：

- 草稿版可以保留，但最终投稿前必须要么填结果，要么删除这些完成时宣称。
- Abstract 中 “Across benchmarks, DACE attains...” 应在结果未完成前改为 “We evaluate...” 或删掉。

## 6. 逐章节具体问题与修改建议

### Title / Abstract

优点：

- 标题清楚，DACE acronym 和方法主线对齐。
- Abstract 结构接近 Claude plan 中的 8 句模板。

问题：

- Abstract 直接宣称 lower ASR、preserves utility、broader strategy coverage，但实验尚未填数。
- “We release the code and replay pool” 需确认发布策略。
- “is pruned only when repeatedly dismissed by an up-to-date defender” 与实际 `prune_min_trials=2`、`prune_threshold=0.45` 不完全匹配；2 次 trial 不能说 repeated 很强。

建议：

- 结果未完成前，把最后两句改成 planned/evaluation framing。
- 成稿后补具体数字，至少给 2-3 个主要结果，例如平均 ASR 降低、coverage 提升、benign compliance 差异。

### Introduction

优点：

- 问题设定强，双病态框架清晰。
- TriPlay-RL 和 SSP 的 gap 比较贴合用户要求。

问题：

- 第三段过长，包含过多 related work 和方法细节。
- “provably keep up” 和 “shallow equilibrium” 等理论词过强。
- `combinatorial emergence` 还没有证据支撑。

建议：

- 拆段，降低 citation 密度。
- 把 “we find” 和 “we observe” 绑定到具体实验/图；如果图还没出，先改为 hypothesis 或 remove。
- contributions 的 empirical bullet 在结果完成前用 TODO 标记或弱化。

### Related Work

优点：

- 正文短，符合 plan。
- 三段结构与 DACE gap 对齐。

问题：

- 引用覆盖很广，但部分文献可能只是占位，容易显得堆砌。
- “None of these address...” 过绝对，容易被 prior work 反驳。

建议：

- 改成 “do not jointly model strategy-level coverage and posterior threat memory”。
- 对最接近的 2-3 篇加更具体的差异表，减少大范围 sweeping claim。

### Preliminaries

优点：

- 用两个 definition 把 collapse 和 forgetting 形式化，结构清晰。

问题：

- Attack Strategy Collapse 的 `H << log |B|` 不是可检验定义，`<<` 过模糊。
- Defense Forgetting 写 safety rate “non-increasing in t” 太强，真实曲线可能波动。
- SPNE 继承 claim 是最大理论风险。

建议：

- 定义 collapse 指标为 normalized entropy / evenness 低于阈值，或 max-cell share 高于阈值。
- Forgetting 改为差值指标：`F(t0,t)=ASR_t(H_t0)-ASR_t0(H_t0)`，若显著为正则遗忘。
- 删除或弱化 SPNE inheritance。

### Method

优点：

- 方法组件完整，和实现大体一致。
- 归一化 coverage reward 的动机明确。
- replay pool 的数据结构、posterior、decay、Thompson sampling、pruning 写得清楚。

问题：

- signed negative reward 与 `clip_negative=True` 不一致。
- `lambda(x)` 中 “success = defender unsafe” 没覆盖 benign over-refusal。
- KL zero-avoiding 说法不严谨。
- i.i.d. Bernoulli 与 non-stationarity 矛盾。
- 公式中的 `epsilon` 同时用于 coverage smoothing 和 prune threshold，容易混淆。

建议：

- 用不同符号：coverage smoothing 用 `\varepsilon_{\mathrm{div}}`，pruning threshold 用 `\tau_{\mathrm{prune}}`。
- 明确 main implementation clips negative diversity reward。
- 对 replay posterior 使用 discounted pseudo-count wording。
- 增加 self-declared strategy 的 audit 说明。

### Experiments

优点：

- RQ 设计很完整，覆盖 safety、utility、OOD attackers、diversity、forgetting、ablation、co-evolution dynamics。
- 表格结构基本合理。

问题：

- 目前完全是 placeholder，不支撑论文 claims。
- RQ 太多，主文篇幅可能爆炸。
- 一些 benchmark 名称和评测协议需要核验，例如 Auto-RT、AutoDAN-Turbo、MAJIC、X-Teaming 的可用性和默认协议。
- “GPT-4o independent verifier” 是外部闭源 judge，需报告 prompt、temperature、版本和日期；双盲下还要注意 API reproducibility。

建议：

- 主文保留 4 个核心 RQ：safety、utility、OOD、diversity/forgetting。Co-evolution matrix 移到 appendix。
- 所有 “expected to” 在成稿中必须改为结果驱动表述。
- 增加 statistical reporting：3 seeds mean/std 或 bootstrap CI。
- 增加 cost/fairness table。

### Appendix

优点：

- 附录结构合理，包含 algorithm、strategy space、prompts、training setup、benchmark protocols、expanded results、dynamics、qualitative examples、related work、ethics。

问题：

- 大量占位内容仍写成完成时，例如 “confirms that ranking is robust”。
- 超参表与实现不一致。
- Strategy space pruning evidence figure 是 placeholder，但正文依赖该证据。
- Broader impact 的 release policy 可能未确认。

建议：

- 所有 placeholder appendix 章节用 TODO 或 draft 标记，不要用完成时。
- 优先填 Strategy Space pruning 的真实统计图，因为这是方法设计正当性的关键证据。
- 附录 prompt 模板至少需要放完整关键文本，否则 reproducibility 不够。

## 7. 优先级修改清单

### P0：必须先修，否则不能投稿

1. **统一论文和实现超参数**：修正 `gamma`、`prune_threshold`、`n_min`、`max_pool_size`、`clip_negative`。
2. **降格所有未验证实验 claim**：abstract、intro contributions、conclusion 中的 “attains / improves / preserves / confirms” 需要等结果出来后再写。
3. **修正 SPNE 继承表述**：避免未证明理论保证。
4. **修正 negative reward / signed gradient 描述**：与 `clip_negative=True` 对齐。
5. **修正 KL zero-avoiding / i.i.d. Bernoulli 的理论表述**。

### P1：强烈建议在实验前完成

1. 增加 strategy declaration faithfulness audit。
2. 重新整理 experiment RQ，把主文压缩到可支撑核心 claim 的最小集合。
3. 确认 SSP、TriPlay-RL、MAJIC、AutoDAN-Turbo 等 citations 和 baseline 实现可用性。
4. 确认 benign SFT v4 的真实 Guard not-safe 率，并替换附录数值。
5. 把 “success” 在 harmful / benign seed 下的定义写清楚。

### P2：结果完成后再做

1. 用真实热力图替换 Figure 1 / Figure 3。
2. 用真实 forgetting curve 和 cross-evaluation matrix 替换 placeholder。
3. 填充所有 main tables 和 appendix tables。
4. 添加 2-3 个 sanitized combinatorial attack case，并给出 annotation protocol。
5. 压缩 introduction 和 method，控制 NeurIPS 主文页数。

## 8. 建议的成稿策略

建议把论文分成两个版本维护：

### 内部写作版

保留中文注释、placeholder、expected analysis、完整 plan 式文字，方便继续协作。

### 投稿编译版

必须满足：

- 无 placeholder 图表
- 无 expected-to 结果段
- 所有 claims 有数字或图支持
- 超参数与脚本一致
- 理论 claim 保守
- appendix 中的 reproducibility 信息完整

具体执行路径：

1. 先修 `Method` 和 `Experiment Setup` 的事实一致性。
2. 跑最小主实验：Qwen2.5-7B 主 backbone，Base / MAGIC / SSP / DACE，至少 safety + utility + strategy coverage + forgetting。
3. 如果结果支持，再扩展 OOD attackers 和 ablations。
4. 结果不支持时，优先调整论文 claim，而不是强行维持当前 ideal-result 叙事。

## 9. 简短结论

Claude 写出的 DACE 论文框架方向正确，写作风格也明显参考了 MAGIC/ReMA/SIE 的论文组织方式。最大价值在于它已经把 DACE 的故事从“给 MAGIC 加两个模块”提升成了“coverage + memory 的协同演化设计原则”。这是一个不错的论文骨架。

但当前版本最大问题是：**论文声称、Claude plan 和实际 v4 实现之间还没有完全对齐，且实验章节仍是预期结果而非真实结果**。如果现在给 reviewer 看，最可能被攻击的点不是英文，而是 unsupported empirical claims、theory overclaim、self-declared strategy reward hacking、以及超参数/实现不一致。

推荐下一轮修改目标不是继续润色语言，而是先做 “truth pass”：逐句检查每个 claim 是否能由当前代码、日志、实验或已核验文献支撑。完成 truth pass 后，再进入 NeurIPS-style compression 和 reviewer-proofing。
