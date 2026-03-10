#!/bin/bash
# Agent健康检查脚本
# 用途：检查所有agent的配置完整性和运行状态

echo "🔍 Agent健康检查开始..."
echo ""

# 检查所有workspace
WORKSPACES=$(find ~/.openclaw -maxdepth 1 -type d -name "workspace*" 2>/dev/null)

for ws in $WORKSPACES; do
    agent_name=$(basename "$ws" | sed 's/workspace-//' | sed 's/workspace/main/')
    echo "📦 检查 $agent_name"
    
    # 检查SOUL.md
    if [ -f "$ws/SOUL.md" ]; then
        echo "  ✅ SOUL.md 存在"
    else
        echo "  ❌ SOUL.md 缺失"
    fi
    
    # 检查memory目录
    if [ -d "$ws/memory" ]; then
        echo "  ✅ memory/ 存在"
    else
        echo "  ⚠️  memory/ 缺失"
    fi
    
    # 检查HEARTBEAT.md
    if [ -f "$ws/HEARTBEAT.md" ]; then
        echo "  ✅ HEARTBEAT.md 存在"
    else
        echo "  ⚠️  HEARTBEAT.md 缺失"
    fi
    
    echo ""
done

echo "✅ 健康检查完成"
