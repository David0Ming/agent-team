#!/bin/bash
# 成果统计
# 统计今日工作成果

echo "📊 今日成果统计"
echo ""
echo "Agent: 11个"
echo "工具: $(ls ~/.openclaw/workspace/tools/*.{sh,py} 2>/dev/null | wc -l)个"
echo "知识: $(ls ~/.openclaw/workspace/memory/learning/knowledge/knowledge-*.md 2>/dev/null | wc -l)个"
echo "文档: $(find ~/.openclaw/workspace/memory -name "*.md" -type f 2>/dev/null | wc -l)个"
