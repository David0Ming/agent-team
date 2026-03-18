# AgentSkills 元数据标准

## 标准Frontmatter格式

```markdown
---
name: skill-name
version: 1.0.0
author: DJJ
compatibility: openclaw >= 2026.3.0
description: "简短描述，触发场景"
tags: [category1, category2]
---
```

## 字段说明

### 必需字段
- **name**: 技能唯一标识符（kebab-case）
- **version**: 语义化版本号（major.minor.patch）
- **author**: 创建者（DJJ/DMing/David/社区）
- **description**: 简短描述和使用场景

### 可选字段
- **compatibility**: OpenClaw最低版本要求
- **tags**: 分类标签（便于搜索）
- **dependencies**: 依赖的其他技能或工具
- **deprecated**: 是否已废弃

## 版本号规则

- **1.0.0**: 初始稳定版本
- **1.1.0**: 新增功能（向后兼容）
- **1.0.1**: Bug修复
- **2.0.0**: 破坏性变更

## 示例

```markdown
---
name: token-estimator
version: 1.2.0
author: DJJ
compatibility: openclaw >= 2026.2.0
description: "Estimate task token cost and recommend model selection"
tags: [optimization, cost-management]
---
```
