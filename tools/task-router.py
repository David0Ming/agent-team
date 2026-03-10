#!/usr/bin/env python3
"""
快速任务分配工具
用途：根据任务类型自动推荐合适的agent
"""

AGENT_CAPABILITIES = {
    "DJJ": ["产品规划", "需求分析", "优先级决策", "团队协调"],
    "DMing": ["技术架构", "代码审查", "性能优化", "技术选型"],
    "David": ["内容运营", "社交媒体", "品牌推广", "用户增长"],
    "Copywriter": ["文案撰写", "Prompt生成", "营销文案", "技术文档"],
    "Videomaker": ["视频制作", "视觉设计", "剪辑优化", "平台适配"],
    "Dplan": ["系统设计", "架构规划", "技术方案"],
    "Dcensor": ["代码审查", "质量把关", "安全检查"],
    "Ddebug": ["问题诊断", "Bug修复", "性能调优"],
    "Dtester": ["测试设计", "质量保证", "自动化测试"],
    "Ddata": ["数据分析", "报表生成", "指标监控"],
    "Uploader": ["文件上传", "资源管理", "平台发布"]
}

def recommend_agent(task_description: str) -> list:
    """根据任务描述推荐合适的agent"""
    recommendations = []
    
    task_lower = task_description.lower()
    
    for agent, capabilities in AGENT_CAPABILITIES.items():
        score = 0
        matched_caps = []
        
        for cap in capabilities:
            if cap in task_description or any(word in task_lower for word in cap.lower().split()):
                score += 1
                matched_caps.append(cap)
        
        if score > 0:
            recommendations.append({
                "agent": agent,
                "score": score,
                "matched_capabilities": matched_caps
            })
    
    return sorted(recommendations, key=lambda x: x["score"], reverse=True)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 task-router.py '任务描述'")
        sys.exit(1)
    
    task = " ".join(sys.argv[1:])
    print(f"📋 任务: {task}\n")
    
    recommendations = recommend_agent(task)
    
    if recommendations:
        print("🎯 推荐的Agent:")
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"{i}. {rec['agent']} (匹配度: {rec['score']})")
            print(f"   匹配能力: {', '.join(rec['matched_capabilities'])}")
    else:
        print("⚠️  未找到匹配的Agent，建议由DJJ协调")
