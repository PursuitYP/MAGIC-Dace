# DACE v4 Review & Polish Plan（第五轮：实现后审查）

## Context

上一轮 plan 已把 DACE v4 全流水线改造落地（13 项改动：core constants、SFT 蒸馏链路、RL 脚本、analyze 脚本、文档），git 当前未提交的 15 个文件就是这一轮的产物。本轮任务 **不是新增功能**，而是：GPT (codex review) 交叉审查加我本人独立审查的结果，把 **实际代码 vs. 原 plan** 的偏差、遗漏、和一致性缺陷列清，给出最小范围的修补计划。

目标：让 v4 能**端到端无阻塞**跑通 Phase 1 → Phase 5，并清掉会被 grep/读 review 时误导的字面不一致。核心 RL 行为无需再改。

本 Context 之下是本轮 review 的分类清单。原第四轮 v4 重建计划保留在本文件底部作历史依据。

---

## 审查证据（已对文件 grep / read 验证的事实）

以 `grep -n "14 Risk" …v4 files…` 和 diff 对齐，以下事实**已当场验证**，不是回忆或猜测：

1. **`data/safety/preprocess_dace.py:71`** — `COMMON_RESPONSE_FORMAT` 的 Rules 块仍写 `"exactly one of the 14 Risk Categories listed above"`。但紧邻的 `COMMON_STRATEGY_GUIDANCE`（L28-56）已经剪到 12 项并把 Elections 挪到第 12 位。Attacker 在 RL 侧拿到的 prompt 会同时说"12 条 list"和"从 14 条中选"。
2. **`data-sft/distill_v4_vanilla_benign_jsonl.py:84`** 和 **`distill_v4_vanilla_harmful_jsonl.py:88`** 的同一段 Rules 已经写成 `"exactly one of the 12 Risk Categories"`；即 SFT 侧正确、RL 侧落后。
3. **`data-sft/distill_v4_vanilla_harmful_jsonl.py:53,55,69`** 的 `COMMON_STRATEGY_GUIDANCE` 仍使用 curly 撇号 `’`（`person’s`、`someone’s`、`AI’s`），而 `preprocess_dace.py` 和 `distill_v4_vanilla_benign_jsonl.py` 已经替换为 ASCII `'`。全文差 3 个码点，但违反 plan 中"benign / harmful 与 preprocess 的 strategy guidance 逐字同步"的自约束。
4. **`scripts/check_benign_data_quality.py:17-20`** 的 `DATA_FILES` 只有 `magic` 和 `dace`（指向 v3 文件），没有 `dace_v4`。plan 的 Phase 1b 命令 `python scripts/check_benign_data_quality.py --dataset dace_v4 --stats-only` 会被 argparse 直接拒绝。
5. **`data-sft/distill_v4_vanilla_benign_jsonl.py:288-289`** 和 **`distill_v4_vanilla_harmful_jsonl.py:312-313`** 明文写 `api_key="sk-URLcpgjQ1w…"` 和 `base_url="http://35.220.164.252:3888/v1/"`。
6. **`scripts/rl/separated/grpo_dace_diversity_v4.sh:10`** 写 `export WANDB_API_KEY="2d2ad4b937a9c0d7623dcc78dc25c07fe3eaa0a9"`，并且 L2 是 `set -x`，执行时会把这行打到 stdout。
7. **`scripts/rl/separated/grpo_dace_diversity_v4.sh:87`** — `QWEN257BI_SFT_DACE_V4_MODEL_PATH=…/checkpoint-N`，`N` 是字面占位符；当前直接执行会把 `checkpoint-N` 当真实路径传给 rollout，rollout 启动阶段 FileNotFoundError 退出。
8. **`data/safety/__pycache__/preprocess_dace.cpython-310.pyc`** — `git ls-files --error-unmatch` 确认是已被跟踪的文件（首个加入 commit `d076575 add all data foders`），当前 `git status` 显示 `deleted:`。这条删除混在 v4 研究改动里，但与 v4 无关，也没被 `.gitignore`。
9. **`data-sft/analyze_strategy_distribution.py:160-167`** — RISK_CATEGORIES 已剪到 12（正确），但 argparse 默认仍是 `sft_data_cot_benign.jsonl` / `sft_data_cot_harmful.jsonl`（v1 文件名），且脚本底部的"Run commands"示例只写了 v1/v2/v3，未加 v4。`python data-sft/analyze_strategy_distribution.py` 无参直接跑会用 12 类矩阵去扫 v1 JSONL（含 S12/S14 行），这些行会被静默丢弃（不在 12 类 lookup 里），产出误导性分布图。
10. **`scripts/analyze_archive_pool.py:52-65,80`** — 常量表剪到 12（正确）；但脚本只适合 v4 12×10 pool。若拿它跑旧 14×10 checkpoint，原 `idx=11 Suicide & Self-Harm` 以及所有 idx≥12 的条目都会走 `bad_strategy` 分支被静默丢弃，同时 heatmap 形状错位。docstring 只写了"12 entries"但没标注"不能用于 legacy 14×10"。
11. **`data-sft/run_cot_distill_v4.sh:75-79`** — clean step 的 `STRATEGY_PATTERN` 仍是严格 `\s*\n\s*` 版本；注释写"mirrors extract_strategy_text in game.py"，但 `src/verl/verl/utils/reward_score/game.py:121-126` 现在是 relaxed `[\s,;]+` 版本。策略上 distill 端保持严格其实合理（Gemini 的输出稳定带换行，严格正则充当 noise filter），但注释说法已陈旧。
12. **`src/360-LLaMA-Factory/examples/train_full/qwen2d5-7b_v4_full_sft_dsz2_cp.yaml`** — 与正式 v4 yaml 同目录共存的 `_cp` 文件名字有"v4"但 `dataset: game_cot_dace_v1nv2_v3_*`、`num_train_epochs: 30`、输出 `…_cp` 路径；是前轮开发 stub，本轮没清理。用户看到"v4_cp"易误用。

