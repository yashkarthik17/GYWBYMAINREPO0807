"""Adult-chain redo post-processing (two-tier: portrait mobile + landscape desktop).

Encodes the 5 raw legs into two tiers:
  - portrait mobile tier (720x1280, CRF 23, -g 48 -keyint_min 24 -- 2s
    keyframes @24fps, retuned for tap-engine's straight sequential playback;
    the old -g 4 grid only paid for the retired scrub-engine's chase-play
    seeks) from this round's portrait leg_{1..5}.mp4 raws -- also stitched
    into journey-m.mp4 (shipped for parity; unused by the live tap-engine).
  - landscape desktop master tier (1920x1080, CRF 20, GOP 8) from this round's
    lleg_{1..5}.mp4 raws -- five standalone full-bleed scene clips, no stitching.

Portrait desktop-quality masters (the old unscaled-portrait CRF-20 tier) RETIRE
for all five scenes: desktop is now served exclusively by the landscape
footage, so there is no more portrait "d" tier to produce. Posters/stills are
extracted from ENCODED clips only (seam-zero doctrine): landscape posters and
portrait posters+stills for all five scenes. Scene 1 ("quiet") was UNFROZEN at
the round-2 preview gate -- a new native-9:16 leg_1.mp4 is generated directly
into redo2/ this round, so it now gets the same full portrait treatment
(quiet-m.mp4 + poster + still) as scenes 2-5 instead of reusing its old
committed assets.

SEAM-GATE PIVOT (mid-plan design change, recorded in the plan's progress log):
the journey is no longer one continuous flight. Scene 1->2 is bridged by a
runtime crossfade and scene 2->3 by an in-clip sparkle-descent transition --
both are DESIGNED discontinuities, so a low SSIM score there is EXPECTED and
is NOT a gate failure or re-roll trigger. Seams 3->4 and 4->5 are the real
chained-continuity seams, checked (in both the raw-handoff and stitched-journey
passes) against the shipped chain's SSIM band of 0.38-0.70; a score drastically
outside that band needs a manual visual frame-pair check (same-scene +
confetti-drift = pass; different scene = FAIL -> report BLOCKED, do not
re-roll from this script).

Outputs staged in work/redo2/out/ -- nothing overwrites assets/ until the gate
is reviewed and Task 9 wires the page by hand.
"""
import subprocess, os, re, json, shutil

RD = r"C:\Users\yashk\gywbt-site\Website\adult\work\redo2"
OUT = os.path.join(RD, "out")
os.makedirs(OUT, exist_ok=True)
os.chdir(RD)

LEGS = [("leg_1", "quiet"), ("leg_2", "glowup"), ("leg_3", "photo"),
        ("leg_4", "patio"), ("leg_5", "sendoff")]
LSCENES = ["quiet", "glowup", "photo", "patio", "sendoff"]  # lleg_1..5 map to these, in order

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

# 0) Resolve portrait leg 1 raw footage. Scene 1 was unfrozen at the round-2
#    preview gate -- a new native-9:16 leg_1.mp4 is generated directly into
#    redo2/ this round, so it's expected to already be here. Simplified from
#    the prior frozen-leg version: no OneDrive/committed-master fallback,
#    since those pointed at the OLD frozen footage and would silently ship
#    stale scene 1 content if this round's raw is missing.
def resolve_leg1():
    local = os.path.join(RD, "leg_1.mp4")
    if os.path.exists(local):
        return local
    raise RuntimeError("leg_1.mp4 unresolved: expected the round-2 regenerated "
                        "native-9:16 raw at redo2/leg_1.mp4")

resolve_leg1()

# 1) Encode portrait mobile tier (720x1280, CRF 23) for all five legs.
for leg, name in LEGS:
    src = f"{leg}.mp4"
    m = os.path.join(OUT, f"{name}-m.mp4")
    if not os.path.exists(m):
        sh(["ffmpeg", "-v", "error", "-y", "-i", src, "-an",
            "-vf", "scale=720:1280,unsharp=5:5:0.8:5:5:0.0",
            "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-pix_fmt", "yuv420p",
            # 2s keyframes @24fps -- tap-engine plays clips straight through and
            # never seeks, so the old -g 4 chase-play seek grid just burned
            # ~6.5 Mbps of extra bitrate for nothing (see investigation-engine.md).
            "-g", "48", "-keyint_min", "24", "-sc_threshold", "0",
            "-movflags", "+faststart", m])
    print(f"encoded {name}-m: mobile {os.path.getsize(m)//1024}K")

