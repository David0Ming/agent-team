#!/usr/bin/env python3
"""
知识使用追踪器
追踪知识卡片使用情况
"""
import os
from pathlib import Path

KNOWLEDGE_DIR = Path.home() / ".openclaw/workspace/memory/learning/knowledge"

def track_usage():
    """追踪知识使用"""
    total = len(list(KNOWLEDGE_DIR.glob("knowledge-*.md")))
    
    # 统计已使用的知识（包含"✅ 已使用"标记）
    used = 0
    index_file = KNOWLEDGE_DIR / "INDEX.md"
    if index_file.exists():
        content = index_file.read_text()
        used = content.count("✅ 已使用")
    
    usage_rate = (used / total * 100) if total > 0 else 0
    
    print(f"📊 知识使用率: {usage_rate:.1f}% ({used}/{total})")
    print(f"目标: >60%")
    
    if usage_rate < 60:
        print(f"⚠️ 低于目标，需要提升")

if __name__ == "__main__":
    track_usage()
