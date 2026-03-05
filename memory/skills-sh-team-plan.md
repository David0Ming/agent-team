# Skills.sh 学习计划 - 团队安排

## 背景
已完成 skills.sh (find-skills) 配置，团队需要学习如何使用 skills 生态系统发现和安装技能。

## 团队分工

### DJJ（我）
- **角色**: 产品经理 / 统筹
- **职责**: 
  - [x] 安装并配置 find-skills 技能
  - [ ] 建立技能发现工作流
  - [ ] 定期评估新技能对团队的价值

### DMing
- **角色**: 技术总监
- **职责**:
  - [ ] 学习 `npx skills find` 搜索技能
  - [ ] 重点研究技术类技能（testing, devops, code-quality）
  - [ ] 评估技能质量并推荐给团队
  - [ ] 学习技能结构，为创建自定义技能做准备

### David
- **角色**: 运营专员
- **职责**:
  - [ ] 学习 `npx skills find` 搜索技能
  - [ ] 重点研究 productivity, documentation 类技能
  - [ ] 整理技能使用文档和最佳实践

## 核心命令速查

```bash
# 1. 搜索技能
npx skills find react performance
npx skills find testing jest
npx skills find deploy docker

# 2. 安装技能（全局+自动确认）
npx skills add owner/repo@skill-name -g -y

# 3. 检查更新
npx skills check

# 4. 更新所有技能
npx skills update

# 5. 浏览技能市场
open https://skills.sh/
```

## 推荐优先学习的技能领域

| 优先级 | 领域 | 原因 |
|--------|------|------|
| P0 | testing | 提升代码质量 |
| P0 | devops | 部署和CI/CD |
| P1 | documentation | 文档自动化 |
| P1 | code-quality | 代码审查和重构 |
| P2 | design | UI/UX 设计 |

## 下一步行动

1. **本周内**: DMing 和 David 各自搜索并安装 2-3 个相关技能
2. **每周同步**: 分享发现的优质技能和使用心得
3. **持续优化**: 根据项目需求不断发现和集成新技能

## 资源

- 技能市场: https://skills.sh/
- 热门来源: 
  - vercel-labs/agent-skills
  - ComposioHQ/awesome-claude-skills
