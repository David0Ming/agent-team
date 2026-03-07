# 周报记录 - 2026年3月

## 周报系统配置
- 触发时间：每周五 17:00 (Asia/Shanghai)
- 发送渠道：飞书 ✅、webchat ✅、钉钉 ❌（需Webhook）

## 2026-02-24 ~ 03-02 第9周

### 升级/优化
- [02-28] 创建 token-estimator skill：自动估算代码任务token成本，推荐最优模型
- [02-28] 学习 OpenClaw Skill 系统：Skill vs Plugin 区别、渐进式披露原则
- [03-02] 模型降级方案：当 Fox/Kimi 不可用时自动切换到 Minimax
- [03-03] 学习 Codex 搜索能力：更新 AGENTS.md，搜索必须用 Codex
- [03-03] 完善记忆系统：创建 memory/projects/agent-team/ 结构
- [03-04] 创建 API 端点数据库：memory/api-endpoints.db

### 任务完成
- [02-28] 完成 token-estimator skill 开发和打包
- [03-02] 解决 Fox/Kimi API 冷却问题，配置 Minimax 备用
- [03-02] 团队学习安排配置（EvoMap + Skills.sh）

### 学到的新技能
- [03-01] EvoMap 注册和 GEP-A2A 协议学习
- [03-01] Skills.sh 技能安装：agent-browser, find-skills, last30days
- [02-28] Skill 设计原则：Concise is Key、自由度匹配、渐进式披露

### 系统运行
- 处理多次模型提供商故障
- Gateway 运行正常，心跳周期30分钟
- 上下文管理优化

---

## 2026-03-03 周

### 升级/优化
- [03-05] 学习策略优化：增加"应用"层（是否需要、是否已掌握），验证层改为"真正掌握了吗"
- [03-05] 创建 self-updater skill：自动更新 OpenClaw
- [03-05] 飞书消息连通：支持私聊和群聊
- [03-05] 周报系统搭建：每周五17:00自动生成

### 任务完成
- [03-05] 搭建嘟嘟巴士先锋引擎项目框架
- [03-05] 完成任务A：生成3组视频提示词（按新模板）
- [03-05] 完成任务B：抓取抖音/小红书竞品数据

### 学到的新技能
- [03-05] Firecrawl 网页抓取
- [03-05] Playwright 浏览器自动化

### 其他
- [03-05] 飞书配置和使用已记录到记忆
- [03-05] 新榜达人清单数据获取（15个小江巴士 + 3个熊猫哒）
- [03-05] 竞品数据详细分析（需要VIP权限获取完整播放量）
- [03-05] 任务执行规范：先说→确认→执行（记录到decisions.md）
- [03-05] GitHub仓库创建并推送

---

## 2026-03-05 今天

### 下午完成
- [03-05 15:04] 学习 Seedance prompt skill（https://github.com/songguoxs/seedance-prompt-skill）
- [03-05 15:10] 整合 Seedance 格式到嘟嘟巴士 Prompt 生成
- [03-05 15:14] 添加 Seedance 格式检查步骤
- [03-05 15:27] 添加每条 Prompt 的 Tag 建议（动态生成）
- [03-05 15:39] Tag 动态根据热点内容决定（除 #嘟嘟巴士 固定）
