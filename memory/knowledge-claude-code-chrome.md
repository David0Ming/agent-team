# 知识卡片：Claude Code 原生 Chrome 集成

## 来源
- **标题**: Claude Code原生支持真正的Chrome浏览器
- **链接**: https://www.aivi.fyi/aiagents/introduce-Claude-Code-for-Chrome
- **作者**: AI超元域
- **学习时间**: 2026-03-05

---

## 1️⃣ 复述

**核心功能**: Claude Code 可以原生接管 Chrome 浏览器，实现端到端自动化。

**解决痛点**:
- 以前：写代码 → 手动切浏览器 → 点点点 → 验证 → 回编辑器
- 现在：Claude 直接操作浏览器，帮你完成整个闭环

**核心优势**:
1. **共享 Session** — 继承你的登录状态，不用重新登录
2. **全能操作** — 点击、输入、读 Console、监控 Network
3. **实时视觉** — 你看着它操作，能立刻发现问题

**使用方式**:
- 启动: `claude --chrome`
- 运行中: `/chrome` 检查状态
- 局限: 仅支持原生 Chrome，暂不支持 WSL

---

## 2️⃣ 应用

**我们可以用**:
1. ✅ 自动化测试 — 不用写 Playwright/Cypress 脚本
2. ✅ UI 调试 — 边写边调，AI 帮你验证
3. ✅ 数据录入 — 自动填表、抓数据
4. ✅ API 测试 — 取代 Postman

---

## 3️⃣ 验证

1. Chrome 扩展怎么安装？
2. 安全机制是什么？
3. Token 消耗如何？

---

## 4️⃣ 记忆

- **启动**: `claude --chrome`
- **优势**: 共享登录 + 实时视觉 + 端到端
- **场景**: 自动化测试、UI调试、数据录入

---

## 5️⃣ 用起来

**下一步**:
- [ ] 安装 Claude in Chrome 扩展
- [ ] 测试 `claude --chrome`
