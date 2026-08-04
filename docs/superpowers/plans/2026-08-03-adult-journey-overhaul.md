# Adult Journey Overhaul Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Regenerate the adult journey's scenes 3–5 with genuinely adults-only footage, add a real 1920×1080 desktop tier for all five scenes, and fix the song (play once, autoplay attempt, honest mute).

**Architecture:** Static site (vanilla HTML/JS) at `Website/`, scroll-scrubbed video journey configured inline in `Website/adult/index.html` and driven by `tap-engine.js`. Footage is generated with the Higgsfield CLI (video: `seedance_2_0` continuations chained start-image → last-frame; stills: `videotape-alpha`), then encoded/stitched with ffmpeg scripts in `Website/adult/work/`. Music is a shared `Website/music.js` controlled by script-tag data attributes.

**Tech Stack:** Higgsfield CLI, ffmpeg/ffprobe, Python 3, vanilla JS, Vercel (repo `main` auto-deploys to production gywbt.com — NEVER merge without user approval).

**Spec:** `docs/superpowers/specs/2026-08-03-adult-journey-overhaul-design.md`

## Global Constraints

> **2026-08-03 CASTING pivot (user-directed, second pivot):** every human in every scene is a YOUNG ADULT in their 20s–30s — the site's target audience. No middle-aged people, no seniors/grandparents, no children. The GUARD sentence and all ground-scene prompts (scenes 1, 3, 4, 5, both tiers) are recast accordingly; sky scene 2 (no humans) is unaffected and its accepted assets stay. Page copy that celebrates older milestones ("Yes, they crash 40ths. And 50ths. And 70ths.", "Your mother is laughing…") gets reconciled with the young-adult cast at Task 9 (copy step), pending user wording approval at the preview.
>
> **2026-08-03 mid-execution design pivot (user-directed), supersedes any conflicting task text below:** the one-continuous-flight doctrine is replaced for scenes 2–5. New shot structure — scene 2 is a standalone SKY shot (cloud + clubhouse + Crasherz flying at dusk; no party, no crowd, no ground clutter); scene 3 opens with a TRANSITION (camera descends from sky through soft golden sparkle) and lands in the ground-level photo moment; scenes 3→4→5 are ground-level party scenes that flow via last-frame chaining; the cloud/clubhouse is OUT OF FRAME in all ground scenes. Prompt doctrine: LEAN — one scene idea per prompt, minimal element lists; the round-1 failure was overloaded prompts rendering wispy clouds and cluttered frames. Chaining: leg 2 does not chain from scene 1 (the runtime 0.15s crossfade bridges quiet→sky); leg 3 does not chain from leg 2 (the in-clip transition IS the bridge); legs 4 and 5 chain from their predecessors' last frames as before. The same structure applies to the landscape tier (lleg/lstill 2–5); scene 1 prompts are unaffected.

- Work only in `C:\Users\yashk\gywbt-site` on branch `adult-overhaul`. Never push `main`. Pushing the branch creates a Vercel PREVIEW deployment only.
- Scene 1 portrait (`quiet`) is frozen — do not regenerate it. Portrait scenes 2–5 (`glowup`, `photo`, `patio`, `sendoff`) ALL regenerate (scope expanded 2026-08-03 with user approval: the Task 1 audit found children in glowup t4–t8 and photo t0–t3, not just patio/sendoff).
- Every new generation prompt MUST end with the adults-only guard sentence defined in Task 3 (verbatim). Every generated clip/still MUST pass the child-audit (Task 1 procedure) before it is accepted.
- Encode settings are fixed (from `Website/adult/work/encode.sh`): desktop master H.264 CRF 20 GOP 8 `-sc_threshold 0 -movflags +faststart`, mobile 720-wide CRF 23 GOP 4, posters = first frame of the ENCODED clip.
- Asset URL cache-busting: all rewired asset references in `adult/index.html` bump to `?v=6`.
- The envelope page (`Website/index.html`) keeps its looping classical strings — `data-once` is opt-in and must NOT be added there.
- The user's second working copy at `C:\Users\yashk\OneDrive\Desktop\Glad You Were Born Today (Repo)` is read-only reference material (raw legs, job JSONs). Never commit or modify anything there.
- A second `git remote` does not exist; `origin` is `YASHKGLADYOUWEREBORNTODAYFINALIAMSODONEBROHOLYCRAP`.
- Generation spends Higgsfield credits (~5–30/video, ~3–9/still). Two hard user checkpoints: after the landscape stills (Task 6) and before any re-roll batch beyond 3 attempts on a single asset.

