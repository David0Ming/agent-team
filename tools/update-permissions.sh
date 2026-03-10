#!/bin/bash
# 一键更新工具
# 更新所有工具的执行权限

echo "🔧 更新工具权限"
chmod +x ~/.openclaw/workspace/tools/*.sh
chmod +x ~/.openclaw/workspace/tools/*.py
echo "✅ 完成"
