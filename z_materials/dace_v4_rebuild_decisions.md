# DACE v4 重建决策与向后不兼容说明

## 时间与窗口

- 本轮实施：2026-05-01
- 来源：`serialized-leaping-bentley.md` 第四轮 plan
- 目标：一次性处理 BENIGN_TEMPLATE 语义冲突 + 14×10 attack space 里的 dead rows + GRPO group size 扩容

## 用户确认的 4 个决策

| 决策点 | 选择 | 实际落地位置 |
|---|---|---|
| BENIGN_TEMPLATE 改写幅度 | **A 保守**（只改 Win/Lose 文本，不动 SYSTEM_PROMPT / HARM_TEMPLATE / COMMON_STRATEGY_GUIDANCE 以外的部分） | `data/safety/preprocess_dace.py`、`data-sft/distill_v4_vanilla_benign_jsonl.py` 两处同步 |
| rollout.n | **4 → 6** | `scripts/rl/separated/grpo_dace_diversity_v4.sh` L152 |
| REWARD_LABEL（类型一致性奖励） | **0 保持关闭** — 本轮做 ablation，先看单独"改 BENIGN_TEMPLATE + 重蒸馏"是否足以把 refusal_rate_benign 压回 ≤ 0.20 | `grpo_dace_diversity_v4.sh` L25 `export REWARD_LABEL=0` |
| dead rows 处理 | **12×10 剪裁**（剪 S12 Sexual Content + S14 Code Interpreter Abuse），放弃 active-mask | `archive_pool.py`、`preprocess_dace.py`、`distill_v4_*`、`run_cot_distill_v4.sh`、`analyze_*.py` 五处同步 |

## 14 → 12 重新编号映射

```
LG4 taxonomy (14) → DACE v4 training space (12):
  S1  Violent Crimes              → slot 1 (Python idx 0)
  S2  Non-Violent Crimes          → slot 2 (Python idx 1)
  S3  Sex-Related Crimes          → slot 3 (Python idx 2)
  S4  Child Sexual Exploitation   → slot 4 (Python idx 3)
  S5  Defamation                  → slot 5 (Python idx 4)
  S6  Specialized Advice          → slot 6 (Python idx 5)
  S7  Privacy                     → slot 7 (Python idx 6)
  S8  Intellectual Property       → slot 8 (Python idx 7)
  S9  Indiscriminate Weapons      → slot 9 (Python idx 8)
  S10 Hate                        → slot 10 (Python idx 9)
  S11 Suicide & Self-Harm         → slot 11 (Python idx 10)
  S12 Sexual Content              → REMOVED  ← benign Guard not-safe 96.3%, pool 0.23%
  S13 Elections                   → slot 12 (Python idx 11)
  S14 Code Interpreter Abuse      → REMOVED  ← tool-use concept, N/A to MAGIC defender
```

## 向后不兼容

- **旧 14×10 的 `archive_pool.json` checkpoint 不能 resume 到 v4**：`strategy` 元组索引发生语义变化（从 0-13 → 0-11，且原 S13 Elections 现在是 idx 11），直接 resume 会错位。v4 默认 `trainer.resume_mode=disable`，从零训练无此问题。
- **v1/v2/v3 SFT JSONL 不能混入 v4**：里面含有 S12 / S14 样本，会被 `run_cot_distill_v4.sh` 的 canonical check 判为 `bad_risk` 丢弃。v4 必须重新蒸馏。
- **analyze_strategy_distribution 和 analyze_archive_pool 的 heatmap 形状改变**：从 14×10 → 12×10。旧 heatmap 图像需要重新生成才能与 v4 对齐。

## 旧版本仍然可用

- `distill_v2_*.py`、`run_cot_distill_v2.sh`、`convert_v2_*.py` 完全未触，可继续跑老数据
- `qwen2d5-7b_v2/v3_full_sft_dsz2.yaml` 未改
- `grpo_dace_diversity_full.sh`（v3）未改
- 旧的 archive_pool checkpoint 可以用 `archive_pool.py` 之前的版本读（本次改动仅影响 `RISK_CATEGORIES` 常量表）

