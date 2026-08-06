# FINDINGS.md — Subtraction pass, verdicts, and fixes

**Session rule:** fix by removing, not adding. Every addition paid for by a deletion. When finished, **fewer** interactive elements and **fewer** on-screen numbers than at the start.

---

## 1. The element table (run screen, assumptions panel closed)

Verdicts: **KEEP** · **MERGE** · **DEMOTE** · **DELETE**. The KEEP test: *if this were gone, would User A decide differently, or User C misunderstand the story?* If neither → not a KEEP.

| Element | Who needs it | At what moment | Verdict | Why |
|---|---|---|---|---|
| Mode pill "SEA-TRIAL MODE" | Presenter, room | at the toggle | **DEMOTE + reword** → "TODAY'S CURVE" / "THE MODEL" | "Sea trial" is jargon; not required to act. Keep as context, plain words. |
| Voyage counter "1 / 10" | All three | always | **KEEP** | Progress reduces anxiety; User A paces themselves. |
| Header keyhints "Space·M·R·E" | Presenter | always | **DELETE** | On-screen instructions User A cannot use; presenter is practised. Point-of-action cue replaces it. |
| Assumptions button | Presenter | on a hostile question | **KEEP + strengthen contrast** | The honesty defence (H8). Must be found in one glance. |
| Route name | All three | offer | **KEEP** | The cargo's identity; text, no jargon. |
| Distance (nm) | Room | offer | **DEMOTE** | Sets scale; not decision-critical. One small number. |
| Cargo tonnes | — | offer | **DELETE** | User A never acts on it; flavour only. |
| Recent market $/t | — | offer | **DELETE** | Meaningless pre-decision to a non-broker; the bidding belongs at resolve. |
| Months since drydock (number) | Room | offer | **MERGE → plain-language cue** | H5. "40" means nothing; "hull last cleaned ~3 yrs ago" means everything. Removes a number. |
| Estimate: sea days | — | offer | **DELETE** | Shipping mechanism detail; User A/C don't act on it. |
| Estimate: bunker (mt) | — | offer | **DELETE** | Fuel tonnes are jargon to a non-specialist. |
| Estimate: "Estimated TCE" | All three | offer | **KEEP + reword** → "You'd expect to earn / **+$4,368 a day**" (TCE tiny secondary) | H1. This is the hero number — but in plain words, and the single largest thing. |
| Freight quote $/t (on offer) | — | offer | **MOVE to resolve** | Meaningless without the competitor to compare; belongs to the bidding reveal. |
| [QUOTE] button | All three | offer | **KEEP + reword** → "TAKE THIS CARGO" (primary) | Self-instructing label. |
| [DECLINE] button | — | offer | **DELETE** | H2. Second CTA doubles hesitation. The human desk quotes everything (that is the point); **the model** is what declines the bad ones — that is the product's value, shown in Model mode, not a human button. |
| Resolve tag WON | All three | resolve | **KEEP + amplify** | Winning is clear. |
| Resolve tag LOST | All three | resolve | **KEEP + amplify to match WON** | H3. Must be as loud as winning or it reads as a mis-click. |
| Competitor quote | Room | resolve | **KEEP** | Shows the bidding mechanic (why we win the ones we underpriced). |
| Reveal: actual sea days | — | resolve | **DELETE** | Mechanism detail. |
| Reveal: actual bunker | — | resolve | **DELETE** | Jargon. |
| Reveal: "Realised TCE" | All three | resolve | **KEEP + reword** → "You actually earned / **+$829 a day**" | The second half of the story; hero of the reveal. |
| Reveal: gap figure | Room | resolve | **MERGE into the two numbers** | The gap is *visible* as expected-vs-actual; a third number restates it. |
| Reveal: context (months + weather index) | — | resolve | **DELETE numbers, keep one plain sentence** | "This hull was overdue and the weather was rough" — no figures needed. |
| Chart bars (estimate vs realised) | Room | always | **KEEP — this is the argument** | The one genuinely strong element. |
| Chart y-axis ticks $0/$2k/$4k/$6k | — | always | **DELETE all but the $0 line** | H9. Room reads bar shapes, not values; sub-18px noise. Keep $0 so losses visibly dip below it. |
| Chart x-axis 1..10 | — | always | **DELETE** | Redundant with the voyage counter; ten sub-18px numbers. |
| Chart legend | Room | always | **KEEP + reword** | Words for the colours (not colour alone). |
| Scoreboard: fixtures won "X / Y" | All three | always | **KEEP number, DELETE denominator, reword** → "Cargoes won" | The "/ quoted" denominator is a second number nobody needs. |
| Scoreboard: total realised profit | All three | always | **KEEP + reword** → "Money made" | Plain; a running hero. |
| Scoreboard: avg gap (est − realised) | — | always | **DELETE** | The chart already shows the gap; the summary states it. A third place is clutter. |
| Summary: two 3-number columns | Room | end | **DEMOTE** | Support, not headline. |
| Summary: verdict "4 fewer / $224,864 more" | All three | end | **KEEP + promote to the single largest thing** | H7. This is the punchline; make the money delta the biggest object on the screen. |

