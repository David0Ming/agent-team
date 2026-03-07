#!/usr/bin/env python3
"""
竞品数据抓取 - Playwright版本
尝试抓取小红书/抖音/视频号的公开数据
"""

import json

from playwright.sync_api import sync_playwright


def crawl_xiaohongshu(keyword):
    """抓取小红书公开数据"""
    print(f"尝试抓取小红书: {keyword}")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # 访问小红书搜索页
            page.goto(f"https://www.xiaohongshu.com/search_result?keyword={keyword}", timeout=15000)
            page.wait_for_load_state("networkidle", timeout=10000)

            # 获取页面内容
            content = page.content()
            browser.close()

            # 简单解析 - 提取视频/笔记数量
            # 由于需要登录，这里可能只能获取到登录页面
            return {"status": "login_required", "content": content[:500]}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def crawl_douyin(keyword):
    """抓取抖音公开数据"""
    print(f"尝试抓取抖音: {keyword}")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # 抖音搜索页面
            page.goto(f"https://www.douyin.com/search/{keyword}", timeout=15000)
            page.wait_for_load_state("networkidle", timeout=10000)

            content = page.content()
            browser.close()

            return {"status": "success", "content": content[:1000]}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def main():
    competitors = ["小江巴士", "熊猫哒巴士"]
    results = {}

    for comp in competitors:
        print(f"\n=== 抓取 {comp} ===")
        result = {}

        # 尝试小红书
        xhs = crawl_xiaohongshu(comp)
        result["小红书"] = xhs

        # 尝试抖音
        dy = crawl_douyin(comp)
        result["抖音"] = dy

        results[comp] = result

    # 保存结果
    with open("/tmp/competitor_test.json", "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n结果已保存到 /tmp/competitor_test.json")

if __name__ == "__main__":
    main()
