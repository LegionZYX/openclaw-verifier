#!/usr/bin/env python3
"""
Web Search - DuckDuckGo 搜索
替代 Exa Search API
"""

import urllib.request
import urllib.parse
import json
from typing import List, Dict

def search(query: str, num_results: int = 5) -> List[Dict]:
    """
    使用 DuckDuckGo 搜索
    
    Args:
        query: 搜索查询
        num_results: 返回结果数量
    
    Returns:
        搜索结果列表
    """
    results = []
    
    # DuckDuckGo Instant Answer API
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json&no_html=1"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            # 提取相关主题
            if data.get("RelatedTopics"):
                for topic in data["RelatedTopics"][:num_results]:
                    if isinstance(topic, dict) and "Text" in topic:
                        results.append({
                            "title": topic.get("Text", "")[:100],
                            "url": topic.get("FirstURL", ""),
                            "snippet": topic.get("Text", "")
                        })
            
            # 如果没有结果，添加摘要
            if not results and data.get("Abstract"):
                results.append({
                    "title": data.get("Heading", query),
                    "url": data.get("AbstractURL", ""),
                    "snippet": data.get("Abstract", "")
                })
                
    except Exception as e:
        results.append({
            "title": "Search Error",
            "url": "",
            "snippet": f"Error: {str(e)}"
        })
    
    return results


def search_google_ps(query: str, num_results: int = 5) -> List[Dict]:
    """
    使用 PowerShell 调用 Google 搜索（解析 HTML）
    """
    import subprocess
    
    results = []
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}&num={num_results}"
    
    ps_script = f'''
    try {{
        $response = Invoke-WebRequest -Uri "{url}" -UseBasicParsing -TimeoutSec 15
        $response.Content
    }} catch {{
        Write-Error $_.Exception.Message
    }}
    '''
    
    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        html = result.stdout
        
        # 简单解析搜索结果
        import re
        
        # 提取标题和链接
        pattern = r'<a href="(/url\?q=([^"]+))"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)[:num_results]
        
        for match in matches:
            results.append({
                "title": match[2],
                "url": urllib.parse.unquote(match[1].split("&")[0]),
                "snippet": ""
            })
            
    except Exception as e:
        results.append({
            "title": "Search Error",
            "url": "",
            "snippet": f"Error: {str(e)}"
        })
    
    return results


if __name__ == "__main__":
    import sys
    
    query = sys.argv[1] if len(sys.argv) > 1 else "OpenClaw security"
    num = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    print(f"Searching: {query}")
    print("-" * 50)
    
    results = search(query, num)
    
    for i, r in enumerate(results, 1):
        print(f"\n{i}. {r['title'][:80]}")
        if r['url']:
            print(f"   URL: {r['url']}")
        if r['snippet']:
            print(f"   {r['snippet'][:200]}")
