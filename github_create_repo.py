from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        channel="chrome"
    )
    
    context = browser.new_context()
    page = context.new_page()
    
    # 直接访问登录页面
    print("Navigating to GitHub login...")
    page.goto("https://github.com/login")
    page.wait_for_load_state("networkidle")
    
    print(f"Page title: {page.title()}")
    page.screenshot(path="github_login_page.png")
    
    # 等待 60 秒让用户登录
    print("等待 60 秒供用户登录...")
    for i in range(60, 0, -1):
        print(f"  倒计时: {i} 秒", end="\r")
        time.sleep(1)
    
    print("\n检查登录状态...")
    
    # 检查是否登录成功
    page.goto("https://github.com")
    page.wait_for_load_state("networkidle")
    page.screenshot(path="github_after_login.png")
    
    # 查找创建仓库按钮
    try:
        # 尝试多种选择器
        selectors = [
            'a[href="/new"]',
            'a[href*="new"]',
            '[data-testid="create-repository-button"]',
            'a.Header-link[href="/new"]'
        ]
        
        new_repo_btn = None
        for selector in selectors:
            new_repo_btn = page.query_selector(selector)
            if new_repo_btn:
                print(f"✅ 找到创建仓库按钮: {selector}")
                break
        
        if new_repo_btn:
            print("点击创建新仓库...")
            new_repo_btn.click()
            page.wait_for_load_state("networkidle")
            
            print(f"当前页面: {page.title()}")
            page.screenshot(path="github_new_repo_page.png")
            
            # 等待页面加载
            time.sleep(2)
            
            # 填写仓库信息
            print("填写仓库信息...")
            
            # 仓库名称
            repo_name_input = page.query_selector('#repository_name')
            if repo_name_input:
                repo_name_input.fill('openclaw-verifier')
                print("✅ 仓库名称: openclaw-verifier")
                time.sleep(1)
            
            # 描述
            desc_input = page.query_selector('#repository_description')
            if desc_input:
                desc_input.fill('Security verification tool for OpenClaw Skills - Scan skills for malicious code')
                print("✅ 描述已填写")
            
            # 选择 Public
            public_radio = page.query_selector('#repository_public_true')
            if public_radio:
                public_radio.click()
                print("✅ 选择 Public")
            
            # 等待创建按钮可用
            time.sleep(2)
            
            # 点击创建按钮
            create_btn = page.query_selector('button[type="submit"]')
            if create_btn:
                create_btn.click()
                print("✅ 点击创建仓库")
                
                # 等待创建完成
                time.sleep(5)
                page.wait_for_load_state("networkidle")
                
                current_url = page.url()
                print(f"当前URL: {current_url}")
                page.screenshot(path="github_repo_created.png")
                
                if "openclaw-verifier" in current_url:
                    print("✅ 仓库创建成功！")
                    print(f"仓库地址: {current_url}")
                else:
                    print("⚠️ 可能创建失败，请检查截图")
        else:
            print("❌ 未找到创建仓库按钮 - 可能未登录")
            page.screenshot(path="github_not_logged_in.png")
            
    except Exception as e:
        print(f"Error: {e}")
        page.screenshot(path="github_error.png")
    
    # 保持浏览器打开
    print("\n等待 10 秒后关闭浏览器...")
    time.sleep(10)
    
    browser.close()
    print("Done")
