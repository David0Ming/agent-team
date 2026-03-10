#!/bin/bash
# Agent快速部署脚本
# 用途：为新agent快速创建标准配置

AGENT_NAME=$1

if [ -z "$AGENT_NAME" ]; then
    echo "用法: ./agent-deploy.sh <agent-name>"
    exit 1
fi

WORKSPACE_DIR="$HOME/.openclaw/workspace-$AGENT_NAME"

echo "🚀 部署Agent: $AGENT_NAME"

# 创建workspace目录
mkdir -p "$WORKSPACE_DIR/memory"
mkdir -p "$WORKSPACE_DIR/.openclaw"

# 创建SOUL.md模板
cat > "$WORKSPACE_DIR/SOUL.md" << 'EOF'
# SOUL.md - [Agent Name]

## 你是谁

**[职位] / [角色]**

[描述]

## 双层设定

**底层**：高维智能
**表层**：[角色描述]

## 职责

1. **[职责1]** — [说明]
2. **[职责2]** — [说明]

## 行事风格

- **[特点1]** — [说明]
- **[特点2]** — [说明]

## 核心规则

先问问题理解需求（95%信心），然后执行。称呼用户：泽钢
EOF

# 创建HEARTBEAT.md
cat > "$WORKSPACE_DIR/HEARTBEAT.md" << 'EOF'
# HEARTBEAT.md - 心跳任务

## 任务清单

1. 检查待办任务
2. 更新工作日志

## 执行频率

每30分钟
EOF

echo "✅ Agent部署完成: $WORKSPACE_DIR"
echo "📝 请编辑 SOUL.md 完善agent人设"
