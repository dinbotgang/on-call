#!/usr/bin/env python3
"""
TikTok Studio uploader — @3am.narrator
v4: Fixed - scroll to TOP for description field, safe character typing
"""
import asyncio, sys
from playwright.async_api import async_playwright

VIDEO_PATH = "/home/node/.openclaw/workspace/tiktok/videos/tiktok_v7.mp4"
COOKIES_FILE = "/root/tiktok_3amnarrator_cookies.txt"
SCREENSHOT_PATH = "/home/node/.openclaw/workspace/tiktok/upload_v7_final.png"
DEBUG_DIR = "/home/node/.openclaw/workspace/tiktok"

# Caption with hashtags as plain text (TikTok parses them automatically on publish)
CAPTION = "Who do you think left that voicemail? 👁️\n\n#scarystories #horrortok #3am #creepy #scarytiktok #spooky #horrorstories #fyp #foryou #3amstories"

# ──────────────────────────────────────────────────────────
def parse_cookies(f):
    cookies = []
    for line in open(f):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        p = line.split("\t")
        if len(p) < 7:
            continue
        c = {
            "name": p[5], "value": p[6],
            "domain": p[0], "path": p[2],
            "secure": p[3] == "TRUE",
            "sameSite": "None"
        }
        try:
            if float(p[4]) > 0:
                c["expires"] = int(float(p[4]))
        except:
            pass
        cookies.append(c)
    return cookies


async def dismiss_dialogs(page):
    """Dismiss popups."""
    selectors = [
        "button:has-text('Allow all')",
        "button:has-text('Got it')",
        "button:has-text('OK')",
    ]
    for sel in selectors:
        try:
            btn = await page.query_selector(sel)
            if btn and await btn.is_visible():
                await btn.click()
                await asyncio.sleep(0.3)
        except:
            pass


