"""Stitch each tap-engine journey into ONE continuous video (per tier).

The clip-by-clip chain always has a handoff seam (decode/settle + event
latency reads as a pause between scenes). A single stitched file removes the
seam by construction: 0.15s crossfades are baked in, and each segment's
APPROVED playback pacing (config playbackRate x scene.rate) is baked in via
setpts, so the file plays at rate 1 and looks exactly like the tuned chain.

Outputs (+ poster webp extracted from frame 0) and a spans JSON mapping each
chain segment to [t0, t1] in the stitched timeline (contiguous through the
middle of each crossfade) — wired into the configs as journey.spans.

Normal GOP (not the scrub-era -g 4): continuous playthrough doesn't need
per-frame seeking, and a 2s keyint halves the file size.

Idempotent: re-running re-encodes the same outputs.
Run from Website/: python work/stitch_tap_journeys.py [--only kids-m,adult,...]
"""
import subprocess, os, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # Website/
FADE = 0.15
# 60fps output grid: rate-baking (setpts) raises the effective source rate to
# ~27.6-31.7fps; a 24fps grid DROPPED 13-24% of frames in an irregular cadence
# (visible judder on camera flights). At 60 every source frame keeps its own
# slot — duplicates fill the rest and encode/decode as near-free skip frames.
FPS = 60

# chain: (basename, baked_rate) in site order. Kids: global 1.15, scenes
# multiply (crashpad/crash 1.10, glowup/finale 1.15); connectors plain 1.15.
# Adult: global 1, per-scene rates from adult-config.js.
KIDS_RATES = [1.15, 1.15, 1.15 * 1.10, 1.15, 1.15 * 1.10, 1.15, 1.15 * 1.15, 1.15, 1.15 * 1.15]
KIDS_NAMES = ["beige", "conn1", "crashpad", "conn2", "crash", "conn3", "glowup", "conn4", "finale"]
ADULT_RATES = [1.235, 1.0, 1.1, 1.1, 1.1]
ADULT_NAMES = ["quiet", "glowup", "photo", "patio", "sendoff"]

JOBS = {
    # key: (vid_dir, [names], suffix, rates, out_basename, crf, maxrate, bufsize)
    "kids":    ("assets/vid",        KIDS_NAMES,  "",   KIDS_RATES,  "journey-tap",   22, "6M",  "12M"),
    "kids-m":  ("assets/vid",        KIDS_NAMES,  "-m", KIDS_RATES,  "journey-tap-m", 26, "4M",  "8M"),
    "adult":   ("adult/assets/vid",  ADULT_NAMES, "",   ADULT_RATES, "journey-tap",   22, "6M",  "12M"),
    "adult-m": ("adult/assets/vid",  ADULT_NAMES, "-m", ADULT_RATES, "journey-tap-m", 26, "4M",  "8M"),
}

# Per-segment (head, tail) trims in SOURCE seconds, applied before rate baking.
# adult landscape glowup: freezedetect measured a 1.33s FROZEN tail (the 2->3
# "stuck" hang — the mobile renders got this trim at the source; the landscape
# files never did). Trim 1.15s so ~0.18s of hold remains, which the 0.15s
# crossfade consumes — the seam lands on moving footage.
TRIMS = {
    "adult": [(0, 0), (0, 1.15), (0, 0), (0, 0), (0, 0)],
}


def sh(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(args)}\n{r.stderr[-800:]}")
    return r.stdout + r.stderr


def dur(f):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "csv=p=0", f]).strip())


def stitch(key):
    vdir, names, suffix, rates, outbase, crf, maxrate, bufsize = JOBS[key]
    vdir = os.path.join(ROOT, vdir)
    files = [os.path.join(vdir, f"{n}{suffix}.mp4") for n in names]
    out = os.path.join(vdir, f"{outbase}.mp4")

    trims = TRIMS.get(key, [(0, 0)] * len(files))
    # effective (trimmed, rate-baked) durations drive the xfade offsets
    raw = [dur(f) for f in files]
    D = [(d - h - t) / r for d, (h, t), r in zip(raw, trims, rates)]
    X = [0.0]
    for i in range(1, len(files)):
        X.append(X[i - 1] + D[i - 1] - FADE)

    inputs = []
    for f in files:
        inputs += ["-i", f]

    # per-input: trim, bake the pacing (setpts) and re-time to CFR for xfade
    parts = []
    for i, r in enumerate(rates):
        h, t = trims[i]
        pre = f"trim=start={h}:end={raw[i] - t:.6f}," if (h or t) else ""
        parts.append(f"[{i}:v]{pre}setpts=(PTS-STARTPTS)/{r:.6f},fps={FPS}[s{i}]")
    prev = "s0"
    for k in range(1, len(files)):
        label = f"v{k}"
        parts.append(f"[{prev}][s{k}]xfade=transition=fade:duration={FADE}:offset={X[k]:.6f}[{label}]")
        prev = label
    fc = ";".join(parts)

    sh(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", f"[{prev}]",
        "-an", "-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-pix_fmt", "yuv420p",
        "-maxrate", maxrate, "-bufsize", bufsize,
        "-g", str(FPS * 2), "-keyint_min", str(FPS), "-movflags", "+faststart", out])

    total = dur(out)
    spans = []
    for i in range(len(files)):
        t0 = X[i] + (FADE / 2 if i > 0 else 0.0)
        t1 = X[i] + D[i] - (FADE / 2 if i < len(files) - 1 else 0.0)
        spans.append([round(t0, 3), round(min(t1, total - 0.05), 3)])

    poster = os.path.join(vdir, "..", f"{outbase}-poster.webp") if suffix == "" \
        else os.path.join(vdir, "..", f"{outbase}-poster.webp")
    # posters live next to the other posters in the assets root of each site
    poster = os.path.normpath(os.path.join(vdir, "..", f"{outbase}-poster.webp"))
    sh(["ffmpeg", "-v", "error", "-y", "-i", out, "-frames:v", "1", poster])

    size_mb = os.path.getsize(out) / 1e6
    print(f"{key}: {os.path.relpath(out, ROOT)}  {total:.2f}s  {size_mb:.1f} MB")
    return {"out": os.path.relpath(out, ROOT).replace(os.sep, "/"),
            "poster": os.path.relpath(poster, ROOT).replace(os.sep, "/"),
            "total": round(total, 3), "spans": spans}


if __name__ == "__main__":
    only = None
    if len(sys.argv) > 2 and sys.argv[1] == "--only":
        only = set(sys.argv[2].split(","))
    results = {}
    for key in JOBS:
        if only and key not in only:
            continue
        results[key] = stitch(key)
    outj = os.path.join(ROOT, "work", "journey-spans.json")
    existing = {}
    if os.path.exists(outj):
        with open(outj, encoding="utf-8") as fh:
            existing = json.load(fh)
    existing.update(results)
    with open(outj, "w", encoding="utf-8") as fh:
        json.dump(existing, fh, indent=2)
    print(json.dumps(results, indent=2))
