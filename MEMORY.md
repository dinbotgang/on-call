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

## Polymarket Esports Betting Bot

**Created:** 2026-02-25 | **Last updated:** 2026-03-10

### What It Is
An **esports betting bot** on Polymarket. Monitors live **Valorant (VCT), CS2, and Dota2** matches via VLR.gg API, detects in-game events (pistol wins, eco wins, map wins, economy swings, barracks fall, kill streaks, etc.) and places directional trades on Polymarket. Runs on Hetzner VPS at `178.156.248.17`.

**Source files:** `/root/polymarket-bot/src/` — `valorant.ts`, `cs2.ts`, `dota2.ts`, `server.ts`, `trader.ts`

### Critical Config
- **Bot path:** `/root/polymarket-bot/` (source: `src/server.ts`, `src/trader.ts`, `src/dota2.ts`, `src/cs2.ts`)
- **Dashboard:** `http://178.156.248.17:8080`
- **Proxy (Switzerland - Zurich, geoblock bypass):** `http://lsuysski:zsuzuo6md8b7@191.101.121.193:6467`
  - VPS is in Virginia (US) — cannot access Polymarket esports markets without proxy
  - Proxy used ONLY for Polymarket API calls, not system-wide (NordVPN warning still applies)
- **Funder wallet:** `0xf30aaAf3B1ADaa5FCfA941891C8c4e05174B6884`
- **Signer:** `0xc6CD220D744e3CCc7195e544cFf5C27FEc6c59dE`
- **State file:** `/root/polymarket-bot/data/esports_state.json`
- **Lockfile:** `/tmp/polymarket-bot.lock` (canonical — do not change)

### Start / Kill
```bash
# Start / Stop / Restart — use systemd (NOT nohup manually)
systemctl start polymarket-bot
systemctl stop polymarket-bot
systemctl restart polymarket-bot
systemctl status polymarket-bot

# Logs
tail -f /tmp/polymarket-bot.log
```
⚠️ DO NOT use `nohup bash run.sh` manually — systemd service (`polymarket-bot.service`) manages the bot. Running manually creates a competing process because systemd's `Restart=always` (RestartSec=5) will keep trying to start and fail the flock, spamming "Bot already running" into the log.

### Key Parameters & Architecture
- **`calcSize(price)`** — helper in `server.ts`: always returns **6 tokens** (flat). CLOB `size` param = TOKEN count, NOT USDC — critical gotcha! Sending USDC as token count caused all low-price orders to fail (e.g. price 0.225 → $1.35 USDC sent as 1.35 tokens → rejected). 6 tokens costs $price*6 USDC, always above Polymarket's 5-share sell minimum
- **`TRADE_SIZE_USDC`** — configured to $1, but `calcSize` overrides upward when needed
- **`pendingGameIds`** — Set that locks a gameId the moment a signal fires (before async order), preventing duplicate trades
- **CLOB `createAndPostOrder` size** — size param is in **TOKEN units** (not USDC). For BUY: `size * price = USDC spent`. Common gotcha!
- **Minimum order sizes on Polymarket:** BUY = $1 USDC minimum; SELL = 5 shares minimum
- **Dota 2 spectator filter:** `MIN_DOTA2_SPECTATORS=5` (set in .env) — skips 0-viewer pub games, tracks anything with at least 5 spectators
- **Auto-approve:** `ensureCollateralAllowance()` before BUY, `ensureConditionalAllowance()` + fresh `updateBalanceAllowance()` before every SELL
- **Market matching:** `findMarketForTeams()` requires BOTH team names to have a unique word match (stopwords: team, gaming, esports, club, the, and)
- **Polymarket tag slugs (CRITICAL):** CS2 markets use BOTH `counter-strike` AND `counter-strike-2` tags. Must query both or ~30% of CS2 markets are missed. Current slug list: `['esports', 'dota-2', 'counter-strike', 'counter-strike-2', 'valorant', 'league-of-legends']`

