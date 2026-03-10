#!/usr/bin/env python3
"""
海野山房酒店 - Prompt生成脚本 v2
每日13:40自动执行，生成5条专业视频提示词
"""

import json
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
PERSONA_FILE = PROJECT_DIR / "prompts/templates/hostess_persona.json"
PROMPT_DIR = PROJECT_DIR / "prompts"

def load_persona():
    with open(PERSONA_FILE) as f:
        return json.load(f)

def generate_prompts():
    """生成5条专业视频提示词（带图片编号）"""
    persona = load_persona()
    hotel = persona["hotel_info"]
    
    # 5个创意方向（带图片编号）
    prompts_data = [
        {
            "theme": "日落泳池",
            "images": ["IMG-012", "IMG-013"],
            "hook": "镜头从泳池水面缓缓抬起，老板娘（25岁，长发飘逸）站在无边泳池边，背后是270度开阔的田园景观，夕阳将天空染成橙粉色。",
            "expand": "她转身微笑，手指向远处：'这里距离贝壳沙滩只有600米，每天傍晚都能看到这样的日落。'",
            "climax": "镜头拉远，展示泳池与田园的完美融合，老板娘轻声说：'在海野山房，时间好像慢了下来。'",
            "ending": "画面定格在酒店标识上，配文：'涠洲岛上的诗意栖居，等你来体验。'"
        },
        {
            "theme": "木质房间",
            "images": ["IMG-011", "IMG-001"],
            "hook": "推开房门，全木质装修的温暖空间映入眼帘，老板娘站在落地窗前，阳光洒在她的长发上。",
            "expand": "她推开阳台门：'每个房间都有这样的景观，270度无遮挡。'镜头跟随她走到阳台。",
            "climax": "坐在阳台小桌旁，远处是开阔的田野和蓝天，她端起茶杯：'这才是度假该有的样子。'",
            "ending": "'海野山房庄园酒店，20间房，每一间都是风景。'"
        },
        {
            "theme": "酒店外观",
            "images": ["IMG-014", "IMG-016"],
            "hook": "黄昏时分，老板娘站在花园茅草亭下，白色现代建筑在晚霞中格外温暖。",
            "expand": "她走向酒店：'我们2026年刚建成，但已经成为涠洲岛最受欢迎的民宿。'",
            "climax": "镜头环绕酒店一周，展示草坪、树木、现代建筑的和谐共存，她微笑：'因为我们保留了这里的每一棵树。'",
            "ending": "'距离火山口地质公园6公里，距离天主教堂1.1公里。'"
        },
        {
            "theme": "入口迎宾",
            "images": ["IMG-019", "IMG-018"],
            "hook": "老板娘站在酒店入口，'海野山房庄园酒店'标识清晰可见，她张开双臂：'欢迎来到海野山房！'",
            "expand": "她带你走进酒店：'我们有家庭套房、花园套房、亲子房，总有一间适合你。'",
            "climax": "夜幕降临，入口灯光亮起，她回头微笑：'这里不只是住宿，是一种生活方式。'",
            "ending": "'涠洲岛上牛栏山1号，等你来。'"
        },
        {
            "theme": "圆床特色房",
            "images": ["IMG-007", "IMG-009"],
            "hook": "推开门，圆形大床映入眼帘，老板娘笑着说：'这是我们的特色房型。'",
            "expand": "她走到床边：'全木质装修，天花板的横梁都是原木，每一处都是用心设计。'",
            "climax": "镜头展示房间细节，她坐在床边：'很多客人说，这是他们住过最舒服的民宿。'",
            "ending": "'海野山房，20间房，每一间都不一样。'"
        }
    ]
    
    # 视频简介（多样化风格，提升播放量）
    descriptions = {
        "日落泳池": """第一次在涠洲岛看到这样的日落🌅

站在无边泳池边，270度开阔视野，夕阳把整个天空染成橙粉色。老板娘说，这里距离贝壳沙滩只有600米，每天傍晚都能看到这样的景色。

在海野山房，时间好像真的慢了下来⏰

📍广西北海·涠洲岛上牛栏山1号
🏡20间房，每一间都是风景
💰人均？评论区告诉你

#涠洲岛民宿 #日落 #治愈系""",
        
        "木质房间": """本以为只是普通民宿，推开门那一刻惊呆了😮

全木质装修，温暖的原木色调，落地窗外是270度无遮挡的田园景观。阳台上有小桌椅，坐在这里喝茶看风景，这才是度假该有的样子。

老板娘说：海野山房20间房，每一间都不一样✨

你最想住哪一间？评论区聊聊👇

#民宿推荐 #木质装修 #度假""",
        
        "酒店外观": """2026年新开的宝藏民宿，已经成为涠洲岛最受欢迎的打卡地🔥

白色现代建筑+原生树木，老板娘说她们保留了这里的每一棵树。距离火山口地质公园6km，距离天主教堂1.1km，位置绝了👍

黄昏时分最美，茅草亭下拍照出片率100%📸

📍海野山房庄园酒店
💡收藏这条，下次来涠洲岛就住这

#涠洲岛攻略 #民宿推荐 #打卡""",
        
        "入口迎宾": """270度无敌景观是什么体验？来海野山房就知道了🌊

老板娘25岁，把这里打造成涠洲岛最有格调的民宿。家庭套房、花园套房、亲子房...总有一间适合你。

她说：这里不只是住宿，是一种生活方式💫

你觉得呢？

📍涠洲岛上牛栏山1号
🔖关注我，带你发现更多宝藏民宿

#生活方式 #民宿 #涠洲岛""",
        
        "圆床特色房": """住过这么多民宿，这是第一次见到圆床房😍

全木质装修，天花板的横梁都是原木，每一处细节都是用心设计。很多客人说，这是他们住过最舒服的民宿。

海野山房20间房，每一间都不一样。你最想体验哪一间？

💰价格？滑到评论区
📍涠洲岛·海野山房庄园酒店

#特色民宿 #圆床 #设计感"""
    }
    
    prompts = []
    for i, data in enumerate(prompts_data, 1):
        # 组合完整prompt
        prompt = f"""【00:00-00:02 Hook】
{data['hook']}

【00:02-00:05 展开】
{data['expand']}

【00:05-00:09 高潮】
{data['climax']}

【00:09-00:12 收尾】
{data['ending']}

参考图片：{', '.join(data['images'])}
规格：9:16竖屏 | 真实照片风格 | 温暖色调"""
        
        prompts.append({
            "id": i,
            "theme": data["theme"],
            "prompt": prompt,
            "description": descriptions[data["theme"]],
            "images": data["images"],
            "tags": ["#海野山房", "#涠洲岛民宿", f"#{data['theme']}"]
        })
    
    return prompts

def save_prompts(prompts):
    """保存到日期目录"""
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = PROMPT_DIR / today
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "prompts.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 生成5条专业prompt，保存到: {output_file}")
    return output_file

if __name__ == "__main__":
    prompts = generate_prompts()
    save_prompts(prompts)
