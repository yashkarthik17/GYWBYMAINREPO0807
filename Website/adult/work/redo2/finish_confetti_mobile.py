"""Mobile-only assembly for the confetti-maxed leg_3 (photo scene) regen.

Scoped subset of finish.py's recipe: re-encodes ONLY photo-m.mp4 from the
accepted leg_3.mp4, regenerates its mobile poster/still webps, and re-stitches
journey-m.mp4 using the EXISTING quiet-m/glowup-m/patio-m/sendoff-m clips
(already in assets/vid, unchanged) plus the new photo-m. Desktop/landscape
tier is NOT touched by this script -- that's a later round pending approval.

Mirrors finish.py's exact ffmpeg flags for byte-for-byte-equivalent encoding
choices (see finish.py in this same directory for the source of truth):
  - mobile encode: scale=720:1280, unsharp=5:5:0.8:5:5:0.0, libx264 preset
    slow, crf 23, yuv420p, -g 48 -keyint_min 24 -sc_threshold 0, faststart
  - stills: ffmpeg -ss T -frames:v 1 -vf scale=720:-2 -c:v libwebp -quality 88
  - journey stitch: trim the duplicated handoff frame (1/fps) at each joint,
    concat filter, same mobile encode flags
  - SSIM seam gate: same band (0.38-0.70) and EXPECTED_DISCONTINUITY set as
    finish.py (seam1 quiet->glowup, seam2 glowup->photo are designed
    discontinuities; seam3 photo->patio and seam4 patio->sendoff are the real
    chained-continuity gate)

Unlike finish.py this script does NOT skip-if-exists -- it always
re-encodes/re-stitches the mobile-tier files it owns, since the whole point
of this run is to replace stale out/ artifacts from the prior (pre-confetti)
photo scene.
"""
import subprocess, os, re, json, hashlib

RD = r"C:\Users\yashk\gywbt-site\Website\adult\work\redo2"
OUT = os.path.join(RD, "out")
ASSETS_VID = r"C:\Users\yashk\gywbt-site\Website\adult\assets\vid"
ASSETS = r"C:\Users\yashk\gywbt-site\Website\adult\assets"
os.makedirs(OUT, exist_ok=True)
os.chdir(RD)

LEGS = [("leg_1", "quiet"), ("leg_2", "glowup"), ("leg_3", "photo"),
        ("leg_4", "patio"), ("leg_5", "sendoff")]

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

# 1) Re-encode photo-m.mp4 from the accepted leg_3.mp4 (always overwrite --
#    this run's whole point is to replace the stale pre-confetti out/ file).
src = "leg_3.mp4"
photo_m = os.path.join(OUT, "photo-m.mp4")
sh(["ffmpeg", "-v", "error", "-y", "-i", src, "-an",
    "-vf", "scale=720:1280,unsharp=5:5:0.8:5:5:0.0",
    "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-pix_fmt", "yuv420p",
    "-g", "48", "-keyint_min", "24", "-sc_threshold", "0",
    "-movflags", "+faststart", photo_m])
print(f"encoded photo-m: {os.path.getsize(photo_m)//1024}K")

# 2) Regenerate photo mobile poster (t=0.0) + still (t=4.0), 720w webp q88.
photo_poster_m = os.path.join(OUT, "photo-poster-m.webp")
photo_still = os.path.join(OUT, "photo.webp")
webp_from(photo_m, 0.0, photo_poster_m, 720)
webp_from(photo_m, 4.0, photo_still, 720)
print("regenerated photo-poster-m.webp + photo.webp")

# 3) Re-stitch journey-m.mp4: quiet-m/glowup-m/patio-m/sendoff-m unchanged
#    from OUT (already there from the prior finish.py run), photo-m is new.
mob_names = ["quiet-m.mp4", "glowup-m.mp4", "photo-m.mp4", "patio-m.mp4", "sendoff-m.mp4"]
mob = [os.path.join(OUT, n) for n in mob_names]
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
journey_poster_m = os.path.join(OUT, "journey-poster-m.webp")
webp_from(journey_m, 0.0, journey_poster_m, 720)
print(f"journey stitched: {dur(journey_m):.3f}s @ {f:.3f}fps")
print("SPANS:", json.dumps(spans))
json.dump(spans, open(os.path.join(OUT, "spans_confetti.json"), "w"))

# 4) SSIM seam gate -- same band/classification as finish.py, but we only
#    care about the seams touching photo: seam2 (glowup->photo, EXPECTED
#    designed discontinuity, not gated) and seam3 (photo->patio, REAL
#    chained-continuity gate, band 0.38-0.70).
SEAM_NAMES = ["quiet -> glowup", "glowup -> photo", "photo -> patio", "patio -> sendoff"]
EXPECTED_DISCONTINUITY = {0, 1}
BAND_LO, BAND_HI = 0.38, 0.70

def classify(i, s):
    if i in EXPECTED_DISCONTINUITY:
        return "EXPECTED (designed transition, not gated)"
    if BAND_LO <= s <= BAND_HI:
        return "PASS (within shipped-chain band)"
    return "CHECK (outside band -- needs visual frame-pair review)"

A, B = os.path.join(OUT, "_ga_confetti.png"), os.path.join(OUT, "_gb_confetti.png")
print("== gate: encoded leg-to-leg handoffs (mobile tier) ==")
for i in range(len(mob) - 1):
    sh(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.06", "-i", mob[i], "-frames:v", "1", "-q:v", "2", A])
    frame_at(mob[i + 1], trim, B)
    s = ssim(A, B)
    print(f"  seam {i+1}: {SEAM_NAMES[i]:<16} SSIM {s:.3f}  {classify(i, s)}")
print("== gate: stitched journey boundaries ==")
for i in range(len(spans) - 1):
    t = spans[i][1]
    frame_at(journey_m, max(t - 0.05, 0), A)
    frame_at(journey_m, t + 0.05, B)
    s = ssim(A, B)
    print(f"  seam {i+1} @{t:>7.3f}s: {SEAM_NAMES[i]:<16} SSIM {s:.3f}  {classify(i, s)}")

# 5) Hash-compare against currently-shipped assets to know what changed.
CHECK = [
    (photo_m, os.path.join(ASSETS_VID, "photo-m.mp4")),
    (photo_poster_m, os.path.join(ASSETS, "photo-poster-m.webp")),
    (photo_still, os.path.join(ASSETS, "photo.webp")),
    (journey_m, os.path.join(ASSETS_VID, "journey-m.mp4")),
    (journey_poster_m, os.path.join(ASSETS, "journey-poster-m.webp")),
]
print("== hash compare (new out/ vs currently shipped assets) ==")
for newf, shippedf in CHECK:
    nh = sha256(newf)
    sh_ = sha256(shippedf) if os.path.exists(shippedf) else "(missing)"
    changed = "CHANGED" if nh != sh_ else "IDENTICAL"
    print(f"  {os.path.basename(newf):<24} new={nh[:12]} shipped={sh_[:12] if sh_ != '(missing)' else sh_}  {changed}")
