#!/bin/bash

set -euo pipefail

# 模型列表（name path 成对）
MODELS=(
  #"q257i|/mnt/shared-storage-user/wenxiaoyu/models/Qwen2.5-7B-Instruct"
  #"self-redteam-q257i|/mnt/shared-storage-user/wenxiaoyu/models/Self-RedTeam-Qwen2.5-7B-Instruct"
  #"magic-q257i|/mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/wenxiaoyu/game/checkpoints/Game-separated/v5-D-q257bi-A-sft_wocode-ratio11-freq15-reward1_0.5_0-woDformat-wo_label_reward-revised_label-2026-01-17_09-37-46/global_step_225/defender/actor/huggingface"
  #"q2514i|/mnt/shared-storage-gpfs2/gpfs2-shared-public/huggingface/hub/models--Qwen--Qwen2.5-14B-Instruct/snapshots/cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8"
  #"self-redteam-q2514i|/mnt/shared-storage-user/wenxiaoyu/models/Self-RedTeam-Qwen2.5-14B-Instruct"
  #"magic-q2514i|/mnt/shared-storage-user/wenxiaoyu/wxy_hf/MAGIC-Qwen2.5-14B-Instruct/"
  #"self-redteam-l318i-qwenguard| /mnt/shared-storage-user/wenxiaoyu/selfplay-redteaming/checkpoints/selfplay_RL_FULL_PTX_SFT_wjbhs_re++_rtg_0327T17:31/ckpt/global_step200_hf"
  "self-redteam-l318i-wildguard|/mnt/shared-storage-user/wenxiaoyu/selfplay-redteaming/checkpoints/selfplay_RL_FULL_PTX_SFT_wjbhs_re++_rtg_0327T13:52/ckpt/global_step200_hf"
)

# 配置
TASKS="wildguardtest,harmbench_precompute,wildjailbreak:benign,wildjailbreak:harmful,do_anything_now,harmbench,or_bench:hard-1k,or_bench:toxic,xstest"
CLASSIFIER="WildGuardAPI"
RUN_TS="$(date +%Y%m%d_%H%M%S)"

# 环境变量 - 使用 WildGuard API 端点
export WILDGUARD_API_ENDPOINT='http://s-20251128155813-x29q2-decode.ailab-safethm.svc:23442/v1'
export WILDGUARD_API_KEY='FAKE_API_KEY'
export HF_DATASETS_CACHE=/data/hf_cache
export OPENAI_API_KEY="fake-key-for-safety-eval"
export HF_TOKEN="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"
export HF_HUB_OFFLINE=0
export HF_DATASETS_VERBOSITY=info

# 激活环境
eval "$(conda shell.bash hook)"
conda activate safety-eval

# 逐个模型运行评测
for model_entry in "${MODELS[@]}"; do
    MODEL_NAME="${model_entry%%|*}"
    MODEL_PATH="${model_entry#*|}"
    RESULTS_DIR="./results/rebuttal/${MODEL_NAME}/${CLASSIFIER}/-2048-${RUN_TS}"

    mkdir -p "$RESULTS_DIR"

    echo "=================================================="
    echo "开始评测模型: $MODEL_NAME"
    echo "MODEL_PATH: $MODEL_PATH"
    echo "RESULTS_DIR: $RESULTS_DIR"
    echo "Classifier: $CLASSIFIER"
    echo "=================================================="

    python -u evaluation/eval.py generators \
        --model_name_or_path "$MODEL_PATH" \
        --model_input_template_path_or_name "game_defender" \
        --tasks "$TASKS" \
        --report_output_path "$RESULTS_DIR/metrics.json" \
        --save_individual_results_path "$RESULTS_DIR/all_results.json" \
        --use_vllm \
        --classifier_model_name "$CLASSIFIER" \
        --batch_size 1 2>&1 | tee "$RESULTS_DIR/eval.log"

    echo "✓ 当前模型评测完成: $MODEL_NAME"
    echo "  结果目录: $RESULTS_DIR"
    echo
done

echo "✓ 全部模型评测完成"