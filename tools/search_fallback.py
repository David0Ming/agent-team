#!/usr/bin/env python3
"""
搜索API Fallback链：Tavily > SerpAPI > Serper > DuckDuckGo
"""

import os
import sys
import json
import requests
from typing import List, Dict, Optional

def search_tavily(query: str, num_results: int = 5) -> Optional[List[Dict]]:
    """使用Tavily搜索"""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return None
    
    try:
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": api_key,
            "query": query,
            "search_depth": "basic",
            "max_results": num_results
        }
        
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("content", "")[:200]
            })
        
        return results if results else None
    
    except Exception as e:
        print(f"Tavily失败: {e}", file=sys.stderr)
        return None

def search_serpapi(query: str, num_results: int = 5) -> Optional[List[Dict]]:
    """使用SerpAPI搜索"""
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        return None
    
    try:
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": api_key,
            "num": num_results
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("organic_results", [])[:num_results]:
            results.append({
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", "")
            })
        
        return results if results else None
    
    except Exception as e:
        print(f"SerpAPI失败: {e}", file=sys.stderr)
        return None

def search_serper(query: str, num_results: int = 5) -> Optional[List[Dict]]:
    """使用Serper搜索"""
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        return None
    
    try:
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "num": num_results
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("organic", [])[:num_results]:
            results.append({
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", "")
            })
        
        return results if results else None
    
    except Exception as e:
        print(f"Serper失败: {e}", file=sys.stderr)
        return None

def search_duckduckgo(query: str, num_results: int = 5) -> Optional[List[Dict]]:
    """使用DuckDuckGo搜索（免费）"""
    try:
        from ddgs import DDGS
        
        results = []
        ddgs = DDGS()
        for r in ddgs.text(query, max_results=num_results):
            results.append({
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", "")
            })
        
        return results if results else None
    
    except Exception as e:
        print(f"DuckDuckGo失败: {e}", file=sys.stderr)
        return None

def search(query: str, num_results: int = 5) -> List[Dict]:
    """
    搜索fallback链：Tavily > SerpAPI > Serper > DuckDuckGo
    """
    
    # 1. 尝试Tavily
    print("尝试Tavily...", file=sys.stderr)
    results = search_tavily(query, num_results)
    if results:
        print("✅ Tavily成功", file=sys.stderr)
        return results
    
    # 2. 尝试SerpAPI
    print("尝试SerpAPI...", file=sys.stderr)
    results = search_serpapi(query, num_results)
    if results:
        print("✅ SerpAPI成功", file=sys.stderr)
        return results
    
    # 3. 尝试Serper
    print("尝试Serper...", file=sys.stderr)
    results = search_serper(query, num_results)
    if results:
        print("✅ Serper成功", file=sys.stderr)
        return results
    
    # 4. 尝试DuckDuckGo
    print("尝试DuckDuckGo...", file=sys.stderr)
    results = search_duckduckgo(query, num_results)
    if results:
        print("✅ DuckDuckGo成功", file=sys.stderr)
        return results
    
    # 全部失败
    print("❌ 所有搜索引擎都失败了", file=sys.stderr)
    return []

def main():
    if len(sys.argv) < 2:
        print("用法: python3 search_fallback.py <query> [num_results]")
        sys.exit(1)
    
    query = sys.argv[1]
    num_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    results = search(query, num_results)
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
