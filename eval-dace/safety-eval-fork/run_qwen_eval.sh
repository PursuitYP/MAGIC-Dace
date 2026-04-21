#!/bin/bash

# 配置
# MODEL_PATH="/mnt/shared-storage-user/wenxiaoyu/hezhida/TROJail/checkpoints/MUSE_D/lora_merged/all_pairs/global_step_60"


# llama 
# 0111 /mnt/shared-storage-user/wenxiaoyu/game-private/checkpoints/Game-separated/v4-D-l318bi-A-l318bisft-reward1_0.5_0-woDformat-ratio11-freq15-wo_label_reward-revised_label-2026-01-08_23-28-04/global_step_225/defender/actor/huggingface
# 0112 defonly /mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/wenxiaoyu/game/checkpoints/Game-separated/v4-D-l318bi-only-A-l318bisft-reward1_0.5_0-woDformat-wo_label_reward-revised_label-2026-01-12_20-18-04/global_step_195
# 0113 a-base /mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/wenxiaoyu/game/checkpoints/Game-separated/v4-D-l318bi-A-l318bia-ratio11-freq15-reward1_0.5_0-woDformat-wo_label_reward-revised_label-2026-01-13_13-50-22/global_step_195/defender/actor/huggingface
# 0119 wocode /mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/wenxiaoyu/game/checkpoints/Game-separated/v5-D-l318bi-A-l318bisft_wocode-ratio11-freq15-reward1_0.5_0-woDformat-wo_label_reward-revised_label-2026-01-19_09-42-38/global_step_195/defender/actor/huggingface
# 0122 nogame /mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/wenxiaoyu/game/checkpoints/Game-separated/v5-D-l318bi-defender-only-seed-trainv2adv-2026-01-22_20-36-45/global_step_195
# llama v4-1.7-freq15-ratio11-revised_label  v4-D-l318bi-A-l318bisft-balanced-8192-reward1_0.5_0.5-woDformat-ratio11-freq15-add_label_reward-revised_label-2026-01-07_11-18-38
# llama v4-1.7-freq10-ratio21-revised_label  v4-D-l318bi-A-l318bisft-reward1_0.5_0.5-woDformat-ratio21-freq10-add_label_reward-revised_label-2026-01-07_11-18-35

# MODEL_PATH="/mnt/shared-storage-user/wenxiaoyu/models/Meta-Llama-3.1-8B-Instruct"



# qwen 7b
# 0104 /mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/wenxiaoyu/game/checkpoints/Game-separated/v3-D-q257bi-A-sftv4-balanced-8192-reward1_0.5_0.5-woDformat-ratio11-freq15-add_label_reward-revised_label-2026-01-04_14-57-50/global_step_285/defender/actor/huggingface
# 0117 wocode-sft /mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/wenxiaoyu/game/checkpoints/Game-separated/v5-D-q257bi-A-sft_wocode-ratio11-freq15-reward1_0.5_0-woDformat-wo_label_reward-revised_label-2026-01-17_09-37-46/global_step_225/defender/actor/huggingface
# def-only v4-D-q257bi-only-A-sftv4-reward1_0.5_0-woDformat-wo_label_reward-revised_label-2026-01-12_20-17-53/global_step_135
# a-it MODEL_PATH="/mnt/shared-storage-user/wenxiaoyu/game-private/checkpoints/Game-separated/v4-D-q257bi-A-q257bi-ratio11-freq15-reward1_0.5_0-woDformat-wo_label_reward-revised_label-2026-01-13_14-25-54/global_step_195/defender/actor/huggingface"
# no-game /mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/wenxiaoyu/game/checkpoints/Game-separated/v5-D-q257bi-defender-only-seed-trainv2adv-2026-01-21_16-36-50/global_step_195/defender/actor/huggingface

# MODEL_PATH="/mnt/shared-storage-user/wenxiaoyu/models/Qwen2.5-7B-Instruct"
# MODEL_PATH="/mnt/shared-storage-user/wenxiaoyu/models/Self-RedTeam-Qwen2.5-7B-Instruct"


