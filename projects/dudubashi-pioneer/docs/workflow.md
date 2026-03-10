# 嘟嘟巴士内容生产工作流程

> 基于2026-03-10实践经验优化

## 概览

**目标**：每日生成高质量、合规的视频prompt，基于竞品数据和热点洞察

**核心原则**：
1. 合规优先 - 任何创意都必须先过合规检查
2. 数据驱动 - 基于单日增量数据做决策
3. 质量>数量 - 宁可少发精品
4. 差异化定位 - 不跟随竞品，找到自己的优势

---

## 完整流程（每日执行）

### 阶段1：竞品数据分析（09:10执行）

**目标**：获取昨天的竞品单日增量数据

**执行步骤**：
```bash
cd ~/.openclaw/workspace/projects/dudubashi-pioneer

# 1. 抓取最新数据
python3 scripts/fetch_newrank_auto.py

# 2. 生成竞品报告
python3 scripts/generate_competitor_report.py

# 3. 生成可视化图表
python3 scripts/visualize_competitors.py

# 4. 计算单日增量
python3 scripts/calculate_daily_increment.py > competitor-data/$(date +%Y-%m-%d)/daily_increment_$(date -d yesterday +%Y-%m-%d).md

# 5. 生成深度分析
python3 scripts/deep_analysis.py > competitor-data/$(date +%Y-%m-%d)/deep_analysis_$(date -d yesterday +%Y-%m-%d).md
```

**输出文件**：
- `competitor-data/YYYY-MM-DD/daily_increment_YYYY-MM-DD.md` - 单日增量数据
- `competitor-data/YYYY-MM-DD/deep_analysis_YYYY-MM-DD.md` - 深度分析报告

**关键指标**：
- 竞品新增作品数
- 竞品新增点赞数
- 平台表现对比（抖音 vs 视频号）
- TOP账号表现
- 互动率分析

---

### 阶段2：热点搜索（09:00执行）

**目标**：找到吸引眼球的真实热点

**执行步骤**：
```bash
# 自动抓取微博热搜（在run_daily.py中）
python3 scripts/run_daily.py --step1
```

**热点要求**：
- ✅ 真实且吸引眼球
- ✅ 与大湾区/深圳/出行相关
- ❌ 不是常规天气热点
- ❌ 不涉及政治、宗教、社会敏感话题

**备用热点库**：
- 深中通道相关（大湾区基建）
- 春招季/职场通勤
- 周末亲子游/景点
- 节假日出行

---

### 阶段3：Prompt生成（09:00执行）

**目标**：生成3-5条高质量、合规的视频prompt

**执行步骤**：

**3.1 生成框架**
```bash
python3 scripts/generate_prompts_v3.py
```
- 输出：`prompts/YYYY-MM-DD/ai_prompts.json`
- 包含：10条提示词框架（钩子、反差、热点）

**3.2 合规预检查**
在填充内容前，先检查框架中的敏感词：
```bash
grep -E "暴力|欺骗|恐惧|焦虑|品牌|广告|营销" prompts/YYYY-MM-DD/ai_prompts.json
```
如果发现敏感词，立即替换：
- "暴力" → "对比"
- "欺骗" → "反转"
- "品牌" → "嘟嘟巴士"

**3.3 填充内容**
基于框架和竞品洞察，撰写完整的视频脚本：

**必须包含**：
1. 粤语开场白（45字内）
2. 完整分镜脚本（12秒，3个阶段）
3. BGM建议
4. Tag建议
5. 合规检查清单

**结构要求**：
- 00:00-00:03【Hook】：视觉钩子
- 00:03-00:08【展开】：反差展示
- 00:08-00:12【收尾】：标识强化

**品牌描述标准**：
车身印有'嘟嘟巴士'四个大字的红色巴士

**Slogan标准**：
嘟嘟巴士！

---

### 阶段4：合规检查（生成后立即执行）

**目标**：确保所有内容符合合规要求

**检查清单**：

**4.1 敏感词检查**
```bash
grep -E "暴力|欺骗|恐惧|焦虑|品牌|广告|营销|推广|黄色|明黄|金黄" prompts/YYYY-MM-DD/*.md
```
- 如果有输出 → 立即修改
- 如果无输出 → 通过

**4.2 品牌描述检查**
```bash
grep -c "车身印有'嘟嘟巴士'四个大字的红色巴士" prompts/YYYY-MM-DD/*.md
```
- 每条prompt至少出现1次
- 不能简化为"巴士"、"大巴"

**4.3 Slogan检查**
```bash
grep "嘟嘟巴士！" prompts/YYYY-MM-DD/*.md
```
- 每条prompt结尾必须有
- 不能使用"呢趟车稳咗"等变体

**4.4 标识展示检查**
- 手动检查分镜脚本
- 确认'嘟嘟巴士'四个大字占画面40-50%

---

### 阶段5：质量验证

**目标**：确保内容质量和差异化

**验证维度**：

**5.1 创意性**
- [ ] 钩子是否吸引眼球（3秒内抓住注意力）
- [ ] 反差是否明显（有情绪起伏）
- [ ] 热点是否真实且相关

**5.2 差异化**
- [ ] 与小江巴士的区别（红色巴士 vs 黄色）
- [ ] 场景化内容（深中通道、通勤、亲子）
- [ ] 不是单纯的司机人设

**5.3 可执行性**
- [ ] 分镜脚本清晰具体
- [ ] BGM建议合理
- [ ] Tag建议精准

**5.4 预期效果**
- 目标互动率：≥124点赞/作品（比小江高50%）
- 平台选择：优先抖音（互动率更高）

---

## 输出文件结构

```
prompts/YYYY-MM-DD/
├── ai_prompts.json          # 框架（10条）
├── manual_prompts.md        # 手动生成的高质量prompt（3-5条）
└── final_prompts.json       # 最终版本（如使用自动填充）

competitor-data/YYYY-MM-DD/
├── daily_increment_YYYY-MM-DD.md  # 单日增量数据
├── deep_analysis_YYYY-MM-DD.md    # 深度分析报告
├── report.md                       # 基础报告
└── charts/                         # 可视化图表
```

---

## 快速执行（一键运行）

```bash
# 完整流程
cd ~/.openclaw/workspace/projects/dudubashi-pioneer
python3 scripts/run_daily.py --force

# 单独执行某个阶段
python3 scripts/run_daily.py --step1  # 热点搜索
python3 scripts/run_daily.py --step2  # 竞品数据
python3 scripts/run_daily.py --step3  # Prompt生成
```

---

## 常见问题

### Q1: 如果微博热搜API失败怎么办？
A: 使用备用热点库（深中通道、春招季、周末游）

### Q2: 如果发现敏感词怎么办？
A: 立即停止，参考`docs/content-standards.md`中的替代词库

### Q3: 如何判断prompt质量？
A: 参考竞品数据，目标互动率≥124点赞/作品

### Q4: 每天生成多少条prompt？
A: 3-5条高质量prompt，质量>数量

### Q5: 如何选择平台？
A: 优先抖音（互动率149.7），其次视频号（42.8）

---

## 参考文档

- `docs/content-standards.md` - 内容生产标准
- `docs/compliance.md` - 合规规范
- `docs/COMPLIANCE-RULES.md` - 详细合规规则
- `docs/creativity.md` - 创意方法
- `docs/Prompt生成核心规范.md` - Prompt规范

---

**版本**：v2.0
**更新时间**：2026-03-10
**更新内容**：
- 整合竞品单日增量数据分析
- 增加合规检查流程
- 优化prompt生成步骤
- 添加质量验证标准
