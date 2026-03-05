# Agent-Browser 学习计划 - 团队安排

## 背景
已完成 agent-browser 技能安装，团队需要学习浏览器自动化技术。

## 团队分工

### DJJ（我）
- **角色**: 产品经理 / 统筹
- **职责**:
  - [x] 安装 agent-browser 技能
  - [ ] 掌握核心命令（open, snapshot, click, fill）
  - [ ] 学习命令链和会话管理
  - [ ] 评估自动化场景并分配给团队

### DMing
- **角色**: 技术总监
- **职责**:
  - [ ] 学习核心命令和工作流
  - [ ] 重点研究 Auth Vault 和 Session 持久化
  - [ ] 掌握 JavaScript Evaluation (eval)
  - [ ] 学习安全功能（domain allowlist, action policy）
  - [ ] 评估 Diff 对比功能用于测试

### David
- **角色**: 运营专员
- **职责**:
  - [ ] 学习核心命令和工作流
  - [ ] 重点研究截图、PDF 生成功能
  - [ ] 掌握 Form 自动化和数据提取
  - [ ] 学习 iOS 模拟器测试
  - [ ] 整理使用文档和模板

## 核心学习路径

### 第 1 阶段：基础命令（本周）
```bash
# 必须掌握
agent-browser open <url>
agent-browser snapshot -i
agent-browser click @e1
agent-browser fill @e2 "text"
agent-browser wait --load networkidle
agent-browser close
```

### 第 2 阶段：进阶功能（下周）
- **DJJ**: 命令链、会话管理
- **DMing**: Auth Vault、Session 持久化、安全功能
- **David**: 截图/PDF、Form 自动化、iOS 测试

### 第 3 阶段：实战应用（第 3 周）
- 各自完成 2-3 个实际自动化任务
- 分享经验和最佳实践

## 实战练习建议

| 角色 | 练习任务 |
|------|----------|
| DJJ | 自动化登录 + 数据抓取流程 |
| DMing | 带认证的自动化测试脚本 |
| David | 批量截图 + 表单填写工具 |

## 关键注意事项

1. **Refs 生命周期** — 页面变化后必须重新 snapshot
2. **会话清理** — 用完必须 `agent-browser close`
3. **并发安全** — 多 Agent 使用 `--session` 隔离
4. **复杂 JS** — 使用 `--stdin` 或 `-b` 避免 shell 转义问题

## 资源

- 技能文档: `~/.openclaw/workspace/skills/agent-browser/SKILL.md`
- 官方文档: https://skills.sh/vercel-labs/agent-browser/agent-browser
- GitHub: https://github.com/vercel-labs/agent-browser
