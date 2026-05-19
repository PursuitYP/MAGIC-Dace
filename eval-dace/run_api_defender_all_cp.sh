#!/bin/bash
### dace: merge api-based defender evals (strongreject + olmes ifeval + alpacaeval) ###
# 统一入口：本脚本一次性跑完三组 defender API 评测
#   1. safety-eval-fork / run_strongreject_defender_api  (StrongReject)
#   2. olmes            / run_api_eval                   (IFEval)
#   3. safety-eval-fork / run_alpaca_eval                (AlpacaEval2)
# defender API URL 保持不变（仅变更部署在 URL 后面的模型），只改 MODEL_NAME。
# 结果保存路径与原六个脚本保持一致，每组仍旧 cd 到原目录、激活原 conda env。

# ！！！！！运行前，除了更改脚本中的 MODEL_NAME，记得手动切换 defender 部署 ！！！！！

# ● 两个合并脚本已放到 eval-dace/ 下：                    
                                                                                                                                                                                                                    
#   1. eval-dace/run_path_defender_all.sh — path-based defender（顶部只需改 MODEL_PATH / MODEL_NAME）                                                                                                                 
#   - [1/3] cd safety-eval-fork + env=safety-eval → run_qwen_eval 的 HarmBench/WildGuardTest/DAN/XSTest/WildJailbreak/OR-Bench                                                                                        
#   - [2/3] cd olmes + env=olmes → run_7_benchmarks_eval 的 ARC-C / GPQA                                                                                                                                              
#   - [3/3] cd safety-eval-fork + env=safety-eval → run_general_capability_eval 的 MMLU                                                                                                                               
                                                                                                                                                                                                                    
#   2. eval-dace/run_api_defender_all.sh — api-based defender（顶部只需改 MODEL_NAME，DEFENDER_API_BASE_URL 保持不变）                                                                                                
#   - [1/3] cd safety-eval-fork + env=safety-eval → run_strongreject_defender_api 的 StrongReject                                                                                                                     
#   - [2/3] cd olmes + env=olmes → run_api_eval 的 IFEval                                                                                                                                                             
#   - [3/3] cd safety-eval-fork + env=safety-eval → run_alpaca_eval 的 AlpacaEval2                                                                                                                                    
                                                                                                                                                                                                                    
#   关键实现点：                                                                                                                                                                                                      
#   - 每组评测都包在 (...) subshell 里，cd / conda activate / export 互不污染                                                                                                                                         
#   - 结果目录完全复用原六个脚本的路径（safety-eval-fork/results/dace/...、olmes/results/dace/...），所以原来 6 个结果文件夹照旧                                                                                      
#   - conda shell.bash hook 在外层 eval 一次，subshell 继承函数；env 切换走 subshell 隔离                                                                                                                             
#   - set -o pipefail 但没用 set -e，某一组失败不会拖垮后面的组                                                                                                                                                       
#   - 原脚本里所有 ### dace: ... ### 注释（tiktoken、alpaca annotator、HF_HUB_CACHE 等）都按原位保留                                                                                                                  
                                                                                                                                                                                                                    
#   直接运行：                                                                                                                                                                                                        
#   bash eval-dace/run_path_defender_all.sh                                                                                                                                                                           
#   bash eval-dace/run_api_defender_all.sh   # 跑前自行切部署                                                                                                                                                         


set -o pipefail

# ============================================================
# 统一配置 (api-based defender)
# ============================================================
# MODEL_NAME="DACE-Qwen2.5-7B-v4-attacker1st-step300"
# MODEL_NAME="DACE-Qwen2.5-7B-v4-step300"
MODEL_NAME="DACE-Llama3.1-8B-v4-defender1st-step300"

# defender API：URL 不变，用户自行切换模型部署
# DEFENDER_API_BASE_URL="http://s-20260429151904-5j4n7-decode.ailab-safethm.svc:28658/v1"
DEFENDER_API_BASE_URL="http://s-20260506181841-rr6rc-decode.ailab-safethm.svc:28658/v1"
DEFENDER_API_KEY="FAKE_API_KEY"
DEFENDER_API_MODEL="orm"

