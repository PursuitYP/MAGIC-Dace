#!/usr/bin/env bash
set -x

PROJECT_DIR="/mnt/shared-storage-user/yupeng/MAGIC"
PROJECT_DIR_WXY="/mnt/shared-storage-user/wenxiaoyu/game-private"
WORKSPACE="/mnt/shared-storage-user/wenxiaoyu"
CHECKPOINT_DIR="/mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/yupeng/ckpt"

# Optional: export VLLM_ATTENTION_BACKEND=XFORMERS
export WANDB_API_KEY="2d2ad4b937a9c0d7623dcc78dc25c07fe3eaa0a9"
export WANDB_BASE_URL="https://api.bandw.top"
export WANDB_MODE=offline
export NCCL_DEBUG=INFO
export SGL_DISABLE_TP_MEMORY_INBALANCE_CHECK=True

export REVISION_MODEL_PATH="${REVISION_MODEL_PATH:-$WORKSPACE/models/roberta-large-wanli}"
export REVISION_MODEL_DEVICE=cpu
export ENABLE_REVISION_REWARD=0
export ENABLE_DEFENDER_QUALITY_REWARD=0
export FORMAT_REWARD_VALUE=1
export RAY_MASTER_PORT=6379
export REWARD_MODEL_USE_ANSWER_TAGS=0
export REWARD_HARM=1
export REWARD_REFUSAL=0.5
export REWARD_LABEL=0
export USE_Q_SAFE_LABEL_FOR_REFUSAL=1
export WILDGUARD_API_ENDPOINT="http://s-20251119153749-lp69w-decode.ailab-safethm.svc:23344/v1"
export SAFETY_RULE_API_ENDPOINT="${SAFETY_RULE_API_ENDPOINT:-}"
export DEFENDER_QUALITY_API_ENDPOINT="${DEFENDER_QUALITY_API_ENDPOINT:-}"
export REVISION_SCORE_ENDPOINT="${REVISION_SCORE_ENDPOINT:-${REVISION_ENDPOINT:-}}"
export SAFETY_SCORE_MODE=${SAFETY_SCORE_MODE:-classifier} # classifier | rule_api (set SAFETY_RULE_API_ENDPOINT + SAFETY_RULE_PROMPT_PATH)
export SAFETY_RULE_SYSTEM_PROMPT_PATH=${SAFETY_RULE_SYSTEM_PROMPT_PATH:-$PROJECT_DIR/src/verl/verl/utils/reward_score/defender_judge_system_prompt.txt}
export SAFETY_RULE_PROMPT_PATH=${SAFETY_RULE_PROMPT_PATH:-$PROJECT_DIR/src/verl/verl/utils/reward_score/defender_judge_user_prompt.txt}
export SAFETY_RULE_SAFE_SYSTEM_PROMPT_PATH=${SAFETY_RULE_SAFE_SYSTEM_PROMPT_PATH:-$PROJECT_DIR/src/verl/verl/utils/reward_score/defender_helpful_system_prompt.txt}
export SAFETY_RULE_SAFE_PROMPT_PATH=${SAFETY_RULE_SAFE_PROMPT_PATH:-$PROJECT_DIR/src/verl/verl/utils/reward_score/defender_judge_user_prompt.txt}
export SAFETY_RULE_SCORE_MIN=${SAFETY_RULE_SCORE_MIN:-0}
export SAFETY_RULE_SCORE_MAX=${SAFETY_RULE_SCORE_MAX:-10}
export REWARD_SCORE_MAX_WORKERS=${REWARD_SCORE_MAX_WORKERS:-1}
export REWARD_SCORE_TIMEOUT_S=${REWARD_SCORE_TIMEOUT_S:-30}

ATTACKER_RATIO=${ATTACKER_RATIO:-1}
DEFENDER_RATIO=${DEFENDER_RATIO:-1}
UPDATE_FREQ=${UPDATE_FREQ:-15}
SWITCH_MODE=${SWITCH_MODE:-ratio} # metric | ratio
SWITCH_METRIC_NAME=${SWITCH_METRIC_NAME:-reward/response_harm}
SWITCH_METRIC_LOW=${SWITCH_METRIC_LOW:-0.80}
SWITCH_METRIC_HIGH=${SWITCH_METRIC_HIGH:-0.90}
SWITCH_METRIC_WINDOW=${SWITCH_METRIC_WINDOW:-3}

timestamp=$(date '+%Y-%m-%d_%H-%M-%S')
project_name=game
# experiment_name="D-q257bi-A-q257bisft_wocode-reward1_0.5_0-woDformat-wo_label_reward-revised_label-${timestamp}"
experiment_name="D-q257bi-A-q257bisft_wocode-reward1_0.5_0-woDformat-wo_label_reward-revised_label-tp2-${timestamp}"

