#!/usr/bin/env python3
"""生成竞品分析报告（Markdown格式）"""
import json
from pathlib import Path
from datetime import datetime

def load_competitor_data(date_str):
    """加载指定日期的竞品数据"""
    base_path = Path(__file__).parent.parent / "competitor-data" / date_str
    
    data = {}
    for file in ["xiaojiangbus_detailed.json", "pandabus_detailed.json", "xiaojiang_bus_detailed.json", "panda_bus_detailed.json"]:
        file_path = base_path / file
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                brand_data = json.load(f)
                data[brand_data['brand']] = brand_data
    
    return data

def generate_markdown_report(data, date_str):
    """生成Markdown格式报告"""
    md = f"# 竞品分析报告\n\n"
    md += f"**数据日期**: {date_str}\n\n"
    
    # 概览
    md += "## 📊 概览\n\n"
    for brand, brand_data in data.items():
        md += f"### {brand}\n"
        md += f"- **总账号数**: {brand_data['total']}\n"
        md += f"- **平台分布**: "
        platforms = brand_data.get('platforms', {})
        md += ", ".join([f"{k}({v}个)" for k, v in platforms.items()])
        md += "\n\n"
    
    # TOP账号
    md += "## 🏆 TOP 10 账号（按NewRank指数）\n\n"
    
    all_accounts = []
    for brand, brand_data in data.items():
        for acc in brand_data.get('accounts', []):
            all_accounts.append({
                'name': acc['name'],
                'brand': brand,
                'platform': acc.get('platform', ''),
                'fans': acc.get('fans', '-'),
                'index': acc.get('new_rank_index', 0),
                'likes': acc.get('recent_likes', '-')
            })
    
    top_accounts = sorted(all_accounts, key=lambda x: x['index'], reverse=True)[:10]
    
    md += "| 排名 | 账号名 | 品牌 | 平台 | 粉丝数 | NewRank指数 | 近期点赞 |\n"
    md += "|------|--------|------|------|--------|-------------|----------|\n"
    
    for idx, acc in enumerate(top_accounts, 1):
        md += f"| {idx} | {acc['name']} | {acc['brand']} | {acc['platform']} | {acc['fans']} | {acc['index']:.1f} | {acc['likes']} |\n"
    
    md += "\n"
    
    # 详细账号列表
    for brand, brand_data in data.items():
        md += f"## 📱 {brand} 详细账号列表\n\n"
        
        accounts = brand_data.get('accounts', [])
        if accounts:
            md += "| 账号名 | 平台 | 粉丝数 | NewRank指数 | 近期作品 | 近期点赞 |\n"
            md += "|--------|------|--------|-------------|----------|----------|\n"
            
            for acc in accounts:
                md += f"| {acc['name']} | {acc['platform']} | {acc.get('fans', '-')} | "
                md += f"{acc.get('new_rank_index', 0):.1f} | {acc.get('recent_works', '-')} | "
                md += f"{acc.get('recent_likes', '-')} |\n"
        
        md += "\n"
        
        # 洞察
        insights = brand_data.get('insights', {})
        if insights:
            md += f"### 💡 {brand} 内容洞察\n\n"
            md += f"- **主要平台**: {insights.get('main_platform', '-')}\n"
            md += f"- **内容类别**: {', '.join(insights.get('content_categories', []))}\n"
            md += f"- **关键主题**: {', '.join(insights.get('key_themes', []))}\n"
            md += f"- **内容风格**: {insights.get('content_style', '-')}\n"
            md += f"- **发布频率**: {insights.get('posting_frequency', '-')}\n\n"
    
    return md

def main():
    # 使用最新日期
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    # 尝试加载今天的数据，如果没有则用最近的
    data = load_competitor_data(date_str)
    if not data:
        date_str = "2026-03-05"
        data = load_competitor_data(date_str)
    
    if not data:
        print("❌ 没有找到竞品数据")
        return None
    
    # 生成报告
    report = generate_markdown_report(data, date_str)
    
    # 保存到文件
    output_path = Path(__file__).parent.parent / "competitor-data" / date_str / "report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 报告已生成: {output_path}")
    return output_path, report

if __name__ == "__main__":
    main()