async def set_description(page, caption: str) -> bool:
    """Type full caption including hashtags. Escape after each line dismisses autocomplete."""
    try:
        await page.evaluate("window.scrollTo(0, 0);")
        await asyncio.sleep(0.5)

        desc_field = await page.query_selector("div[contenteditable='true']")
        if not desc_field:
            print("❌ Description field not found")
            return False

        await desc_field.scroll_into_view_if_needed()
        await asyncio.sleep(0.3)
        await desc_field.click()
        await asyncio.sleep(0.5)

        # Clear existing content
        await page.keyboard.press("Control+a")
        await asyncio.sleep(0.1)
        await page.keyboard.press("Delete")
        await asyncio.sleep(0.3)

        # Type caption word by word.
        # For hashtags: type then press Enter to confirm via TikTok's autocomplete
        # (Enter with no ArrowDown confirms the typed text as a proper hashtag link).
        # For regular text: type normally.
        lines = caption.split("\n")
        for i, line in enumerate(lines):
            if line:
                words = line.split(" ")
                for j, word in enumerate(words):
                    if not word:
                        continue
                    if word.startswith("#"):
                        await page.keyboard.type(word, delay=25)
                        await asyncio.sleep(1.2)   # let autocomplete fully populate
                        await page.keyboard.press("Enter")  # confirm typed text as hashtag
                        await asyncio.sleep(0.4)
                        # space between tags (not after last word on last line)
                        is_last = (i == len(lines) - 1 and j == len(words) - 1)
                        if not is_last:
                            await page.keyboard.type(" ")
                            await asyncio.sleep(0.1)
                    else:
                        suffix = " " if j < len(words) - 1 else ""
                        await page.keyboard.type(word + suffix, delay=20)
            if i < len(lines) - 1:
                await page.keyboard.press("Enter")
                await asyncio.sleep(0.2)

        await asyncio.sleep(0.8)

        actual = await page.evaluate(
            "() => document.querySelector(\"div[contenteditable='true']\")?.innerText || ''"
        )
        if actual.strip():
            print(f"✅ Description set ({len(actual.strip())} chars)")
            print(f"   Content: {actual[:80].replace(chr(10), ' ')!r}...")
            return True
        print("⚠️ Description appears empty after typing")
        return False

    except Exception as e:
        print(f"❌ Description failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def upload():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
            ]
        )
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
        )
        await ctx.add_cookies(parse_cookies(COOKIES_FILE))
        page = await ctx.new_page()

        # ── Load page ─────────────────────────────────────
        print("→ Loading TikTok Studio upload page...")
        await page.goto(
            "https://www.tiktok.com/tiktokstudio/upload?lang=en",
            wait_until="domcontentloaded",
            timeout=30000
        )
        await asyncio.sleep(5)
        await dismiss_dialogs(page)

        page_text = await page.evaluate("() => document.body.innerText")
        if "Something went wrong" in page_text:
            print("  ⚠️ Error on load, reloading...")
            await page.reload(wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(5)
            await dismiss_dialogs(page)
            page_text = await page.evaluate("() => document.body.innerText")
            if "Something went wrong" in page_text:
                print("❌ Page persistently erroring.")
                await browser.close()
                return False
        print("✅ Page loaded")

        # ── Attach video ──────────────────────────────────
        print("→ Attaching video...")
        await page.wait_for_selector("input[type='file']", state="attached", timeout=20000)
        await page.evaluate("document.querySelector('input[type=\"file\"]').style.display='block'")
        fi = await page.query_selector("input[type='file']")
        await fi.set_input_files(VIDEO_PATH)
        print("✅ Video attached")
        await asyncio.sleep(5)

        # ── Wait for processing ───────────────────────────
        print("→ Waiting for video to process (30s)...")
        await asyncio.sleep(20)
        await dismiss_dialogs(page)
        await asyncio.sleep(10)
        await dismiss_dialogs(page)

        # Verify still healthy
        page_text = await page.evaluate("() => document.body.innerText")
        if "Something went wrong" in page_text:
            print("❌ Page errored after video processing.")
            await browser.close()
            return False
        print("✅ Video processing complete")

        # ── Set description with caption + hashtags ───────
        print("→ Setting description...")
        desc_ok = await set_description(page, CAPTION)
        if not desc_ok:
            print("⚠️ Description may not have been set correctly")
        
        await asyncio.sleep(1)
        # Scroll to top to verify caption is visible in screenshot
        await page.evaluate("window.scrollTo(0, 0);")
        await asyncio.sleep(0.3)
        await page.screenshot(path=f"{DEBUG_DIR}/debug_with_caption.png")
        print("📸 debug_with_caption.png")

        # ── Verify privacy ────────────────────────────────
        print("→ Verifying privacy...")
        privacy_text = await page.evaluate("""() => {
            const el = Array.from(document.querySelectorAll('*')).find(
                el => el.innerText && el.innerText.includes('Who can watch')
            );
            const dropdown = el ? el.closest('div')?.querySelector('div[role="button"], button') : null;
            return dropdown ? dropdown.innerText : 'Unknown';
        }""")
        print(f"  Privacy: {privacy_text!r}")
        if "Everyone" not in privacy_text:
            print("  → Setting privacy to Everyone...")
            await page.evaluate("""() => {
                const btns = Array.from(document.querySelectorAll('button, div[role="button"]'));
                const privBtn = btns.find(b =>
                    b.innerText.includes('Only me') ||
                    b.innerText.includes('Friends') ||
                    b.innerText.includes('Followers')
                );
                if (privBtn) privBtn.click();
            }""")
            await asyncio.sleep(1)
            try:
                ev = await page.wait_for_selector("text=Everyone", timeout=2000)
                await ev.click()
                print("✅ Privacy set to Everyone")
            except:
                print("ℹ️ Could not set privacy")

        # ── Scroll to Post button ─────────────────────────
        print("→ Scrolling to Post button...")
        await page.evaluate("""
            document.querySelectorAll('*').forEach(el => {
                if (el.scrollHeight > el.clientHeight) el.scrollTop = el.scrollHeight;
            });
        """)
        await asyncio.sleep(1)

        btns = await page.evaluate("""() =>
            Array.from(document.querySelectorAll('button'))
                .filter(b => b.offsetParent !== null && b.innerText.trim())
                .map(b => ({ text: b.innerText.trim(), disabled: b.disabled }))
        """)
        print(f"  Visible buttons: {[b['text'] for b in btns[:8]]}")

        # ── Post ──────────────────────────────────────────
        print("→ Clicking Post...")
        clicked = await page.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
                .find(b => b.innerText.trim() === 'Post' && !b.disabled);
            if (btn) { btn.click(); return true; }
            return false;
        }""")
        
        if not clicked:
            print("⚠️ Post button not found or disabled")
            await page.screenshot(path=SCREENSHOT_PATH)
            await browser.close()
            return False

        print("✅ Post clicked")
        await asyncio.sleep(5)

        # ── Handle "Continue to post?" confirmation dialog ──
        # TikTok shows this when content check is still running
        try:
            post_now = await page.wait_for_selector(
                "button:has-text('Post now')", timeout=4000
            )
            await post_now.click()
            print("✅ Clicked 'Post now' on confirmation dialog")
            await asyncio.sleep(8)
        except:
            await asyncio.sleep(5)

        # ── Final screenshot & confirmation ───────────────
        await page.screenshot(path=SCREENSHOT_PATH)
        print(f"📸 Final: {SCREENSHOT_PATH}")
        print(f"→ URL: {page.url}")

        content = await page.evaluate("() => document.body.innerText")
        success = any(s.lower() in content.lower() for s in [
            "uploading", "processing", "successfully", "view video", "your video"
        ]) or "manage" in page.url

        if success or "upload" not in page.url:
            print("✅ SUCCESS — video posted!")
            await browser.close()
            return True
        else:
            print("⚠️ Upload status unclear — check final screenshot")
            print(f"  Page text: {content[:200].replace(chr(10), ' ')}")
            await browser.close()
            return False


if __name__ == "__main__":
    result = asyncio.run(upload())
    sys.exit(0 if result else 1)