---

### Task 1: Child-audit script + audit of current footage

Establishes the objective pass/fail tool every later generation task reuses, and pins down exactly which live scenes contain children.

**Files:**
- Create: `Website/adult/work/audit_frames.py`
- Create: `Website/adult/work/audit-2026-08-03.md` (findings)

**Interfaces:**
- Produces: `python audit_frames.py <video-or-image> [<outdir>]` → writes 1 frame/second as `<outdir>/<stem>-t<sec>.jpg`. Manual (or agent-visual) inspection of those frames is the pass/fail gate: PASS = zero human children/babies/minors visible in any frame. The four Crasher characters and Starry are NOT children — they are the vinyl-toy mascots and always allowed.

- [ ] **Step 1: Write the frame-ripper**

```python
# Website/adult/work/audit_frames.py
"""Rip 1 frame/second from a clip (or copy a still) for child-audit review.
Usage: python audit_frames.py path/to/clip.mp4 [outdir]   (outdir default: ./audit)"""
import os, subprocess, sys

src = sys.argv[1]
outdir = sys.argv[2] if len(sys.argv) > 2 else "audit"
os.makedirs(outdir, exist_ok=True)
stem = os.path.splitext(os.path.basename(src))[0]

if src.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
    out = os.path.join(outdir, f"{stem}-t0.jpg")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-q:v", "3", out], check=True)
    print(out)
    sys.exit(0)

dur = float(subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
    capture_output=True, text=True, check=True).stdout.strip())
t = 0.0
while t < dur:
    out = os.path.join(outdir, f"{stem}-t{int(t)}.jpg")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", src,
                    "-frames:v", "1", "-q:v", "3", out], check=True)
    print(out)
    t += 1.0
```

- [ ] **Step 2: Run it against all five live portrait masters**

```bash
cd Website/adult/work
for s in quiet glowup photo patio sendoff; do python audit_frames.py ../assets/vid/$s.mp4 audit/$s; done
```
Expected: ~8 JPEGs per scene in `audit/<scene>/`.

- [ ] **Step 3: Inspect every frame and record findings**

View each `audit/<scene>/*.jpg` (Read tool renders images). For each scene record in `audit-2026-08-03.md`: scene, verdict (CLEAN / HAS-CHILDREN), and which timestamps show children. Known from spot-checks: `patio` has a human toddler at the table (~t5), `sendoff` has a child in the foreground (~t5). Verify `photo` across ALL its frames (t5 was clean; t2 unverified), and confirm `quiet`/`glowup` are clean (they are frozen either way — findings are informational).

- [ ] **Step 4: Commit**

```bash
git add Website/adult/work/audit_frames.py Website/adult/work/audit-2026-08-03.md
git commit -m "Add child-audit frame ripper + audit of live adult footage"
```
(Do NOT commit the `audit/` JPEGs — add nothing else.)

---

### Task 2: music.js — play-once mode, real autoplay attempt, honest mute

**Files:**
- Modify: `Website/music.js`
- Modify: `Website/adult/index.html` (line 47: the music script tag)
- Create: `Website/adult/work/music-qa.md` (manual QA matrix + results)

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: `<script src="../music.js?v=14" data-autostart data-once data-start="11">` behavior contract: attempts `play()` at load; if blocked, first pointer gesture NOT on `#sw-music` starts it; on `ended` playback stops, button shows off; ♪ click replays from `data-start`. `window.swMusic.on/off/swap` signatures unchanged.

- [ ] **Step 1: Add `data-once` (stop at end instead of relooping)**

In `music.js`, next to the `AUTO` flag read, add:

```js
  var ONCE = !!(tag && tag.hasAttribute('data-once'));
```

Replace the `ended` handler and the `audio.loop` assignment:

```js
    audio.loop = (START === 0) && !ONCE;
    audio.addEventListener('ended', function () {
      if (ONCE) { setUi(false); try { audio.currentTime = START; } catch (e) {} return; }
      if (START > 0) { seekIntoTrack(); audio.play().catch(function () {}); }
    });
```

- [ ] **Step 2: Make button state honest (single UI function, only called from truth points)**

Split UI updates out of `set()` so nothing flips the button optimistically:

