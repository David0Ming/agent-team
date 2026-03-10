#!/usr/bin/env python3
"""
智能任务路由工具 v2
用途：使用语义匹配推荐合适的agent
"""

AGENT_PROFILES = {
    "DJJ": {
        "keywords": ["产品", "规划", "需求", "决策", "优先级", "协调", "团队", "方案"],
        "capabilities": ["产品规划", "需求分析", "优先级决策", "团队协调"]
    },
    "DMing": {
        "keywords": ["技术", "架构", "代码", "性能", "优化", "开发", "系统", "方案"],
        "capabilities": ["技术架构", "代码审查", "性能优化", "技术选型"]
    },
    "David": {
        "keywords": ["运营", "推广", "内容", "营销", "社交", "用户", "品牌", "增长"],
        "capabilities": ["内容运营", "社交媒体", "品牌推广", "用户增长"]
    },
    "Copywriter": {
        "keywords": ["文案", "写作", "脚本", "prompt", "营销", "文档", "内容"],
        "capabilities": ["文案创作", "Prompt工程", "营销文案", "技术文档"]
    },
    "Videomaker": {
        "keywords": ["视频", "制作", "剪辑", "视觉", "设计", "画面", "镜头"],
        "capabilities": ["视频制作", "视觉设计", "剪辑优化", "平台适配"]
    },
    "Dplan": {
        "keywords": ["设计", "架构", "系统", "方案", "规划"],
        "capabilities": ["系统设计", "架构规划", "技术方案"]
    },
    "Dcensor": {
        "keywords": ["审查", "检查", "质量", "规范", "安全"],
        "capabilities": ["代码审查", "质量把关", "安全检查"]
    },
    "Ddebug": {
        "keywords": ["调试", "bug", "问题", "修复", "错误", "排查"],
        "capabilities": ["问题诊断", "Bug修复", "性能调优"]
    },
    "Dtester": {
        "keywords": ["测试", "质量", "用例", "自动化", "验证"],
        "capabilities": ["测试设计", "质量保证", "自动化测试"]
    },
    "Ddata": {
        "keywords": ["数据", "分析", "统计", "报表", "可视化", "爬虫"],
        "capabilities": ["数据分析", "可视化", "数据采集"]
    },
    "Uploader": {
        "keywords": ["上传", "发布", "平台", "资源", "管理"],
        "capabilities": ["平台发布", "资源管理", "格式适配"]
    }
}

def recommend_agent(task: str) -> list:
    """智能推荐agent"""
    task_lower = task.lower()
    recommendations = []
    
    for agent, profile in AGENT_PROFILES.items():
        score = 0
        matched = []
        
        # 关键词匹配
        for keyword in profile["keywords"]:
            if keyword in task_lower:
                score += 2
                matched.append(keyword)
        
        # 能力匹配
        for cap in profile["capabilities"]:
            if any(word in task_lower for word in cap.lower().split()):
                score += 1
        
        if score > 0:
            recommendations.append({
                "agent": agent,
                "score": score,
                "matched": matched,
                "capabilities": profile["capabilities"]
            })
    
    return sorted(recommendations, key=lambda x: x["score"], reverse=True)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 task-router-v2.py '任务描述'")
        sys.exit(1)
    
    task = " ".join(sys.argv[1:])
    print(f"📋 任务: {task}\n")
    
    recommendations = recommend_agent(task)
    
    if recommendations:
        print("🎯 推荐的Agent:")
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"\n{i}. {rec['agent']} (匹配度: {rec['score']})")
            if rec['matched']:
                print(f"   匹配关键词: {', '.join(rec['matched'])}")
            print(f"   核心能力: {', '.join(rec['capabilities'][:2])}")
    else:
        print("⚠️  未找到匹配的Agent，建议由DJJ协调")
