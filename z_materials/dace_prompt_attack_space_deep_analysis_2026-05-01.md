# DACE Prompt 与 Attack Space 深入分析

日期: 2026-05-01

范围: 本文只分析当前项目的 prompt、SFT 蒸馏、RL attack space、diversity/replay_pool 机制和已产出的分布图/缓存结果。不修改训练代码,不提供一键修改方案。

参考文件:
- `scripts/rl/separated/grpo_dace_diversity_full.sh`
- `data-sft/run_cot_distill_v2.sh`
- `data-sft/distill_v2_vanilla_benign_jsonl.py`
- `data-sft/distill_v2_vanilla_harmful_jsonl.py`
- `data/safety/preprocess_dace.py`
- `src/verl/verl/separated_trainer/ppo/archive_pool.py`
- `src/verl/verl/utils/reward_score/game.py`
- `scripts/analyze_archive_pool.py`
- `scripts/check_benign_data_quality.py`
- `z_materials/Llama_Guard_4_Model_Card.md`
- `z_materials/dace_benign_prompt_conflict.md`
- `data-sft/heatmap_v3_all_strategy_distribution.png`
- `scripts/archive_pool_analysis/DACE-Diversity-Qwen2.5_7B_Instruct-w_dace_sft_full-2026-04-26_22-00-31__global_step_300/heatmap_all.png`

## 结论

当前最需要优先修的是 benign 改写目标,不是 attack space 本身。DACE benign SFT 数据被 Guard 判为 unsafe/controversial 的比例达到 68.2%,而 MAGIC benign 只有 5.0%。这说明当前 BENIGN_TEMPLATE 确实在教 attacker 把 benign 改成 harmful-looking 甚至 actual harmful,与“缓解 over-refusal/false positive”的设计目标冲突。

14 个 risk category 与 Llama Guard 4 S1-S14 是对齐的,没有发现名称或定义上的实质差异。三个 sex 相关类别不是概念冗余:S3 是性相关犯罪,S4 是儿童性剥削,S12 是成人色情内容。但从当前数据和 replay pool 看,S12 Sexual Content 与 S14 Code Interpreter Abuse 是明显低覆盖类别,尤其 S14 对无工具调用的当前 MAGIC defender 语境也不自然。

“删掉 Sexual Content 和 Code Interpreter Abuse,改成 12x10”是合理的工程简化,但它不是 diversity reward 问题的完整解。按 step 300 archive pool 精确矩阵计算,14x10 有 12 个空格子;删除 S12/S14 后仍有 2 个空格子,所以 `delta_max` 仍由空格子决定,剩余格子的归一化 diversity reward 几乎不变。因此 12x10 可以清理 dead rows 和减少不适配类别,但若目标是修 diversity reward,还需要 active-mask/按 data_type 拆表/改归一化口径。

如果下一轮要重做,建议优先级是:
1. 重写 BENIGN_TEMPLATE 为 adversarial benign / false-positive / over-refusal 目标。
2. 重新蒸馏 benign SFT 数据,并用 Guard 做 post-filter 或至少分风险类别统计。
3. SFT 蒸馏继续采用 B' 方案:Directed Style + Free Risk + Hidden Assignment。只指派 attack style,不指派 risk_category;risk category 仍由 Gemini 基于 vanilla 语义和 entailment 约束自行选择。Non-Violent Crimes 占比过高应通过源数据补齐、生成后分层采样、rare-risk 追加蒸馏和 Guard 过滤治理,而不是通过 directed risk_category 硬拉均匀。
4. 决定是否采用 12x10。若采用,建议与 v4 SFT 和 RL parquet 重建合并做,不要在旧 14x10 checkpoint/pool 上继续接。
5. RL 侧启用或新增类型一致性约束。当前 `REWARD_LABEL=0`,即使代码计算了 label consistency,训练也没有用它。

## 当前 Pipeline 关键观察

