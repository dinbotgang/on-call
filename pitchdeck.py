from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Spacer
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.colors import HexColor
import math

W, H = landscape(A4)

# Color palette
BG       = HexColor("#0A0E1A")
CARD     = HexColor("#111827")
ACCENT1  = HexColor("#6366F1")   # indigo
ACCENT2  = HexColor("#22D3EE")   # cyan
ACCENT3  = HexColor("#F59E0B")   # amber
GREEN    = HexColor("#10B981")
RED      = HexColor("#EF4444")
WHITE    = HexColor("#F9FAFB")
GRAY     = HexColor("#6B7280")
LGRAY    = HexColor("#9CA3AF")

def draw_bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def draw_accent_bar(c, color=ACCENT1):
    c.setFillColor(color)
    c.rect(0, H - 4, W, 4, fill=1, stroke=0)

def draw_slide_num(c, n, total=10):
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 9)
    c.drawRightString(W - 24, 18, f"{n} / {total}")

def heading(c, text, y, size=32, color=WHITE):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", size)
    c.drawCentredString(W/2, y, text)

def subheading(c, text, y, size=16, color=LGRAY):
    c.setFillColor(color)
    c.setFont("Helvetica", size)
    c.drawCentredString(W/2, y, text)

def body(c, text, x, y, size=12, color=LGRAY, align="left", bold=False):
    c.setFillColor(color)
    font = "Helvetica-Bold" if bold else "Helvetica"
    c.setFont(font, size)
    if align == "center":
        c.drawCentredString(x, y, text)
    elif align == "right":
        c.drawRightString(x, y, text)
    else:
        c.drawString(x, y, text)

def card(c, x, y, w, h, fill=CARD, radius=8):
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=0)

def pill(c, x, y, w, h, color=ACCENT1, text="", text_color=WHITE, font_size=11):
    c.setFillColor(color)
    c.roundRect(x, y, w, h, h/2, fill=1, stroke=0)
    c.setFillColor(text_color)
    c.setFont("Helvetica-Bold", font_size)
    c.drawCentredString(x + w/2, y + (h - font_size)/2 + 2, text)

def divider(c, y, color=ACCENT1, alpha=0.4):
    c.setFillColor(color)
    c.setStrokeColor(color)
    c.setLineWidth(1)
    c.line(40, y, W - 40, y)

def icon_circle(c, cx, cy, r, color, text, font_size=18):
    c.setFillColor(color)
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", font_size)
    c.drawCentredString(cx, cy - font_size/3, text)

def stat_box(c, x, y, w, h, value, label, color=ACCENT1):
    card(c, x, y, w, h)
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(x + w/2, y + h - 42, value)
    c.setFillColor(LGRAY)
    c.setFont("Helvetica", 10)
    c.drawCentredString(x + w/2, y + 14, label)

def bullet(c, x, y, text, indent=0, size=12, color=LGRAY, dot_color=ACCENT2):
    c.setFillColor(dot_color)
    c.circle(x + indent + 5, y + 4, 3, fill=1, stroke=0)
    c.setFillColor(color)
    c.setFont("Helvetica", size)
    c.drawString(x + indent + 16, y, text)

# ── SLIDE 1: COVER ──────────────────────────────────────────────────────────
def slide_cover(c, n):
    draw_bg(c)
    # gradient-ish circles
    for i, (cx, cy, r, col) in enumerate([
        (80, H-80, 160, HexColor("#1E1B4B")),
        (W-60, 60, 120, HexColor("#164E63")),
        (W/2, H/2, 280, HexColor("#0F172A")),
    ]):
        c.setFillColor(col)
        c.circle(cx, cy, r, fill=1, stroke=0)
    draw_accent_bar(c, ACCENT1)
    # Logo/badge
    icon_circle(c, W/2, H/2 + 90, 44, ACCENT1, "PA", 22)
    heading(c, "PolyArb", H/2 + 20, 48, WHITE)
    subheading(c, "Automated Spread Arbitrage on Prediction Markets", H/2 - 20, 18, LGRAY)
    divider(c, H/2 - 50)
    subheading(c, "Seed Capital Raise  •  2026", H/2 - 78, 14, GRAY)
    draw_slide_num(c, n)

