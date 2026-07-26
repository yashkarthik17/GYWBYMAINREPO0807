# Envelope Splash Overhaul — Animated Royal Envelope Video

**Date:** 2026-07-26
**Page:** `Website/index.html` (landing / splash)
**Status:** Approved design, pending spec review

## Problem

The landing page's envelope is procedurally built in Three.js (flat planes, gold
tube trim, torus-ring wax seal). It reads as programmer art — "cheesy" — and
clashes with the rich Pixar-style animated world of the story pages.

## Goal

Replace the Three.js envelope with a ~6-second animated video sequence in the
exact art style of the existing story world (warm Pixar-style 3D: glowing
enchanted forest, fireflies, god rays): a regal royal envelope — ivory paper,
gold-foil deckled edges, crimson wax seal with crown crest — flies through the
enchanted forest, settles front-and-center, and opens on tap to reveal the
letter with the two site-entry buttons.

**Mobile-first.** Portrait is the primary deliverable; desktop landscape is the
secondary tier.

## Non-goals

- No changes to story.html, adult/, nav.js, scrub-engine.js, or any other page.
- No photorealism — style must match the existing story-world posters.
- No new interaction model: same flow as today (auto intro → tap to open →
  buttons on letter → optional "Seal it back").

## The sequence (~6s per orientation, one stitched file)

One video file per orientation containing both beats, split at a hardcoded
anchor timestamp (`ANCHOR`, ~3.5s):

1. **Intro, 0 → ANCHOR (auto-plays once, muted, playsinline):** sealed envelope
   swoops through the enchanted forest and settles front-and-center, filling
   the frame. Video pauses exactly at ANCHOR. "Break the seal" appears.
2. **Open, ANCHOR → end (tap-driven):** from the identical settled frame, the
   wax seal cracks, the flap lifts, the letter slides up and out, ending on a
   motionless hold with the letter face-on. Final ~0.5s must be still so the
   HTML buttons can sit naturally on it.
3. **"Seal it back":** steps `currentTime` backward from end to ANCHOR (the
   reverse-scrub technique already proven in the story pages). Buttons hide
   (and lose pointer-events) the moment reverse starts.

Using a single stitched file per orientation guarantees pixel-perfect
continuity at ANCHOR and means one download, one decode pipeline.

## Link safety (the "random tap" problem)

The In Real Life / Kids Zone buttons remain real HTML (`.sheet-actions`),
absolutely positioned over the letter's final-frame position:

- From page load until the open clip reaches its final frame the overlay is
  `opacity: 0` **and `pointer-events: none`** — taps physically cannot land on
  a link; they fall through to the tap-to-open layer.
- Only on the held final frame does the overlay become visible and
  `pointer-events: auto`.
- This preserves the guarantee documented in the current index.html ("while
  the envelope is sealed, the invisible choices must swallow NOTHING").

Button positions are defined as fractions of the video frame (one set per
orientation, since the portrait and landscape masters compose differently) and
mapped through the object-fit: cover crop math to screen coordinates by JS —
same pattern the current page uses to position choices on the 3D letter.

## Asset production (Higgsfield)

1. **Keyframe stills first (user approval gate).** Generate three
   style-matched stills per orientation with existing story posters attached
   as style references: (a) envelope mid-flight in forest, (b) envelope
   settled center, (c) envelope open, letter out. **User approves the look
   before any video credits are spent.**
2. **Video.** Seedance image-to-video: (a)→(b) for the intro, (b)→(c) for the
   open, per orientation. Portrait (9:16) generated first and treated as the
   quality bar; landscape (16:9) second.
3. **Post.** Stitch intro+open per orientation (ffmpeg), trim to ~6s, encode
   to site conventions, extract posters.
4. **Costs are confirmed with the user before every paid generation call**, per
   the standard Higgsfield flow. Rough budget: ~20–40 credits stills,
   ~40–80 credits video, retries included.

## Asset naming & encoding (site conventions)

| File | Purpose |
|---|---|
| `assets/vid/envelope-m.mp4` | Portrait ~9:16, primary, target ≤ 6 MB |
| `assets/vid/envelope.mp4` | Landscape 16:9, desktop, target ≤ 12 MB |
| `assets/envelope-poster-m.webp` / `-poster.webp` | First-paint poster (settled frame) |
| `assets/envelope-p.webp` | Tiny blurred placeholder |

H.264 MP4, no audio track, keyframe interval tight enough for smooth
`currentTime` stepping (match existing story-page encodes; the `-m` files there
run 3–10 MB).

## index.html changes

- **Remove:** the entire Three.js scene (~600 lines), the three.js CDN
  `<script>`, sky/cloud CSS for this page.
- **Add:** `<video muted playsinline preload="auto">` with poster, the
  tap-to-open layer, ANCHOR pause logic, reverse stepper for "Seal it back",
  overlay gating, and cover-crop button positioning.
- **Keep (adapted):** loading screen, title copy, `#toggle` button as the
  keyboard/screen-reader path (focusable, same aria labels), confetti on open,
  music.js wiring.

## Fallbacks & accessibility

- **Autoplay blocked** (iOS Low Power Mode etc.): skip the intro — seek to
  ANCHOR, show the settled poster and "Break the seal"; the first tap is a user
  gesture so playback of the open segment is permitted.
- **`prefers-reduced-motion`:** no auto intro; page loads on the settled
  poster; tap jumps straight to the final frame (fast fade, no scrub) and
  reveals the buttons.
- **Keyboard / screen reader:** `#toggle` remains a real button that drives the
  same open/close; buttons get focus once revealed. Tap targets ≥ 44 px.
- **Video load failure:** after a timeout, fall back to the settled poster
  image with the overlay revealed on tap — the site must never dead-end.

## Testing / QA

- iPhone Safari (primary): autoplay, pause-at-ANCHOR accuracy, reverse scrub
  smoothness, button hit-testing during every phase, Low Power Mode path.
- Android Chrome: same pass.
- Desktop Chrome/Safari/Firefox: landscape tier, resize/orientation change
  re-positions buttons correctly.
- Lighthouse mobile: first paint on poster ≤ current page.
- Verify a rapid-fire random tapping session during intro/open can never
  trigger navigation.

## Rollout

Work on a branch off `main` in "Glad You Were Born Today (Repo)"; preview
deploy to the `born-today-world` Vercel project for on-device testing before
promoting to production.