# 2) Encode landscape desktop master tier (1920x1080, CRF 20, GOP 8) for all
#    five scenes, plus a poster grabbed straight off the encoded master
#    (seam-zero doctrine: same doctrine as encode.sh, landscape geometry).
for n, scene in enumerate(LSCENES, start=1):
    d = os.path.join(OUT, f"{scene}.mp4")
    if not os.path.exists(d):
        sh(["ffmpeg", "-y", "-v", "error", "-i", f"lleg_{n}.mp4", "-an",
            "-vf", "scale=1920:1080,unsharp=5:5:0.8:5:5:0.0",
            "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
            "-g", "8", "-keyint_min", "8", "-sc_threshold", "0", "-movflags", "+faststart",
            d])
    poster = os.path.join(OUT, f"{scene}-poster.webp")
    if not os.path.exists(poster):
        sh(["ffmpeg", "-y", "-v", "error", "-i", d,
            "-frames:v", "1", "-qscale:v", "75", poster])
    print(f"encoded {scene}: landscape {os.path.getsize(d)//1024}K")
print("landscape masters + posters extracted")

# 3) Portrait posters + stills for all five scenes. Scene 1 ("quiet") was
#    unfrozen at the round-2 preview gate, so it now gets the same
#    encoded-clip extraction as scenes 2-5 instead of reusing its old
#    committed poster/still assets.
for _, name in LEGS:
    webp_from(os.path.join(OUT, f"{name}-m.mp4"), 0.0,
              os.path.join(OUT, f"{name}-poster-m.webp"), 720)
    webp_from(os.path.join(OUT, f"{name}-m.mp4"), 4.0,
              os.path.join(OUT, f"{name}.webp"), 720)
print("portrait posters + stills extracted (all 5 scenes)")

# 4) Stitch mobile journey, trimming the duplicated handoff frame at each joint
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
    # kept consistent with the per-scene -m tier above even though journey-m
    # is unused by the live tap-engine today (it still ships).
    "-g", "48", "-keyint_min", "24", "-sc_threshold", "0", "-movflags", "+faststart", j])
webp_from(j, 0.0, os.path.join(OUT, "journey-poster-m.webp"), 720)
print(f"journey stitched: {dur(j):.3f}s @ {f:.3f}fps")
print("SPANS:", json.dumps(spans))
json.dump(spans, open(os.path.join(OUT, "spans.json"), "w"))

# 5) SSIM seam gate -- adapted per the mid-plan seam-gate interpretation pivot.
# Seams are numbered 1..4 across the five scenes (quiet-glowup-photo-patio-sendoff).
# Seam 1 (quiet->glowup) and seam 2 (glowup->photo) are DESIGNED discontinuities
# (runtime crossfade / in-clip sparkle-descent transition) -- reported, not gated.
# Seams 3 (photo->patio) and 4 (patio->sendoff) are the real chained-continuity
# gate: shipped-chain SSIM band is 0.38-0.70; a score drastically outside that
# band needs a manual visual frame-pair check (same-scene + confetti-drift =
# pass; different scene = FAIL -> BLOCKED, do not re-roll from this script).
SEAM_NAMES = [f"{LEGS[i][1]} -> {LEGS[i+1][1]}" for i in range(len(LEGS) - 1)]
EXPECTED_DISCONTINUITY = {0, 1}   # 0-indexed: seam 1 and seam 2
BAND_LO, BAND_HI = 0.38, 0.70

def classify(i, s):
    if i in EXPECTED_DISCONTINUITY:
        return "EXPECTED (designed transition, not gated)"
    if BAND_LO <= s <= BAND_HI:
        return "PASS (within shipped-chain band)"
    # Above BAND_HI is flagged too, not just below BAND_LO: near-1.0 SSIM on a
    # seam usually means a frozen/duplicate-frame stitch, not a great match.
    return "CHECK (outside band -- needs visual frame-pair review)"

A, B = os.path.join(OUT, "_ga.png"), os.path.join(OUT, "_gb.png")
print("== gate: encoded leg-to-leg handoffs ==")
genuine_scores = []
for i in range(len(mob) - 1):
    last_frame(mob[i], A)
    frame_at(mob[i + 1], trim, B)   # first frame AFTER the trimmed duplicate
    s = ssim(A, B)
    verdict = classify(i, s)
    if i not in EXPECTED_DISCONTINUITY:
        genuine_scores.append(s)
    print(f"  seam {i+1}: {SEAM_NAMES[i]:<16} SSIM {s:.3f}  {verdict}")
print("== gate: stitched journey boundaries ==")
for i in range(len(spans) - 1):
    t = spans[i][1]
    frame_at(j, max(t - 0.05, 0), A)
    frame_at(j, t + 0.05, B)
    s = ssim(A, B)
    verdict = classify(i, s)
    if i not in EXPECTED_DISCONTINUITY:
        genuine_scores.append(s)
    print(f"  seam {i+1} @{t:>7.3f}s: {SEAM_NAMES[i]:<16} SSIM {s:.3f}  {verdict}")
worst_genuine = min(genuine_scores) if genuine_scores else 1.0
gate_green = all(BAND_LO <= s <= BAND_HI for s in genuine_scores)
print(f"GATE {'GREEN' if gate_green else 'CHECK'} "
      f"(worst genuine-seam SSIM {worst_genuine:.3f}, expected band {BAND_LO}-{BAND_HI})")
