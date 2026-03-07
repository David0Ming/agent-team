# 知识卡片：Claude Code Hooks 零轮询方案

## 来源
- **标题**: OpenClaw高级使用经验之如何调用Claude Code最省Token
- **链接**: https://www.aivi.fyi/aiagents/OpenClaw-Agent-Teams
- **来源**: AI超元域 (aivi.fyi)
- **学习时间**: 2026-03-04

---

## 1️⃣ 复述

**问题**: OpenClaw 调用 Claude Code 时，每隔几秒轮询一次进程状态，任务执行时间越长，Token 消耗越大。

**解决方案**: 使用 Claude Code 的 Hooks 回调机制 + Agent Teams：
1. **发射后不管**: OpenClaw 下达一次任务，Claude Code 后台独立运行
2. **双重回调**: Claude Code 完成 后自动触发 Stop Hook + SessionEnd Hook
3. **双通道设计**:
   - `latest.json` = 数据通道（存完整结果）
   - Wake Event = 信号通道（通知 AGI 醒来）
4. **Agent Teams**: 多个 Agent 并行协作，主进程不被阻塞

**效果**: OpenClaw 消耗的 Token 几乎可以忽略不计。

---

## 2️⃣ 应用

**我们系统可以用在**:
1. ✅ **coding-agent skill**: 让 Claude Code 后台运行，不阻塞主会话
2. ✅ **任务完成通知**: 任务完成后自动推送消息到聊天群组
3. ✅ **容错设计**: 即使 Gateway API 挂了，latest.json 依然保存结果

---

## 3️⃣ 验证

**检验问题**:
1. Claude Code Hooks 如何配置？需要哪些环境变量？
2. Agent Teams 和 subagents 有什么区别？
3. Wake Event 的 text 字段长度限制是多少？

---

## 4️⃣ 记忆

**核心概念**:
- Dispatch（发射后不管）
- 双通道冗余（latest.json + wake event）
- Hooks 回调机制
- Agent Teams 并行协作

---

## 5️⃣ 用起来

**下一步行动**:
- [ ] 配置 Claude Code Hooks 到我们的 coding-agent
- [ ] 测试零轮询调用效果
- [ ] 对比 Token 消耗差异

**参考项目**: https://github.com/win4r/claude-code-hooks
