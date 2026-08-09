# Task r12 — Confetti re-chain (portrait mobile), clips 3-4

Branch: `adult-overhaul` (verified at start; not touched main, not pushed, not deployed).
Work dir: `Website/adult/work/redo2/`.

## Status: PARTIAL — leg_3 fixed and PASSING (incl. a mid-session hidden-cut fix); leg_4
BLOCKED (3/3 fresh attempts failed the Starry-scale gate); mobile assembly intentionally
NOT run this round because it depends on a passing leg_4.

This report covers two chained sessions: the original credit-blocked resume (steps 1-3
below), and a follow-up round that fixed a user-reported hidden cut discovered in the
first accepted leg_3 take (steps 4-6 below).

## Step 1 — `pstill_3b` (new confetti-full ending anchor) — 1 attempt — PASS

Unchanged from the prior write-up: new group-photo anchor still with the air completely
full of confetti at every depth, spliced from the STARRY/CRASHERS/GATE descriptors and the
`pstill_2b.txt` framing preamble. Zero `streamer` matches. PASS on attempt 1, audited
composition/cast/confetti/artifacts against `start_leg4.png` and the reference sheets.

## Step 2 — Re-extract `start_leg3.png` from `leg_2.mp4` — DONE

Idempotent re-extraction confirmed the new fancier-clubhouse, active-cannon-blast frame
matching `leg_2.mp4`'s final frame.

## Step 3 — `leg_3` regen, round A (confetti-full ending) — 1 attempt — PASS (later superseded)

Credits were topped up to 1039.14 between sessions, clearing the `not_enough_credits` block
from the original report. Submitted `./gen_leg.sh leg_3 leg_3.txt 9:16 start_leg3.png
pstill_3b.png`; passed on attempt 1/3 — dense airborne confetti through every 1s-interval
audit frame including the final group-photo settle, cast/no-children/no-wire-artifact
checks clean, t1 continuous with `leg_2`'s ending, t9 closely matching `pstill_3b.png`.
Kept live. **This take was later found to contain a hidden mid-shot cut — see Step 4.**

## Step 3b — `start_leg4.png` re-extract + `leg_4` regen (round A target) — BLOCKED, 3/3 attempts

Re-extracted `start_leg4.png` from the (then-live) round-A `leg_3.mp4`; matched `pstill_3b.png`
closely. Archived the prior `leg_4.mp4` → `leg_4_calmstart.mp4`/`.json` (the r9-approved
scale-fixed take chained from the OLD calm start frame, now superseded).

Submitted 3 fresh content attempts against the new confetti-storm `start_leg4.png` (plus one
uncounted transient job-level failure with zero credit charge, immediately retried):

- **Attempt 1**: reproduced the exact "Starry's giant face fills the top of frame behind the
  cake" bug that r9 had already fixed once for the old chain — at t6-t9 his chin/mouth fills
  the frame directly over the candles.
- **Attempt 2** (after strengthening the guard to explicitly forbid any part of him entering
  the tightest close-up, with retreat-during-push-in language): identical failure reproduced.
- **Attempt 3** (after rewriting the guard again — Starry now positioned far in the
  background *before* the push-in begins, fully static, never moving near the lens during the
  shot, camera itself tilts away from him rather than him dodging it): identical failure a
  third time.
- **Verdict**: 3/3 genuine content attempts (confirmed charged via credit-balance deltas)
  failed the same gate under three materially different prompt strategies. This reads as a
  strong, consistent model bias rather than a wording problem fixable within budget.
  BLOCKED per the 3-strikes rule. Live `leg_4.mp4`/`.json` restored to `leg_4_calmstart`
  bytes (hash-verified exact match) — left in the last known-good, self-consistent state
  rather than pointing at an unreviewed failure.
