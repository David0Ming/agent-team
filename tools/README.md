# Agent自动化工具集

> 提升agent团队效率的工具集合

## 🚀 快速开始

```bash
# 快速启动菜单（推荐）
bash ~/.openclaw/workspace/tools/quick-start.sh
```

## 📦 工具列表

### 健康检查与监控

**agent-health-check.sh** - Agent配置完整性检查
```bash
bash ~/.openclaw/workspace/tools/agent-health-check.sh
```

**agent-test.py** - Agent能力测试（评分系统）
```bash
python3 ~/.openclaw/workspace/tools/agent-test.py
```

**agent-monitor.py** - 性能监控
```bash
# 查看所有agent
python3 ~/.openclaw/workspace/tools/agent-monitor.py

# 查看特定agent
python3 ~/.openclaw/workspace/tools/agent-monitor.py dming
```

### 任务管理

**task-router-v2.py** - 智能任务路由
```bash
python3 ~/.openclaw/workspace/tools/task-router-v2.py "任务描述"
```

**daily-report.py** - 每日工作报告
```bash
python3 ~/.openclaw/workspace/tools/daily-report.py
```

### 知识管理

**knowledge-maintenance.py** - 知识库维护
```bash
python3 ~/.openclaw/workspace/tools/knowledge-maintenance.py
```

**knowledge-learner.py** - 知识学习自动化
```bash
python3 ~/.openclaw/workspace/tools/knowledge-learner.py
```

### Agent管理

**agent-deploy.sh** - 快速部署新agent
```bash
bash ~/.openclaw/workspace/tools/agent-deploy.sh <agent-name>
```

## 📊 使用场景

### 每日例行检查
```bash
# 1. 快速启动菜单
bash ~/.openclaw/workspace/tools/quick-start.sh

# 或手动执行
openclaw status
bash ~/.openclaw/workspace/tools/agent-health-check.sh
python3 ~/.openclaw/workspace/tools/knowledge-maintenance.py
```

### 任务分配
```bash
# 智能推荐agent
python3 ~/.openclaw/workspace/tools/task-router-v2.py "优化数据库性能"
```

### 新建agent
```bash
# 创建新agent
bash ~/.openclaw/workspace/tools/agent-deploy.sh new-agent

# 编辑配置
nano ~/.openclaw/workspace-new-agent/SOUL.md
```

## 🎯 工具特点

- ✅ 全自动化：无需手动检查
- ✅ 智能推荐：准确匹配agent能力
- ✅ 性能监控：实时追踪效率
- ✅ 快速部署：标准化配置

## 📝 维护说明

所有工具位于：`~/.openclaw/workspace/tools/`

更新工具后记得：
1. 更新此README
2. 更新knowledge-agent-tools.md
3. 测试工具功能
