"""Rebuild journey-m with short crossfades at the joints (replaces hard-cut concat).

The two anchor-pinned seams are structurally continuous but re-render the
confetti/sparkle field, so a hard cut reads as a one-frame twinkle-pop. A
4-frame xfade absorbs it. Spans put each section boundary at the blend center.
"""
import subprocess, os, json

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.chdir(OUT)
NAMES = ["quiet", "glowup", "photo", "patio", "sendoff"]
D = 4 / 24.0  # 4-frame crossfade @ 24fps

def sh(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(args)}\n{r.stderr[-500:]}")
    return r.stdout + r.stderr

def dur(f):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "csv=p=0", f]).strip())

clips = [f"{n}-m.mp4" for n in NAMES]
durs = [dur(c) for c in clips]

inputs, filters = [], []
for c in clips:
    inputs += ["-i", c]
L = durs[0]
prev = "[0:v]"
offsets = []
for i in range(1, len(clips)):
    off = L - D
    offsets.append(off)
    lab = f"[x{i}]" if i < len(clips) - 1 else "[out]"
    filters.append(f"{prev}[{i}:v]xfade=transition=fade:duration={D:.4f}:offset={off:.4f}{lab}")
    prev = f"[x{i}]"
    L = L + durs[i] - D

sh(["ffmpeg", "-v", "error", "-y", *inputs,
    "-filter_complex", ";".join(filters), "-map", "[out]",
    "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-pix_fmt", "yuv420p",
    "-g", "4", "-keyint_min", "4", "-sc_threshold", "0",
    "-movflags", "+faststart", "journey-m.mp4"])

bounds = [round(o + D / 2, 3) for o in offsets]
spans = []
start = 0.0
for b in bounds + [round(dur("journey-m.mp4"), 3)]:
    spans.append([round(start, 3), b])
    start = b
print("journey duration:", round(dur("journey-m.mp4"), 3))
print("SPANS:", json.dumps(spans))
