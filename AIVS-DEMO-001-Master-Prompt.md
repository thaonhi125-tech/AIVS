# AIVS-DEMO-001 — Master Prompt: The Voyage Pricing Simulator

**Version:** v1.0 | **Date:** 2026-08-06 | **Status:** ACTIVE
**Parent document:** AIVS-MASTER-001 v1.1 (the pitch). This document inherits all of its invariant rules.
**Purpose:** build one interactive HTML artefact that a team member runs live, on stage, for 90 seconds, during a 15-minute pitch on Saturday 8 August 2026.

---

## 0. HOW TO USE THIS DOCUMENT

Paste this entire file as the first message in a Claude Code session. Then say: **"Build Phase 1."** Do not skip to Phase 3. Phases are ordered so that stopping early still leaves something presentable.

This is a two-day build for a live stage demo. Every constraint below exists because a demo that fails on stage is worse than no demo.

---

## 1. INVARIANT RULES — violating any one of these makes the build wrong

**Inherited from the pitch:**

1. The organisation is a **dry bulk shipowner/manager**, 30 Handysize vessels, trading **mostly spot / voyage charter**.
2. The money is lost in **mispriced voyage estimates**, not in time-charter performance claims.
3. Noon reports **already arrive structured**. Never depict document scanning, OCR, or "AI reading messy PDFs."
4. **Hindcast weather is not ground truth.** It is a second imperfect instrument. Never display it as "the real weather" against which a report is checked.
5. **No crew-blame framing anywhere.** No master names, no crew identifiers, no "reported vs actual" comparison at person level, no accuracy score attached to a human. Not in the UI, not in the code, not in variable names. If a variable is called `captainError`, the build is wrong.
6. **No invented numbers presented as real.** Every parameter in the simulation must be visible and editable in an Assumptions panel, and the screen must state that these are illustrative parameters, not company data.

**Specific to this build:**

7. **Single self-contained `.html` file. No network at any point.** No CDN, no Google Fonts, no `fetch`, no external images. It must run correctly by double-clicking the file from a USB stick with wifi switched off. This is not a preference — venue wifi fails, and if the demo needs a CDN it dies in front of the panel.
8. **Deterministic.** A seeded PRNG. The same seed produces the same ten voyages every single time. The presenter rehearses on Friday and gets the identical run on Saturday. Never `Math.random()`.
9. **No storage APIs.** No `localStorage`, no `sessionStorage`, no cookies. State lives in JS variables only.
10. **No framework, no build step.** Vanilla JS, one file, opens in any modern browser.

---

## 2. WHAT WE ARE BUILDING, AND WHY

### The one sentence

> An audience member plays the chartering desk for ten voyages using the old sea trial curve, watches money leak, then replays the same ten voyages with the model — and discovers they **win fewer cargoes but earn more money**.

### Why this specific interaction

The hardest claim in our pitch is counter-intuitive: *a better model makes our quotes less attractive, we lose fixtures, and that is the project working.* Said out loud, a panel disbelieves it. Bet on it themselves for ninety seconds and they prove it to themselves.

The demo must land three things in this order:

1. **The error only points one way.** Realised cost is always above estimate, never below.
2. **Adverse selection.** The cargoes we win are the ones we priced worst — this emerges from the mechanics, it is not asserted.
3. **The adoption valley.** Turning on the model reduces the win count. The audience feels the discomfort before they see the payoff.

If the finished artefact does not produce those three realisations in order, it has failed, no matter how polished it looks.

---

## 3. SCREEN SPEC

One page, three regions, no routing, no scrolling during the demo.

```
┌──────────────────────────────────────────────────────────────────┐
│  HEADER: mode indicator  ·  voyage counter  ·  assumptions toggle │
├────────────────────────────────┬─────────────────────────────────┤
│  LEFT — THE CARGO ON OFFER     │  RIGHT — THE RUNNING BOOK       │
│                                │                                 │
│  route, distance, cargo, hull  │  cumulative chart               │
│  age since drydock             │  estimated vs realised TCE      │
│                                │  per voyage, as bars            │
│  YOUR ESTIMATE (from curve):   │                                 │
│    voyage days · bunker · TCE  │  SCOREBOARD                     │
│    → your freight quote        │   fixtures won                  │
│                                │   total realised profit         │
│  [ QUOTE ]      [ DECLINE ]    │   avg gap: estimate − realised  │
│                                │                                 │
│  → then reveal: WHAT HAPPENED  │                                 │
└────────────────────────────────┴─────────────────────────────────┘
```

### Flow, per voyage

