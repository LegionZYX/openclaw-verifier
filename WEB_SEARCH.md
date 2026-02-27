# Web Search 替代方案

## 方案

### 1. PowerShell Invoke-WebRequest（推荐）
- 无需额外依赖
- 直接调用搜索引擎
- 解析 HTML 结果

### 2. 浏览器自动化
- Playwright
- 获取完整渲染结果

### 3. DuckDuckGo API
- 免费，无需 API Key
- 直接 HTTP 请求

---

## 实现

使用 DuckDuckGo Instant Answer API：
```
https://api.duckduckgo.com/?q=查询&format=json
```

或使用 Bing/Google 搜索结果解析。

---

现在开始用 PowerShell Web Fetch 替代 exa search。
