# Adult Journey Overhaul — Design

**Date:** 2026-08-03
**Site:** gywbt.com (`born-today-world` Vercel project, auto-deploys `main`)
**Pages affected:** `Website/adult/index.html`, `Website/music.js`, `Website/adult/assets/**`

## Problem

1. **No desktop footage exists for the adult journey.** All five "desktop" clips in
   `Website/adult/assets/vid/*.mp4` are 1080×1920 portrait; desktop letterboxes them
   via a CSS hack (`object-fit: contain`) in `adult/index.html`.
2. **Scenes 3–5 show children.** The generation prompts (`adult/work/leg_3.txt` etc.)
   ask for a "family group photo … two real giggling children." The adult side of the
   site must be adults-only.
3. **The song loops forever.** `music.js` restarts the track at its `data-start`
   offset (11 s) on `ended`, so the adult page's song never stops.
4. **Mute is flaky.** The first-gesture autostart listener can race the ♪ mute
   button; button state can disagree with actual playback.
5. **Song requires a tap.** The adult page should get as close to
   play-on-load as browser autoplay policy allows, with an always-available mute.

## Goals

- Adults-only footage for scenes 3–5 (Say Cheese, Patio Party, Send-Off), portrait tier.
- Real 1920×1080 landscape footage for **all five** scenes, wired as a proper desktop
  tier; letterbox hack removed.
- Visual continuity preserved: each leg continues from the previous scene's final
  frame; seams pass the existing QA gates.
- Song on the adult site: attempts autoplay at load, falls back to first touch,
  plays **once**, then stops (♪ replays). Mute always works and never lies.
- Production (gywbt.com) untouched until the user approves a preview deployment.

## Non-goals

- No changes to the envelope splash page's behavior (its looping classical strings
  stay), the kids story, games, cards, store, hire, or mission pages.
- No changes to scenes 1–2 portrait clips (Quiet Party, The Crash).
- No new story beats: scenes 3–5 keep their titles, scroll structure, and copy
  (except kid references).
- No checkout/store work, no nav redesign.

## Current architecture (for orientation)

- The adult journey is a scroll-scrubbed video experience driven by
  `adult/tap-engine.js` (`mountTapWorld`), configured inline in `adult/index.html`.
- Mobile phones scrub one stitched file, `assets/vid/journey-m.mp4`, using the
  `journeyMobile.spans` time ranges. Desktop/tablet scrub per-scene clips.
- Scenes were generated with Higgsfield (image-to-video continuations from anchor
  stills); prompts and job records live in `Website/adult/work/`. Character
  descriptions ("preamble") keep Starry, the three Crashers, and the cloud on-model.
- The kids side already did a landscape-tier retrofit on 2026-07-24
  (`Website/work/redo-landscape` playbook, documented in `Website/README.md`).
- `music.js` is shared by every page; per-page behavior comes from script-tag data
  attributes (`data-autostart`, `data-src`, `data-start`).

## Design

### 1. Portrait regeneration of scenes 3–5 (adults-only)

- Edit `adult/work/leg_3.txt`, `leg_4.txt`, `leg_5.txt`: keep the camera-language
  opening, the character preamble, and the cloud block **verbatim**; replace only the
  human cast and party staging. New cast direction: adult friends, couples, and
  grandparents — milestone-birthday energy (30th/40th/70th), matching the existing
  on-screen copy ("Yes, they crash 40ths", "Enchantment doesn't card"). Explicit
  negative: no children, no minors anywhere in frame.
- Regenerate any anchor stills those legs start from where the still itself contains
  children; otherwise reuse existing stills.
