# On Call — Product Roadmap

## Phase 0 — Foundation (Pre-Build)
- [x] Define target launch city → **Austin, TX**
- [x] Define MVP job categories → **Lawn care, Handyman, Event bartender/server, Moving help, Cleaning**
- [ ] Decide tech stack (leaning web-first MVP → React Native for native apps)
- [ ] Competitive analysis (TaskRabbit, Thumbtack, Handy, Bark)
- [ ] User interviews — 10 hirers + 10 workers (Austin locals)
- [ ] Wireframes (hiring flow + worker flow)
- [ ] Brand identity — name lock, logo, color palette
- [ ] Legal: contractor vs employee classification research (gig economy)
- [x] **Landing page** — dual signup (hire / work), collect city + top category

## Phase 1 — MVP (First Buildable Thing)
Goal: Prove that workers and hirers can match and complete a job end-to-end.

**Hirers can:**
- [ ] Sign up + set location
- [ ] Browse available nearby workers (basic list)
- [ ] View worker profile (photo, skills, rate, rating)
- [ ] Send a booking request
- [ ] Pay in-app via Stripe
- [ ] Rate the worker after

**Workers can:**
- [ ] Sign up + set skills + hourly rate + radius
- [ ] Toggle availability on/off
- [ ] Receive + accept/decline booking requests
- [ ] See job details + hirer location
- [ ] Mark job complete
- [ ] Get paid (Stripe Connect)

**Backend:**
- [ ] Auth (email/phone)
- [ ] Real-time availability/job matching (WebSockets or Supabase realtime)
- [ ] Push notifications (job requests, acceptance, reminders)
- [ ] Basic admin panel (flag users, handle disputes)

## Phase 2 — Polish & Trust
- [ ] Background check integration (Checkr or Sterling)
- [ ] ID verification
- [ ] Rich Hinge-style worker profiles (photo carousel, prompts)
- [ ] Mutual ratings + written reviews
- [ ] In-app chat (pre/during job)
- [ ] Job photo proof (worker uploads completion photo)
- [ ] Cancellation policy + fees

## Phase 3 — Growth & Scale
- [ ] Swipe/card stack discovery UI
- [ ] Map view of nearby workers
- [ ] "Schedule ahead" bookings (not just on-demand)
- [ ] Worker "Pro" subscription tier
- [ ] Boost / featured placement for jobs
- [ ] Referral program (hirers + workers)
- [ ] Category expansion (launch with 5, grow to full list)
- [ ] iOS + Android polished apps

## Phase 4 — Network Effects
- [ ] Teams / crews (book a 2-person snow crew)
- [ ] Repeat booking ("Book same worker again")
- [ ] Favorites list
- [ ] Worker portfolio (photos of past work)
- [ ] Seasonal job alerts ("Snow workers near you are available")
- [ ] Corporate/event accounts

---

## Prioritization Framework (RICE)

| Feature | Reach | Impact | Confidence | Effort | Score |
|---|---|---|---|---|---|
| Landing page (waitlist) | High | High | High | Low | 🔴 P0 |
| Real-time availability toggle | High | High | High | Low | 🔴 P0 |
| In-app payments (Stripe) | High | High | High | Med | 🔴 P0 |
| Worker profiles | High | High | High | Med | 🔴 P0 |
| Push notifications | High | High | High | Low | 🔴 P0 |
| Austin Tier 1 categories (5) | High | High | High | Low | 🔴 P0 |
| Background checks | Med | High | High | Med | 🟠 P1 |
| In-app chat | Med | Med | High | Med | 🟠 P1 |
| Austin Tier 2 categories (5) | Med | High | High | Low | 🟠 P1 |
| Swipe UI | Med | Med | Med | High | 🟡 P2 |
| Map view | Med | Med | High | High | 🟡 P2 |
| Scheduling | High | Med | Med | High | 🟡 P2 |
| National city expansion | High | High | Med | High | 🟡 P2 |
| Worker subscriptions | Low | High | Med | Med | 🟢 P3 |

---

Last updated: 2026-03-11
