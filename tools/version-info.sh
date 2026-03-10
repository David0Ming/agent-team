#!/bin/bash
# 版本信息
# 显示系统版本信息

echo "📌 版本信息"
echo ""
echo "OpenClaw: $(openclaw --version 2>&1 | head -1)"
echo "Python: $(python3 --version)"
echo "Node: $(node --version)"
echo "系统: $(uname -s) $(uname -r)"
