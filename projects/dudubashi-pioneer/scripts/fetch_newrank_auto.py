#!/usr/bin/env python3
"""使用DOM直接提取NewRank数据 - 自动化版本"""
import json
import time
import sys
from datetime import datetime
from pathlib import Path

# 依赖检查
def check_dependencies():
    """检查并安装必需依赖"""
    required = {
        'playwright': 'playwright',
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"⚠️  缺少依赖: {', '.join(missing)}")
        print("尝试安装...")
        import subprocess
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--user'] + missing, check=True)
            print("✅ 依赖安装成功")
        except subprocess.CalledProcessError:
            print("❌ 依赖安装失败，请手动安装:")
            print(f"   pip3 install --user {' '.join(missing)}")
            sys.exit(1)

check_dependencies()

from playwright.sync_api import sync_playwright

PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "competitor-data"
CONFIG_FILE = PROJECT_DIR / "config" / "newrank.json"
COOKIES_FILE = PROJECT_DIR / "newrank_cookies.json"

def load_config():
    """加载配置文件"""
    if not CONFIG_FILE.exists():
        print(f"❌ 配置文件不存在: {CONFIG_FILE}")
        print("请先创建配置文件，参考 WORKFLOW.md")
        sys.exit(1)
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def scrape_newrank(brand: str, url: str) -> dict:
    """抓取NewRank数据"""
    print(f"抓取 {brand} 数据...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        
        # 加载cookies
        if COOKIES_FILE.exists():
            with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
                context.add_cookies(cookies)
        else:
            print(f"⚠️  Cookies文件不存在: {COOKIES_FILE}")
        
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
                    
                    // 清理账号名称（移除序号和换行符）
                    const cleanName = name.replace(/^\\d+\\n/, '').replace(/\\n/g, ' ').trim();
                    
                    data.push({
                        name: cleanName,
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
    # 加载配置
    config = load_config()
    competitors = config.get('competitors', {})
    
    if not competitors:
        print("❌ 配置文件中没有竞品信息")
        sys.exit(1)
    
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = DATA_DIR / today
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for brand, info in competitors.items():
        url = info.get('url')
        if not url:
            print(f"⚠️  {brand} 没有配置URL，跳过")
            continue
        
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