---

## 问题分级与修补方案

### P0（阻塞端到端跑通，必须本轮修）

**P0.1 · 同步 `preprocess_dace.py` 的 "14 Risk Categories" 为 "12"**
- 文件：`data/safety/preprocess_dace.py`
- 位置：L71 单行
- 改动：`exactly one of the 14 Risk Categories` → `exactly one of the 12 Risk Categories`
- 理由：该文件是 RL attacker 实时 prompt 源，当前和 L28-56 的 12 项 list 自相矛盾；attacker SFT 已学到"12 中选一"，RL 阶段 prompt 突然说 14 会直接冲击 format reward 和 strategy 命中率。
- 标注：保持现有 `### dace: v4 — 12-risk strategy space …` 注释不变。

**P0.2 · `check_benign_data_quality.py` 追加 `dace_v4` 入口**
- 文件：`scripts/check_benign_data_quality.py`
- 位置：L17-20 `DATA_FILES` 字典
- 改动：新增 `"dace_v4": "src/360-LLaMA-Factory/data/game_cot_dace_v4_benign.json"`
- 理由：Phase 1b `--dataset dace_v4 --stats-only` 是 plan 写死的验收步骤；当前未加会直接 argparse KeyError。
- 不改别的：不动 base_url / api_key 默认（那些已是占位 `{{FAKE_API_KEY}}`，另案）。

**P0.3 · 解除硬编码 secrets**
- 文件 A：`data-sft/distill_v4_vanilla_benign_jsonl.py:288-289`
- 文件 B：`data-sft/distill_v4_vanilla_harmful_jsonl.py:312-313`
- 文件 C：`scripts/rl/separated/grpo_dace_diversity_v4.sh:10`
- 改动统一模式：
  ```python
  # distill_v4_*.py
  api_key = os.environ.get("DACE_DISTILL_API_KEY")
  base_url = os.environ.get("DACE_DISTILL_BASE_URL", "http://35.220.164.252:3888/v1/")
  assert api_key, "set DACE_DISTILL_API_KEY to run distillation"
  client = OpenAI(api_key=api_key, base_url=base_url)
  ```
  ```bash
  # grpo_dace_diversity_v4.sh
  : "${WANDB_API_KEY:?set WANDB_API_KEY before running v4 RL}"
  export WANDB_API_KEY
  ```