- Generate each leg as a continuation from the exact final frame of the preceding
  scene (leg 3 continues from scene 2's cloud-flight ending), preserving the
  one-continuous-shot illusion.
- Encode with the existing `adult/work/encode.sh` settings (same codec/GOP/bitrate
  tiers: 1080p master + 720p `-m` mobile encode).
- Re-extract posters (`<scene>-poster[-m].webp`) and stills (`<scene>.webp`) for the
  three redone scenes.
- Re-stitch `journey-m.mp4` (0.15 s crossfades) using the existing stitch script
  pattern (`Website/work/stitch_journey.py` equivalent for the adult chain) and
  update `journeyMobile.spans` in `adult/index.html` with the printed values.
- Run the seam QA (SSIM gate + visual frame-pair inspection) across the full chain;
  re-roll legs that fail visibly.

### 2. Landscape (desktop) tier — all five scenes

- Generate 16:9 anchor stills for all five scenes: same prompts and reference
  images, recomposed for widescreen. Scenes 1–2 keep current content/mood; 3–5 use
  the new adults-only prompts.
- **User checkpoint:** present the landscape stills (and the revised 3–5 portrait
  stills) for approval BEFORE generating any video legs — this is the main
  credit-burn gate.
- Generate the five landscape legs as continuations, chained for continuity like the
  portrait tier.
- Encode true 1920×1080 masters to `assets/vid/<scene>.mp4` (replacing the portrait
  stand-ins), plus matching posters.
- Wire the desktop tier in `adult/index.html`: per-scene `clip` fields point at the
  landscape files (bump `?v=`), and delete the letterbox CSS block
  (`object-fit: contain` override) and its comment.
- Desktop text layout: keep the current floating-copy design; verify it reads
  correctly over widescreen footage at 1280–2560 px widths.

### 3. Music behavior (`music.js`)

- New opt-in attribute `data-once` on the script tag (adult pages only):
  - On `ended`, do NOT restart. Stop, reset `currentTime` to the `data-start`
    offset, flip the ♪ button to the off state. Tapping ♪ replays from the offset.
  - Pages without `data-once` keep today's behavior (envelope strings loop natively).
- Autoplay: on `data-autostart` pages, call `play()` immediately at load. If the
  browser blocks it, arm one-time first-gesture listeners (today's fallback). This
  already mostly exists; the change is to keep it and make it compatible with the
  fixes below.
- Mute correctness:
  - The first-gesture fallback listeners must ignore gestures that land on the ♪
    button itself (check the event target), so tapping mute as your first touch
    never starts the music.
  - Button state (`is-on` class, `aria-pressed`) may only change inside the
    `play()` promise resolution / `pause()` call — never optimistically — so the
    button can never show "on" while silent or vice versa.
  - An explicit mute (sessionStorage `'0'`) continues to suppress `swap()` and
    `on()` re-arms, unchanged.

### 4. Copy touch-ups

- `adult/index.html` SEO block: "Hugs from the little ones included." → an
  adults-only line (e.g. "Hugs from your favorite people included."). Final wording
  set at implementation, kept in sync with the visible copy rule in the README.
- On-screen section copy unchanged unless the delivered footage contradicts it
  (decided at the footage-review checkpoint).

### 5. Deploy safety rails

- All work on branch `adult-overhaul`; pushes produce Vercel **preview** deployments
  of the `born-today-world` project.
- User reviews the preview URL on phone (portrait tier) and desktop (landscape
  tier) before anything merges.
- Merge to `main` (= production gywbt.com) only on explicit user approval.
- Large media: generated assets are committed to the repo like the existing ones
  (repo already carries ~100 MB of clips). `work/` scratch stays in the repo per
  current convention.

## Error handling / fallbacks (unchanged but re-verified)

- Reduced-motion → stills; data-saver → stills; video-load failure → poster
  fallback. Re-verify all three after the asset swap.
- `journey-m.mp4` must still stream via byte-range (Vercel answers 206).

## Testing

- `python -m http.server` local run: scroll the full adult journey on desktop
  viewport and phone emulation; no console errors; every referenced asset URL
  answers 200 (existing URL-check script pattern).
- Seam QA: SSIM gate + frame-pair inspection across both tiers' chains.
- Music: matrix of {fresh visit, arrived-from-envelope, returning-with-mute} ×
  {tap mute first, let it autoplay, replay after end} on Chrome + iOS Safari.
- Preview deployment checked by the user on real phone + desktop.

## Risks

- **Landscape 1–2 look-match:** widescreen recomposition may drift from the
  portrait originals' look. Mitigated by same prompts + reference stills, and the
  stills-approval checkpoint before video generation.
- **Seam quality on regenerated legs:** the crossfade hides confetti-level drift
  only; a visibly different party (new cast) makes leg-3's handoff from scene 2 the
  most sensitive seam. Budgeted for re-rolls.
- **Credit spend:** ~8 video legs + stills + re-rolls. Stills gate limits exposure.
- **iOS autoplay:** true play-on-load will still fail on a fresh iOS visit; the
  first-touch fallback is the designed floor, not a bug.
