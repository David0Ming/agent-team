#!/usr/bin/env python3
"""
豆包 Seedance 视频生成脚本
使用 OpenAI 兼容格式调用
"""
import argparse
import os
import sys
import requests
import json
import time

def generate_video(prompt, output="./output.mp4", width=1080, height=1920):
    """调用豆包 API 生成视频"""
    
    api_key = os.environ.get("ARK_API_KEY", "f76f61ca-73e1-4edd-83a7-82100f367b86")
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 正确的模型名称
    model = "doubao-seed-2-0-pro-260215"
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": f"生成视频: {prompt}, 尺寸: {width}x{height}"
            }
        ],
        "stream": False
    }
    
    try:
        print(f"调用模型: {model}")
        print(f"提示词: {prompt}")
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"成功!")
            print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 提取返回内容
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0].get("message", {}).get("content", "")
                print(f"\n生成内容: {content}")
            
            return output
        else:
            print(f"错误: {response.text}")
            sys.exit(1)
            
    except Exception as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="豆包视频生成")
    parser.add_argument("--prompt", required=True, help="视频描述")
    parser.add_argument("--output", default="./output.mp4", help="输出路径")
    parser.add_argument("--width", type=int, default=1080, help="视频宽度")
    parser.add_argument("--height", type=int, default=1920, help="视频高度")
    
    args = parser.parse_args()
    generate_video(args.prompt, args.output, args.width, args.height)

if __name__ == "__main__":
    main()