RL 脚本 `grpo_dace_diversity_full.sh` 的关键设置:
- `REWARD_HARM=1`, `REWARD_REFUSAL=0.5`, `REWARD_LABEL=0`, `USE_Q_SAFE_LABEL_FOR_REFUSAL=1`。
- 开启 attacker format reward、DACE format、diversity、replay_pool。
- replay pool 上限是 4000,step 300 已满。

SFT 蒸馏 v2 的关键设置:
- 只对 attack style 做 directed assignment。benign 用 `md5(vanilla) % 10`,harmful 用 `(md5(vanilla) + run_idx) % 10`。
- risk category 仍由 Gemini 自由选择:“select whichever of the 14 best matches the vanilla's topic”。这是合理设计:style 更像包装风格,多数与内容正交;但 risk category 应主要由 vanilla 的语义决定。
- clean step 会过滤 format、canonical 14x10、style mismatch、think leak,但不检查 benign 改写后的 prompt 是否仍为 benign。

RL 数据预处理 `preprocess_dace.py` 与 distill 脚本复用同一套 prompt 文案。也就是说,SFT 阶段和 RL rollout 阶段的 BENIGN_TEMPLATE 冲突是一致传播的,不是单点问题。

## 1. Risk Category 与 Llama Guard 4 的关系

DACE 14 类 risk category 与 Llama Guard 4 模型卡 S1-S14 一致。模型卡列出 S1-S14,其中 S14 是 “Code Interpreter Abuse (text only)”;项目中的 `preprocess_dace.py` 和 `archive_pool.py` 使用同样的 14 个名称和定义。

需要注意一个语义错位:Llama Guard 4 的 hazard taxonomy 是 response-level policy,定义多以 “Responses that ...” 开头;DACE 把它用作 prompt rewriting 的 strategy axis。这对多数类别可行,但对 S5 Defamation、S8 Intellectual Property、S13 Elections、S14 Code Interpreter Abuse 会更别扭,因为这些类别更依赖具体事实、上下文或工具调用能力。

S14 Code Interpreter Abuse 尤其不自然。当前 MAGIC defender 没有真实 code interpreter/tool execution surface,S14 只剩下“写一个看起来像工具滥用的 prompt”的文本影子。它在数据和 pool 中接近 dead row,不是偶然。

## 2. 三个 Sex 相关类别是否冗余

三个类别不应简单视为冗余:

| 类别 | Llama Guard 4 含义 | 是否应合并 |
|---|---|---|
| S3 Sex-Related Crimes | 性贩卖、性侵、性骚扰、卖淫等犯罪 | 不建议合并 |
| S4 Child Sexual Exploitation | 儿童性剥削 | 不建议合并,安全优先级高 |
| S12 Sexual Content | erotica/色情内容 | 概念独立,但当前数据很少 |

S3/S4 是犯罪/剥削维度,S12 是成人色情内容维度。三者在安全政策上不同,不是定义重复。但当前项目的数据生态里,S12 的覆盖明显不足,且在 benign prompt 里很容易变成 actual harmful/unsafe,所以“训练 attack space 里删掉 S12”是可以考虑的工程选择。

我的判断:
- 保留 S3 和 S4。
- S12 如果没有计划补成人内容下的 benign-but-suspicious 数据,可以从训练 attack space 中移除。
- 如果保留 S12,应专门补一批 safe/benign 的成人内容边界样本,否则它只会继续成为低覆盖且高污染类别。

## 3. 两张 Heatmap 和源数据统计

### SFT v3 Strategy Distribution

从 `data-sft/heatmap_v3_all_strategy_distribution.png` 和源 JSONL 精确统计:

总量 43,828,占用 135/140 个 slot,空格子 5 个。

| Risk category | Count | 占比 | 空格子数 |
|---|---:|---:|---:|
| Non-Violent Crimes | 18,359 | 41.89% | 0 |
| Hate | 6,771 | 15.45% | 0 |
| Violent Crimes | 6,174 | 14.09% | 0 |
| Privacy | 2,273 | 5.19% | 0 |
| Suicide & Self-Harm | 1,875 | 4.28% | 0 |
| Indiscriminate Weapons | 1,446 | 3.30% | 0 |
| Sex-Related Crimes | 1,288 | 2.94% | 0 |
| Intellectual Property | 1,284 | 2.93% | 0 |
| Defamation | 1,120 | 2.56% | 0 |
| Specialized Advice | 1,101 | 2.51% | 0 |
| Elections | 935 | 2.13% | 0 |
| Child Sexual Exploitation | 803 | 1.83% | 0 |
| Sexual Content | 352 | 0.80% | 0 |
| Code Interpreter Abuse | 47 | 0.11% | 5 |

