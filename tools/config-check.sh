#!/bin/bash
# 配置完整性检查
# 快速验证关键配置文件

echo "🔍 配置完整性检查"
echo ""

# 检查SOUL.md
if [ -f ~/.openclaw/workspace/SOUL.md ]; then
    echo "✅ SOUL.md 存在"
else
    echo "❌ SOUL.md 缺失"
fi

# 检查HEARTBEAT.md
if [ -f ~/.openclaw/workspace/HEARTBEAT.md ]; then
    echo "✅ HEARTBEAT.md 存在"
else
    echo "❌ HEARTBEAT.md 缺失"
fi

# 检查memory目录
if [ -d ~/.openclaw/workspace/memory ]; then
    echo "✅ memory/ 存在"
else
    echo "❌ memory/ 缺失"
fi

echo ""
echo "检查完成"
