#!/usr/bin/env python3
"""
嘟嘟巴士先锋引擎 - Prompt生成模块 V3
混合方案：规则引擎 + AI生成 + 反思学习
"""

import json
import random
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "competitor-data"
PROMPT_DIR = PROJECT_DIR / "prompts"
LIBRARY_DIR = PROMPT_DIR / "library"

# 确保库目录存在
LIBRARY_DIR.mkdir(parents=True, exist_ok=True)

# 钩子库（8类）
HOOK_TYPES = [
    "巨物恐惧",  # 巨大的巴士、夸张的场景
    "色彩暴力",  # 红色巴士的视觉冲击
    "声音误导",  # 意外的音效
    "空间错位",  # 车内外的空间对比
    "时间异常",  # 快慢镜头
    "材质欺骗",  # 光影效果
    "尺度混淆",  # 远近对比
    "光影魔术"   # 光线变化
]

# 反差表（5组）
CONTRAST_PAIRS = [
    ("危险", "安全"),    # 路况复杂→巴士平稳
    ("混乱", "有序"),    # 拥挤→舒适
    ("冷漠", "热情"),    # 陌生→温暖
    ("旧", "新"),        # 传统→现代
    ("虚", "实")         # 期待→实现
]

def load_creativity_library():
    """加载创意库"""
    lib_file = LIBRARY_DIR / "creativity-library.json"
    if lib_file.exists():
        with open(lib_file, encoding="utf-8") as f:
            return json.load(f)
    return {"hooks": [], "contrasts": [], "expressions": []}

def load_boundary_conditions():
    """加载边界条件库"""
    bc_file = LIBRARY_DIR / "boundary-conditions.json"
    if bc_file.exists():
        with open(bc_file, encoding="utf-8") as f:
            return json.load(f)
    return {"errors": [], "forbidden": []}

def save_creativity_library(library):
    """保存创意库"""
    lib_file = LIBRARY_DIR / "creativity-library.json"
    with open(lib_file, "w", encoding="utf-8") as f:
        json.dump(library, f, ensure_ascii=False, indent=2)

def save_boundary_conditions(conditions):
    """保存边界条件库"""
    bc_file = LIBRARY_DIR / "boundary-conditions.json"
    with open(bc_file, "w", encoding="utf-8") as f:
        json.dump(conditions, f, ensure_ascii=False, indent=2)

def select_hook_and_contrast():
    """规则引擎：选择钩子和反差组合"""
    hook = random.choice(HOOK_TYPES)
    contrast = random.choice(CONTRAST_PAIRS)
    return hook, contrast

def load_hotspots(date=None):
    """加载热点"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    hotspot_file = DATA_DIR / date / "hotspots.json"
    if hotspot_file.exists():
        with open(hotspot_file, encoding="utf-8") as f:
            return json.load(f)
    return [
        {"source": "backup", "content": "大湾区便捷出行"},
        {"source": "backup", "content": "城际巴士新体验"},
        {"source": "backup", "content": "扫码购票真方便"}
    ]

def build_prompt_for_ai(hook, contrast, hotspot, has_driver=True):
    """构建给AI的提示词"""
    contrast_from, contrast_to = contrast
    
    base_prompt = f"""请创作一个12秒的嘟嘟巴士视频提示词。

**创意要求**：
- 钩子类型：{hook}
- 反差设计：{contrast_from} → {contrast_to}
- 热点结合：{hotspot}

**结构要求**（严格遵守）：
- 0-3秒【Hook】：使用"{hook}"手法，制造视觉冲击
- 4-8秒【展开】：展示"{contrast_from}→{contrast_to}"的反差
- 9-12秒【收尾】：强化品牌"嘟嘟巴士"

**品牌要求**（必须）：
- 车辆描述：车身印有'嘟嘟巴士'四个大字的红色巴士
- 品牌露出：大字占画面40-60%
- 固定Slogan：结尾必须出现"嘟嘟巴士"

**合规红线**（禁止）：
- 禁止黄色/明黄等非品牌颜色
- 禁止巨物恐慌、政治隐喻、社会焦虑、危险行为

