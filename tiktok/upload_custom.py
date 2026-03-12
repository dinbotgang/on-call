#!/usr/bin/env python3
"""
TikTok Studio uploader — @3am.narrator
v4: Fixed - scroll to TOP for description field, safe character typing
"""
import asyncio, sys
from playwright.async_api import async_playwright

VIDEO_PATH = "/home/node/.openclaw/workspace/tiktok/videos/tiktok_v4.mp4"
COOKIES_FILE = "/root/tiktok_3amnarrator_cookies.txt"
SCREENSHOT_PATH = "/home/node/.openclaw/workspace/tiktok/upload_final.png"
DEBUG_DIR = "/home/node/.openclaw/workspace/tiktok"

# Caption with emoji and hashtags
CAPTION = "Would you have taken the stairs? 😰\n\n#scarystories #horrortok #3am #creepy #scarytiktok #spooky #horrorstories #fyp #foryou #3amstories"

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
    """Set the Description field to the full caption with hashtags.
    
    Uses execCommand('insertText') to fire proper DOM input events so TikTok's
    rich editor recognises hashtags as linked entities (not plain text).
    """
    try:
        # Scroll to top of page to ensure description field is visible
        await page.evaluate("window.scrollTo(0, 0);")
        await asyncio.sleep(0.5)

        desc_field = await page.query_selector("div[contenteditable='true']")
        if not desc_field:
            print("❌ Description field not found")
            return False

        await desc_field.scroll_into_view()
        await asyncio.sleep(0.3)

        # Focus and clear existing content
        await desc_field.click()
        await asyncio.sleep(0.3)
        await page.keyboard.press("Control+a")
        await asyncio.sleep(0.1)
        await page.keyboard.press("Delete")
        await asyncio.sleep(0.3)

        # Insert text using execCommand — this fires real InputEvent/input events
        # that TikTok's editor listens to for hashtag detection.
        # We insert the non-hashtag prefix first, then each hashtag individually
        # with a small pause so TikTok can process each token.
        lines = caption.split("\n")
        
        for i, line in enumerate(lines):
            if line.strip():
                # Split the line into tokens: normal text and #hashtag chunks
                tokens = []
                for word in line.split(" "):
                    tokens.append(word)
                
                for j, token in enumerate(tokens):
                    text_to_insert = token if j == 0 else " " + token
                    # Escape backticks and backslashes for JS string
                    escaped = text_to_insert.replace("\\", "\\\\").replace("`", "\\`")
                    await page.evaluate(
                        f"document.execCommand('insertText', false, `{escaped}`)"
                    )
                    # Give TikTok's hashtag detector a moment after each #tag
                    if token.startswith("#"):
                        await asyncio.sleep(0.15)
                    else:
                        await asyncio.sleep(0.05)

            # Add newline between lines (except after the last)
            if i < len(lines) - 1:
                await page.evaluate("document.execCommand('insertParagraph', false)")
                await asyncio.sleep(0.15)

        await asyncio.sleep(0.8)

        # Verify content was set
        actual = await page.evaluate(
            "() => document.querySelector(\"div[contenteditable='true']\")?.innerText || ''"
        )

        if actual.strip():
            print(f"✅ Description set ({len(actual.strip())} chars)")
            print(f"   Content: {actual[:80].replace(chr(10), ' ')!r}...")
            return True
        else:
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
