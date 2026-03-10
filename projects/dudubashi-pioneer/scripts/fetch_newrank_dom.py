#!/usr/bin/env python3
"""使用DOM直接提取NewRank数据"""
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
            
            # 使用JavaScript直接提取表格数据
            accounts = page.evaluate('''() => {
                const rows = Array.from(document.querySelectorAll('table tbody tr'));
                const data = [];
                
                for (const row of rows) {
                    const cells = Array.from(row.querySelectorAll('td'));
                    if (cells.length < 10) continue;
                    
                    const name = cells[0]?.innerText?.trim() || '';
                    if (!name || name === '达人名称') continue;
                    
                    data.push({
                        name: name,
                        recent_works: cells[1]?.innerText?.trim() || '-',
                        category: cells[2]?.innerText?.trim() || '-',
                        fans: cells[5]?.innerText?.trim() || '-',
                        platform: cells[6]?.innerText?.trim() || '-',
                        new_rank_index: parseFloat(cells[7]?.innerText?.trim()) || 0,
                        region: cells[8]?.innerText?.trim() || '-',
                        recent_likes: cells[10]?.innerText?.trim() || '-'
                    });
                }
                
                return data;
            }''')
            
            browser.close()
            
            # 统计平台分布
            platforms = {}
            for acc in accounts:
                p = acc['platform']
                platforms[p] = platforms.get(p, 0) + 1
            
            return {
                "brand": brand,
                "list_id": url.split('uuid=')[1].split('&')[0] if 'uuid=' in url else '',
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
        filename = brand.replace("巴士", "bus").replace("小江", "xiaojiang").replace("熊猫哒", "panda") + "_detailed.json"
        with open(output_dir / filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {brand}: {data['total']}个账号")
        time.sleep(3)
    
    print(f"\n✅ 数据已保存到: {output_dir}")

if __name__ == "__main__":
    main()
