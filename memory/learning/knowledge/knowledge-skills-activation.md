# OpenClaw技能激活指南

**创建时间**: 2026-03-07
**分类**: 工具/技能
**使用场景**: 激活missing skills，扩展agent能力

## 📝 技能分类

### 高优先级（建议激活）

**通信类**:
- `discord` - Discord聊天、反应、频道管理
- `slack` - Slack消息、频道、集成
- `wacli` - WhatsApp消息

**开发类**:
- `github` - GitHub操作（PR、Issue、CI）
- `gh-issues` - GitHub Issue自动化

**知识类**:
- `notion` - Notion笔记、数据库
- `obsidian` - Obsidian笔记

**效率类**:
- `things-mac` - 任务管理
- `session-logs` - 会话日志分析

### 中优先级

**媒体类**:
- `spotify-player` - Spotify控制
- `video-frames` - 视频帧提取

**办公类**:
- `gog` - Google Workspace
- `himalaya` - 邮件管理

## 🎯 激活方法

### 方法1: 安装新技能
```bash
npx clawhub install <skill-name>
```

### 方法2: 查看技能详情
```bash
npx clawhub inspect <skill-name>
```

### 方法3: 搜索技能
```bash
npx clawhub search <keyword>
```

## 📦 常用技能

| 技能 | 用途 | 优先级 |
|------|------|--------|
| discord | Discord运营 | 高 |
| github | 代码协作 | 高 |
| notion | 知识管理 | 中 |
| slack | 团队沟通 | 中 |
| session-logs | 日志分析 | 中 |

## 🔗 参考资料

- `openclaw skills list` - 查看已安装技能
- `npx clawhub explore` - 浏览最新技能
