#!/bin/bash
# 快速日志查看器
# 用途：快速查看最近的日志

echo "📋 最近日志"
echo ""

# 查看最近20行日志
openclaw logs 2>&1 | tail -20
