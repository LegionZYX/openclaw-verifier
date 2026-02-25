import subprocess
import time
import os
from playwright.sync_api import sync_playwright

# Chrome 路径
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
debug_port = 9223
user_data_dir = os.path.join(os.environ['TEMP'], 'chrome_automation_profile')

# 启动 Chrome（带调试端口）
print("启动 Chrome...")
cmd = [
    chrome_path,
    f"--remote-debugging-port={debug_port}",
    f"--user-data-dir={user_data_dir}",
    "--no-first-run",
    "--no-default-browser-check",
    "https://github.com/login"
]

process = subprocess.Popen(cmd)
print(f"Chrome 已启动 (PID: {process.pid})")

# 等待 Chrome 启动
time.sleep(5)

# 使用 Playwright 连接
print("连接到 Chrome...")
with sync_playwright() as p:
    try:
        browser = p.chromium.connect_over_cdp(f"http://localhost:{debug_port}")
        print("Connected!")
        
        # 获取页面
        contexts = browser.contexts
        if contexts:
            pages = contexts[0].pages
            if pages:
                page = pages[0]
                print(f"Page: {page.title()}")
                
                # 等待用户登录
                print("Waiting 60 seconds for login...")
                time.sleep(60)
                
                # 检查登录状态
                page.goto("https://github.com")
                time.sleep(2)
                
                # 截图
                page.screenshot(path="github_status.png")
                print("Screenshot saved")
                
        input("Press Enter to close...")
        browser.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        process.terminate()
