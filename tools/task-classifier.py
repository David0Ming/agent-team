#!/usr/bin/env python3
"""
任务分类器
自动判断任务类型和执行模式
"""

def classify_task(task_description):
    """分类任务"""
    # 简单规则判断
    keywords_quick = ["查看", "检查", "显示", "列出"]
    keywords_complex = ["开发", "设计", "优化", "重构"]
    
    for kw in keywords_quick:
        if kw in task_description:
            return "快速任务", "直接执行"
    
    for kw in keywords_complex:
        if kw in task_description:
            return "复杂任务", "详细计划"
    
    return "标准任务", "确认需求"

if __name__ == "__main__":
    print("任务分类器已就绪")
