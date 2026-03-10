#!/bin/bash
# Token使用监控脚本

# 获取当前token使用情况（需要从session_status解析）
# 这里是示例，实际需要调用session_status工具

THRESHOLD=80

echo "🔍 检查Token使用率..."

# 示例输出格式
# 实际使用时需要调用session_status并解析结果
CURRENT_USAGE=47  # 当前使用率（示例）
CURRENT_TOKENS="94k/200k"

if [ $CURRENT_USAGE -gt $THRESHOLD ]; then
    echo "⚠️  警告：Token使用率 ${CURRENT_USAGE}% (${CURRENT_TOKENS})"
    echo "建议：重启会话以获得最佳性能"
else
    echo "✅ Token使用正常：${CURRENT_USAGE}% (${CURRENT_TOKENS})"
fi

# 记录到日志
echo "$(date '+%Y-%m-%d %H:%M:%S') - Token使用率: ${CURRENT_USAGE}%" >> ~/.openclaw/workspace/memory/token-usage.log
