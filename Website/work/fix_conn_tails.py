import subprocess, os, re

WORK = r"C:\Users\yashk\OneDrive\Desktop\Glad You Were Born Today (Repo)\Website\work"
ASSETS = r"C:\Users\yashk\OneDrive\Desktop\Glad You Were Born Today (Repo)\Website\assets"
V = os.path.join(ASSETS, "vid")
os.chdir(WORK)
PAIRS = [("conn_1", "crashpad"), ("conn_2", "crash"), ("conn_3", "glowup"), ("conn_4", "finale")]

def sh(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(args)}\n{r.stderr[-500:]}")
    return r.stdout + r.stderr

def dur(f):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).strip())

def frame_at(video, t, out):
    sh(["ffmpeg", "-v", "error", "-y", "-i", video, "-ss", f"{t:.3f}", "-frames:v", "1", "-q:v", "2", out])

def ssim(a, b):
    out = sh(["ffmpeg", "-v", "info", "-i", a, "-i", b, "-lavfi", "ssim,scale=8:8", "-f", "null", "-"]) if False else \
          sh(["ffmpeg", "-v", "info", "-i", a, "-i", b, "-lavfi", "ssim", "-f", "null", "-"])
    m = re.search(r"All:([0-9.]+)", out)
    return float(m.group(1)) if m else 0.0

def enc(src, out, end_t, mobile=False):
    vf = "scale=-2:720,unsharp=5:5:0.6:5:5:0.0" if mobile else "unsharp=5:5:0.8:5:5:0.0"
    crf = "23" if mobile else "20"
    g = "4" if mobile else "8"
    sh(["ffmpeg", "-v", "error", "-y", "-i", src, "-t", f"{end_t:.3f}", "-an", "-vf", vf,
        "-c:v", "libx264", "-preset", "slow", "-crf", crf, "-pix_fmt", "yuv420p",
        "-g", g, "-keyint_min", g, "-sc_threshold", "0", "-movflags", "+faststart", out])

for conn, nxt in PAIRS:
    src = f"{conn}.mp4"
    d = dur(src)
    frame_at(os.path.join(V, f"{nxt}.mp4"), 0.0, "_next0.png")
    # sweep the connector's last 2.5s (never trim below half its length)
    t0 = max(d / 2, d - 2.5)
    best_t, best_s, end_s = None, -1.0, None
    t = t0
    while t <= d - 0.04:
        frame_at(src, t, "_probe.png")
        s = ssim("_next0.png", "_probe.png")
        if s > best_s: best_t, best_s = t, s
        end_s = s  # last measured = closest to true end
        t += 0.1
    trim_end = d - 0.05
    if best_s - end_s > 0.02 and best_t < d - 0.15:
        trim_end = best_t + 0.02
        print(f"{conn}: end ssim={end_s:.3f}, best@{best_t:.1f}s={best_s:.3f} -> TRIM to {trim_end:.2f}s (of {d:.2f}s)", flush=True)
    else:
        print(f"{conn}: end ssim={end_s:.3f}, best@{best_t:.1f}s={best_s:.3f} -> keep full length", flush=True)
    i = conn.split("_")[1]
    enc(src, os.path.join(V, f"conn{i}.mp4"), trim_end, mobile=False)
    enc(src, os.path.join(V, f"conn{i}-m.mp4"), trim_end, mobile=True)

# Full-chain gate
def last_frame(video, out):
    if os.path.exists(out): os.remove(out)
    for o in (0.05, 0.1, 0.2, 0.35, 0.5):
        sh(["ffmpeg", "-v", "error", "-y", "-sseof", f"-{o}", "-i", video, "-frames:v", "1", "-q:v", "2", out])
        if os.path.exists(out) and os.path.getsize(out) > 0: return
    raise RuntimeError(f"no last frame: {video}")

chain = ["beige.mp4", "conn1.mp4", "crashpad.mp4", "conn2.mp4", "crash.mp4",
         "conn3.mp4", "glowup.mp4", "conn4.mp4", "finale.mp4"]
print("=== SSIM SEAM GATE (final) ===", flush=True)
worst = 1.0
for a, b in zip(chain, chain[1:]):
    last_frame(os.path.join(V, a), "_ga.png")
    frame_at(os.path.join(V, b), 0.0, "_gb.png")
    s = ssim("_ga.png", "_gb.png")
    worst = min(worst, s)
    tag = "PASS" if s >= 0.90 else ("WARN" if s >= 0.75 else "FAIL")
    print(f"{tag}  {a}>{b}  ssim={s:.4f}", flush=True)
print(f"=== GATE DONE (worst={worst:.4f}) ===", flush=True)