---

## 2. Structural fixes (behaviour, not new elements)

- **Pre-play voyage 1 (H4).** On load/reset, voyage 1 is already resolved: the very first thing anyone sees is one completed cargo — *expected +$4,368, actually +$829, won* — and one bar on the chart. This (a) kills the empty cold-open chart, (b) teaches the win/bid/reality mechanic by example before User A must act, and (c) still lets User A generate voyages 2–10 themselves, so the *pattern* is self-discovered by voyage four. Tagged on screen "first cargo — played for you" so it is not mistaken for their own action. It does **not** touch the simulation model or determinism (it only sets `decisions[0]=quote`).
- **Make the toggle the peak (H6).** The summary after the first (today's-curve) run shows **only that run's result** and one unmissable line: *"▶ Press M to run the same ten cargoes with the model."* The model column is withheld until M is pressed — so M *reveals the second column and the punchline* instead of silently re-labelling a header. The turn of the argument now happens on the toggle, where the spec wants the peak.
- **Point-of-action cue replaces the header keyhints.** After every resolve: *"Press Space for the next cargo."* Recognition, at the moment it is needed — not a legend, tooltip, or help layer.

---

## 3. Every finding → the fix applied

| Finding | Fix (in preference order: delete > merge > reword > restyle) |
|---|---|
| **F1 TCE is jargon** | Reword every "TCE" to plain "earn … a day / a day"; keep "TCE" only as a tiny secondary label for the shipping-literate. |
| **F2 no cue, two CTAs** | Delete DECLINE. One primary self-instructing button, "TAKE THIS CARGO". The expected profit shown in green makes taking obviously reasonable — the trap is that it *looks* good. |
| **F3 losing looks broken** | Amplify LOST to the same visual weight as WON — full-width coloured banner, "A rival bid lower — cargo lost", with both bids. Losing is now an event. |
| **F4 empty voyage-1 chart** | Pre-play voyage 1; the room sees a bar and the mechanic immediately, User A still discovers the pattern. |
| **F5 "40 months" meaningless** | Replace the number with a plain state cue: "hull last cleaned ~3 yrs ago — overdue". Removes a number, adds meaning. |
| **F6 toggle looks like settings** | Withhold the model column until M; M now reveals the comparison + punchline. The peak lives on the toggle. |
| **F7 too many numbers / no hero** | Cut the run screen from ~34 numbers to ~10; make the money delta the single largest object on the summary; one dominant number per moment. |
| **F8 assumptions hard to find** | Keep the button, raise its contrast (solid, not outline), so the honesty defence is one glance away. |
| **F9 chart axis noise** | Delete x-axis 1..10 and the $2k/$4k/$6k ticks; keep only the $0 line so losses read as dipping below break-even. |

---

## 4. Invariants re-checked after the changes

- Search for `captain`, `master`, `crew` → **zero hits** (re-run at the end).
- Opens from `file://`, wifi off; no network, no storage, no `Math.random` → unchanged.
- Same seed → identical run → unchanged (the model math in §4 of AIVS-DEMO-001 was **not** touched; only presentation and the pre-play flag).
- Every on-screen number still derives from the Assumptions panel or is labelled illustrative → unchanged.

---

## 5. The count (filled in after implementation — see bottom of this file and the HTML)

Counting scope: the **demo screen** the audience sees during the 90-second run (assumptions panel closed). Numbers are counted as *visible numeric instances* in a given state. The panel itself holds 12 parameter inputs + 3 buttons, **required to stay by AIVS-DEMO-001 invariant 6** (every parameter visible and editable) and hidden during the run — reported separately, unchanged.

### Interactive elements (run screen)

| | Before | After |
|---|---|---|
| Controls | Assumptions · QUOTE · DECLINE | Assumptions · TAKE THIS CARGO |
| **Count** | **3** | **2** |

DECLINE deleted (F2). The human desk now only *takes* cargoes; the discipline of declining the bad ones is what **the model** demonstrates — which is the product, not a button.

### On-screen numbers

| State | Before | After | Removed |
|---|---|---|---|
| Decide | **28** | **6** | cargo tonnes, recent market, months-since-drydock, sea days, bunker, freight quote, 4 y-ticks, 10 x-labels |
| Resolved (won) | **34** | **9** | + actual sea days, actual bunker, gap figure, weather index |
| Summary | **10** | **6** | avg-gap ×2, the "/10" denominators, one profit-column figure each |

Every "after" figure is lower. The busiest run-screen state fell from **34 → 9** numbers; the ending from **10 → 6**.

---

## 6. Acceptance tests — result

- **Ten-second test.** Cold open shows a completed example (bid → won → *expected +$4,368 vs actually +$829*); the next screen is one cargo, one hero number, one button labelled TAKE THIS CARGO. A stranger can state the task without asking. **Pass.**
- **Silent test.** By voyage 3–4 the chart shows expected bars tall, earned bars short, two dipping **below the break-even line** in amber — the pattern reads at four metres with no narration. **Pass.**
- **Clicker test.** Full run on `Space` / `M` / `R` / `E` only; `E` reaches the summary in one keystroke. **Pass.**
- **Peak test.** The model column is *withheld* until `M`; pressing it reveals the $224,864 delta as the largest object on screen. It cannot be mistaken for a filter. **Pass.**
- **Jargon sweep.** Words required for action: "TAKE THIS CARGO", "expect to earn", "+$X a day" — zero jargon. "TCE", "curve", "nm" appear only as secondary labels. **Pass (zero jargon required to act).**
- **The count.** Interactive 3 → 2; numbers 34 → 9 (run), 10 → 6 (summary). **Pass.**
- **Invariants.** `captain`/`master`/`crew` → zero hits; opens from `file://`, no network/storage/`Math.random`; same seed → identical run (canonical still 8/$206,835 vs 4/$431,699, sea-trial realised-below-expected on every won voyage). The §4 model was not touched. **Pass.**

---

## FINAL LINE

**Interactive elements: 3 → 2.  On-screen numbers: 34 → 9 (run screen), 10 → 6 (summary).**
Both numbers in every pair are smaller. The session did its job.

---

# ADDENDUM — stage-hardening pass (driven as User B, on the deployed build)

Run after deployment, driving the live page as the presenter rather than inspecting
state. One finding was severe enough to have killed the demo on stage.

## F10 — the demo ignored every key a presentation clicker sends (CRITICAL)

Only `Space` advanced. Presentation remotes (Logitech, Kensington) emit
`PageDown`/`PageUp`, and some emit arrow keys — **not** `Space`. Measured on the
deployed build before the fix:

| Key a remote emits | Response |
|---|---|
| `PageDown` | none |
| `ArrowRight` / `ArrowDown` | none |
| `Enter` | none |

AIVS-DEMO-001 §6 states the presenter "will be holding a clicker, not a mouse", so
the build contradicted its own stage requirement: clicking the remote would have left
a frozen-looking screen in front of the panel. This is precisely User B's stated fear —
*"a demo that survives nerves, a bad projector"*.

**Fix.** Accept every forward key a remote can emit (`Space`, `PageDown`, `ArrowRight`,
`ArrowDown`, `Enter`, `N`) and every back key (`PageUp`, `ArrowLeft`, `ArrowUp`,
`Backspace`, `P`). No new on-screen element — keys only, so the subtraction count above
is unaffected.

## F11 — forward at the summary did nothing (dead end)

At the first summary the screen says *"Press M to run the same ten cargoes with the
model"*, but the forward button — the one the presenter is already holding down — did
nothing. A press that produces no response reads as a broken demo and invites a second,
harder press.

**Fix.** Forward at the first summary now starts the model run, i.e. it does what the
screen already instructs. **The entire demo is now drivable with the forward button
alone** — verified end to end: 39 presses from cold open to the final comparison, with
the mode switching automatically at press 20. `E` remains the shortcut (≈10 presses to
the punchline).

## F12 — overshooting cost a full reset

There was no way back. A presenter who pressed once too many could only hit `R` and
start the whole run again, on stage, under time pressure.

**Fix.** Back keys step to the previous resolved cargo. This exposed a latent bug: the
scoreboard counted every decided cargo regardless of position, so stepping back left the
money total ahead of the chart. Chart and scoreboard now share one `reachedIndex()`, so
both rewind together (verified: cargoes won 2 → 1 on stepping back).

## F13 — `Esc` did not close the assumptions panel

The panel is the honesty defence, opened mid-question and then in the way.
**Fix.** `Esc` closes it.

## Re-verified after the addendum

- Clicker keys, back-step, `M`, `R`, `E`, `Esc` — all confirmed on the deployed build.
- Typing in the assumptions inputs does not trigger shortcuts.
- No console errors; no page scroll (810 = 810); layout stable.
- **Simulation untouched:** 8 won / \$206,835 → 4 won / \$431,699, delta **\$224,864**,
  realised-below-expected true on every won voyage — identical to the pre-addendum build.

**Not verified by machine:** real clicker hardware. The automation harness can only
dispatch synthetic key events, so the physical remote should be plugged in and run
once before Saturday.
