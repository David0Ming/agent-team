# openclaw-MacOS 升级方案

**目标**：优化Agent组织结构、记忆方式、项目组织方式

## 第一步：配置飞书消息接收

编辑 `~/.openclaw/openclaw.json`，在 `channels.feishu` 部分添加：
```json
"requireMention": false
```

重启Gateway：
```bash
openclaw gateway restart
```

## 第二步：更新AGENTS.md

从local复制最新的AGENTS.md v2.0（4-Block结构）

## 第三步：优化记忆系统

建立主题文件分类：
- `memory/decisions.md` - 决策记录
- `memory/lessons.md` - 经验教训
- `memory/tools.md` - 工具配置
- `memory/projects.md` - 项目管理

## 第四步：建立项目组织

采用 `projects/{project-name}/` 结构：
- README.md - 项目概述
- docs/ - 流程文档

## 完成后

在 `bot-comm/mac-to-local/` 创建确认文件