1. **Offer.** A cargo appears: route name, distance in nm, cargo tonnes, freight rate on offer, and **months since last drydock** for the assigned vessel.
2. **Estimate.** The panel shows what the current curve predicts: sea days, bunker tonnes, estimated TCE.
3. **Decide.** Two buttons: `QUOTE` or `DECLINE`. In Phase 1 the user just presses QUOTE — the decision matters in Phase 2.
4. **Market resolves.** A competing quote is revealed. You win the fixture if your quote is the lower one.
5. **Reality runs.** If won, show actual sea days, actual bunker, actual TCE, and the gap — **the gap is always negative in sea-trial mode, and the audience must be able to see that pattern by voyage four.**
6. **Book updates.** The chart gains a bar. The scoreboard updates.

After ten voyages, a summary screen. Then the mode toggle becomes available.

### The two modes

| | **SEA TRIAL MODE** (start here) | **MODEL MODE** |
|---|---|---|
| Estimate uses | fixed trial curve + flat weather margin | curve corrected for this hull's age, with a confidence band |
| Typical result | wins a lot, realised TCE below estimate every time | wins less, realised TCE ≈ estimated |
| What the audience sees | steady leak | fewer bars, but taller and honest |

**Critical:** replaying MODEL MODE must use **the identical ten cargoes** — same seed, same routes, same hull ages, same competing quotes. Otherwise the comparison proves nothing and a sharp panel member will say so.

---

## 4. THE SIMULATION MODEL — implement exactly this, do not improvise

All parameters live in one `ASSUMPTIONS` object at the top of the file, all editable in the UI, all labelled *illustrative*.

### Vessel and curve

```
v_trial      = 13.0    kn      // sea trial speed
c_trial      = 22.0    mt/day  // sea trial ME consumption at v_trial
k_foul       = 0.004   /month  // consumption penalty per month since drydock (~4.8%/yr)
s_foul       = 0.0015  /month  // speed loss fraction per month since drydock
m_weather    = 0.09            // consumption penalty per unit of weather index
s_weather    = 0.035           // speed loss fraction per unit of weather index
margin_desk  = 0.05            // the flat weather margin the desk already adds today
```

### Per voyage

```
h        = months since drydock            (seeded, 0..60)
W        = weather index for the voyage    (seeded, 0..3, mean ≈ 1.2)
D        = distance, nm
port_days= fixed per route

// what actually happens
v_actual    = v_trial * (1 - s_foul*h - s_weather*W)
c_actual    = c_trial * (1 + k_foul*h) * (1 + m_weather*W)
days_actual = D / (24 * v_actual)
fuel_actual = days_actual * c_actual

// SEA TRIAL MODE estimate  — note the margin is FLAT, so it under-corrects old hulls
days_est = (D / (24 * v_trial)) * (1 + margin_desk)
fuel_est = days_est * c_trial   * (1 + margin_desk)

// MODEL MODE estimate — corrected for this hull's age, blind to this voyage's weather
v_model    = v_trial * (1 - s_foul*h - s_weather*W_expected)   // W_expected = 1.2
c_model    = c_trial * (1 + k_foul*h) * (1 + m_weather*W_expected)
days_est   = D / (24 * v_model)
fuel_est   = days_est * c_model
band       = ±(confidence, widens with h and with coastal routes)
```

> **The flat desk margin is the most important line of code in this file.** It is why the error grows with hull age: a constant 5 % cushion over-corrects a freshly docked hull and badly under-corrects one at fifty months. That single mechanic produces the entire argument. Do not replace it with a margin that scales.

### Economics

```
revenue        = freight_rate * cargo_tonnes
voyage_costs   = fuel * bunker_price + port_costs
total_days     = sea_days + port_days
TCE            = (revenue - voyage_costs) / total_days
```

### Winning the fixture

```
our_quote        = break_even_rate(estimate) * (1 + target_margin)
competitor_quote = seeded, drawn around the true market rate
we win  if  our_quote <= competitor_quote
```

This is the mechanism that produces adverse selection **without asserting it**: an optimistic estimate lowers our quote, so we win exactly the voyages we understood least well. Let the mechanic do the arguing.

### Determinism

Use `mulberry32` seeded with a fixed constant. Every seeded draw — hull age, weather, competitor quote — comes from that one stream, consumed in a fixed order. Add a visible seed field so the presenter can rehearse and, if asked by the panel, change it live to show the result is not cherry-picked. **That last capability is a strong answer to a hostile question; build it.**

---

## 5. VISUAL SYSTEM — match the deck exactly

```
INK      #0E2438   background (dark, so it does not blind a dark room)
INK2     #17334D   cards
TEAL     #1C7293   model / good / leading indicators
AMBER    #C9702A   the leak, the loss, the risk
GREEN    #2E7D68   realised gain
MIST     #EEF3F6   light text panels
FADE     #B9C7D2   muted text on dark
WHITE    #FFFFFF
```