"""
    
    if has_driver:
        base_prompt += """
**司机人设**（必须）：
- 性格：粤语司机，爱吐槽但暖心
- 语言：粤语为主，地道表达
- 手势：竖大拇指等标志性动作

请输出：
1. 粤语开场白（30-50字）
2. 完整分镜脚本（包含镜头语言）
3. BGM建议
4. Tag建议
"""
    else:
        base_prompt += """
**无司机版本**：
- 重点展示：线路信息、票价、红色巴士
- 可以是纯景观、乘客视角、品牌展示等

请输出：
1. 视频描述（50字内）
2. 完整分镜脚本（包含镜头语言）
3. BGM建议
4. Tag建议
"""
    
    return base_prompt

def check_brand_compliance(content):
    """品牌合规检查"""
    issues = []
    
    # 检查品牌颜色
    wrong_colors = ["黄色", "明黄", "金黄", "橙色"]
    for color in wrong_colors:
        if color in content:
            issues.append(f"❌ 出现非品牌颜色：{color}")
    
    # 检查品牌描述
    if "嘟嘟巴士" not in content:
        issues.append("❌ 缺少品牌名称：嘟嘟巴士")
    
    if "红色巴士" not in content and "红色大巴" not in content:
        issues.append("⚠️ 建议明确车辆颜色：红色")
    
    return issues

def reflect_and_learn(prompts, date):
    """反思学习：分析生成的prompt，更新创意库和边界条件"""
    library = load_creativity_library()
    conditions = load_boundary_conditions()
    
    # 分析每条prompt
    for i, prompt in enumerate(prompts):
        # 检查品牌合规
        issues = check_brand_compliance(prompt["content"])
        
        if issues:
            # 记录边界条件
            conditions["errors"].append({
                "date": date,
                "prompt_index": i + 1,
                "issues": issues
            })
        else:
            # 记录好的创意
            library["hooks"].append({
                "date": date,
                "hook": prompt["hook"],
                "contrast": prompt["contrast"],
                "quality": "good"
            })
    
    # 保存
    save_creativity_library(library)
    save_boundary_conditions(conditions)
    
    # 生成反思报告
    reflection = {
        "date": date,
        "total_prompts": len(prompts),
        "issues_found": len([p for p in prompts if check_brand_compliance(p["content"])]),
        "creativity_count": len(library["hooks"]),
        "boundary_count": len(conditions["errors"])
    }
    
    return reflection

def generate_all_prompts(date=None):
    """生成10条prompt：前5条司机版，后5条品牌版"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    hotspots = load_hotspots(date)
    prompts = []
    
    # 前5条：司机版
    for i in range(5):
        hook, contrast = select_hook_and_contrast()
        hotspot = hotspots[i % len(hotspots)]["content"]
        
        ai_prompt = build_prompt_for_ai(hook, contrast, hotspot, has_driver=True)
        
        prompts.append({
            "index": i + 1,
            "type": "driver",
            "hook": hook,
            "contrast": contrast,
            "hotspot": hotspot,
            "ai_prompt": ai_prompt,
            "content": ""  # 待AI生成
        })
    
    # 后5条：品牌版
    for i in range(5, 10):
        hook, contrast = select_hook_and_contrast()
        hotspot = hotspots[i % len(hotspots)]["content"]
        
        ai_prompt = build_prompt_for_ai(hook, contrast, hotspot, has_driver=False)
        
        prompts.append({
            "index": i + 1,
            "type": "brand",
            "hook": hook,
            "contrast": contrast,
            "hotspot": hotspot,
            "ai_prompt": ai_prompt,
            "content": ""  # 待AI生成
        })
    
    # 保存AI提示词（供外部AI生成）
    output_file = PROMPT_DIR / date / "ai_prompts.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已生成10条AI提示词: {output_file}")
    print(f"📝 请使用AI模型根据这些提示词生成具体内容")
    
    return output_file

if __name__ == "__main__":
    generate_all_prompts()
