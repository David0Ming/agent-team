#!/usr/bin/env python3
"""
合规检查模块 - 确保生成的prompt符合法律法规和平台规则
"""

import re
from typing import Dict, List, Tuple

# 违规关键词库
FORBIDDEN_KEYWORDS = {
    "侵权类": [
        "模仿", "复刻", "致敬", "参考XX广告", "像XX一样",
        "明星", "名人", "演员", "歌手", "网红",
        "抖音热门", "爆款视频", "模仿热门"
    ],
    "低俗类": [
        "性感", "诱惑", "暴露", "低俗", "色情"
    ],
    "虚假宣传": [
        "最好", "第一", "唯一", "绝对", "保证",
        "100%", "完全", "永久", "终身"
    ],
    "颜色违规": [
        "黄色巴士", "金黄巴士", "明黄巴士", "橙色巴士"
    ]
}

# 必须包含的合规元素
REQUIRED_ELEMENTS = [
    "原创",
    "红色巴士",
    "嘟嘟巴士"
]

def check_compliance(prompt: str) -> Tuple[bool, List[str]]:
    """
    检查prompt是否合规
    
    Returns:
        (is_compliant, issues) - (是否合规, 问题列表)
    """
    issues = []
    
    # 1. 检查违规关键词
    for category, keywords in FORBIDDEN_KEYWORDS.items():
        for keyword in keywords:
            if keyword in prompt:
                issues.append(f"[{category}] 包含违规关键词: {keyword}")
    
    # 2. 检查必须元素
    for element in REQUIRED_ELEMENTS:
        if element not in prompt:
            issues.append(f"[缺失] 缺少必须元素: {element}")
    
    # 3. 检查品牌描述
    if "巴士" in prompt and "红色巴士" not in prompt:
        issues.append("[品牌] 巴士描述不规范，必须使用'红色巴士'")
    
    # 4. 检查价格真实性
    price_pattern = r'(\d+)元'
    prices = re.findall(price_pattern, prompt)
    for price in prices:
        if int(price) != 29:
            issues.append(f"[虚假宣传] 价格不准确: {price}元（正确价格: 29元）")
    
    # 5. 检查是否有原创声明
    if "原创" not in prompt and "不得与" not in prompt:
        issues.append("[合规] 缺少原创声明")
    
    is_compliant = len(issues) == 0
    return is_compliant, issues

def add_compliance_declaration(prompt: str) -> str:
    """
    为prompt添加合规声明
    """
    declaration = """
【原创声明】：本片为100%原创设计，不得与任何现有广告、影视作品相似。

【素材要求】：
- 音乐：免版税音乐库（Epidemic Sound/抖音版权库）
- 字体：开源字体（思源黑体/阿里普惠体）
- 画面：AI生成原创场景，无真实影视片段

【合规要求】：
- 符合公序良俗，无低俗、暴力、猎奇
- 宣传内容真实准确（票价29元，覆盖大湾区15城）
- 无侵权元素，无虚假承诺
- 标注"AI辅助创作，人工深度修改"
"""
    
    # 如果prompt中没有合规声明，添加
    if "【原创声明】" not in prompt:
        prompt = declaration + "\n" + prompt
    
    return prompt

def fix_brand_description(prompt: str) -> str:
    """
    修正品牌描述
    """
    # 将所有"巴士"替换为"车身印有'嘟嘟巴士'四个大字的红色巴士"
    # 但保留已经正确的描述
    if "车身印有'嘟嘟巴士'四个大字的红色巴士" in prompt:
        return prompt
    
    # 简单替换：巴士 → 红色巴士
    prompt = re.sub(r'(?<!红色)巴士', '红色巴士', prompt)
    
    # 确保至少出现一次完整品牌描述
    if "车身印有'嘟嘟巴士'四个大字" not in prompt:
        prompt += "\n\n【品牌元素】：车身印有'嘟嘟巴士'四个大字的红色巴士，品牌色鲜艳红色。"
    
    return prompt

def generate_compliance_report(prompt: str) -> Dict:
    """
    生成合规检查报告
    """
    is_compliant, issues = check_compliance(prompt)
    
    report = {
        "is_compliant": is_compliant,
        "issues": issues,
        "timestamp": datetime.now().isoformat(),
        "prompt_length": len(prompt),
        "has_original_declaration": "原创" in prompt,
        "has_brand_description": "红色巴士" in prompt,
        "has_compliance_requirements": "合规要求" in prompt
    }
    
    return report

if __name__ == "__main__":
    # 测试
    test_prompt = """
    9:16竖屏，主题：从混乱到有序。
    0-3秒：车票特写，29元。
    4-8秒：红色巴士整齐停靠。
    9-12秒：车身"嘟嘟巴士"大字。
    """
    
    print("=== 合规检查测试 ===")
    is_compliant, issues = check_compliance(test_prompt)
    print(f"是否合规: {is_compliant}")
    if issues:
        print("问题列表:")
        for issue in issues:
            print(f"  - {issue}")
    
    print("\n=== 添加合规声明 ===")
    compliant_prompt = add_compliance_declaration(test_prompt)
    print(compliant_prompt[:200] + "...")
    
    print("\n=== 修正品牌描述 ===")
    fixed_prompt = fix_brand_description(test_prompt)
    print(fixed_prompt)
