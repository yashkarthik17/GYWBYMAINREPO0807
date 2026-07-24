"""Pick the better take per re-rolled connector (v1 vs fresh). Scores each candidate:
  start = SSIM(candidate first frame, previous dive's handoff frame  = its start_image)
  arrive = best SSIM over the candidate's last 2.5s vs next dive's first frame (same
           sweep the finish pass uses, so the score predicts the post-trim seam)
Winner = higher min(start, arrive); the loser is kept as *_lose.mp4 for reference.
The winner ends up at conn_N.mp4 so finish_landscape.py picks it up unchanged."""
import subprocess, re, os, shutil

WORK = r"C:\Users\yashk\OneDrive\Desktop\Glad You Were Born Today (Repo)\Website\work\redo-landscape"
os.chdir(WORK)
CONNS = [("conn_2", "last_crashpad.png", "first_crash.png"),
         ("conn_3", "last_crash.png",    "first_glowup.png"),
         ("conn_4", "last_glowup.png",   "first_finale.png")]

def sh(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(args)}\n{r.stderr[-300:]}")
    return r.stdout + r.stderr

def dur(f):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).strip())

def frame_at(video, t, out):
    sh(["ffmpeg", "-v", "error", "-y", "-i", video, "-ss", f"{t:.3f}", "-frames:v", "1", "-q:v", "2", out])

def ssim(a, b):
    out = sh(["ffmpeg", "-v", "info", "-i", a, "-i", b, "-lavfi",
              "[0:v]scale=960:540[a];[1:v]scale=960:540[b];[a][b]ssim", "-f", "null", "-"])
    m = re.search(r"All:([0-9.]+)", out)
    return float(m.group(1)) if m else 0.0

def score(clip, start_png, next0_png):
    frame_at(clip, 0.0, "_cmp_first.png")
    start = ssim("_cmp_first.png", start_png)
    d = dur(clip)
    t = max(d / 2, d - 2.5)
    arrive = -1.0
    while t <= d - 0.04:
        frame_at(clip, t, "_cmp_probe.png")
        arrive = max(arrive, ssim("_cmp_probe.png", next0_png))
        t += 0.1
    return start, arrive

for conn, start_png, next0_png in CONNS:
    v1, v2 = f"{conn}_v1.mp4", f"{conn}.mp4"
    s1 = score(v1, start_png, next0_png)
    s2 = score(v2, start_png, next0_png)
    pick2 = min(s2) >= min(s1)
    win, lose, sw, sl = (v2, v1, s2, s1) if pick2 else (v1, v2, s1, s2)
    print(f"{conn}: fresh start={s2[0]:.3f} arrive={s2[1]:.3f} | v1 start={s1[0]:.3f} arrive={s1[1]:.3f}"
          f" -> keep {'fresh' if pick2 else 'v1'} (min {min(sw):.3f} vs {min(sl):.3f})", flush=True)
    if not pick2:
        shutil.move(v2, f"{conn}_lose.mp4")
        shutil.move(v1, v2)
