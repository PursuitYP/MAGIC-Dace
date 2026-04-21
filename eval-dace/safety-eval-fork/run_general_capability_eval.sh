#!/bin/bash

# 配置
MODEL_PATH="/mnt/shared-storage-user/wenxiaoyu/hezhida/TROJail/checkpoints/MUSE_D/lora_merged/all_pairs/global_step_60"
MODEL_NAME="muse-s60"

# Qwen defender 模型建议使用 game_defender
# 如果切到普通 instruct 模型，可改成 "hf"

# 可选: "mmlu" / "mtbench" / "gsm8k"
TASKS="mmlu,gsm8k"

RESULTS_DIR="/mnt/shared-storage-user/wenxiaoyu/game-private/eval/safety-eval-fork/results/multi-turn-defense/MUSE/$MODEL_NAME-helpful/-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULTS_DIR"

# 环境变量
export HF_DATASETS_CACHE=/data/hf_cache
export HF_TOKEN="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"
export HF_HUB_OFFLINE=0
export HF_DATASETS_VERBOSITY=info

# MTBench judge 配置
# 如果 TASKS 里不包含 mtbench，这组变量不会被用到
export OPENAI_API_KEY="sk-D0wGaXJBOV1f6VTnJzwRuhLewJ0Crn1KNQeSXnRRn2dM6ITR"
export OPENAI_BASE_URL="https://api.boyuerichdata.opensphereai.com/v1"
export OPENAI_MODEL="gpt-4o"
export MTBENCH_JUDGE_MODEL="gpt-4o"
export MTBENCH_REF_MODEL="gpt-4o"
export MTBENCH_JUDGE_WORKERS=16

# 激活环境
eval "$(conda shell.bash hook)"
conda activate safety-eval

if [[ "$TASKS" == *"mtbench"* ]] && [[ -z "$OPENAI_API_KEY" || "$OPENAI_API_KEY" == "fake-key-for-safety-eval" ]]; then
    echo "[ERROR] TASKS 包含 mtbench，但 OPENAI_API_KEY 还是占位值。"
    echo "[ERROR] 请先把 OPENAI_API_KEY 改成可用 judge key；如走兼容接口，也请同步设置 OPENAI_BASE_URL。"
    exit 1
fi

echo "[INFO] MODEL_PATH=$MODEL_PATH"
echo "[INFO] MODEL_INPUT_TEMPLATE=$MODEL_INPUT_TEMPLATE"
echo "[INFO] TASKS=$TASKS"
echo "[INFO] RESULTS_DIR=$RESULTS_DIR"

if [[ "$TASKS" == *"mtbench"* ]]; then
    echo "[INFO] MTBENCH_JUDGE_MODEL=$MTBENCH_JUDGE_MODEL"
    echo "[INFO] MTBENCH_REF_MODEL=$MTBENCH_REF_MODEL"
    if [[ -n "$OPENAI_BASE_URL" ]]; then
        echo "[INFO] OPENAI_BASE_URL=$OPENAI_BASE_URL"
    fi
fi

CUDA_VISIBLE_DEVICES=0,1 python -u evaluation/eval.py generators \
    --model_name_or_path "$MODEL_PATH" \
    --model_input_template_path_or_name "hf" \
    --tasks "$TASKS" \
    --report_output_path "$RESULTS_DIR/metrics.json" \
    --save_individual_results_path "$RESULTS_DIR/all_results.json" \
    --batch_size 1 2>&1 | tee "$RESULTS_DIR/eval.log"

echo "✓ 通用能力评测完成: $RESULTS_DIR"
echo "  任务: $TASKS"
