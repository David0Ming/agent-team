#!/bin/bash
# 系统健康度评分
# 评估系统整体健康度

SCORE=0

# 检查Gateway
if openclaw status 2>&1 | grep -q "running"; then
    SCORE=$((SCORE + 25))
fi

# 检查Agent
if [ $(find ~/.openclaw -maxdepth 1 -type d -name 'workspace*' 2>/dev/null | wc -l) -ge 10 ]; then
    SCORE=$((SCORE + 25))
fi

# 检查工具
if [ $(ls ~/.openclaw/workspace/tools/*.{sh,py} 2>/dev/null | wc -l) -ge 20 ]; then
    SCORE=$((SCORE + 25))
fi

# 检查知识
if [ $(ls ~/.openclaw/workspace/memory/learning/knowledge/knowledge-*.md 2>/dev/null | wc -l) -ge 30 ]; then
    SCORE=$((SCORE + 25))
fi

echo "🏥 系统健康度: $SCORE/100"
