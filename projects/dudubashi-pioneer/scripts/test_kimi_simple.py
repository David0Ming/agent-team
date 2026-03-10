#!/usr/bin/env python3
"""测试Kimi Code API Key"""

import anthropic

api_key = "sk-kimi-CJdGG7t6B8gxdtao4o7labU4YNWKuaqPtX6pnPiqXlu0bVQfQL6MNprW7sLak3CK"
base_url = "https://api.kimi.com/coding/"

print(f"测试Kimi Code...")
print(f"Base URL: {base_url}")
print(f"API Key: {api_key[:20]}...")

try:
    client = anthropic.Anthropic(
        api_key=api_key,
        base_url=base_url
    )
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=100,
        messages=[
            {"role": "user", "content": "你好，请回复'测试成功'"}
        ]
    )
    
    content = message.content[0].text
    print(f"\n✅ 测试成功！")
    print(f"响应: {content}")
    
except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    print("\n可能的原因:")
    print("1. API Key无效或过期")
    print("2. 需要在Kimi会员页面重新生成key")
    print("3. Base URL不正确")
