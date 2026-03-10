#!/usr/bin/env python3
"""竞品深度分析 - 基于单日增量数据"""
import json
from pathlib import Path
from datetime import datetime, timedelta

PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "competitor-data"

def load_data(date_str, brand="xiaojiangbus"):
    """加载指定日期的数据"""
    data_file = DATA_DIR / date_str / f"{brand}_detailed.json"
    if not data_file.exists():
        return None
    with open(data_file) as f:
        return json.load(f)

def analyze_daily_increment():
    """深度分析昨天的单日增量"""
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d")
    
    yesterday_data = load_data(yesterday)
    today_data = load_data(today)
    
    if not yesterday_data or not today_data:
        print("数据不完整")
        return
    
    # 建立账号索引
    yesterday_accounts = {acc["name"]: acc for acc in yesterday_data["accounts"]}
    today_accounts = {acc["name"]: acc for acc in today_data["accounts"]}
    
    # 收集增量数据
    increments = []
    for name, today_acc in today_accounts.items():
        yesterday_acc = yesterday_accounts.get(name)
        if not yesterday_acc:
            continue
        
        try:
            today_works = int(today_acc.get("recent_works", "0") or "0")
            yesterday_works = int(yesterday_acc.get("recent_works", "0") or "0")
            works_inc = today_works - yesterday_works
            
            today_likes = int(str(today_acc.get("recent_likes", "0") or "0").replace("-", "0"))
            yesterday_likes = int(str(yesterday_acc.get("recent_likes", "0") or "0").replace("-", "0"))
            likes_inc = today_likes - yesterday_likes
            
            # 计算互动率
            engagement_rate = likes_inc / works_inc if works_inc > 0 else 0
            
            increments.append({
                "name": name,
                "platform": today_acc["platform"],
                "works_inc": works_inc,
                "likes_inc": likes_inc,
                "engagement_rate": engagement_rate,
                "fans": today_acc.get("fans", "-"),
                "new_rank_index": today_acc.get("new_rank_index", 0)
            })
        except:
            continue
    
    return increments, yesterday

# 执行分析
increments, date = analyze_daily_increment()

