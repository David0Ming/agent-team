# Lessons 分层管理结构

## 架构设计

**渐进式创建模式**：按实际需求创建，避免过度设计

### 文件结构

```
memory/
├── lessons.md              # 通用经验（所有Agent共享）
├── lessons-dming.md        # DMing + 技术团队经验
├── lessons-david.md        # David + 运营团队经验
└── lessons-{agent}.md      # 按需创建（当经验>10条时）
```

### 创建规则

**初始阶段**（当前）：
- 核心Agent：DJJ、DMing、David有独立lessons
- 子Agent：经验暂时记录在对应核心Agent的lessons中

**触发条件**（创建独立lessons）：
1. 某个子Agent的经验>10条
2. 或经验类型明显不同于核心Agent

**示例**：
- Dplan的架构经验记录在lessons-dming.md的"架构设计"小节
- 当Dplan的经验>10条时，创建lessons-dplan.md

### 读取规则

**会话启动时**：
- 所有Agent：读取 lessons.md（通用经验）
- 核心Agent：读取自己的专业lessons
- 子Agent：读取对应核心Agent的lessons

**心跳时**：
- 检查lessons文件更新
- 如有重要更新，重新读取

### 内容分类

**lessons.md（通用）**：
- 任务执行原则
- 沟通协作方法
- 知识管理策略
- 系统维护经验

**lessons-dming.md（技术）**：
- 架构设计决策
- 代码审查经验
- 调试技巧
- 性能优化方法

**lessons-david.md（运营）**：
- 内容创作经验
- 视频脚本技巧
- 用户洞察
- 传播策略

---

**创建时间**：2026-03-08
**维护规则**：
- 通用经验由DJJ维护
- 专业经验由各Agent自己维护
- 每月检查并归档过时经验
