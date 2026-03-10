#!/usr/bin/env python3
"""测试Kimi API"""

import requests

api_key = "sk-kimi-CJdGG7t6B8gxdtao4o7labU4YNWKuaqPtX6pnPiqXlu0bVQfQL6MNprW7sLak3CK"
api_url = "https://api.kimi.com/coding/"

test_prompt = """请创作一个12秒的嘟嘟巴士视频提示词。

**创意要求**：
- 钩子类型：尺度混淆
- 反差设计：虚 → 实
- 热点结合：深圳天气：晴转多云，23-28°C

请输出：
1. 粤语开场白（30-50字）
2. 完整分镜脚本（包含镜头语言）
3. BGM建议
4. Tag建议
5. 发布文案（50-100字）
6. 字幕（如有）
"""

print("测试Kimi API...")
print(f"API URL: {api_url}")

try:
    response = requests.post(
        api_url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "kimi",
            "messages": [
                {"role": "system", "content": "你是嘟嘟巴士的视频创意专家。"},
                {"role": "user", "content": test_prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 2000
        },
        timeout=60
    )
    
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text[:500]}")
    
    if response.status_code == 200:
        data = response.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        print("\n生成内容:")
        print(content[:500])
        print("\n✅ Kimi API测试成功")
    else:
        print(f"\n❌ API返回错误: {response.status_code}")
        
except Exception as e:
    print(f"\n❌ 测试失败: {e}")
