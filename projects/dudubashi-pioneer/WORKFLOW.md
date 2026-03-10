# 嘟嘟巴士竞品数据抓取 - 标准工作流程

> 本文档记录竞品数据抓取的完整流程，确保下次执行时可以直接参考

## 📋 目录

1. [环境准备](#环境准备)
2. [配置文件](#配置文件)
3. [执行流程](#执行流程)
4. [故障排查](#故障排查)
5. [自动化配置](#自动化配置)

---

## 环境准备

### 必需依赖

```bash
# Python依赖
pip3 install --user playwright beautifulsoup4 matplotlib

# Playwright浏览器
playwright install chromium
```

### 目录结构

```
dudubashi-pioneer/
├── scripts/
│   ├── fetch_newrank_dom.py       # 数据抓取脚本
│   ├── generate_competitor_report.py  # 报告生成
│   └── visualize_competitors.py   # 可视化
├── config/
│   └── newrank.json               # NewRank配置
├── competitor-data/
│   └── YYYY-MM-DD/                # 每日数据
├── newrank_cookies.json           # 登录cookies
└── logs/
    └── reflection-YYYY-MM-DD.md   # 执行复盘
```

---

## 配置文件

### 1. NewRank配置 (`config/newrank.json`)

**首次创建**：
```bash
mkdir -p config
cat > config/newrank.json << 'EOF'
{
  "competitors": {
    "小江巴士": {
      "url": "https://www.newrank.cn/talentlist/share?f=share&source=9513&keyword=drqd&l=qwiswt2tu9fo&uuid=qwiswt2tu9fo",
      "list_id": "qwiswt2tu9fo"
    },
    "熊猫哒巴士": {
      "url": "https://www.newrank.cn/talentlist/share?f=share&source=9513&keyword=drqd&l=ozs697lbubnf&uuid=ozs697lbubnf",
      "list_id": "ozs697lbubnf"
    }
  },
  "cookies_file": "newrank_cookies.json"
}
EOF
```

### 2. Cookies配置 (`newrank_cookies.json`)

**获取方式**：
1. 浏览器打开 https://www.newrank.cn
2. 微信扫码登录
3. F12 → Application → Cookies → 复制所有cookies
4. 保存到 `newrank_cookies.json`

**格式**：
```json
[
  {
    "name": "token",
    "value": "...",
    "domain": ".newrank.cn",
    "path": "/"
  }
]
```

**有效期**：约30天，过期后需重新获取

---

## 执行流程

### 手动执行

```bash
cd ~/projects/dudubashi-pioneer

# 1. 抓取数据（自动化版本，推荐）
python3 scripts/fetch_newrank_auto.py

# 2. 生成报告
python3 scripts/generate_competitor_report.py

# 3. 生成可视化（可选）
python3 scripts/visualize_competitors.py
```

**自动化脚本特性**：
- ✅ 自动读取配置文件（config/newrank.json）
- ✅ 自动检查和安装依赖
- ✅ 自动清理账号名称（移除序号和换行符）
- ✅ 错误提示清晰

### 预期输出

```
抓取 小江巴士 数据...
✅ 小江巴士: 15个账号
抓取 熊猫哒巴士 数据...
✅ 熊猫哒巴士: 12个账号

✅ 数据已保存到: competitor-data/2026-03-09
✅ 报告已生成: competitor-data/2026-03-09/report.md
```

### 输出文件

- `competitor-data/YYYY-MM-DD/xiaojiangbus_detailed.json` - 小江巴士数据
- `competitor-data/YYYY-MM-DD/pandabus_detailed.json` - 熊猫哒巴士数据
- `competitor-data/YYYY-MM-DD/report.md` - 竞品分析报告
- `competitor-data/YYYY-MM-DD/charts/` - 可视化图表（如果生成）

---

## 故障排查

### 问题1：抓取返回0个账号

**原因**：
- Cookies过期
- URL不完整
- 页面结构变化

**解决**：
1. 检查cookies是否有效（重新登录获取）
2. 确认URL包含完整参数（f=share, source, keyword等）
3. 运行测试脚本查看页面内容：
   ```bash
   python3 scripts/test_newrank_page.py
   ```

### 问题2：matplotlib未安装

**解决**：
```bash
pip3 install --user matplotlib
# 或
pip3 install matplotlib --break-system-packages
```

### 问题3：Playwright浏览器未安装

**解决**：
```bash
playwright install chromium
```

### 问题4：数据质量问题

**检查**：
- 账号名称是否包含序号和换行符
- NewRank指数是否为0
- 平台分布是否合理

**解决**：运行数据清洗脚本（待开发）

---

## 自动化配置

### 方案1：集成到run_daily.py

**修改 `scripts/run_daily.py`**：
```python
# 在09:00执行时，同时抓取竞品数据
if current_hour == 9 and 0 <= current_minute <= 5:
    print("抓取竞品数据...")
    subprocess.run(['python3', 'scripts/fetch_newrank_dom.py'])
    subprocess.run(['python3', 'scripts/generate_competitor_report.py'])
```

### 方案2：独立cron任务

**添加到crontab**：
```bash
# 每天09:10执行竞品数据抓取
10 9 * * * cd ~/projects/dudubashi-pioneer && python3 scripts/fetch_newrank_dom.py && python3 scripts/generate_competitor_report.py
```

### 方案3：心跳任务

**添加到 `HEARTBEAT.md`**：
```markdown
### 竞品数据抓取（每日 09:10）
检查当前时间是否 09:10-09:15 (Asia/Shanghai)，如果是且今日未执行：
```bash
python3 ~/.openclaw/workspace/projects/dudubashi-pioneer/scripts/fetch_newrank_dom.py
python3 ~/.openclaw/workspace/projects/dudubashi-pioneer/scripts/generate_competitor_report.py
```
```

---

## 关键注意事项

1. **Cookies有效期**：约30天，需定期更新
2. **完整URL**：必须包含所有参数（f=share, source, keyword等）
3. **数据验证**：抓取后检查账号数量和数据质量
4. **Fallback机制**：失败时使用上次数据
5. **执行时间**：建议09:10执行（避开嘟嘟巴士引擎的09:00）

---

## 快速参考

**一键执行（自动化版本）**：
```bash
cd ~/projects/dudubashi-pioneer && \
python3 scripts/fetch_newrank_auto.py && \
python3 scripts/generate_competitor_report.py
```

**查看最新报告**：
```bash
cat competitor-data/$(date +%Y-%m-%d)/report.md
```

**检查数据**：
```bash
ls -lh competitor-data/$(date +%Y-%m-%d)/
```

---

**最后更新**：2026-03-09
**维护者**：DJJ

## 改进记录

### 2026-03-09
- ✅ 创建自动化脚本 `fetch_newrank_auto.py`
- ✅ 自动读取配置文件
- ✅ 自动检查依赖
- ✅ 自动清理数据
- ✅ 完整的错误提示

