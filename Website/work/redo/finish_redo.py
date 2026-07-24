"""Redo-chain post-processing: trim-align seams, encode the mobile tier into assets/vid,
extract posters, regenerate phone stills (-p.webp), and run the SSIM seam gate.
Adapted from work/finish_portrait.py but sourcing from work/redo/."""
import subprocess, os, re

WORK = r"C:\Users\yashk\OneDrive\Desktop\Glad You Were Born Today (Repo)\Website\work\redo"
ASSETS = r"C:\Users\yashk\OneDrive\Desktop\Glad You Were Born Today (Repo)\Website\assets"
V = os.path.join(ASSETS, "vid")
os.chdir(WORK)
NAMES = ["beige", "crashpad", "crash", "glowup", "finale"]
PAIRS = [("pconn_1", "crashpad"), ("pconn_2", "crash"), ("pconn_3", "glowup"), ("pconn_4", "finale")]
TAIL = 0.15

def sh(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(args)}\n{r.stderr[-400:]}")
    return r.stdout + r.stderr

def dur(f):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).strip())

def frame_at(video, t, out):
    sh(["ffmpeg", "-v", "error", "-y", "-i", video, "-ss", f"{t:.3f}", "-frames:v", "1", "-q:v", "2", out])

def last_frame(video, out):
    if os.path.exists(out): os.remove(out)
    for o in (0.05, 0.1, 0.2, 0.35, 0.5):
        sh(["ffmpeg", "-v", "error", "-y", "-sseof", f"-{o}", "-i", video, "-frames:v", "1", "-q:v", "2", out])
        if os.path.exists(out) and os.path.getsize(out) > 0: return
    raise RuntimeError(f"no last frame: {video}")

def ssim(a, b):
    out = sh(["ffmpeg", "-v", "info", "-i", a, "-i", b, "-lavfi",
              "[0:v]scale=540:960[a];[1:v]scale=540:960[b];[a][b]ssim", "-f", "null", "-"])
    m = re.search(r"All:([0-9.]+)", out)
    return float(m.group(1)) if m else 0.0

def enc_mobile(src, out, start=0.0, end_t=None):
    args = ["ffmpeg", "-v", "error", "-y", "-i", src, "-ss", f"{start:.3f}"]
    if end_t is not None:
        args += ["-t", f"{max(end_t - start, 0.5):.3f}"]
    args += ["-an", "-vf", "scale=720:-2,unsharp=5:5:0.6:5:5:0.0",
             "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-pix_fmt", "yuv420p",
             "-g", "4", "-keyint_min", "4", "-sc_threshold", "0", "-movflags", "+faststart", out]
    sh(args)

# 1) dives: tail-trim to the handoff frame; encode as <name>-m.mp4
for n in NAMES:
    d = dur(f"pdive_{n}.mp4")
    enc_mobile(f"pdive_{n}.mp4", os.path.join(V, f"{n}-m.mp4"), 0.0, d - TAIL)
    print(f"dive {n} -> {n}-m.mp4 (dur {d - TAIL:.2f})", flush=True)

# 2) connectors: sweep tail vs next dive's first frame, trim where it helps
for conn, nxt in PAIRS:
    src = f"{conn}.mp4"
    d = dur(src)
    frame_at(os.path.join(V, f"{nxt}-m.mp4"), 0.0, "_pnext0.png")
    t0 = max(d / 2, d - 2.5)
    best_t, best_s, end_s = None, -1.0, None
    t = t0
    while t <= d - 0.04:
        frame_at(src, t, "_pprobe.png")
        s = ssim("_pnext0.png", "_pprobe.png")
        if s > best_s: best_t, best_s = t, s
        end_s = s
        t += 0.1
    trim_end = d - 0.05
    if best_s - end_s > 0.02 and best_t < d - 0.15:
        trim_end = best_t + 0.02
        print(f"{conn}: end={end_s:.3f} best@{best_t:.1f}={best_s:.3f} -> TRIM to {trim_end:.2f}s", flush=True)
    else:
        print(f"{conn}: end={end_s:.3f} best@{best_t:.1f}={best_s:.3f} -> keep", flush=True)
    i = conn.split("_")[1]
    enc_mobile(src, os.path.join(V, f"conn{i}-m.mp4"), 0.0, trim_end)

# 3) posters from the new mobile encodes
for n in NAMES:
    png = "_pposter.png"
    sh(["ffmpeg", "-v", "error", "-y", "-ss", "0", "-i", os.path.join(V, f"{n}-m.mp4"),
        "-frames:v", "1", "-q:v", "2", png])
    sh(["ffmpeg", "-v", "error", "-y", "-i", png, "-c:v", "libwebp", "-quality", "84",
        os.path.join(ASSETS, f"{n}-poster-m.webp")])
print("posters extracted", flush=True)

# 4) phone stills (-p.webp) from the new scene stills
for n in NAMES:
    sh(["ffmpeg", "-v", "error", "-y", "-i", f"pstill_{n}.png",
        "-vf", "scale=900:-2", "-c:v", "libwebp", "-quality", "86",
        os.path.join(ASSETS, f"{n}-p.webp")])
print("phone stills regenerated", flush=True)

# 5) SSIM gate over the chain
chain = ["beige-m.mp4", "conn1-m.mp4", "crashpad-m.mp4", "conn2-m.mp4", "crash-m.mp4",
         "conn3-m.mp4", "glowup-m.mp4", "conn4-m.mp4", "finale-m.mp4"]
print("=== SSIM SEAM GATE ===", flush=True)
worst = 1.0
for a, b in zip(chain, chain[1:]):
    last_frame(os.path.join(V, a), "_pga.png")
    frame_at(os.path.join(V, b), 0.0, "_pgb.png")
    s = ssim("_pga.png", "_pgb.png")
    worst = min(worst, s)
    tag = "PASS" if s >= 0.90 else ("WARN" if s >= 0.75 else "FAIL")
    print(f"{tag}  {a}>{b}  ssim={s:.4f}", flush=True)
print(f"=== GATE DONE (worst={worst:.4f}) ===", flush=True)
