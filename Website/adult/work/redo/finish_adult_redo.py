"""Adult-chain redo post-processing.

Encodes the 5 raw legs into desktop + mobile scrub tiers, extracts posters and
stills FROM THE ENCODED CLIPS (seam-zero doctrine), stitches the mobile journey
with the duplicated handoff frame trimmed at each joint, computes the scrub
spans from the real encoded durations, and runs the SSIM seam gate.
Outputs staged in work/redo/out/ — nothing overwrites assets/ until the gate
is green and the page is wired by hand.
"""
import subprocess, os, re, json

RD = r"C:\Users\yashk\OneDrive\Desktop\Glad You Were Born Today (Repo)\Website\adult\work\redo"
OUT = os.path.join(RD, "out")
os.makedirs(OUT, exist_ok=True)
os.chdir(RD)

LEGS = [("leg_1", "quiet"), ("leg_2", "glowup"), ("leg_3", "photo"),
        ("leg_4", "patio"), ("leg_5", "sendoff")]

def sh(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(str(a) for a in args)}\n{r.stderr[-500:]}")
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

def last_frame(video, out):
    sh(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.06", "-i", video,
        "-frames:v", "1", "-q:v", "2", out])

def webp_from(video, t, out, w):
    sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
        "-vf", f"scale={w}:-2", "-c:v", "libwebp", "-quality", "88", out])

# 1) Encode both tiers
for leg, name in LEGS:
    src = f"{leg}.mp4"
    d = os.path.join(OUT, f"{name}.mp4")
    m = os.path.join(OUT, f"{name}-m.mp4")
    if not os.path.exists(d):
        sh(["ffmpeg", "-v", "error", "-y", "-i", src, "-an",
            "-vf", "unsharp=5:5:0.8:5:5:0.0",
            "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
            "-g", "8", "-keyint_min", "8", "-sc_threshold", "0",
            "-movflags", "+faststart", d])
    if not os.path.exists(m):
        sh(["ffmpeg", "-v", "error", "-y", "-i", src, "-an",
            "-vf", "scale=720:1280,unsharp=5:5:0.8:5:5:0.0",
            "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-pix_fmt", "yuv420p",
            "-g", "4", "-keyint_min", "4", "-sc_threshold", "0",
            "-movflags", "+faststart", m])
    print(f"encoded {name}: desktop {os.path.getsize(d)//1024}K, mobile {os.path.getsize(m)//1024}K")

# 2) Posters (first frame of each ENCODED tier) + stills (mid-frame art)
for _, name in LEGS:
    webp_from(os.path.join(OUT, f"{name}.mp4"), 0.0, os.path.join(OUT, f"{name}-poster.webp"), 1080)
    webp_from(os.path.join(OUT, f"{name}-m.mp4"), 0.0, os.path.join(OUT, f"{name}-poster-m.webp"), 720)
    webp_from(os.path.join(OUT, f"{name}.mp4"), 4.0, os.path.join(OUT, f"{name}.webp"), 1080)
print("posters + stills extracted")

# 3) Stitch mobile journey, trimming the duplicated handoff frame at each joint
mob = [os.path.join(OUT, f"{n}-m.mp4") for _, n in LEGS]
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
j = os.path.join(OUT, "journey-m.mp4")
sh(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[out]",
    "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-pix_fmt", "yuv420p",
    "-g", "4", "-keyint_min", "4", "-sc_threshold", "0", "-movflags", "+faststart", j])
webp_from(j, 0.0, os.path.join(OUT, "journey-poster-m.webp"), 720)
print(f"journey stitched: {dur(j):.3f}s @ {f:.3f}fps")
print("SPANS:", json.dumps(spans))

# 4) SSIM seam gate
A, B = os.path.join(OUT, "_ga.png"), os.path.join(OUT, "_gb.png")
print("== gate: encoded leg-to-leg handoffs ==")
worst = 1.0
for i in range(len(mob) - 1):
    last_frame(mob[i], A)
    frame_at(mob[i + 1], trim, B)   # first frame AFTER the trimmed duplicate
    s = ssim(A, B)
    worst = min(worst, s)
    print(f"  {LEGS[i][1]:>8} -> {LEGS[i+1][1]:<8} SSIM {s:.3f}")
print("== gate: stitched journey boundaries ==")
for i in range(len(spans) - 1):
    t = spans[i][1]
    frame_at(j, max(t - 0.05, 0), A)
    frame_at(j, t + 0.05, B)
    s = ssim(A, B)
    worst = min(worst, s)
    print(f"  seam @{t:>7.3f}s SSIM {s:.3f}")
print(f"GATE {'GREEN' if worst >= 0.90 else 'CHECK'} (worst {worst:.3f})")
