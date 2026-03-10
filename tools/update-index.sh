#!/bin/bash
# 工具索引更新
# 自动更新工具列表

echo "📝 更新工具索引"
echo ""
echo "工具总数: $(ls ~/.openclaw/workspace/tools/*.{sh,py} 2>/dev/null | wc -l)"
echo ""
echo "更新完成"
