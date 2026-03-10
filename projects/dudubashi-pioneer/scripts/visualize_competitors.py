#!/usr/bin/env python3
"""竞品数据可视化脚本"""
import json
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
from datetime import datetime

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

def load_competitor_data(date_str):
    """加载指定日期的竞品数据"""
    base_path = Path(__file__).parent.parent / "competitor-data" / date_str
    
    data = {}
    # 支持新旧文件名格式
    file_patterns = [
        ["xiaojiangbus_detailed.json", "pandabus_detailed.json"],
        ["xiaojiang_bus_detailed.json", "panda_bus_detailed.json"]
    ]
    
    for patterns in file_patterns:
        for file in patterns:
            file_path = base_path / file
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    brand_data = json.load(f)
                    data[brand_data['brand']] = brand_data
        
        if data:  # 如果找到数据就停止
            break
    
    return data

def create_platform_distribution_chart(data, output_path):
    """创建平台分布图"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    for idx, (brand, brand_data) in enumerate(data.items()):
        platforms = brand_data.get('platforms', {})
        axes[idx].pie(platforms.values(), labels=platforms.keys(), autopct='%1.1f%%')
        axes[idx].set_title(f'{brand} 平台分布')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

def create_account_comparison_chart(data, output_path):
    """创建账号数量对比图"""
    brands = list(data.keys())
    totals = [data[brand]['total'] for brand in brands]
    
    plt.figure(figsize=(8, 6))
    plt.bar(brands, totals, color=['#FF6B6B', '#4ECDC4'])
    plt.title('竞品账号数量对比', fontsize=14, fontweight='bold')
    plt.ylabel('账号数量')
    plt.grid(axis='y', alpha=0.3)
    
    for i, v in enumerate(totals):
        plt.text(i, v + 0.5, str(v), ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

def create_top_accounts_chart(data, output_path):
    """创建TOP账号排行"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    all_accounts = []
    for brand, brand_data in data.items():
        for acc in brand_data.get('accounts', []):
            all_accounts.append({
                'name': acc['name'],
                'brand': brand,
                'index': acc.get('new_rank_index', 0),
                'platform': acc.get('platform', '')
            })
    
    # 按指数排序，取TOP10
    top_accounts = sorted(all_accounts, key=lambda x: x['index'], reverse=True)[:10]
    
    names = [f"{acc['name']}\n({acc['platform']})" for acc in top_accounts]
    indices = [acc['index'] for acc in top_accounts]
    colors = ['#FF6B6B' if acc['brand'] == '小江巴士' else '#4ECDC4' for acc in top_accounts]
    
    ax.barh(names, indices, color=colors)
    ax.set_xlabel('NewRank指数')
    ax.set_title('TOP 10 账号排行', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

def main():
    # 使用最新日期
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    # 尝试加载今天的数据，如果没有则用昨天的
    data = load_competitor_data(date_str)
    if not data:
        date_str = "2026-03-05"  # fallback
        data = load_competitor_data(date_str)
    
    if not data:
        print("❌ 没有找到竞品数据")
        return
    
    # 创建输出目录
    output_dir = Path(__file__).parent.parent / "competitor-data" / date_str / "charts"
    output_dir.mkdir(exist_ok=True)
    
    # 生成图表
    print("📊 生成平台分布图...")
    create_platform_distribution_chart(data, output_dir / "platform_distribution.png")
    
    print("📊 生成账号数量对比图...")
    create_account_comparison_chart(data, output_dir / "account_comparison.png")
    
    print("📊 生成TOP账号排行...")
    create_top_accounts_chart(data, output_dir / "top_accounts.png")
    
    print(f"✅ 图表已生成到: {output_dir}")
    return output_dir

if __name__ == "__main__":
    main()
