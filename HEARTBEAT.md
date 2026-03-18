# HEARTBEAT.md - 心跳任务清单

## 核心任务（每次心跳执行）

### 1. 系统监控
- 执行 `openclaw status` 检查 Gateway 状态
- 执行 `openclaw logs 2>&1 | tail -20` 检查错误日志
- 记录到 `memory/heartbeat-status.json`
- 发现严重错误时主动报告

### 2. 持续学习（轻量）
**目标**：发现1个先进知识并记录

**信息来源**（轮换）：
- Skills.sh: `npx skills find [topic]`
- GitHub Trending: `curl https://github.com/trending`
- Hacker News: 技术新闻
- 其他专业网站

**记录格式**：
- 是什么：简单描述
- 为什么有价值：1-2句话
- 存到：`memory/learning-log.md`

### 3. 待办任务
- 读取 `memory/projects.md`
- **展示所有 `[ ]` 未完成的任务列表**
- 尝试完成其中一个简单任务
- 复杂任务需要向泽钢确认

**展示格式**：
```
📋 当前待办任务：
- [ ] 任务1
- [ ] 任务2
- [ ] 任务3
```

### 4. 更新记录
**追加到 `memory/daily/YYYY-MM-DD.md`**：
- 时间：HH:MM 心跳
- 系统状态：Gateway状态、错误（仅在有异常时记录）
- 学习成果：发现的先进知识（简要）
- 待办检查：列出未完成任务
- 完成工作：简要列表

**重要学习成果**：
- 写入主题文件（`memory/decisions.md`, `memory/lessons.md`等）

## 定时任务

### 文件归档（每周日）
检查当前是否周日，如果是：
- 归档>7天的日志到memory/archive/
  ```bash
  find memory/daily/ -name "*.md" -mtime +7 -exec sh -c 'mkdir -p memory/archive/$(date -r {} +%Y-%m) && mv {} memory/archive/$(date -r {} +%Y-%m)/' \;
  ```
- 评估知识卡片：删除6个月未使用的
  - 检查memory/learning/knowledge/中的文件
  - 查看最后修改时间：`find memory/learning/knowledge/ -name "*.md" -mtime +180`
  - 确认后删除无价值的卡片
- 压缩MEMORY.md：保持<100行
  - 检查行数：`wc -l memory/MEMORY.md`
  - 如果>100行，提炼精简或归档到knowledge/

## 执行频率
- 所有Agent: 每1小时心跳一次

## 状态文件格式
```json
{
  "lastCheck": "2026-03-08T08:00:00+08:00",
  "gateway": {
    "running": true,
    "agents": 11,
    "sessions": 50
  },
  "errors": []
}
```

## 完成标志
如果无需关注的事项，回复：`HEARTBEAT_OK`
