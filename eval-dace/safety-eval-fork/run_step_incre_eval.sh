#!/bin/bash

# 流水线式评测脚本 - 测试多个checkpoint的defender模型
# 用途：对同一个训练run的不同step进行HarmBench评测

# ========================================
# 配置区域
# ========================================

# 基础路径
BASE_PATH="/mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/wenxiaoyu/game/checkpoints/Game-separated/v4-D-q257bi-A-sftv4-ratio11-freq5-reward1_0.5_0-woDformat-wo_label_reward-revised_label-2026-01-14_11-15-25"
#/mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/game/checkpoints/Game-separated/v2-D-q7bi-A-q7biv3-zerosum-format1-balanced-8192-2025-12-12_19-44-33/global_step_135/defender/actor/huggingface
MODEL_NAME="v4-1.14-freq5"

# 要测试的checkpoint steps
STEPS=(15 30 45)

# 固定任务
TASK="harmbench"

# 分类器配置
CLASSIFIER="Qwen3GuardAPI"

# 结果保存根目录
RESULTS_BASE_DIR="./results/eval-1.14//step_incremental-qwen3guard/$MODEL_NAME-$(date +%Y%m%d_%H%M%S)"
mkdir -p $RESULTS_BASE_DIR

# ========================================
# 环境变量配置
# ========================================
export WILDGUARD_API_ENDPOINT='http://s-20251119153749-lp69w-decode.ailab-safethm.svc:23344/v1'
export WILDGUARD_API_KEY='FAKE_API_KEY'
export HF_DATASETS_CACHE=/data/hf_cache
export OPENAI_API_KEY="fake-key-for-safety-eval"
export HF_TOKEN="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"
export HF_HUB_OFFLINE=0
export HF_DATASETS_VERBOSITY=info

# ========================================
# 激活环境
# ========================================
eval "$(conda shell.bash hook)"
conda activate safety-eval

# ========================================
# 创建汇总文件
# ========================================
SUMMARY_FILE="$RESULTS_BASE_DIR/evaluation_summary.txt"
echo "=====================================" > $SUMMARY_FILE
echo "Multi-Checkpoint Evaluation Summary" >> $SUMMARY_FILE
echo "=====================================" >> $SUMMARY_FILE
echo "Model: $MODEL_NAME" >> $SUMMARY_FILE
echo "Task: $TASK" >> $SUMMARY_FILE
echo "Start Time: $(date)" >> $SUMMARY_FILE
echo "=====================================" >> $SUMMARY_FILE
echo "" >> $SUMMARY_FILE

# ========================================
# 流水线评测主循环
# ========================================
total_steps=${#STEPS[@]}
current_step=0

for STEP in "${STEPS[@]}"; do
    current_step=$((current_step + 1))
    
    echo ""
    echo "======================================================================="
    echo "[$current_step/$total_steps] Evaluating checkpoint: global_step_$STEP"
    echo "======================================================================="
    
    # 构建模型路径
    MODEL_PATH="$BASE_PATH/global_step_$STEP/defender/actor/huggingface"
    
    # 检查路径是否存在
    if [ ! -d "$MODEL_PATH" ]; then
        echo "❌ ERROR: Model path does not exist: $MODEL_PATH"
        echo "Step $STEP - FAILED: Model path not found" >> $SUMMARY_FILE
        continue
    fi
    
    # 检查关键文件
    if [ ! -f "$MODEL_PATH/config.json" ]; then
        echo "❌ ERROR: config.json not found in $MODEL_PATH"
        echo "Step $STEP - FAILED: config.json missing" >> $SUMMARY_FILE
        continue
    fi
    
    echo "✓ Model path verified: $MODEL_PATH"
    
    # 为当前step创建结果目录
    STEP_RESULTS_DIR="$RESULTS_BASE_DIR/step_$STEP"
    mkdir -p $STEP_RESULTS_DIR
    
    # 记录开始时间
    step_start_time=$(date +%s)
    
    echo "Running evaluation..."
    echo "  - Model: $MODEL_PATH"
    echo "  - Task: $TASK"
    echo "  - Results: $STEP_RESULTS_DIR"
    
    # 运行评测
    timeout 7200 python -u evaluation/eval.py generators \
        --model_name_or_path "$MODEL_PATH" \
        --model_input_template_path_or_name "hf" \
        --tasks "$TASK" \
        --report_output_path "$STEP_RESULTS_DIR/metrics.json" \
        --save_individual_results_path "$STEP_RESULTS_DIR/all_results.json" \
        --use_vllm \
        --classifier_model_name "$CLASSIFIER" \
        --no_extract_answer \
        --batch_size 1 2>&1 | tee "$STEP_RESULTS_DIR/eval.log"
    
    # 检查执行结果
    exit_code=${PIPESTATUS[0]}
    step_end_time=$(date +%s)
    step_duration=$((step_end_time - step_start_time))
    
    if [ $exit_code -eq 0 ]; then
        echo "✓ Evaluation completed successfully for step $STEP"
        echo "  Duration: ${step_duration}s"
        
        # 提取关键指标（如果metrics.json存在）
        if [ -f "$STEP_RESULTS_DIR/metrics.json" ]; then
            echo "" >> $SUMMARY_FILE
            echo "Step $STEP - SUCCESS (Duration: ${step_duration}s)" >> $SUMMARY_FILE
            echo "  Metrics file: $STEP_RESULTS_DIR/metrics.json" >> $SUMMARY_FILE
            
            # 尝试提取ASR等关键指标
            if command -v jq &> /dev/null; then
                echo "  Key metrics:" >> $SUMMARY_FILE
                jq -r 'to_entries[] | "    \(.key): \(.value)"' "$STEP_RESULTS_DIR/metrics.json" >> $SUMMARY_FILE 2>/dev/null || echo "    (Could not parse metrics)" >> $SUMMARY_FILE
            fi
        else
            echo "⚠ Warning: metrics.json not found" >> $SUMMARY_FILE
        fi
    else
        echo "❌ ERROR: Evaluation failed for step $STEP (exit code: $exit_code)"
        echo "Step $STEP - FAILED (exit code: $exit_code)" >> $SUMMARY_FILE
    fi
    
    echo ""
    echo "-----------------------------------------------------------------------"
done

# ========================================
# 完成汇总
# ========================================
echo "" >> $SUMMARY_FILE
echo "=====================================" >> $SUMMARY_FILE
echo "End Time: $(date)" >> $SUMMARY_FILE
echo "=====================================" >> $SUMMARY_FILE

echo ""
echo "======================================================================="
echo "All evaluations completed!"
echo "======================================================================="
echo ""
echo "Results directory: $RESULTS_BASE_DIR"
echo ""
echo "Summary:"
cat $SUMMARY_FILE
echo ""
echo "Individual results:"
for STEP in "${STEPS[@]}"; do
    STEP_DIR="$RESULTS_BASE_DIR/step_$STEP"
    if [ -f "$STEP_DIR/metrics.json" ]; then
        echo "  ✓ Step $STEP: $STEP_DIR/metrics.json"
    else
        echo "  ✗ Step $STEP: No results"
    fi
done
echo ""
echo "To view detailed results for a specific step:"
echo "  cat $RESULTS_BASE_DIR/step_<STEP>/metrics.json"
echo "  cat $RESULTS_BASE_DIR/step_<STEP>/all_results.json"
echo ""
