#!/usr/bin/env python3
"""
知识库维护脚本
用途：检查未使用的知识卡片，清理过期内容
"""
import os
from datetime import datetime, timedelta
from pathlib import Path

KNOWLEDGE_DIR = Path.home() / ".openclaw/workspace/memory/learning/knowledge"
DAYS_THRESHOLD = 30

def check_unused_knowledge():
    """检查超过30天未使用的知识卡片"""
    print("🔍 检查未使用的知识卡片...")
    
    if not KNOWLEDGE_DIR.exists():
        print("❌ 知识库目录不存在")
        return
    
    unused = []
    now = datetime.now()
    
    for file in KNOWLEDGE_DIR.glob("knowledge-*.md"):
        if file.name == "knowledge-template.md":
            continue
            
        mtime = datetime.fromtimestamp(file.stat().st_mtime)
        days_old = (now - mtime).days
        
        if days_old > DAYS_THRESHOLD:
            unused.append((file.name, days_old))
    
    if unused:
        print(f"\n⚠️  发现 {len(unused)} 个超过{DAYS_THRESHOLD}天未使用的知识卡片：")
        for name, days in sorted(unused, key=lambda x: x[1], reverse=True):
            print(f"  - {name} ({days}天未使用)")
    else:
        print(f"✅ 所有知识卡片都在{DAYS_THRESHOLD}天内使用过")

if __name__ == "__main__":
    check_unused_knowledge()
