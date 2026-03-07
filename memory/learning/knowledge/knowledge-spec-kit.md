# 知识卡片：Spec Kit - 规格驱动开发

## 来源
- **标题**: Spec Kit 实战！7条命令跑通规格驱动开发+强制 TDD
- **链接**: https://www.aivi.fyi/llms/introduce-spec-kit
- **作者**: AI超元域
- **学习时间**: 2026-03-05

---

## 1️⃣ 复述

**Spec Kit** 是 GitHub 推出的规格驱动开发（SDD）工具链。

**核心理念**: "规格=一等公民"，代码只是规格的表达

**7条命令流水线**:
1. `/constitution` — 确立团队工程原则（铁律）
2. `/specify` — 把想法生成结构化规格
3. `/clarify` — 问清楚不确定的点
4. `/plan` — 生成技术方案
5. `/tasks` — 自动拆解任务（带并行标记）
6. `/analyze` — 一致性检查
7. `/implement` — 落地实现（TDD顺序）

**关键特性**:
- 模板强制"规格写 WHAT/WHY，禁止 HOW"
- TDD 写进流程：先测试再写代码
- 跨 Agent 支持：Claude/Cursor/Codex
- Gate 机制：简单性、反抽象、集成优先

---

## 2️⃣ 应用

**我们可以用**:
1. ✅ 复杂项目起盘
2. ✅ 团队协作统一规范
3. ✅ 避免"意图走样"

---

## 3️⃣ 验证

1. Spec Kit vs Superpowers 哪个更好？
2. 如何集成到我们系统？
3. 实际效果如何？

---

## 4️⃣ 记忆

- **安装**: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`
- **流程**: constitution → specify → clarify → plan → tasks → analyze → implement
- **核心**: 规格驱动，TDD内置

---

## 5️⃣ 用起来

**下一步**:
- [ ] 安装 Spec Kit
- [ ] 对比 Superpowers
