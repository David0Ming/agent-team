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
| Notion | NOTION_API_KEY / ~/.config/notion/api_key | ✅ 已配置 |

## Notion 记录系统（2026-03-19建立）

### 自动写入触发口令（按意图识别，不死扣字面）

#### 题库写入触发
以下表达都默认触发“按算法题模板写入 Notion 题库”：
- 记到题库
- 把这题记到 Notion
- 记录今天这道题
- 这题加入题库
- 这题标记待复习
- 帮我记一下这道题

#### 面试复盘触发
以下表达都默认触发“按面试模板写入 Notion 面试复盘库”：
- 复盘这场面试
- 复盘这次面试
- 记录这场面试
- 把这次面试记到 Notion
- 记一下面试复盘
- 帮我复盘今天的面试

#### 默认行为
- 不要求用户必须说固定口令
- 只要语义明确表达“记录/复盘/加入题库”，就按对应模板执行
- 这是**专属流程**，优先级高于通用问答/通用提问流程
- 信息足够 → 直接写入
- 信息不足 → 只追问最关键的 1-3 项
- 默认遵循：`personal/career/Notion记录模板与规则.md`

### 1. 算法题库（已完善）
- **名称**: 算法题库
- **database_id**: `327a832b-f7a4-8198-8f31-f6c52b056092`
- **data_source_id**: `327a832b-f7a4-815b-bc59-000b3b3151b8`
- **url**: https://www.notion.so/327a832bf7a481988f31f6c52b056092

**字段设计**：
- 基础：题目、难度、类型、状态、日期
- 关键复盘：我的错误、正确思路、学到什么、关键方法
- 记忆强化：复习次数、下次复习、是否掌握
- 追溯：来源

**记录原则**：
- 只记题目 = 无效记录
- 每道题至少补3项：`我的错误` + `正确思路` + `学到什么`
- 做完题后优先记录“为什么错”，不是只记答案
- `关键方法`里写可复用套路（如双指针/递归/单调栈）
- 默认模板规范见：`personal/career/Notion记录模板与规则.md`

### 2. 面试复盘库（新建）
- **名称**: 面试复盘库
- **database_id**: `1fd29bd0-582c-4997-9506-398e9f195b87`
- **data_source_id**: `b125ace1-3168-43f3-8371-791ad300dec3`
- **url**: https://www.notion.so/1fd29bd0582c49979506398e9f195b87

**字段设计**：
- 基础：标题、公司、岗位、日期、轮次、结果、方向标签
- 面试内容：面试问题、我的回答
- 复盘核心：做得好、待改进、改进行动
- 跟进：表现评分、下次跟进

**记录原则**：
- 每场面试至少记录：`面试问题` + `我的回答` + `待改进` + `改进行动`
- `待改进`写具体失误，不写空话
- `改进行动`必须可执行（如“补一段3分钟自我介绍”）
- 面试当天完成复盘，不拖到第二天
- 默认模板规范见：`personal/career/Notion记录模板与规则.md`

## 工具路由补充规则（第三轮最小增强）

### 专属流程型工具路由
以下场景默认视为工具路由问题，而不是普通聊天问题：

- **更新 OpenClaw / 升级 OpenClaw / update openclaw**
  - 默认路由到：`self-updater`
  - 优先级：高于通用建议流程

- **明确命中某个已安装 skill 描述的任务**
  - 默认动作：先读取对应 `SKILL.md`
  - 原则：已有成熟 skill 时，优先按 skill 流程处理，而不是临时 improvisation

- **天气 / voice-call / notion / healthcheck / feishu 等明确工具场景**
  - 默认动作：优先走对应 skill 或专用流程
  - 原则：工具型任务优先路由，不先展开长篇通用分析

### 工具路由原则
- 工具和外部系统规则服务于DJJ主链
- 命中专属工具场景时，优先走工具路由，不退回通用问答
- 路由时不仅看能力，也看任务成本：低成本任务可直接处理；高成本任务优先走严格流程

## GitHub 配置

- **账号**: David0Ming
- **邮箱**: david0ming@github.com
- **Token**: 已保存在 ~/.git-credentials（不提交到仓库）
- **仓库**: https://github.com/David0Ming/agent-team
