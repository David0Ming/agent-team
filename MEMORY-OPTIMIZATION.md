# OpenClaw 记忆架构优化配置

## 优化内容

### 1. 文件优先原则
- 文件是唯一真相来源（Single Source of Truth）
- 口头"记住了"无效，必须说明写入哪个文件
- 会话记忆会消失，文件记忆永久存在

### 2. 检索优先协议
- 回答问题前 → memory_search相关主题
- 执行任务前 → 检查memory/projects.md和相关知识
- 做决策前 → 搜索过往decisions
- 不确定时 → 搜索而不是猜测

### 3. 预压缩刷新配置
```json
{
  "compaction": {
    "mode": "safeguard",
    "reserveTokensFloor": 40000,
    "memoryFlush": {
      "enabled": true,
      "softThresholdTokens": 4000
    }
  }
}
```

### 4. 知识进化路径
1. 日常经验 → memory/daily/*.md
2. 提炼规则 → memory/lessons-*.md
3. 通用知识 → memory/learning/knowledge/*.md
4. 可复用能力 → skills/

### 5. 定期归档规则
- 每周日归档>7天的日志
- 删除6个月未使用的知识卡片
- 压缩MEMORY.md保持<100行

## 配置文件

- `AGENTS.md` - Agent工作规则
- `HEARTBEAT.md` - 心跳任务
- `openclaw.json.template` - 配置模板（需替换API keys）

## 参考资料

- [coolmanns 12层架构](https://github.com/coolmanns/openclaw-memory-architecture)
- [VelvetShark 记忆指南](https://velvetshark.com/openclaw-memory-masterclass)
- EvoMap GEP协议
