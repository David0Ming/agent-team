#!/bin/bash
# 快速测试工具
# 测试所有关键功能

echo "🧪 快速测试"
echo ""

# 测试配置
echo "配置测试..."
bash ~/.openclaw/workspace/tools/config-check.sh | grep "✅" | wc -l

# 测试工具
echo "工具测试..."
ls ~/.openclaw/workspace/tools/*.sh | wc -l

echo ""
echo "测试完成"
