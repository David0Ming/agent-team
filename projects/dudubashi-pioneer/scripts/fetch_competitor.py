#!/usr/bin/env python3
"""
竞品数据抓取脚本 - 使用agent-browser
"""

import subprocess
import json
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "competitor-data"

def run_agent_browser(command):
    """执行agent-browser命令"""
    result = subprocess.run(
        f"agent-browser {command}",
        shell=True,
        capture_output=True,
        text=True,
        timeout=30
    )
    return result.stdout, result.returncode

def fetch_xiaohongshu_competitor(competitor_name):
    """抓取小红书竞品数据"""
    print(f"抓取小红书 - {competitor_name}")
    
    try:
        # 1. 打开小红书搜索页
        url = f"https://www.xiaohongshu.com/search_result?keyword={competitor_name}"
        run_agent_browser(f'open "{url}"')
        
        # 2. 等待加载
        run_agent_browser('wait --load networkidle')
        
        # 3. 获取快照
        output, code = run_agent_browser('snapshot -i')
        
        # 4. 截图保存
        today = datetime.now().strftime("%Y-%m-%d")
        screenshot_path = DATA_DIR / today / f"{competitor_name}_xiaohongshu.png"
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        run_agent_browser(f'screenshot --full > {screenshot_path}')
        
        # 5. 关闭浏览器
        run_agent_browser('close')
        
        return {
            "platform": "xiaohongshu",
            "competitor": competitor_name,
            "status": "success",
            "snapshot": output[:500],  # 保存部分快照
            "screenshot": str(screenshot_path),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        print(f"抓取失败: {e}")
        return {
            "platform": "xiaohongshu",
            "competitor": competitor_name,
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def main():
    """主函数"""
    competitors = ["小江巴士", "熊猫哒巴士"]
    results = []
    
    for comp in competitors:
        result = fetch_xiaohongshu_competitor(comp)
        results.append(result)
    
    # 保存结果
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = DATA_DIR / today / "competitor_data.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 竞品数据已保存: {output_file}")

if __name__ == "__main__":
    main()