- Failed attempts archived as `leg_4_v4`/`_v5`/`_v6` (not `_v1`/`_v2`, which are already used
  by the prior r9 round's own failed attempts — reusing those names would have silently
  clobbered that round's provenance; caught before staging).

## Step 4 — Mid-session defect report: hidden cut in the accepted leg_3 (round A)

A hidden mid-shot cut was reported in the round-A `leg_3.mp4`: the shot jumped from the
open-lawn dance to the picnic-table composition instead of traveling there, because the
prompt scripted the confetti/dance beats but never scripted the relocation that the
`pstill_3b` end-anchor's table-foreground composition implies.

**Independently verified before acting**: dense-sampled the round-A `leg_3.mp4` at 0.25s
intervals (`ffmpeg -ss 3.5 -t 3.5 -vf fps=4`) across the exact window my original 1s-interval
audit had sampled through (t5 at 4.04s showed open lawn/no table, t6 at 5.03s already showed
the table prominently in frame — a gap wide enough to hide a cut). Confirmed: dense frames at
t=4.0s (open lawn, cloud/clubhouse still in background, no table) and t=4.25s (table suddenly
fills the foreground, entire background changed, camera position jumped) show a genuine hard
cut, not continuous travel. The defect was real, not a false report.

## Step 5 — `leg_3` regen, round B (no-cut fix) — 1 attempt — PASS

Edited exactly one sentence in `leg_3.txt` — replaced "The camera eases back and glides
forward across the lawn as the friends and the four characters gather together facing the
camera." with a version that explicitly scripts the continuous lawn-to-table glide (everyone
walking over together, the table rising into the bottom foreground "in one continuous
motion"). Every other sentence, all confetti language, and the GATE paragraph verified
untouched (`git diff` shows exactly 1 line changed).

Archived the cut take as `leg_3_hiddencut.mp4`/`.json`. Re-submitted
`./gen_leg.sh leg_3 leg_3.txt 9:16 start_leg3.png pstill_3b.png`.

**Passed on attempt 1/3**, audited with the standard 9 frames plus a new **NO-CUT GATE**:
dense-sampled the same 3.5s relocation window at 4fps (14 frames) and inspected every
consecutive pair. Result: smooth, continuous, monotonic approach to the table across
dense_01 through dense_09 (table grows progressively larger frame-over-frame, background/
lighting/characters stay consistent, camera and cast visibly traveling together) — no
teleport at any adjacent pair. All prior gates also re-confirmed on this take: airborne
confetti dense through every frame including the final settle, t1 continuous with `leg_2`'s
ending, t9 closely matching `pstill_3b.png`, cast exactly 1 Starry + 3 Crashers throughout,
zero children, string-light zoom clean (no wire/squiggle artifacts). Kept live as the final
`leg_3.mp4`.

## Step 6 — `start_leg4` re-extract + comparison call (per instruction, not silently spent)

Re-extracted `start_leg4.png` from the fixed round-B `leg_3.mp4`. Compared directly against
the round-A extraction (saved as `start_leg4_prevfix.png`): **materially identical
composition** — same 8-person cluster arrangement, same Starry/Crashers positions, same
table-foreground props, same background. This is expected since both leg_3 takes anchor to
the same `pstill_3b` ending; the cut-fix changed the *path* to that ending, not the ending
itself. Per the instruction, this means leg_4's chain-continuity target is unchanged by the
leg_3 fix — **no additional leg_4 re-render was triggered by this comparison alone.**

However, leg_4 independently remains BLOCKED from Step 3b's 3-strikes exhaustion, and the
live `leg_4.mp4` (restored to `leg_4_calmstart` bytes) is chained from the OLD calm
`start_leg4`, not this new confetti-storm one. That mismatch pre-dates and is unrelated to
the cut-fix — it will remain until a future round lands a working Starry-scale guard.

## Mobile assembly — NOT RUN this round (judgment call, flagged rather than silently done)

Steps 7-8 of the original plan (mobile-tier encode of glowup-m/photo-m/patio-m, journey-m
re-stitch, hash compare, `adult-config.js` version bumps, commit + push) were **not
attempted**. Assembling now would bake the leg_3/leg_4 seam mismatch (new confetti-storm
leg_3 ending → old calm leg_4 opening) into shipped mobile assets, which is strictly worse
than the pre-existing `leg_3_confetti_v2`-based mismatch already flagged in the prior report.
`Website/adult-config.js` was not touched. `Website/adult/assets/` was not written to.
`redo2/out/` was not written to.

### Current mobile-tier version params in `adult-config.js` (unchanged this round, still the
values recorded in the prior report — read-only, not re-verified this round since assembly
did not run)

