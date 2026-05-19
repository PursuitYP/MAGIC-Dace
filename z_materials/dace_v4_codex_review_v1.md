# Codex Review: DACE v4 Opus Implementation

## Summary

- Opus v4 实现方向总体正确：已覆盖 benign prompt 语义修复、12x10 attack space、v4 SFT/RL 脚本、dataset 注册和 `rollout.n=6`。
- 但当前实现不建议直接跑正式 v4，全链路仍有几处运行阻断和一致性问题。
- 已做只读校验：`git diff --check` 通过，两个 shell 脚本 `bash -n` 通过，新增 Python 文件 AST 通过，`dataset_info.json` 合法，SFT YAML 可解析，`ArchivePool` 12x10 抽取逻辑基本正确。

## P0 Findings

- `data/safety/preprocess_dace.py` 的 `COMMON_RESPONSE_FORMAT` 仍写 "14 Risk Categories"，但 v4 distill 脚本已写 12；这会造成 RL prompt 与 SFT prompt 不一致。必须改为 12。
- `scripts/check_benign_data_quality.py --dataset dace_v4` 被文档列为运行步骤，但 `DATA_FILES` 没有 `dace_v4`，命令当前不可用。必须追加 v4 benign JSON 路径。
- v4 蒸馏脚本硬编码 OpenAI-compatible API key/base_url，RL 脚本硬编码 `WANDB_API_KEY`，且 `set -x` 会扩大泄露风险。必须改为环境变量读取或 fail-fast。
- `scripts/rl/separated/grpo_dace_diversity_v4.sh` 的 v4 SFT checkpoint 仍是 `checkpoint-N` 占位；直接运行会失败。必须要求环境变量传入真实 checkpoint 或增加路径检查。
- `data/safety/__pycache__/preprocess_dace.cpython-310.pyc` 是已跟踪文件且当前被删除。不要混入 v4 研究提交；单独恢复或单独清理 tracked cache。

## P1 Findings

- `analyze_strategy_distribution.py` 已改成 12 类，但默认输入仍是 v1 JSONL；直接运行默认命令会用 12 类分析旧 14 类数据，S12/S14 会被丢掉。应把 v4 命令写成显式参数，或加 taxonomy/version 参数。
- `scripts/analyze_archive_pool.py` 现在只适合 v4 12x10 pool；若拿它分析旧 14x10 pool，会把旧 idx 12/13 计入 `bad_strategy`，结果误导。文档要明确只用于 v4，或保留 legacy 模式。
- `run_cot_distill_v4.sh` 清洗正则仍强制 strategy 两行换行，和 reward/archive 的 relaxed regex 不一致。若保留严格清洗，应修正文档注释，不要写 "mirrors extract_strategy_text"。
- `distill_v4_vanilla_harmful_jsonl.py` 的 `COMMON_STRATEGY_GUIDANCE` 和 `preprocess_dace.py` 仅有撇号字符差异，语义不变，但不满足"逐字同步"的计划描述。建议统一为完全一致文本或抽共享模板。
- Opus 记录里"12x10 会释放 delta_max 压制"的表述偏强。剪 S12/S14 能减少 dead rows 和数据污染，但不能保证 diversity reward 分母问题显著改善；若要彻底解决，后续仍需 active-mask 或按 data_type 拆表。

## Recommended Fix Plan

- 同步 prompt：把 active v4 文件里的 14/12 计数、risk list、response format 全部校齐，尤其 `preprocess_dace.py`。
- 补齐可运行入口：增加 `dace_v4` Guard 检查入口，更新文档中的 analyze 命令为显式 v4 JSONL。
- 移除硬编码秘密：蒸馏 API、W&B key、内部 endpoint 全部改成环境变量；RL 脚本对缺失 v4 checkpoint 立即退出。
- 明确版本边界：v4 analyze 脚本只分析 v4 pool/v4 JSONL；旧 14x10 结果用旧脚本或显式 legacy 参数。
- 清理提交边界：不要把 pyc 删除和研究代码混在一个提交；生成的 v4 SFT JSON 大文件只在确认为必要输入时提交。

## Acceptance Checks

- `grep` active v4 files 不再出现误导性的 "14 Risk Categories"。
- `python scripts/check_benign_data_quality.py --dataset dace_v4 --stats-only` 能解析参数。
- `ArchivePool` 自检得到 `N_RISK=12, N_STYLE=10, N_SLOTS=120`，`Elections -> (11, 0)`，`Sexual Content/Code Interpreter Abuse -> None`。
- `python data-sft/analyze_strategy_distribution.py --benign data-sft/sft_data_cot_v4_benign.jsonl --harmful data-sft/sft_data_cot_v4_harmful.jsonl --tag v4` 作为唯一推荐 v4 分布命令。
- RL smoke 前确认 v4 checkpoint 真实存在，不是 `checkpoint-N`。
