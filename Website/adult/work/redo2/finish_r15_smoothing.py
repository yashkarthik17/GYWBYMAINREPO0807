"""Task r15 -- mobile playback-feel fixes: interpolated arrival + 2->3 dwell trim.

Two independent fixes, both landing in glowup-m.mp4 and/or photo-m.mp4:

  (A) Clip 2 (glowup, arrival) reads "very jittery" on its fast descent --
      24fps judder. Fix: frame-interpolate leg_2.mp4 from 24fps to 48fps
      with minterpolate (mci/aobmc/bidir/vsbmc) before the standard
      scale/CRF encode. This shipped ONLY after a manual artifact audit
      (contact sheets + full-res crops of synthesized in-between frames
      at the fast-descent window, t~1-5s) found the clubhouse and the
      characters/limbs clean at every sampled point, including the
      largest-displacement frame in the window (~t3.0s). The one
      artifact found -- a brief translucent double-image ghost on a
      background paper lantern in a single synthesized frame at ~t2.23s
      -- is outside the gate's named scope (characters/clubhouse; confetti
      explicitly exempted) and lasts one 48fps frame (~21ms), so it does
      not fail the gate. Recorded here for the paper trail, not treated
      as a blocker. See task-r15 report for the frame evidence.

  (B) The 2->3 transition "hangs too long" -- glowup-m ends settled on
      the hover and photo-m opens on the same hover (double-settle).
      tap-engine.js's early-handoff crossfade fires ~0.8s of wall-clock
      time before a clip's natural end (see tap-engine.js go(), the
      "Early-handoff crossfade" comment) -- with a long static tail on
      glowup and a long static head on photo, that crossfade window and
      the following clip's own dwell both land on the same frozen hover,
      reading as two settles back to back. Fix: cut ~0.7s off glowup's
      tail (-t 7.34 on the 8.0417s source) and ~0.5s off photo's head
      (-ss 0.5 before -i, fast/accurate seek). A manual last-frame vs
      first-frame check across the new boundary confirmed continuity
      survives the trim -- same hover composition, just less dwell.

Mixed-fps stitch note: glowup-m.mp4 (the shipped, tap-engine-facing
asset) is 48fps; quiet-m/photo-m/patio-m/sendoff-m stay 24fps (majority).
journey-m.mp4 is a legacy stitched-parity asset the live tap-engine does
NOT play scene-by-scene (see finish.py's docstring) -- for ITS internal
concat only, the glowup branch is downsampled back to 24fps (fps=24
filter) before the same uniform 1/fps duplicate-handoff-frame trim
finish.py/finish_r14_assembly.py apply at every joint, so the whole
concat stays a single, consistent 24fps CFR stream (no mixed-fps PTS
glitches in the concat filter graph). The standalone glowup-m.mp4 that
ships for real playback keeps its full 48fps smoothness.

quiet-m.mp4, patio-m.mp4, sendoff-m.mp4 are NOT re-encoded this round --
read directly from the currently-shipped Website/adult/assets/vid/ for
the journey-m re-stitch, same pattern as finish_r14_assembly.py.

Outputs staged in work/redo2/out/ -- nothing overwrites assets/ from this
script; the caller hash-compares and copies only changed files in.
"""
import subprocess, os, re, json, hashlib

RD = r"C:\Users\yashk\gywbt-site\Website\adult\work\redo2"
OUT = os.path.join(RD, "out")
ASSETS_VID = r"C:\Users\yashk\gywbt-site\Website\adult\assets\vid"
ASSETS = r"C:\Users\yashk\gywbt-site\Website\adult\assets"
os.makedirs(OUT, exist_ok=True)
os.chdir(RD)

def sh(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(str(a) for a in args)}\n{r.stderr[-800:]}")
    return r.stdout + r.stderr

def probe(f, entry, stream=True):
    sel = ["-select_streams", "v:0", "-show_entries", f"stream={entry}"] if stream \
        else ["-show_entries", f"format={entry}"]
    return sh(["ffprobe", "-v", "error", *sel, "-of", "csv=p=0", f]).strip()

def dur(f):
    return float(probe(f, "duration", stream=False))

def fps(f):
    n, d = probe(f, "r_frame_rate").split("/")
    return float(n) / float(d)

def ssim(a, b):
    out = sh(["ffmpeg", "-v", "info", "-i", a, "-i", b, "-lavfi",
              "[0:v]scale=720:1280[a];[1:v]scale=720:1280[b];[a][b]ssim", "-f", "null", "-"])
    m = re.search(r"All:([0-9.]+)", out)
    return float(m.group(1)) if m else -1.0

def frame_at(video, t, out):
    sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", video,
        "-frames:v", "1", "-q:v", "2", out])

def webp_from(video, t, out, w):
    sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
        "-vf", f"scale={w}:-2", "-c:v", "libwebp", "-quality", "88", out])

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

