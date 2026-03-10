#!/bin/bash
# 工作流程检查
# 检查关键工作流程是否正常

echo "🔄 工作流程检查"
echo ""

# 检查配置
if [ -f ~/.openclaw/workspace/SOUL.md ]; then
    echo "✅ 配置文件正常"
else
    echo "❌ 配置文件缺失"
fi

# 检查工具
TOOL_COUNT=$(ls ~/.openclaw/workspace/tools/*.{sh,py} 2>/dev/null | wc -l)
if [ $TOOL_COUNT -gt 0 ]; then
    echo "✅ 工具集正常 ($TOOL_COUNT 个)"
else
    echo "❌ 工具集缺失"
fi

echo ""
echo "检查完成"