# 判官用 GPT-4o API（strongreject/alpacaeval 共用）
GPT4_OPENAI_API_KEY="sk-ua4rD1WerZKpDyb7JHOSKxVvMmvMZIKi6rXGPotdX9nfxNXr"
GPT4_OPENAI_BASE_URL="http://35.220.164.252:3888/v1/"
GPT4_OPENAI_MODEL="gpt-4o"

REPO_ROOT="/mnt/shared-storage-user/yupeng/MAGIC"
EVAL_DACE="$REPO_ROOT/eval-dace"

# HF 通用
export HF_TOKEN="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"
export HF_DATASETS_CACHE=/data/hf_cache
export HF_DATASETS_VERBOSITY=info

# Conda hook
eval "$(conda shell.bash hook)"

echo "=========================================================="
echo "[API-DEFENDER]  MODEL_NAME            = $MODEL_NAME"
echo "[API-DEFENDER]  DEFENDER_API_BASE_URL = $DEFENDER_API_BASE_URL"
echo "[API-DEFENDER]  DEFENDER_API_MODEL    = $DEFENDER_API_MODEL"
echo "=========================================================="

# ============================================================
# 1/3  Table 1 · safety-eval-fork / run_strongreject_defender_api
#     StrongReject (defender API + GPT-4 autograder)
# ============================================================
echo ""
echo "=========================================================="
echo "[1/3] run_strongreject_defender_api  (safety-eval-fork, env=safety-eval)"
echo "=========================================================="
(
    cd "$EVAL_DACE/safety-eval-fork"
    conda activate safety-eval

    export DEFENDER_API_BASE_URL="$DEFENDER_API_BASE_URL"
    export DEFENDER_API_KEY="$DEFENDER_API_KEY"
    export DEFENDER_API_MODEL="$DEFENDER_API_MODEL"

    export OPENAI_API_KEY="$GPT4_OPENAI_API_KEY"
    export OPENAI_BASE_URL="$GPT4_OPENAI_BASE_URL"
    export OPENAI_MODEL="$GPT4_OPENAI_MODEL"

    export HF_HUB_OFFLINE=0

    TASKS="strongreject"
    RESULTS_DIR="$EVAL_DACE/safety-eval-fork/results/dace/$TASKS-$MODEL_NAME-$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$RESULTS_DIR"

    echo "【Defender API】 $DEFENDER_API_BASE_URL  model=$DEFENDER_API_MODEL"
    echo "【GPT-4 Judge】  $OPENAI_BASE_URL  model=$OPENAI_MODEL"
    echo "【Results】      $RESULTS_DIR"

    timeout 7200 python -u evaluation/eval.py generators \
        --model_name_or_path "$MODEL_NAME" \
        --model_input_template_path_or_name "hf" \
        --tasks "$TASKS" \
        --report_output_path "$RESULTS_DIR/metrics.json" \
        --save_individual_results_path "$RESULTS_DIR/all_results.json" \
        --use_defender_api \
        --use_gpt4_autograder \
        --batch_size 1 2>&1 | tee "$RESULTS_DIR/eval.log"

    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        echo "✓ [1/3] strongreject 完成: $RESULTS_DIR"
        if [ -f "$RESULTS_DIR/metrics.json" ] && command -v jq >/dev/null 2>&1; then
            ASR=$(jq -r '.strongreject["ASR (Attack Success Rate)"]' "$RESULTS_DIR/metrics.json" 2>/dev/null)
            RTA=$(jq -r '.strongreject["RTA (Robustness to Attacks)"]' "$RESULTS_DIR/metrics.json" 2>/dev/null)
            echo "  ASR: ${ASR:-N/A}"
            echo "  RTA: ${RTA:-N/A}"
        fi
    else
        echo "✗ [1/3] strongreject 失败, exit=$EXIT_CODE"
    fi
)

