# aivi.fyi 学习 - 2026-03-05

## 网站概述
- **名称**: AI超元域 (aivi.fyi)
- **类型**: 中文AI智能体博客
- **内容**: OpenClaw 教程、使用技巧、经验分享

## 核心知识点

### 1. OpenClaw 核心特性
- 持久记忆 + 定时任务
- 可集成 Home Assistant 控制智能家居
- **边执行边学习**：能记住踩过的坑并更新到 Skill
- 安全机制：自动拒绝危险命令（如 `rm -rf /`）

### 2. 三大核心 Skill
| Skill | 功能 |
|-------|------|
| X Post | 自动发布 X (Twitter) |
| Podcast | 生成英文播客（从链接提取内容）|
| Claude Code | 调用 Claude Code + SpecKit 规格驱动开发 |

### 3. Skill 迭代方法论
```
需求 → 执行 → 报错 → 调试 → 经验写 Skill → 测试 → 更新 Skill → 循环
```

### 4. 让 AI 越用越聪明
- 完成任务后让 AI 将经验存到记忆文件
- 同时更新到对应 Skill
- 下次执行类似任务直接读取经验

## 何时使用
- 搭建新 Agent 时
- 优化 Skill 开发流程时
- 需要让 AI 学习新能力时

## 验证问题
- OpenClaw 如何拒绝危险命令？
- SpecKit 是什么？怎么用？
- 如何让 Agent 自动更新 Skill？
