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
   - 每次学习必须完成5步，缺一不可
   - 1️⃣ **复述**: 用自己的话解释这个知识是什么
   - 2️⃣ **应用**: 思考我们系统哪里可以用这个知识 → 我们需要这个知识吗？我们已经掌握了吗？← 扩充
   - 3️⃣ **时机**: 明确这个知识/技能什么时候使用
   - 4️⃣ **验证**: 验证自己是否真正掌握这个知识/技能，会用了吗？能向别人讲清楚吗？← 修正
   - 5️⃣ **记忆**: 存到 `memory/knowledge-[主题].md`，形成知识卡片

   **学习分工**:
   - DJJ本人: 技术/Agent相关
   - David(运营): **视频创意、审美、美术** ← 新增重点
   - DMing(技术): 搜索/爬虫/数据

   **David团队学习方向 (每3天轮换)**:
   - 短视频创意：TikTok/抖音热门视频分析
   - 视觉美学：配色、构图、镜头语言
   - 文案技巧：开场白、Hook、反转
   - 平台热点：即梦/可灵/veo热门提示词
   - 竞品分析：同行动态
   - 6️⃣ **用起来**: 立即实践，能用的马上实现，不能用的规划实现
   
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

5. **更新日志**
   - 记录心跳期间完成的工作到 `memory/daily/YYYY-MM-DD.md`
   - 格式：简洁记录时间、任务、成果
   - 示例：`### HH:MM 心跳 - 学习了X技能，解决了Y问题`

6. **更新记忆**
   - 重要学习成果写入主题文件
   - 新知识 → `memory/learning/knowledge/knowledge-[主题].md`
   - 重要决策 → `memory/decisions.md`
   - 经验教训 → `memory/lessons.md`

7. **尝试解决一个待办任务**
   - 读取 `memory/projects.md`
   - 找到 `[ ]` 未完成的任务
   - **重要待办提醒**（每次心跳必须列出）:
     - ❌ 学习三个中等题视频
     - ❌ 找合适的实验论文综述
     - ❌ 给OpenClaw连接Discord
     - ❌ 飞书机器人上传文件权限 + 竞品可视化上传
     - ❌ 测试prompt生成质量
   - 尝试完成其中一个（不是所有）
   - 完成后更新 projects.md 标记为 `[x]`
   - **注意**：只尝试，不强制完成；复杂的需要向泽钢确认

8. **嘟嘟巴士先锋引擎（每日09:00）**
   - 检查当前时间是否 09:00-09:05 (Asia/Shanghai)
   - 如果是且今日未执行，运行 `python3 ~/.openclaw/workspace/projects/dudubashi-pioneer/scripts/run_daily.py`
   - 执行后记录状态

9. **周报任务（每周五17:00）**
   - 检查当前时间是否周五 17:00-17:05
   - 如果是，生成周报
   - 读取 memory/weekly-records.md
   - 输出到 memory/周报-YYYY-Wxx.md

## 执行频率

- DJJ 每 **1小时** 心跳一次
- 其他 Agent 每 30 分钟心跳一次
- **个人待办提醒**：每 **30分钟** 独立执行（不与心跳合并）

## 🚀 定时自动化任务

### 个人待办提醒（每30分钟）

单独设置定时任务，提醒5个待办事项：
- 学习三个中等题视频
- 找合适的实验论文综述
- 给OpenClaw连接Discord
- 飞书机器人上传文件权限 + 竞品可视化上传
- 给韦达发送3条Prompt

## 🚀 定时自动化任务

### 嘟嘟巴士先锋引擎（每日 09:00）

检查是否到执行时间（09:00），如果到达且今日未执行，运行：

```bash
python3 ~/.openclaw/workspace/projects/dudubashi-pioneer/scripts/run_daily.py
```

任务内容：
- 任务A：抓取热点 + 生成3组视频提示词
- 任务B：监控竞品数据（小江巴士、熊猫哒巴士）

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

## 🛡️ 系统维护（预防机制）

### 每日维护（每次心跳）
- [ ] 检查今日创建的文件，评估价值
- [ ] 检查技能使用情况（参考SKILL-USAGE-RULES.md）
- [ ] 提醒未使用的技能

### 每周维护（周日执行）
**触发条件**：当前是周日

- [ ] 清理本周未使用的知识卡片
- [ ] 评估技能使用率（目标>80%）
- [ ] 检查记忆文件数量（目标<80）
- [ ] 更新INDEX.md使用统计

**执行命令**：
```bash
# 检查知识卡片数量
ls ~/.openclaw/workspace/memory/learning/knowledge/knowledge-*.md | wc -l

# 检查技能数量
ls -d ~/.openclaw/workspace/skills/*/ | wc -l

# 检查记忆文件总数
find ~/.openclaw/workspace/memory -type f -name "*.md" | wc -l
```

### 每月维护（月初执行）
**触发条件**：当前是每月1-3号

- [ ] 归档上月日志
- [ ] 清理>30天未使用的知识卡片
- [ ] 清理>30天未使用的技能
- [ ] 生成月度维护报告

**执行命令**：
```bash
# 归档上月日志
LAST_MONTH=$(date -d "last month" +%Y-%m)
mkdir -p ~/.openclaw/workspace/memory/archive/$LAST_MONTH/
mv ~/.openclaw/workspace/memory/daily/$LAST_MONTH/* ~/.openclaw/workspace/memory/archive/$LAST_MONTH/
```

## 📊 监控指标（每次心跳检查）

- 知识卡片数量（目标<50，当前27）
- 技能使用率（目标>80%，当前23%）
- 记忆文件总数（目标<80，当前98）

**警报触发**：
- 知识卡片>60 → 立即清理
- 技能使用率<70% → 反思并改进
- 记忆文件>100 → 立即清理

