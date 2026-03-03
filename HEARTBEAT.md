# HEARTBEAT.md - 自动监控任务

## 任务清单

每次心跳执行：

1. **获取 Gateway 状态**
   - 执行: `openclaw status`
   - 记录到: `memory/heartbeat-status.json`
   - 检查: Agent 是否在线、当前模型、错误状态

2. **检查日志错误**
   - 执行: `openclaw logs 2>&1 | tail -20`
   - 记录错误到: `memory/heartbeat-errors.log`
   - 发现 FailoverError / 403 等错误时主动报告

3. **持续学习 - 只学习网上先进知识**

   **学习原则 (深度学习框架):**
   - 每次学习必须完成4步，缺一不可
   - 1️⃣ **复述**: 用自己的话解释这个知识是什么
   - 2️⃣ **应用**: 思考我们系统哪里可以用这个知识
   - 3️⃣ **验证**: 写下2-3个相关问题供日后检验
   - 4️⃣ **记忆**: 存到 `memory/knowledge-[主题].md`，形成知识卡片
   - 5️⃣ **用起来**: 立即实践，能用的马上实现，不能用的规划实现
   
   **重要**: 学习是为了掌握知识，不仅要记住，更要在合适的时候想起来、用起来！
   **不需要跟用户确认**，直接按这个流程执行

   **信息来源 (按优先级):**
   1. **EvoMap (最前沿)** - Gene+Capsule 进化知识
   2. **Skills.sh (实用工具)** - 最新Agent技能
   3. **GitHub Trending** - 热门开源项目
   4. **Hacker News** - 技术新闻和讨论
   5. **AI Research Papers** - 最新AI研究
   6. **Tech Blogs** - 知名技术博客

   **EvoMap 学习 (核心):**
   - 发送心跳: `POST /a2a/heartbeat` (使用完整 GEP-A2A 协议)
   - 获取 promoted assets: `POST /a2a/fetch` (include_tasks: true)
   - 筛选: 只学习评分 > 4.0 的 Gene+Capsule
   - 记录到 `memory/evomap-learning.md`
   - 失败时尝试备用源

   **Skills.sh 学习 (优先实用):**
   - 搜索新技能: `npx skills find [topic]` (topic轮换: ai → devops → testing → productivity)
   - 筛选: 只安装评分 > 4.0 的技能
   - 学习至少 1 个先进Agent技能
   - 记录到 `memory/skills-sh-learning.md`
   - 先进性标准: 解决实际问题、有完整文档、最近更新

   **GitHub Trending 学习 (开源项目):**
   - 获取今日/本周 Trending: `curl https://github.com/trending`
   - 筛选: 只关注 AI/DevOps/Productivity 相关
   - 学习至少 1 个先进开源项目
   - 记录到 `memory/github-trending-learning.md`

   **Hacker News 学习 (技术深度):**
   - 获取 Top Stories: `curl https://hacker-news.firebaseio.com/v0/topstories.json`
   - 筛选: 只学习技术深度 > 3 的内容
   - 记录到 `memory/hackernews-learning.md`

   **学习质量保证:**
   - 每次心跳必须获得至少 1 个先进知识
   - 知识必须满足"先进性"标准 (新、前沿、有价值)
   - 记录学习成果到 `memory/advanced-knowledge-log.md`

4. **更新状态文件**
   - 记录当前时间、模型、Agent数量
   - 供后续查询使用

## 执行频率

- 每 30 分钟检查一次
- 只在 main session 执行
- **学习保证**: 每次心跳必须获得至少 1 个学习成果

## 先进知识验证

每次心跳后检查:
1. `memory/evomap-learning.md` 是否有新 Gene+Capsule
2. `memory/skills-sh-learning.md` 是否有新Agent技能
3. `memory/github-trending-learning.md` 是否有新开源项目
4. `memory/hackernews-learning.md` 是否有新技术深度内容

**先进性标准:**
- ✅ 发布时间 < 30 天
- ✅ 技术深度 > 3 (1-5分)
- ✅ 实用价值 > 3 (1-5分)
- ✅ 不是已掌握的基础知识

如果未获得先进知识，则:
- 记录警告到 `memory/advanced-knowledge-warnings.log`
- 扩大搜索范围 (Reddit / Twitter / 技术论坛)
- 确保下次心跳获得先进知识

## 状态文件格式

```json
{
  "lastCheck": "2026-02-27T18:59:00Z",
  "gateway": {
    "running": true,
    "agents": 7,
    "defaultModel": "gpt-5.1-codex"
  },
  "currentSession": {
    "model": "k2p5",
    "tokens": "59k/262k"
  },
  "errors": []
}
```
