"""Task r14 -- full mobile assembly for the confetti chain (clips 2, 3, 4).

Scoped subset of finish.py's recipe, extended from finish_confetti_mobile.py
(which only re-did photo-m) to also re-encode glowup-m (leg_2) and patio-m
(leg_4), since this round accepts fresh takes for all three middle scenes:
  - leg_2.mp4 -> glowup-m.mp4  (confetti-storm arrival)
  - leg_3.mp4 -> photo-m.mp4   (cut-free confetti jump-off, freshly accepted)
  - leg_4.mp4 -> patio-m.mp4   (scale-correct cake take, calm opening)

quiet-m.mp4 and sendoff-m.mp4 are NOT re-encoded (untouched this round) --
they are read directly from the currently-shipped Website/adult/assets/vid/
for the journey-m re-stitch, per task instruction.

Mirrors finish.py's exact ffmpeg flags (see finish.py in this same directory
for the source of truth):
  - mobile encode: scale=720:1280, unsharp=5:5:0.8:5:5:0.0, libx264 preset
    slow, crf 23, yuv420p, -g 48 -keyint_min 24 -sc_threshold 0, faststart, -an
  - stills: ffmpeg -ss T -frames:v 1 -vf scale=720:-2 -c:v libwebp -quality 88
    (poster-m at t=0.0, scene still .webp at t=4.0)
  - journey stitch: trim the duplicated handoff frame (1/fps) at each joint,
    concat filter, same mobile encode flags
  - SSIM seam gate: same band (0.38-0.70) and EXPECTED_DISCONTINUITY set as
    finish.py (seam1 quiet->glowup, seam2 glowup->photo are designed
    discontinuities; seam3 photo->patio and seam4 patio->sendoff are the real
    chained-continuity gate)

journey-poster-m.webp is only regenerated/flagged-changed if its source frame
(t=0.0 of journey-m, i.e. quiet-m's first frame) actually differs from the
currently-shipped journey-m's t=0.0 frame -- hash-compared as raw PNG bytes,
not just re-encoded and assumed different.

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

# 1) Re-encode glowup-m/photo-m/patio-m from the accepted leg_2/leg_3/leg_4.mp4
#    (always overwrite -- this run's whole point is fresh confetti-chain takes).
ENCODE = [("leg_2.mp4", "glowup-m.mp4"), ("leg_3.mp4", "photo-m.mp4"), ("leg_4.mp4", "patio-m.mp4")]
built = {}
for src, outname in ENCODE:
    outp = os.path.join(OUT, outname)
    sh(["ffmpeg", "-v", "error", "-y", "-i", src, "-an",
        "-vf", "scale=720:1280,unsharp=5:5:0.8:5:5:0.0",
        "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-pix_fmt", "yuv420p",
        "-g", "48", "-keyint_min", "24", "-sc_threshold", "0",
        "-movflags", "+faststart", outp])
    built[outname] = outp
    print(f"encoded {outname}: {os.path.getsize(outp)//1024}K")

# 2) Regenerate poster-m (t=0.0) + still (t=4.0), 720w webp q88, for the 3
#    re-encoded scenes.
STILLS = [("glowup-m.mp4", "glowup-poster-m.webp", "glowup.webp"),
          ("photo-m.mp4", "photo-poster-m.webp", "photo.webp"),
          ("patio-m.mp4", "patio-poster-m.webp", "patio.webp")]
for clipname, postername, stillname in STILLS:
    clip = built[clipname]
    poster = os.path.join(OUT, postername)
    still = os.path.join(OUT, stillname)
    webp_from(clip, 0.0, poster, 720)
    webp_from(clip, 4.0, still, 720)
    print(f"regenerated {postername} + {stillname}")

# 3) Re-stitch journey-m.mp4: quiet-m/sendoff-m come from the currently-
#    shipped assets/vid (untouched this round), glowup-m/photo-m/patio-m are
#    the freshly built out/ files above.
mob_names = ["quiet-m.mp4", "glowup-m.mp4", "photo-m.mp4", "patio-m.mp4", "sendoff-m.mp4"]
mob = [
    os.path.join(ASSETS_VID, "quiet-m.mp4"),
    built["glowup-m.mp4"],
    built["photo-m.mp4"],
    built["patio-m.mp4"],
    os.path.join(ASSETS_VID, "sendoff-m.mp4"),
]
for m in mob:
    if not os.path.exists(m):
        raise RuntimeError(f"missing required mobile clip: {m}")
f = fps(mob[0])
trim = 1.0 / f
parts, spans, t0 = [], [], 0.0
for i, mp in enumerate(mob):
    d = dur(mp)
    start = trim if i > 0 else 0.0
    parts.append((mp, start, d))
    seg = d - start
    spans.append([round(t0, 3), round(t0 + seg, 3)])
    t0 += seg
inputs, filts = [], []
for i, (mp, start, d) in enumerate(parts):
    inputs += ["-i", mp]
    filts.append(f"[{i}:v]trim=start={start:.4f},setpts=PTS-STARTPTS[v{i}]")
fc = ";".join(filts) + ";" + "".join(f"[v{i}]" for i in range(len(parts))) + \
     f"concat=n={len(parts)}:v=1:a=0[out]"
journey_m = os.path.join(OUT, "journey-m.mp4")
sh(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[out]",
    "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-pix_fmt", "yuv420p",
    "-g", "48", "-keyint_min", "24", "-sc_threshold", "0", "-movflags", "+faststart", journey_m])
print(f"journey stitched: {dur(journey_m):.3f}s @ {f:.3f}fps")
print("SPANS:", json.dumps(spans))
json.dump(spans, open(os.path.join(OUT, "spans_r14.json"), "w"))

# 3b) journey-poster-m.webp: only regenerate/flag-changed if the t=0.0 source
#     frame actually differs from the currently-shipped journey-m's t=0.0
#     frame (quiet-m is unchanged and is first in the concat, so this is
#     expected to be identical -- verified, not assumed).
shipped_journey_m = os.path.join(ASSETS_VID, "journey-m.mp4")
new_frame_png = os.path.join(OUT, "_journey_t0_new.png")
old_frame_png = os.path.join(OUT, "_journey_t0_shipped.png")
frame_at(journey_m, 0.0, new_frame_png)
frame_source_changed = True
if os.path.exists(shipped_journey_m):
    frame_at(shipped_journey_m, 0.0, old_frame_png)
    frame_source_changed = sha256(new_frame_png) != sha256(old_frame_png)
journey_poster_m = os.path.join(OUT, "journey-poster-m.webp")
webp_from(journey_m, 0.0, journey_poster_m, 720)
print(f"journey-poster-m.webp source frame changed vs shipped: {frame_source_changed}")

# 4) SSIM seam gate -- same band/classification as finish.py. All four seams
#    checked since glowup/photo/patio all changed this round (seam1
#    quiet->glowup and seam2 glowup->photo remain EXPECTED designed
#    discontinuities, not gated; seam3 photo->patio and seam4 patio->sendoff
#    are the real chained-continuity gate).
SEAM_NAMES = ["quiet -> glowup", "glowup -> photo", "photo -> patio", "patio -> sendoff"]
EXPECTED_DISCONTINUITY = {0, 1}
BAND_LO, BAND_HI = 0.38, 0.70

def classify(i, s):
    if i in EXPECTED_DISCONTINUITY:
        return "EXPECTED (designed transition, not gated)"
    if BAND_LO <= s <= BAND_HI:
        return "PASS (within shipped-chain band)"
    return "CHECK (outside band -- needs visual frame-pair review)"

A, B = os.path.join(OUT, "_ga_r14.png"), os.path.join(OUT, "_gb_r14.png")
print("== gate: encoded leg-to-leg handoffs (mobile tier) ==")
genuine = []
for i in range(len(mob) - 1):
    sh(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.06", "-i", mob[i], "-frames:v", "1", "-q:v", "2", A])
    frame_at(mob[i + 1], trim, B)
    s = ssim(A, B)
    if i not in EXPECTED_DISCONTINUITY:
        genuine.append(s)
    print(f"  seam {i+1}: {SEAM_NAMES[i]:<16} SSIM {s:.3f}  {classify(i, s)}")
print("== gate: stitched journey boundaries ==")
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

# 5) Hash-compare against currently-shipped assets to know what changed.
CHECK = [
    (built["glowup-m.mp4"], os.path.join(ASSETS_VID, "glowup-m.mp4")),
    (os.path.join(OUT, "glowup-poster-m.webp"), os.path.join(ASSETS, "glowup-poster-m.webp")),
    (os.path.join(OUT, "glowup.webp"), os.path.join(ASSETS, "glowup.webp")),
    (built["photo-m.mp4"], os.path.join(ASSETS_VID, "photo-m.mp4")),
    (os.path.join(OUT, "photo-poster-m.webp"), os.path.join(ASSETS, "photo-poster-m.webp")),
    (os.path.join(OUT, "photo.webp"), os.path.join(ASSETS, "photo.webp")),
    (built["patio-m.mp4"], os.path.join(ASSETS_VID, "patio-m.mp4")),
    (os.path.join(OUT, "patio-poster-m.webp"), os.path.join(ASSETS, "patio-poster-m.webp")),
    (os.path.join(OUT, "patio.webp"), os.path.join(ASSETS, "patio.webp")),
    (journey_m, shipped_journey_m),
    (journey_poster_m, os.path.join(ASSETS, "journey-poster-m.webp")),
]
print("== hash compare (new out/ vs currently shipped assets) ==")
for newf, shippedf in CHECK:
    nh = sha256(newf)
    sh_ = sha256(shippedf) if os.path.exists(shippedf) else "(missing)"
    changed = "CHANGED" if nh != sh_ else "IDENTICAL"
    print(f"  {os.path.basename(newf):<24} new={nh[:12]} shipped={sh_[:12] if sh_ != '(missing)' else sh_}  {changed}")
