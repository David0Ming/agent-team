#!/usr/bin/env python3
"""
填充AI提示词 - 通过David生成完整内容

不依赖外部API，使用OpenClaw内部的多Agent架构
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
PROMPT_DIR = PROJECT_DIR / "prompts"

def call_david(ai_prompt, index):
    """通过Kimi API直接生成内容（不依赖David agent）"""
    import os
    import requests
    
    message = f"""请根据以下要求生成一条完整的嘟嘟巴士视频prompt（Prompt #{index}）：

{ai_prompt}

请直接输出完整的视频脚本内容，包含：
1. 开场白/视频描述
2. 完整分镜脚本
3. BGM建议
4. Tag建议
"""
    
    try:
        # 使用Kimi API
        api_key = os.getenv("MOONSHOT_API_KEY")
        if not api_key:
            return {"error": "缺少MOONSHOT_API_KEY", "full_content": "（配置错误）"}
        
        response = requests.post(
            "https://api.moonshot.cn/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "moonshot-v1-8k",
                "messages": [{"role": "user", "content": message}],
                "temperature": 0.8
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            return {"full_content": content}
        else:
            print(f"⚠️ API调用失败: {response.status_code}")
            return {"error": f"API错误 {response.status_code}", "full_content": "（生成失败）"}
            
    except Exception as e:
        print(f"⚠️ 调用异常: {e}")
        return {"error": str(e), "full_content": "（调用异常）"}

def fill_all_prompts():
    """填充所有prompt"""
    today = datetime.now().strftime("%Y-%m-%d")
    ai_prompts_file = PROMPT_DIR / today / "ai_prompts.json"
    
    if not ai_prompts_file.exists():
        print(f"❌ 文件不存在: {ai_prompts_file}")
        return None
    
    # 读取AI提示词
    with open(ai_prompts_file, "r", encoding="utf-8") as f:
        prompts = json.load(f)
    
    # 填充每条prompt
    for prompt in prompts:
        print(f"生成 Prompt #{prompt['index']}...")
        content = call_david(prompt['ai_prompt'], prompt['index'])
        prompt['content'] = content
    
    # 保存最终结果
    final_file = PROMPT_DIR / today / "final_prompts.json"
    with open(final_file, "w", encoding="utf-8") as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 完整prompt已生成: {final_file}")
    return final_file

if __name__ == "__main__":
    fill_all_prompts()
