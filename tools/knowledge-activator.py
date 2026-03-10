#!/usr/bin/env python3
"""
知识自动激活脚本
根据任务类型自动激活相关知识
"""

KNOWLEDGE_MAP = {
    "性能": ["performance-optimization", "cache-penetration", "async-batch"],
    "Agent": ["agent-debugging", "agent-memory", "agent-efficiency"],
    "API": ["resilient-api", "robust-error-handling", "robust-http"],
    "分布式": ["circuit-breaker", "fault-tolerance", "distributed-tracing"],
}

def activate_knowledge(task_description):
    """根据任务描述激活相关知识"""
    activated = []
    for keyword, knowledge_list in KNOWLEDGE_MAP.items():
        if keyword in task_description:
            activated.extend(knowledge_list)
    return activated

if __name__ == "__main__":
    print("知识自动激活脚本已就绪")
