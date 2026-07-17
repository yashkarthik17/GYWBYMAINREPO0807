import subprocess, os, re, sys

WORK = r"C:\Users\yashk\OneDrive\Desktop\Glad You Were Born Today (Repo)\Website\work"
ASSETS = r"C:\Users\yashk\OneDrive\Desktop\Glad You Were Born Today (Repo)\Website\assets"
os.chdir(WORK)
NAMES = ["beige", "crashpad", "crash", "glowup", "finale"]
CONN_BEFORE = {"crashpad": "conn_1", "crash": "conn_2", "glowup": "conn_3", "finale": "conn_4"}
TAIL = 0.15  # connectors started from the frame extracted at -0.15s before each dive's end

def sh(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(args)}\n{r.stderr[-500:]}")
    return r.stdout + r.stderr

def dur(f):
    out = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f])
    return float(out.strip())

def frame_at(video, t, out):
    sh(["ffmpeg", "-v", "error", "-y", "-i", video, "-ss", f"{t:.3f}", "-frames:v", "1", "-q:v", "2", out])

def last_frame(video, out, off=0.05):
    if os.path.exists(out):
        os.remove(out)
    for o in (off, 0.1, 0.2, 0.35, 0.5):
        sh(["ffmpeg", "-v", "error", "-y", "-sseof", f"-{o}", "-i", video, "-frames:v", "1", "-q:v", "2", out])
        if os.path.exists(out) and os.path.getsize(out) > 0:
            return
    raise RuntimeError(f"could not extract last frame of {video}")

def ssim(a, b):
    out = sh(["ffmpeg", "-v", "info", "-i", a, "-i", b, "-lavfi", "ssim", "-f", "null", "-"])
    m = re.search(r"All:([0-9.]+)", out)
    return float(m.group(1)) if m else 0.0

# 1) Head-trim sweep: where in each dive does the incoming connector actually land?
head = {n: 0.0 for n in NAMES}
for n, conn in CONN_BEFORE.items():
    last_frame(f"{conn}.mp4", "_conn_end.png")
    best_t, best_s, s0 = 0.0, -1.0, None
    t = 0.0
    while t <= 2.01:
        frame_at(f"dive_{n}.mp4", t, "_probe.png")
        s = ssim("_conn_end.png", "_probe.png")
        if s0 is None: s0 = s
        if s > best_s: best_t, best_s = t, s
        t += 0.1
    if best_t > 0 and best_s - s0 > 0.02:
        head[n] = best_t
    print(f"{conn}->{n}: ssim@0={s0:.3f} best@{best_t:.1f}s={best_s:.3f} -> head-trim {head[n]:.1f}s", flush=True)

# 2) Re-encode every dive with head/tail trims (master + mobile), from the raw renders.
for n in NAMES:
    d = dur(f"dive_{n}.mp4")
    out_d = d - head[n] - TAIL
    src, h = f"dive_{n}.mp4", head[n]
    sh(["ffmpeg", "-v", "error", "-y", "-i", src, "-ss", f"{h:.3f}", "-t", f"{out_d:.3f}", "-an",
        "-vf", "unsharp=5:5:0.8:5:5:0.0", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
        "-pix_fmt", "yuv420p", "-g", "8", "-keyint_min", "8", "-sc_threshold", "0",
        "-movflags", "+faststart", os.path.join(ASSETS, "vid", f"{n}.mp4")])
    sh(["ffmpeg", "-v", "error", "-y", "-i", src, "-ss", f"{h:.3f}", "-t", f"{out_d:.3f}", "-an",
        "-vf", "scale=-2:720,unsharp=5:5:0.6:5:5:0.0", "-c:v", "libx264", "-preset", "slow", "-crf", "23",
        "-pix_fmt", "yuv420p", "-g", "4", "-keyint_min", "4", "-sc_threshold", "0",
        "-movflags", "+faststart", os.path.join(ASSETS, "vid", f"{n}-m.mp4")])
    print(f"re-encoded {n}: head={h:.1f} tail={TAIL} dur={out_d:.2f}", flush=True)

# 3) Re-extract posters from the new encodes.
for n in NAMES:
    for suffix, poster in (("", f"{n}-poster.webp"), ("-m", f"{n}-poster-m.webp")):
        clip = os.path.join(ASSETS, "vid", f"{n}{suffix}.mp4")
        png = f"_poster_tmp.png"
        sh(["ffmpeg", "-v", "error", "-y", "-ss", "0", "-i", clip, "-frames:v", "1", "-q:v", "2", png])
        sh(["ffmpeg", "-v", "error", "-y", "-i", png, "-c:v", "libwebp", "-quality", "84",
            os.path.join(ASSETS, poster)])
print("posters re-extracted", flush=True)

# 4) Gate: SSIM across every seam of the encoded chain.
V = os.path.join(ASSETS, "vid")
chain = ["beige.mp4", "conn1.mp4", "crashpad.mp4", "conn2.mp4", "crash.mp4",
         "conn3.mp4", "glowup.mp4", "conn4.mp4", "finale.mp4"]
print("=== SSIM SEAM GATE (post-fix) ===", flush=True)
worst = 1.0
for a, b in zip(chain, chain[1:]):
    last_frame(os.path.join(V, a), "_ga.png")
    frame_at(os.path.join(V, b), 0.0, "_gb.png")
    s = ssim("_ga.png", "_gb.png")
    worst = min(worst, s)
    tag = "PASS" if s >= 0.90 else ("WARN" if s >= 0.75 else "FAIL")
    print(f"{tag}  {a}>{b}  ssim={s:.4f}", flush=True)
print(f"=== GATE DONE (worst={worst:.4f}) ===", flush=True)
