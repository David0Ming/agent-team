# Agent工具使用指南

**创建时间**: 2026-03-07
**分类**: 工具/技能
**使用场景**: 使用自动化工具提升效率

## 📝 工具清单

### 1. agent-health-check.sh
**用途**: 检查所有agent配置完整性
**使用**: `bash ~/.openclaw/workspace/tools/agent-health-check.sh`
**输出**: 每个agent的SOUL.md、memory/、HEARTBEAT.md状态

### 2. knowledge-maintenance.py
**用途**: 检查超过30天未使用的知识卡片
**使用**: `python3 ~/.openclaw/workspace/tools/knowledge-maintenance.py`
**输出**: 未使用知识卡片列表

### 3. task-router-v2.py
**用途**: 智能推荐合适的agent
**使用**: `python3 ~/.openclaw/workspace/tools/task-router-v2.py "任务描述"`
**输出**: 推荐的agent及匹配度

### 4. agent-deploy.sh
**用途**: 快速创建新agent
**使用**: `bash ~/.openclaw/workspace/tools/agent-deploy.sh <agent-name>`
**输出**: 创建workspace和配置模板

### 5. daily-report.py
**用途**: 生成每日工作报告
**使用**: `python3 ~/.openclaw/workspace/tools/daily-report.py`
**输出**: 今日任务统计和详细内容

### 6. agent-monitor.py
**用途**: 监控agent性能
**使用**: `python3 ~/.openclaw/workspace/tools/agent-monitor.py [agent-name]`
**输出**: 任务数、成功率、平均耗时

### 7. quick-start.sh
**用途**: 快速启动菜单
**使用**: `bash ~/.openclaw/workspace/tools/quick-start.sh`
**输出**: 交互式菜单

### 8. agent-test.py
**用途**: 测试agent配置完整性
**使用**: `python3 ~/.openclaw/workspace/tools/agent-test.py`
**输出**: 每个agent的配置分数

## 🎯 使用场景

### 每日例行
```bash
# 1. 系统状态
openclaw status

# 2. Agent健康检查
bash ~/.openclaw/workspace/tools/agent-health-check.sh

# 3. 知识库维护
python3 ~/.openclaw/workspace/tools/knowledge-maintenance.py
```

### 任务分配
```bash
# 推荐合适的agent
python3 ~/.openclaw/workspace/tools/task-router-v2.py "任务描述"
```

### 新建agent
```bash
# 创建新agent
bash ~/.openclaw/workspace/tools/agent-deploy.sh new-agent
# 编辑SOUL.md完善人设
```

## 💡 最佳实践

1. **每日健康检查**: 确保所有agent配置完整
2. **定期知识维护**: 清理过期知识卡片
3. **智能任务路由**: 使用v2版本获得更准确的推荐
4. **性能监控**: 定期查看agent性能指标

## 🔗 参考资料

- quick-reference.md
- agent-collaboration-best-practices.md
