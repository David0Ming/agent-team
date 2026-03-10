#!/usr/bin/env python3
"""
Tavily Search API Wrapper
需要环境变量: TAVILY_API_KEY
"""

import os
import sys
import json
import requests
from typing import List, Dict, Optional

def search_tavily(
    query: str,
    search_depth: str = "basic",
    max_results: int = 5,
    include_domains: Optional[List[str]] = None,
    exclude_domains: Optional[List[str]] = None
) -> Optional[List[Dict]]:
    """
    使用Tavily API搜索
    
    Args:
        query: 搜索查询
        search_depth: "basic" 或 "advanced"
        max_results: 最大结果数
        include_domains: 包含的域名列表
        exclude_domains: 排除的域名列表
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("错误: 缺少TAVILY_API_KEY环境变量", file=sys.stderr)
        print("获取API key: https://tavily.com/", file=sys.stderr)
        return None
    
    try:
        url = "https://api.tavily.com/search"
        
        payload = {
            "api_key": api_key,
            "query": query,
            "search_depth": search_depth,
            "max_results": max_results
        }
        
        if include_domains:
            payload["include_domains"] = include_domains
        if exclude_domains:
            payload["exclude_domains"] = exclude_domains
        
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("content", ""),
                "score": item.get("score", 0),
                "published_date": item.get("published_date", "")
            })
        
        return results if results else None
    
    except Exception as e:
        print(f"Tavily搜索失败: {e}", file=sys.stderr)
        return None

def main():
    if len(sys.argv) < 2:
        print("用法: python3 tavily_search.py <query> [search_depth] [max_results]")
        print("search_depth: basic (默认) 或 advanced")
        sys.exit(1)
    
    query = sys.argv[1]
    search_depth = sys.argv[2] if len(sys.argv) > 2 else "basic"
    max_results = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    
    results = search_tavily(query, search_depth, max_results)
    
    if results:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("搜索失败", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