| Ref | Current `?v=` |
|---|---|
| `journeyMobile.clip` (journey-m.mp4) | v9 |
| `journeyMobile.poster` (journey-poster-m.webp) | v7 |
| `glowup.posterMobile` (glowup-poster-m.webp) | v8 |
| `glowup.clipMobile` (glowup-m.mp4) | v8 |
| `glowup.still` (glowup.webp — mobile-derived) | v8 |
| `photo.posterMobile` (photo-poster-m.webp) | v9 |
| `photo.clipMobile` (photo-m.mp4) | v9 |
| `photo.still` (photo.webp — mobile-derived) | v9 |
| `patio.posterMobile` (patio-poster-m.webp) | v7 |
| `patio.clipMobile` (patio-m.mp4) | v7 |
| `patio.still` (patio.webp — mobile-derived) | v7 |
| `quiet.*` / `sendoff.*` | still unchanged — not touched by the finish_confetti_mobile.py recipe |

## Seam check

- **2→3 clubhouse continuity**: solid — `start_leg3.png` matches `leg_2.mp4`'s ending and
  `pstill_2b.png`'s target.
- **3→4 continuity (composition)**: solid — the fixed `leg_3.mp4`'s final frame and the
  re-extracted `start_leg4.png` both match `pstill_3b.png` closely, confirmed materially
  identical to the pre-cut-fix extraction.
- **3→4 continuity (live shipped state)**: **broken** — live `leg_4.mp4` is still the OLD
  calm-start take (`leg_4_calmstart`), so the actual chained pair as currently committed is
  confetti-storm leg_3 ending → calm-start leg_4 opening. Will self-resolve once a leg_4
  attempt passes against the current `start_leg4.png`.
- **4→5 continuity**: not applicable this round — `leg_4` regen never passed, `start_leg5.png`
  untouched throughout (verified unchanged mtime/hash before every leg_4 submission).

## Commit

Two commits this session:

1. (Prior session, already landed) `pstill_3b.txt`, `pstill_3b.json`, `leg_3_calmend.json`.
2. (This session) `leg_3.txt` (no-cut sentence edit), `leg_3.json` (live record, now the
   round-B pass), `leg_3_hiddencut.json` (archive record of the round-A cut take, for
   provenance), `leg_4.txt` (final round-3 Starry guard wording, kept even though it didn't
   fully solve the bug — genuine improvement candidate for the next round), `leg_4_calmstart.json`
   (archive record of the pre-this-round leg_4, i.e. the live-restore target),
   `leg_4_v4/_v5/_v6.json` (this round's 3 failed content attempts, renamed from the `_v1/_v2`
   the gen script would have used to avoid clobbering r9's own `_v1/_v2` archives).

No `.mp4`/`.png`/`.err`/`audit/` files committed (gitignored, consistent with prior rounds).
No edits to `Website/adult-config.js`, no assembly output. **Nothing pushed** — the task's
push instruction is scoped to after a successful mobile-assembly commit, which did not happen
this round.

## Summary

| Asset | Attempts | Result |
|---|---|---|
| pstill_3b | 1 | PASS — confetti-full ending anchor |
| start_leg3.png re-extract | — | DONE |
| leg_3, round A (confetti-full) | 1 | PASS at the time, **later found to contain a hidden mid-shot cut** |
| leg_3, round B (no-cut fix) | 1 | **PASS** — dense-sampled no-cut gate confirms continuous lawn-to-table travel; kept live |
| leg_4 (Starry-scale fix, 3 prompt strategies) | 3 content attempts (+1 uncounted infra failure) | **BLOCKED** — restored to last known-good `leg_4_calmstart`, mismatched with the new `start_leg4.png` |
| Mobile assembly | not attempted | **BLOCKED** (downstream of leg_4) |

## Concerns / what's needed to unblock

leg_4's Starry-scale bug survived three materially different prompt strategies this round
(explicit no-part-of-him-visible language, retreat-during-push-in, and static-distant-before-
push-in) on top of the wording that had worked for r9's *old* chain. This looks like it may
need a different mechanism entirely rather than a fourth prompt variant — candidates for the
next round: (a) an anchor-still approach for leg_4 similar to how `pstill_2b`/`pstill_3b`
pre-compose an on-model keyframe (e.g. a `pstill_4` mid-close-up still with Starry already
correctly out-of-frame, fed in as an additional `--image` reference or an interpolation
keyframe partway through), (b) physically removing Starry from the candle-close-up beat's
prompt language entirely and only reintroducing him in a final pull-back sentence, or (c)
accepting the calm-start seam as a known limitation for this ship and revisiting leg_4 in a
dedicated follow-up round with a larger attempt budget. `start_leg3.png` and the fixed
`leg_3.mp4`/`pstill_3b.png` chain are solid and ready; only `leg_4` blocks assembly.