if increments:
    print(f"# 竞品深度分析报告 - {date}")
    print(f"\n生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. 总体数据
    total_works = sum(inc["works_inc"] for inc in increments if inc["works_inc"] > 0)
    total_likes = sum(inc["likes_inc"] for inc in increments if inc["likes_inc"] > 0)
    active_accounts = len([inc for inc in increments if inc["works_inc"] > 0])
    
    print(f"\n## 📊 总体数据（{date}单日）")
    print(f"\n- **新增作品**：{total_works} 条")
    print(f"- **新增点赞**：{total_likes} 个")
    print(f"- **活跃账号**：{active_accounts} 个")
    print(f"- **平均互动率**：{total_likes/total_works if total_works > 0 else 0:.1f} 点赞/作品")
    
    # 2. TOP账号表现
    print(f"\n## 🏆 TOP账号表现")
    print(f"\n### 按点赞增量排序")
    print(f"\n| 账号名 | 平台 | 新增作品 | 新增点赞 | 互动率 |")
    print(f"|--------|------|----------|----------|--------|")
    
    top_by_likes = sorted([inc for inc in increments if inc["likes_inc"] > 0], 
                          key=lambda x: x["likes_inc"], reverse=True)[:5]
    for inc in top_by_likes:
        print(f"| {inc['name']} | {inc['platform']} | {inc['works_inc']} | {inc['likes_inc']} | {inc['engagement_rate']:.1f} |")
    
    # 3. 平台对比
    print(f"\n## 📱 平台表现对比")
    
    platforms = {}
    for inc in increments:
        platform = inc["platform"]
        if platform not in platforms:
            platforms[platform] = {"works": 0, "likes": 0, "accounts": 0}
        if inc["works_inc"] > 0:
            platforms[platform]["works"] += inc["works_inc"]
            platforms[platform]["likes"] += inc["likes_inc"]
            platforms[platform]["accounts"] += 1
    
    print(f"\n| 平台 | 活跃账号 | 新增作品 | 新增点赞 | 平均互动率 |")
    print(f"|------|----------|----------|----------|------------|")
    for platform, data in sorted(platforms.items(), key=lambda x: x[1]["likes"], reverse=True):
        avg_rate = data["likes"] / data["works"] if data["works"] > 0 else 0
        print(f"| {platform} | {data['accounts']} | {data['works']} | {data['likes']} | {avg_rate:.1f} |")
    
    # 4. 账号矩阵策略分析
    print(f"\n## 🎯 账号矩阵策略洞察")
    
    # 高产账号
    high_output = [inc for inc in increments if inc["works_inc"] >= 3]
    print(f"\n### 高产账号（≥3条/天）")
    if high_output:
        for inc in sorted(high_output, key=lambda x: x["works_inc"], reverse=True):
            print(f"- **{inc['name']}**（{inc['platform']}）：{inc['works_inc']}条作品，{inc['likes_inc']}点赞")
    else:
        print("- 无")
    
    # 高互动账号
    high_engagement = [inc for inc in increments if inc["engagement_rate"] >= 200 and inc["works_inc"] > 0]
    print(f"\n### 高互动账号（≥200点赞/作品）")
    if high_engagement:
        for inc in sorted(high_engagement, key=lambda x: x["engagement_rate"], reverse=True):
            print(f"- **{inc['name']}**（{inc['platform']}）：互动率{inc['engagement_rate']:.0f}，{inc['works_inc']}条作品")
    else:
        print("- 无")
    
    # 5. 差异化机会
    print(f"\n## 💡 差异化机会分析")
    print(f"\n### 小江巴士的优势")
    print(f"1. **账号矩阵规模**：15个账号，多平台布局（抖音+视频号+小红书）")
    print(f"2. **高产能力**：单日{total_works}条作品，保持高频更新")
    print(f"3. **平台策略**：{'抖音' if platforms.get('抖音', {}).get('likes', 0) > platforms.get('视频号', {}).get('likes', 0) else '视频号'}表现更好")
    
    print(f"\n### 嘟嘟巴士的机会")
    avg_engagement = total_likes / total_works if total_works > 0 else 0
    print(f"1. **内容质量**：小江平均互动率{avg_engagement:.1f}，我们可以通过更精品化的内容提升互动率")
    print(f"2. **视觉差异**：强化'红色巴士'视觉符号，与小江的黄色形成对比")
    print(f"3. **场景化内容**：深中通道、通勤、亲子游等场景化内容，而非单纯的司机人设")
    print(f"4. **平台选择**：重点布局表现更好的{'抖音' if platforms.get('抖音', {}).get('likes', 0) > platforms.get('视频号', {}).get('likes', 0) else '视频号'}平台")
    
    # 6. 行动建议
    print(f"\n## 🚀 行动建议")
    print(f"\n### 短期（本周）")
    print(f"1. 测试3条高质量prompt（深中通道、春招通勤、周末亲子）")
    print(f"2. 重点投放{'抖音' if platforms.get('抖音', {}).get('likes', 0) > platforms.get('视频号', {}).get('likes', 0) else '视频号'}平台")
    print(f"3. 目标互动率：≥{avg_engagement * 1.5:.0f}点赞/作品（比小江高50%）")
    
    print(f"\n### 中期（本月）")
    print(f"1. 建立2-3个核心账号（司机人设+场景化内容）")
    print(f"2. 每日更新频率：2-3条（保证质量）")
    print(f"3. 数据追踪：每日对比小江的增量数据")
    
    print(f"\n### 长期（季度）")
    print(f"1. 形成差异化的内容风格（红色巴士+大湾区场景）")
    print(f"2. 建立账号矩阵（5-8个账号）")
    print(f"3. 目标：单账号粉丝≥2万，互动率≥300")
