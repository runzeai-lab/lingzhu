#!/bin/bash
# Ollama启动脚本（包含优化环境变量）
# 任务T2：提升Ollama本地推理速度

echo "🚀 正在启动Ollama服务（优化版）..."

# 优化1：并发优化（根据CPU核心数设置）
export OLLAMA_NUM_PARALLEL=2  # 4核CPU → 并发数2（推荐：CPU核心数的一半）
echo "✅ 并发数已设置：OLLAMA_NUM_PARALLEL=$OLLAMA_NUM_PARALLEL"

# 优化2：GPU加速（如果有GPU，取消注释下面一行）
# export OLLAMA_GPU=1  # 需要Windows安装NVIDIA驱动，WSL内用nvidia-smi验证
# 检查GPU是否可用
if nvidia-smi > /dev/null 2>&1; then
    export OLLAMA_GPU=1
    echo "✅ GPU加速已启用：OLLAMA_GPU=$OLLAMA_GPU"
else
    echo "⚠️ GPU未检测到，使用CPU模式"
fi

# 优化3：模型优化（已使用最小模型qwen:0.5b，无需更换）

# 停止可能运行的Ollama服务
pkill -f "ollama serve" > /dev/null 2>&1
sleep 2

# 启动Ollama服务（后台运行）
nohup ollama serve > /tmp/ollama.log 2>&1 &
sleep 5

# 验证启动是否成功
if ps aux | grep -v grep | grep -q "ollama serve"; then
    echo "✅ Ollama服务启动成功！"
    echo "   并发数：$(nproc --all 2>/dev/null || echo $OLLAMA_NUM_PARALLEL)"
    echo "   GPU加速：$([ "$OLLAMA_GPU" = "1" ] && echo '已启用' || echo '未启用')"
    echo "   日志文件：/tmp/ollama.log"
else
    echo "❌ Ollama服务启动失败，请查看日志：/tmp/ollama.log"
    exit 1
fi

# 测试模型是否可用
echo ""
echo "🧪 测试模型 qwen:0.5b 是否可用..."
if ollama list 2>&1 | grep -q "qwen:0.5b"; then
    echo "✅ 模型 qwen:0.5b 已可用"
else
    echo "⚠️ 模型 qwen:0.5b 未找到，正在拉取..."
    ollama pull qwen:0.5b
fi

echo ""
echo "🎉 Ollama启动脚本执行完成！"
