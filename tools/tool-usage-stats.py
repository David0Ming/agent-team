#!/usr/bin/env python3
"""
工具使用统计
用途：追踪工具使用频率，识别常用/冷门工具
"""
import os
from pathlib import Path
from datetime import datetime

TOOLS_DIR = Path.home() / ".openclaw/workspace/tools"

def analyze_tool_usage():
    """分析工具使用情况"""
    print("📊 工具使用统计\n")
    
    tools = []
    for file in TOOLS_DIR.glob("*"):
        if file.is_file() and file.suffix in [".sh", ".py"]:
            stat = file.stat()
            tools.append({
                "name": file.name,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime),
                "executable": os.access(file, os.X_OK)
            })
    
    # 按修改时间排序
    tools.sort(key=lambda x: x["modified"], reverse=True)
    
    print(f"总工具数: {len(tools)}\n")
    print("最近使用的工具:")
    for tool in tools[:5]:
        print(f"  - {tool['name']}: {tool['modified'].strftime('%Y-%m-%d %H:%M')}")
    
    # 统计可执行工具
    executable_count = sum(1 for t in tools if t["executable"])
    print(f"\n可执行工具: {executable_count}/{len(tools)}")

if __name__ == "__main__":
    analyze_tool_usage()
