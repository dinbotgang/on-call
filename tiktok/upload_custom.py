#!/usr/bin/env python3
import asyncio, sys
from playwright.async_api import async_playwright

VIDEO_PATH = "/home/node/.openclaw/workspace/tiktok/videos/tiktok_v4.mp4"
COOKIES_FILE = "/root/tiktok_3amnarrator_cookies.txt"
CAPTION = """Would you have taken the stairs? 😰

#scarystories #horrortok #3am #creepy #scarytiktok #spooky #horrorstories #fyp #foryou #3amstories"""

def parse_cookies(f):
    cookies = []
    for line in open(f):
        line = line.strip()
        if not line or line.startswith("#"): continue
        p = line.split("\t")
        if len(p) < 7: continue
        c = {"name":p[5],"value":p[6],"domain":p[0],"path":p[2],"secure":p[3]=="TRUE","sameSite":"None"}
        try:
            if float(p[4]) > 0: c["expires"] = int(float(p[4]))
        except: pass
        cookies.append(c)
    return cookies

async def dismiss(page):
    for sel in ["text=Got it","button:has-text('Got it')","button:has-text('OK')","text=I understand"]:
        try: await page.click(sel, timeout=800); await asyncio.sleep(0.3)
        except: pass

async def upload():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox","--disable-blink-features=AutomationControlled"])
        ctx = await browser.new_context(viewport={"width":1280,"height":900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        await ctx.add_cookies(parse_cookies(COOKIES_FILE))
        page = await ctx.new_page()

        print("→ Loading upload page...")
        await page.goto("https://www.tiktok.com/tiktokstudio/upload?lang=en", wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(4)
        await dismiss(page)

        print("→ Attaching video...")
        await page.wait_for_selector("input[type='file']", state="attached", timeout=15000)
        await page.evaluate("document.querySelector('input[type=\"file\"]').style.display='block'")
        fi = await page.query_selector("input[type='file']")
        await fi.set_input_files(VIDEO_PATH)
        print("✅ Video attached")

        print("→ Waiting for upload to process (15s)...")
        await asyncio.sleep(15)
        await dismiss(page)

        print("→ Setting caption...")
        try:
            ce = await page.wait_for_selector("[contenteditable='true']", timeout=10000)
            await ce.click(); await asyncio.sleep(0.5)
            await page.keyboard.press("Control+a"); await page.keyboard.press("Backspace")
            await ce.type(CAPTION, delay=10)
            print("✅ Caption set")
        except Exception as e:
            print(f"⚠️ Caption: {e}")

        await asyncio.sleep(2)
        await dismiss(page)

        # Set privacy to Everyone
        print("→ Setting privacy to Everyone...")
        try:
            await page.evaluate("""() => {
                const btns = Array.from(document.querySelectorAll('button, div[role="button"]'));
                const priv = btns.find(b => b.innerText.includes('Only me') || b.innerText.includes('Friends'));
                if (priv) priv.click();
            }""")
            await asyncio.sleep(1)
            everyone = await page.wait_for_selector("text=Everyone", timeout=3000)
            await everyone.click()
            print("✅ Privacy set to Everyone")
            await asyncio.sleep(1)
        except:
            print("ℹ️ Privacy already Everyone or not found")

        # Scroll all scrollable areas to bottom to expose Post button
        await page.evaluate("""
            document.querySelectorAll('*').forEach(el => {
                if (el.scrollHeight > el.clientHeight) el.scrollTop = el.scrollHeight;
            });
        """)
        await asyncio.sleep(2)
        await dismiss(page)

        # Find and print ALL visible buttons
        btns = await page.evaluate("""() => {
            return Array.from(document.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                visible: b.offsetParent !== null,
                disabled: b.disabled,
                class: b.className.substring(0,60)
            })).filter(b => b.visible && b.text);
        }""")
        print(f"→ Visible buttons: {[b['text'] for b in btns]}")

        # Click Post via JS to bypass overlay interception
        print("→ Clicking Post via JS...")
        clicked = await page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const post = btns.find(b => b.innerText.trim() === 'Post' && !b.disabled);
            if (post) { post.click(); return true; }
            return false;
        }""")
        print(f"JS click result: {clicked}")
        await asyncio.sleep(3)

        # Handle any "exit" confirmation — click Cancel to stay
        try:
            cancel = await page.wait_for_selector("button:has-text('Cancel')", timeout=3000)
            await cancel.click()
            print("Dismissed exit dialog")
            await asyncio.sleep(2)
            # Click Post again via JS
            await page.evaluate("""() => {
                const b = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim()==='Post');
                if(b) b.click();
            }""")
            await asyncio.sleep(8)
        except:
            await asyncio.sleep(6)

        await page.screenshot(path="/home/node/.openclaw/workspace/tiktok/upload_final.png")
        print("→ Final URL:", page.url)

        # Check for success
        content = await page.content()
        success = any(x in content for x in ["Your video is being uploaded", "video is processing", "successfully", "content/manage"])
        print("✅ SUCCESS" if success else "⚠️ Could not confirm — check screenshot")
        await browser.close()
        return success

asyncio.run(upload())