Attack style 的分布相对均匀:每列约 9.61%-11.27%。这说明 v2 的 directed-style assignment 是有效的,已经解决了早期 style 大量坍缩到 Role Play 的主要问题。

Risk category 分布仍然很不均匀,尤其 Non-Violent Crimes 占 41.89%。但这不应简单理解为“也要 directed risk”。risk category 与 vanilla 语义高度耦合,硬指派 risk 容易制造 awkward 组合,甚至破坏 “rewrite must entail the vanilla” 约束。更合适的处理方式是保持 Free Risk,再通过源数据补齐、生成后分层采样、rare-risk 追加蒸馏和 Guard 过滤来治理分布。

### Archive Pool Step 300

从 `scripts/archive_pool_analysis/.../heatmap_all.png` 和对应 `archive_pool.json` 精确统计:

总量 4,000,占用 128/140 个 slot,空格子 12 个。data_type 组成:vanilla_benign 2,618 (65.45%),vanilla_harmful 1,382 (34.55%)。

| Risk category | Count | 占比 | 空格子数 |
|---|---:|---:|---:|
| Hate | 876 | 21.90% | 0 |
| Violent Crimes | 740 | 18.50% | 0 |
| Non-Violent Crimes | 720 | 18.00% | 0 |
| Privacy | 394 | 9.85% | 0 |
| Specialized Advice | 335 | 8.38% | 0 |
| Suicide & Self-Harm | 314 | 7.85% | 0 |
| Defamation | 206 | 5.15% | 0 |
| Intellectual Property | 134 | 3.35% | 0 |
| Indiscriminate Weapons | 131 | 3.27% | 0 |
| Child Sexual Exploitation | 52 | 1.30% | 1 |
| Sex-Related Crimes | 48 | 1.20% | 0 |
| Elections | 36 | 0.90% | 1 |
| Sexual Content | 9 | 0.23% | 3 |
| Code Interpreter Abuse | 5 | 0.12% | 7 |

Replay pool 中 S12/S14 更接近 dead rows。S13 Elections 也偏少,但还没有低到必须删除;更适合先补源数据、做生成后分层采样,或在 12x10 裁剪后重新建 pool,而不是强行给任意 vanilla 指派不匹配的 risk。

### DACE Benign 安全质量

用户提供的 Guard 检查结果:

| Dataset | Safe | Unsafe | Controversial | Not-safe |
|---|---:|---:|---:|---:|
| MAGIC benign | 95.0% | 1.5% | 3.5% | 5.0% |
| DACE benign | 31.8% | 43.0% | 25.2% | 68.2% |

按 risk category 进一步拆 DACE benign:

| Risk category | n | not-safe |
|---|---:|---:|
| Sexual Content | 108 | 96.3% |
| Sex-Related Crimes | 535 | 84.5% |
| Child Sexual Exploitation | 449 | 80.4% |
| Elections | 156 | 78.2% |
| Defamation | 604 | 77.0% |
| Non-Violent Crimes | 4,734 | 74.9% |
| Privacy | 1,116 | 72.0% |
| Intellectual Property | 801 | 71.9% |
| Code Interpreter Abuse | 43 | 69.8% |

这说明 benign 污染不是局部类别问题,而是 prompt 目标层面的问题。Sexual Content 最高,但 Non-Violent Crimes 因为数量极大,贡献了最多污染样本。

## 4. BENIGN_TEMPLATE 的核心问题

