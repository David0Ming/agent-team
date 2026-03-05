# 知识卡片：Chrome DevTools MCP

## 来源
- **标题**: 谷歌Chrome DevTools MCP彻底颠覆AI浏览器自动化
- **链接**: https://www.aivi.fyi/aiagents/introduce-Chrome-DevTools-MCP
- **作者**: AI超元域
- **学习时间**: 2026-03-05

---

## 1️⃣ 复述

**Chrome DevTools MCP** 把 Chrome DevTools 能力封装成 MCP 工具，让 AI 能直接操控浏览器。

**解决的问题**:
- AI 以前看不到真实运行时
- 需要人工打开浏览器复现问题
- 现在 AI 自己能"看见、点得动、测得准"

**核心能力**:
- 浏览器操控：点击、输入、填表、拖拽
- 调试取证：网络请求、控制台日志、DOM快照
- 性能分析：LCP、TBT、CLS 指标
- 仿真：弱网、CPU降频、移动端尺寸

**使用方式**:
```bash
# Claude Code
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest

# Codex
codex mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
```

---

## 2️⃣ 应用

**我们可以用**:
1. ✅ 表单自动化测试
2. ✅ 性能回归检测
3. ✅ Bug 复现取证
4. ✅ 弱网体验评估

---

## 3️⃣ 验证

1. MCP 和 OpenClaw 的 browser 工具哪个好？
2. 如何集成到我们系统？
3. 安全性和隔离如何？

---

## 4️⃣ 记忆

- **启动**: `npx chrome-devtools-mcp@latest`
- **能力**: 浏览器操控 + 调试取证 + 性能分析
- **场景**: 自动化测试、Bug复现、性能评估

---

## 5️⃣ 用起来

**下一步**:
- [ ] 配置 Chrome DevTools MCP
- [ ] 测试浏览器自动化
