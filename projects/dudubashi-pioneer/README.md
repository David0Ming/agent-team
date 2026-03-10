# 嘟嘟巴士先锋引擎 - 视频Prompt生成项目

## 项目概述

自动化生成嘟嘟巴士营销视频的AI Prompt，应用创意方法和合规标准，确保内容质量和平台合规。

## 项目目标

- 每日生成10条高质量视频prompt
- 应用5种创意方法（情感共鸣、叙事反转、场景融合、热点结合、用户视角）
- 严格遵守四大合规标准
- 保持品牌一致性

## 目录结构

```
projects/dudubashi-pioneer/
├── README.md              # 项目概述（本文件）
├── docs/
│   ├── workflow.md        # Prompt生成流程（必读）
│   ├── compliance.md      # 四大合规标准（必读）
│   └── creativity.md      # 创意方法库
├── scripts/               # 生成脚本
│   ├── generate_prompts_v3.py
│   ├── run_daily.py
│   └── ...
├── prompts/               # 输出目录
│   └── YYYY-MM-DD/
│       ├── ai_prompts.json
│       └── video_prompts_*.md
└── logs/                  # 日志目录
```

## 快速开始

### 对于David（CMO）

当你接手嘟嘟巴士视频prompt生成任务时：

1. **阅读核心文档**（必读）：
   - `docs/workflow.md` - 了解完整的生成流程
   - `docs/compliance.md` - 掌握四大合规标准

2. **执行生成流程**：
   ```bash
   cd ~/.openclaw/workspace/projects/dudubashi-pioneer
   python3 scripts/generate_prompts_v3.py
   ```

3. **按照workflow.md中的5步流程执行**：
   - Step 1: 生成框架
   - Step 2: 四大维度预检
   - Step 3: 填充内容
   - Step 4: 10项必检
   - Step 5: 最终确认

4. **输出位置**：
   - `prompts/YYYY-MM-DD/video_prompts_*.md`

### 对于其他Agent

如果你需要接手这个项目：
1. 先读本README了解项目
2. 再读`docs/workflow.md`了解流程
3. 按流程执行即可

## 核心原则

1. **合规第一**：四大合规标准是红线，不可违反
2. **创意为王**：避免机械套用公式，每条prompt都要有独特性
3. **品牌一致**：红色巴士、品牌露出、固定Slogan
4. **双重检查**：预检（概念阶段）+ 自检（生成后）

## 品牌规范

- **车辆描述**：车身印有'嘟嘟巴士'四个大字的红色巴士
- **品牌露出**：大字占画面40-60%
- **固定Slogan**：结尾必须出现"嘟嘟巴士，这趟车稳了！"
- **司机手势**：竖大拇指等标志性动作

## 联系人

- **项目负责人**：David（CMO）
- **技术支持**：DMing（CTO）
- **产品经理**：DJJ

## 版本历史

- v3.0 (2026-03-09): 整合四大合规标准，建立完整流程
- v2.0 (2026-03-09): 增加双重检查机制
- v1.0 (2026-03-09): 初始版本