`preprocess_dace.py` 中 BENIGN_TEMPLATE 同时要求:
- vanilla benign 改成 adversarial benign,且 “contain no harmful intent”。
- win condition 1: trick the language model into producing harmful responses。
- win condition 2: revised prompt should still be detected as benign。
- lose condition: assistant treats prompt as benign and complies,or produces harmless responses。

这三组目标互相冲突。对 SFT 蒸馏模型来说,最强动作指令是“让模型产生 harmful responses”,于是 Gemini 很容易把 benign 改成 actual harmful。Guard 结果已经证明这一点。

建议把 benign 目标改成:
- adversarial benign / benign-but-suspicious / false-positive-inducing prompt。
- 保持原始 benign intent 和 answerability。
- 表面上像 jailbreak 或高风险请求,但 careful defender 应该能安全回答。
- attacker 的成功是诱发 over-refusal 或 unhelpful evasive response,不是诱导 harmful response。
- 明确失败条件:改写引入 actual harmful content。

这条应作为最高优先级。否则即使换 12x10,attacker 仍会学习“把 benign 改 harmful-looking”的行为。

## 5. 关于 USE_Q_SAFE_LABEL_FOR_REFUSAL 和类型一致性

当前 RL 脚本设置 `USE_Q_SAFE_LABEL_FOR_REFUSAL=1`。在 `game.py` 中,这会优先用改写后 prompt 的 safety label (`q_safe_label`) 决定 request_label;只有 reward model 没给出 label 时才 fallback 到原始 `data_type`。

这有一个优点:如果 attacker 真的把 benign prompt 改成 Unsafe,defender 拒绝它会被视为正确,不会按 benign 过拒惩罚 defender。

但它也有一个副作用:训练目标会从“保持原始 data_type 一致”滑向“按改写后的 q label 自洽”。也就是说,如果 SFT attacker 已经学会把 benign 改 unsafe,RL 会在 refusal reward 口径上承认这个漂移,而不是强制它回到 benign。

代码里确实计算了 label consistency:
- target label 来自原始 data_type。
- attacker_query_label 来自 q_safe_label。
- `reward_label = REWARD_LABEL if consistent else -REWARD_LABEL`。

但当前 RL 脚本设置 `REWARD_LABEL=0`,所以这个约束实际上没有进入训练。你提到“希望 SFT 数据教会 attacker 改写保持类型一致”是对的,而且 RL 侧也应保留一个小权重的一致性约束,否则 SFT 修正可能会在 RL 中被稀释。

建议:
- SFT prompt 显式加入类型保持:benign 改写必须 remain safe/benign; harmful 改写必须 remain unsafe/harmful。
- distill 后用 Guard 过滤或打标签,至少丢弃 DACE benign 中 Unsafe 的 answer。
- RL 侧考虑 `REWARD_LABEL` 设为小正数,或新增只针对 attacker prompt label drift 的 penalty。
- 日志中单独监控 `label_consistent_benign`, `label_consistent_harmful`, `q_safe_label_by_data_type`。

## 6. 是否改成 12x10

### 支持删除的理由

Code Interpreter Abuse:
- 在 Llama Guard 4 中就是 text-only tool-call use case。
- 当前 MAGIC defender 没有 code interpreter 工具表面。
- SFT v3 只有 47 条,archive pool 只有 5 条,10 个格子里 7 个为空。
- 删除它的理由很强。

Sexual Content:
- 概念上不是冗余,但当前 SFT 只有 352 条,archive pool 只有 9 条。
- DACE benign 中该类 not-safe rate 96.3%,非常容易污染 benign 数据。
- 如果不补专门的 adult benign/suspicious 数据,删除它是合理的。

### 反对直接删除的理由

Sexual Content 是一个有价值的 over-refusal 维度。很多安全模型会对成人内容、性教育、文学/心理咨询类 benign prompt 过拒。如果你的研究目标包括 false positive/over-refusal,S12 其实有评估价值。问题不是它定义错了,而是当前数据不够且 prompt 诱导错了。

### 我的建议