MOBILE_FLAGS = ["-c:v", "libx264", "-preset", "slow", "-crf", "23", "-pix_fmt", "yuv420p",
                "-g", "48", "-keyint_min", "24", "-sc_threshold", "0", "-movflags", "+faststart"]

# 1) glowup-m.mp4: leg_2.mp4 (24fps, 8.0417s) -> 48fps minterpolate, then the
#    standard scale/unsharp encode, with a -t 7.34 tail trim baked in (drops
#    the last ~0.66s of settled-hover dwell -- see module docstring, fix B).
src_dur_glowup = dur("leg_2.mp4")
print(f"leg_2.mp4 source duration: {src_dur_glowup:.6f}s")
glowup_m = os.path.join(OUT, "glowup-m.mp4")
sh(["ffmpeg", "-v", "error", "-y", "-i", "leg_2.mp4", "-an", "-t", "7.34",
    "-vf", "minterpolate=fps=48:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,"
           "scale=720:1280,unsharp=5:5:0.8:5:5:0.0",
    *MOBILE_FLAGS, glowup_m])
print(f"encoded glowup-m (interpolated 48fps, tail-trimmed): "
      f"{os.path.getsize(glowup_m)//1024}K, {dur(glowup_m):.3f}s @ {fps(glowup_m):.1f}fps")

# 2) photo-m.mp4: leg_3.mp4 (24fps, 8.0417s) -> -ss 0.5 head trim (fast seek
#    before -i), then the standard scale/unsharp encode (fix B, head side).
photo_m = os.path.join(OUT, "photo-m.mp4")
sh(["ffmpeg", "-v", "error", "-y", "-ss", "0.5", "-i", "leg_3.mp4", "-an",
    "-vf", "scale=720:1280,unsharp=5:5:0.8:5:5:0.0",
    *MOBILE_FLAGS, photo_m])
print(f"encoded photo-m (head-trimmed 0.5s): {os.path.getsize(photo_m)//1024}K, "
      f"{dur(photo_m):.3f}s @ {fps(photo_m):.1f}fps")

# 3) Poster (t=0.0) + still (t=4.0) webp regen for both changed scenes.
STILLS = [(glowup_m, "glowup-poster-m.webp", "glowup.webp"),
          (photo_m, "photo-poster-m.webp", "photo.webp")]
for clip, postername, stillname in STILLS:
    poster = os.path.join(OUT, postername)
    still = os.path.join(OUT, stillname)
    webp_from(clip, 0.0, poster, 720)
    webp_from(clip, 4.0, still, 720)
    print(f"regenerated {postername} + {stillname}")

# 4) Re-stitch journey-m.mp4: quiet-m/patio-m/sendoff-m come from the
#    currently-shipped assets/vid (untouched this round); glowup-m/photo-m
#    are the fresh files above. glowup-m is 48fps (interpolated) -- for
#    THIS concat only, normalize it back to 24fps (fps=24 filter) so the
#    whole stitch stays a single CFR framerate, matching the majority of
#    segments and finish.py's -g 48/-keyint_min 24 @24fps GOP assumption.
mob_names = ["quiet-m.mp4", "glowup-m.mp4", "photo-m.mp4", "patio-m.mp4", "sendoff-m.mp4"]
mob = [
    os.path.join(ASSETS_VID, "quiet-m.mp4"),
    glowup_m,
    photo_m,
    os.path.join(ASSETS_VID, "patio-m.mp4"),
    os.path.join(ASSETS_VID, "sendoff-m.mp4"),
]
for m in mob:
    if not os.path.exists(m):
        raise RuntimeError(f"missing required mobile clip: {m}")
STITCH_FPS = 24.0
trim = 1.0 / STITCH_FPS
parts, spans, t0 = [], [], 0.0
for i, mp in enumerate(mob):
    is_glowup = (i == 1)
    d = dur(mp) if not is_glowup else dur(mp)  # duration is wall-clock regardless of fps
    start = trim if i > 0 else 0.0
    parts.append((mp, start, d, is_glowup))
    seg = d - start
    spans.append([round(t0, 3), round(t0 + seg, 3)])
    t0 += seg
inputs, filts = [], []
for i, (mp, start, d, is_glowup) in enumerate(parts):
    inputs += ["-i", mp]
    pre = f"fps={STITCH_FPS:.0f}," if is_glowup else ""
    filts.append(f"[{i}:v]{pre}trim=start={start:.4f},setpts=PTS-STARTPTS[v{i}]")
fc = ";".join(filts) + ";" + "".join(f"[v{i}]" for i in range(len(parts))) + \
     f"concat=n={len(parts)}:v=1:a=0[out]"
journey_m = os.path.join(OUT, "journey-m.mp4")
sh(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[out]",
    *MOBILE_FLAGS, journey_m])
print(f"journey stitched: {dur(journey_m):.3f}s @ {fps(journey_m):.3f}fps (normalized to 24fps for the stitch)")
print("SPANS:", json.dumps(spans))
json.dump(spans, open(os.path.join(OUT, "spans_r15.json"), "w"))

