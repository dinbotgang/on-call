# On Call — Tech Stack Options

## Decision Pending — Options Below

---

## Option A: React Native + Supabase (Recommended for MVP speed)

### Frontend
- **React Native** (Expo) — single codebase for iOS + Android
- **React Navigation** — native navigation
- **Zustand** — lightweight state management
- **React Native Maps** — Google Maps integration
- **Reanimated** — swipe/card animations (Tinder-style deck)

### Backend
- **Supabase** — Postgres DB + Auth + Realtime (WebSockets for live availability)
- **Supabase Edge Functions** — serverless logic (job matching, notifications)
- **Stripe + Stripe Connect** — payments + worker payouts
- **Expo Push Notifications** — job alerts

### Infrastructure
- Supabase handles hosting/scaling for MVP
- Move to dedicated infra if/when needed

---

## Option B: Flutter + Firebase

### Frontend
- **Flutter** — fast UI, excellent animations, one codebase
- Better performance than RN for complex UI (swipe cards, maps)

### Backend
- **Firebase Firestore** — real-time DB
- **Firebase Auth** — phone/email
- **Firebase Cloud Functions** — server logic
- **Stripe** — payments

---

## Option C: Web-First MVP (Fastest to validate)

- **Next.js** — web app (mobile-responsive)
- **Supabase** — DB + auth + realtime
- **Stripe** — payments
- **Vercel** — hosting

> Rationale: Skip app store delays. Validate the concept via web first, then build native apps with learnings.

---

## Recommended Approach

**Start with Option C (Web MVP)** to validate demand quickly, then build native with Option A once PMF signals emerge.

- No app store approval delays
- Faster iteration cycles
- Same Supabase backend carries forward to native apps
- Workers can use mobile browser for basic availability toggling

---

## Key Integrations Needed

| Service | Purpose | Cost |
|---|---|---|
| Stripe Connect | Worker payouts | 2.9% + 30¢ per transaction |
| Checkr | Background checks | ~$25/worker |
| Twilio | SMS notifications | ~$0.0079/message |
| Google Maps | Location, routing | Pay-per-use |
| Expo / APNs / FCM | Push notifications | Free |
| Cloudinary | Worker photo storage | Free tier → $89/mo |

---

Last updated: 2026-03-11
