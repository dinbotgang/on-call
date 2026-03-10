---
name: propath
description: Full context and workflows for ProPath Coaching (propathcoach.com) — elite youth soccer mentorship platform. Use when working on the ProPath website, enrollment system, Airtable, Stripe, Resend emails, VPS deployment, SEO, content strategy, or business growth. Triggers on mentions of ProPath, propathcoach, coaches Efetobo Aror or William Cornog or Richard Paulus, George Summers, or any task involving the coaching site.
metadata:
  author: ProPath Coaching
  version: 1.0.0
---

# ProPath Coaching Skill

## Infrastructure

| Service | Detail |
|---|---|
| VPS | `178.156.248.17` — exec directly, no SSH needed |
| Site root | `/var/www/propathcoach/` |
| Source | `/home/node/.openclaw/workspace/propath/` |
| GitHub repo | `https://github.com/dinbotgang/propath-website` |
| GitHub PAT | `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` |
| PM2 process | `propath-enrollment` on port 3001 |
| Nginx | `/etc/nginx/sites-available/propathcoach` → copy to sites-enabled |
| Nginx binary | `/usr/sbin/nginx` (not in PATH) |

## API Keys

| Service | Credential |
|---|---|
| Airtable Token | `patMCjo9x5XgY6amY.b3dd5cbcc247828b96d2973e99478daf543e87adb558b0fbb9772b41a6cbb76a` |
| Airtable Base | `app6ufkdTlQUFHu0f` / Table: `ProPath Athletes` |
| Resend | `re_NhECp86F_65q2zrnCEMSzkxz22DUwgXfA` |
| Stripe Live | `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` |
| Google Analytics | `G-H8M15B78P1` |
| Google Search Console | Verified via TXT record |

## Stripe Products (all have 90-day free trial)
- Essential $23/mo: `price_1T9FSJPPcAV4qesXbz5XgecZ` / `plink_1T9FSQPPcAV4qesXy9n3u46a`
- Pro $45/mo: `price_1T9FSKPPcAV4qesXtZ4Nan7P` / `plink_1T9FSRPPcAV4qesXjrrUOi49`
- Elite $90/mo: `price_1T9FSKPPcAV4qesXXqrmM05w` / `plink_1T9FSRPPcAV4qesXaPuONul3`

## Standard Deploy
```bash
# Edit → deploy → push
cp /home/node/.openclaw/workspace/propath/index.html /var/www/propathcoach/
cd /tmp/propath-website && git add -A && \
  git commit -m "message" && \
  git push https://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@github.com/dinbotgang/propath-website.git main
```

## Restart Server
```bash
pm2 stop propath-enrollment
pm2 start /var/www/propathcoach/server.js --name "propath-enrollment" \
  --env AIRTABLE_TOKEN=patMCjo9x5XgY6amY.b3dd5cbcc247828b96d2973e99478daf543e87adb558b0fbb9772b41a6cbb76a \
  --env AIRTABLE_BASE_ID=app6ufkdTlQUFHu0f \
  --env RESEND_API_KEY=re_NhECp86F_65q2zrnCEMSzkxz22DUwgXfA \
  --env STRIPE_SECRET_KEY=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
pm2 save
```

## Nginx
```bash
/usr/sbin/nginx -t && /usr/sbin/nginx -s reload
# Port 443 bound to 178.156.248.17 explicitly (Tailscale conflict on 0.0.0.0:443)
```

## Key Business Context
- **Coaches:** Efetobo Aror (MLS draft story = viral content), William Cornog (NCAA Champ), Richard Paulus (NASM)
- **Tiers:** Essential $23/mo (monthly check-in), Pro $45/mo (bi-weekly), Elite $90/mo (weekly + recruiting)
- **Status:** Pre-order mode — 90-day Stripe trial, no charge until launch
- **First customer:** George Summers (Elite tier)
- **Emails:** team@propathcoach.com (notifications), hello@propathcoach.com (contact)

## Current Outstanding TODOs
- Coach photos (Efetobo, William, Richard) — #1 priority
- Stripe business name: change "Richard Paulus" → "ProPath Coaching" in Stripe dashboard
- Instagram + TikTok accounts (@propathcoach)
- Email drip: Day 3 "Meet coaches", Day 7 "What to expect"
- Referral program

## Common Errors
| Error | Fix |
|---|---|
| Site down | `pm2 status` + `ss -tlnp \| grep 443` |
| Nginx won't bind 443 | Tailscale holds 0.0.0.0:443 — use `listen 178.156.248.17:443 ssl;` |
| Airtable 422 | Field name is `Athlete Status` not `Status` |
| Emails not sending | Check Resend key + DNS records in Squarespace |

## Airtable Fields
`Athlete First Name`, `Athlete Last Name`, `Athlete Age`, `Sport / Position`, `Team / Club`, `Parent Name`, `Parent Phone`, `Parent Email`, `Program Tier`, `Referral Source`, `Signup Date`, `Next Check-up`, `Athlete Status` (Trial/Active/Cancelled), `Notes`
