#!/bin/bash
# 快速诊断工具
# 一键检查系统状态

echo "🔍 系统诊断"
echo ""

# 检查Gateway
echo "Gateway状态:"
openclaw status 2>&1 | grep "Gateway service" | head -1

# 检查Agent
echo ""
echo "Agent数量: $(find ~/.openclaw -maxdepth 1 -type d -name 'workspace*' 2>/dev/null | wc -l)"

# 检查工具
echo "工具数量: $(ls ~/.openclaw/workspace/tools/*.{sh,py} 2>/dev/null | wc -l)"

# 检查知识
echo "知识卡片: $(ls ~/.openclaw/workspace/memory/learning/knowledge/knowledge-*.md 2>/dev/null | wc -l)"