# ============================================================
# 2/3  Table 2 · olmes / run_api_eval
#     IFEval (defender API)
# ============================================================
echo ""
echo "=========================================================="
echo "[2/3] run_api_eval  (olmes, env=olmes, IFEval)"
echo "=========================================================="
(
    cd "$EVAL_DACE/olmes"
    conda activate olmes

    export HF_DATASETS_OFFLINE=1
    export HF_HUB_OFFLINE=1
    ### dace: point tiktoken to litellm's pre-bundled cl100k_base cache so offline GPU nodes don't try to fetch it from openaipublic.blob.core.windows.net ###
    export TIKTOKEN_CACHE_DIR=/home/yupeng/.conda/envs/olmes/lib/python3.10/site-packages/litellm/litellm_core_utils/tokenizers

    OUTPUT_DIR="$EVAL_DACE/olmes/results/dace/ifeval/$MODEL_NAME-$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$OUTPUT_DIR"

    echo "【Defender API】 $DEFENDER_API_BASE_URL  model=$DEFENDER_API_MODEL"
    echo "【Results】      $OUTPUT_DIR"

    python "$EVAL_DACE/olmes/api_eval.py" \
        --task ifeval \
        --api-key "$DEFENDER_API_KEY" \
        --base-url "$DEFENDER_API_BASE_URL" \
        --model "$DEFENDER_API_MODEL" \
        --output-dir "$OUTPUT_DIR"

    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        echo "✓ [2/3] ifeval 完成: $OUTPUT_DIR"
    else
        echo "✗ [2/3] ifeval 失败, exit=$EXIT_CODE"
    fi
)

# ============================================================
# 3/3  Table 2 · safety-eval-fork / run_alpaca_eval
#     AlpacaEval2 (defender API + GPT-4o)
# ============================================================
echo ""
echo "=========================================================="
echo "[3/3] run_alpaca_eval  (safety-eval-fork, env=safety-eval)"
echo "=========================================================="
(
    cd "$EVAL_DACE/safety-eval-fork"
    conda activate safety-eval

    export DEFENDER_API_BASE_URL="$DEFENDER_API_BASE_URL"
    export DEFENDER_API_KEY="$DEFENDER_API_KEY"
    export DEFENDER_API_MODEL="$DEFENDER_API_MODEL"

    export OPENAI_API_KEY="$GPT4_OPENAI_API_KEY"
    export OPENAI_BASE_URL="$GPT4_OPENAI_BASE_URL"
    export OPENAI_MODEL="$GPT4_OPENAI_MODEL"

    ### dace: use the self-contained annotator config under eval-dace so we don't depend on hezhida/wenxiaoyu's home paths ###
    export ALPACA_EVAL_ANNOTATORS_CONFIG="${ALPACA_EVAL_ANNOTATORS_CONFIG:-$EVAL_DACE/safety-eval-fork/evaluation/tasks/generation/alpacaeval/weighted_alpaca_eval_gpt4o}"
    export ALPACA_EVAL_EXTRA_RETRIES=3
    export ALPACA_EVAL_RETRY_SLEEP_SECONDS=5
    export ALPACA_EVAL_SKIP_CONTENT_FILTER=1

    ### dace: point hf_hub_download (used by alpaca_eval for df_gamed.csv) at the same shared cache as HF_DATASETS_CACHE ###
    export HF_HUB_CACHE=/data/hf_cache/hub
    ### dace: force HF hub offline so alpaca_eval's length_controlled_winrate reads pre-staged df_gamed.csv from HF_HUB_CACHE instead of timing out on huggingface.co ###
    export HF_HUB_OFFLINE=1

    TASKS="alpacaeval"
    RESULTS_DIR="$EVAL_DACE/safety-eval-fork/results/dace/$TASKS-$MODEL_NAME-$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$RESULTS_DIR"

    echo "【Defender API】 $DEFENDER_API_BASE_URL  model=$DEFENDER_API_MODEL"
    echo "【GPT-4 Judge】  $OPENAI_BASE_URL  model=$OPENAI_MODEL"
    echo "【Annotator】    $ALPACA_EVAL_ANNOTATORS_CONFIG"
    echo "【Results】      $RESULTS_DIR"

    timeout 72000 python -u evaluation/eval.py generators \
        --model_name_or_path "$MODEL_NAME" \
        --model_input_template_path_or_name "hf" \
        --tasks "$TASKS" \
        --report_output_path "$RESULTS_DIR/metrics.json" \
        --save_individual_results_path "$RESULTS_DIR/all_results.json" \
        --use_defender_api \
        --batch_size 1 2>&1 | tee "$RESULTS_DIR/eval.log"

    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        echo "✓ [3/3] alpacaeval 完成: $RESULTS_DIR"
    else
        echo "✗ [3/3] alpacaeval 失败, exit=$EXIT_CODE"
    fi
)

echo ""
echo "=========================================================="
echo "[DONE] 所有 api-based defender 评测完成"
echo "=========================================================="
