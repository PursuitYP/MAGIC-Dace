#!/bin/bash
### dace: merge path-based defender evals (qwen_eval + olmes 7bench + general_capability mmlu) ###
# 统一入口：本脚本一次性跑完三组需要本地 checkpoint 的评测
#   1. safety-eval-fork / run_qwen_eval                 (HarmBench / WildGuardTest / DAN / XSTest ...)
#   2. olmes            / run_7_benchmarks_eval         (ARC-C / GPQA)
#   3. safety-eval-fork / run_general_capability_eval   (MMLU)
# 结果保存路径与原六个脚本保持一致，每组仍旧 cd 到原目录、激活原 conda env。


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
# 统一配置 (path-based defender)
# ============================================================
# MODEL_PATH="/mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/yupeng/ckpt/Game-separated/DACE-Diversity-Qwen2.5_7B_Instruct-w_dace_sft_v4-2026-05-03_14-30-23/global_step_300/defender/actor/huggingface"
# MODEL_NAME="DACE-Qwen2.5-7B-v4-attacker1st-step300"
# MODEL_PATH="/mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/yupeng/ckpt/Game-separated/DACE-Diversity-Qwen2.5_7B_Instruct-w_dace_sft_v4-defender1st_2026-05-03_14-47-05/global_step_300/defender/actor/huggingface"
# MODEL_NAME="DACE-Qwen2.5-7B-v4-step300"
MODEL_PATH="/mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/yupeng/ckpt/Game-separated/DACE-Diversity-Llama3.1_8B_Instruct-w_dace_sft_v4-defender1st_2026-05-05_14-10-21/global_step_300/defender/actor/huggingface"
MODEL_NAME="DACE-Llama3.1-8B-v4-defender1st-step300"

REPO_ROOT="/mnt/shared-storage-user/yupeng/MAGIC"
EVAL_DACE="$REPO_ROOT/eval-dace"

# HF 通用
export HF_TOKEN="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"
export HF_DATASETS_CACHE=/data/hf_cache
export HF_DATASETS_VERBOSITY=info

# Conda hook（子 shell 继承函数定义；activate 只在各自 subshell 内生效）
eval "$(conda shell.bash hook)"

echo "=========================================================="
echo "[PATH-DEFENDER]  MODEL_PATH = $MODEL_PATH"
echo "[PATH-DEFENDER]  MODEL_NAME = $MODEL_NAME"
echo "=========================================================="

# ============================================================
# 1/3  Table 1 · safety-eval-fork / run_qwen_eval
#     HarmBench / WildGuardTest / DAN / XSTest / WildJailbreak / OR-Bench
# ============================================================
echo ""
echo "=========================================================="
echo "[1/3] run_qwen_eval  (safety-eval-fork, env=safety-eval)"
echo "=========================================================="
(
    cd "$EVAL_DACE/safety-eval-fork"
    conda activate safety-eval

    export WILDGUARD_API_ENDPOINT='http://s-20251119153749-lp69w-decode.ailab-safethm.svc:23344/v1'
    export WILDGUARD_API_KEY='FAKE_API_KEY'
    export OPENAI_API_KEY="fake-key-for-safety-eval"
    export HF_HUB_OFFLINE=0
    export VLLM_WORKER_MULTIPROC_METHOD=spawn

    TASKS="wildguardtest,harmbench_precompute,wildjailbreak:benign,wildjailbreak:harmful,do_anything_now,harmbench,or_bench:hard-1k,or_bench:toxic,xstest"
    CLASSIFIER="Qwen3GuardAPI"
    RESULTS_DIR="$EVAL_DACE/safety-eval-fork/results/dace/$MODEL_NAME-$CLASSIFIER-$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$RESULTS_DIR"

    CUDA_VISIBLE_DEVICES=0,1 timeout 10800 python -u evaluation/eval.py generators \
        --model_name_or_path "$MODEL_PATH" \
        --model_input_template_path_or_name "game_defender" \
        --tasks "$TASKS" \
        --report_output_path "$RESULTS_DIR/metrics.json" \
        --save_individual_results_path "$RESULTS_DIR/all_results.json" \
        --use_vllm \
        --classifier_model_name "$CLASSIFIER" \
        --no_extract_answer false \
        --batch_size 1 2>&1 | tee "$RESULTS_DIR/eval.log"

    echo "✓ [1/3] safety 评测完成: $RESULTS_DIR"
)

