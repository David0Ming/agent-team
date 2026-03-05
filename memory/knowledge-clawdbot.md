# 知识卡片：Clawdbot (Moltbot) 完整指南

## 来源
- **标题**: 实测Clawdbot彻底改变我的工作方式
- **链接**: https://www.aivi.fyi/aiagents/introduce-Clawdbot
- **作者**: AI超元域
- **学习时间**: 2026-03-04

---

## 1️⃣ 复述

**Clawdbot** (现在叫 Moltbot) 是一个开源的个人 AI 助手框架，核心特点：

1. **本地优先** — 数据存在本地，不泄露隐私
2. **多渠道** — WhatsApp/Telegram/Discord/iMessage 都能控制
3. **自我进化** — 能自己学习、写 agent.md
4. **无限记忆** — Markdown 文件存储，可 Git 版本控制
5. **浏览器自动化** — 直接操作网页

**核心理念**: 把 AI 从"咨询工具"变成"数字员工"

**架构**:
- Gateway (网关): WebSocket 控制中枢
- Channels (渠道): WhatsApp/Telegram 等
- Nodes (节点): macOS/iOS/Android 设备
- Skills (技能): 可扩展插件

---

## 2️⃣ 应用

**我们可以用**:
1. ✅ 替代 OpenClaw（更轻量）
2. ✅ WhatsApp/Telegram 控制本地电脑
3. ✅ Cron 定时任务自动化
4. ✅ 浏览器自动化

---

## 3️⃣ 验证

1. Clawdbot 和 OpenClaw 有什么区别？
2. 如何配置 WhatsApp 渠道？
3. Nodes 支持哪些设备？

---

## 4️⃣ 记忆

- **安装**: `curl -fsSL https://molt.bot/install.sh | bash`
- **配置模型**: `clawdbot config set models.providers.minimax.apiKey "xxx"`
- **Cron**: `clawdbot cron add --name "xxx" --cron "0 9 * * *" --message "xxx"`
- **安全**: 默认配对模式 + 沙箱

---

## 5️⃣ 用起来

**下一步**:
- [ ] 对比 Clawdbot vs OpenClaw
- [ ] 试用 Clawdbot
