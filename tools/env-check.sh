#!/bin/bash
# 环境检查
# 检查必要的命令和工具

echo "🔧 环境检查"
echo ""

# 检查Python
if command -v python3 &> /dev/null; then
    echo "✅ Python3: $(python3 --version)"
else
    echo "❌ Python3 未安装"
fi

# 检查Node
if command -v node &> /dev/null; then
    echo "✅ Node: $(node --version)"
else
    echo "❌ Node 未安装"
fi

# 检查OpenClaw
if command -v openclaw &> /dev/null; then
    echo "✅ OpenClaw 已安装"
else
    echo "❌ OpenClaw 未安装"
fi
