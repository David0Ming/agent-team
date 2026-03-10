#!/usr/bin/env python3
"""生成飞书文档格式的竞品报告（无表格）"""
import json
from pathlib import Path
from datetime import datetime

def load_competitor_data(date_str):
    base_path = Path(__file__).parent.parent / "competitor-data" / date_str
    data = {}
    for file in ["xiaojiang_bus_detailed.json", "panda_bus_detailed.json"]:
        file_path = base_path / file
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                brand_data = json.load(f)
                data[brand_data['brand']] = brand_data
    return data

def generate_feishu_report(data, date_str):
    md = f"# 竞品分析报告\n\n**数据日期**: {date_str}\n\n---\n\n"
    
    # 概览
    md += "## 📊 概览对比\n\n"
    for brand, brand_data in data.items():
        platforms = brand_data.get('platforms', {})
        platform_str = "、".join([f"{k}({v}个)" for k, v in platforms.items()])
        md += f"**{brand}**\n- 总账号数：{brand_data['total']}\n- 平台分布：{platform_str}\n\n"
    
    # TOP账号
    md += "## 🏆 TOP 10 账号排行\n\n"
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
    
    for idx, acc in enumerate(top_accounts, 1):
        md += f"**{idx}. {acc['name']}** ({acc['brand']})\n"
        md += f"- 平台：{acc['platform']}\n"
        md += f"- 粉丝：{acc['fans']}\n"
        md += f"- NewRank指数：{acc['index']:.1f}\n"
        md += f"- 近期点赞：{acc['likes']}\n\n"
    
    # 详细分析
    for brand, brand_data in data.items():
        md += f"## 📱 {brand}\n\n"
        
        insights = brand_data.get('insights', {})
        if insights:
            md += "### 内容策略\n"
            md += f"- **主要平台**：{insights.get('main_platform', '-')}\n"
            md += f"- **内容类别**：{', '.join(insights.get('content_categories', []))}\n"
            md += f"- **关键主题**：{', '.join(insights.get('key_themes', []))}\n"
            md += f"- **内容风格**：{insights.get('content_style', '-')}\n"
            md += f"- **发布频率**：{insights.get('posting_frequency', '-')}\n\n"
        
        md += f"### 账号矩阵（共{brand_data['total']}个）\n\n"
        
        # 按平台分组
        accounts_by_platform = {}
        for acc in brand_data.get('accounts', []):
            platform = acc.get('platform', '其他')
            if platform not in accounts_by_platform:
                accounts_by_platform[platform] = []
            accounts_by_platform[platform].append(acc)
        
        for platform, accounts in accounts_by_platform.items():
            md += f"**{platform}平台**（{len(accounts)}个账号）\n"
            for acc in sorted(accounts, key=lambda x: x.get('new_rank_index', 0), reverse=True)[:5]:
                md += f"- {acc['name']}：指数{acc.get('new_rank_index', 0):.1f}"
                if acc.get('fans') and acc['fans'] != '-':
                    md += f"，粉丝{acc['fans']}"
                md += "\n"
            if len(accounts) > 5:
                md += f"- ...还有{len(accounts)-5}个账号\n"
            md += "\n"
    
    return md

def main():
    date_str = datetime.now().strftime('%Y-%m-%d')
    data = load_competitor_data(date_str)
    if not data:
        date_str = "2026-03-05"
        data = load_competitor_data(date_str)
    
    if not data:
        print("❌ 没有找到竞品数据")
        return None
    
    report = generate_feishu_report(data, date_str)
    
    output_path = Path(__file__).parent.parent / "competitor-data" / date_str / "feishu_report.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 飞书报告已生成: {output_path}")
    print(f"📝 报告长度: {len(report)} 字符")
    return output_path, report

if __name__ == "__main__":
    main()
