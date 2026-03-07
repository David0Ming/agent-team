#!/usr/bin/env python3
"""
嘟嘟巴士先锋引擎 - Prompt生成模块 V2
抽象框架，保证创造力
"""

import json
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "competitor-data"
PROMPT_DIR = PROJECT_DIR / "prompts"

def load_driver_persona():
    """加载司机人设"""
    persona_file = PROJECT_DIR / "prompts" / "templates" / "driver_persona.json"
    with open(persona_file, encoding="utf-8") as f:
        return json.load(f)

def load_hotspots(date=None):
    """加载热点"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    hotspot_file = DATA_DIR / date / "hotspots.json"
    if hotspot_file.exists():
        with open(hotspot_file, encoding="utf-8") as f:
            return json.load(f)
    return []

def generate_abstract_prompt(persona, hotspots, prompt_index):
    """生成抽象框架的 Prompt - 给 AI 创造空间"""
    
    hot_topic = hotspots[prompt_index % len(hotspots)]['content'] if hotspots else "大湾区出行"
    
    # 抽象框架 - 不给具体内容，只给约束
    prompt = f"""# 视频提示词 {prompt_index + 1}（12秒）

## 创作要求

**主题方向**: {hot_topic}

**司机人设**:
- 性格: {persona['personality']}
- 语言风格: {persona['style']['language']}
- 语气: {persona['style']['tone']}

**视频结构** (严格遵守):
- 0-3秒 【Hook】: {', '.join(persona['video_format']['hook_types'])} 任选其一
- 4-8秒 【展开】: 司机讲述/展示，结合窗外景色
- 9-12秒 【收尾】: {', '.join(persona['video_format']['ending_types'])} 任选其一

**品牌展示** (必须):
- 车辆: {persona['brand_visual']['vehicle']}
- 必须出现: {', '.join(persona['brand_visual']['must_show'])}

**公司信息** (可选融入):
- {persona['company_info']['name']}
- 特点: {', '.join(persona['company_info']['features'])}
- 覆盖: {persona['company_info']['coverage']}

**技术参数**:
- 画幅: {persona['video_format']['aspect_ratio']}
- 总时长: 12秒
- 色调: 暖色调/明亮
- 节奏: 根据内容自由把握

**禁止项**:
- 禁止出现其他巴士品牌logo
- 禁止水印
- 车身必须有"嘟嘟巴士"大字

## 创作提示

请基于以上框架，自由创作：
1. 设计一个吸引人的 Hook（0-3秒）
2. 编写粤语风格的司机开场白（30-50字）
3. 描述具体的画面分镜（包含镜头语言）
4. 建议合适的 BGM 和 Tag

---
"""
    return prompt

def generate_all_prompts(date=None):
    """生成所有提示词"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    persona = load_driver_persona()
    hotspots = load_hotspots(date)
    
    if not hotspots:
        hotspots = [
            {"source": "backup", "content": "大湾区便捷出行"},
            {"source": "backup", "content": "城际巴士新体验"},
            {"source": "backup", "content": "扫码购票真方便"}
        ]

    content = f"""# 嘟嘟巴士日报 - 视频提示词框架
# 生成日期: {date}
# 平台：即梦（Seedance）
# 版本：V2 抽象框架

## 热点来源
{json.dumps(hotspots, ensure_ascii=False, indent=2)}

---

"""

    # 生成3组抽象框架
    for i in range(3):
        content += generate_abstract_prompt(persona, hotspots, i)
        content += "\n"

    # 保存
    prompt_file = PROMPT_DIR / date / "morning_prompt_v2.md"
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ 抽象框架已生成: {prompt_file}")
    return prompt_file

if __name__ == "__main__":
    generate_all_prompts()
