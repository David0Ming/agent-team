# 技能学习队列

## 待学习技能（按优先级排序）

### P0 - 立即学习
- [x] agent-browser (Vercel) - 浏览器自动化
- [ ] evomap-skill - 如果 EvoMap 发布官方技能

### P1 - 本周学习 (Skills.sh)
- [ ] testing-skills - 测试相关技能
- [ ] devops-skills - 部署/CI-CD 技能
- [ ] documentation-skills - 文档自动化

### P2 - 下周学习 (Skills.sh)
- [ ] code-quality-skills - 代码审查/重构
- [ ] design-skills - UI/UX 设计
- [ ] productivity-skills - 工作流自动化

## 学习来源

### 1. EvoMap (优先)
- **URL**: https://evomap.ai
- **协议**: GEP-A2A
- **内容**: Gene (策略) + Capsule (实现) + EvolutionEvent (过程)
- **获取方式**: `POST /a2a/fetch`
- **优势**: 实战验证的解决方案，可直接复用

### 2. Skills.sh (并行)
- **URL**: https://skills.sh
- **CLI**: `npx skills find [query]` / `npx skills add [skill]`
- **内容**: 结构化技能文档 (SKILL.md)
- **优势**: 丰富的社区技能，易于安装

### 3. Clawhub
- **CLI**: `clawhub search [query]`
- **内容**: OpenClaw 官方技能
- **优势**: 与 OpenClaw 深度集成

## 学习记录

| 时间 | 技能 | 来源 | 状态 |
|------|------|------|------|
| 2026-03-01 | agent-browser | skills.sh | ✅ 已安装 |
| 2026-03-01 | find-skills | skills.sh | ✅ 已安装 |
| 2026-03-01 | evomap-protocol | evomap.ai | ✅ 已学习 |
| 2026-03-01 | last30days | clawhub | ✅ 已安装 |

## 团队学习分配

- **DJJ**: 统筹 EvoMap + Skills.sh 学习，优先学习产品管理相关
- **DMing**: 优先学习技术类技能（testing, devops, code-quality）
- **David**: 优先学习运营类技能（documentation, productivity, design）

## 心跳学习策略

每次心跳 (30分钟):
1. **EvoMap**: 获取新的 Gene+Capsule (实战方案)
2. **Skills.sh**: 搜索并安装 1 个新技能 (工具能力)
3. **记录更新**: 同步到 evomap-learning.md + skills-learned.md
