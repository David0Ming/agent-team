#!/usr/bin/env python3
"""抓取NewRank竞品数据"""
import json
import time
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "competitor-data"

COMPETITORS = {
    "小江巴士": "https://www.newrank.cn/talentlist/share?uuid=qwiswt2tu9fo",
    "熊猫哒巴士": "https://www.newrank.cn/talentlist/share?uuid=ozs697lbubnf"
}

def scrape_newrank(brand: str, url: str) -> dict:
    """抓取NewRank数据"""
    print(f"抓取 {brand} 数据...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(url, wait_until='networkidle', timeout=60000)
            time.sleep(3)
            
            # 提取账号数据
            accounts = page.evaluate('''() => {
                const rows = document.querySelectorAll('tr');
                const data = [];
                
                rows.forEach(row => {
                    const cells = row.querySelectorAll('td');
                    if (cells.length >= 5) {
                        data.push({
                            name: cells[0]?.innerText?.trim() || '',
                            platform: cells[1]?.innerText?.trim() || '',
                            fans: cells[2]?.innerText?.trim() || '-',
                            new_rank_index: parseFloat(cells[3]?.innerText?.trim()) || 0,
                            recent_works: cells[4]?.innerText?.trim() || '-',
                            recent_likes: cells[5]?.innerText?.trim() || '-'
                        });
                    }
                });
                
                return data.filter(d => d.name);
            }''')
            
            browser.close()
            
            return {
                "brand": brand,
                "total": len(accounts),
                "accounts": accounts,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"抓取失败: {e}")
            browser.close()
            return {"brand": brand, "total": 0, "accounts": [], "error": str(e)}

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = DATA_DIR / today
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_data = {}
    
    for brand, url in COMPETITORS.items():
        data = scrape_newrank(brand, url)
        all_data[brand] = data
        
        # 保存单独文件
        filename = brand.replace(" ", "_").lower() + "_detailed.json"
        with open(output_dir / filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        time.sleep(2)
    
    print(f"✅ 数据已保存到: {output_dir}")
    return all_data

if __name__ == "__main__":
    main()
