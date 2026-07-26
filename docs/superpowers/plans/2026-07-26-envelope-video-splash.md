# Envelope Video Splash Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Three.js envelope on `Website/index.html` with a ~6s Pixar-style animated video (enchanted-forest flythrough → tap-to-open royal envelope), mobile-first, built from Higgsfield-generated assets.

**Architecture:** One stitched MP4 per orientation (portrait primary, landscape secondary) containing intro + open beats split at a measured ANCHOR timestamp. A small state machine drives autoplay-to-ANCHOR, tap-forward play, and reverse-step close. Site-entry links are an HTML overlay that is `pointer-events:none` until the final frame holds.

**Tech Stack:** Higgsfield (stills + Seedance image-to-video), ffmpeg/ffprobe + cwebp for post, vanilla HTML/CSS/JS (no Three.js, no libraries), Vercel for deploy.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-07-26-envelope-video-overhaul-design.md` — re-read before starting.
- Mobile-first: portrait 1080×1920 is the primary asset and quality bar; landscape 1920×1080 is the desktop tier.
- Art style MUST match the existing story world. Style references: `Website/assets/crash-poster.webp`, `Website/assets/beige-poster.webp`, `Website/assets/finale-poster.webp`.
- Envelope look (from spec): ivory/cream cotton paper, gold-foil deckled edges, crimson wax seal with crown crest — regal, but rendered in the warm Pixar story-world style, NOT photoreal.
- File size targets: `envelope-m.mp4` ≤ 6 MB, `envelope.mp4` ≤ 12 MB.
- Naming conventions: `assets/vid/<name>-m.mp4` (portrait), `assets/vid/<name>.mp4` (landscape), `assets/<name>-poster-m.webp`, `assets/<name>-poster.webp`, `assets/<name>-p.webp`.
- **Every paid Higgsfield call: state the credit cost and get user confirmation BEFORE calling.**
- Only `Website/index.html` and new asset files change. story.html, adult/, nav.js, scrub-engine.js untouched.
- All work on branch `envelope-video` off `main` in `Glad You Were Born Today (Repo)`.
- H.264 encodes use a short GOP (`-g 12`) — required for smooth `currentTime` reverse stepping.

---

### Task 0: Branch + working directory

**Files:**
- Create: `Assets/envelope/` (raw generation masters, committed)

- [ ] **Step 1: Create the branch and folder**

```bash
cd "/c/Users/yashk/OneDrive/Desktop/Glad You Were Born Today (Repo)"
git checkout -b envelope-video
mkdir -p Assets/envelope
```

- [ ] **Step 2: Verify tooling exists**

Run: `ffmpeg -version | head -1 && ffprobe -version | head -1 && ffmpeg -hide_banner -encoders | grep libwebp`
Expected: version strings + libwebp encoder listed (ffmpeg's built-in webp encoder replaces cwebp; no separate install).

---

### Task 1: Keyframe stills (USER APPROVAL GATE)

Generate the three keyframes per orientation with Higgsfield, style-locked to
the story posters. No video generation happens until the user approves these.

**Files:**
- Create: `Assets/envelope/still-flight-m.png`, `still-settled-m.png`, `still-open-m.png` (portrait 9:16)
- Create: `Assets/envelope/still-flight.png`, `still-settled.png`, `still-open.png` (landscape 16:9)

**Interfaces:**
- Produces: approved stills; `still-settled-*` composition = the pause frame; `still-open-*` = final frame whose letter must have clear space for two stacked buttons (portrait) / side-by-side buttons (landscape).

- [ ] **Step 1: Invoke the higgsfield-generate skill** (it owns model choice + exact CLI). Use a reference-image model (Nano Banana Pro) with the three style-reference posters attached. Confirm cost with user first.

Portrait prompts (generate all three, 9:16):

1. *flight:* "A regal royal envelope — thick ivory cotton paper, gold-foil deckled edges, crimson wax seal embossed with a crown — flying through a glowing enchanted forest at dusk, motion-tilted mid-swoop between huge mossy trees, spiral fireflies, god rays through the canopy, spotted red mushrooms. Warm Pixar-style 3D animation matching the reference images' rendering, lighting and palette. No text, no characters."
2. *settled:* "The same royal envelope now floating perfectly still, face-on, centered, filling most of the frame, seal centered on the flap point, enchanted forest softly blurred behind it, fireflies drifting. Same style as references. No text, no characters."
3. *open:* "The same royal envelope with wax seal broken in two, flap open upward, an ivory letter card risen up out of it filling the upper two-thirds of frame, letter mostly blank with a small gold crown crest at its top and generous empty space below the crest, warm glow spilling from inside the envelope, enchanted forest bokeh behind. Same style as references. No text on the letter."

- [ ] **Step 2: Repeat for landscape 16:9** (same three prompts, "centered, occupying the middle third of frame" for settled/open).

- [ ] **Step 3: Show all six stills to the user. Iterate on any they reject.** Do not proceed to Task 2 without explicit approval of all six.

- [ ] **Step 4: Commit**

```bash
git add Assets/envelope/still-*.png
git commit -m "Envelope stills: six approved keyframes (portrait + landscape)"
```

---

### Task 2: Video clips (Seedance image-to-video)

**Files:**
- Create: `Assets/envelope/intro-m-raw.mp4`, `open-m-raw.mp4`, `intro-raw.mp4`, `open-raw.mp4`

**Interfaces:**
- Consumes: approved stills from Task 1.
- Produces: four raw clips where each intro's LAST frame is the exact FIRST frame of the matching open clip (seam guarantee below).

- [ ] **Step 1: Generate portrait intro** via higgsfield-generate (Seedance, image-to-video, ~3.5–4s, 9:16). Start frame: `still-flight-m.png`. End-frame/prompt guidance toward `still-settled-m.png` composition: "The envelope swoops forward through the enchanted forest and settles to a perfectly still, face-on, centered hover filling the frame; camera comes to rest; final second is completely motionless." Confirm cost first. Retry until the final ~0.5s is still and composition ≈ settled still.

- [ ] **Step 2: Extract the intro's actual last frame — this is the seam trick**

```bash
ffmpeg -sseof -0.05 -i Assets/envelope/intro-m-raw.mp4 -frames:v 1 -update 1 Assets/envelope/seam-m.png
```

- [ ] **Step 3: Generate portrait open** (Seedance i2v, ~2.5s, 9:16). **Start frame: `seam-m.png`** (NOT the settled still — guarantees a pixel-perfect stitch). Prompt: "The crimson wax seal cracks in two and the halves fall aside, the flap lifts open upward, an ivory letter with a small gold crown crest rises smoothly up out of the envelope; everything then holds perfectly still for the final half second. Camera locked off, no cuts." Retry until the final ~0.5s is motionless.

- [ ] **Step 4: Repeat Steps 1–3 for landscape** (`intro-raw.mp4`, `seam.png`, `open-raw.mp4`, 16:9).

- [ ] **Step 5: Show the four clips to the user; iterate until approved.**

- [ ] **Step 6: Commit**

```bash
git add Assets/envelope/*-raw.mp4 Assets/envelope/seam*.png
git commit -m "Envelope clips: raw Seedance intro/open, both orientations"
```

---

### Task 3: Post-production (stitch, encode, posters, measure ANCHOR)

**Files:**
- Create: `Website/assets/vid/envelope-m.mp4`, `Website/assets/vid/envelope.mp4`
- Create: `Website/assets/envelope-poster-m.webp`, `envelope-poster.webp`, `envelope-p.webp`
- Create: `Assets/envelope/anchor.txt`

**Interfaces:**
- Produces: final videos; `anchor.txt` containing two lines `ANCHOR_M=<seconds>` and `ANCHOR_D=<seconds>` (exact intro durations) consumed by Task 4.

**AMENDED (user directive 2026-07-26): the fly-in intro is CUT. The video is the
open clip only; the page loads directly on the sealed envelope (video frame 0).
ANCHOR is dead — everywhere later tasks reference `CFG.anchor`, the value is 0.**

- [ ] **Step 1: Encode portrait + landscape from the open clips only**

```bash
cd "/c/Users/yashk/OneDrive/Desktop/Glad You Were Born Today (Repo)"
ffmpeg -y -i Assets/envelope/open-m-raw.mp4 \
  -vf "scale=1080:1920:flags=lanczos,fps=30" \
  -an -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 23 -preset slow \
  -g 12 -movflags +faststart Website/assets/vid/envelope-m.mp4
ffmpeg -y -i Assets/envelope/open-raw.mp4 \
  -vf "scale=1920:1080:flags=lanczos,fps=30" \
  -an -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 23 -preset slow \
  -g 12 -movflags +faststart Website/assets/vid/envelope.mp4
```

- [ ] **Step 3: Verify sizes**

Run: `ls -la Website/assets/vid/envelope*.mp4`
Expected: `-m` ≤ 6 MB, landscape ≤ 12 MB. If over: bump `-crf` to 26 and re-encode.

- [ ] **Step 4: Posters + placeholder** (settled frame at ANCHOR)

Posters are the videos' FIRST frame (the sealed envelope):

```bash
ffmpeg -y -i Website/assets/vid/envelope-m.mp4 -frames:v 1 -update 1 -c:v libwebp -q:v 82 Website/assets/envelope-poster-m.webp
ffmpeg -y -i Website/assets/vid/envelope.mp4 -frames:v 1 -update 1 -c:v libwebp -q:v 82 Website/assets/envelope-poster.webp
ffmpeg -y -i Website/assets/vid/envelope-m.mp4 -frames:v 1 -vf "scale=40:-1,gblur=sigma=2" -update 1 -c:v libwebp -q:v 40 Website/assets/envelope-p.webp
```

- [ ] **Step 5: Commit**

```bash
git add Website/assets/vid/envelope*.mp4 Website/assets/envelope-*.webp Assets/envelope/anchor.txt
git commit -m "Envelope: stitched mobile-first videos, posters, anchor times"
```

---

### Task 4: Rewrite index.html — video skeleton (autoplay → pause at ANCHOR)

**Files:**
- Modify: `Website/index.html` (full rewrite of `<canvas id="scene">`, three.js CDN tag, sky/cloud markup+CSS, and the entire IIFE script; KEEP head metadata, fonts, `.title`, `.open-btn`, `.sheet-actions`, `.loading` CSS blocks and the `.ui`/`#sheet`/`#confetti`/`#loading` markup)

**Interfaces:**
- Produces: `state` machine (`'loading'|'flying'|'sealed'|'opening'|'open'|'closing'|'fallback'`), `const v = document.getElementById("scene-video")`, `CFG` object, `setState(s)` — Task 5/6 code plugs into these exact names.

- [ ] **Step 1: BEFORE editing, save the confetti block** — copy lines 618–696 of the current `Website/index.html` (from `// ---- Confetti ---` through the end of `confettiStep`, i.e. the `sizeConfetti`/`fireConfetti`/`confettiStep` functions and their variables) to `Assets/envelope/confetti-snippet.js`. It is reinserted verbatim in Step 3.

- [ ] **Step 2: Markup/CSS surgery** in `Website/index.html`:
  - Delete: `<div class="sky">`, the three `<span class="cloud …">` elements, `.sky`/`.cloud` CSS rules, `<canvas id="scene">`, and the `<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>` tag.
  - Replace canvas with (directly after `<body>`):

```html
<div class="stage" aria-hidden="true">
  <img class="stage__ph" id="ph" src="assets/envelope-p.webp" alt="" />
  <video id="scene-video" muted playsinline preload="auto"
         poster="assets/envelope-poster-m.webp"></video>
  <button class="tap-layer" id="taplayer" tabindex="-1" aria-hidden="true"></button>
</div>
```

  - Add CSS (keep existing `:root` vars; body background stays `var(--sky)`):

```css
.stage{position:fixed;inset:0;z-index:1;background:var(--sky);}
.stage__ph,#scene-video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;}
.stage__ph{filter:blur(14px);transform:scale(1.06);transition:opacity .5s ease;}
.stage__ph.gone{opacity:0;}
.tap-layer{position:absolute;inset:0;z-index:3;background:none;border:0;padding:0;cursor:pointer;-webkit-tap-highlight-color:transparent;}
.tap-layer[disabled]{cursor:default;}
```

- [ ] **Step 3: Replace the entire old IIFE `<script>`** with:

```html
<script>
(function () {
  "use strict";
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const portrait = window.matchMedia("(orientation: portrait)").matches;

  // ---- Config (anchor is 0: the video IS the open animation, frame 0 = sealed) ----
  const CFG = portrait ? {
    src: "assets/vid/envelope-m.mp4", poster: "assets/envelope-poster-m.webp",
    anchor: 0, frameW: 1080, frameH: 1920,
    letter: { x: 0.50, y: 0.46, h: 0.42 }   // fractions; re-measured in Task 5
  } : {
    src: "assets/vid/envelope.mp4", poster: "assets/envelope-poster.webp",
    anchor: 0, frameW: 1920, frameH: 1080,
    letter: { x: 0.50, y: 0.44, h: 0.55 }
  };

  const v = document.getElementById("scene-video");
  const ph = document.getElementById("ph");
  const tap = document.getElementById("taplayer");
  const btn = document.getElementById("toggle");
  const titleEl = document.querySelector(".title");
  const sheetEl = document.getElementById("sheet");
  const loading = document.getElementById("loading");

  v.poster = CFG.poster; v.src = CFG.src;

  // ---- State machine ----
  let state = "loading";
  function setState(s) { state = s; onState(); }

  const EPS = 1 / 30;      // one frame at 30fps
  const END = () => (v.duration || 6) - EPS;

  // rAF watcher pauses playback at a target time
  let watchRAF = 0;
  function playUntil(t, done) {
    cancelAnimationFrame(watchRAF);
    const step = () => {
      if (v.currentTime >= t - EPS) { v.pause(); v.currentTime = t; done(); return; }
      watchRAF = requestAnimationFrame(step);
    };
    v.play().catch(() => { v.currentTime = CFG.anchor; setState("sealed"); });  // play only ever follows a user gesture; catch resets safely
    watchRAF = requestAnimationFrame(step);
  }

  function onState() {
    const sealed = state === "sealed", open = state === "open";
    titleEl.classList.toggle("faded", !sealed);
    btn.hidden = !(sealed || open);
    btn.textContent = open ? "Seal it back" : "Break the seal";
    btn.setAttribute("aria-label", open ? "Close the envelope" : "Open the envelope");
    sheetEl.setAttribute("aria-hidden", open ? "false" : "true");
    if (!open) { sheetEl.style.opacity = "0"; sheetEl.style.pointerEvents = "none"; }
    if (open) revealSheet();                     // defined in Task 5
  }

  // ---- Boot: no intro — the page waits on the sealed envelope (frame 0) ----
  v.addEventListener("loadeddata", () => {
    loading.classList.add("gone"); ph.classList.add("gone");
    setState("sealed");
  }, { once: true });
  v.load();

  // ==== CONFETTI (verbatim from Assets/envelope/confetti-snippet.js) ====
  //  paste the saved block here, unchanged
  // ======================================================================

  window.addEventListener("resize", () => { sizeConfetti(); if (state === "open") revealSheet(); });
})();
</script>
```

Paste the confetti snippet at the marked slot. `revealSheet` is added in Task 5 — for this task only, add a temporary stub `function revealSheet(){}` directly above `onState` so the file runs.

- [ ] **Step 4: Verify in browser**

Run: `npx serve "Website" -l 8123` then open `http://localhost:8123` in Chrome with DevTools device emulation (iPhone 14 Pro).
Expected: blurred placeholder → sealed envelope (video frame 0, NOT playing) → title fades in, "Break the seal" appears. Nothing auto-plays. No console errors. Toggle emulation off and reload → landscape asset loads instead.

- [ ] **Step 5: Commit**

```bash
git add Website/index.html Assets/envelope/confetti-snippet.js
git commit -m "index.html: video skeleton replaces Three.js envelope"
```

---

### Task 5: Open/close interaction, overlay gating, button positioning

**Files:**
- Modify: `Website/index.html` (extend the Task 4 script)

**Interfaces:**
- Consumes: `v`, `CFG`, `state`, `setState`, `playUntil`, `EPS`, `END`, `sheetEl`, `tap`, `btn`, `fireConfetti` — exact names from Task 4.
- Produces: `revealSheet()` (replaces stub), `toggle()`.

- [ ] **Step 1: Measure the real letter fractions.** Open `Website/assets/vid/envelope-m.mp4` paused on its last frame (`ffmpeg -sseof -0.05 -i … -frames:v 1 last-m.png`, view it), and note where button block should sit on the letter: center-x, center-y, and usable height as fractions of 1080×1920. Update `CFG.letter` for portrait; repeat with the landscape file.

- [ ] **Step 2: Replace the `revealSheet` stub and add `toggle` + input wiring** (insert directly above the confetti block):

```js
  // ---- Buttons on the letter: cover-crop mapping -----------------------
  function revealSheet() {
    const vw = window.innerWidth, vh = window.innerHeight;
    const scale = Math.max(vw / CFG.frameW, vh / CFG.frameH);
    const dw = CFG.frameW * scale, dh = CFG.frameH * scale;
    const ox = (dw - vw) / 2, oy = (dh - vh) / 2;
    sheetEl.style.left = (CFG.letter.x * dw - ox) + "px";
    sheetEl.style.top  = (CFG.letter.y * dh - oy) + "px";
    const s = Math.min(1.18, Math.max(0.62, (CFG.letter.h * dh) / 440));
    sheetEl.style.setProperty("--s", s.toFixed(3));
    sheetEl.style.opacity = "1";
    sheetEl.style.pointerEvents = "auto";      // ONLY here does the overlay become tappable
  }

  // ---- Open / close (let: the Task 6 static-poster fallback reassigns it) ----
  let toggle = function () {
    if (state === "sealed") {
      setState("opening");
      if (reduced) { v.currentTime = END(); setState("open"); fireConfetti(); return; }
      playUntil(END(), () => { setState("open"); fireConfetti(); });
    } else if (state === "open") {
      setState("closing");
      if (reduced) { v.currentTime = CFG.anchor; setState("sealed"); return; }
      let last = performance.now();
      const back = (now) => {
        const dt = (now - last) / 1000; last = now;
        v.currentTime = Math.max(CFG.anchor, v.currentTime - dt * 1.6);
        if (v.currentTime <= CFG.anchor + EPS) { v.currentTime = CFG.anchor; setState("sealed"); return; }
        requestAnimationFrame(back);
      };
      requestAnimationFrame(back);
    }
  };

  tap.addEventListener("click", () => toggle());
  btn.addEventListener("click", () => toggle());
  if (/[?&]open/.test(location.search))        // QA shortcut, same as old page
    v.addEventListener("loadeddata", () => setTimeout(() => { v.currentTime = CFG.anchor; setState("sealed"); toggle(); }, 300), { once: true });
```

- [ ] **Step 3: Verify the interaction loop**

On `http://localhost:8123` (portrait emulation): tap anywhere → seal cracks, letter rises, video holds on last frame → confetti fires, In Real Life / Kids Zone fade in ON the letter, sized sensibly. "Seal it back" → smooth reverse to the settled frame, buttons vanish instantly. Repeat 3 open/close cycles — no drift, no seam jump. `http://localhost:8123/?open` lands open.

- [ ] **Step 4: Verify link safety.** In the console run a rapid-tap simulation during the intro and during opening:

```js
setInterval(() => {
  const el = document.elementFromPoint(Math.random()*innerWidth, Math.random()*innerHeight);
  if (el && el.closest(".sheet-btn")) console.error("LINK REACHABLE TOO EARLY", el);
}, 50);
```

Expected: zero errors before the open state; buttons reachable only after the letter holds.

- [ ] **Step 5: Commit**

```bash
git add Website/index.html
git commit -m "Envelope: tap open, reverse seal-back, gated letter buttons"
```

---

### Task 6: Fallbacks + accessibility

**Files:**
- Modify: `Website/index.html`

**Interfaces:**
- Consumes: everything from Tasks 4–5.

- [ ] **Step 1: Load-failure path** (insert after the boot block; there is no autoplay in this design, so no autoplay-refusal handling is needed):

```js
  // Video never arrives: static-poster fallback — the site must never dead-end
  const bail = setTimeout(() => {
    if (state !== "loading") return;
    v.remove();
    ph.src = CFG.poster; ph.classList.remove("gone"); ph.style.filter = "none"; ph.style.transform = "none";
    loading.classList.add("gone");
    setState("sealed");
    // in fallback, "open" = reveal buttons over the poster, centered
    toggle = function () {
      if (state === "sealed") { setState("open"); sheetEl.style.left = "50%"; sheetEl.style.top = "58%"; sheetEl.style.opacity = "1"; sheetEl.style.pointerEvents = "auto"; fireConfetti(); }
    };
    tap.addEventListener("click", () => toggle());
    btn.addEventListener("click", () => toggle());
  }, 8000);
  v.addEventListener("loadeddata", () => clearTimeout(bail), { once: true });
```

(Task 5 already declares `toggle` with `let` and wires listeners through arrow wrappers, so this reassignment takes effect for both the tap layer and the button.)

- [ ] **Step 2: Accessibility pass.** Confirm in the markup: `#toggle` keeps `class="open-btn sr-open"` and its focus styles; after `revealSheet()` runs, add `sheetEl.querySelector("a").focus({ preventScroll: true })` at the end of `revealSheet` so keyboard users land on the first choice; `.sheet-btn` computed size ≥ 44×44 px at `--s` minimum (check with DevTools at 320 px width — if under, raise the `0.62` clamp until it passes).

- [ ] **Step 3: Verify all fallbacks**

- DevTools → Network → throttle Offline after cache-clear reload: after 8 s the poster fallback appears, tap reveals buttons. 
- `prefers-reduced-motion` emulation: no intro; tap jumps straight to open frame + buttons.
- Keyboard only: Tab reaches "Break the seal", Enter opens, focus moves to "In Real Life", Tab reaches "Kids Zone".

- [ ] **Step 4: Commit**

```bash
git add Website/index.html
git commit -m "Envelope: autoplay/offline fallbacks + keyboard a11y"
```

---

### Task 7: Device QA + deploy

**AMENDED (user directive 2026-07-26): no preview deploy and NO local browser
verification — after Task 6's review passes, merge and deploy straight to
production. The user tests on the live site.**

- [ ] **Step 1: User tests on their phone against PRODUCTION** after Step 4:
tap-open smooth, buttons land on the letter, seal-back works. Fix and
redeploy until the user signs off.

- [ ] **Step 3: Desktop pass** on the preview URL: landscape tier loads, window resize while open re-seats the buttons, rapid-tap console check from Task 5 Step 4 passes.

- [ ] **Step 3b: Lighthouse mobile** (DevTools → Lighthouse, mobile, Performance): first contentful paint lands on the placeholder/poster and the score is not worse than the current production index.html (spec requirement).

- [ ] **Step 4: Merge + production**

```bash
cd "/c/Users/yashk/OneDrive/Desktop/Glad You Were Born Today (Repo)"
git checkout main && git merge envelope-video
git push origin main
cd Website && vercel --prod
```

Expected: https://born-today-world.vercel.app shows the new envelope. Verify once live.
