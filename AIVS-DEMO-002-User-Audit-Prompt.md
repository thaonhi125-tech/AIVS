# AIVS-DEMO-002 — Follow-up Prompt: Wear the User's Hat, Then Cut

**Version:** v1.0 | **Date:** 2026-08-06
**Parent:** AIVS-DEMO-001 (all invariant rules still apply, especially 5 — no crew-blame — and 7 — offline single file)
**Run this after Phase 1 and Phase 2 are working.**

---

## 0. WHAT THIS SESSION IS

This is **not** a feature session. Nothing gets added because it would be nice.

This is a session where you stop being the builder, become each of three real users, actually walk through the product turn by turn, write down every moment of hesitation, and then **fix by removing rather than by adding.**

**Hard rule for this session:** when you finish, the screen must have **fewer** interactive elements and **fewer** on-screen numbers than when you started. Every addition must be paid for by a deletion. If you cannot pay, do not add.

Report the before/after count at the end.

---

## 1. THE THREE USERS

Written in the course's own value-proposition form. Treat these as the specification; the previous document specified the machine, this one specifies the experience.

### User A — the panel member handed the clicker (THE HARD ONE)

> **As** a business examiner who has never seen this screen, does not work in shipping, and is being watched by thirty people,
> **I want** to understand what I am being asked to decide within ten seconds and without asking a question,
> **to achieve** the feeling that I personally discovered the bias, rather than being shown it.

**Acceptance criteria:**
- Understands the decision without anyone explaining the screen
- Never needs to know what TCE stands for in order to act
- Never has to ask "did that work?" after pressing a button
- Is never confronted with a term they cannot infer from context
- Feels competent, not tested

**This user cannot read instructions.** They are standing up, holding a clicker, in public. Anything that requires reading a paragraph has already failed.

### User B — the presenter

> **As** the team member running this on stage with ninety seconds and one attempt,
> **I want** to advance, recover, and reach the punchline without ever looking for a mouse,
> **to achieve** a demo that survives nerves, a bad projector, and running over time.

**Acceptance criteria:**
- Completes a full run using only `Space`, `M`, `R`, `E`
- Can hand over and take back the clicker mid-run with no state confusion
- Can reach the summary in one keystroke when time runs short
- Never sees an error, a blank frame, or a layout that breaks on the venue projector

### User C — the room

> **As** one of thirty people watching from four metres away who will never touch this,
> **I want** to follow what just happened without hearing it narrated,
> **to achieve** understanding of the argument even while the presenter is silent.

**Acceptance criteria:**
- The one number that matters is the largest thing on screen at any moment
- The pattern — realised always below estimated — is visible by voyage four **without narration**
- Nothing important is conveyed by colour alone, or by anything smaller than 18px

---

## 2. THE COLD-OPEN WALKTHROUGH — do this before changing a single line

Create `WALKTHROUGH.md`. Play each user in turn. Write the log **as they experience it, second by second**, not as you know it works.

For every step record:

```
[t+Xs] What is on screen  |  What the user is trying to do
       → What they look at first
       → Where they hesitate, and for how long
       → What they get wrong
       → VERDICT: clear / friction / broken
```

If you have a headless browser available, render actual screenshots at each step and inspect them. If you do not, do the written walkthrough with full rigour — the discipline is in refusing to describe intent and only describing what a stranger sees.

**Rule:** you are not allowed to write "the user then clicks QUOTE." You must justify *why* they would know to. If you cannot justify it, that is a finding.

Do three passes: User A cold, User B under time pressure, User C from four metres.

---

## 3. FRICTION HYPOTHESES TO TEST FIRST

These are predicted failure points. Confirm or reject each in the walkthrough; do not assume any is real, and do not stop at these.

1. **"TCE" is jargon.** User A does not know it. It is probably the largest word on screen. Can the demo work with the words *profit per day* instead, with TCE shown as a small secondary label for the shipping-literate?
2. **No indication of what a good decision looks like.** User A sees QUOTE and DECLINE with nothing telling them what either means. What is the minimum cue that makes the choice obvious without making it trivial?
3. **Losing a fixture looks like a broken button.** If the competitor underbids and nothing visibly happens, User A assumes they clicked wrong. Losing must be as visible an event as winning.
4. **Voyage 1 has nothing to compare against.** The chart has one bar and looks empty. The core pattern needs at least three points. Should the first voyage be pre-played so the user starts at voyage 2 with a pattern already forming?
5. **"47 months since drydock" is meaningless to a non-specialist.** Does it need a plain-language cue — *hull last cleaned nearly four years ago* — or a small visual state?
6. **The mode toggle is the emotional peak and it is currently a header button.** Nobody notices peaks that look like settings. This is the moment the whole argument turns.
7. **The summary screen probably has too many numbers.** Which single number is the punchline? Everything else on that screen is competing with it.
8. **The assumptions panel is the honesty defence but is probably invisible.** If the panel asks "where did these numbers come from" and the presenter fumbles to find it, the defence is lost.