# ============================================================
# 2/3  Table 2 · olmes / run_7_benchmarks_eval
#     ARC-C / GPQA
# ============================================================
echo ""
echo "=========================================================="
echo "[2/3] run_7_benchmarks_eval  (olmes, env=olmes)"
echo "=========================================================="
(
    cd "$EVAL_DACE/olmes"
    conda activate olmes

    export HF_DATASETS_OFFLINE=1
    export HF_HUB_OFFLINE=1
    ### dace: point tiktoken to litellm's pre-bundled cl100k_base cache so offline GPU nodes don't try to fetch it from openaipublic.blob.core.windows.net ###
    export TIKTOKEN_CACHE_DIR=/home/yupeng/.conda/envs/olmes/lib/python3.10/site-packages/litellm/litellm_core_utils/tokenizers

    RESULTS_BASE_DIR="$EVAL_DACE/olmes/results/dace/$MODEL_NAME-$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$RESULTS_BASE_DIR"

    TASKS=(
        "arc_challenge"
        "gpqa"
    )

    for TASK in "${TASKS[@]}"; do
        echo ""
        echo "-----------------------------------------------------------------------"
        echo "开始评测: $TASK"
        echo "-----------------------------------------------------------------------"
        TASK_RESULTS_DIR="$RESULTS_BASE_DIR/$TASK"
        mkdir -p "$TASK_RESULTS_DIR"

        case $TASK in
            ("arc_challenge")
                TASK_ARGS="--task arc_challenge --model-type hf --batch-size 16"
                ;;
            ("gpqa")
                TASK_ARGS="--task gpqa --model-type hf --batch-size 4"
                ;;
            (*)
                echo "未知任务: $TASK"
                continue
                ;;
        esac

        timeout 7200 python -m oe_eval.run_eval \
            --model-path "$MODEL_PATH" \
            $TASK_ARGS \
            --output-dir "$TASK_RESULTS_DIR" \
            2>&1 | tee "$TASK_RESULTS_DIR/eval.log"

        if [ ${PIPESTATUS[0]} -eq 0 ] && [ -f "$TASK_RESULTS_DIR/metrics.json" ]; then
            echo "✓ $TASK 评测完成: $TASK_RESULTS_DIR/metrics.json"
        else
            echo "❌ $TASK 评测失败"
        fi
    done

    echo "✓ [2/3] olmes 7benchmarks 完成: $RESULTS_BASE_DIR"
)

# ============================================================
# 3/3  Table 2 · safety-eval-fork / run_general_capability_eval
#     MMLU
# ============================================================
echo ""
echo "=========================================================="
echo "[3/3] run_general_capability_eval  (safety-eval-fork, env=safety-eval, MMLU)"
echo "=========================================================="
(
    cd "$EVAL_DACE/safety-eval-fork"
    conda activate safety-eval

    export HF_HUB_OFFLINE=0
    # MTBench judge（只有 TASKS 含 mtbench 才会用到，这里保留以免今后扩展）
    export OPENAI_API_KEY="sk-D0wGaXJBOV1f6VTnJzwRuhLewJ0Crn1KNQeSXnRRn2dM6ITR"
    export OPENAI_BASE_URL="https://api.boyuerichdata.opensphereai.com/v1"
    export OPENAI_MODEL="gpt-4o"
    export MTBENCH_JUDGE_MODEL="gpt-4o"
    export MTBENCH_REF_MODEL="gpt-4o"
    export MTBENCH_JUDGE_WORKERS=16

    TASKS="mmlu"
    RESULTS_DIR="$EVAL_DACE/safety-eval-fork/results/dace/$TASKS-$MODEL_NAME-$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$RESULTS_DIR"

    CUDA_VISIBLE_DEVICES=0,1 python -u evaluation/eval.py generators \
        --model_name_or_path "$MODEL_PATH" \
        --model_input_template_path_or_name "hf" \
        --tasks "$TASKS" \
        --report_output_path "$RESULTS_DIR/metrics.json" \
        --save_individual_results_path "$RESULTS_DIR/all_results.json" \
        --batch_size 1 2>&1 | tee "$RESULTS_DIR/eval.log"

    echo "✓ [3/3] general capability (MMLU) 完成: $RESULTS_DIR"
)

echo ""
echo "=========================================================="
echo "[DONE] 所有 path-based defender 评测完成"
echo "=========================================================="
