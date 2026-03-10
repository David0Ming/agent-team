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

**注意**：心跳中只做轻量发现，深度学习（5步法）在专门学习时进行

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
- 完成工作：简要列表（允许与详细记录重复）

**重要学习成果**：
- 写入主题文件（`memory/decisions.md`, `memory/lessons.md`等）

**注意**：心跳记录允许重复，会话结束时会整合去重

## 定时任务

### 文件归档（每周日）
检查当前是否周日，如果是：
- 归档 >7天的日志到 memory/archive/
  ```bash
  find memory/daily/ -name "*.md" -mtime +7 -exec sh -c 'mkdir -p memory/archive/$(date -r {} +%Y-%m) && mv {} memory/archive/$(date -r {} +%Y-%m)/' \;
  ```

### 嘟嘟巴士先锋引擎（每日 09:00）
检查当前时间是否 09:00-09:05 (Asia/Shanghai)，如果是且今日未执行：
```bash
python3 ~/.openclaw/workspace/projects/dudubashi-pioneer/scripts/run_daily.py
```

### 海野山房酒店视频（每日 13:40）
检查当前时间是否 13:40-13:45 (Asia/Shanghai)，如果是且今日未执行：
```bash
python3 ~/.openclaw/workspace/projects/haiye-hotel/scripts/run_daily.py
```

### 竞品数据抓取（每日 09:10）
检查当前时间是否 09:10-09:15 (Asia/Shanghai)，如果是且今日未执行：
```bash
cd ~/.openclaw/workspace/projects/dudubashi-pioneer && \
python3 scripts/fetch_newrank_auto.py && \
python3 scripts/generate_competitor_report.py && \
python3 scripts/visualize_competitors.py
```

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