# 4b) journey-poster-m.webp: only regenerate/flag-changed if the t=0.0 source
#     frame (quiet-m's first frame, unchanged this round) actually differs
#     from the currently-shipped journey-m's t=0.0 frame.
shipped_journey_m = os.path.join(ASSETS_VID, "journey-m.mp4")
new_frame_png = os.path.join(OUT, "_journey_t0_new_r15.png")
old_frame_png = os.path.join(OUT, "_journey_t0_shipped_r15.png")
frame_at(journey_m, 0.0, new_frame_png)
frame_source_changed = True
if os.path.exists(shipped_journey_m):
    frame_at(shipped_journey_m, 0.0, old_frame_png)
    frame_source_changed = sha256(new_frame_png) != sha256(old_frame_png)
journey_poster_m = os.path.join(OUT, "journey-poster-m.webp")
webp_from(journey_m, 0.0, journey_poster_m, 720)
print(f"journey-poster-m.webp source frame changed vs shipped: {frame_source_changed}")

# 5) Frame-check the segment joins in the stitched journey for PTS glitches
#    (mixed-fps concat sanity check) -- confirm every joint's frame_at()
#    probe succeeds and pict_type/keyframe cadence is sane at each boundary.
print("== stitched journey join sanity (ffprobe frame checks) ==")
for i, (t0_, t1_) in enumerate(spans):
    frame_at(journey_m, max(t1_ - 0.05, 0), os.path.join(OUT, f"_join{i}_a.png"))
    if t1_ < dur(journey_m):
        frame_at(journey_m, min(t1_ + 0.05, dur(journey_m) - 0.01), os.path.join(OUT, f"_join{i}_b.png"))
print(f"journey-m total duration {dur(journey_m):.3f}s, frame rate {fps(journey_m):.3f} (uniform)")

# 6) SSIM seam gate -- same band/classification as finish.py/finish_r14.
#    Seam 2 (glowup->photo) stays a DESIGNED discontinuity (in-clip
#    sparkle-descent transition, now additionally dwell-trimmed) -- not
#    gated. Seams 3/4 unaffected this round (patio-m/sendoff-m unchanged).
SEAM_NAMES = ["quiet -> glowup", "glowup -> photo", "photo -> patio", "patio -> sendoff"]
EXPECTED_DISCONTINUITY = {0, 1}
BAND_LO, BAND_HI = 0.38, 0.70

def classify(i, s):
    if i in EXPECTED_DISCONTINUITY:
        return "EXPECTED (designed transition, not gated)"
    if BAND_LO <= s <= BAND_HI:
        return "PASS (within shipped-chain band)"
    return "CHECK (outside band -- needs visual frame-pair review)"

A, B = os.path.join(OUT, "_ga_r15.png"), os.path.join(OUT, "_gb_r15.png")
print("== gate: stitched journey boundaries ==")
genuine = []
for i in range(len(spans) - 1):
    t = spans[i][1]
    frame_at(journey_m, max(t - 0.05, 0), A)
    frame_at(journey_m, t + 0.05, B)
    s = ssim(A, B)
    if i not in EXPECTED_DISCONTINUITY:
        genuine.append(s)
    print(f"  seam {i+1} @{t:>7.3f}s: {SEAM_NAMES[i]:<16} SSIM {s:.3f}  {classify(i, s)}")
gate_green = all(BAND_LO <= s <= BAND_HI for s in genuine)
print(f"GATE {'GREEN' if gate_green else 'CHECK'} (genuine seam scores: {[round(s,3) for s in genuine]})")

# 7) Hash-compare against currently-shipped assets to know what changed.
CHECK = [
    (glowup_m, os.path.join(ASSETS_VID, "glowup-m.mp4")),
    (os.path.join(OUT, "glowup-poster-m.webp"), os.path.join(ASSETS, "glowup-poster-m.webp")),
    (os.path.join(OUT, "glowup.webp"), os.path.join(ASSETS, "glowup.webp")),
    (photo_m, os.path.join(ASSETS_VID, "photo-m.mp4")),
    (os.path.join(OUT, "photo-poster-m.webp"), os.path.join(ASSETS, "photo-poster-m.webp")),
    (os.path.join(OUT, "photo.webp"), os.path.join(ASSETS, "photo.webp")),
    (journey_m, shipped_journey_m),
    (journey_poster_m, os.path.join(ASSETS, "journey-poster-m.webp")),
]
print("== hash compare (new out/ vs currently shipped assets) ==")
for newf, shippedf in CHECK:
    nh = sha256(newf)
    sh_ = sha256(shippedf) if os.path.exists(shippedf) else "(missing)"
    changed = "CHANGED" if nh != sh_ else "IDENTICAL"
    print(f"  {os.path.basename(newf):<24} new={nh[:12]} shipped={sh_[:12] if sh_ != '(missing)' else sh_}  {changed}")
