#!/usr/bin/env python3
"""
Agent性能基准测试
用途：建立性能基线，追踪性能变化
"""
import time
from pathlib import Path

def test_file_operations():
    """测试文件操作性能"""
    start = time.time()
    
    # 测试读取
    test_file = Path.home() / ".openclaw/workspace/SOUL.md"
    if test_file.exists():
        content = test_file.read_text()
    
    duration = time.time() - start
    return {"operation": "file_read", "duration": duration}

def test_command_execution():
    """测试命令执行性能"""
    import subprocess
    start = time.time()
    
    subprocess.run(["echo", "test"], capture_output=True)
    
    duration = time.time() - start
    return {"operation": "command_exec", "duration": duration}

def run_benchmark():
    """运行基准测试"""
    print("🏃 Agent性能基准测试\n")
    
    results = []
    
    # 文件操作测试
    result = test_file_operations()
    results.append(result)
    print(f"✅ 文件读取: {result['duration']:.4f}s")
    
    # 命令执行测试
    result = test_command_execution()
    results.append(result)
    print(f"✅ 命令执行: {result['duration']:.4f}s")
    
    print(f"\n📊 总测试项: {len(results)}")

if __name__ == "__main__":
    run_benchmark()
