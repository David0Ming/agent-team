#!/usr/bin/env python3
"""
嘟嘟巴士先锋引擎 - Prompt生成模块
整合：司机人设 + 公司信息 + Seedance格式 + 热点/竞品
"""

import json
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "competitor-data"
PROMPT_DIR = PROJECT_DIR / "prompts"

def apply_brand_replacement(text):
    """应用品牌替换规则"""
    replacements = {
        "红色巴士": "车身印有'嘟嘟巴士'四个大字的红色巴士",
        "明黄巴士": "车身印有'嘟嘟巴士'四个大字的红色巴士",
        "大巴": "车身印有'嘟嘟巴士'四个大字的红色巴士",
        "车辆": "车身印有'嘟嘟巴士'四个大字的红色巴士"
    }
    
    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)
    
    return text

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

def load_competitor_insights(date=None):
    """加载竞品洞察"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    insights = []

    # 小红书洞察
    xhs_file = DATA_DIR / date / "xiaojiang_bus_xiaohongshu.md"
    if xhs_file.exists():
        with open(xhs_file, encoding="utf-8") as f:
            insights.append(("小红书", f.read()))

    return insights

def generate_prompt_v1(persona, hotspots, insights):
    """生成视频提示词 V1 - 基于热点"""
    hot_topic = hotspots[0]['content'] if hotspots else "今日热门话题"

    prompt = f"""# 视频提示词 1（12秒）

## 视频主题
《{hot_topic}》

## 司机开场白（45字，语速快）
"{persona['catchphrases'][0]}！{persona['style']['voice']}，今日同大家倾下{hot_topic}！{persona['catchphrases'][2]}"

## 画面描述（12秒分镜，Seedance格式）
**0-3秒 【Hook】**：{persona['video_format']['requirement']}
**4-8秒 【展开】**：司机单手方向盘，另一只手比划，窗外景色闪过
**9-12秒 【反转/收尾】**：司机眨眼竖大拇指，"呢趟车{persona['catchphrases'][2]}"，比OK手势

## 技术参数
- 画幅：{persona['video_format']['aspect_ratio']}
- 色调：暖色调
- 节奏：快切，每3秒一切换
- 禁止项：禁止出现其他巴士logo、水印，车身必须有"嘟嘟巴士"大字

## BGM建议
欢快电子卡点音乐，0:08-秒开始高潮

## 建议Tag
#嘟嘟巴士 {generate_dynamic_tags(hot_topic)}

---
"""
    return apply_brand_replacement(prompt)

def generate_dynamic_tags(topic):
    """根据热点动态生成Tag"""
    tags = []

    if "天气" in topic or "热" in topic or "冷" in topic:
        tags.extend(["#天气出行", "#出行提示"])
    if "开通" in topic or "新线路" in topic or "通车" in topic:
        tags.extend(["#新线路", "#通车"])
    if "春节" in topic or "春运" in topic or "假期" in topic:
        tags.extend(["#春运", "#假期出行"])
    if "优惠" in topic or "便宜" in topic or "降价" in topic:
        tags.extend(["#优惠", "#省钱"])
    if "天气" not in topic and "开通" not in topic and "春节" not in topic and "优惠" not in topic:
        tags.extend(["#热点话题", "#司机日常"])

    return " ".join(tags[:3])  # 最多3个

def generate_prompt_v2(persona, hotspots, insights):
    """生成视频提示词 V2 - 基于竞品对比"""
    # 提取竞品热门话题
    comp_topic = "便捷出行体验"
    if insights:
        for platform, content in insights:
            if "方便" in content or "便捷" in content:
                comp_topic = "出行便捷性"
                break

    prompt = f"""# 视频提示词 2（12秒）

## 视频主题
《{comp_topic}》

## 司机开场白（45字）
"家人们！坐巴士最紧要乜？就系{persona['company_info']['features'][1]}啦！我话你知，边间巴士{persona['company_info']['features'][0]}，呢D先至系真正噶{persona['catchphrases'][1]}！"

## 画面描述（12秒分镜）
**0-3秒 【Hook】**：司机突然转头对镜头，表情夸张
**4-8秒 【展开】**：司机展示手机扫码购票，窗外城市景色
**9-12秒 【反转/收尾】**：司机竖大拇指，"你睇，{persona['company_info']['name']}{persona['catchphrases'][2]}"

## 技术参数
- 画幅：9:16
- 色调：明亮暖色
- 节奏：中速，结尾定格

