#!/bin/bash
# 临时文件清理
# 清理临时和草稿文件

echo "🧹 清理临时文件"
echo ""

# 清理草稿文件
find ~/.openclaw/workspace -name "*-draft.md" -type f -delete 2>/dev/null
find ~/.openclaw/workspace -name "*-temp.*" -type f -delete 2>/dev/null
find ~/.openclaw/workspace -name "*.tmp" -type f -delete 2>/dev/null

echo "✅ 清理完成"
