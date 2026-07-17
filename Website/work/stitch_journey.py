"""Stitch the 9 portrait mobile clips into one seamless journey video.

Crossfades (0.15s, same width as the site's seam dissolve) are baked in between
segments, so the single video needs no runtime seam handling at all. Output keeps
the tight-GOP settings (-g 4) so single-element scroll-scrubbing stays cheap.
Prints the per-segment time spans to wire into index.html (journeyMobile.spans).
Idempotent: re-running just re-encodes the same output.
"""
import subprocess, os, json

WORK = r"C:\Users\yashk\OneDrive\Desktop\Glad You Were Born Today (Repo)\Website\work"
V = r"C:\Users\yashk\OneDrive\Desktop\Glad You Were Born Today (Repo)\Website\assets\vid"
os.chdir(V)

# site order: dive0, conn1, dive1, conn2, dive2, conn3, dive3, conn4, dive4
CHAIN = ["beige-m", "conn1-m", "crashpad-m", "conn2-m", "crash-m",
         "conn3-m", "glowup-m", "conn4-m", "finale-m"]
FADE = 0.15
OUT = "journey-m.mp4"

def sh(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(args)}\n{r.stderr[-600:]}")
    return r.stdout + r.stderr

def dur(f):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "csv=p=0", f]).strip())

D = [dur(f"{n}.mp4") for n in CHAIN]

# xfade chain: clip i starts contributing at X_i; transition k has offset X_k
X = [0.0]
for i in range(1, len(CHAIN)):
    X.append(X[i - 1] + D[i - 1] - FADE)

inputs = []
for n in CHAIN:
    inputs += ["-i", f"{n}.mp4"]

parts, prev = [], "0:v"
for k in range(1, len(CHAIN)):
    label = f"v{k}"
    parts.append(f"[{prev}][{k}:v]xfade=transition=fade:duration={FADE}:offset={X[k]:.6f}[{label}]")
    prev = label
fc = ";".join(parts)

sh(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", f"[{prev}]",
    "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-pix_fmt", "yuv420p",
    "-g", "4", "-keyint_min", "4", "-sc_threshold", "0", "-movflags", "+faststart", OUT])

total = dur(OUT)
# per-segment spans, CONTIGUOUS through the middle of each crossfade — adjacent
# segments share a boundary time, so the scroll→time mapping never jumps at a seam
spans = []
for i, n in enumerate(CHAIN):
    t0 = X[i] + (FADE / 2 if i > 0 else 0.0)
    t1 = X[i] + D[i] - (FADE / 2 if i < len(CHAIN) - 1 else 0.0)
    spans.append([round(t0, 3), round(min(t1, total - 0.05), 3)])

size_mb = os.path.getsize(OUT) / 1e6
print(f"journey: {OUT}  {total:.2f}s  {size_mb:.1f} MB")
print("spans (index.html journeyMobile.spans):")
print(json.dumps(spans))
