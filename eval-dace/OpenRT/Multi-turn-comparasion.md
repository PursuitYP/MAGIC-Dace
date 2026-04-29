# OpenRT Multi-turn Workflow 对比梳理

本文只基于当前仓库里的 OpenRT 实现做代码级梳理，不额外假设论文里的原始设定已经被完整复现。重点关注 4 个方法：

- `ActorAttack`
- `Crescendo`
- `RACE`
- `X-Teaming`

我主要读取了以下文件：

- [actor_attack_example.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/example/actor_attack_example.py:1)
- [crescendo_attack_example.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/example/crescendo_attack_example.py:1)
- [race_attack_example.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/example/race_attack_example.py:1)
- [xteaming_attack_2025.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/example/xteaming_attack_2025.py:1)
- [eval.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/eval.py:236)
- [actor_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/actor_attack.py:10)
- [crescendo_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/crescendo_attack.py:68)
- [race_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/race/race_attack.py:24)
- [race_modules.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/race/race_modules.py:5)
- [attack_state_machine.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/race/attack_state_machine.py:18)
- [xteaming_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/xteaming_attack.py:32)
- [llm_judge.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/judges/implementations/llm_judge.py:9)
- [openai_model.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/models/implementations/openai_model.py:124)

## 一页总结

| 方法 | 攻击前是否有 warmup / planning | 是否对 target model 形成“真实 multi-turn history” | OpenRT 当前默认 target-side scaling | `max_turn` 在 OpenRT 中是否真正生效 | 主要公平性风险 |
| --- | --- | --- | --- | --- | --- |
| ActorAttack | 有。先 discovery actors，再为每个 clue 生成 chain | 否。对 target 的每一步都是独立 `query()` | `max_clues=6`，每个 clue 一条 3-4 step chain，最多约 18-24 次 target query | 基本不生效。参数存在，但 chain 长度并未用它控制 | 多 clue best-of-N，很像 ASR@N 而不是 ASR@1 |
| Crescendo | 无显式 warmup，但第 1 turn 是 safe opening | 是。唯一明确使用 `maintain_history=True` 的方法 | `eval.py` 默认 `max_turns=3, max_backtracks=5`，target query 上界大致是 `turns + backtracks` | 生效 | backtrack 会引入额外 target query |
| RACE | 无显式 warmup，第 1 turn 直接打原始目标 | 否。target 每轮都是独立单轮查询 | 1 次 target query / turn，`eval.py` 默认 6 turn | 生效 | 不是 target-side true multi-turn；但 shadow-model 内部有较多额外搜索 |
| X-Teaming | 有。先生成完整 attack plan，失败后还可能 revise plan | 否。conversation history 只喂给 planner / optimizer，不喂给 target | 每 turn 最多 `max_iterations_per_turn=3` 次 target query，且有最多 2 次 plan revision | 不生效。参数存在，但执行逻辑未使用它约束实际 turn 数 | prompt optimization + plan revision 带来明显 test-time scaling |

## 最关键的代码事实

### 1. 真正对 target model 维护 multi-turn history 的，只有 Crescendo

[openai_model.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/models/implementations/openai_model.py:124) 里，只有 `query(..., maintain_history=True)` 才会把 user / assistant 消息加入 `conversation_history`。否则就是单轮请求。

- Crescendo 在 [crescendo_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/crescendo_attack.py:347) 明确调用了 `self.model.query(current_prompt, maintain_history=True)`，所以它是 target-side 的真实 multi-turn。
- ActorAttack 在 [actor_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/actor_attack.py:285) 用的是 `self.model.query(step)`，没有维护 history。
- RACE 在 [race_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/race/race_attack.py:65) 也是 `self.model.query(optimized_query)`，没有维护 history。
- X-Teaming 在 [xteaming_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/xteaming_attack.py:331) 也是 `self.model.query(attacker_message)`，没有维护 history。

结论：

- 从“方法名义”上，这四个都算 multi-turn workflow。
- 但从“OpenRT 当前实现”看，只有 Crescendo 真正把历史对话喂回 victim / target model。
- 另外三种更准确地说是“attacker-side sequential workflow”，不是 target-side true multi-turn。