- Headers: `Cambria, Georgia, serif`. Body: `Calibri, "Segoe UI", system-ui, sans-serif`. **System fonts only — no webfonts, they need the network.**
- Body text minimum **18px**; the numbers that matter minimum **40px**. This is read from the back of a room, not from a laptop.
- Target 1920×1080; must remain readable and unbroken at 1366×768.
- Charts: hand-rolled inline **SVG**. No chart library — every one of them needs a CDN.
- Animation: nothing longer than 400ms. Stage time is expensive.

---

## 6. STAGE-USE REQUIREMENTS

These are not nice-to-haves. Each one exists because of a specific way live demos fail.

- **Keyboard control:** `Space` = next / advance, `M` = toggle mode, `R` = reset, `E` = jump straight to the summary. The presenter will be holding a clicker, not a mouse.
- **`E` (jump to end) is mandatory.** If the pitch is running long, the presenter must be able to reach the punchline in one keystroke.
- **A visible reset that returns to voyage one, same seed.** Rehearse, present, reset, present again.
- **Nothing may depend on a random outcome.** Same seed, same story, every time.
- **No error state visible to the audience.** Wrap the render loop in a try/catch that fails to a static summary rather than a blank screen.
- **Assumptions panel** toggleable from the header, showing every parameter with its value and the words *illustrative — not company data*. When the panel asks "where did these numbers come from", the presenter opens this and hands the question back honestly.

---

## 7. BUILD PHASES — stop wherever time runs out

**Phase 1 — the spine (build this first, it is the demo).**
One page. Ten voyages in sea trial mode. Offer → estimate → resolve → reality → book. The cumulative chart. The scoreboard. Keyboard control. Deterministic seed. If only Phase 1 exists on Saturday, the demo still works.

**Phase 2 — the reveal.**
Mode toggle. Replay the identical ten cargoes with the model curve. Side-by-side summary: fixtures won, total realised profit, average estimate-to-realised gap. **This is where "we win less and earn more" becomes visible.** Add the confidence band to the model estimate.

**Phase 3 — optional, only if Phase 1 and 2 are finished and rehearsed.**
The normalisation toy: a slider for how strict the good-weather filter is. As it tightens, usable data points collapse from ~40 to ~5 and the fitted curve's confidence band balloons. Flip to "normalise" and all points return, band tightens. This is slide 7 made playable. **Do not start Phase 3 on Friday night.**

---

## 8. WHAT NOT TO BUILD

- No login, no backend, no database, no API.
- No fake AI chat, no simulated LLM output, no typing animation pretending a model is thinking.
- No 3D ship, no map animation, no particle effects, no sound.
- No crew or master data of any kind — see invariant 5.
- No dashboard of twenty metrics. Four numbers on the scoreboard, maximum.
- No mobile layout. This runs on a projector.
- No dark-pattern polish that consumes the two days: skip favicons, skip loading screens, skip settings pages.

---

## 9. ACCEPTANCE CHECKLIST — run before Saturday

- [ ] Opens correctly from `file://` with wifi disabled
- [ ] Same seed produces an identical run, three times in a row
- [ ] In sea trial mode, realised TCE is **below** estimated TCE on every won voyage — no exceptions
- [ ] By voyage four, the one-directional pattern is visible without being explained
- [ ] Model mode wins **fewer** fixtures and produces **higher** total realised profit on the same ten cargoes
- [ ] `Space`, `M`, `R`, `E` all work; the demo is completable without a mouse
- [ ] Every number on screen is either derived from the assumptions panel or labelled illustrative
- [ ] Search the source for `captain`, `master`, `crew`, `blame`, `honest`, `accurate` — **zero hits**
- [ ] Body text readable from four metres on a 1080p projector
- [ ] Full run, offer to summary, completes in **under 90 seconds** with a practised presenter

---

## 10. WHERE THIS SITS IN THE PITCH

Slide 5 of the deck is *"We don't lose randomly. We win the cargoes we priced worst."* That slide currently asserts adverse selection with a static graphic.

**Replace that slide with the live demo.** Ninety seconds. The presenter hands the clicker to a panel member for the first three voyages, takes it back, and runs to the summary.

Suggested spoken frame, before starting:

> "Rather than tell you our estimates are biased, I would like you to run our chartering desk for ninety seconds. These are our assumptions, they are on the screen, and you can change any of them."

And after the mode toggle:

> "Same ten cargoes. Same weather. You just won four fewer, and made more money. That is the project working — and it is also the six months where it looks like the project failing."

Then straight into slide 8, the adoption valley. The demo sets it up; the slide pays it off.

---

## 11. CHANGELOG

- **v1.0 — 2026-08-06** — Initial. Scope deliberately limited to one hero interaction after judging that three demos in a 15-minute pitch would produce three weak ones. The flat desk margin was chosen as the core mechanic because it generates the hull-age-dependent error without needing to assert it.