- 理由：`set -x` + hardcoded key 每次 stderr 都泄露；只要这脚本/文件被 pastebin、wandb 日志、screen copy 出去就外泄。
- 副作用：执行前需要 `export DACE_DISTILL_API_KEY=… && export WANDB_API_KEY=…`；在 `dace_v4_rebuild_decisions.md` 的 Phase 1 / Phase 3 命令前加一行说明。

**P0.4 · v4 SFT checkpoint 路径失败即停**
- 文件：`scripts/rl/separated/grpo_dace_diversity_v4.sh`
- 位置：L86-87 附近
- 改动：
  ```bash
  QWEN257BI_SFT_DACE_V4_MODEL_PATH="${QWEN257BI_SFT_DACE_V4_MODEL_PATH:-}"
  if [[ -z "$QWEN257BI_SFT_DACE_V4_MODEL_PATH" || ! -d "$QWEN257BI_SFT_DACE_V4_MODEL_PATH" ]]; then
    echo "[v4] ERROR: set QWEN257BI_SFT_DACE_V4_MODEL_PATH to the real Phase-2 checkpoint" >&2
    exit 2
  fi
  ```
- 理由：当前 `checkpoint-N` 占位符会让 rollout 在 HF load 时 FileNotFoundError（几秒内退出，但白白占用 ray 集群启动）；早退能节省 30-60s/次 trial。
- 同时更新 `dace_v4_rebuild_decisions.md` Phase 3 的命令前提："export QWEN257BI_SFT_DACE_V4_MODEL_PATH=…/checkpoint-XXXX"。

**P0.5 · 切分 `.pyc` 删除到独立提交**
- 文件：`data/safety/__pycache__/preprocess_dace.cpython-310.pyc`
- 改动建议：不在本轮 v4 commit 里 stage 这个 delete；拆成独立 "chore: stop tracking cached pyc" + 在 `.gitignore` 追加 `*.pyc` / `__pycache__/`。
- 理由：此删除动作与 v4 研究无关，混入会让 v4 commit diff 多一个 Bin 文件扰动；另外 `.gitignore` 目前不覆盖 pyc，未来还会被再次加入。
- 本轮只需：`git restore --staged data/safety/__pycache__/preprocess_dace.cpython-310.pyc` 之后 `git checkout -- <path>` 或保留 working-tree delete 但**不 stage**进 v4 commit；不强求本轮改 `.gitignore`。

### P1（不阻塞但影响正确性/可读性，本轮一起修成本低）

**P1.1 · 修正 `analyze_strategy_distribution.py` 默认参数 + 补 v4 用法**
- 文件：`data-sft/analyze_strategy_distribution.py`
- 改动 A：把默认 `--benign` / `--harmful` 改为 v4 文件名（`sft_data_cot_v4_benign.jsonl` / `_harmful.jsonl`），并把 `--tag` 默认改为 `"v4"`；或保持默认不变但在 `main()` 入口额外加一条"若用默认路径，stderr 提示这只适用于 v4"。前者改动最小，推荐。
- 改动 B：脚本底部 Run commands docstring 追加 v4 例：
  ```
  # v4 (after running bash data-sft/run_cot_distill_v4.sh):
  python data-sft/analyze_strategy_distribution.py \
      --benign  data-sft/sft_data_cot_v4_benign.jsonl \
      --harmful data-sft/sft_data_cot_v4_harmful.jsonl \
      --tag v4
  ```
- 理由：脚本常量表已剪到 12，但默认指向 v1 JSONL；无参执行会用 12 类矩阵分析含 S12/S14 的旧数据 → 14 类里 idx 11/13 条目被 `update_matrix` 的 `if risk in risk2idx` 静默丢弃，heatmap 结果偏低且不报错。

**P1.2 · `harmful` distill 模板撇号同步**
- 文件：`data-sft/distill_v4_vanilla_harmful_jsonl.py`
- 位置：L53、L55、L69
- 改动：3 处 `’` → `'`
- 理由：让 `preprocess_dace.py` / `distill_v4_benign` / `distill_v4_harmful` 的 `COMMON_STRATEGY_GUIDANCE` 保持字节级一致。方便后续 diff/校验（`diff <(sed -n '/Risk Categories/,/^$/p' …benign) <(sed -n '…' …harmful)` 直接干净）。
- 注：此差异对 Gemini 语义无影响，仅影响一致性审计。