```js
    function setUi(on) {
      btn.classList.toggle('is-on', on);
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      btn.setAttribute('aria-label', on ? 'Pause the theme song' : 'Play the theme song');
    }

    function set(on) {
      if (on) {
        seekIntoTrack();
        audio.play().then(function () {
          setUi(true);
          try { sessionStorage.setItem(KEY, '1'); } catch (e) {}
        }).catch(function () { setUi(false); /* blocked: stay off, next tap retries */ });
      } else {
        audio.pause();
        setUi(false);
        try { sessionStorage.setItem(KEY, '0'); } catch (e) {}
      }
    }
```

(`ended` also fires `setUi(false)` via Step 1 — an ended track shows the off state.)

- [ ] **Step 3: First-gesture fallback must ignore the mute button**

Replace the tail block (`var stored = ...` through the two listeners) with:

```js
    var stored = null;
    try { stored = sessionStorage.getItem(KEY); } catch (e) {}
    var wanted = stored === '1' || (AUTO && stored !== '0');
    if (wanted) {
      set(true);   // real autoplay attempt at load; works when the visit already had a gesture
      var once = function (e) {
        window.removeEventListener('pointerdown', once);
        window.removeEventListener('touchend', once);
        if (e && e.target && e.target.closest && e.target.closest('#sw-music')) return; // their first tap IS the mute button — respect it
        if (audio.paused) set(true);
      };
      window.addEventListener('pointerdown', once);
      window.addEventListener('touchend', once, { passive: true });
    }
```

- [ ] **Step 4: Syntax check**

Run: `node --check Website/music.js`
Expected: no output (exit 0).

- [ ] **Step 5: Wire the adult page**

In `Website/adult/index.html` change the music script tag to:

```html
<script src="../music.js?v=14" data-autostart data-once data-start="11"></script>
```

Grep-verify no other page gained `data-once`: `grep -rn "data-once" Website/ --include=*.html` → only `adult/index.html`.

- [ ] **Step 6: Manual QA against a local server**

```bash
cd Website && python -m http.server 8000
```
Record each row's result in `Website/adult/work/music-qa.md`:

| # | Steps (Chrome, fresh profile/incognito) | Expected |
|---|---|---|
| 1 | Open `/adult/` directly, touch nothing, wait | Music blocked; ♪ shows OFF (never lies "on") |
| 2 | From row 1, click anywhere on the page | Music starts at 0:11; ♪ ON |
| 3 | From row 1, click ♪ FIRST | The generic first-gesture listener does NOT hijack the tap; the ♪ click acts as a normal toggle (music starts, ♪ ON). Clicking ♪ again pauses it, sets `sw-music-on=0`, and later page clicks do NOT restart it. (While music is PLAYING, a first tap on ♪ mutes and sticks.) |
| 4 | Let the song play to the end | Playback stops (no loop), ♪ flips OFF |
| 5 | After row 4, click ♪ | Song replays from 0:11 |
| 6 | Open `/` (envelope), tap open, choose grown-ups | Music carries into `/adult/` and starts without a new tap |
| 7 | Envelope page: let strings play 2+ minutes | Strings still loop (envelope unaffected) |

- [ ] **Step 7: Commit**

```bash
git add Website/music.js Website/adult/index.html Website/adult/work/music-qa.md
git commit -m "Adult music: play once, honest mute, autoplay attempt with first-touch fallback"
```

---

### Task 3: Harden the adults-only prompts (portrait 3–5 + landscape variants)