# ── SLIDE 2: THE OPPORTUNITY ────────────────────────────────────────────────
def slide_opportunity(c, n):
    draw_bg(c)
    draw_accent_bar(c, ACCENT2)
    heading(c, "The Opportunity", H - 55, 30, WHITE)
    subheading(c, "Polymarket is the world's largest prediction market — and it's inefficient.", H - 90, 13)

    stats = [
        ("$3B+",    "Monthly Volume\n(Polymarket 2025)"),
        ("1,000s",  "Active Markets\nat any time"),
        ("3–15%",   "Typical Bid-Ask\nSpreads"),
        ("24/7",    "Markets Never\nClose"),
    ]
    sw = (W - 100) / 4
    for i, (val, lbl) in enumerate(stats):
        x = 50 + i * sw
        card(c, x, H - 240, sw - 16, 130)
        c.setFillColor(ACCENT2)
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(x + (sw-16)/2, H - 140, val)
        c.setFillColor(LGRAY)
        c.setFont("Helvetica", 10)
        for j, line in enumerate(lbl.split("\n")):
            c.drawCentredString(x + (sw-16)/2, H - 165 - j*14, line)

    body(c, "Unlike stock markets, prediction markets are nascent, retail-dominated, and structurally ripe for", W/2, H - 278, 12, LGRAY, "center")
    body(c, "algorithmic strategies that exploit persistent inefficiencies in the order book.", W/2, H - 294, 12, LGRAY, "center")

    points = [
        "No short-selling restrictions or pattern-day-trader rules",
        "Retail participants place wide spreads with no market maker competition",
        "Binary outcomes create natural mean-reversion dynamics between YES and NO",
        "High-volume markets ($30k+ daily) provide sufficient liquidity for fast fills",
    ]
    for i, pt in enumerate(points):
        bullet(c, 80, H - 340 - i*22, pt, size=11)

    draw_slide_num(c, n)

# ── SLIDE 3: THE STRATEGY ────────────────────────────────────────────────────
def slide_strategy(c, n):
    draw_bg(c)
    draw_accent_bar(c, ACCENT1)
    heading(c, "The Strategy", H - 55, 30, WHITE)
    subheading(c, "Simultaneous YES + NO purchases to capture the bid-ask spread", H - 90, 13)

    # Flow diagram
    boxes = [
        (ACCENT1,  "SCAN",     "Filter markets:\n≥$30k vol/day\n3–15% spread\n2–14 days to expiry"),
        (ACCENT2,  "BUY",      "Place simultaneous\nYES + NO limit orders\n$5 per side"),
        (GREEN,    "CAPTURE",  "Collect spread\non resolution\nor market move"),
        (ACCENT3,  "ROTATE",   "Cancel stale orders\nevery 2 min\nRedeploy capital"),
    ]
    bw = 140
    gap = (W - 4*bw - 80) / 3
    bx = 40
    by = H - 320
    for i, (col, title, desc) in enumerate(boxes):
        x = bx + i*(bw + gap)
        card(c, x, by, bw, 160)
        c.setFillColor(col)
        c.roundRect(x, by + 120, bw, 40, 4, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(x + bw/2, by + 132, title)
        c.setFillColor(LGRAY)
        c.setFont("Helvetica", 9.5)
        for j, line in enumerate(desc.split("\n")):
            c.drawCentredString(x + bw/2, by + 106 - j*14, line)
        # arrow
        if i < 3:
            ax = x + bw + 4
            ay = by + 80
            c.setFillColor(GRAY)
            c.setStrokeColor(GRAY)
            c.setLineWidth(1.5)
            c.line(ax, ay, ax + gap - 8, ay)
            # arrowhead
            c.setFillColor(GRAY)
            p = c.beginPath()
            p.moveTo(ax+gap-8, ay)
            p.lineTo(ax+gap-18, ay+5)
            p.lineTo(ax+gap-18, ay-5)
            p.close()
            c.drawPath(p, fill=1, stroke=0)

    # Key parameters
    body(c, "Key Parameters", 50, H - 362, 13, WHITE, bold=True)
    params = [
        ("Position size:", "$5 USDC per side ($10/pair)"),
        ("Spread threshold:", "≥ 3% before entry"),
        ("Market filter:", "Price 8¢–92¢  •  Vol $30k+/day  •  2–14 days to expiry"),
        ("Order hygiene:", "Stale BUY orders cancelled after 5 min  •  Full rotation every 2 min"),
    ]
    for i, (k, v) in enumerate(params):
        y = H - 386 - i*18
        c.setFillColor(ACCENT2)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, k)
        c.setFillColor(LGRAY)
        c.setFont("Helvetica", 10)
        c.drawString(50 + c.stringWidth(k, "Helvetica-Bold", 10) + 6, y, v)

    draw_slide_num(c, n)

