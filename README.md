# The Voyage Pricing Simulator (AIVS-DEMO-001)

A single, self-contained HTML artefact for a live, on-stage pitch demo. An audience
member plays the chartering desk for ten dry-bulk voyages using the old sea-trial
curve, watches money leak, then replays the **identical ten voyages** with the model —
and discovers they **win fewer cargoes but earn more money**.

**Live:** https://aivs-two.vercel.app

> **For the stage, do not rely on the live link.** Download `index.html` and open it by
> double-clicking. No server, no network, no install — it runs from a USB stick with wifi
> switched off. Venue wifi fails; the file does not.

## What it demonstrates

1. **The error only points one way** — realised earnings are always below the estimate.
2. **Adverse selection** — the cargoes we win are the ones we priced worst. This emerges
   from the bidding mechanic; it is never asserted.
3. **The adoption valley** — turning on the model *reduces* the win count. The discomfort
   comes before the payoff.

## Controls (clicker-friendly)

| Key | Action |
|---|---|
| `Space` · `PageDown` · `→` · `↓` · `Enter` | take the cargo / advance |
| `PageUp` · `←` · `↑` · `Backspace` | step back one cargo (recover from overshooting) |
| `M` | switch pricing: today's curve ⇄ the model |
| `R` | reset to a fresh presentation |
| `E` | jump straight to the summary |
| `Esc` | close the assumptions panel |

**The whole demo runs on the forward button alone.** Presentation remotes
(Logitech, Kensington) send `PageDown`/`PageUp` rather than `Space`, so every key a
remote can emit is accepted. At the first summary, forward starts the model run — the
demo never dead-ends on a press that appears to do nothing.

Fastest stage path: hand over the clicker for three or four cargoes → `E` → talk →
forward (or `M`) → `E`. About ten presses to the punchline.

The header button **"Where do these numbers come from?"** opens the Assumptions panel —
every parameter is visible, editable, and labelled *illustrative, not company data*.
Changing the seed live re-runs the whole thing deterministically (the answer to a
"did you cherry-pick this?" question).

## Design rules (invariant)

- Single `.html` file. No network, no CDN, no fonts, no `fetch`. System fonts only.
- Deterministic: a seeded `mulberry32` PRNG. Same seed → the same ten voyages every time.
  Never `Math.random()`.
- No storage APIs (no `localStorage`/`sessionStorage`/cookies). State lives in JS variables.
- No framework, no build step. Vanilla JS.
- **No crew-blame framing anywhere.** Hindcast weather is a second imperfect instrument,
  never "the real weather" a report is checked against.

## Files

| File | What it is |
|---|---|
| `index.html` | The demo. The deliverable. Self-contained — download and double-click. |
| `AIVS-DEMO-001-Master-Prompt.md` | The build spec (the machine). |
| `AIVS-DEMO-002-User-Audit-Prompt.md` | The UX-audit spec (the experience). |
| `WALKTHROUGH.md` | Three cold-open user logs, second by second. |
| `FINDINGS.md` | The subtraction pass: element table, verdicts, fixes, before→after counts. |
| `verify.py` | Standalone harness that locks the simulation parameters and proves the acceptance checks. |

## Verified

- Sea-trial mode: realised earnings **below** the estimate on every won voyage.
- Model mode on the same ten cargoes: **4 fewer** fixtures, **$224,864 more** money
  ( 8 won / \$206,835  →  4 won / \$431,699 ).
- After the UX audit: interactive elements 3 → 2; on-screen numbers 34 → 9 (run), 10 → 6 (summary).

Run `python3 verify.py` to reproduce the parameter checks.
