"""Package the stitched journey masters into self-hosted HLS ladders.

Delivery upgrade (QA: stutter/quality on weak connections + old devices):
each journey gets a multi-bitrate HLS rendition ladder + master playlist,
served as plain static files (Vercel CDN-caches the segments). Playback
starts on a low rung immediately and adapts up — no more choosing between
"buffer forever" and "stutter". The progressive MP4s stay as fallback.

Keyframes align to segment boundaries (g = 2s, hls_time = 4s -> 2 GOPs per
segment), fMP4 segments (Safari native + hls.js both happy).

Run from Website/: python work/hls_package.py [--only kids-m,...]
Idempotent: re-running re-encodes the same outputs.
"""
import subprocess, os, json, sys

# forward slashes throughout: ffmpeg's hls muxer joins the init-segment path
# against the playlist dirname by splitting on '/', so Windows-mixed
# separators silently strand the init file elsewhere
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace(os.sep, "/")

# job -> (master_path, out_dir, portrait?, fps, rungs)
# rung: (name, scale_arg, out_fps, crf, maxrate_k)
# rung: (name, scale_arg, out_fps, crf, maxrate_k, "WxH", codec)
# dims/codec are explicit — the fMP4 init segment doesn't expose them to
# ffprobe, and a malformed RESOLUTION= breaks the master playlist. Codec
# levels follow x264's auto level for each dims@fps (High profile).
LANDSCAPE_RUNGS = [
    ("r1080", "1920:-2", 60, 22, 5500, "1920x1080", "avc1.64002A"),
    ("r720",  "1280:-2", 60, 23, 3000, "1280x720",  "avc1.640020"),
    ("r540",  "960:-2",  30, 24, 1400, "960x540",   "avc1.64001F"),
    ("r360",  "640:-2",  30, 25, 700,  "640x360",   "avc1.64001E"),
]
PORTRAIT_RUNGS = [
    ("r720", "720:-2", 60, 23, 3600, "720x1280", "avc1.640020"),
    ("r540", "540:-2", 60, 24, 2000, "540x960",  "avc1.640020"),
    ("r360", "360:-2", 30, 25, 850,  "360x640",  "avc1.64001E"),
]

JOBS = {
    "kids":    ("assets/vid/journey-tap.mp4",         "assets/vid/hls/journey-tap",         LANDSCAPE_RUNGS),
    "kids-m":  ("assets/vid/journey-tap-m.mp4",       "assets/vid/hls/journey-tap-m",       PORTRAIT_RUNGS),
    "adult":   ("adult/assets/vid/journey-tap.mp4",   "adult/assets/vid/hls/journey-tap",   LANDSCAPE_RUNGS),
    "adult-m": ("adult/assets/vid/journey-tap-m.mp4", "adult/assets/vid/hls/journey-tap-m", PORTRAIT_RUNGS),
}


def sh(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(args)}\n{r.stderr[-800:]}")
    return r.stdout + r.stderr


def probe(path, entries, stream=True):
    sel = ["-select_streams", "v:0", "-show_entries", f"stream={entries}"] if stream \
        else ["-show_entries", f"format={entries}"]
    return sh(["ffprobe", "-v", "error", *sel, "-of", "csv=p=0", path]).strip()


def package(key):
    master, outdir, rungs = JOBS[key]
    master = ROOT + "/" + master
    outdir = ROOT + "/" + outdir
    os.makedirs(outdir, exist_ok=True)

    dur = float(probe(master, "duration", stream=False))
    mw = int(probe(master, "width").split(",")[0])
    variants = []
    for name, scale, fps, crf, mrk, res, codec in rungs:
        # never upscale: skip rungs wider than the master (e.g. a 720p master
        # skips the 1080 rung)
        if int(scale.split(":")[0]) > mw:
            print(f"  {key}/{name}: skipped (master is {mw}px wide)")
            continue
        seg = f"{outdir}/{name}_%03d.m4s"
        pl = f"{outdir}/{name}.m3u8"
        sh(["ffmpeg", "-v", "error", "-y", "-i", master,
            "-vf", f"scale={scale},fps={fps}",
            "-an", "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
            "-maxrate", f"{mrk}k", "-bufsize", f"{mrk * 2}k", "-pix_fmt", "yuv420p",
            "-g", str(fps * 2), "-keyint_min", str(fps * 2), "-sc_threshold", "0",
            "-f", "hls", "-hls_time", "4", "-hls_playlist_type", "vod",
            "-hls_segment_type", "fmp4",
            "-hls_segment_filename", seg,
            "-hls_fmp4_init_filename", f"{name}_init.mp4",
            pl])
        size = sum(os.path.getsize(os.path.join(outdir, f)) for f in os.listdir(outdir)
                   if f.startswith(name + "_") and (f.endswith(".m4s") or f.endswith(".mp4")))
        avg_bw = int(size * 8 / dur)
        peak_bw = max(int(mrk * 1000 * 1.15), avg_bw)
        variants.append((peak_bw, avg_bw, res, fps, codec, f"{name}.m3u8"))
        print(f"  {key}/{name}: {res}@{fps} avg {avg_bw//1000}kbps ({size/1e6:.1f} MB)")

    lines = ["#EXTM3U", "#EXT-X-VERSION:7", "#EXT-X-INDEPENDENT-SEGMENTS"]
    for peak, avg, res, fps, codec, uri in variants:
        lines.append(f'#EXT-X-STREAM-INF:BANDWIDTH={peak},AVERAGE-BANDWIDTH={avg},'
                     f'RESOLUTION={res},FRAME-RATE={fps}.000,CODECS="{codec}"')
        lines.append(uri)
    with open(os.path.join(outdir, "journey.m3u8"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    total = sum(os.path.getsize(os.path.join(outdir, f)) for f in os.listdir(outdir))
    print(f"{key}: master journey.m3u8, {len(variants)} rungs, ladder total {total/1e6:.1f} MB")


if __name__ == "__main__":
    only = None
    if len(sys.argv) > 2 and sys.argv[1] == "--only":
        only = set(sys.argv[2].split(","))
    for k in JOBS:
        if only and k not in only:
            continue
        print(f"== {k} ==")
        package(k)
