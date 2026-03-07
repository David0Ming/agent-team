# 系统清理计划 - 2026-03-07

## 📊 当前状态（触发警报）

- ❌ 知识卡片：70个（目标<50，超标20个）
- ❌ 技能使用率：18.75%（3/16，目标>80%）
- ❌ 记忆文件总数：125个（目标<80，超标45个）

**结论**：需要立即清理！

## 🗑️ 建议删除清单

### 1. 知识卡片（建议删除30个，保留40个）

#### 可以删除的知识卡片（低频/过时）
- `knowledge-chrome-devtools-mcp.md` - 未使用
- `knowledge-clawdbot.md` - 未使用
- `knowledge-clawrouter.md` - 未使用
- `knowledge-openalice.md` - 未使用
- `knowledge-openfang.md` - 未使用
- `knowledge-fusheng-lobster.md` - 未使用（富生龙虾？）
- `knowledge-gpt-5.2-deep-test.md` - 过时
- `knowledge-opus-vs-codex.md` - 过时
- `knowledge-digital-twin.md` - 未使用
- `knowledge-edge-computing.md` - 未使用
- `knowledge-cross-domain-ai.md` - 未使用
- `knowledge-predictive-autoscaling.md` - 未使用
- `knowledge-predictive-monitoring.md` - 未使用
- `knowledge-lifecycle-monitor.md` - 未使用
- `knowledge-logging-pipeline.md` - 未使用
- `knowledge-memory-leak-diagnostics.md` - 未使用
- `knowledge-mq-delay.md` - 未使用
- `knowledge-nginx-lb.md` - 未使用
- `knowledge-object-pooling.md` - 未使用
- `knowledge-serverless-cold-start.md` - 未使用
- `knowledge-slowquery.md` - 未使用
- `knowledge-websocket.md` - 未使用
- `knowledge-zero-copy.md` - 未使用
- `knowledge-memoization.md` - 未使用
- `knowledge-exponential-backoff.md` - 未使用
- `knowledge-token-bucket.md` - 未使用
- `knowledge-race-condition.md` - 未使用
- `knowledge-redis-rate-limit.md` - 未使用
- `knowledge-elastic-scaling.md` - 未使用
- `knowledge-event-driven.md` - 未使用

**保留的知识卡片（高频/实用）**：
- `knowledge-agent-browser.md` ✅ 已使用
- `knowledge-product-management.md` ✅ 已使用
- `knowledge-tavily-search.md` ✅ 已使用
- `knowledge-text-summarization.md` ✅ 最近创建
- `knowledge-systematic-debugging.md` - 应该使用
- `knowledge-agent-memory.md` - 应该使用
- `knowledge-distributed-transaction.md` - 可能有用
- `knowledge-circuit-breaker.md` - 可能有用
- `knowledge-cache-penetration.md` - 可能有用
- `knowledge-connection-pool.md` - 可能有用
- 其他10个高频知识卡片

### 2. 技能（建议删除/归档6个）

#### 可以删除的技能
- `browser-auto` - 与agent-browser功能重叠
- `doubao-video-gen` - 未使用，无明确需求
- `webapp-testing` - 未使用，无明确需求

#### 可以归档的技能（暂不删除，但标记为低优先级）
- `receiving-code-review` - 有用但未使用
- `requesting-code-review` - 有用但未使用
- `test-driven-development` - 有用但未使用

**保留并主动使用的技能**：
- `agent-browser` ✅
- `product-manager-toolkit` ✅
- `tavily-search` ✅
- `git-commit` - 应该使用
- `systematic-debugging` - 应该使用
- `token-estimator` - 应该使用
- `self-updater` - 应该使用
- `find-skills` - 应该使用
- `last30days` - 应该使用
- `web-scraping` - 应该使用

### 3. 学习记录（建议整合）

#### 可以删除的学习记录
- `memory/learning/aivi/aivi-fyi-learning.md` - 过时
- `memory/learning/david-learning.md` - 应该整合到主文件
- `memory/learning/evomap/evomap密集学习.md` - 重复
- `memory/learning/evomap/evomap-真实学习-2026-03-05.md` - 过时
- `memory/learning/skills/hackernews-learning.md` - 空文件？
- `memory/learning/skills/local-skills-learning.md` - 应该整合

#### 保留的学习记录
- `memory/learning/knowledge/INDEX.md` ✅
- `memory/learning/evomap/evomap-learning.md` - 最新
- `memory/learning/skills-sh/skills-sh-learning.md` - 最新

### 4. 日志文件（建议归档）

#### 可以归档的日志（>30天）
- `memory/daily/2026-02/` 下的所有文件（2月的日志）

#### 保留的日志
- `memory/daily/2026-03/` 下的所有文件（3月的日志）

## ✅ 执行计划

### 第1步：删除无用知识卡片（30个）
```bash
cd ~/.openclaw/workspace/memory/learning/knowledge/
rm knowledge-chrome-devtools-mcp.md knowledge-clawdbot.md knowledge-clawrouter.md ...
```

### 第2步：删除重复技能（3个）
```bash
cd ~/.openclaw/workspace/skills/
rm -rf browser-auto doubao-video-gen webapp-testing
```

### 第3步：整合学习记录
合并分散的学习记录到主文件

### 第4步：归档旧日志
```bash
mkdir -p ~/.openclaw/workspace/memory/archive/2026-02/
mv ~/.openclaw/workspace/memory/daily/2026-02/* ~/.openclaw/workspace/memory/archive/2026-02/
```

## 📊 预期结果

- 知识卡片：70 → 40（减少30个）
- 技能数量：16 → 13（删除3个）
- 记忆文件：125 → 85（减少40个）
- 技能使用率：18.75% → 76.9%（10/13）

## ⚠️ 风险评估

**低风险**：
- 删除的知识卡片都是未使用的
- 删除的技能都是重复或无用的
- 归档的日志可以随时恢复

**建议**：先执行，如果发现问题可以从git恢复

---

**等待确认**：是否执行清理计划？
