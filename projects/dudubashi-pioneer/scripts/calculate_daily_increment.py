#!/usr/bin/env python3
"""计算竞品单日增量数据"""
import json
from pathlib import Path
from datetime import datetime, timedelta

PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "competitor-data"

def load_data(date_str):
    """加载指定日期的数据"""
    data_file = DATA_DIR / date_str / "xiaojiangbus_detailed.json"
    if not data_file.exists():
        return None
    with open(data_file) as f:
        return json.load(f)

def calculate_increment(yesterday_data, today_data):
    """计算单日增量"""
    if not yesterday_data or not today_data:
        return None
    
    # 按账号名建立索引
    yesterday_accounts = {acc["name"]: acc for acc in yesterday_data["accounts"]}
    today_accounts = {acc["name"]: acc for acc in today_data["accounts"]}
    
    increments = []
    for name, today_acc in today_accounts.items():
        yesterday_acc = yesterday_accounts.get(name)
        if not yesterday_acc:
            continue
        
        # 计算增量
        try:
            today_works = int(today_acc.get("recent_works", "0") or "0")
            yesterday_works = int(yesterday_acc.get("recent_works", "0") or "0")
            works_increment = today_works - yesterday_works
            
            today_likes = int(str(today_acc.get("recent_likes", "0") or "0").replace("-", "0"))
            yesterday_likes = int(str(yesterday_acc.get("recent_likes", "0") or "0").replace("-", "0"))
            likes_increment = today_likes - yesterday_likes
            
            if works_increment > 0 or likes_increment > 0:
                increments.append({
                    "name": name,
                    "platform": today_acc["platform"],
                    "works_increment": works_increment,
                    "likes_increment": likes_increment
                })
        except:
            continue
    
    return increments

# 计算昨天的增量
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
today = datetime.now().strftime("%Y-%m-%d")

yesterday_data = load_data(yesterday)
today_data = load_data(today)

if yesterday_data and today_data:
    increments = calculate_increment(yesterday_data, today_data)
    
    print(f"# 竞品单日增量报告 - {yesterday}")
    print(f"\n## 小江巴士")
    print(f"\n| 账号名 | 平台 | 新增作品 | 新增点赞 |")
    print(f"|--------|------|----------|----------|")
    
    for inc in sorted(increments, key=lambda x: x["likes_increment"], reverse=True):
        if inc["works_increment"] > 0 or inc["likes_increment"] > 0:
            print(f"| {inc['name']} | {inc['platform']} | {inc['works_increment']} | {inc['likes_increment']} |")
    
    # 统计总计
    total_works = sum(inc["works_increment"] for inc in increments)
    total_likes = sum(inc["likes_increment"] for inc in increments)
    print(f"\n**总计**: 新增作品 {total_works} 条，新增点赞 {total_likes} 个")
else:
    print("数据不完整，无法计算增量")
