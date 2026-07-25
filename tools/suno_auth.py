import asyncio
from playwright.async_api import async_playwright
import os

async def save_session():
    print("🚀 Starting Suno Auth Session Capture...")
    async with async_playwright() as p:
        # Using a dedicated user data directory for the Suno Automation profile
        user_data_dir = os.path.expanduser("~/suno_automation_profile")
        
        # Launch browser in non-headless mode for manual login
        browser = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        
        page = await browser.new_page()
        await page.goto("https://suno.com/create")
        
        print("\n🔒 PLEASE LOG IN TO SUNO USING YOUR GOOGLE ACCOUNT.")
        print("Waiting for you to complete login...")
        print("Once you are logged in and seeing the 'Create' page, come back here.")
        
        # Wait for the user to login - looking for the 'Create' intent or user avatar
        # We'll wait indefinitely until the user closes the browser or we detect success
        try:
            # Check for a selector that only appears when logged in, or just wait for manual closure
            await page.wait_for_selector("button:has-text('Create')", timeout=0)
            print("\n✅ Login detected! Saving session...")
        except Exception:
            print("\n⚠️ Browser closed or interrupted.")
            
        await browser.close()
        print(f"📂 Session state saved to: {user_data_dir}")

if __name__ == "__main__":
    asyncio.run(save_session())
