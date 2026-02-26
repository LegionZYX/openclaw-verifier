from playwright.sync_api import sync_playwright
import time

print("=== GitHub Repository Creator ===")

with sync_playwright() as p:
    # 启动新的 Chromium 实例
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    # 访问 GitHub
    print("Opening GitHub...")
    page.goto("https://github.com")
    page.wait_for_load_state("networkidle")
    
    print(f"Title: {page.title()}")
    
    # 检查是否已登录
    try:
        # 等待页面加载
        time.sleep(2)
        
        # 查找创建仓库按钮
        new_btn = page.query_selector('a[href="/new"]')
        
        if new_btn:
            print("Already logged in! Creating repository...")
            
            # 点击创建仓库
            new_btn.click()
            page.wait_for_load_state("networkidle")
            time.sleep(2)
            
            print(f"Current page: {page.title()}")
            
            # 填写仓库信息
            print("Filling repository details...")
            
            # 仓库名称
            name = page.wait_for_selector('#repository_name', timeout=10000)
            name.fill('openclaw-verifier')
            print("  Name: openclaw-verifier")
            time.sleep(1)
            
            # 描述
            desc = page.query_selector('#repository_description')
            if desc:
                desc.fill('Security verification tool for OpenClaw Skills - Scan skills for malicious code before installation')
                print("  Description: filled")
            
            # 选择 Public
            public = page.query_selector('#repository_public_true')
            if public:
                public.click()
                print("  Visibility: Public")
            
            # 等待创建按钮可用
            time.sleep(3)
            
            # 点击创建
            submit = page.query_selector('button[type="submit"]')
            if submit:
                submit.click()
                print("  Clicking Create...")
                
                # 等待创建完成
                time.sleep(5)
                page.wait_for_load_state("networkidle")
                
                url = page.url
                print(f"\n=== Result ===")
                print(f"URL: {url}")
                
                if "openclaw-verifier" in url:
                    print("\nSUCCESS! Repository created!")
                    print(f"Repository: {url}")
                    
                    # 保存 URL 到文件
                    with open("repo_url.txt", "w") as f:
                        f.write(url)
                    print("URL saved to repo_url.txt")
                else:
                    print("\nPlease check the browser window")
                    page.screenshot(path="result.png")
                    print("Screenshot saved: result.png")
        else:
            print("Not logged in. Please login first.")
            print("Waiting 60 seconds for login...")
            
            for i in range(60, 0, -1):
                print(f"  {i} seconds remaining...", end="\r")
                time.sleep(1)
            
            # 重新检查
            page.goto("https://github.com")
            page.wait_for_load_state("networkidle")
            
            new_btn = page.query_selector('a[href="/new"]')
            if new_btn:
                print("\nLogged in! Please run script again.")
            else:
                print("\nStill not logged in.")
            
            page.screenshot(path="login_status.png")
            print("Screenshot saved: login_status.png")
            
    except Exception as e:
        print(f"Error: {e}")
        page.screenshot(path="error.png")
        print("Screenshot saved: error.png")
    
    print("\nBrowser will close in 10 seconds...")
    time.sleep(10)
    
    browser.close()
    print("Done")