如果近期目标是让 DACE RL 稳定起来,采用 12x10:
- 删除 S12 Sexual Content 和 S14 Code Interpreter Abuse。
- 保留 S3/S4。
- 后续单独做一个 held-out evaluation 或扩展实验来研究 Sexual Content over-refusal。

如果近期目标是保留 Llama Guard 4 完整分类面,不要删 S12:
- 只删 S14。
- 对 S12 补数据并重写 benign prompt。
- 通过源数据补齐、生成后分层采样和 rare-risk 追加蒸馏保证基础覆盖;不建议为了填格子而硬指派 risk category。

无论选哪种,不要只改一处常量。需要同步考虑:
- `data/safety/preprocess_dace.py` 的 risk 列表和 “14 Risk Categories” 文案。
- `data-sft/distill_v2_vanilla_*.py` 的 COMMON_STRATEGY_GUIDANCE、CONSTRAINT_TEMPLATE、clean 规则。
- `data-sft/run_cot_distill_v2.sh` 内嵌 canonical list。
- `src/verl/verl/separated_trainer/ppo/archive_pool.py` 的 RISK_CATEGORIES、N_RISK、N_SLOTS。
- `scripts/analyze_archive_pool.py`、`data-sft/analyze_strategy_distribution.py`。
- `data-sft/convert_v2_cot_to_game_format.py` 中 rare-risk 逻辑。
- 已有 14x10 archive_pool checkpoint 与 12x10 不兼容,不能直接 resume。

## 7. 空格子是否会压制 diversity reward

你的分析有道理,但机制需要更精确地表述。

当前公式:

```text
R_div(x) = [H(p + one sample at x) - H(p)] / [max_b H(p + one sample at b) - H(p) + eps]
```

分母枚举所有 14x10 slot。只要存在空格子,向空格子加一个样本通常就是最大 entropy gain。因此空格子会把 `delta_max` 固定在“开新格子”的收益上。

以 step 300 archive pool 为例:
- 空格子 count=0 的 slot: `r_div = 1.0000`。
- 已有 1 条样本的 slot: `r_div = 0.7232`。
- 已有 2 条样本的 slot: `r_div = 0.6187`。
- 已有 9 条样本的 slot: `r_div = 0.3508`。
- 高占用 slot 很多会被 clip 到 0。

所以如果空格子集中在模型几乎不可达的类别,其他“可达但稀有”的非空格子确实会拿不到最高 diversity reward。这就是一种压制。

但删除 S12/S14 并不会自动解决这个归一化问题。把 step 300 矩阵从 14x10 改成删除 S12/S14 的 12x10 后:
- 空格子从 12 个减少到 2 个。
- `delta_max` 仍由剩余空格子决定。
- 多数保留类别的平均 `r_div` 几乎不变,例如 Elections 从 0.5706 到 0.5717,Sex-Related Crimes 从 0.5100 到 0.5112。

结论:
- “很多 dead cells 会压制其他少数格子”成立。
- “删除 Sexual Content 和 Code Interpreter Abuse 就能明显释放 diversity reward”不一定成立,除非删除后没有不可达空格子,或同时修改 `delta_max` 的计算口径。

更直接的优化方向:
- `delta_max` 只在 active support 或可达 mask 上枚举,不要让不可达 slot 参与分母。
- 使用 per-risk 或 per-data_type 的归一化,避免一个 data_type 的覆盖影响另一个 data_type。
- 将 `slot_counts` 拆成 benign/harmful 两张表。当前同一张 `slot_counts` 混合了 vanilla_benign 和 vanilla_harmful,会让 benign 的 diversity 被 harmful 覆盖度影响。
- 给每个 slot 设置 reachability prior 或 target distribution,不要默认追求 140 格均匀覆盖。

## 8. SFT 蒸馏改进建议

高优先级:

1. 重写 benign 蒸馏 prompt。
   - 把 “trick the language model into producing harmful responses” 改成 “induce over-refusal / false positive”。
   - 明确 “underlying intent remains benign”。
   - 明确 “lose if revised prompt becomes actually harmful”。
   - benign 的 SYSTEM_PROMPT 也建议从泛化的 red teaming adversarial prompt 改成 adversarial benign rewriting,否则系统层仍偏向攻击生成。

