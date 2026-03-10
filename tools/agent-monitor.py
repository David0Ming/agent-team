#!/usr/bin/env python3
"""
Agent性能监控工具
用途：监控agent的响应时间、任务完成率、错误率
"""
import json
from datetime import datetime
from pathlib import Path

MONITOR_DIR = Path.home() / ".openclaw/workspace/memory/monitoring"
MONITOR_DIR.mkdir(exist_ok=True)

def log_task(agent: str, task: str, duration: float, success: bool):
    """记录任务执行情况"""
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = MONITOR_DIR / f"{today}.jsonl"
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent,
        "task": task,
        "duration": duration,
        "success": success
    }
    
    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")

def get_stats(agent: str = None):
    """获取统计数据"""
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = MONITOR_DIR / f"{today}.jsonl"
    
    if not log_file.exists():
        print("📊 今日暂无监控数据")
        return
    
    tasks = []
    with open(log_file) as f:
        for line in f:
            entry = json.loads(line)
            if agent is None or entry["agent"] == agent:
                tasks.append(entry)
    
    if not tasks:
        print(f"📊 {agent or '所有agent'} 今日暂无数据")
        return
    
    total = len(tasks)
    success = sum(1 for t in tasks if t["success"])
    avg_duration = sum(t["duration"] for t in tasks) / total
    
    print(f"📊 {agent or '所有agent'} 今日统计:")
    print(f"  总任务数: {total}")
    print(f"  成功率: {success/total*100:.1f}%")
    print(f"  平均耗时: {avg_duration:.2f}s")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        get_stats(sys.argv[1])
    else:
        get_stats()