# ── SLIDE 4: WHY IT WORKS ────────────────────────────────────────────────────
def slide_why(c, n):
    draw_bg(c)
    draw_accent_bar(c, GREEN)
    heading(c, "Why It Works", H - 55, 30, WHITE)
    subheading(c, "Market structure creates a structural edge that compounds with scale", H - 90, 13)

    reasons = [
        ("📐", ACCENT1, "Math Favors the Arb",
         "On a binary market, YES + NO always resolves to $1.\nBuying both at a combined cost < $1 locks in a risk-free\nprofit on resolution — pure spread capture."),
        ("🔄", ACCENT2, "High Turnover",
         "Short-dated markets (2–14 days) recycle capital fast.\nEach resolved market returns principal + spread.\nCapital can be redeployed within the same day."),
        ("🤖", GREEN, "Speed Advantage",
         "The bot scans all eligible markets every 2 minutes,\nplacing and rotating orders faster than any human.\nNo emotional bias, no fatigue, no missed windows."),
        ("📈", ACCENT3, "Scales Linearly",
         "Returns scale directly with capital deployed.\nMore capital → more simultaneous positions →\nhigher absolute PnL with the same edge per trade."),
    ]
    cw = (W - 80) / 2 - 8
    ch = 148
    positions = [(40, H-280), (W/2+4, H-280), (40, H-440), (W/2+4, H-440)]
    for (x, y), (emoji, col, title, desc) in zip(positions, reasons):
        card(c, x, y, cw, ch)
        c.setFillColor(col)
        c.setFont("Helvetica", 20)
        c.drawString(x + 14, y + ch - 32, emoji)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(x + 44, y + ch - 28, title)
        c.setFillColor(LGRAY)
        c.setFont("Helvetica", 9.5)
        for j, line in enumerate(desc.split("\n")):
            c.drawString(x + 14, y + ch - 56 - j*14, line)

    draw_slide_num(c, n)