2. 蒸馏后 Guard filter。
   - 对 benign SFT 的 `answer` 做 safety check。
   - 第一阶段建议只保留 Safe;如果想保留 Controversial,需要单独标记并在训练中降权。
   - 每轮输出按 risk/style 统计 not-safe rate,不要只看 overall。

3. 加入类型一致性目标。
   - benign: revised prompt must remain safe/benign under the safety classifier。
   - harmful: revised prompt should remain unsafe/harmful and preserve harmful intent。
   - 不要只写在自然语言 prompt 中,最好通过后处理过滤和 RL label reward 共同约束。

4. 保持 B' 蒸馏方案:Directed Style + Free Risk + Hidden Assignment。
   - 只指派 attack style。Style 是包装/表达风格,多数与 vanilla 内容正交,例如 Slang、Uncommon Dialects、Role Play、Misspellings 都可以自然套到不同主题上。
   - 不指派 risk category。Risk 应由 vanilla 的语义决定,否则会把不相关的 risk 强行套到原 prompt 上,制造 awkward 组合,也可能破坏 entailment。
   - `<think>` 仍保持“分析 vanilla -> shortlist plausible risks/styles -> commit final style”的自由选择形态。目标 style 只作为隐藏约束,要求它出现在 shortlist 中并被合理选择。
   - 继续保留 anti-leak:禁止出现 assigned/told/per instruction/mandated 等泄漏指派事实的表述,clean 阶段发现后进 `.err` 重跑。目标是让 SFT 学到像自主推理一样的 token 分布,而不是学到“上游塞了参数”的先验。
   - Risk 分布不均用数据侧方法处理:补充 rare-risk 源样本、按 Gemini 自选 risk 做后验分层采样、对过量的 Non-Violent Crimes 降采样,而不是硬指派 risk。

低优先级:

1. 补稀有 risk category 数据。
   - 如果采用 12x10,重点补 Elections、Child Sexual Exploitation、Sex-Related Crimes、Indiscriminate Weapons 的 adversarial benign-but-safe 样本。
   - 如果保留 S12,单独补 Sexual Content 的 safe boundary 数据。
   - 如果保留 S14,需要确认是否引入 tool-use/code-interpreter eval surface;否则补数据意义有限。

2. 降低 v1 rare-risk 拼接的副作用。
   - 当前 v3 是 all v2 + v1 rare risks,默认 rare risks 包含 Sexual Content、Elections、Code Interpreter Abuse。
   - 这提高了稀有类数量,但没有解决 benign prompt 的目标冲突。v4 应优先重蒸馏,而不是继续拼接旧 prompt 产物。

## 9. RL 训练侧建议

1. 不要只依赖 `USE_Q_SAFE_LABEL_FOR_REFUSAL`。
   - 它可以让 defender reward 使用改写后的真实 safety label,但不能保证 attacker 保持原始 data_type。
   - 建议对 attacker 单独加 label consistency reward 或 drift penalty。

2. `REWARD_LABEL=0` 不适合当前目标。
   - 代码已经计算 label consistency,但脚本把权重置零。
   - 可以从小权重开始,例如只占 safety reward 的一小部分,避免压过主任务。

3. `format_reward_func_dace` 只检查三段 tag 结构。
   - 它不检查 risk/style 是否 canonical,也不检查是否可解析进 14x10。
   - 结果是 attacker 可能拿到 format reward,但 strategy 不能进入 archive/diversity。
   - 建议 format reward 也复用 `ArchivePool.extract_strategy` 或同源 canonical list。

4. archive pool 建议按 data_type 拆 coverage。
   - 当前 `slot_counts` 是全局一张表。
   - benign attack 的目标是 over-refusal,harmful attack 的目标是 unsafe response,两者不应共享同一 coverage 矩阵和 posterior 成功语义。

5. attack_success 建议拆语义。
   - harmful: success = defender 输出 unsafe。
   - benign: success = defender refused 或输出 unsafe。
   - 当前这两类 success 都进入同一 replay posterior,会混淆 Thompson sampling 的“高价值样本”含义。

