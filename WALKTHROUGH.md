# WALKTHROUGH.md — Cold-open logs (before any change)

**Build audited:** AIVS-DEMO-001-Voyage-Pricing-Simulator.html (Phase 1 + 2, pre-audit)
**Method:** Ran the real file in a browser, drove each state, inspected the rendered screen at four metres and up close. The rule for this log: describe only what a stranger sees. Never write "then they click QUOTE" without justifying *why they would know to*. Where I cannot justify it, that is a finding (tagged →FINDING-n, resolved in FINDINGS.md).

---

## PASS 1 — User A, the panel member handed the clicker (cold, watched, non-shipping)

Screen at handover: voyage 1, "decide" state. Left column: cargo card + estimate card + two buttons. Right column: an almost-empty chart and a scoreboard of zeros.

```
[t+0s]  Screen: "THE CARGO ON OFFER — Santos → Qingdao", four labelled
        numbers, then "YOUR ESTIMATE — SEA-TRIAL CURVE + FLAT MARGIN",
        three more numbers, a freight quote, and buttons [QUOTE] [DECLINE].
        Trying to: work out what they are being asked to do.
        → Looks at first: the biggest thing on screen — "$4,368/day",
          labelled "Estimated TCE".
        → Hesitates: "TCE?" Two-plus seconds. It is the largest word on the
          card and they do not know it. They do not want to ask, thirty
          people are watching.                                   →FINDING-1
        → Gets wrong: nothing yet, because they have not acted.
        VERDICT: friction. The headline number is labelled in jargon.

[t+4s]  Screen: unchanged. Trying to: choose a button.
        → Looks at: [QUOTE] and [DECLINE], equal weight, side by side.
        → Hesitates: "Which one is right? What happens if I decline? Is
          declining the safe answer or the wrong answer?" No cue anywhere
          tells them what either does or which a competent person picks.
          Two equal calls to action = doubled hesitation, in public. ~4s.
                                                                  →FINDING-2
        VERDICT: friction. Two competing actions, no cue, while watched.

[t+8s]  Trying to: sanity-check the numbers to feel safe before pressing.
        → Reads "Months since drydock 40". Means nothing to them. Is 40 a
          lot? A little? Good ship or bad ship? No cue.            →FINDING-5
        → Reads "Recent market $36.93/t" vs "Your freight quote $30.76/t".
          *Might* infer "we are cheaper, cheaper is good" — but only if
          they already think like a shipbroker. Not safe to assume.
        VERDICT: friction. Nothing here helps a non-specialist decide.

[t+12s] Decides to press QUOTE — but only because it is on the left and
        sounds active, not because anything told them to. I cannot honestly
        justify that they *knew* to. → That is FINDING-2.
        → Screen changes: a green "FIXTURE WON" tag, then a block of new
          numbers (actual sea days, actual bunker, "Realised TCE $829/day",
          a gap figure), plus a bar appears on the chart.
        → Reaction: "Something happened, good." But the reveal is again
          dense and jargon-led; they latch onto "$829" being smaller than
          "$4,368" without being sure that is the point.
        VERDICT: clear-ish that an outcome occurred; unclear what it means.

[t+16s] Presses again (the hint says Space). Voyage 2 resolves similarly:
        estimate high, realised lower. By now they *feel* a direction but
        could not name it — the two big numbers are both labelled "TCE".

--- Later, a LOST voyage (voyage 3) ---
[t+Xs]  Screen: after pressing, a small grey tag "FIXTURE LOST" appears,
        low-contrast, roughly the size of the panel subtitle. The estimate
        card above it is unchanged.
        → Reaction: "Did that work? Did I press the wrong thing?" The lost
          outcome is quieter than the won outcome, so it reads as a
          non-event or a mis-click rather than "the market beat you."
                                                                  →FINDING-3
        VERDICT: friction bordering on broken. Losing must be as loud as
        winning, or it reads as a bug the panelist caused.

Overall User A: acts, but from momentum, not comprehension. Feels *tested*
(jargon they don't know, a choice with no guidance), which is the opposite
of the "I discovered the bias myself" feeling the spec demands.
```

---

