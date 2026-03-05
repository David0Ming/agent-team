# Agent Skill 学习任务分配

## 背景
泽钢要求 DMing 和子 Agent 学习 Agent Skill 系统，参考资源：
- https://agentskills.me/
- https://github.com/vercel-labs/agent-skills

## 学习资料

### 必读文件
1. `~/.npm-global/lib/node_modules/openclaw/skills/coding-agent/SKILL.md` — Skill 完整示例
2. `~/.openclaw/workspace/skills/token-estimator/SKILL.md` — 我们自建的 Skill 案例
3. `~/.npm-global/lib/node_modules/openclaw/skills/skill-creator/SKILL.md` — Skill 创建指南

### 在线资源
- Vercel Agent Skills 展示站: https://agentskills.me/
- GitHub 开源实现: https://github.com/vercel-labs/agent-skills

---

## 任务分配

### DMing (CTO)
**目标**: 全面掌握 Skill 系统设计，规划团队 Skill 体系

**任务**:
1. 阅读所有必读文件
2. 研究 Vercel Agent Skills 的设计理念
3. 输出学习笔记 `skill-learning-notes.md`，包含：
   - Skill vs Plugin 的区别
   - Skill 的标准结构（SKILL.md + scripts/ + references/ + assets/）
   - 好 Skill 的设计原则（渐进式披露、自由度匹配）
   - 建议团队开发的 3-5 个新 Skill

### Dplan (架构师)
**目标**: 掌握 Skill 调用机制，设计 Skill 集成方案

**任务**:
1. 阅读 coding-agent SKILL.md
2. 理解 Skill 的渐进式披露设计
3. 输出笔记 `skill-notes.md`，包含：
   - 子 Agent 使用 Skill 的最佳实践
   - Skill 调用的常见坑和注意事项

### Dcensor (审查员)
**目标**: 建立 Skill 质量审查标准

**任务**:
1. 阅读 coding-agent SKILL.md
2. 理解 Skill 的安全边界
3. 输出审查清单 `skill-review-checklist.md`，包含：
   - Skill 安全审查的 5 个要点
   - Skill 质量评估标准

### Ddebug (调试专家)
**目标**: 掌握 Skill 调试方法

**任务**:
1. 阅读 coding-agent SKILL.md
2. 理解 Skill 执行流程
3. 输出调试指南 `skill-debug-guide.md`，包含：
   - Skill 执行失败的常见原因
   - 调试步骤和工具

### David (运营)
**目标**: 了解 Skill 的基本概念

**任务**:
1. 快速阅读 coding-agent SKILL.md
2. 输出简要总结 `skill-summary.md`

---

## 交付时间
- Dplan/Dcensor/Ddebug/David: 1 小时内完成
- DMing: 2 小时内完成（需要深度研究）

## 交付位置
- DMing: `workspace-dming/skill-learning-notes.md`
- Dplan: `workspace-dplan/skill-notes.md`
- Dcensor: `workspace-dcensor/skill-review-checklist.md`
- Ddebug: `workspace-ddebug/skill-debug-guide.md`
- David: `workspace-david/skill-summary.md`
