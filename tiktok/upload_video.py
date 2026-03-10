#!/usr/bin/env python3
"""
TikTok Upload Script — 3AM Narrator
Algorithm-optimized posting with shadowban protection.
"""

import json
import sys
from tiktok_uploader.upload import upload_video

# ── ALGORITHM-OPTIMIZED CAPTION ───────────────────────────────────────────────
# Strategy:
# - Opens with a question → drives comments (boosts engagement signal)
# - Short, punchy — doesn't get cut off in feed
# - Question at end → keeps viewers engaged in comments section
# - NO banned hashtags, NO copyrighted claims

CAPTION = """Would you have taken the stairs? 😰

#scarystories #horrortok #3am #creepy #scarytiktok #spooky #horrorstories #fyp #foryou #3amstories"""

# ── SHADOWBAN PROTECTION RULES ────────────────────────────────────────────────
# ✅ Original audio (Kokoro TTS + Minecraft ambience) — no copyright issues
# ✅ No copyrighted music
# ✅ No banned hashtags (verified clean list below)
# ✅ No spam posting (max 1-2/day on new account)
# ✅ Hashtag mix: broad + niche + FYP signals
# ✅ No watermarks from other platforms
# ✅ Video under 60s (TikTok prefers shorter on new accounts)

# ── HASHTAG STRATEGY ──────────────────────────────────────────────────────────
# Tier 1 — Massive reach (100M+ views): #fyp #foryou #scary
# Tier 2 — Mid (10M-100M views): #scarystories #horrortok #creepy #spooky
# Tier 3 — Niche (1M-10M): #3am #horrorstories #3amstories #scarytiktok
# Total: 10 hashtags (sweet spot — not spammy, enough signal)

VIDEO_PATH = "/home/node/.openclaw/workspace/tiktok/videos/tiktok_v4.mp4"
COOKIES_PATH = "/root/tiktok_account1_cookies.txt"

print("Uploading to TikTok...")
print(f"Video: {VIDEO_PATH}")
print(f"Caption: {CAPTION[:80]}...")

try:
    upload_video(
        filename=VIDEO_PATH,
        description=CAPTION,
        cookies=COOKIES_PATH,
        headless=True,
        wait=5
    )
    print("✅ Upload successful!")
except Exception as e:
    print(f"❌ Upload failed: {e}")
    sys.exit(1)
