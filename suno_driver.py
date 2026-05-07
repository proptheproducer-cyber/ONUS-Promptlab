import asyncio
from playwright.async_api import async_playwright
import os
import json
import sys

async def run_suno_gen(prompt_data):
    user_data_dir = os.path.expanduser("~/suno_automation_profile")
    
    async with async_playwright() as p:
        # Launch using the saved profile
        browser = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False, # Keep headed for now so you can watch
        )
        
        page = await browser.new_page()
        await page.goto("https://suno.com/create")
        
        # 1. Ensure 'Custom' mode is ON
        # Suno UI often has a toggle for 'Custom Mode'
        custom_toggle = page.get_by_role("button", name="Custom")
        if await custom_toggle.is_visible():
            await custom_toggle.click()

        # 2. Input Lyrics (lyrics_prompt)
        lyrics_box = page.get_by_placeholder("Enter your own lyrics")
        await lyrics_box.fill(prompt_data.get('lyrics', ''))
        
        # 3. Input Style (style_prompt)
        style_box = page.get_by_placeholder("Enter style of music")
        await style_box.fill(prompt_data.get('style', ''))
        
        # 4. Input Title
        title_box = page.get_by_placeholder("Enter title")
        await title_box.fill(prompt_data.get('title', 'Suno Masterpiece'))
        
        # 5. Handle Sliders (Model/Version and Weirdness)
        # Note: Suno UI sliders are often range inputs or custom div sliders.
        # This part may require specific coordinate/drag logic depending on the latest UI.
        
        # 6. Click Create
        create_button = page.get_by_role("button", name="Create", exact=True)
        await create_button.click()
        
        print(f"🎵 Track '{prompt_data.get('title')}' generation started!")
        
        # Keep open long enough to see it start
        await asyncio.sleep(5)
        await browser.close()

if __name__ == "__main__":
    # Expecting prompt data via JSON string in stdin or argument
    if len(sys.argv) > 1:
        data = json.loads(sys.argv[1])
    else:
        # Fallback test data
        data = {
            "title": "Test Track",
            "lyrics": "[Verse]\nHello from ONUS Automation",
            "style": "lo-fi, chill, hip-hop"
        }
    asyncio.run(run_suno_gen(data))