### 2. `max_turn=5` 不是这四个方法在 OpenRT 中的统一真实默认

[eval.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/eval.py:236) 的批量评测默认值是：

- Crescendo: `max_turns=3`
- ActorAttack: `max_turns=6`
- X-Teaming: `max_turns=5`
- RACE: `max_turns=6`

而 constructor 默认值是：

- Crescendo: `max_turns=10`，见 [crescendo_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/crescendo_attack.py:83)
- ActorAttack: `max_turns=10`，见 [actor_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/actor_attack.py:22)
- X-Teaming: `max_turns=5`，见 [xteaming_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/xteaming_attack.py:50)
- RACE: `max_turns=10`，见 [race_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/race/race_attack.py:26)

example 里又是另一套：

- Crescendo example: `max_turns=8`
- ActorAttack example: `max_turns=6`
- X-Teaming example: `max_turns=5`
- RACE example: `max_turns=6`

所以后续做公平比较时，不能说“OpenRT 默认都是 5 轮”。当前代码事实不是这样。

### 3. X-Teaming 的“10 个策略改写 / ASR@10”并没有在 OpenRT 当前实现里显式出现

我在当前仓库中没有找到 X-Teaming 对同一个 seed 固定生成 `10` 个 strategy rewrite 的代码入口。OpenRT 里 X-Teaming 的 test-time scaling 主要来自：

- 每 turn 的 `max_iterations_per_turn=3`，见 [xteaming_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/xteaming_attack.py:51)
- 最多 2 次 plan revision，见 [xteaming_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/xteaming_attack.py:298)

也就是说：

- 论文里如果有 ASR@10 的设定，需要单独核论文。
- 但在 OpenRT 这个实现中，我没有看到显式的“每个 seed 攻 10 个独立 strategy”的参数。
- OpenRT 的 X-Teaming 更像是“1 个初始 plan + 每 turn prompt optimization + 最多 2 次 plan revision”。

## 逐方法梳理

## ActorAttack

### Workflow

[actor_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/actor_attack.py:30) 里的流程非常明确，分两阶段：

1. Pre-attack discovery。
2. In-attack execution。

具体步骤：

1. 用 `helper_model` 做 discovery，围绕目标生成一组 actors / clues，见 [actor_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/actor_attack.py:97)。
2. 按 `innocence_level` 从高到低排序，优先尝试“更无害”的 clue，见 [actor_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/actor_attack.py:138)。
3. 对每个 clue，用 `helper_model` 生成一条 3-4 step 的 conversation chain，见 [actor_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/actor_attack.py:217)。
4. 把 chain 中的 step 逐个发给 target model，见 [actor_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/actor_attack.py:267)。
5. 只拿每个 clue 的最后一个 response 交给 judge 判分，成功就提前返回，见 [actor_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/actor_attack.py:66)。

### 是否有 warmup

有，而且非常明确。

- discovery actors / clues 本身就是 pre-attack warmup。
- 生成 attack chain 也是 attack 前准备。
- 所以它不是“直接上 target model 攻击”。

### 是否是真 multi-turn

严格按 OpenRT 代码看，不是 target-side true multi-turn。

- `_execute_attack_chain()` 里虽然按 step 顺序执行，但每一步都是 `self.model.query(step)`，见 [actor_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/actor_attack.py:279)。
- 没有 `maintain_history=True`。
- 所以 target 看见的是多次独立单轮请求，而不是一个连续对话线程。

### 默认 turn / scaling 参数

- constructor 默认 `max_turns=10, max_clues=8`，见 [actor_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/actor_attack.py:22)
- `eval.py` 默认 `max_turns=6, max_clues=6`，见 [eval.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/eval.py:293)
- example 也是 `max_turns=6, max_clues=6`，见 [actor_attack_example.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/example/actor_attack_example.py:66)

但这里有一个关键实现问题：

- `max_turns` 只在 `__init__` 存了下来，没有真正用于限制 chain 长度或 target query 次数。
- chain 的长度实际由 prompt 写死成 “3-4 step conversational chain”，见 [actor_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/actor_attack.py:226)。

