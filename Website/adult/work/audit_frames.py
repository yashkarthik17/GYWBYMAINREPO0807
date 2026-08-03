# Website/adult/work/audit_frames.py
"""Rip 1 frame/second from a clip (or copy a still) for child-audit review.
Usage: python audit_frames.py path/to/clip.mp4 [outdir]   (outdir default: ./audit)"""
import os, subprocess, sys

src = sys.argv[1]
outdir = sys.argv[2] if len(sys.argv) > 2 else "audit"
os.makedirs(outdir, exist_ok=True)
stem = os.path.splitext(os.path.basename(src))[0]

if src.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
    out = os.path.join(outdir, f"{stem}-t0.jpg")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-q:v", "3", out], check=True)
    print(out)
    sys.exit(0)

dur = float(subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
    capture_output=True, text=True, check=True).stdout.strip())
t = 0.0
while t < dur:
    out = os.path.join(outdir, f"{stem}-t{int(t)}.jpg")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", src,
                    "-frames:v", "1", "-q:v", "3", out], check=True)
    print(out)
    t += 1.0