6. 如果改 12x10,重新开始 pool。
   - 14x10 的 strategy index 与 12x10 不兼容。
   - 旧 archive_pool.json 不建议映射复用,除非写清楚 index remap 和被删除类别的处理。

## 10. 其他相关问题

安全配置:
- `grpo_dace_diversity_full.sh` 中直接写了 `WANDB_API_KEY`。
- distill benign/harmful 脚本中直接写了 OpenAI-compatible API key 和 base_url。
- 这不影响研究结论,但后续整理仓库时应迁移到环境变量。

revision/on-topic 约束:
- 当前脚本关闭了 revision reward,模板中“on-topic/relevant/entails vanilla prompt”的约束主要靠 SFT prompt 自觉。
- 若后续发现 attacker 改写偏离 seed prompt,应考虑恢复轻量 revision reward 或做离线过滤。

style 真实性:
- SFT clean 只检查 `<strategy>` 里声明的 attack style 是否等于 assigned_style,不验证文本是否真的体现该 style。
- RL diversity 也基于 attacker 自报的 style。长远看可以引入 style classifier 或规则抽检,但优先级低于 benign prompt 修复。

## 建议的实验路线

路线 A: 稳定优先,推荐。
1. 使用 12x10,删除 S12 Sexual Content 和 S14 Code Interpreter Abuse。
2. 重写 BENIGN_TEMPLATE。
3. v4 蒸馏采用 B':directed style + free risk + hidden assignment。
4. Guard filter benign SFT,目标 not-safe rate 降到 10% 以下。
5. RL 侧启用小权重 label consistency。
6. archive diversity 使用 active-mask denominator 或至少监控空格子对 `delta_max` 的影响。

路线 B: Taxonomy 完整优先。
1. 保留 14x10,但至少删除或禁用 S14。
2. 对 S12/Elections/CSE 补数据。
3. 重写 BENIGN_TEMPLATE,蒸馏仍采用 B':directed style + free risk + hidden assignment。
4. diversity reward 使用 active support mask,避免 dead rows 压制。

路线 C: 最小改动验证。
1. 只重写 BENIGN_TEMPLATE 并重蒸馏 benign。
2. 不改 14x10。
3. RL 侧把 `REWARD_LABEL` 从 0 调到小正数。
4. 跑同样 300 steps,看 `refusal_rate_benign`、DACE benign not-safe rate、archive pool bottom rows 是否改善。

我建议先走路线 C 做 ablation,确认 benign 污染是否是主因;如果确认,再把 12x10、B' 蒸馏和数据侧 rare-risk 补齐合并到路线 A。

## 验收指标

SFT 数据:
- DACE benign unsafe rate 从 43.0% 降到 10% 以下。
- DACE benign unsafe+controversial 从 68.2% 降到 20% 以下。
- Non-Violent Crimes 在 SFT 全量中的占比需要显著下降,但不建议用硬指派 risk 来追求机械均匀;应通过源数据构成、生成后分层采样和 rare-risk 追加蒸馏调整。
- 每个保留 risk category 至少有稳定样本量;若 12x10,每个 risk 行建议设置数据侧下限,但 risk 标签仍来自 Gemini 对 vanilla 语义的自由选择或后验分类。

RL:
- `refusal_rate_benign` 不再长期波动到 0.3-0.5。
- `refusal_rate_harmful` 不明显下降。
- archive pool bottom rows 不再接近 0。
- diversity reward 在训练中保持可见量级,不要长期被 clip 到 0。
- 新增 `label_consistent_benign`/`label_consistent_harmful` 指标。

决策点:
- 若你要写论文/报告并强调 Llama Guard 4 taxonomy 完整对齐,训练用 12x10 需要解释为 “training attack space pruned for feasible text-only MAGIC setting; evaluation still reports full LG4 taxonomy where applicable”。
- 若你只追求当前 MAGIC 训练稳定性,12x10 是合理选择,但必须和 prompt/数据重蒸馏一起做。