### Grid.gg API (replaces PandaScore — 2026-03-11)
- **API Key:** `ZD00KtvLrCENS95kbG9TL3B0YSpAlAtCtxiJEM5c`
- **Stored in:** `/root/polymarket-bot/.env` as `GRID_API_KEY`
- **Intended use:** CS2 (and potentially Valorant/LoL) live match data
- **Status:** Key authenticates (x-api-key header) but gets PERMISSION_DENIED on live data feed endpoints — likely needs premium/enterprise plan activated by Grid.gg for live CS2 game state access
- **Central Data GraphQL:** `https://api.grid.gg/central-data/graphql`
- **Live Data Feed:** `https://api.grid.gg/live-data-feed/series-state` (requires elevated permissions)
- **PandaScore removed** — was used for Valorant live data, now gone from `.env`

### Active Games (User Preference — 2026-03-10)
- **LoL:** ✅ ENABLED
- **Dota 2:** ✅ ENABLED
- **CS2:** ❌ DISABLED (user preference — `pollCS2()` commented out in server.ts)
- **Valorant:** ❌ DISABLED (user preference — VCT matches filtered out in `getLiveMatches()`)

### CS2 Status
- Infrastructure built (`src/cs2.ts`) with HLTV scorebot WebSocket for real-time round data
- **Blocked:** HLTV.org is Cloudflare-protected — `getLiveMatches()` fails with Access Denied
- **Fix (TODO):** Use a scraping API for match discovery, scorebot WebSocket is fine for live data
- **Currently disabled by user preference**

### Telegram Trade Notifications
- Set up via `HEARTBEAT.md` — checks `data/esports_state.json` on each heartbeat
- State tracked in `memory/bot-trade-state.json` (notifiedIds array)
- Sends entry reason on open, PnL on close
- Cost guard: if daily spend > $3 on notifications, auto-disables and alerts George

### Hard-Won Lessons
- **Duplicate trades:** Fixed with `pendingGameIds` Set — add before placeOrder, remove after push/fail
- **Partial close:** If position has < 5 shares, can't sell. Top-up approach: buy more shares, but be careful — `size` is tokens not USDC, and min buy is $1 USDC. To avoid: always use `calcSize` with 6 share minimum
- **"delayed" orders:** Polymarket CLOB returns `status: "delayed"` for accepted orders — need to poll balance to confirm fill, not just check response
- **Conditional allowance:** Must call `updateBalanceAllowance({ asset_type: CONDITIONAL, token_id })` before every SELL, not just once

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

## On Call App

**Created:** 2026-03-11

### What It Is
A two-sided marketplace app concept — Uber meets Hinge for contract work (handymen, bartenders, movers, lawn care, etc.). Austin TX beta target. Concept docs at `/home/node/.openclaw/workspace/on-call/`.

### Assets Built
- `on-call/CONCEPT.md` — full concept, categories, UX flows, business model
- `on-call/landing/index.html` — marketing landing page
- `on-call/app-store/index.html` — 5 App Store screenshot mockups (iPhone 14 Pro, dark theme)
- `on-call/demo/index.html` — interactive web demo (not hosted)

### React Native App
- **Location:** `/home/node/.openclaw/workspace/on-call/rn/`
- **Stack:** Expo SDK 54, React Navigation (stack + bottom tabs), `@expo/vector-icons` Ionicons, custom Avatar component
- **Theme:** dark (`#0a0a0a` bg), accent orange `#FF5C00`, hire blue `#3B82F6`, work green `#22c55e`

#### Screens
- **ModeSelect** — entry, choose Hire or Work mode
- **Hire:** HireHome → WorkerList → WorkerProfile → BookingConfirm → ActiveJob
- **Work:** WorkHome → JobPing → JobNavigation → JobComplete
- Placeholders: MyJobs, HireProfile, Earnings, WorkProfile, Jobs

#### Key components
- `src/components/Avatar.js` — colored initials circles, hash-based palette per name (no emoji faces)
- `src/theme.js` — design tokens

#### Running the dev server
```bash
cd /home/node/.openclaw/workspace/on-call/rn
npx expo start --tunnel --port 8082
```
- User tests via **Expo Go** on iPhone — no Apple Dev account needed
- Tunnel URL changes on restart; check ngrok: `curl -s http://localhost:4040/api/tunnels`
- Compatible with **Expo Go SDK 54** (App Store version as of 2026-03-11)

#### Notes
- Do NOT use emojis for icons — all replaced with Ionicons + Avatar initials
- SafeAreaView deprecation warning is cosmetic only

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
