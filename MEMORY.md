# MEMORY.md — Long-Term Memory

## GitHub & ProPath Website

- **GitHub token:** `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`
- **Repo:** `https://github.com/dinbotgang/propath-website` (org: `dinbotgang`)
- **Local copy:** `/home/node/.openclaw/workspace/propath/`
- Also stored in `.env` as `GITHUB_TOKEN`


## ProPath Website
- **GitHub repo:** https://github.com/dinbotgang/propath-website
- **GitHub PAT:** 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
- **Netlify PAT:** nfp_AnJvtPdc8MgPBLF7uD3TGoncgZMRb95La68b
- **Netlify Site ID:** 30b972a5-f6f3-4f61-8d1e-80a0e82dc4b4
- **VPS:** 178.156.248.17 — I am running ON this VPS, no SSH needed, use exec directly
- **Resend API Key:** re_NhECp86F_65q2zrnCEMSzkxz22DUwgXfA
- **Stripe Live Secret Key:** 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
- **Airtable Token:** patMCjo9x5XgY6amY.b3dd5cbcc247828b96d2973e99478daf543e87adb558b0fbb9772b41a6cbb76a
- **Airtable Base ID:** app6ufkdTlQUFHu0f
- **Airtable Table:** ProPath Athletes
- **Live site:** https://propathcoach.com
- **Local copy:** `/home/node/.openclaw/workspace/propath/index.html`
- Push via: `git push https://<token>@github.com/dinbotgang/propath-website.git main`

## Polymarket Spread-Arb Bot

**Created:** 2026-02-25

### What It Is
A spread-arbitrage bot that buys YES+NO on the same Polymarket binary market simultaneously, targeting the bid-ask spread. Runs on Hetzner VPS at `178.156.248.17`.

### Critical Config
- **Bot path:** `/root/polymarket-bot/` (source: `src/server.ts`, `src/trader.ts`)
- **Dashboard:** `http://178.156.248.17:8080`
- **Proxy (Germany geoblock bypass):** `http://lsuysski:zsuzuo6md8b7@142.111.67.146:5611`
- **Funder wallet:** `0xf30aaAf3B1ADaa5FCfA941891C8c4e05174B6884`
- **Signer:** `0xc6CD220D744e3CCc7195e544cFf5C27FEc6c59dE`
- **Account slug:** `0xf30aaAf3B1ADaa5FCfA941891C8c4e05174B6884-1771971337765`

### Start / Kill
```bash
# Start
rm -f /tmp/polymarket-bot.lock
nohup /root/polymarket-bot/run.sh > /tmp/polymarket-bot.log 2>&1 &

# Kill
kill -9 $(ps aux | grep run.sh | grep -v grep | awk '{print $2}')
kill $(lsof -ti:8080)
rm -f /tmp/polymarket-bot.lock
```

### Key Parameters
- `sizePerSide = 5` USDC (min $10/pair)
- Balance threshold: $9.80 (sizePerSide*2 - 0.20)
- Market filter: 2–14 days to expiry, price 0.08–0.92, vol24h ≥ $30k, spread ≥ 3%
- Stale order rotation: every 2 min, cancel BUY orders open > 5 min
- PID lock: `/tmp/polymarket-bot.lock`

### Polymarket PnL API (Hard-Won Knowledge)
- Dedicated portfolio endpoints (`/portfolio`, `/portfolio/value`, etc.) all return 404
- **Real PnL data lives in:** `__NEXT_DATA__` on the profile page
  ```
  GET https://polymarket.com/profile/0xf30aaaf3b1adaa5fcfa941891c8c4e05174b6884
  Parse: props.pageProps.dehydratedState.queries
  ```
- **portfolio-pnl query key:** `['portfolio-pnl', slug, wallet, '1D']`  
  → time-series `[{t: unix_timestamp, p: pnl_value}, ...]` (hourly)
- **volume/pnl key:** `['/api/profile/volume', wallet, wallet]`  
  → `{amount, pnl: X, realized: 0, unrealized: 0}` where `pnl` = all-time realized PnL
- These internal Next.js routes return 404 if called directly; must be scraped from page HTML

### NordVPN Warning
DO NOT use NordVPN system-wide on the VPS — it reroutes all traffic including the dashboard port, making it inaccessible externally. The SOCKS5 proxy in `.env` handles API geoblocking only.

### Files
- `data/pnl.json` — PnL store: `{closedPnl, lastAssets, snapshots[]}`
- `.env` — PK, FUNDER_ADDRESS, PORT=8080, SOCKS5_PROXY
- `run.sh` — auto-restart loop with 5s cooldown

## TikTok Video Pipeline

**Created:** 2026-03-10

### Setup
- All settings: `/home/node/.openclaw/workspace/tiktok/SETTINGS.md`
- Video log: `/home/node/.openclaw/workspace/tiktok/VIDEOS.md`
- Output folder: `/home/node/.openclaw/workspace/tiktok/videos/`

### Key Preferences (George)
- **Voice:** Kokoro TTS `bm_lewis`, speed 0.85 — British male, smooth
- **Captions:** Dead center screen (ASS Alignment=5), flashy bold white + thick black outline + drop shadow
- **Background:** Real Minecraft parkour 1080p60 vertical from YouTube
- **YouTube download:** `yt-dlp --cookies /root/yt_cookies.txt --no-js-runtimes --js-runtimes node --extractor-args "youtube:player_client=mediaconnect" -f "299+140"`
- **Minecraft audio:** Keep at ~15% volume under voice for ambiance
- **Story style:** Short creepy horror, punchy sentences, twist ending, ~10 sentences
- **Video length: 25–35 seconds STRICT** — check after voice gen, adjust speed or add/remove sentences if outside range
- **Kokoro models in /tmp** — need re-download after VPS reboot
- **Minecraft footage:** REUSE `/tmp/tiktok-video/minecraft_real.mp4` (702s, `7yl7Wc1dtWc`) — track position in `tiktok/minecraft_progress.json`, read `next_start` before every render, update after. Re-download when running low or file missing from /tmp.
- **Serve for download:** Python HTTP on port 7654, PowerShell `Invoke-WebRequest` to `C:\Users\georg\Downloads\`