---

## 4. THE USER-SCIENCE RULES THAT GOVERN THE FIXES

Apply these as decision rules, not decoration. Each one produces a concrete change here.

**Peak–end.** People remember the most intense moment and the ending, not the average. The **peak** is the mode toggle — the instant they see they won less and earned more. The **end** is the summary. Spend your remaining effort on those two moments and take it from everywhere else. A polished voyage-3 screen is wasted budget.

**Recognition over recall.** User A cannot hold rules in their head. Anything they need at the moment of deciding must be visible at the moment of deciding — not in a legend, not in a header, not explained thirty seconds earlier.

**One decision at a time.** At any moment there should be exactly one thing to press. Two competing calls to action doubles the hesitation and User A is being watched.

**Response under 400ms.** Anything slower and the user thinks it did not register, then presses again. Confirm every input within 100ms even if the result takes longer.

**Contrast carries meaning.** The single most important number on screen should be the largest and the only one in its colour. If three things are emphasised, nothing is.

**Progress reduces anxiety.** User A needs to know how many voyages remain, or they cannot pace themselves. One small persistent indicator, not a progress bar with animation.

---

## 5. THE SUBTRACTION PASS

After the walkthrough, before fixing anything, list every element on screen and mark each:

| Element | Who needs it | At what moment | Verdict |
|---|---|---|---|

Verdicts: **KEEP** · **MERGE** into something else · **DEMOTE** to secondary size/weight · **DELETE**.

Then apply this test to every KEEP: *if this were gone, would User A make a different decision, or User C misunderstand the story?* If neither, it is not a KEEP.

Expect to delete more than you think. A demo that runs for ninety seconds does not need a settings area, a legend, a subtitle under every panel, or four decimal places.

**Then fix.** Prefer, in this order:
1. Delete the thing causing the friction
2. Merge it into something already on screen
3. Change wording
4. Change size, weight or position
5. Only then, add something new — and delete something else to pay for it

---

## 6. ACCEPTANCE TESTS

- **The ten-second test.** Show voyage 1 to someone with zero context. Within ten seconds they must be able to say what they are being asked to do. If they ask a question, the screen has failed — fix the screen, do not add an explanation.
- **The silent test.** Run voyages 1–10 with no narration. Can User C state what the pattern was? If not, the pattern is not visible enough.
- **The clicker test.** Complete a full run using only the four keys. No mouse, no trackpad, no touching the laptop.
- **The peak test.** At the mode toggle, does the screen make it unmistakable that something significant just changed? If it looks like a filter was applied, it has failed.
- **The jargon sweep.** List every word on screen that a non-shipping business examiner would not know. Target: zero words that are required for action. Terms may appear as secondary labels, never as the primary instruction.
- **The count.** Interactive elements and on-screen numbers, before and after. After must be lower.
- **The invariants, again.** Search the source for `captain`, `master`, `crew`. Zero hits. Confirm it still opens from `file://` with wifi off, and that the same seed still produces an identical run.

---

## 7. WHAT NOT TO DO IN THIS SESSION

- Do not add a tutorial, a tooltip layer, an onboarding overlay, or a help button. Every one of those is an admission that the screen is not clear. Fix the screen.
- Do not add sound, confetti, celebration animation, or a scoring streak. This is a board-level argument, not a game. Delight here reads as unserious and undermines the pitch.
- Do not add mobile responsiveness. It runs on one projector.
- Do not refactor the simulation model. Section 4 of AIVS-DEMO-001 is settled; changing the mechanics invalidates the rehearsals.
- Do not start Phase 3. If Phase 1 and 2 are not yet flawless for all three users, Phase 3 is a distraction with a deadline attached.

---

## 8. DELIVERABLES FROM THIS SESSION

1. `WALKTHROUGH.md` — the three cold-open logs, with every hesitation recorded
2. `FINDINGS.md` — the element table, verdicts, and the fix applied to each finding
3. The updated single `.html` file
4. One line at the end: **interactive elements before → after, on-screen numbers before → after**

If the second number in each pair is not smaller, the session did not do its job.
