# Task r9 — Portrait clips 2-4 regen: confetti storm, no streamers, Starry scale guard

Branch: `adult-overhaul` (verified before starting; never touched main, no deploy).
Scope respected: only `Website/adult/work/redo2/` media, prompts, json touched. No edits to
`Website/adult-config.js` or any HTML (Spanish-i18n agent's files, untouched, confirmed by
final `git status` review). No assembly/encode run into `Website/adult/` assets this round —
`out/` directory (which holds the shipped `patio-m.mp4` etc.) was not written to.

## Prompt edits applied

1. **Streamer removal** — deleted every "ribbon streamers"/"streamers" mention (the diagnosed
   wire-artifact trigger) from `pstill_2b.txt`, `leg_2.txt`, `leg_3.txt`. Confirmed via
   `grep -in streamer` on all four touched files post-edit: zero matches. (`leg_4.txt` never
   had the phrase.)
2. **`pstill_2b.txt`** — confetti cannon changed from "fires a soft arc" to "caught mid-blast,
   firing a thick dense jet," added confetti "pours and spills off the cloud's edges in
   curtains," crowd now stands in "air ... filled with colorful drifting confetti."
3. **`leg_2.txt`** — added continuous cannon-blast + cloud-deck-spill language through the
   descent/fence-sweep and into the final hover ("the cannon still firing and confetti still
   drifting thick around the cloud, ready to continue").
4. **`leg_3.txt`** — three rounds of strengthening (see attempts below) aimed at keeping
   airborne confetti alive through the group-photo settle; final version decouples the
   confetti supply from the departing cloud ("the enormous blizzard of confetti it already
   released keeps falling like heavy snow ... completely unaffected by the cloud leaving").
5. **`leg_4.txt`** — added a Starry mention (previously absent) with a scale/position guard;
   two rounds of strengthening (see attempts below) to stop Starry from looming behind the
   cake during the candle close-up. No other content in `leg_4.txt` was changed (camera
   language, beats, cake/sparkler descriptors, GATE paragraph all untouched).

All GATE paragraphs (cast-count / no-children) preserved verbatim in every file.

## Archiving (step 1)

- `leg_2.mp4`/`.json` → `leg_2_r7approved.mp4`/`.json`
- `leg_4.mp4`/`.json` → `leg_4_r4approved.mp4`/`.json`
- `leg_3_r7approved.*` already existed — kept as-is
- `pstill_2b.png` → `pstill_2b_r7.png`

## pstill_2b — 1 attempt — PASS

`./gen_still.sh pstill_2b pstill_2b.txt 9:16 refs/ref_starry.png refs/ref_starry_turnaround.png refs/ref_crashers_turnaround.png refs/ref_1.png`
(ref order recovered by SHA-256 hash-matching the 4 `medias` URLs recorded in the prior
`pstill_2b.json` against the local `refs/*.png` files — exact match confirmed.)

- Confetti storm: cannon caught mid-blast firing a dense jet, confetti spilling off the cloud
  edges in curtains, air full of drifting confetti — matches directive, verified by direct
  view and cropped zooms (`audit/_pstill2b_r8_sky_zoom.png`, `_crashers_zoom.png`,
  `_starry_zoom.png`).
- Cast: exactly ONE Starry, exactly THREE Crashers, on-model (compared side-by-side against
  `pstill_2b_r7.png` baseline crop — same character design/quality).
- No children, young-adult crowd only.
- Sky scanned across all crops: zero wire/rope/squiggle artifacts.

## leg_2 — 1 attempt — PASS

`./gen_leg.sh leg_2 leg_2.txt 9:16 - pstill_2b.png` (end-keyframe = new pstill_2b, per the
"final ≈ new pstill_2b" audit spec).

Audited all 9 frames (`audit/leg_2_r4/`):
- t1: burst-through-glow opening confirmed — no cloud visible at t0/t1, just the flaring glow
  over rooftops.
- t2-t9: smooth continuous descent/sweep/hover, motion gate passes.
- **Confetti gate**: massive improvement over the `audit/leg_2_r3` too-little baseline. In r3
  (`leg_2-t6.jpg`), the cannon is static/unfired and confetti is sparse. In r4, the cannon
  fires a visible dense jet from t5 onward and the cloud sheds confetti in cascading curtains;
  by t7-t9 confetti fills the frame edge-to-edge around the whole crowd.
- **Artifact gate**: zoomed the sparkle-trail region in t2/t3 (`_t2_trail_zoom.jpg`,
  `_t3_trail_zoom.jpg`) — clean gold sparkle trail only, no squiggly wire/rope shapes anywhere.
  Directly contrasts with `audit/leg_2_r3/leg_2-t6.jpg`, which shows two dangling
  ribbon/wire artifacts hanging off the cloud (the diagnosed bug) — confirmed absent in every
  r4 frame.
- Cast: 1 Starry + 3 Crashers throughout, no children, young adults only.
- Final (t9) closely matches the new `pstill_2b.png` composition and confetti density.
- Chain: `start_leg3.png` re-extracted via `ffmpeg -sseof -0.3` from the new `leg_2.mp4`
  (non-empty, confirmed by direct view) — carries the confetti storm forward into leg_3.

## leg_3 — 3 attempts — BLOCKED (3 strikes)

`./gen_leg.sh leg_3 leg_3.txt 9:16 start_leg3.png start_leg4.png`

Goal: sustained airborne confetti through all 8s, specifically not fading out by the
group-photo settle (the exact failure the currently-accepted `leg_3_r7approved` take has,
per user diagnosis, and the same failure documented in the `audit/leg_3_r4` baseline).

- **Attempt 1** (`leg_3_v1.mp4`/`.json`): t1-t4 (leap/landing) had strong dense confetti, but
  t5-t9 (dance/gather/photo) faded to near-nothing airborne — only ground/table confetti
  remained. Same failure mode as the problem being fixed. Archived, prompt strengthened
  (explicit foreground-lens confetti + "never thinning" language at the settle).
- **Attempt 2** (`leg_3_v2.mp4`/`.json`): same fade pattern reproduced despite the stronger
  wording — t6-t9 essentially clean sky, confetti only on ground/table. Archived, prompt
  strengthened again: decoupled the confetti supply from the departing cloud ("the enormous
  blizzard of confetti it already released keeps falling like heavy snow ... unaffected by
  the cloud leaving") on the theory that the model was treating the cloud's exit from frame as
  a cue to stop the confetti "source."
- **Attempt 3** (`leg_3_v3.mp4`/`.json`): same result a third time — t9 zoom
  (`_t9_upper_zoom.jpg`) shows an empty sky, indistinguishable from the explicitly-rejected
  `audit/leg_3_r4/leg_3-t7.jpg`/`t8.jpg` "too settled" baseline used as the failure reference.
- **Verdict**: 3/3 attempts failed the airborne-confetti-at-settle gate identically. This
  looks like a strong, consistent model bias (group-photo/selfie compositions trained toward
  a "calm" finish) rather than something more prompt wording was going to fix within budget.
  Per the 3-strikes rule, stopped here and reported BLOCKED rather than continuing to spend
  credits on a fourth attempt.
- **Live-file handling**: since none of the 3 attempts improved on this specific axis over the
  already-accepted `leg_3_r7approved` baseline, `leg_3.mp4`/`leg_3.json` were restored to the
  `leg_3_r7approved` bytes (not left pointing at an unreviewed failed attempt). All 3 failed
  attempts are preserved as `leg_3_v1/_v2/_v3.mp4`/`.json` with corresponding audit frame
  dumps (`audit/leg_3_r5_attempt1/2/3`) for human review. The streamer removal and the
  strengthened confetti prompt language in `leg_3.txt` are still committed as-is — they are a
  genuine improvement candidate even though generation didn't yet realize the late-shot
  density goal.
- Cast/no-children/no-wire checks all passed cleanly in every attempt — only the airborne
  confetti persistence gate failed.

## leg_4 — 3 submissions (1 infra retry + 2 content failures + 1 pass) — PASS

`./gen_leg.sh leg_4 leg_4.txt 9:16 start_leg4.png start_leg5.png`
(`start_leg5.png` verified present before starting — pre-existing chain asset, untouched.)

- First submission hit a transient `HTTP 502` from the Higgsfield API with no job created
  (confirmed via empty `leg_4.err`/`leg_4.json` — no job id assigned). Did not count against
  the 3-attempt budget; resubmitted the identical command immediately.
- **Attempt 1** (`leg_4_v1.mp4`/`.json`): reproduced the exact diagnosed bug. At t5-t8, Starry's
  face fills the top of frame directly behind/over the cake as the camera pushes in for the
  candle close-up — visually near-identical to the original failure frame
  `audit/leg_4/leg_4-t5.jpg` (the "encoded patio-m t5" giant-face reference). The
  first-pass scale-guard sentence ("exactly person-sized ... never closer to the camera than
  the people") wasn't specific enough to prevent this — the actual failure mechanism is
  positional (Starry standing directly in the camera's forward path behind the cake), not raw
  size. Archived; guard rewritten to add explicit positioning ("standing off to the side of
  the table ... never directly behind the cake ... never filling the frame even in the
  close-up").
- **Attempt 2** (`leg_4_v2.mp4`/`.json`): identical failure reproduced again at t4-t7 despite
  the positioning language. Archived; guard rewritten a third time to target the actual
  mechanism directly: Starry "steps out of the camera's path as it pushes in on the cake and
  candles, staying at the edge of frame or fully out of frame during that close-up shot."
- **Attempt 3** (final, kept as live `leg_4.mp4`/`.json`): fixed. t1-t3 show Starry at normal
  person-scale in the group/reveal shots (matches `start_leg4.png` continuity). t4-t5 show him
  receding to the background/edge of frame as the camera pushes in. t6-t7 (tightest candle
  close-up) show Starry essentially fully out of frame. t8-t9 show only a small, heavily
  out-of-focus blurred gold fragment at the very top edge — compared directly against
  `start_leg5.png` (the pre-existing, already-approved chain target for this exact moment):
  that still has the *same* soft blurred-star-fragment-at-top composition, confirming this is
  the intended target framing, not a residual artifact. No sharp/giant/looming Starry face at
  any point — scale gate passes.
- Cake/sparkler beats intact throughout: host carries the lit-sparkler cake to the table,
  crowd cheers/claps, Crashers bounce at the table edge holding paper plates.
- First frame (t1) matches `start_leg4.png` closely (same selfie-group pose/characters).
  Final frame (t9) matches `start_leg5.png` closely (same cake/candle/sparkler framing).
- Cast: 3 Crashers + 1 Starry throughout, no children, young adults only, no wire/streamer
  artifacts observed.

## Commit

Committed only prompt `.txt` files, live `.json` job records, and archive `.json` records
(`leg_2_r7approved.json`, `leg_3_r7approved.json`, `leg_3_v1/_v2/_v3.json`,
`leg_4_r4approved.json`, `leg_4_v1/_v2.json`). No `.mp4`/`.png`/`audit/` — all gitignored by
`Website/adult/work/redo2/*.{mp4,png,err}` / `audit/` rules already in `.gitignore`, consistent
with "no asset copies" instruction. No edits to `Website/adult-config.js` or any HTML file
(verified untouched in final `git status`). No assembly/encode run.

## Summary

| Clip | Attempts | Result |
|---|---|---|
| pstill_2b | 1 | PASS — confetti storm, on-model, no artifacts |
| leg_2 | 1 | PASS — cannon blast + cloud spill confirmed, zero wire artifacts, matches r3-baseline comparison |
| leg_3 | 3 | **BLOCKED** — airborne confetti still fades out by the group-photo settle in all 3 attempts; live file restored to `leg_3_r7approved` |
| leg_4 | 3 (2 fail + 1 pass, +1 uncounted infra retry) | PASS — Starry scale/looming bug fixed by keeping him out of the camera's push-in path during the candle close-up |