## PASS 2 — User B, the presenter (ninety seconds, one attempt, clicker only)

```
[pre]   Knows the four keys. Header shows "Space advance · M mode · R reset
        · E end", which is reassuring but is also clutter the audience sees.
[t+0s]  Space, Space, Space — advances voyages. Works. Confirmation is
        instant (<100ms). Good. Clicker-only run is achievable.  VERDICT: clear.
[t+30s] Hands clicker to a panelist. Panelist stalls on FINDING-1/2 above.
        Presenter has to break silence and explain "TCE means profit per
        day, just press QUOTE" — i.e. narrates around a screen that should
        have carried itself. The explanation costs stage time and undercuts
        "you discovered it."                                      →FINDING-1/2
[t+50s] Takes clicker back. No state confusion — the voyage counter tells
        them where they are. VERDICT: clear. (Progress indicator works.)
[t+60s] Reaches the end. Presses M to switch to the model. The switch just
        quietly re-labels the header pill and restarts at voyage 1. It looks
        like a settings toggle, not the turn of the argument.     →FINDING-6
        VERDICT: friction. The emotional peak looks like a filter.
[t+75s] Panel asks "where did these numbers come from?" Presenter needs the
        Assumptions panel. There *is* a button top-right, but under stage
        light it is a low-contrast outline among header text; a nervous
        presenter hunts for it for a beat.                        →FINDING-8
[t+85s] If running long, presses E — jumps straight to summary. Works well.
        VERDICT: clear. (E is a genuine strength; keep it.)
```

---

## PASS 3 — User C, the room (four metres, silent, never touches it)

```
[t+0s]  Voyage 1. The chart has one short bar and reads as *empty*. Nothing
        to compare against; no pattern is possible with one point. The room
        cannot yet see any argument.                              →FINDING-4
        VERDICT: friction. Cold chart wastes the opening seconds.
[t+8s]  Several numbers are emphasised at once — "Estimated TCE", the freight
        quote, and the scoreboard figures all compete. From four metres it
        is unclear which number is *the* number.                  →FINDING-7
        VERDICT: friction. No single dominant number per moment.
[t+20s] By voyage 3–4 the pattern (realised bar always shorter than the
        estimate bar, some dipping below zero) does start to read from four
        metres — the colour + the below-zero dip carries it. This is the
        strongest part of the build. VERDICT: clear (once enough bars exist).
[t+40s] Chart axis shows "$0 $2k $4k $6k" and "1..10". From four metres these
        tick labels are unreadable sub-18px noise; the room reads the bar
        *shapes*, not the values. The axis numbers earn nothing.  →FINDING-9
[t+55s] Summary screen: two columns, three numbers each, plus a verdict with
        two more. Six-to-ten numbers at once. The punchline ("more money on
        fewer cargoes") is present but is one line among many, not the
        single largest thing.                                     →FINDING-7
        VERDICT: friction. The ending dilutes its own punchline.
```

---

## What the walkthrough confirms / rejects (see FINDINGS.md for fixes)

- **H1 TCE is jargon** — CONFIRMED. It is the largest word on the screen and User A does not know it.
- **H2 no cue for the decision** — CONFIRMED. Two equal buttons, no guidance, User A guesses.
- **H3 losing looks like a broken button** — CONFIRMED. Lost is a quiet grey tag; won is a loud green reveal.
- **H4 voyage 1 has nothing to compare** — CONFIRMED. One bar reads as empty; the room gets nothing for the first seconds.
- **H5 "40 months since drydock" is meaningless** — CONFIRMED. No cue whether it is good or bad.
- **H6 the toggle is the peak but looks like settings** — CONFIRMED. M silently re-labels; no sense of an argument turning.
- **H7 too many numbers / no single hero** — CONFIRMED, on both the run screen and the summary.
- **H8 assumptions panel is the honesty defence but hard to find** — CONFIRMED (mild). It exists, but is low-contrast under stage light.
- **New — H9 chart axis labels earn nothing** — the room reads bar shapes, not tick values; the axis numbers are sub-18px noise.

The single genuine strength to protect: **the chart's estimate-vs-realised bars, and the `E` jump-to-summary.** Everything else is a subtraction target.