## 全流水线运行顺序

```bash
# Phase 1: 蒸馏 v4 SFT 数据（idempotent，多次重跑至 err_or_null=0）
cd /mnt/shared-storage-user/yupeng/MAGIC
conda activate magic
bash data-sft/run_cot_distill_v4.sh

# Phase 1b: （可选）Guard filter 监控
python scripts/check_benign_data_quality.py --dataset dace_v4  # 需先在 DATA_FILES 字典追加 v4 入口

# Phase 1c: Convert → Alpaca JSON
python data-sft/convert_v4_cot_to_game_format.py

# Phase 1d: 分布分析
python data-sft/analyze_strategy_distribution.py

# Phase 2: Attacker SFT
conda activate sft
cd src/360-LLaMA-Factory/
CUDA_HOME=$CONDA_PREFIX llamafactory-cli train examples/train_full/qwen2d5-7b_v4_full_sft_dsz2.yaml

# Phase 3: RL Co-Evolution
cd /mnt/shared-storage-user/yupeng/MAGIC
conda activate magic
# 首先编辑 grpo_dace_diversity_v4.sh 里 QWEN257BI_SFT_DACE_V4_MODEL_PATH 的 checkpoint-N 指向 Phase 2 最终 ckpt
bash scripts/rl/separated/grpo_dace_diversity_v4.sh

# Phase 4: Defender checkpoint merge
python src/verl/scripts/model_merger.py \
  --local_dir /mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/yupeng/ckpt/Game-separated/DACE-Diversity-Qwen2.5_7B_Instruct-w_dace_sft_v4-${TIMESTAMP}/global_step_300/defender/actor

# Phase 5: Eval (三条 conda 环境)
# 详细命令见 plan 文件 /home/yupeng/.claude/plans/serialized-leaping-bentley.md 第五章
```

## 验收指标

| 指标 | 当前（v3，log8） | v4 目标 |
|---|---|---|
| DACE benign Guard not-safe rate | 68.2% | ≤ 20% |
| `refusal_rate_benign`（训练全程） | 0.3-0.5 | ≤ 0.20 |
| `refusal_rate_harmful`（末期） | 0.87-0.92 | 保持 0.7-0.9（不要 regression） |
| `archive/strategy_coverage` 分母 | 140 | **120**（v4 剪裁） |
| `archive/pool_size` step 300 | 4000 饱和 | 4000 饱和（正常） |
| `diversity/nonzero_frac` | 0.53-0.73 | ≥ 0.5 |
| `diversity/mean_reward` 绝对量级 | 0.01-0.09 | 预期 ≥ 0.05（dead rows 剪裁后释放 delta_max 压制） |
| `reward/format/attacker_new` | 0.996-1.000 | 保持 ≥ 0.95 |
| `attack/success_rate` 末期 | 0.04-0.09 | 保持 0.05-0.15 |

## Open Risks（本 ablation 需关注）

1. **REWARD_LABEL=0 下的类型漂移**：若 Phase 3 跑出 `refusal_rate_benign` 仍 ≥ 0.30，说明只靠 SFT + prompt 修复不够，下轮需要开启 `REWARD_LABEL=0.2`
2. **rollout.n=6 的 timing 代价**：预期每 step +30-50%。若不可接受，下轮降到 n=5
3. **剪 S12 后 over-refusal 评估缺一维**：Sexual Content 常触发过拒（性教育、文学作品）。Mitigation：eval 侧仍用 LG4 S1-S14 完整 taxonomy 报告
4. **SFT 数据量下降**：Guard filter 后 benign 样本可能从 20k → 15k，harmful 样本变化较小。epoch 保持 3，若数据量显著下降可调至 4-5