## BGM建议
轻快抒情，0:15-0:25高潮段

## 建议Tag
#嘟嘟巴士 #便捷出行 #扫码购票 #城际巴士

---
"""
    return apply_brand_replacement(prompt)

def generate_prompt_v3(persona, hotspots, insights):
    """生成视频提示词 V3 - 基于路线/服务"""

    prompt = f"""# 视频提示词 3（12秒）

## 视频主题
《{persona['company_info']['hot_routes'][0]}线开通啦！》

## 司机开场白（45字）
"{persona['catchphrases'][0]}！好消息！{persona['company_info']['hot_routes'][0]}开通啦！以后出行{persona['company_info']['features'][1]}，仲有{persona['company_info']['features'][0]}，{persona['catchphrases'][1]}速度上车啦！"

## 画面描述（12秒分镜）
**0-3秒 【Hook】**：司机兴奋拍方向盘，眼睛发亮
**4-8秒 【展开】**：展示车厢内乘客笑容，窗外高速景色
**9-12秒 【反转/收尾】**：司机做"请"的手势，"呢趟车{persona['catchphrases'][2]}"

## 技术参数
- 画幅：9:16
- 色调：活力橙黄
- 节奏：前慢后快

## BGM建议
励志激昂，0:10-0:20

## 建议Tag
#嘟嘟巴士 #新线路 #广州珠海 #城际出行 #通车

---
"""
    return apply_brand_replacement(prompt)

def generate_all_prompts(date=None):
    """生成所有提示词"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    persona = load_driver_persona()
    hotspots = load_hotspots(date)
    insights = load_competitor_insights(date)

    # 组装完整Prompt
    insights_text = ""
    for p, c in insights:
        insights_text += f"### {p}\n{c[:500]}\n\n"

    content = f"""# 嘟嘟巴士日报 - 视频提示词
# 生成日期: {date}
# 平台：即梦（Seedance）

## 热点来源
{json.dumps(hotspots, ensure_ascii=False, indent=2)}

## 竞品洞察
{insights_text}

---

"""

    content += generate_prompt_v1(persona, hotspots, insights)
    content += generate_prompt_v2(persona, hotspots, insights)
    content += generate_prompt_v3(persona, hotspots, insights)

    # ========== 步骤4：对照 Seedance Skill 格式检查 ==========
    content += "\n---\n## Seedance 格式检查\n"
    content += validate_seedance_format(content)

    # 保存
    prompt_file = PROMPT_DIR / date / "morning_prompt_v1.md"
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Prompt已生成: {prompt_file}")
    return prompt_file

def validate_seedance_format(prompt_text):
    """对照 Seedance Skill 检查格式"""
    issues = []

    # 检查项
    if "12秒" not in prompt_text:
        issues.append("❌ 时长不是12秒")
    if "0-3秒" not in prompt_text:
        issues.append("❌ 缺少0-3秒分镜")
    if "4-8秒" not in prompt_text:
        issues.append("❌ 缺少4-8秒分镜")
    if "9-12秒" not in prompt_text:
        issues.append("❌ 缺少9-12秒分镜")
    if "【Hook】" not in prompt_text:
        issues.append("❌ 缺少Hook")
    if "【反转" not in prompt_text and "【收尾" not in prompt_text:
        issues.append("❌ 缺少反转/收尾")
    if "禁止" not in prompt_text and "禁止项" not in prompt_text:
        issues.append("❌ 缺少禁止项")
    if "嘟嘟巴士" not in prompt_text and "大字" not in prompt_text:
        issues.append("❌ 缺少品牌展示：车身大字")
    if "BGM" not in prompt_text and "音乐" not in prompt_text:
        issues.append("⚠️ 建议添加BGM")
    if "9:16" not in prompt_text and "竖屏" not in prompt_text:
        issues.append("⚠️ 建议注明9:16竖屏")
    
    # 品牌描述检查
    wrong_brands = ["红色巴士", "明黄巴士", "大巴", "车辆"]
    for wrong in wrong_brands:
        if wrong in prompt_text:
            issues.append(f"❌ 发现错误品牌描述：{wrong}，应使用'车身印有'嘟嘟巴士'四个大字的红色巴士'")

    if not issues:
        return "✅ 格式检查通过"

    return "格式检查结果：\n" + "\n".join(issues)

if __name__ == "__main__":
    generate_all_prompts()
