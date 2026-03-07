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

### 🏢 产品工作轨（工作时间）

**优先级基于 RICE 分析 (2026-03-07)**

- [x] **P0: 测试prompt生成质量** (RICE: 1000.0) ✅ 已完成
  - 完成时间：2026-03-07
  - 成果：
    - 测试了旧版prompt质量（6.5/10）
    - 修复了P0问题（语言风格、文本重复、逻辑错误）
    - 重构为混合方案（规则引擎+AI生成+反思学习）
    - 生成了10条高质量prompt（前5条司机版+后5条品牌版）
    - 质量提升到8.5/10（博人眼球、创意丰富）
    - 创建了反思学习机制和创意库

- [ ] **P1: 飞书机器人上传文件权限+竞品可视化** (RICE: 10.0)
  - 任务：配置飞书应用权限，上传文件能力
  - 任务：把竞品信息设置成可视化图表并上传
  - 影响：50个团队成员
  - 工作量：Large (需要权限申请+开发)
  - **建议：本周内完成**

- [ ] **P2: 给OpenClaw连接Discord** (RICE: 4.0)
  - 任务：配置Discord频道，让OpenClaw可以发送消息到Discord
  - 影响：10个潜在用户
  - 工作量：Medium
  - **建议：下周执行**

### 📚 个人成长轨（学习时间）

- [ ] 学习三个中等题视频 (RICE: 0.33)
  - 任务：找3个讲解中等难度题目的视频学习
  - 目标：掌握解题思路和方法
  - **建议：每天晚上1小时**
  
- [ ] 找合适的实验论文综述 (RICE: 0.16)
  - 任务：搜索并阅读实验论文综述
  - 目标：掌握分析实验结果的方法
  - **建议：本周找到合适的综述**

---

### 其他想法/待办

- [x] 检查学习策略：确保学到的知识和技能都记录了"何时使用"
  - [x] 更新现有学习记录（github-trending-learning.md, skills-sh-learning.md）
  - [x] 更新 HEARTBEAT.md 的学习流程 ← 刚完成
- [x] 批判性学习两个微信文章
  - [x] 文章1：微信文章自动总结+同步飞书 (Victor)
  - [x] 文章2：傅盛的龙虾实践课 (郎瀚威 Will)
- [x] 批判性学习 aivi.fyi 所有内容