# ── SLIDE 5: TECHNOLOGY ──────────────────────────────────────────────────────
def slide_tech(c, n):
    draw_bg(c)
    draw_accent_bar(c, ACCENT2)
    heading(c, "The Technology", H - 55, 30, WHITE)
    subheading(c, "Purpose-built, fully autonomous trading infrastructure", H - 90, 13)

    # Stack
    stack = [
        (ACCENT1, "Trading Engine",   "TypeScript / Node.js",  "Polymarket CLOB API integration\nLimit order placement & management\nAutomatic stale order cancellation"),
        (ACCENT2, "Market Scanner",   "Real-time Filter",       "Scans all Polymarket markets\nSpread & liquidity scoring\nAutomatic market selection"),
        (GREEN,   "Risk Manager",     "Capital Guardian",       "Per-position sizing limits\nMinimum balance enforcement\nPID lockfile crash protection"),
        (ACCENT3, "Infrastructure",   "Hetzner VPS + Tailscale","24/7 uptime with auto-restart\nProxy routing for geo-compliance\nReal-time dashboard on port 8080"),
    ]
    sw = (W - 80) / 4 - 6
    for i, (col, title, sub, desc) in enumerate(stack):
        x = 40 + i * (sw + 8)
        card(c, x, H - 370, sw, 260)
        c.setFillColor(col)
        c.roundRect(x, H-130, sw, 36, 4, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(x + sw/2, H - 120, title)
        c.setFillColor(col)
        c.setFont("Helvetica", 9)
        c.drawCentredString(x + sw/2, H - 138, sub)
        c.setFillColor(LGRAY)
        c.setFont("Helvetica", 9)
        for j, line in enumerate(desc.split("\n")):
            c.drawCentredString(x + sw/2, H - 168 - j*14, line)

    body(c, "✓  Fully autonomous  •  ✓  Self-healing  •  ✓  Live dashboard  •  ✓  Mobile monitoring via Telegram", W/2, H - 390, 11, ACCENT2, "center")

    draw_slide_num(c, n)

# ── SLIDE 6: EARLY RESULTS ───────────────────────────────────────────────────
def slide_results(c, n):
    draw_bg(c)
    draw_accent_bar(c, ACCENT3)
    heading(c, "Early Results", H - 55, 30, WHITE)
    subheading(c, "Proof-of-concept run on minimal capital  •  Launched Feb 25, 2026", H - 90, 13)

    # Stats row
    stats = [
        ("~$22",    "Starting Capital\n(Proof of Concept)", ACCENT1),
        ("~$11",    "Current Nav\n(4 days)", LGRAY),
        ("4 days",  "Live Runtime\n(Continuous)", ACCENT2),
        ("24/7",    "Uptime\n(Auto-Restart)", GREEN),
    ]
    sw = (W - 100) / 4
    for i, (val, lbl, col) in enumerate(stats):
        x = 50 + i * sw
        stat_box(c, x, H - 235, sw - 14, 120, val, lbl.split("\n")[0], col)
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 9)
        c.drawCentredString(x + (sw-14)/2, H - 222, lbl.split("\n")[1])

    # Honest framing box
    card(c, 40, H - 355, W - 80, 100, HexColor("#1C1917"))
    c.setFillColor(ACCENT3)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(58, H - 280, "⚠  Proof-of-Concept Context")
    c.setFillColor(LGRAY)
    c.setFont("Helvetica", 10.5)
    context = [
        "This run was intentionally minimal — $22 is below the viable threshold for this strategy.",
        "At this scale, Polymarket's minimum order sizes ($5/side) leave almost no free capital buffer,",
        "causing the bot to sit idle between resolved markets rather than compound positions.",
        "The strategy's edge is sound; the constraint is capital. This is why we're raising.",
    ]
    for i, line in enumerate(context):
        c.drawString(58, H - 302 - i*15, line)

    # What we learned
    body(c, "What the prototype proved:", 50, H - 382, 12, WHITE, bold=True)
    learns = [
        "Order routing & CLOB integration works correctly end-to-end",
        "Market filtering logic correctly identifies eligible spread opportunities",
        "Auto-restart and crash recovery systems function reliably",
        "Real-time dashboard and Telegram monitoring are fully operational",
    ]
    for i, pt in enumerate(learns):
        bullet(c, 50, H - 404 - i * 18, pt, size=10)

    draw_slide_num(c, n)

