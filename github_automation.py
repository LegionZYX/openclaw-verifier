from playwright.sync_api import sync_playwright
import time
import os

with sync_playwright() as p:
    # 使用独立的配置目录，避免冲突
    browser = p.chromium.launch(
        headless=False,
        channel="chrome"
    )
    
    context = browser.new_context()
    page = context.new_page()
    
    # 访问 GitHub
    print("Navigating to GitHub...")
    page.goto("https://github.com")
    page.wait_for_load_state("networkidle")
    
    # 检查页面标题
    print(f"Page title: {page.title()}")
    
    # 截图
    page.screenshot(path="github_home.png")
    print("Screenshot saved to github_home.png")
    
    # 检查是否有登录按钮
    try:
        sign_in = page.query_selector('a[href="/login"]')
        if sign_in:
            print("Found login button - clicking...")
            sign_in.click()
            page.wait_for_load_state("networkidle")
            print(f"After click - Page title: {page.title()}")
            page.screenshot(path="github_login.png")
            print("Login page screenshot saved")
        else:
            print("No login button found - might be logged in")
            # 检查是否有用户头像
            avatar = page.query_selector('img[alt*="avatar"]')
            if avatar:
                print("Found user avatar - logged in!")
    except Exception as e:
        print(f"Error: {e}")
    
    # 等待用户查看
    time.sleep(10)
    
    browser.close()
    print("Done")