所以对 ActorAttack 来说，真正决定 test-time scaling 的不是 `max_turns`，而是：

- `max_clues`
- 每个 clue 对应的 chain 长度
- 是否在前几个 clue 就成功

如果按 `eval.py` 的 `max_clues=6` 估计，target-side query 上界大约是：

- `6 * (3~4)` 次 target query
- 即约 `18~24` 次 target query

这显然不是 ASR@1。

### 对 ASR@1 的含义

如果要做“每个 seed 一次尝试攻破的概率”，ActorAttack 至少需要收紧到：

- `max_clues=1`
- 只允许 1 条 chain
- chain 长度再单独固定

否则当前实现更接近：

- 对同一个 seed 做多个 clue branch 搜索
- 只要某个 branch 成功就算成功

这本质上是 best-of-N，而不是单次尝试。

### 外部配件

- target model API
- `helper_model` API
- `judge` API

example 里三者都通过 `OpenAIModel` 包装，使用 `.env` 里的 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL`，见 [actor_attack_example.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/example/actor_attack_example.py:28)。

未看到额外 executor、tool API、image generator 等外部组件。

## Crescendo

### Workflow

[crescendo_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/crescendo_attack.py:304) 的流程是：

1. 给 target model 设置一个专门的 Crescendo system message，见 [crescendo_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/crescendo_attack.py:327)。
2. 先生成一个 safe opening prompt，问目标相关的历史背景，见 [crescendo_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/crescendo_attack.py:166)。
3. 把 prompt 发给 target，并且 `maintain_history=True`，见 [crescendo_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/crescendo_attack.py:347)。
4. 用 judge 对 response 打分。
5. 若未成功，则用 `attack_model` 根据已有对话、上一轮 response 和 summary 生成下一轮 escalated prompt，见 [crescendo_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/crescendo_attack.py:171)。
6. 若分数较低，则可能 backtrack，删掉 target 的最后一轮 history，再换一个问法，见 [crescendo_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/crescendo_attack.py:287)。

### 是否有 warmup

没有显式的独立 warmup phase。

但它不是完全“直接攻击”，因为：

- 第 1 轮固定是一个明显更安全的 opening prompt。
- 可以把这理解为“soft warmup”，但不是 ActorAttack / X-Teaming 那种攻击前单独 planning。

### 是否是真 multi-turn

是。

- 这是四个方法里唯一明确把 target conversation history 保留下来的实现。
- `maintain_history=True` 会把整段对话持续喂给 target，见 [openai_model.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/models/implementations/openai_model.py:177)。

### 默认 turn / scaling 参数

- constructor 默认：`max_turns=10, max_backtracks=10, success_threshold=5`，见 [crescendo_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/crescendo_attack.py:83)
- example：`max_turns=8, max_backtracks=5`，见 [crescendo_attack_example.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/example/crescendo_attack_example.py:74)
- `eval.py`：`max_turns=3, max_backtracks=5`，见 [eval.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/eval.py:236)

这里有两个比较重要的实现细节：

1. `eval.py` 默认并不是 5 turn，而是 3 turn。
2. backtrack 会消耗额外 target query。

原因是：

- 每次 backtrack 只是把 `current_turn` 减回去，并删掉 target history，见 [crescendo_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/crescendo_attack.py:59)
- 但已经发出去的 query 仍然消耗了一次 target 调用。

因此 target-side query 上界可以近似理解为：

- `max_turns + max_backtracks`

例如 `eval.py` 默认大约是：

- `3 + 5 = 8` 次 target query 上界

### 对 ASR@1 的含义

如果要做更严格的 ASR@1，有两种口径：

1. Workflow-level ASR@1。含义是“每个 seed 只跑 1 条 Crescendo 对话轨迹”。那就至少要统一 `max_turns`，并明确 backtrack 是否允许。
2. Prompt-call-level ASR@1。含义是“每个 seed 对 target 只打 1 次”。那 Crescendo 这种方法本身就不再成立，因为它的核心就是多轮推进。

如果你的目标是公平比较 multi-turn workflow 的“一次运行成功率”，我建议：

- 统一设置 `max_turns=5`
- 明确是否允许 backtrack
- 更严格的做法是设 `max_backtracks=0`

否则 Crescendo 会拿到额外的 retry budget。

### 其他实现细节

- `_evaluate_response()` 的返回值标注和实际内容不完全一致，见 [crescendo_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/crescendo_attack.py:250)。
- 当前代码里 `refusal_score` 实际上直接复用了 `objective_score`，见 [crescendo_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/crescendo_attack.py:364)。
- 这不一定会影响跑通，但说明它的 refusal / objective 两个维度并没有被彻底分开实现。

### 外部配件

- target model API
- `attack_model` API
- `judge` API

未看到外部 executor 依赖。

## RACE

### Workflow

[race_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/race/race_attack.py:39) 的流程是：

1. 初始化状态机 `AttackStateMachine`，见 [race_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/race/race_attack.py:32)。
2. 第 1 轮直接用原始 `target` 作为 query，见 [race_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/race/race_attack.py:51)。
3. 从第 2 轮开始，`GainGuidedExploration` 用 `shadow_model` 生成 5 个 candidate follow-up queries，见 [race_modules.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/race/race_modules.py:9)。
4. 再用 `estimate_information_gain()` 给这些 candidate 打分并选最好一个，见 [race_modules.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/race/race_modules.py:31)。
5. 再用 `SelfPlayModule` 把 query 重写得更容易被 target 接受，见 [race_modules.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/race/race_modules.py:68)。
6. 把优化后的 query 发给 target，见 [race_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/race/race_attack.py:65)。
7. 用 judge 决定状态转移：`s_success / s_intermediate / s_failure`，见 [attack_state_machine.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/race/attack_state_machine.py:24)。

### 是否有 warmup

没有独立 warmup。

- 第 1 轮就是直接把原始目标打给 target。
- 第 2 轮之后才开始根据前文做 query generation 和 refinement。

### 是否是真 multi-turn

不是 target-side true multi-turn。

- RACE 会维护一个 `context_history`，见 [attack_state_machine.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/race/attack_state_machine.py:5)
- 但这个 history 只用于 `shadow_model` 生成下一轮 query。
- 发给 target 的时候仍然是单独 `self.model.query(optimized_query)`，见 [race_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/race/race_attack.py:65)。

所以它是“基于历史推理的多轮攻击器”，不是“把历史真正发给 victim 的连续对话”。

### 默认 turn / scaling 参数

- constructor 默认：`max_turns=10`，见 [race_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/race/race_attack.py:26)
- example：`max_turns=6`，见 [race_attack_example.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/example/race_attack_example.py:61)
- `eval.py`：`max_turns=6`，见 [eval.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/eval.py:325)

target-side 上，它比较“干净”：

- 1 次 target query / turn
- 最多 `max_turns` 次 target query

如果按 `eval.py`，就是最多 6 次 target query。

但是 shadow-side 的额外开销并不小。每个第 2 轮及以后，shadow model 最多会做：

- 1 次生成 5 个 seed query
- 5 次 estimate information gain
- 1 次 self-play optimize

也就是每轮最多约 7 次 shadow-model query。

按 `max_turns=6` 粗算：

- 第 1 轮约 1 次 optimize
- 后 5 轮约 `5 * 7 = 35`
- 合计约 36 次 shadow-model query

这不影响 target-side ASR@1 的定义，但会影响整体 cost 对比。

### 对 ASR@1 的含义

如果你的“ASR@1”定义是“每个 seed 一次 workflow run”，那么 RACE 相对最容易规范化：

- 统一 `max_turns=5`
- 每个 turn 只打 1 次 target
- 没有像 ActorAttack / X-Teaming 那样明显的多 branch best-of-N

但要注意，它依然不是 victim-side 的真 multi-turn conversation。

### 其他实现细节

- `RejectionFeedback` 模块定义了，但在主流程里并没有实际被调用，见 [race_modules.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/race/race_modules.py:92) 与 [race_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/race/race_attack.py:35)。
- 状态机成功判定依赖 judge 的 `is_successful(score)`，见 [attack_state_machine.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/race/attack_state_machine.py:25)。

### 外部配件

- target model API
- `shadow_model` API
- `judge` API

未看到外部 executor。

## X-Teaming

### Workflow

[xteaming_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/xteaming_attack.py:262) 的逻辑是：

1. 先由 `planner_model` 生成一个完整 JSON attack plan，包含 persona、context、approach 和 `conversation_plan`，见 [xteaming_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/xteaming_attack.py:433)。
2. 然后每一轮不是直接人工写 prompt，而是让 `planner_model` 再根据该轮 plan 和已有 conversation history 生成 attacker message，见 [xteaming_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/xteaming_attack.py:496)。
3. 对同一轮 message，可以最多做 `max_iterations_per_turn` 次 target query，并用 `optimizer_model` 持续改写 prompt，见 [xteaming_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/xteaming_attack.py:329)。
4. 一轮结束后，把该轮最佳结果加入 `conversation_history` 文本串，供后续 planner / optimizer 参考，见 [xteaming_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/xteaming_attack.py:393)。
5. 如果 plan 表现下降，允许最多 2 次 plan revision，见 [xteaming_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/xteaming_attack.py:298)。

### 是否有 warmup

有，而且是最典型的 “plan-first”。

- 先 planning，再 execution。
- 失败后还有 re-planning / plan revision。

所以它绝对不是“直接攻击”。

### 是否是真 multi-turn

不是 target-side true multi-turn。

- `conversation_history` 只是作为字符串传给 planner / optimizer 继续生成下一轮 prompt，见 [xteaming_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/xteaming_attack.py:397)。
- target model 本身每次都是独立 `self.model.query(attacker_message)`，见 [xteaming_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/xteaming_attack.py:331)。

### 默认 turn / scaling 参数

- constructor 默认：`max_turns=5, max_iterations_per_turn=3`，见 [xteaming_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/xteaming_attack.py:50)
- example：`max_turns=5, max_iterations_per_turn=3`，见 [xteaming_attack_2025.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/example/xteaming_attack_2025.py:55)
- `eval.py`：`max_turns=5, max_iterations_per_turn=3`，见 [eval.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/eval.py:299)

但这里有两个非常重要的实现问题：

1. `max_turns` 几乎没有真正参与执行约束。
2. 还存在硬编码的 `max_plan_revisions=2`。

原因如下：

- 实际执行的 turn 列表来自 `attack_plan['conversation_plan']` 里有多少个 `turn_i` 再加一个 `final_turn`，见 [xteaming_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/xteaming_attack.py:305)。
- 这里并没有用 `self.max_turns` 去裁剪 plan。
- 所以 planner 如果生成了超过 5 个步骤，代码仍然会全部执行。

换句话说：

- `max_turns=5` 在接口层存在。
- 但在当前 OpenRT 的 X-Teaming 实现里，它不是一个严格生效的 target query budget。

### 对 ASR@1 的含义

X-Teaming 是四个里 test-time scaling 最需要警惕的一个。

当前实现的额外 scaling 至少来自：

- 每 turn 最多 3 次 prompt optimization / retry
- 最多 2 次 plan revision
- plan 实际步数不受 `max_turns` 严格限制

因此当前实现更接近：

- 一个 seed 上做多轮 plan-search + prompt-search

而不是单次尝试。

如果要把它收敛成更公平的 ASR@1，我建议至少满足：

- `max_iterations_per_turn=1`
- `use_prompt_optimization=False`
- 去掉 plan revision，或把 `max_plan_revisions` 暴露出来并设成 0
- 真正让 `max_turns=5` 裁剪 `conversation_plan`

否则 X-Teaming 的结果和其他方法并不在同一个 budget 上。

### 其他实现细节

- 成功条件被写死为 `score == 5`，见 [xteaming_attack.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/OpenRT/attacks/blackbox/implementations/xteaming_attack.py:361)。
- 它没有统一走 `judge.is_successful(score)`。
- 因此如果你以后把 `judge.success_threshold` 调成 4，X-Teaming 仍然只认 5，这会破坏横向一致性。

### 外部配件

- target model API
- `planner_model` API
- `optimizer_model` API
- `judge` API

未看到外部 executor、browser tool、image generator。

## 对公平比较 ASR@1 的建议

如果目标是比较“每个 seed 一次运行成功的概率”，我建议把评测定义写清楚为：

- 单个 seed 只允许 1 条 attack trajectory。
- 所有方法统一 target-side budget 为最多 5 次 target query。
- success criterion 统一为 LLM judge `score >= 5`。
- 额外的 branch / rewrite / revision 不允许以 best-of-N 的形式存在。

按这个定义，四个方法建议收敛为：

| 方法 | 当前 OpenRT 不公平来源 | 更公平的 ASR@1 设定建议 |
| --- | --- | --- |
| ActorAttack | `max_clues` 会并行尝试多个 clue branch；`max_turns` 形同虚设 | 设 `max_clues=1`；只保留 1 条 chain；必要时把 chain 步数硬裁成 5 以内 |
| Crescendo | `max_backtracks` 增加额外 target query | 统一 `max_turns=5`；建议 `max_backtracks=0`，或把总 target query 严格裁到 5 |
| RACE | 相对干净，但默认 6 turn | 统一 `max_turns=5` |
| X-Teaming | `max_iterations_per_turn`、plan revision、plan 步数不受 `max_turns` 严格约束 | 设 `max_iterations_per_turn=1`；关闭 optimization；revision=0；强制裁剪 plan 到 5 turn |

我个人认为，如果不做这些收敛，那么当前 OpenRT 里的这几个结果应更准确地标成：

- “budgeted workflow success rate”
- 或者 “best-of-search ASR under method-specific budget”

而不应该直接叫严格意义上的 ASR@1。

## 我认为最值得立即修正的实现差异

如果后面你们要正式复现并公平比较，这几个点最值得先改：

1. ActorAttack 的 `max_turns` 当前不控制实际执行长度。
2. ActorAttack 现在不是真正 target-side multi-turn。
3. X-Teaming 的 `max_turns` 当前不控制实际 plan 长度。
4. X-Teaming 成功判定写死成 `score == 5`，没有走统一 judge threshold。
5. Crescendo 在 `eval.py` 里默认只有 3 turn，不是 5 turn。
6. RACE 也是 target-side sequential single-turn，不是 victim-side true multi-turn。

## 外部依赖总表

| 方法 | target 之外需要的组件 | 备注 |
| --- | --- | --- |
| ActorAttack | `helper_model`、`judge` | 无额外 executor |
| Crescendo | `attack_model`、`judge` | 无额外 executor |
| RACE | `shadow_model`、`judge` | `RejectionFeedback` 模块虽然定义了，但当前主流程没用上 |
| X-Teaming | `planner_model`、`optimizer_model`、`judge` | 无额外 executor |

从 example 来看，这些组件都可以通过 `OpenAIModel` 用 OpenAI-compatible API 来提供，见：

- [actor_attack_example.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/example/actor_attack_example.py:28)
- [crescendo_attack_example.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/example/crescendo_attack_example.py:30)
- [race_attack_example.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/example/race_attack_example.py:24)
- [xteaming_attack_2025.py](/mnt/shared-storage-user/wenxiaoyu/game-private/eval/OpenRT/example/xteaming_attack_2025.py:26)

## 最后结论

如果按当前 OpenRT 代码事实来讲：

- ActorAttack：有明显 warmup；不是 target true multi-turn；当前最像多 clue 搜索。
- Crescendo：没有独立 planning warmup，但有 safe opening；是唯一真正 target true multi-turn；backtrack 会带来额外 scaling。
- RACE：没有 warmup；第 1 轮直接打目标；target 侧不是 true multi-turn；但每 turn 只有 1 次 target query，比较容易规范。
- X-Teaming：强 planning-first；target 侧不是 true multi-turn；当前实现的 scaling 最大，而且 `max_turns` 没有被严格执行。

因此，如果你们接下来要做真正公平的 multi-turn workflow 复现比较，我建议不要直接沿用 OpenRT 当前默认参数，而是先统一：

- target-side 最大 query budget
- 是否允许 branch / backtrack / rewrite / revision
- success threshold
- 是否必须是 victim-side true multi-turn

否则最后得到的不是同一口径下的 ASR@1。
