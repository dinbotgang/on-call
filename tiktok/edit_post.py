#!/usr/bin/env python3
"""
Edit the most recent TikTok post — fix description to include caption + hashtags.
"""
import asyncio
from playwright.async_api import async_playwright

COOKIES_FILE = "/root/tiktok_3amnarrator_cookies.txt"
DEBUG_DIR = "/home/node/.openclaw/workspace/tiktok"

CORRECT_CAPTION = "Would you have taken the stairs? 😰\n\n#scarystories #horrortok #3am #creepy #scarytiktok #spooky #horrorstories #fyp #foryou #3amstories"

def parse_cookies(f):
    cookies = []
    for line in open(f):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        p = line.split("\t")
        if len(p) < 7:
            continue
        c = {"name": p[5], "value": p[6], "domain": p[0], "path": p[2],
             "secure": p[3] == "TRUE", "sameSite": "None"}
        try:
            if float(p[4]) > 0:
                c["expires"] = int(float(p[4]))
        except:
            pass
        cookies.append(c)
    return cookies


async def edit():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
        )
        await ctx.add_cookies(parse_cookies(COOKIES_FILE))
        page = await ctx.new_page()

        print("→ Loading content manager...")
        await page.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(4)

        # Dismiss cookie banner
        try:
            btn = await page.query_selector("button:has-text('Allow all')")
            if btn: await btn.click()
        except: pass
        await asyncio.sleep(1)

        # Find and click the pencil/edit icon (first action button on video row)
        print("→ Clicking edit (pencil) icon...")
        
        # The pencil icon is an SVG button in the actions column
        # Try various approaches to find it
        clicked = await page.evaluate("""() => {
            // Find all buttons in the page
            const allBtns = Array.from(document.querySelectorAll('button, [role="button"]'));
            
            // Look for button with SVG that looks like an edit/pencil icon
            // Often has aria-label="Edit" or contains a pencil SVG path
            for (const btn of allBtns) {
                const label = (btn.getAttribute('aria-label') || '').toLowerCase();
                const title = (btn.getAttribute('title') || '').toLowerCase();
                if (label.includes('edit') || title.includes('edit')) {
                    btn.click();
                    return 'edit-aria';
                }
            }
            
            // Try SVG title elements
            const svgTitles = Array.from(document.querySelectorAll('title'));
            for (const t of svgTitles) {
                if (t.textContent.toLowerCase().includes('edit')) {
                    const btn = t.closest('button') || t.closest('[role="button"]');
                    if (btn) { btn.click(); return 'svg-title'; }
                }
            }
            
            return null;
        }""")
        
        if not clicked:
            # Get all button details to find the right one
            all_btns = await page.evaluate("""() =>
                Array.from(document.querySelectorAll('button, [role="button"]'))
                    .filter(b => b.offsetParent !== null)
                    .map(b => ({
                        text: b.innerText.trim().substring(0, 30),
                        ariaLabel: b.getAttribute('aria-label') || '',
                        title: b.getAttribute('title') || '',
                        class: b.className.substring(0, 60),
                        hasIcon: b.querySelector('svg') !== null
                    }))
            """)
            print("All visible buttons:")
            for b in all_btns:
                print(f"  text={b['text']!r} aria={b['ariaLabel']!r} title={b['title']!r} hasIcon={b['hasIcon']}")
            
            # The edit button is likely the first icon button (with SVG, no text) in the action row
            # Try clicking the first SVG icon button that's likely in the video row
            clicked = await page.evaluate("""() => {
                const iconBtns = Array.from(document.querySelectorAll('button'))
                    .filter(b => b.offsetParent !== null && b.querySelector('svg') && !b.innerText.trim());
                console.log('Icon buttons found:', iconBtns.length);
                // The pencil/edit is typically the FIRST icon button in the actions area
                if (iconBtns.length > 0) {
                    iconBtns[0].click();
                    return 'first-icon-btn';
                }
                return null;
            }""")
            
        print(f"  Click result: {clicked}")
        await asyncio.sleep(3)
        await page.screenshot(path=f"{DEBUG_DIR}/edit_after_click.png")
        print("📸 edit_after_click.png")
        
        url = page.url
        print(f"→ URL after click: {url}")

        # Check if we navigated to an edit page
        if "edit" in url.lower() or "post" in url.lower():
            print("✅ Navigated to edit page")
        else:
            # Maybe a modal opened
            page_text = await page.evaluate("() => document.body.innerText")
            if "Description" in page_text or "Caption" in page_text or "contenteditable" in await page.evaluate("() => document.body.innerHTML"):
                print("✅ Edit UI appeared (modal or panel)")
            else:
                print("⚠️ Edit didn't navigate — trying direct edit URL approach")
                # Try going to the edit page directly if we can find the video ID
                # Look for video IDs in the page
                video_ids = await page.evaluate("""() => {
                    const links = Array.from(document.querySelectorAll('a[href*="/video/"]'));
                    return links.map(l => l.href);
                }""")
                print(f"  Video links: {video_ids}")
                
                if video_ids:
                    vid_url = video_ids[0]
                    # Extract video ID
                    import re
                    m = re.search(r'/video/(\d+)', vid_url)
                    if m:
                        vid_id = m.group(1)
                        edit_url = f"https://www.tiktok.com/tiktokstudio/post/{vid_id}"
                        print(f"  Trying edit URL: {edit_url}")
                        await page.goto(edit_url, wait_until="domcontentloaded", timeout=30000)
                        await asyncio.sleep(3)
                        url = page.url

        # Now try to find and fill the description field
        print("→ Looking for description field...")
        ces = await page.query_selector_all("div[contenteditable='true'], textarea")
        print(f"  Found {len(ces)} editable fields")
        
        if ces:
            ce = ces[0]
            await ce.scroll_into_view_if_needed()
            await ce.click()
            await asyncio.sleep(0.3)
            
            # Select all and clear
            await page.keyboard.press("Control+a")
            await asyncio.sleep(0.1)
            await page.keyboard.press("Delete")
            await asyncio.sleep(0.2)
            
            # Type the caption
            lines = CORRECT_CAPTION.split("\n")
            for i, line in enumerate(lines):
                if line:
                    await page.keyboard.type(line, delay=15)
                if i < len(lines) - 1:
                    await page.keyboard.press("Enter")
                    await asyncio.sleep(0.1)
            
            await asyncio.sleep(0.5)
            actual = await ce.evaluate("el => el.innerText || el.value || ''")
            print(f"  Caption preview: {actual[:80]!r}")
            await page.screenshot(path=f"{DEBUG_DIR}/edit_with_caption.png")
            print("📸 edit_with_caption.png")
            
            # Find and click Save
            saved = False
            for sel in ["button:has-text('Save')", "button:has-text('Post')", "button:has-text('Update')"]:
                try:
                    save_btn = await page.query_selector(sel)
                    if save_btn and await save_btn.is_visible():
                        await save_btn.click()
                        print(f"✅ Clicked {sel}")
                        saved = True
                        await asyncio.sleep(5)
                        break
                except:
                    pass
            
            if not saved:
                print("⚠️ Save button not found")
                btns = await page.evaluate("""() =>
                    Array.from(document.querySelectorAll('button'))
                        .filter(b => b.offsetParent !== null && b.innerText.trim())
                        .map(b => b.innerText.trim())
                """)
                print(f"  Available buttons: {btns}")
        else:
            print("❌ No editable fields found")

        await page.screenshot(path=f"{DEBUG_DIR}/edit_final.png")
        print("📸 edit_final.png")
        await browser.close()


asyncio.run(edit())