**Files:**
- Create: `Website/adult/work/redo2/` (this round's pipeline dir)
- Create: `Website/adult/work/redo2/GUARD.txt`
- Create: `Website/adult/work/redo2/leg_{3,4,5}.txt` (portrait), `Website/adult/work/redo2/lleg_{1,2,3,4,5}.txt` (landscape), `Website/adult/work/redo2/lstill_{1,2,3,4,5}.txt` (landscape stills)

**Interfaces:**
- Consumes: existing prompts `Website/adult/work/redo/leg_*.txt`, `redo/preamble.txt`, `redo/characters.txt`, plus Task 1's audit verdicts.
- Produces: final prompt files used verbatim by Tasks 5, 6, 7. Every file ends with the GUARD sentence.

- [ ] **Step 1: Write the guard**

`Website/adult/work/redo2/GUARD.txt` (single line, used verbatim at the END of every prompt):

```
Every human being in the scene is a grown adult in their 30s, 40s, 60s or 70s — absolutely no human children, no babies, no toddlers, no minors, no small human figures of any kind anywhere in frame or background; the only child-sized figures allowed are the three vinyl-toy Crasher mascots in their hooded onesies.
```

Why: the previous redo failed because "toddler-sized creatures … hooded onesies" pulls the model toward rendering real human toddlers (the live patio scene shows one wearing a Crasher-print hoodie). The guard names that failure mode explicitly.

- [ ] **Step 2: Portrait legs 2–5**

For each of `redo/leg_2.txt`, `redo/leg_3.txt`, `redo/leg_4.txt`, `redo/leg_5.txt`: copy into `redo2/leg_N.txt`, then (a) replace cast phrases that imply families with explicitly adult casting — e.g. leg_3's "laughing guests" → "laughing adult friends in their 30s and 40s"; scan legs 4–5 for "family", "grandparents arm in arm with…", or any wording implying children and recast per the on-screen copy ("Yes, they crash 40ths", "Enchantment doesn't card") — grandparents themselves are fine; (b) append `\n` + the GUARD sentence. Keep all camera-language and Crasher/cloud descriptions byte-identical otherwise.

- [ ] **Step 3: Landscape stills 1–5**

Write `redo2/lstill_N.txt` for scenes quiet(1)/glowup(2)/photo(3)/patio(4)/sendoff(5). Formula per file: take `redo/preamble.txt`, change the first clause to landscape ("Cinematic photorealistic wide photograph, 16:9 landscape framing, shot on a full-frame camera with a 35mm lens" — rest of the preamble unchanged; drop the "safe for portrait phone screens" clause, replace with "composed with the focal subjects in the central two-thirds, generous lateral headroom for widescreen"), then append the scene description. Scene descriptions: for 1–2 derive from `redo/still_quiet_v2.txt` / `redo/still_crash.txt` (same content/mood — these scenes are only being reframed); for 3–5 derive the settled final composition described at the end of the corresponding `redo2/leg_N.txt`. Append the GUARD sentence to all five.

- [ ] **Step 4: Landscape legs 1–5**

Write `redo2/lleg_N.txt`: copy the corresponding portrait leg prompt (`redo/leg_1.txt`, `redo/leg_2.txt` for 1–2; `redo2/leg_N.txt` for 3–5), change "vertical 9:16" to "wide 16:9 landscape", and append the GUARD (1–2 need it added too). No other changes.

- [ ] **Step 5: Verify guard coverage + commit**

```bash
cd Website/adult/work/redo2
for f in leg_2.txt leg_3.txt leg_4.txt leg_5.txt lleg_*.txt lstill_*.txt; do grep -q "no human children" "$f" || echo "MISSING GUARD: $f"; done
```
Expected: no output. Then:

```bash
git add Website/adult/work/redo2/
git commit -m "Adults-only hardened prompts for portrait 3-5 and landscape tier"
```

---

### Task 4: Stage generation inputs (reference images + chain start frames)

**Files:**
- Create: `Website/adult/work/redo2/refs/` (character reference images)
- Create: `Website/adult/work/redo2/start_leg2.png` (portrait chain restart point)
- Create: `Website/adult/work/redo2/fetch_refs.py`

**Interfaces:**
- Consumes: job records `Website/adult/work/redo/leg_3.json` (media URLs), encoded `Website/adult/assets/vid/glowup.mp4`.
- Produces: `refs/ref_1.png`, `refs/ref_2.png`, … (character reference images, in the original media order, start_image excluded) and `start_leg3.png` — consumed by Tasks 5–7's generation commands.

- [ ] **Step 1: Pull the reference images the previous run used**

```python
# Website/adult/work/redo2/fetch_refs.py
"""Download the non-start-image reference medias recorded in redo/leg_3.json."""
import json, os, urllib.request

os.makedirs("refs", exist_ok=True)
d = json.load(open("../redo/leg_3.json"))
j = d[0] if isinstance(d, list) else d
medias = j["params"]["medias"]
n = 0
for m in medias:
    if m.get("role") == "start_image":
        continue
    n += 1
    url = m["data"]["url"]
    out = f"refs/ref_{n}.png"
    urllib.request.urlretrieve(url, out)
    print(out, "<-", url)
print(f"{n} refs")
```

Run: `cd Website/adult/work/redo2 && python fetch_refs.py`
Expected: ≥1 `refs/ref_*.png` downloaded. **If the CloudFront URLs are dead (403/404):** extract character reference crops instead — Starry and the Crashers are sharply visible in `../../assets/vid/sendoff.mp4` around t=1s and in `Assets/` character art at repo root; save equivalent PNGs into `refs/` and note the substitution in the commit message.

- [ ] **Step 2: Extract the leg-2 start frame (scene 1's final frame)**

```bash
cd Website/adult/work/redo2
ffmpeg -y -v error -sseof -0.06 -i ../../assets/vid/quiet.mp4 -frames:v 1 start_leg2.png
```
View `start_leg2.png` to confirm it's the end of the quiet-party scene (scene 1 is CLEAN and frozen; the regenerated chain starts from its final frame).

- [ ] **Step 3: Commit (scripts only, not media)**

```bash
git add Website/adult/work/redo2/fetch_refs.py
git commit -m "Add reference-image fetcher for the regen pipeline"
```

---

### Task 5: Generate portrait legs 2–5 (chained, audited)

**Files:**
- Create: `Website/adult/work/redo2/gen_leg.sh`
- Create: `Website/adult/work/redo2/leg_{2,3,4,5}.mp4` (raw, gitignored via existing rules)

**Interfaces:**
- Consumes: `redo2/leg_N.txt` (Task 3), `redo2/refs/*.png` + `redo2/start_leg2.png` (Task 4), `audit_frames.py` (Task 1).
- Produces: accepted raw clips `redo2/leg_2.mp4` … `leg_5.mp4` for Task 8's encode. Chain rule: each `start_legN+1.png` = last frame of the accepted `leg_N.mp4`.

- [ ] **Step 1: Write the generator (mirrors the recorded job params)**

```bash
#!/bin/bash
# gen_leg.sh <name> <prompt.txt> <start.png> <aspect>   e.g.: ./gen_leg.sh leg_3 leg_3.txt start_leg3.png 9:16
# Params mirror redo/leg_3.json: seedance_2_0, mode std, 1080p, 8s.
set -u
NAME="$1"; PROMPT="$2"; START="$3"; AR="$4"
REFS=$(ls refs/ref_*.png 2>/dev/null | sed 's/^/--image /' | tr '\n' ' ')
higgsfield generate create seedance_2_0 \
  --prompt "$(cat "$PROMPT")" \
  --start-image "$START" $REFS \
  --mode std --resolution 1080p --aspect_ratio "$AR" --duration 8 \
  --wait --wait-timeout 20m --json > "$NAME.json" 2> "$NAME.err"
url=$(python -c "
import json,sys
try:
    d=json.load(open('$NAME.json')); d=d[0] if isinstance(d,list) else d
    print(d.get('result_url') or (d.get('results') or [{}])[0].get('url') or '')
except Exception: print('')")
[ -n "$url" ] && curl -fsSL "$url" -o "$NAME.mp4" && echo "OK $NAME.mp4" || { echo "FAIL $NAME"; head -c 300 "$NAME.json"; head -2 "$NAME.err"; }
```

First run `higgsfield generate create --help`; if the reference-image flag is not `--image`, adjust the `REFS` line to the actual flag (the recorded job attaches them as `media_input` alongside `start_image`).

- [ ] **Step 2: Generate + audit leg 2 (this costs credits)**

```bash
cd Website/adult/work/redo2 && ./gen_leg.sh leg_2 leg_2.txt start_leg2.png 9:16
python ../audit_frames.py leg_2.mp4 audit/leg_2
```
Inspect every `audit/leg_2/*.jpg`: (a) zero human children (GUARD held), (b) first frame visually continues from `start_leg2.png`, (c) characters on-model. Re-roll on failure (max 3 attempts, keep `leg_2_vN.mp4` history like the previous redo did). If 3 attempts all fail → STOP, show the user the best frames, get direction.

- [ ] **Step 3: Chain and repeat for legs 3, 4 and 5**

```bash
for n in 3 4 5; do
  ffmpeg -y -v error -sseof -0.06 -i leg_$((n-1)).mp4 -frames:v 1 start_leg$n.png
  ./gen_leg.sh leg_$n leg_$n.txt start_leg$n.png 9:16
  python ../audit_frames.py leg_$n.mp4 audit/leg_$n
  # STOP each iteration: inspect audit frames (children/continuity/on-model) before chaining on; re-roll ladder as above
done
```

- [ ] **Step 4: Commit pipeline artifacts (scripts + job JSONs, no video)**

```bash
git add Website/adult/work/redo2/gen_leg.sh Website/adult/work/redo2/leg_*.json
git commit -m "Generate adults-only portrait legs 2-5 (audited, chained)"
```

---

### Task 6: Landscape stills for all five scenes — USER CHECKPOINT

**Files:**
- Create: `Website/adult/work/redo2/gen_still.sh`
- Create: `Website/adult/work/redo2/lstill_{1..5}.png`

**Interfaces:**
- Consumes: `redo2/lstill_N.txt` (Task 3), `redo2/refs/*.png` (Task 4).
- Produces: five approved 16:9 stills — the start images for Task 7's landscape legs. **HARD GATE: the user approves these before Task 7 spends video credits.**

- [ ] **Step 1: Write the still generator (mirrors redo/still_crash.json: videotape-alpha, 2k)**

```bash
#!/bin/bash
# gen_still.sh <name> <prompt.txt>    e.g.: ./gen_still.sh lstill_1 lstill_1.txt
set -u
NAME="$1"; PROMPT="$2"
REFS=$(ls refs/ref_*.png 2>/dev/null | sed 's/^/--image /' | tr '\n' ' ')
higgsfield generate create videotape-alpha \
  --prompt "$(cat "$PROMPT")" $REFS \
  --resolution 2k --aspect_ratio 16:9 \
  --wait --wait-timeout 10m --json > "$NAME.json" 2> "$NAME.err"
url=$(python -c "
import json,sys
try:
    d=json.load(open('$NAME.json')); d=d[0] if isinstance(d,list) else d
    print(d.get('result_url') or (d.get('results') or [{}])[0].get('url') or '')
except Exception: print('')")
[ -n "$url" ] && curl -fsSL "$url" -o "$NAME.png" && echo "OK $NAME.png" || { echo "FAIL $NAME"; head -c 300 "$NAME.json"; }
```

- [ ] **Step 2: Generate all five + self-audit**

```bash
cd Website/adult/work/redo2
for n in 1 2 3 4 5; do ./gen_still.sh lstill_$n lstill_$n.txt; done
for n in 1 2 3 4 5; do python ../audit_frames.py lstill_$n.png audit/lstill; done
```
Inspect: no children anywhere; scenes 1–2 match the portrait originals' content and mood (compare against `../../assets/quiet.webp`, `../../assets/glowup.webp`); characters on-model. Re-roll individual failures (≤3 attempts each).

- [ ] **Step 3: Post the stills (checkpoint waived by user 2026-08-03)**

Show the user all five landscape stills for visibility, but do NOT block on approval — Task 7 starts immediately once the stills pass self-audit. (The user explicitly waived the blocking gate: "no user checkpoint just post them".)

- [ ] **Step 4: Commit job records**

```bash
git add Website/adult/work/redo2/gen_still.sh Website/adult/work/redo2/lstill_*.json
git commit -m "Landscape anchor stills for all five adult scenes"
```

---

### Task 7: Generate landscape legs 1–5 (chained, audited)

**Files:**
- Create: `Website/adult/work/redo2/lleg_{1..5}.mp4` (raw)

**Interfaces:**
- Consumes: `redo2/lleg_N.txt` (Task 3), approved `lstill_1.png` (Task 6), `gen_leg.sh` (Task 5), `audit_frames.py` (Task 1).
- Produces: accepted raw `lleg_1..5.mp4` for Task 8's encode. Chain rule: `lstill_1.png` starts leg 1; thereafter `lstart_N.png` = last frame of the accepted previous leg (the approved `lstill_N.png` serve as composition targets, not start frames, keeping the flight continuous).

- [ ] **Step 1: Generate the chain**

```bash
cd Website/adult/work/redo2
cp lstill_1.png lstart_1.png
for n in 1 2 3 4 5; do
  ./gen_leg.sh lleg_$n lleg_$n.txt lstart_$n.png 16:9
  python ../audit_frames.py lleg_$n.mp4 audit/lleg_$n
  # STOP HERE each iteration: inspect audit frames (children / continuity / on-model) before chaining on
  ffmpeg -y -v error -sseof -0.06 -i lleg_$n.mp4 -frames:v 1 lstart_$((n+1)).png
done
```
Run this loop MANUALLY one iteration at a time — each leg's audit must pass before its last frame seeds the next. Re-roll ladder ≤3 per leg; a 3-strike leg pauses for user direction.

- [ ] **Step 2: Commit job records**

```bash
git add Website/adult/work/redo2/lleg_*.json
git commit -m "Landscape legs 1-5 generated as one chained flight (audited)"
```

---

### Task 8: Encode both tiers, stitch the mobile journey, compute spans

**Files:**
- Create: `Website/adult/work/redo2/finish.py` (adapted from `redo/finish_adult_redo.py`)
- Create: `Website/adult/work/redo2/out/` (staged encodes — NOT yet copied into `assets/`)

**Interfaces:**
- Consumes: raw `leg_{2,3,4,5}.mp4` (Task 5), `lleg_{1..5}.mp4` (Task 7), frozen original `../redo/leg_1.mp4` — **fallback if absent in this clone:** the raw leg 1 also lives in the OneDrive copy `.../Website/adult/work/redo/leg_1.mp4` (read-only; copy it in, never modify there). If neither exists, re-derive from the committed encoded master `../../assets/vid/quiet.mp4` (already a CRF-20 encode — acceptable as a stitch source since the mobile tier re-encodes to CRF 23 anyway).
- Produces: `out/` containing — portrait: `glowup-m.mp4`, `photo-m.mp4`, `patio-m.mp4`, `sendoff-m.mp4`, `journey-m.mp4`, portrait posters/stills for 2–5 (portrait masters for 2–5 are NOT produced — they retire; see Task 9); landscape: `quiet.mp4` … `sendoff.mp4` (1920×1080 masters) + `<scene>-poster.webp`; plus `spans.json` (the five `[start,end]` pairs). Consumed by Task 9.

- [ ] **Step 1: Adapt the finisher**

Copy `../redo/finish_adult_redo.py` to `redo2/finish.py` and change ONLY:
1. `RD = r"C:\Users\yashk\gywbt-site\Website\adult\work\redo2"`.
2. Its five-leg portrait input list: leg 1 points at the frozen raw file (resolved per Interfaces above), legs 2–5 at this round's `leg_{2,3,4,5}.mp4`.
3. Add a landscape pass reusing its `sh()` helpers — for each `lleg_N.mp4` → scene name (`quiet glowup photo patio sendoff`):

```python
# landscape masters: 1920x1080, CRF 20, GOP 8 (same doctrine as encode.sh, landscape geometry)
sh(["ffmpeg", "-y", "-v", "error", "-i", f"lleg_{n}.mp4", "-an",
    "-vf", "scale=1920:1080,unsharp=5:5:0.8:5:5:0.0",
    "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
    "-g", "8", "-keyint_min", "8", "-sc_threshold", "0", "-movflags", "+faststart",
    os.path.join(OUT, f"{scene}.mp4")])
sh(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(OUT, f"{scene}.mp4"),
    "-frames:v", "1", "-qscale:v", "75", os.path.join(OUT, f"{scene}-poster.webp")])
```
4. Dump the computed spans: `json.dump(spans, open(os.path.join(OUT, "spans.json"), "w"))`.

- [ ] **Step 2: Run it**

Run: `cd Website/adult/work/redo2 && python finish.py`
Expected: `out/` populated; console shows the SSIM seam table. Gate: no seam scores drastically below the shipped chain's 0.38–0.70 band without a visual frame-pair check clearing it (same-scene + confetti-drift = pass; different scene = FAIL → re-roll that leg via Task 5/7 procedure).

- [ ] **Step 3: Verify geometry + duration of every output**

```bash
cd Website/adult/work/redo2/out
for f in *.mp4; do echo "$f: $(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$f")"; done
```
Expected: `journey-m` + `*-m` = 720×1280; the five scene masters = 1920×1080. Confirm `spans.json` holds five pairs and the last end ≈ `journey-m.mp4` duration.

- [ ] **Step 4: Commit the finisher**

```bash
git add Website/adult/work/redo2/finish.py
git commit -m "Add two-tier finisher: encode, stitch, spans, seam gate"
```

---

### Task 9: Wire the page — new assets, desktop tier, spans, copy

**Files:**
- Modify: `Website/adult/index.html`
- Modify/Create under: `Website/adult/assets/` (encoded outputs move in here)

**Interfaces:**
- Consumes: `redo2/out/*` + `spans.json` (Task 8).
- Produces: the shippable page. `sections[n].clip` → landscape masters `assets/vid/<scene>.mp4?v=6`; `clipMobile` unchanged for 1–2, `?v=6` for 3–5; `journeyMobile.clip = 'assets/vid/journey-m.mp4?v=6'`; `journeyMobile.spans` = spans.json values.

- [ ] **Step 1: Move staged outputs into assets**

```bash
cd Website/adult
cp work/redo2/out/journey-m.mp4 assets/vid/
cp work/redo2/out/{glowup,photo,patio,sendoff}-m.mp4 assets/vid/
cp work/redo2/out/{quiet,glowup,photo,patio,sendoff}.mp4 assets/vid/     # landscape masters REPLACE the portrait stand-ins
cp work/redo2/out/*.webp assets/    # posters + stills produced by finish.py (portrait 2-5 + landscape)
```
Note: the old portrait 1080×1920 "masters" for 2–5 are intentionally overwritten by landscape files of the same name — desktop was the only consumer.

- [ ] **Step 2: Update the inline config**

In `adult/index.html`: bump every touched asset ref to `?v=6` (all five `clip`, the 2–5 `clipMobile`/`still`/`poster`/`posterMobile`, `journeyMobile.clip`, `journeyMobile.poster`); paste the five `spans.json` pairs into `journeyMobile.spans`.

- [ ] **Step 3: Delete the letterbox hack**

Remove from the `<style>` block (lines 24–27 of the current file):

```css
  /* Desktop: letterbox the portrait flight centered; copy floats in the left margin. */
  @media (min-width:861px){
    .sw-scene__video,.sw-scene__still,.tw video,.tw .tw-still{object-fit:contain !important;object-position:center !important;}
  }
```

- [ ] **Step 4: Fix the SEO copy**

In the `data-sw-seo` block replace `<p>Hugs from the little ones included.</p>` with `<p>Hugs from your favorite people included.</p>`. Check the visible section copy against the accepted footage (Task 5 audit frames): if a section's `body`/`tags` now contradicts what's on screen, adjust the wording minimally and mirror it into the SEO block.

- [ ] **Step 5: Local verification**

```bash
cd Website && python -m http.server 8000
```
- Desktop viewport (≥1280 px): every scene shows full-bleed widescreen footage (no pillarboxing), scroll scrubs smoothly through all five, copy readable at 1280 and 2560 widths.
- Phone emulation (portrait): journey plays via the stitched file; scene boundaries land where the beats change; scenes 1–2 unchanged.
- Reduced-motion emulation: stills render. DevTools console: zero errors.
- Asset sweep: `python - <<'EOF'` script or curl loop — every URL referenced in `adult/index.html` (both tiers, `?v=6`) returns 200 on localhost.

- [ ] **Step 6: Commit**

```bash
git add Website/adult/assets Website/adult/index.html
git commit -m "Wire adults-only journey: real landscape desktop tier, new spans, letterbox hack removed"
```

---

### Task 10: Preview deployment + user sign-off gate

**Files:**
- None new (operations only).

**Interfaces:**
- Consumes: the completed branch.
- Produces: a Vercel preview URL for user review. Merge to `main` happens ONLY on explicit user approval, as its own step afterward.

- [ ] **Step 1: Push the branch**

```bash
git push -u origin adult-overhaul
```

- [ ] **Step 2: Confirm the preview deployment builds**

```bash
vercel ls born-today-world
```
Expected: a new Preview deployment (seconds–minutes old), status Ready. Note: preview URLs sit behind Vercel authentication — the user opens it logged in to Vercel, or generate a shareable link from the Vercel dashboard if needed.

- [ ] **Step 3: Hand the preview to the user**

Give the user the preview URL with a checklist: phone portrait run-through (scenes 3–5 adults-only, seams, music once-through + mute), desktop run-through (real widescreen, no letterboxing). WAIT for approval.

- [ ] **Step 4 (only after explicit user approval): merge to production**

```bash
git checkout main && git pull && git merge --no-ff adult-overhaul -m "Adult journey: adults-only scenes 3-5, real desktop tier, music fixes"
git push origin main
```
Then verify gywbt.com serves `?v=6` assets and spot-check the live adult page.

---

## Self-review notes

- Spec coverage: portrait 3–5 regen → Tasks 3/4/5; landscape tier all five → Tasks 3/6/7/8/9; letterbox removal + spans + `?v=6` → Task 9; music (once/autoplay/mute) → Task 2; SEO copy → Task 9 Step 4; audit/QA gates → Tasks 1, 5, 6, 7, 8, 9; deploy rails + user gate → Task 10; stills credit checkpoint → Task 6 Step 3.
- The CLI reference-image flag is verified against `--help` in Task 5 Step 1 before any credits are spent; all other generation params are copied from the recorded job JSONs.
- Frozen raw legs 1–2 resolution order (redo2 → OneDrive read-only → encoded masters) is spelled out in Task 8's Interfaces.
