# 泽钢团队 任务/机制清单

## 📚 文件体系（所有机制都在这）

| 文件 | 作用 | 谁维护 |
|------|------|--------|
| `TEAM.md` | **你正在看的** - 核心清单 | DJJ |
| `HEARTBEAT.md` | 心跳任务详情 | DJJ |
| `AGENTS.md` | 代理配置、对话规则 | DJJ |
| `SOUL.md` | 我的角色设定 | DJJ+泽钢 |
| `USER.md` | 你的信息 | DJJ |
| `memory/` | 记忆文件夹 | DJJ |

---

## 🔴 心跳任务（每15分钟自动执行）

来自 `HEARTBEAT.md`：

1. **Gateway状态** — 检查Agent是否在线
2. **日志错误** — 检查FailoverError/403
3. **持续学习** — 从EvoMap/Skills.sh/GitHub学新知识
4. **待办任务** — 尝试完成一个 `memory/projects.md` 的任务
5. **嘟嘟巴士** — 每日10:00执行
6. **周报** — 每周五17:00生成

---

## 🎯 手动任务

| 任务 | 命令 | 谁做 |
|------|------|------|
| 嘟嘟巴士日报 | `python scripts/run_daily.py` | DMing |
| 代码质量检查 | `ruff check .` | 自动化 |
| 数据清理 | `python scripts/cleanup_data.py` | DJJ→你确认 |

---

## ⚠️ 重要原则

1. **诚实** — 不假装学习，不编造知识
2. **落地** — 学到的东西立即评估用途，不用=没学
3. **透明** — 让你知道我在做什么
4. **高效** — 用最少的token完成任务
5. **可靠** — 说到做到

---

## 🔗 关键文件位置

```
~/.openclaw/workspace/
├── TEAM.md              ← 核心清单（你在这）
├── HEARTBEAT.md         ← 心跳任务详情
├── AGENTS.md            ← 代理规则
├── SOUL.md              ← 我是谁
├── USER.md              ← 你是谁
├── TOOLS.md             ← 工具笔记
└── memory/              ← 记忆库
    ├── projects.md      ← 待办任务
    ├── knowledge-*.md   ← 学到的知识
    └── YYYY-MM-DD.md   ← 每日记录
```