**P1.3 · `run_cot_distill_v4.sh` 注释与真实正则的同步说明**
- 文件：`data-sft/run_cot_distill_v4.sh:75`
- 改动：把注释 `### dace: strategy regex mirrors extract_strategy_text in src/verl/verl/utils/reward_score/game.py ###` 改为：
  ```
  ### dace: strategy regex is a strict subset of extract_strategy_text in game.py
  # (distill-time validator keeps `\n` requirement as an extra noise filter on
  # Gemini output; game.py's relaxed regex only matters at RL rollout parse time). ###
  ```
- 理由：用户/reviewer 看到"mirrors"字样后翻 game.py 会发现不一致，会误以为 v4 漏改。明说"strict subset / 设计差异"可以避免二次 review。

**P1.4 · `analyze_archive_pool.py` 对老 pool 的 legacy 兼容**
- 文件：`scripts/analyze_archive_pool.py`
- 改动 A（最小）：在 docstring 顶端补一行警告：
  ```
  NOTE: v4 only. Cannot analyze legacy 14x10 pools correctly — old idx 11/12/13
  (Suicide & Self-Harm / Sexual Content / Elections / Code Interpreter Abuse in
  the 14-slot ordering) will be silently dropped as bad_strategy. Use the v3
  branch of this script for 14x10 archives.
  ```
- 改动 B（可选）：加 `--legacy-14x10` 开关，命中时换用 14 项表 + 140 slot heatmap。复杂度中等，可留给下一轮。
- 本轮：做改动 A 即可，把误用门槛拉高；改动 B 列成未来 TODO。

**P1.5 · 清理 / 重命名 `qwen2d5-7b_v4_full_sft_dsz2_cp.yaml`**
- 文件：`src/360-LLaMA-Factory/examples/train_full/qwen2d5-7b_v4_full_sft_dsz2_cp.yaml`
- 改动：直接删除此 stub（它实际用 v3 数据 + 30 epoch），或重命名成 `qwen2d5-7b_v4_full_sft_dsz2_draft_30ep.yaml` 并 `# DO NOT USE for v4 training` 置顶。推荐**删除**。
- 理由：与正式 `qwen2d5-7b_v4_full_sft_dsz2.yaml` 同目录同前缀，tab-补全时极易误选；且 `_cp` stub 没有任何 active 依赖。

### P2（文档/留档性质，不必本轮改，但列清避免遗忘）

**P2.1 · Plan 中"12x10 会释放 delta_max 压制"表述收紧**
- 文件：`z_materials/dace_v4_rebuild_decisions.md`
- 建议在 "Open Risks" 段追加一条："剪 dead rows 只减少 delta_max 分母里的 '对空 slot 加 1' 这一项的上界贡献，但若剩余 120 slot 里仍有占比 < 5% 的稀有 slot，delta_max 依然由它们决定。若 v4 实跑后 `diversity/mean_reward` 没显著抬升，下一轮考虑 active-mask 或按 `data_type` 拆双 pool"。
- 理由：GPT review 和我独立分析都指出此表述有点强；为后续实验阅读者留一条 hedge。

**P2.2 · eval 侧 LG4 S1-S14 报告口径说明**
- 文件：`z_materials/dace_v4_rebuild_decisions.md` "向后不兼容" 段
- 追加："Eval（safety-eval-fork / AISafetyLab / OpenRT）不受 v4 剪裁影响；它们沿用外部 LG3/LG4 完整分类（含 Sexual Content / Code Interpreter Abuse）。v4 训练空间 12×10 只影响 attacker SFT/RL 的 strategy conditioning"。
- 已 grep 验证：`eval-dace/AISafetyLab/.../llama_guard_3_scorer.py:40-42` 还写着 `S12 Sexual Content` / `S14 Code Interpreter Abuse`，这是**正确行为**（外部 scorer），不要改。

**P2.3 · `dataset_info.json` 未映射 `answer` 列属预期**
- v4 三项 `game_cot_dace_v4_{benign,harmful,all}` 只映射 `instruction/input/output/system`，未显式映射 `answer`。这与 v2/v3 入口完全一致；`answer` 字段在 convert_v4 输出里仅作为 metadata 保留，LLaMA-Factory 训练只用 `output` 里的完整 CoT。无需改。但在下一轮 README 里说明：若未来要让 SFT loss 只打在 `<answer>` 片段上，需要改 dataset schema + trainer mask 逻辑，不是仅改 dataset_info。

