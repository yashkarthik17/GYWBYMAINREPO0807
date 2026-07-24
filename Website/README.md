# Glad You Were Born Today — Scroll World

A scroll-scrubbed "fly through the world" landing page: as the visitor scrolls, a
pre-rendered camera dives into each scene of the Starry & the Crashers story and flies
on to the next with no cuts. Scroll only drives time — like Apple's product pages.

## Run it locally

The page fetches its clips with `fetch()` (blob playback), so it needs any HTTP server —
opening the pages directly from the file system won't work:

```
cd "Website"
python -m http.server 8000
# open http://localhost:8000
```

Pages: `index.html` (envelope splash front door) splits the site in two.
Kids side (no store): `story.html` (scroll world) → `crashers.html` (meet the
characters), `games.html` (mini-games), `cards.html` (card studio).
Grown-ups side: `adult/` (scroll story) → `adult/crew.html` (the crew) and
`store.html` (the full shop: party boxes, Crash Kit merch, the music corner,
and the Compassion mission band).

## The journey (scroll order)

1. **The Beige Party** — a joyless birthday, all sepia
2. **The Crash Pad** — Starry's cloud HQ, the party radar spots the signal
3. **The Crash** — the Crashers burst in, color floods the room
4. **The Glow-Up** — the same room rebuilt into the best party ever
5. **Starry's Send-Off** — hero finale + CTA ("Bring the Crashers")

## Files

- `story.html` — copy, palette, section config, SEO block for the scroll world.
  Desktop/tablet serves the landscape tier (`assets/vid/<scene>.mp4`, `?v=4`);
  phones serve the portrait tier (`-m` clips, `-p` stills, stitched journey).
- `scrub-engine.js` — the portable scroll-scrub engine (vanilla JS, framework-agnostic).
- `assets/` — everything the page serves (~97 MB):
  - `<scene>.webp` — stills (reduced-motion / fallback artwork)
  - `<scene>-poster[-m].webp` — posters extracted from the encoded clips
  - `vid/<scene>.mp4` — 1080p scrub masters (desktop/tablet)
  - `vid/<scene>-m.mp4` — 720p tight-GOP mobile encodes (phones)
  - `vid/conn1..4[-m].mp4` — the aerial connector flights between scenes
  - `vid/journey-m.mp4` — ALL nine mobile clips stitched into one seamless video
    (0.15s crossfades baked in). Phones scrub this single element instead of nine —
    real iPhones cap concurrent video decoders, so one element is the reliable path.
    Streamed via byte-range (the host MUST answer Range requests with 206; Vercel
    does). Regenerate with `work/stitch_journey.py`, which also prints the
    `journeyMobile.spans` values wired in `index.html`.
- `work/` — pipeline scratch (~140 MB): raw renders, prompt files, generation scripts,
  seam-repair + QA scripts. Safe to delete once you're happy with the site; keep it if
  you may re-roll or re-edit scenes (scripts are idempotent — re-running only
  regenerates missing assets).

## Deploying

Copy `index.html`, `scrub-engine.js`, and `assets/` to any static host. Byte-range
support is NOT required (clips load as blobs). The copy in the `data-sw-seo` block is
what crawlers see — keep it in sync if you edit the section copy.

## QA status

2026-07-15 (original chain):
- SSIM seam gate: 3 PASS / 5 WARN (confetti-level render drift, hidden by the 0.15
  crossfade), 0 FAIL after one connector re-roll + trim alignment
- Browser QA: 8/8 seams continuous (pop-ratio metric), blob seeking OK, scroll→time
  tracking OK, no console errors
- Fallbacks verified: reduced-motion → stills, data-saver → stills, phone → mobile
  encodes, tablet → 1080p masters

2026-07-24 (landscape tier redo, `work/redo-landscape`):
- All 9 landscape clips re-rendered at 1080p and wired into `story.html` (desktop
  fields moved off the portrait stand-ins back to the landscape files, `?v=4`)
- Raw adjacent-frame SSIM across the shipped chain reads low (0.38–0.70) — expected:
  dives are tail-trimmed 0.15s so the runtime crossfade bridges the handoff, and the
  known-good mobile chain scores the same range on this metric. Visual frame-pair
  inspection of the worst seams: same scene/composition, confetti-level drift only
- Every asset URL referenced by `story.html` (both tiers + dynamic still paths)
  verified 200 against a local server; inline config and engine pass a JS syntax check
