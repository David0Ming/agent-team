# 🤔 Important Decisions

## 决策记录模板

```
日期: YYYY-MM-DD
决策: 
背景: 
选项: 
- 选项A: 
- 选项B: 
选择: 
原因: 
结果: 
```

## 已做出的决策

### 2026-03-05: 任务执行规范
- **问题**: 直接执行任务，不记录待办，不等确认
- **规范**:
  - 执行任务前：先说打算怎么做，等确认后再执行
  - 重要操作加入待办清单
  - 禁止说"记住了"而不行动
- **反馈**: "记住了"是敷衍回答，真正的记住是记录+行动

### 2026-02-28: 禁用内置 memory-lancedb
- **决策**: 禁用 OpenClaw 内置的 memory-lancedb
- **原因**: 使用自定义的 memory-lancedb-pro 插件替代
- **配置**: 在 openclaw.json 中设置 `agents.defaults.memorySearch.enabled: false`

### 2026-02-28: 配置 memory-lancedb-pro 插件
- **决策**: 使用 jina-embeddings-v5-text-small 模型
- **配置**: 
  - API Key: jina_*
  - Model: jina-embeddings-v5-text-small
  - BaseURL: https://api.jina.ai/v1
  - Dimensions: 1024

### 2026-02-28: 拆分 MEMORY.md 为主题文件
- **决策**: 将单一的 MEMORY.md 拆分为多个主题文件
- **结构**: identity.md, user.md, lessons.md, decisions.md, projects.md, tools.md

### 2026-02-28: 配置模型容灾机制
- **决策**: 建立双线模型策略（限时额度 + 最佳模型）
- **线路1（最佳模型）**: 
  - DJJ: anthropic/claude-opus-4-6
  - DMing: fox/gpt-5.2
  - David: fox/gpt-5.1-codex-mini
  - 其他子 Agent: 轻量模型
- **线路2（限时额度）**: anthropic/claude-opus-4-6（通过 imds.ai 中转）
- **切换规则**: 代码任务预估 >300万 token（文件>1200万字符）→ 切最佳模型
- ** Anthropic 配置**: 
  - BASE_URL: https://imds.ai/v1
  - API_KEY: sk-2864...（已配置到 env）