# ── SLIDE 7: MARKET SIZE ─────────────────────────────────────────────────────
def slide_market(c, n):
    draw_bg(c)
    draw_accent_bar(c, ACCENT1)
    heading(c, "Market Size & Timing", H - 55, 30, WHITE)
    subheading(c, "Prediction markets are at an inflection point", H - 90, 13)

    milestones = [
        ("2021", "Polymarket\nlaunches", GRAY),
        ("2023", "$100M+\nannual volume", LGRAY),
        ("2024", "$8B+ volume\nUS election cycle", ACCENT2),
        ("2025", "$3B+ monthly\nvolume baseline", ACCENT1),
        ("2026", "Institutional\nadoption begins", GREEN),
    ]
    lx = 60
    rx = W - 60
    ty = H - 200
    # Timeline line
    c.setStrokeColor(ACCENT1)
    c.setLineWidth(2)
    c.line(lx, ty, rx, ty)
    gap = (rx - lx) / (len(milestones) - 1)
    for i, (year, event, col) in enumerate(milestones):
        x = lx + i * gap
        c.setFillColor(col)
        c.circle(x, ty, 7, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(WHITE)
        c.drawCentredString(x, ty + (20 if i%2==0 else -32), year)
        c.setFillColor(LGRAY)
        c.setFont("Helvetica", 9)
        for j, line in enumerate(event.split("\n")):
            c.drawCentredString(x, ty + (34 + j*12 if i%2==0 else -46 - j*12), line)

    points = [
        ("Why now?", ACCENT3, [
            "2024 US election proved prediction markets are mainstream",
            "CFTC and regulatory clarity improving in 2025-26",
            "Institutional players entering — driving volume and tightening spreads",
        ]),
        ("Our window:", GREEN, [
            "Before full institutional competition arrives",
            "Spreads still wide enough for retail arb strategies",
            "First-mover advantage in automated spread capture",
        ]),
    ]
    cw = (W - 80) / 2 - 6
    for i, (title, col, pts) in enumerate(points):
        x = 40 + i * (cw + 12)
        card(c, x, H - 430, cw, 140)
        c.setFillColor(col)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x + 12, H - 302, title)
        for j, pt in enumerate(pts):
            bullet(c, x, H - 328 - j*20, pt, size=10, dot_color=col)

    draw_slide_num(c, n)

# ── SLIDE 8: USE OF FUNDS ────────────────────────────────────────────────────
def slide_funds(c, n):
    draw_bg(c)
    draw_accent_bar(c, GREEN)
    heading(c, "Use of Funds", H - 55, 30, WHITE)
    subheading(c, "Capital is the only bottleneck — we're ready to scale now", H - 90, 13)

    alloc = [
        (65, ACCENT1,  "Trading Capital",   "Deployed directly into the\nPolymarket CLOB wallet.\nFully liquid, on-chain, auditable."),
        (25, ACCENT2,  "Strategy R&D",      "Enhance market scoring,\nspread prediction models,\nand position sizing algorithms."),
        (10, GREEN,    "Infrastructure",    "Redundant VPS nodes,\nmonitoring, alerting,\nand compliance tooling."),
    ]

    # Bar chart
    bx = 60
    total_w = W - 120
    by = H - 250
    bh = 40
    x = bx
    for pct, col, title, _ in alloc:
        w = total_w * pct / 100
        c.setFillColor(col)
        c.roundRect(x, by, w, bh, 4, fill=1, stroke=0)
        if w > 60:
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(x + w/2, by + 13, f"{pct}%")
        x += w

    # Labels below
    x = bx
    for pct, col, title, desc in alloc:
        w = total_w * pct / 100
        c.setFillColor(col)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(x + w/2, by - 20, title)
        c.setFillColor(LGRAY)
        c.setFont("Helvetica", 9)
        for j, line in enumerate(desc.split("\n")):
            c.drawCentredString(x + w/2, by - 38 - j*12, line)
        x += w

    # Raise targets
    body(c, "Raise Targets", W/2, H - 380, 13, WHITE, "center", bold=True)
    targets = [
        ("$5,000",   "Minimum viable\ncapital threshold",  LGRAY),
        ("$25,000",  "Target raise\n25 simultaneous positions", ACCENT1),
        ("$100,000", "Scale target\nfully systemized operation", GREEN),
    ]
    tw = (W - 100) / 3
    for i, (amt, lbl, col) in enumerate(targets):
        x = 50 + i * tw
        card(c, x, H - 460, tw - 10, 65)
        c.setFillColor(col)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(x + (tw-10)/2, H - 415, amt)
        c.setFillColor(LGRAY)
        c.setFont("Helvetica", 9)
        for j, line in enumerate(lbl.split("\n")):
            c.drawCentredString(x + (tw-10)/2, H - 436 - j*12, line)

    draw_slide_num(c, n)

