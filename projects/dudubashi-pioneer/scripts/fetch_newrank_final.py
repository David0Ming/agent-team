#!/usr/bin/env python3
"""使用完整链接抓取NewRank竞品数据"""
import json
import time
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "competitor-data"
COOKIES_FILE = PROJECT_DIR / "newrank_cookies.json"

COMPETITORS = {
    "小江巴士": "https://www.newrank.cn/talentlist/share?f=share&source=9513&keyword=drqd&l=qwiswt2tu9fo&uuid=qwiswt2tu9fo",
    "熊猫哒巴士": "https://www.newrank.cn/talentlist/share?f=share&source=9513&keyword=drqd&l=ozs697lbubnf&uuid=ozs697lbubnf"
}

def scrape_newrank(brand: str, url: str) -> dict:
    """抓取NewRank数据"""
    print(f"抓取 {brand} 数据...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        
        # 加载cookies
        if COOKIES_FILE.exists():
            with open(COOKIES_FILE, 'r') as f:
                cookies = json.load(f)
                context.add_cookies(cookies)
        
        page = context.new_page()
        
        try:
            page.goto(url, wait_until='networkidle', timeout=60000)
            time.sleep(5)
            
            # 提取账号数据
            text = page.evaluate('() => document.body.innerText')
            
            # 解析数据（从文本中提取）
            accounts = []
            lines = text.split('\n')
            
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                # 查找账号名称行（包含平台信息）
                if any(p in line for p in ['视频号', '抖音', '小红书', '快手']):
                    # 提取账号信息
                    name_parts = line.split('\t')
                    if len(name_parts) >= 2:
                        name = name_parts[0].strip()
                        if name and not name.startswith('达人名称'):
                            # 查找后续行的数据
                            try:
                                works = name_parts[1] if len(name_parts) > 1 else '-'
                                category = name_parts[2] if len(name_parts) > 2 else '-'
                                fans = name_parts[5] if len(name_parts) > 5 else '-'
                                platform = name_parts[6] if len(name_parts) > 6 else '-'
                                index_str = name_parts[7] if len(name_parts) > 7 else '0'
                                likes = name_parts[10] if len(name_parts) > 10 else '-'
                                
                                accounts.append({
                                    'name': name,
                                    'platform': platform,
                                    'fans': fans,
                                    'new_rank_index': float(index_str) if index_str.replace('.', '').isdigit() else 0,
                                    'recent_works': works,
                                    'recent_likes': likes,
                                    'category': category
                                })
                            except:
                                pass
                
                i += 1
            
            browser.close()
            
            # 统计平台分布
            platforms = {}
            for acc in accounts:
                p = acc['platform']
                platforms[p] = platforms.get(p, 0) + 1
            
            return {
                "brand": brand,
                "total": len(accounts),
                "platforms": platforms,
                "accounts": accounts,
                "data_date": datetime.now().strftime("%Y-%m-%d"),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"抓取失败: {e}")
            import traceback
            traceback.print_exc()
            browser.close()
            return {"brand": brand, "total": 0, "accounts": [], "error": str(e)}

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = DATA_DIR / today
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for brand, url in COMPETITORS.items():
        data = scrape_newrank(brand, url)
        
        # 保存文件
        filename = brand.replace(" ", "_").lower() + "_detailed.json"
        with open(output_dir / filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {brand}: {data['total']}个账号")
        time.sleep(3)
    
    print(f"\n✅ 数据已保存到: {output_dir}")

if __name__ == "__main__":
    main()
