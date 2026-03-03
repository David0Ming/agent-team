# 🚀 Projects

> ⚠️ 每次心跳检查待办，尝试解决一个。完成后删除该项目。

## 进行中

### Agent 团队架构
- **状态**: ✅ 已完成
- **核心团队**: DJJ（产品经理）、DMing（CTO）、David（CMO）
- **技术团队**: Dplan（架构）、Dcensor（审查）、Ddebug（调试）
- **模型策略**: 限时额度优先，大任务切最佳模型

## 已完成

### OpenClaw 配置优化
- **状态**: ✅ 已完成
- **开始**: 2026-02-28
- **目标**: 配置自定义 memory 插件，优化工作流程
- **任务**:
  - [x] 禁用内置 memory-lancedb
  - [x] 配置 memory-lancedb-pro 插件
  - [x] 拆分 MEMORY.md 为主题文件
  - [x] 配置 Agent 人设（双层设定）
  - [x] 配置模型容灾机制（双线策略）
  - [x] 重启验证新配置

### Token Estimator Skill
- **状态**: ✅ 已完成
- **时间**: 2026-02-28
- **成果**: 
  - 创建了 `token-estimator` skill
  - 实现了文件大小检测脚本 `estimate.py`
  - 设定了阈值规则：
    - < 3M 字符 → Lightweight (Opus 4.6)
    - 3M-12M 字符 → Standard (GPT-5.1)
    - > 12M 字符 → Premium (GPT-5.2)
  - 打包为 `.skill` 文件，可分发安装
- **位置**: `~/.openclaw/workspace/skills/token-estimator/`

### Agent 三层协作架构
- **状态**: ✅ 已完成
- **时间**: 2026-03-03
- **来源**: 基于 Shubham Saboo 40天实验
- **成果**:
  - [x] 身份层：SOUL.md, IDENTITY.md, USER.md
  - [x] 操作层：AGENTS.md, HEARTBEAT.md
  - [x] 知识层：MEMORY.md, memory/YYYY-MM-DD.md
  - [x] 共享层：memory/shared-context/THESIS.md, FEEDBACK-LOG.md
  - [x] 单写者原则写入 AGENTS.md
- **验证**: 与文章方法论100%对齐

## 想法/待办

- [ ] 考虑安装 mem0 插件（高级记忆系统）
- [ ] 配置 git 同步
