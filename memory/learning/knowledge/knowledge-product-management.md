# 产品管理知识卡片

**创建时间**: 2026-03-07  
**来源**: product-manager-toolkit skill (sickn33/antigravity-awesome-skills)  
**重要性**: ⭐⭐⭐⭐⭐

## 核心知识

### RICE 优先级框架

**公式**: `Score = (Reach × Impact × Confidence) / Effort`

**参数定义**:
- **Reach**: 每季度影响的用户数
- **Impact**: 
  - Massive = 3x
  - High = 2x
  - Medium = 1x
  - Low = 0.5x
  - Minimal = 0.25x
- **Confidence**: High=100%, Medium=80%, Low=50%
- **Effort**: 人月数（XL/L/M/S/XS）

**使用场景**: 
- 功能需求太多，不知道先做哪个
- 需要向团队/老板解释优先级决策
- 季度规划时分配资源

### 客户访谈分析

**工具**: `customer_interview_analyzer.py`

**能力**:
- 自动提取痛点（带严重程度）
- 识别功能需求（带优先级）
- Jobs-to-be-done 模式识别
- 情感分析
- 主题提取
- 竞品提及
- 关键引用

**使用场景**:
- 用户访谈后快速提取洞察
- 多个访谈的模式识别
- 验证产品假设

### PRD 模板

**4种模板**:
1. **标准 PRD**: 复杂功能（6-8周）
2. **一页 PRD**: 简单功能（2-4周）
3. **功能简报**: 探索阶段（1周）
4. **敏捷 Epic**: 基于 Sprint 交付

**核心结构**: 问题 → 解决方案 → 成功指标

## 应用场景

### 在嘟嘟巴士先锋引擎中

**当前问题**: 
- 有很多视频创意想法，不知道先做哪个
- 不确定哪些提示词模板更有价值

**可以用 RICE**:
```csv
name,reach,impact,confidence,effort
热点追踪功能,1000,high,high,m
竞品监控,500,medium,high,s
提示词优化,2000,massive,medium,l
```

运行: `python scripts/rice_prioritizer.py features.csv --capacity 15`

### 在 Agent 团队协作中

**当前问题**:
- DMing/David/Dplan 等 Agent 的任务分配不够科学
- 缺少明确的需求文档

**可以用 PRD 模板**:
- 为每个 Agent 写清晰的职责 PRD
- 用一页 PRD 快速对齐新功能

### 在产品决策中

**当前问题**:
- 泽钢有很多想法，需要帮他排优先级
- 需要数据支持决策

**可以用**:
- RICE 框架量化每个想法的价值
- 客户访谈分析（如果有用户反馈）
- 北极星指标框架

## 验证问题

1. **场景题**: 泽钢说"我想做3个功能：A能影响1000用户但要3个月，B能影响500用户但只要1周，C能影响2000用户但不确定效果"。如何用 RICE 排序？

2. **实操题**: 如何用这个工具包帮泽钢规划下季度的嘟嘟巴士功能？

3. **判断题**: 什么时候用标准 PRD，什么时候用一页 PRD？

## 使用时机

**触发条件**:
- ✅ 泽钢说"不知道先做哪个"
- ✅ 需要写需求文档
- ✅ 季度规划/路线图
- ✅ 有用户访谈记录需要分析
- ✅ 需要向团队解释优先级

**不适用**:
- ❌ 紧急 bug 修复（直接做）
- ❌ 已经明确的小任务
- ❌ 探索性研究（太早）

## 工具位置

- 安装路径: `~/.openclaw/workspace/.agents/skills/product-manager-toolkit`
- RICE 脚本: `scripts/rice_prioritizer.py`
- 访谈分析: `scripts/customer_interview_analyzer.py`
- PRD 模板: `references/prd_templates.md`

## 下一步行动

1. **立即实践**: 用 RICE 框架评估当前 `memory/projects.md` 中的待办任务
2. **建立流程**: 每次泽钢提新想法时，先用 RICE 评估
3. **文档化**: 为 Agent 团队写一页 PRD
