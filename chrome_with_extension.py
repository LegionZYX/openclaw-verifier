import subprocess
import time
import os
from playwright.sync_api import sync_playwright

# Chrome extension path
extension_path = os.path.expandvars(r"%USERPROFILE%\.openclaw\browser\chrome-extension")

# User data directory
user_data = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")

# Chrome path
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Debug port
debug_port = 18792

print("=== Starting Chrome with OpenClaw Extension ===")
print(f"Extension: {extension_path}")
print(f"Debug port: {debug_port}")

# Start Chrome command
cmd = [
    chrome_path,
    f"--remote-debugging-port={debug_port}",
    f"--load-extension={extension_path}",
    "--disable-extensions-except=" + extension_path,
    f"--user-data-dir={user_data}",
    "--profile-directory=Default",
    "https://github.com/login"
]

# Start Chrome
process = subprocess.Popen(cmd)
print(f"\nChrome started (PID: {process.pid})")

# Wait for Chrome to start
print("\nWaiting 15 seconds...")
time.sleep(15)

# Connect with Playwright
print("\n=== Connecting with Playwright ===")
with sync_playwright() as p:
    try:
        browser = p.chromium.connect_over_cdp(f"http://localhost:{debug_port}")
        print("Connected to Chrome")
        
        # Get contexts
        contexts = browser.contexts
        print(f"Contexts: {len(contexts)}")
        
        if contexts:
            pages = contexts[0].pages
            print(f"Pages: {len(pages)}")
            
            for i, page in enumerate(pages):
                print(f"  Page {i+1}: {page.title()}")
        
        print("\nBrowser is open.")
        print("Please login to GitHub, then press Enter...")
        
        # Wait for user input
        input()
        
        # Check login status
        if contexts and contexts[0].pages:
            page = contexts[0].pages[0]
            page.goto("https://github.com")
            time.sleep(2)
            
            # Screenshot
            page.screenshot(path="github_status.png")
            print("Screenshot saved: github_status.png")
            
            # Check for New button
            try:
                new_btn = page.query_selector('a[href="/new"]')
                if new_btn:
                    print("Logged in! Found 'New repository' button")
                    
                    # Click New button
                    print("Clicking 'New' button...")
                    new_btn.click()
                    time.sleep(3)
                    
                    # Fill repository form
                    print("Filling form...")
                    
                    # Repository name
                    name_input = page.wait_for_selector('#repository_name', timeout=5000)
                    if name_input:
                        name_input.fill('openclaw-verifier')
                        print("  Name: openclaw-verifier")
                        time.sleep(1)
                    
                    # Description
                    desc = page.query_selector('#repository_description')
                    if desc:
                        desc.fill('Security verification tool for OpenClaw Skills')
                        print("  Description filled")
                    
                    # Public
                    public = page.query_selector('#repository_public_true')
                    if public:
                        public.click()
                        print("  Selected Public")
                    
                    time.sleep(2)
                    
                    # Submit
                    submit = page.query_selector('button[type="submit"]')
                    if submit:
                        submit.click()
                        print("  Clicked Create")
                        
                        time.sleep(5)
                        page.wait_for_load_state("networkidle")
                        
                        url = page.url
                        print(f"\nCurrent URL: {url}")
                        
                        if "openclaw-verifier" in url:
                            print("\n=== SUCCESS ===")
                            print(f"Repository URL: {url}")
                        else:
                            print("\nMay need to check manually")
                            
                else:
                    print("Not logged in yet")
            except Exception as e:
                print(f"Error: {e}")
        
        browser.close()
        
    except Exception as e:
        print(f"Connection error: {e}")

print("\nDone")