# DEFENDER BASE MODEL
LLAMA_38BI_MODEL_PATH=$WORKSPACE/models/Meta-Llama-3-8B-Instruct/snapshots/8afb486c1db24fe5011ec46dfbe5b5dccdb575c2
LLAMA_318BI_MODEL_PATH=$WORKSPACE/models/Meta-Llama-3.1-8B-Instruct
LLAMA_318BIA_MODEL_PATH=$WORKSPACE/models/Meta-Llama-3.1-8B-Instruct-abliterated
QWEN_257BI_MODEL_PATH=$WORKSPACE/models/Qwen2.5-7B-Instruct
QWEN_257B_MODEL_PATH=$WORKSPACE/models/Qwen2.5-7B
QWEN_2514B_MODEL_PATH=${QWEN_2514B_MODEL_PATH:-/path/to/Qwen2.5-14B-Instruct}
QWEN_38BI_MODEL_PATH=$WORKSPACE/models/Qwen3-8B
QWEN_38B_BASE_MODEL_PATH=$WORKSPACE/models/Qwen3-8B-Base
QWEN_314B_MODEL_PATH=$WORKSPACE/models/Qwen3-14B
QWEN_314B_BASE_MODEL_PATH=$WORKSPACE/models/Qwen3-14B-Base

# SFT MODEL
LLAMA3_8BI_MODEL_PATH=$PROJECT_DIR/src/360-LLaMA-Factory/saves/llama3-8BI-cot_w_harm_gemini/full/sft/checkpoint-9200
LLAMA31_8BI_MODEL_PATH=$PROJECT_DIR/src/360-LLaMA-Factory/saves/llama31-8BI-cot_w_harm_gemini/full/sft/checkpoint-9600
LLAMA31_8BIA_MODEL_PATH=$PROJECT_DIR/src/360-LLaMA-Factory/saves/llama31-8BIA-cot_w_harm_gemini/full/sft/checkpoint-9200
LLAMA31_8BI_SFT_WOCODE_MODEL_PATH=$PROJECT_DIR/src/360-LLaMA-Factory/saves/llama31-8BI-cot_w_harm_gemini_wocode/full/sft/checkpoint-8367
SFTV1_MODEL_PATH=$PROJECT_DIR/src/360-LLaMA-Factory/saves/qwen2.5-7B-Base-cot_w_harm/full/sft/checkpoint-4000
# SFTV2_MODEL_PATH=$PROJECT_DIR/src/360-LLaMA-Factory/saves/qwen2.5-7BI-cot_w_harm_gemini/full/sft/checkpoint-7200
SFTV3_MODEL_PATH=$PROJECT_DIR/src/360-LLaMA-Factory/saves/qwen2.5-7B-Base-cot_w_harm_gemini/full/sft/checkpoint-8800
SFTV4_MODEL_PATH=$PROJECT_DIR/src/360-LLaMA-Factory/saves/qwen2.5-7BI-cot_w_harm_gemini/full/sft/checkpoint-9200
SFTV5_MODEL_PATH=$PROJECT_DIR/src/360-LLaMA-Factory/saves/qwen2.5-7BI-cot_w_harm_gemini_v2/full/sft/checkpoint-6150
SFTV6_MODEL_PATH=$PROJECT_DIR/src/360-LLaMA-Factory/saves/qwen2.5-7B-cot_w_harm_gemini_v2/full/sft/checkpoint-6150
SFTV7_MODEL_PATH=$PROJECT_DIR/src/360-LLaMA-Factory/saves/qwen2.5-7BI-cot_w_harm_gemini_v3/full/sft/checkpoint-12885
# use PROJECT_DIR_WXY (not PROJECT_DIR) for sft checkpoints
QWEN257BI_SFT_WOCODE_MODEL_PATH=$PROJECT_DIR_WXY/src/360-LLaMA-Factory/saves/qwen2.5-7BI-cot_w_harm_gemini_wocode/full/sft/checkpoint-8367
QWEN2514B_SFT_MODEL_PATH=$PROJECT_DIR/src/360-LLaMA-Factory/saves/qwen2.5-14BI-cot_w_harm_gemini/full/sft/checkpoint-9705
QWEN2514B_SFT_WOCODE_MODEL_PATH=$PROJECT_DIR/src/360-LLaMA-Factory/saves/qwen2.5-14BI-cot_w_harm_gemini_wocode/full/sft/checkpoint-8367
QWEN38BI_MODEL_PATH=$PROJECT_DIR/src/360-LLaMA-Factory/saves/qwen3-8B-cot_w_harm_gemini/full/sft/checkpoint-8800
QWEN38B_BASE_MODEL_PATH=$PROJECT_DIR/src/360-LLaMA-Factory/saves/qwen3-8B-Base-cot_w_harm_gemini/full/sft/checkpoint-8800
QWEN314B_BASE_MODEL_PATH=$PROJECT_DIR/src/360-LLaMA-Factory/saves/qwen3-14B-Base-cot_w_harm_gemini/full/sft/checkpoint-9702
QWEN314B_MODEL_PATH=$PROJECT_DIR/src/360-LLaMA-Factory/saves/qwen3-14B-cot_w_harm_gemini/full/sft/checkpoint-9702


