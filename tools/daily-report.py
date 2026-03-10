#!/usr/bin/env python3
"""
每日工作报告生成器
用途：自动生成每日工作总结
"""
from datetime import datetime
from pathlib import Path

MEMORY_DIR = Path.home() / ".openclaw/workspace/memory"

def generate_daily_report():
    """生成每日工作报告"""
    today = datetime.now().strftime("%Y-%m-%d")
    daily_file = MEMORY_DIR / f"{today}.md"
    
    if not daily_file.exists():
        print(f"⚠️  今日记录文件不存在: {daily_file}")
        return
    
    content = daily_file.read_text()
    
    # 简单统计
    lines = content.split('\n')
    tasks_completed = len([l for l in lines if '✅' in l or '[x]' in l])
    tasks_pending = len([l for l in lines if '[ ]' in l])
    
    report = f"""
# 每日工作报告 - {today}

## 📊 统计
- 完成任务: {tasks_completed}
- 待办任务: {tasks_pending}

## 📝 详细内容
{content}
"""
    
    print(report)

if __name__ == "__main__":
    generate_daily_report()
