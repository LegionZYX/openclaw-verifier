from playwright.sync_api import sync_playwright
import time

print("Starting browser automation...")

with sync_playwright() as p:
    # 启动 Chromium（不使用系统 Chrome）
    browser = p.chromium.launch(
        headless=False,
        args=['--start-maximized']
    )
    
    context = browser.new_context()
    page = context.new_page()
    
    # 访问 GitHub 登录页
    print("Opening GitHub login...")
    page.goto("https://github.com/login", wait_until="networkidle")
    print(f"Title: {page.title()}")
    
    # 截图
    page.screenshot(path="github_login.png")
    
    # 等待用户登录（120秒）
    print("\n" + "="*50)
    print("PLEASE LOGIN TO GITHUB IN THE BROWSER WINDOW")
    print("Waiting 120 seconds...")
    print("="*50 + "\n")
    
    for i in range(120, 0, -1):
        print(f"Countdown: {i} seconds  ", end="\r")
        time.sleep(1)
    
    print("\n\nChecking login status...")
    
    # 访问 GitHub 主页
    page.goto("https://github.com", wait_until="networkidle")
    page.screenshot(path="github_after_login.png")
    
    # 检查是否登录
    try:
        # 尝试找到 "New" 按钮（创建仓库）
        new_btn = page.query_selector('a[href="/new"]')
        if new_btn:
            print("SUCCESS: Logged in! Found 'New repository' button")
            
            # 点击创建仓库
            print("Clicking 'New' button...")
            new_btn.click()
            page.wait_for_load_state("networkidle")
            
            print(f"Current page: {page.title()}")
            page.screenshot(path="github_new_repo.png")
            
            # 填写仓库信息
            print("Filling repository info...")
            
            # 仓库名
            name_input = page.wait_for_selector('#repository_name', timeout=5000)
            if name_input:
                name_input.fill('openclaw-verifier')
                print("  - Name: openclaw-verifier")
                time.sleep(1)
            
            # 描述
            desc_input = page.query_selector('#repository_description')
            if desc_input:
                desc_input.fill('Security verification tool for OpenClaw Skills')
                print("  - Description filled")
            
            # 选择 Public
            public_btn = page.query_selector('#repository_public_true')
            if public_btn:
                public_btn.click()
                print("  - Selected Public")
            
            # 等待创建按钮可用
            time.sleep(2)
            
            # 点击创建
            create_btn = page.query_selector('button[type="submit"]')
            if create_btn:
                create_btn.click()
                print("  - Clicking Create button")
                
                # 等待创建完成
                time.sleep(5)
                page.wait_for_load_state("networkidle")
                
                current_url = page.url
                print(f"\nCurrent URL: {current_url}")
                page.screenshot(path="github_repo_created.png")
                
                if "openclaw-verifier" in current_url:
                    print("\n" + "="*50)
                    print("SUCCESS! Repository created!")
                    print(f"URL: {current_url}")
                    print("="*50)
                else:
                    print("\nRepository creation might have failed")
                    print("Check the screenshot: github_repo_created.png")
        else:
            print("NOT LOGGED IN: Could not find 'New' button")
            print("Please try again")
            
    except Exception as e:
        print(f"Error: {e}")
        page.screenshot(path="github_error.png")
    
    # 等待查看结果
    print("\nBrowser will close in 10 seconds...")
    time.sleep(10)
    
    browser.close()
    print("Done")
