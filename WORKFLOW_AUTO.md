# WORKFLOW_AUTO.md - 自动工作流配置

## 概述
此文件定义OpenClaw启动时自动加载的工作流配置，确保系统协议在上下文重置后恢复。

## 核心工作流

### 1. 启动协议
- **每次启动时**：读取 SOUL.md、USER.md、AGENTS.md
- **主会话时**：读取 memory/README.md 和相关主题文件
- **每日检查**：读取当天的 memory/YYYY-MM-DD.md

### 2. 心跳工作流
- **频率**：每30分钟执行一次
- **任务**：
  1. 检查Gateway状态 (`openclaw status`)
  2. 检查日志错误 (`openclaw logs`)
  3. 持续学习先进知识（EvoMap + Skills.sh + GitHub）
  4. 更新状态文件和知识记录

### 3. 学习工作流
- **优先级**：
  1. EvoMap (Gene/Capsule先进知识)
  2. Skills.sh (Agent技能)
  3. GitHub Trending (开源项目)
  4. Hacker News (技术新闻)
  5. AI Research Papers (学术研究)

- **先进性标准**：
  - 发布时间 < 30天
  - 技术深度 > 3/5
  - 实用价值 > 3/5
  - 不是已掌握的基础知识

### 4. 团队同步工作流
- **DJJ**：统筹全局，分配任务，质量控制
- **DMing**：技术实施，代码开发，系统架构
- **David**：运营推广，社区建设，内容创作

### 5. 模型管理工作流
- **默认模型**：deepseek-chat (成本效益)
- **大上下文任务**：切换到GPT-5.1-Codex等大容量模型
- **代码任务**：根据文件大小自动选择模型
  - > 1200万字符 → 最佳模型
  - ≤ 1200万字符 → 限时额度模型

## 文件依赖

### 必需文件
- `SOUL.md` - 身份和个性定义
- `USER.md` - 用户信息
- `AGENTS.md` - 工作空间指南
- `HEARTBEAT.md` - 心跳任务清单

### 内存文件
- `memory/README.md` - 内存系统说明
- `memory/YYYY-MM-DD.md` - 每日记录
- `memory/identity.md` - 身份记忆
- `memory/user.md` - 用户记忆
- `memory/decisions.md` - 决策记录
- `memory/projects.md` - 项目跟踪

### 状态文件
- `memory/heartbeat-status.json` - Gateway状态
- `memory/heartbeat-errors.log` - 错误日志
- `memory/advanced-knowledge-log.md` - 知识学习记录

## 错误处理

### 常见错误
1. **文件不存在**：创建缺失的文件
2. **模型配额耗尽**：切换到备用模型
3. **上下文饱和**：触发压缩或重启会话
4. **插件警告**：设置plugins.allow配置

### 恢复策略
1. **优雅降级**：使用可用资源继续运行
2. **自动修复**：创建缺失的配置文件
3. **通知用户**：报告问题并建议解决方案
4. **学习记录**：记录错误和修复过程

## 更新记录
- **创建时间**: 2026-03-02 05:43
- **创建原因**: 系统启动时要求读取此文件
- **维护者**: DJJ (agent:main)

---
**注意**: 此文件应在每次OpenClaw启动时自动读取，确保工作流配置正确加载。