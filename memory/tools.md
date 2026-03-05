# 🛠️ Tools & Environment

## 环境信息

- **主机**: mzg-OMEN-by-HP-Gaming-Laptop-16-k0xxx
- **OS**: Linux 6.17.0-14-generic
- **OpenClaw 版本**: 2026.2.24
- **工作区**: ~/.openclaw/workspace

## 模型配置

### 最佳模型（线路1）
| Agent | 模型 | 用途 |
|-------|------|------|
| DJJ | anthropic/claude-opus-4-6 | 规划决策 |
| DMing | fox/gpt-5.2 | 技术拆解 |
| Dplan/Dcensor/Ddebug/David | fox/gpt-5.1-codex-mini | 执行 |

### 限时额度模型（线路2）
| Provider | 模型 | 所有 Agent 默认使用 |
|----------|------|-------------------|
| Anthropic (imds.ai) | claude-opus-4-6 | 默认 |

### Fallback 链
- DJJ: anthropic/claude-opus-4-6 → fox/gpt-5.2 → kimi-coding/k2p5 → deepseek/deepseek-chat

### 模型别名
| 别名 | 模型 |
|------|------|
| DJJ-GPT | fox/gpt-5.1-codex |
| GPT-5.3 | fox/gpt-5.3-codex |
| Kimi-执行 | kimi-coding/k2p5 |
| GPT-Mini | fox/gpt-5.1-codex-mini |

## 常用命令

```bash
# Gateway 管理
openclaw gateway status
openclaw gateway restart
openclaw logs --follow

# 配置
openclaw config get <path>
openclaw config set <path> <value>
```

## 插件

### memory-lancedb-pro
- **路径**: plugins/memory-lancedb-pro
- **Embedding**: jina-embeddings-v5-text-small
- **API**: https://api.jina.ai/v1

## API 配置

| Provider | 环境变量 | 状态 |
|----------|---------|------|
| Fox | FOX_API_KEY | ✅ 已配置 |
| Kimi | OPENAI_API_KEY | ✅ 已配置 |
| DeepSeek | DEEPSEEK_API_KEY | ✅ 已配置 |
| Anthropic (中转) | ANTHROPIC_API_KEY + ANTHROPIC_BASE_URL | ✅ 已配置 |
