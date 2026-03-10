#!/bin/bash
# 系统状态摘要
# 快速查看关键指标

echo "📊 系统状态摘要"
echo ""
echo "Agent数量: $(find ~/.openclaw -maxdepth 1 -type d -name 'workspace*' 2>/dev/null | wc -l)"
echo "工具数量: $(ls ~/.openclaw/workspace/tools/*.{sh,py} 2>/dev/null | wc -l)"
echo "知识卡片: $(ls ~/.openclaw/workspace/memory/learning/knowledge/knowledge-*.md 2>/dev/null | wc -l)"