cd "$PROJECT_DIR"
export PYTHONPATH=$(pwd)/src/verl:$PYTHONPATH

ray stop --force

mkdir -p "logs/${project_name}/${experiment_name}"
ray start --head --port=$RAY_MASTER_PORT --dashboard-host=0.0.0.0 --num-gpus 8

sleep 30

SWITCH_ARGS=()
if [[ "${SWITCH_MODE}" == "metric" ]]; then
    SWITCH_ARGS=(
        "algorithm.switch_agent.mode=metric"
        "+algorithm.switch_agent.metric_name=${SWITCH_METRIC_NAME}"
        "+algorithm.switch_agent.metric_low=${SWITCH_METRIC_LOW}"
        "+algorithm.switch_agent.metric_high=${SWITCH_METRIC_HIGH}"
        "+algorithm.switch_agent.metric_window=${SWITCH_METRIC_WINDOW}"
    )
else
    SWITCH_ARGS=(
        "algorithm.switch_agent.mode=ratio"
        "algorithm.switch_agent.freq=${UPDATE_FREQ}"
        "algorithm.switch_agent.update_ratio={}"
        "+algorithm.switch_agent.update_ratio.attacker=${ATTACKER_RATIO}"
        "+algorithm.switch_agent.update_ratio.defender=${DEFENDER_RATIO}"
    )
fi

PYTHONUNBUFFERED=1 python -m verl.separated_trainer.main_ppo \
    trainer.project_name=Game-separated \
    trainer.experiment_name="${experiment_name}" \
    trainer.default_local_dir="${CHECKPOINT_DIR}/Game-separated/${experiment_name}" \
    trainer.resume_mode=disable \
    trainer.nnodes=1 \
    trainer.n_gpus_per_node=4 \
    data.train_files=data/safety/train.parquet \
    data.val_files=data/safety/test_wjb.parquet \
    data.val_batch_size=256 \
    data.train_batch_size=64 \
    data.max_prompt_length=8192 \
    data.max_response_length=6144 \
    actor_rollout_ref.model.use_remove_padding=True \
    +actor_rollout_ref.model.trust_remote_code=True \
    actor_rollout_ref.actor.use_dynamic_bsz=True \
    actor_rollout_ref.actor.use_kl_loss=False \
    actor_rollout_ref.actor.kl_loss_coef=1e-3 \
    actor_rollout_ref.actor.entropy_coeff=0 \
    actor_rollout_ref.actor.ulysses_sequence_parallel_size=1 \
    actor_rollout_ref.actor.ppo_mini_batch_size=32 \
    actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=8 \
    actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=32 \
    actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=32 \
    actor_rollout_ref.rollout.tensor_model_parallel_size=2 \
    actor_rollout_ref.rollout.max_num_batched_tokens=49152 \
    actor_rollout_ref.rollout.max_num_turns=1 \
    actor_rollout_ref.rollout.n=4 \
    actor_rollout_ref.rollout.stop_when_truncated=True \
    actor_rollout_ref.actor.optim.lr=1e-6 \
    actor_rollout_ref.actor.fsdp_config.optimizer_offload=True \
    actor_rollout_ref.rollout.stop_when_truncated_roles=[defender] \
    +trainer.val_before_train=False \
    +trainer.val_only=False \
    +trainer.save_val_generations=True \
    +trainer.save_train_generations=True \
    trainer.test_freq=15 \
    trainer.save_freq=15 \
    trainer.total_epochs=1 \
    trainer.total_training_steps=300 \
    algorithm.adv_estimator=grpo \
    algorithm.switch_agent.model_paths=[${QWEN257BI_SFT_WOCODE_MODEL_PATH},${QWEN_257BI_MODEL_PATH}] \
    algorithm.switch_agent.agent_roles=[attacker,defender] \
    algorithm.switch_agent.train_roles=[attacker,defender] \
    algorithm.switch_agent.start_agent=defender \
    "${SWITCH_ARGS[@]}" \
    reward_model.reward_manager=game \
    reward_model.mask_unfinished_reward=True \
    +reward_model.use_format_reward=True \
    +reward_model.format_reward_roles=[attacker] \
    algorithm.filter_groups.enable=False \
    trainer.logger=[console,wandb] \
    2>&1 | tee "${PROJECT_DIR}/logs/game/${experiment_name}.log"

ray stop --force
