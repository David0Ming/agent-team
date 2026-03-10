#!/usr/bin/env python3
"""
Agent能力测试脚本
用途：验证每个agent的基本功能是否正常
"""
from pathlib import Path

WORKSPACE_ROOT = Path.home() / ".openclaw"

def test_agent_config(agent_name: str) -> dict:
    """测试单个agent的配置"""
    workspace = WORKSPACE_ROOT / f"workspace-{agent_name}" if agent_name != "main" else WORKSPACE_ROOT / "workspace"
    
    results = {
        "agent": agent_name,
        "workspace_exists": workspace.exists(),
        "soul_exists": (workspace / "SOUL.md").exists(),
        "memory_exists": (workspace / "memory").exists(),
        "heartbeat_exists": (workspace / "HEARTBEAT.md").exists(),
        "score": 0
    }
    
    # 计算分数
    if results["workspace_exists"]: results["score"] += 25
    if results["soul_exists"]: results["score"] += 25
    if results["memory_exists"]: results["score"] += 25
    if results["heartbeat_exists"]: results["score"] += 25
    
    return results

def run_tests():
    """运行所有测试"""
    agents = ["main", "dming", "david", "copywriter", "videomaker", 
              "dplan", "dcensor", "ddebug", "dtester", "ddata", "uploader"]
    
    print("🧪 Agent能力测试开始...\n")
    
    all_results = []
    for agent in agents:
        result = test_agent_config(agent)
        all_results.append(result)
        
        status = "✅" if result["score"] == 100 else "⚠️" if result["score"] >= 75 else "❌"
        print(f"{status} {agent}: {result['score']}/100")
    
    # 总结
    avg_score = sum(r["score"] for r in all_results) / len(all_results)
    print(f"\n📊 平均分数: {avg_score:.1f}/100")
    
    if avg_score == 100:
        print("🎉 所有agent配置完美！")
    elif avg_score >= 90:
        print("👍 配置良好，有少量改进空间")
    else:
        print("⚠️ 需要优化配置")

if __name__ == "__main__":
    run_tests()
