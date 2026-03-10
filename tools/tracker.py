#!/usr/bin/env python3
"""
使用追踪系统 - 记录文件和技能使用情况
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

WORKSPACE = Path.home() / ".openclaw" / "workspace"
TRACKER_FILE = WORKSPACE / "memory" / "logs" / "usage-tracker.json"

def load_tracker() -> Dict:
    """加载追踪数据"""
    if TRACKER_FILE.exists():
        with open(TRACKER_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"files": {}, "skills": {}}

def save_tracker(data: Dict):
    """保存追踪数据"""
    TRACKER_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def track_file_access(file_path: str):
    """记录文件访问"""
    data = load_tracker()
    now = datetime.now().isoformat()
    
    if file_path not in data["files"]:
        data["files"][file_path] = {
            "first_access": now,
            "last_access": now,
            "access_count": 1
        }
    else:
        data["files"][file_path]["last_access"] = now
        data["files"][file_path]["access_count"] += 1
    
    save_tracker(data)

def track_skill_usage(skill_name: str, description: str = ""):
    """记录技能使用"""
    data = load_tracker()
    now = datetime.now().isoformat()
    
    if skill_name not in data["skills"]:
        data["skills"][skill_name] = {
            "first_use": now,
            "last_use": now,
            "use_count": 1,
            "description": description
        }
    else:
        data["skills"][skill_name]["last_use"] = now
        data["skills"][skill_name]["use_count"] += 1
    
    save_tracker(data)

def get_usage_stats(days: int = 30) -> Dict:
    """获取使用统计（最近N天）"""
    data = load_tracker()
    now = datetime.now()
    cutoff = (now - timedelta(days=days)).isoformat()
    
    # 统计文件
    recent_files = [
        f for f, info in data["files"].items()
        if info["last_access"] >= cutoff
    ]
    
    # 统计技能
    recent_skills = [
        s for s, info in data["skills"].items()
        if info["last_use"] >= cutoff
    ]
    
    return {
        "total_files": len(data["files"]),
        "recent_files": len(recent_files),
        "file_usage_rate": len(recent_files) / len(data["files"]) * 100 if data["files"] else 0,
        "total_skills": len(data["skills"]),
        "recent_skills": len(recent_skills),
        "skill_usage_rate": len(recent_skills) / len(data["skills"]) * 100 if data["skills"] else 0,
        "recent_files_list": recent_files[:10],
        "recent_skills_list": recent_skills
    }

if __name__ == "__main__":
    import sys
    from datetime import timedelta
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 tracker.py file <path>  # 记录文件访问")
        print("  python3 tracker.py skill <name> [description]  # 记录技能使用")
        print("  python3 tracker.py stats [days]  # 查看统计")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "file":
        track_file_access(sys.argv[2])
        print(f"✅ 已记录文件访问: {sys.argv[2]}")
    
    elif action == "skill":
        skill_name = sys.argv[2]
        description = sys.argv[3] if len(sys.argv) > 3 else ""
        track_skill_usage(skill_name, description)
        print(f"✅ 已记录技能使用: {skill_name}")
    
    elif action == "stats":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        stats = get_usage_stats(days)
        
        print(f"\n📊 使用统计（最近{days}天）")
        print(f"\n文件:")
        print(f"  总数: {stats['total_files']}")
        print(f"  最近使用: {stats['recent_files']}")
        print(f"  使用率: {stats['file_usage_rate']:.1f}%")
        
        print(f"\n技能:")
        print(f"  总数: {stats['total_skills']}")
        print(f"  最近使用: {stats['recent_skills']}")
        print(f"  使用率: {stats['skill_usage_rate']:.1f}%")
        
        if stats['recent_skills_list']:
            print(f"\n最近使用的技能:")
            for skill in stats['recent_skills_list']:
                print(f"  - {skill}")
