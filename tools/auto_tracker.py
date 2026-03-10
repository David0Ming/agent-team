#!/usr/bin/env python3
"""
自动追踪系统 - 分析工作流自动记录技能使用
"""

import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set

WORKSPACE = Path.home() / ".openclaw" / "workspace"
TRACKER_FILE = WORKSPACE / "memory" / "logs" / "usage-tracker.json"

# 技能使用特征（自动检测）
SKILL_PATTERNS = {
    "git-commit": {
        "git_commits": True,
        "keywords": ["commit", "提交"]
    },
    "tavily-search": {
        "commands": ["search_fallback.py", "tavily"],
        "keywords": ["搜索", "search"]
    },
    "systematic-debugging": {
        "keywords": ["debug", "bug", "错误", "调试"]
    },
    "agent-browser": {
        "commands": ["agent-browser", "browser"],
        "files": ["fetch_competitor.py"]
    },
    "product-manager-toolkit": {
        "keywords": ["RICE", "优先级", "priorit"],
        "files": ["rice_prioritizer.py"]
    }
}

def load_tracker() -> Dict:
    """加载追踪数据"""
    if TRACKER_FILE.exists():
        with open(TRACKER_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"files": {}, "skills": {}, "auto_detected": {}}

def save_tracker(data: Dict):
    """保存追踪数据"""
    TRACKER_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def detect_git_activity() -> bool:
    """检测是否有git提交"""
    try:
        result = subprocess.run(
            ["git", "log", "--since=1.hour.ago", "--oneline"],
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=5
        )
        return bool(result.stdout.strip())
    except:
        return False

def detect_file_modifications() -> List[str]:
    """检测最近修改的文件"""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1..HEAD"],
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip().split("\n") if result.stdout.strip() else []
    except:
        return []

def auto_detect_skills() -> Set[str]:
    """自动检测使用的技能"""
    detected = set()
    
    # 检测git提交
    if detect_git_activity():
        detected.add("git-commit")
    
    # 检测文件修改
    modified_files = detect_file_modifications()
    for file in modified_files:
        for skill, pattern in SKILL_PATTERNS.items():
            if "files" in pattern:
                if any(f in file for f in pattern["files"]):
                    detected.add(skill)
    
    # 检测命令历史（最近1小时）
    try:
        history_file = Path.home() / ".bash_history"
        if history_file.exists():
            with open(history_file) as f:
                recent_commands = f.readlines()[-100:]  # 最近100条命令
            
            for skill, pattern in SKILL_PATTERNS.items():
                if "commands" in pattern:
                    for cmd in recent_commands:
                        if any(c in cmd for c in pattern["commands"]):
                            detected.add(skill)
    except:
        pass
    
    return detected

def auto_track():
    """自动追踪技能使用"""
    data = load_tracker()
    now = datetime.now().isoformat()
    
    detected_skills = auto_detect_skills()
    
    if not detected_skills:
        print("未检测到技能使用")
        return
    
    for skill in detected_skills:
        if skill not in data["skills"]:
            data["skills"][skill] = {
                "first_use": now,
                "last_use": now,
                "use_count": 1,
                "auto_detected": True
            }
        else:
            data["skills"][skill]["last_use"] = now
            data["skills"][skill]["use_count"] += 1
        
        print(f"✅ 自动检测到技能使用: {skill}")
    
    # 记录自动检测历史
    if "auto_detected" not in data:
        data["auto_detected"] = {}
    
    data["auto_detected"][now] = list(detected_skills)
    
    save_tracker(data)

if __name__ == "__main__":
    print("🔍 自动检测技能使用...")
    auto_track()
