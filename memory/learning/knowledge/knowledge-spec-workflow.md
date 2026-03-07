# 知识卡片：Claude Code Spec Workflow

## 来源
- **标题**: Claude Code Spec Workflow为Claude Code完美复现Kiro的Spec-Driven规范驱动开发
- **链接**: https://www.aivi.fyi/aiagents/introduce-Claude-Code-Spec-Workflow
- **作者**: AI超元域
- **学习时间**: 2026-03-05

---

## 1️⃣ 复述

**Claude Code Spec Workflow** 是一个 GitHub 开源项目（1.7k Star），为 Claude Code 提供规格驱动开发工作流。

**两个核心工作流**:

1. **Spec Workflow (功能开发)**
   - 需求分析 → 技术设计 → 任务分解 → 代码实现
   - 指令: `/spec-create feature-name "描述"`

2. **Bug Fix Workflow (Bug修复)**
   - 报告 → 分析 → 修复 → 验证
   - 指令: `/bug-create` → `/bug-analyze` → `/bug-fix` → `/bug-verify`

**关键技术优势**:
- **Steering Documents**: 定义项目产品愿景、技术栈、代码结构
- **Token 优化**: 减少 60-80% API 消耗
- **Web Dashboard**: 实时追踪任务进度

**安装**:
```bash
npm i -g @pimzino/claude-code-spec-workflow
```

---

## 2️⃣ 应用

**我们可以用**:
1. ✅ 标准化功能开发流程
2. ✅ Bug 修复流程规范化
3. ✅ 团队协作与进度追踪

---

## 3️⃣ 验证

1. 和 Spec Kit 有什么区别？
2. 如何集成到 OpenClaw？
3. 实际效果如何？

---

## 4️⃣ 记忆

- **安装**: `npm i -g @pimzino/claude-code-spec-workflow`
- **功能开发**: `/spec-create`
- **Bug修复**: `/bug-create` → `/bug-analyze` → `/bug-fix` → `/bug-verify`
- **Token优化**: 60-80%

---

## 5️⃣ 用起来

**下一步**:
- [ ] 安装 Spec Workflow
- [ ] 对比 Spec Kit vs Spec Workflow
