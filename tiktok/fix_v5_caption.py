#!/usr/bin/env python3
"""Fix v5 caption — hover row, click edit pencil, set caption."""
import asyncio, sys
from playwright.async_api import async_playwright

COOKIES_FILE = "/root/tiktok_3amnarrator_cookies.txt"
SCREENSHOT_DIR = "/home/node/.openclaw/workspace/tiktok"
TARGET_VIDEO_ID = "7616153628788788493"

CAPTION = "What would you do if your GPS led you somewhere that doesn't exist? 👁️\n\n#scarystories #horrortok #3am #creepy #scarytiktok #spooky #horrorstories #fyp #foryou #3amstories"


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
        await asyncio.sleep(0.3)

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
                    await asyncio.sleep(0.2 if token.startswith("#") else 0.05)

            if i < len(lines) - 1:
                await page.evaluate("document.execCommand('insertParagraph', false)")
                await asyncio.sleep(0.15)

        await asyncio.sleep(0.8)

        actual = await page.evaluate(
            "() => document.querySelector(\"div[contenteditable='true']\")?.innerText || ''"
        )
        if actual.strip():
            print(f"✅ Caption set ({len(actual.strip())} chars): {actual[:80].replace(chr(10),' ')!r}...")
            return True
        print("⚠️ Caption appears empty")
        return False

    except Exception as e:
        print(f"❌ Caption insert failed: {e}")
        import traceback; traceback.print_exc()
        return False


async def run():
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

        print("→ Loading content page...")
        await page.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(4)

        # Dismiss any cookie/dialog banners first
        for sel in ["button:has-text('Allow all')", "button:has-text('Decline optional cookies')", "button:has-text('Got it')", "button:has-text('OK')"]:
            try:
                btn = await page.query_selector(sel)
                if btn and await btn.is_visible():
                    await btn.click()
                    print(f"  Dismissed: {sel}")
                    await asyncio.sleep(1)
            except:
                pass

        await asyncio.sleep(2)

        # Find the video link and get its row Y position
        video_link = await page.query_selector(f'a[href*="{TARGET_VIDEO_ID}"]')
        if not video_link:
            print("❌ Video not found on content page")
            await browser.close()
            return False

        bbox = await video_link.bounding_box()
        row_y = bbox['y'] + bbox['height'] / 2
        print(f"  Video row Y: {row_y}")

        # Hover over the video link to reveal action icons
        await video_link.hover()
        await asyncio.sleep(1.2)

        # Move mouse to edit pencil icon (leftmost action icon, ~x=1003)
        edit_x = 1003
        edit_y = row_y
        print(f"→ Moving to edit icon at ({edit_x}, {edit_y})...")
        await page.mouse.move(edit_x, edit_y)
        await asyncio.sleep(0.5)
        await page.screenshot(path=f"{SCREENSHOT_DIR}/fix_on_edit_icon.png")
        print("📸 fix_on_edit_icon.png")

        # Click the edit icon
        await page.mouse.click(edit_x, edit_y)
        await asyncio.sleep(4)
        print(f"  URL after click: {page.url}")
        await page.screenshot(path=f"{SCREENSHOT_DIR}/fix_after_edit_click.png")
        print("📸 fix_after_edit_click.png")

        # Check for description field
        desc_field = await page.query_selector("div[contenteditable='true']")
        if not desc_field:
            # Maybe a modal/panel opened on the same page — check again
            await asyncio.sleep(2)
            desc_field = await page.query_selector("div[contenteditable='true']")

        if not desc_field:
            print("❌ No description field found after click")
            # Show all visible text to debug
            text = await page.evaluate("() => document.body.innerText.substring(0, 500)")
            print(f"  Page text: {text}")
            await browser.close()
            return False

        # Set the caption
        print("→ Setting caption...")
        ok = await insert_caption(page, CAPTION)
        if not ok:
            await browser.close()
            return False

        await page.screenshot(path=f"{SCREENSHOT_DIR}/fix_caption_set.png")
        print("📸 fix_caption_set.png")

        # Save
        print("→ Saving...")
        saved = await page.evaluate("""() => {
            const labels = ['Save', 'Save changes', 'Update', 'Done'];
            const btn = Array.from(document.querySelectorAll('button'))
                .find(b => labels.some(l => b.innerText.trim().toLowerCase().includes(l.toLowerCase())) && !b.disabled);
            if (btn) { btn.click(); return btn.innerText.trim(); }
            // Show all buttons for debugging
            return Array.from(document.querySelectorAll('button'))
                .filter(b => b.offsetParent)
                .map(b => b.innerText.trim()).join(', ');
        }""")
        print(f"  Save result: {saved}")
        await asyncio.sleep(4)
        await page.screenshot(path=f"{SCREENSHOT_DIR}/fix_final.png")
        print("📸 fix_final.png")
        await browser.close()
        return True


if __name__ == "__main__":
    result = asyncio.run(run())
    sys.exit(0 if result else 1)