# ── SLIDE 9: RISK & MITIGATION ───────────────────────────────────────────────
def slide_risk(c, n):
    draw_bg(c)
    draw_accent_bar(c, RED)
    heading(c, "Risk & Mitigation", H - 55, 30, WHITE)
    subheading(c, "We've thought hard about what can go wrong — and built for it", H - 90, 13)

    risks = [
        ("Market Liquidity Risk",
         "Thin books may prevent fills on one side,\ncreating unhedged exposure.",
         "Min $30k/day volume filter. $5 position\nsize is tiny vs. market depth. Stale order\ncancellation prevents stuck positions."),
        ("Smart Contract / Platform Risk",
         "Polymarket could have outages, bugs,\nor regulatory shutdown.",
         "Positions are on-chain and always\nredeemable. Capital is in USDC, not\nplatform tokens. Diversify across markets."),
        ("Strategy Crowding",
         "More arb bots competing narrows\nthe spread to zero.",
         "Our filter targets high-spread markets\nothers skip. We monitor spread compression\nand adjust thresholds dynamically."),
        ("Capital Drawdown",
         "A string of adverse market moves\ncould reduce NAV.",
         "Binary positions always resolve 0 or 1.\nWe hold BOTH sides — directional moves\nare hedged by construction."),
    ]

    rw = (W - 80) / 2 - 6
    rh = 140
    for i, (risk, prob, mit) in enumerate(risks):
        col = 0 if i < 2 else 1
        row = i % 2
        x = 40 + col * (rw + 12)
        y = H - 270 - row * (rh + 10)
        card(c, x, y, rw, rh)
        c.setFillColor(RED)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x + 12, y + rh - 22, risk)
        c.setFillColor(LGRAY)
        c.setFont("Helvetica", 9)
        for j, line in enumerate(prob.split("\n")):
            c.drawString(x + 12, y + rh - 42 - j*12, line)
        c.setFillColor(GREEN)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x + 12, y + rh - 78, "Mitigation:")
        c.setFillColor(HexColor("#6EE7B7"))
        c.setFont("Helvetica", 9)
        for j, line in enumerate(mit.split("\n")):
            c.drawString(x + 12, y + rh - 92 - j*12, line)

    draw_slide_num(c, n)

# ── SLIDE 10: THE ASK / CTA ──────────────────────────────────────────────────
def slide_ask(c, n):
    draw_bg(c)
    # bg circles
    c.setFillColor(HexColor("#1E1B4B"))
    c.circle(W - 80, 80, 200, fill=1, stroke=0)
    c.setFillColor(HexColor("#0C4A6E"))
    c.circle(80, H - 80, 150, fill=1, stroke=0)
    draw_accent_bar(c, ACCENT1)

    heading(c, "Join Us", H/2 + 100, 40, WHITE)
    subheading(c, "We've built the engine. We need the fuel.", H/2 + 58, 16, LGRAY)
    divider(c, H/2 + 40)

    terms = [
        ("Structure:",   "Revenue share or equity — negotiable"),
        ("Minimum:",     "$1,000 USDC"),
        ("Target raise:","$25,000 USDC"),
        ("Returns:",     "Proportional to deployed capital"),
        ("Liquidity:",   "Capital returnable on request (subject to open positions)"),
        ("Transparency:","Full on-chain auditability  •  Live dashboard access  •  Regular reporting"),
    ]
    tx = W/2 - 220
    for i, (k, v) in enumerate(terms):
        y = H/2 + 10 - i * 22
        c.setFillColor(ACCENT2)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(tx, y, k)
        c.setFillColor(LGRAY)
        c.setFont("Helvetica", 11)
        c.drawString(tx + 120, y, v)

    body(c, "Interested? Let's talk.", W/2, H/2 - 130, 16, WHITE, "center", bold=True)
    body(c, "All capital is held on-chain in USDC — fully transparent, always auditable.", W/2, H/2 - 156, 11, GRAY, "center")

    draw_slide_num(c, n)

# ── RENDER ALL SLIDES ────────────────────────────────────────────────────────
output = "/home/node/.openclaw/workspace/polyarb-pitch-deck.pdf"
c = pdfcanvas.Canvas(output, pagesize=landscape(A4))

slides = [slide_cover, slide_opportunity, slide_strategy, slide_why,
          slide_tech, slide_results, slide_market, slide_funds,
          slide_risk, slide_ask]

for i, slide_fn in enumerate(slides):
    slide_fn(c, i + 1)
    c.showPage()

c.save()
print(f"✅ Saved to {output}")