# Qwen2.5-14B 
# base /mnt/shared-storage-gpfs2/gpfs2-shared-public/huggingface/hub/models--Qwen--Qwen2.5-14B-Instruct/snapshots/cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8
# self-redteam /mnt/shared-storage-user/wenxiaoyu/models/Self-RedTeam-Qwen2.5-14B-Instruct
# 0118 wocode-sft /mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/wenxiaoyu/game/checkpoints/Game-separated/v5-D-q2514bi-A-q2514bisft_wocode-ratio11-freq15-reward1_0.5_0-woDformat-wo_label_reward-revised_label-2026-01-18_17-48-29/global_step_255
# 0121 code-sft
# /mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/wenxiaoyu/game/checkpoints/Game-separated/v5-D-q2514bi-A-q2514bisft-ratio11-freq15-reward1_0.5_0-woDformat-wo_label_reward-revised_label-2026-01-21_19-47-07/global_step_255/defender/actor/huggingface
# 0123 nogame /mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/wenxiaoyu/game/checkpoints/Game-separated/v5-D-q2514bi-defender-only-seed-trainv2adv-2026-01-23_07-48-54/global_step_195

# v4-1.6-freq15-ratio11-revised_label  v4-D-q257bi-A-sftv4-balanced-8192-reward1_0.5_0.5-woDformat-ratio11-freq15-add_label_reward-revised_label-2026-01-06_13-58-22
# v4-1.6-freq10-ratio21-revised_label  v4-D-q257bi-A-sftv4-balanced-reward1_0.5_0.5-woDformat-ratio21-freq10-add_label_reward-revised_label-2026-01-06_13-58-21


# dace
MODEL_PATH="/mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/yupeng/ckpt/Game-separated/D-q257bi-A-q257bisft_wocode-reward1_0.5_0-woDformat-wo_label_reward-revised_label-tp2-2026-03-31_12-55-34/global_step_300"



#MODEL_NAME="0122-no_game-llama3.1-8b-it"
#MODEL_NAME="0123-no_game-qwen2.5-14b-it"
MODEL_NAME=Muse-step60
#MODEL_NAME="v4-1.6-freq15-ratio11-revised_label"
#TASKS="wildguardtest"
TASKS="wildguardtest,harmbench_precompute,wildjailbreak:benign,wildjailbreak:harmful,do_anything_now,harmbench,or_bench:hard-1k,or_bench:toxic,xstest"
# TASKS="wildjailbreak:benign,xstest"
#STEP="240"
CLASSIFIER="Qwen3GuardAPI"  # 新增：指定分类器
RESULTS_DIR="/mnt/shared-storage-user/wenxiaoyu/game-private/eval/safety-eval-fork/results/multi-turn-defense/MUSE/$MODEL_NAME/$CLASSIFIER/-$(date +%Y%m%d_%H%M%S)"
mkdir -p $RESULTS_DIR

# 环境变量
export WILDGUARD_API_ENDPOINT='http://s-20251119153749-lp69w-decode.ailab-safethm.svc:23344/v1'
export WILDGUARD_API_KEY='FAKE_API_KEY'
export HF_DATASETS_CACHE=/data/hf_cache
export OPENAI_API_KEY="fake-key-for-safety-eval"
export HF_TOKEN="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"
export HF_HUB_OFFLINE=0  # 确保在线模式
export HF_DATASETS_VERBOSITY=info  # 添加详细日志

# 激活环境（修复版本）
 eval "$(conda shell.bash hook)"
 conda activate safety-eval

export VLLM_WORKER_MULTIPROC_METHOD=spawn

# 任务列表
#TASKS="wildguardtest,harmbench_precompute,wildjailbreak:benign,wildjailbreak:harmful,do_anything_now,harmbench,or_bench:hard-1k,or_bench:toxic,xstest"
#wildguardtest无法连接
# 运行评测
CUDA_VISIBLE_DEVICES=0,1 timeout 10800 python -u evaluation/eval.py generators \
    --model_name_or_path "$MODEL_PATH" \
    --model_input_template_path_or_name "game_defender" \
    --tasks $TASKS \
    --report_output_path "$RESULTS_DIR/metrics.json" \
    --save_individual_results_path "$RESULTS_DIR/all_results.json" \
    --use_vllm \
    --classifier_model_name "$CLASSIFIER" \
    --no_extract_answer false\
    --batch_size 1 2>&1 | tee "$RESULTS_DIR/eval.log"

echo "✓ 评测完成: $RESULTS_DIR"