---

## 关键文件 & 位置索引（本轮要动的文件，按依赖顺序）

| Priority | 文件 | 位置 | 动作 |
|---|---|---|---|
| P0.1 | `data/safety/preprocess_dace.py` | L71 | `14` → `12` |
| P0.2 | `scripts/check_benign_data_quality.py` | L17-20 | 追加 `dace_v4` 条目 |
| P0.3a | `data-sft/distill_v4_vanilla_benign_jsonl.py` | L287-290 | api_key/base_url 读 env |
| P0.3b | `data-sft/distill_v4_vanilla_harmful_jsonl.py` | L311-314 | 同上 |
| P0.3c | `scripts/rl/separated/grpo_dace_diversity_v4.sh` | L10 | WANDB_API_KEY 读 env + fail-fast |
| P0.4 | `scripts/rl/separated/grpo_dace_diversity_v4.sh` | L86-88 | v4 ckpt 存在性校验 |
| P0.5 | `data/safety/__pycache__/preprocess_dace.cpython-310.pyc` | (working tree) | 单独成 commit 或保留 untracked |
| P1.1 | `data-sft/analyze_strategy_distribution.py` | L160-167, 200-230 | 默认路径 + 用法示例 |
| P1.2 | `data-sft/distill_v4_vanilla_harmful_jsonl.py` | L53, 55, 69 | 撇号改 ASCII |
| P1.3 | `data-sft/run_cot_distill_v4.sh` | L75 | 注释改为 "strict subset" 说明 |
| P1.4 | `scripts/analyze_archive_pool.py` | L1-40 docstring | legacy 告警 |
| P1.5 | `src/360-LLaMA-Factory/examples/train_full/qwen2d5-7b_v4_full_sft_dsz2_cp.yaml` | 整文件 | 删除 |

`src/verl/verl/separated_trainer/ppo/archive_pool.py`、`src/verl/verl/utils/reward_score/game.py`、`src/verl/verl/separated_trainer/ppo/ray_trainer.py` 本轮**不改动**（v4 核心行为无已知 bug；第三轮已完成 relaxed regex + flow metric）。

---

## 验收命令（每条对应一个修补项）

```bash
# Root
cd /mnt/shared-storage-user/yupeng/MAGIC

# P0.1: 确保 v4 surface 无 "14 Risk" 残留
grep -rn -E "of the 14 Risk|14 Risk Categories" \
  data/safety/preprocess_dace.py \
  data-sft/distill_v4_vanilla_*.py \
  data-sft/run_cot_distill_v4.sh \
  src/verl/verl/separated_trainer/ppo/archive_pool.py
# 期望：无输出

# P0.2: --dataset dace_v4 能被 argparse 解析
python scripts/check_benign_data_quality.py --dataset dace_v4 --stats-only --help 2>&1 | head -3
# 期望：正常打印 usage，而不是 "invalid choice: 'dace_v4'"

# P0.3: 没有硬编码 secret
grep -nE 'api_key\s*=\s*"sk-|WANDB_API_KEY="[0-9a-f]' \
  data-sft/distill_v4_vanilla_*.py \
  scripts/rl/separated/grpo_dace_diversity_v4.sh
# 期望：无输出

# P0.4: grpo v4 脚本在缺 checkpoint 时立即退出
bash -x scripts/rl/separated/grpo_dace_diversity_v4.sh 2>&1 | head -10
# 期望：前几行就看到 "[v4] ERROR: set QWEN257BI_SFT_DACE_V4_MODEL_PATH …"

# P1.1: analyze_strategy_distribution 默认跑 v4
ls -la data-sft/sft_data_cot_v4_benign.jsonl data-sft/sft_data_cot_v4_harmful.jsonl 2>/dev/null
python data-sft/analyze_strategy_distribution.py  # 或默认改后就自然指向 v4

# P1.2: 撇号一致
python3 -c "import pathlib; \
a=pathlib.Path('data-sft/distill_v4_vanilla_benign_jsonl.py').read_text(); \
b=pathlib.Path('data-sft/distill_v4_vanilla_harmful_jsonl.py').read_text(); \
print('benign_curly', a.count('’'), 'harmful_curly', b.count('’'))"
# 期望：benign_curly 0 harmful_curly 0

# P1.3: 注释不再声称 mirror
grep -n "mirrors extract_strategy_text" data-sft/run_cot_distill_v4.sh
# 期望：无匹配（已改为 "strict subset"）

# P1.4: docstring 带 legacy 警告
head -20 scripts/analyze_archive_pool.py | grep -i "v4 only\|Cannot analyze legacy"
# 期望：命中新增警告行

# P1.5: stub yaml 已清理
ls src/360-LLaMA-Factory/examples/train_full/qwen2d5-7b_v4_full_sft_dsz2*.yaml
# 期望：只有正式 qwen2d5-7b_v4_full_sft_dsz2.yaml
```

