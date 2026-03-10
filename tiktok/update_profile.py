import asyncio, json
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def update_profile():
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="en-US",
        )
        page = await context.new_page()

        # Navigate to TikTok first, then inject cookies
        await page.goto("https://www.tiktok.com", wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(2)

        raw_cookies = json.load(open("/root/tiktok_cookies.json"))
        for c in raw_cookies:
            c["sameSite"] = "None"
            c["secure"] = True
        await context.add_cookies(raw_cookies)

        await page.reload(wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(4)

        await page.goto("https://www.tiktok.com/@dinothegamerrr", wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(3)

        btns = await page.query_selector_all("button")
        btn_texts = []
        for b in btns:
            t = (await b.inner_text()).strip()
            if t:
                btn_texts.append(t)
        print("Buttons:", btn_texts[:15])
        print("Edit profile visible:", "Edit profile" in btn_texts)

        await page.screenshot(path="/home/node/.openclaw/workspace/tiktok/tt_profile_check.png")
        await browser.close()

asyncio.run(update_profile())
