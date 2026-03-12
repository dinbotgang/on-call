#!/usr/bin/env python3
"""
TikTok Studio — edit caption on an already-posted video.
Uses execCommand('insertText') so hashtags are properly linked.
"""
import asyncio, sys

COOKIES_FILE = "/root/tiktok_3amnarrator_cookies.txt"
VIDEO_ID     = "7615872151874211085"
SCREENSHOT_DIR = "/home/node/.openclaw/workspace/tiktok"

# Same caption, hashtags will now be properly linked
CAPTION = "Would you have taken the stairs? 😰\n\n#scarystories #horrortok #3am #creepy #scarytiktok #spooky #horrorstories #fyp #foryou #3amstories"


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


async def insert_caption(page, caption: str) -> bool:
    """Insert caption using execCommand so TikTok recognises hashtags."""
    try:
        await page.evaluate("window.scrollTo(0, 0);")
        await asyncio.sleep(0.5)

        desc_field = await page.query_selector("div[contenteditable='true']")
        if not desc_field:
            print("❌ Description field not found")
            return False

        await desc_field.scroll_into_view()
        await asyncio.sleep(0.3)
        await desc_field.click()
        await asyncio.sleep(0.3)

        # Clear existing content
        await page.keyboard.press("Control+a")
        await asyncio.sleep(0.1)
        await page.keyboard.press("Delete")
        await asyncio.sleep(0.3)

        lines = caption.split("\n")
        for i, line in enumerate(lines):
            if line.strip():
                words = line.split(" ")
                for j, token in enumerate(words):
                    text_to_insert = token if j == 0 else " " + token
                    escaped = text_to_insert.replace("\\", "\\\\").replace("`", "\\`")
                    await page.evaluate(
                        f"document.execCommand('insertText', false, `{escaped}`)"
                    )
                    # Pause after each hashtag so TikTok's detector fires
                    await asyncio.sleep(0.2 if token.startswith("#") else 0.05)

            if i < len(lines) - 1:
                await page.evaluate("document.execCommand('insertParagraph', false)")
                await asyncio.sleep(0.15)

        await asyncio.sleep(0.8)

        actual = await page.evaluate(
            "() => document.querySelector(\"div[contenteditable='true']\")?.innerText || ''"
        )
        if actual.strip():
            print(f"✅ Caption set ({len(actual.strip())} chars): {actual[:60].replace(chr(10),' ')!r}...")
            return True
        print("⚠️ Caption appears empty")
        return False

    except Exception as e:
        print(f"❌ Caption insert failed: {e}")
        import traceback; traceback.print_exc()
        return False


async def edit_video():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled", "--disable-dev-shm-usage"]
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

        # ── Navigate to Studio content manager ───────────
        edit_url = f"https://www.tiktok.com/tiktokstudio/content"
        print(f"→ Loading TikTok Studio content page...")
        await page.goto(edit_url, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(5)

        await page.screenshot(path=f"{SCREENSHOT_DIR}/edit_01_content_page.png")
        print("📸 edit_01_content_page.png")

        # ── Find the video and click its Edit button ──────
        print(f"→ Looking for video {VIDEO_ID}...")

        # Try direct edit URL first
        direct_edit = f"https://www.tiktok.com/tiktokstudio/video/edit/{VIDEO_ID}"
        print(f"→ Trying direct edit URL: {direct_edit}")
        await page.goto(direct_edit, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(5)

        await page.screenshot(path=f"{SCREENSHOT_DIR}/edit_02_edit_page.png")
        print("📸 edit_02_edit_page.png")

        page_text = await page.evaluate("() => document.body.innerText")

        # Check if we're on an edit page with a description field
        desc_field = await page.query_selector("div[contenteditable='true']")
        if not desc_field:
            print("⚠️ No editable field on direct URL — trying content page approach...")
            # Fall back: content page, find the video card and click Edit
            await page.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(4)

            # Look for a link/button containing the video ID or an Edit button
            clicked = await page.evaluate(f"""() => {{
                // Try to find a link with the video ID
                const links = Array.from(document.querySelectorAll('a'));
                const link = links.find(a => a.href && a.href.includes('{VIDEO_ID}'));
                if (link) {{ link.click(); return 'link'; }}

                // Try any Edit button on the first video card
                const btns = Array.from(document.querySelectorAll('button'));
                const editBtn = btns.find(b => b.innerText.trim().toLowerCase() === 'edit');
                if (editBtn) {{ editBtn.click(); return 'button'; }}
                return null;
            }}""")
            print(f"  Fallback click result: {clicked}")
            await asyncio.sleep(4)
            await page.screenshot(path=f"{SCREENSHOT_DIR}/edit_03_fallback.png")
            print("📸 edit_03_fallback.png")

        # ── Set the caption ───────────────────────────────
        print("→ Setting caption with proper hashtag events...")
        ok = await insert_caption(page, CAPTION)
        if not ok:
            await page.screenshot(path=f"{SCREENSHOT_DIR}/edit_fail.png")
            await browser.close()
            return False

        await page.screenshot(path=f"{SCREENSHOT_DIR}/edit_04_caption_set.png")
        print("📸 edit_04_caption_set.png")

        # ── Click Save / Update ───────────────────────────
        print("→ Looking for Save button...")
        saved = await page.evaluate("""() => {
            const labels = ['Save', 'Save changes', 'Update', 'Done'];
            const btn = Array.from(document.querySelectorAll('button'))
                .find(b => labels.some(l => b.innerText.trim().toLowerCase().includes(l.toLowerCase())) && !b.disabled);
            if (btn) { btn.click(); return btn.innerText.trim(); }
            return null;
        }""")
        if saved:
            print(f"✅ Clicked '{saved}'")
        else:
            print("⚠️ No Save button found — listing all buttons:")
            btns = await page.evaluate("""() =>
                Array.from(document.querySelectorAll('button'))
                    .filter(b => b.offsetParent !== null)
                    .map(b => b.innerText.trim())
            """)
            print(f"  Buttons: {btns}")

        await asyncio.sleep(4)
        await page.screenshot(path=f"{SCREENSHOT_DIR}/edit_05_final.png")
        print("📸 edit_05_final.png")

        content = await page.evaluate("() => document.body.innerText")
        success = any(s in content.lower() for s in ["saved", "updated", "success", "changes saved"])
        print("✅ Edit saved!" if success else "⚠️ Unclear if saved — check edit_05_final.png")

        await browser.close()
        return success


if __name__ == "__main__":
    result = asyncio.run(edit_video())
    sys.exit(0 if result else 1)