---

## 兼容性 & 风险

- 本轮全部改动都在**非核心 RL 路径**：不动 archive_pool 的 Thompson/prune/decay、不动 reward_score/game.py 的 regex、不动 ray_trainer switching 逻辑。已通过的 15 条 regression（第四轮落地时验证过）无需重跑；只需重跑 P0.2/P0.3/P0.4 对应的入口级 smoke。
- P0.3 改完后，如果之前有别的人在这台机器上靠 shell history 恢复密钥去跑 distill，会出现 "assert failed"；这是有意的行为（从此不再留明文）。在 `dace_v4_rebuild_decisions.md` Phase 1 前加一行 export 指令即可。
- P0.5 如果误 stage 了 `.pyc` 删除，后续 pull 的同事本地会缺这个 binary，无副作用（Python 会自动重新生成）。

---

## 未处理 / 留给下一轮（不在本轮修补范围）

- `archive_pool.py` 的 `extract_strategy` 语义是否需要 active-mask（S12/S14 已整体剪掉，剩余 120 slot 如果仍出现稀有 slot 压制 delta_max，再议）
- `data-sft/analyze_strategy_distribution.py` 是否加 `--version v4` 开关族（本轮用默认路径切换即可）
- `scripts/analyze_archive_pool.py` 的 `--legacy-14x10` 开关（本轮仅加警告，不做双模式）
- Eval 链路的 LG4 taxonomy 全量报告（与训练空间解耦，与 v4 无关）
- `compute_reward_bundle` 的 benign 成功判定是否再加"q_safe_label 必须仍 benign"的硬兜底（与 prompt 修复同步上线前不动）

---

## 本轮只改以下 12 个文件（对照 P0/P1/P2 清单收敛）

```
modified:
  data/safety/preprocess_dace.py                               (P0.1)
  scripts/check_benign_data_quality.py                         (P0.2)
  data-sft/distill_v4_vanilla_benign_jsonl.py                  (P0.3a)
  data-sft/distill_v4_vanilla_harmful_jsonl.py                 (P0.3b, P1.2)
  scripts/rl/separated/grpo_dace_diversity_v4.sh               (P0.3c, P0.4)
  data-sft/analyze_strategy_distribution.py                    (P1.1)
  data-sft/run_cot_distill_v4.sh                               (P1.3)
  scripts/analyze_archive_pool.py                              (P1.4)
  z_materials/dace_v4_rebuild_decisions.md                     (P2.1, P2.2, Phase 1/3 env 说明)

deleted:
  src/360-LLaMA-Factory/examples/train_full/qwen2d5-7b_v4_full_sft_dsz2_cp.yaml   (P1.5)

keep working-tree only (do NOT stage in v4 commit):
  data/safety/__pycache__/preprocess_dace.cpython-310.pyc       (P0.5)

no touch:
  src/verl/... (archive_pool.py, reward_score/game.py, ray_trainer.py)
  src/360-LLaMA-Factory/data/dataset_info.json      (v4 三条注册已正确)
  src/360-LLaMA-Factory/examples/train_full/qwen2d5-7b_v4_full_sft_dsz2.yaml
  data-sft/convert_v4_cot_to_game_format.py          (review 无发现)
  z_materials/dace_benign_prompt_conflict.md         (头部 update 已写)
```
