from playwright.sync_api import sync_playwright
import time
import os

print("=== GitHub Repository Creator (Using existing Chrome profile) ===")

# 使用用户的 Chrome 配置文件
user_data = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")

with sync_playwright() as p:
    # 使用持久化上下文（保留登录状态）
    context = p.chromium.launch_persistent_context(
        user_data_dir=user_data,
        headless=False,
        channel="chrome",
        args=["--profile-directory=Default"]
    )
    
    # 获取或创建页面
    if len(context.pages) > 0:
        page = context.pages[0]
    else:
        page = context.new_page()
    
    # 访问 GitHub
    print("Opening GitHub...")
    page.goto("https://github.com")
    page.wait_for_load_state("networkidle")
    
    print(f"Title: {page.title()}")
    time.sleep(2)
    
    # 检查登录状态
    try:
        new_btn = page.query_selector('a[href="/new"]')
        
        if new_btn:
            print("SUCCESS: Already logged in!")
            print("Creating repository...")
            
            # 点击创建仓库
            new_btn.click()
            page.wait_for_load_state("networkidle")
            time.sleep(2)
            
            # 填写仓库信息
            print("Filling details...")
            
            # 仓库名称
            name = page.wait_for_selector('#repository_name', timeout=10000)
            name.fill('openclaw-verifier')
            print("  Name: openclaw-verifier")
            time.sleep(1)
            
            # 描述
            desc = page.query_selector('#repository_description')
            if desc:
                desc.fill('Security verification tool for OpenClaw Skills')
                print("  Description: filled")
            
            # Public
            public = page.query_selector('#repository_public_true')
            if public:
                public.click()
                print("  Visibility: Public")
            
            time.sleep(3)
            
            # 创建
            submit = page.query_selector('button[type="submit"]')
            if submit:
                submit.click()
                print("  Creating...")
                
                time.sleep(5)
                page.wait_for_load_state("networkidle")
                
                url = page.url
                print(f"\nURL: {url}")
                
                if "openclaw-verifier" in url:
                    print("\n=== SUCCESS ===")
                    print(f"Repository: {url}")
                    
                    with open("repo_url.txt", "w") as f:
                        f.write(url)
                else:
                    print("\nCheck browser window")
        else:
            print("Not logged in with this profile")
            print("Please login in the browser window...")
            
            for i in range(120, 0, -1):
                print(f"  {i} seconds...", end="\r")
                time.sleep(1)
            
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nPress Enter to close browser...")
    input()
    
    context.close()
    print("Done")
