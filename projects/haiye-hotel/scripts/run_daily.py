#!/usr/bin/env python3
"""
海野山房酒店 - 每日定时任务
每日13:40自动执行
"""

import subprocess
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
LOG_DIR = PROJECT_DIR / "logs"

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[{timestamp}] {msg}")

def is_1340():
    """检查是否13:40"""
    now = datetime.now()
    return now.hour == 13 and 40 <= now.minute < 45

def main():
    if not is_1340():
        log("⏰ 未到执行时间（13:40），跳过")
        return
    
    log("🚀 开始生成视频提示词...")
    
    # 执行prompt生成
    script = PROJECT_DIR / "scripts/generate_prompts.py"
    result = subprocess.run(["python3", str(script)], capture_output=True, text=True)
    
    if result.returncode == 0:
        log("✅ 任务完成")
        log(result.stdout)
    else:
        log(f"❌ 任务失败: {result.stderr}")

if __name__ == "__main__":
    main()
