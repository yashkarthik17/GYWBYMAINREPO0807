#!/bin/bash
# Landscape chain phase 1: 5 dives (16:9 1080p, seedance_2_0) + boundary frame extraction.
WORK="/c/Users/yashk/OneDrive/Desktop/Glad You Were Born Today (Repo)/Website/work/redo-landscape"
cd "$WORK" || exit 1
VMODEL=seedance_2_0
VOPTS="--mode std --resolution 1080p"

geturl() { python -c "
import json,sys
try:
    d=json.load(open(sys.argv[1]))
    print(d[0].get('result_url') or '')
except Exception:
    print('')
" "$1"; }

gen_vid() { # outbase promptfile extra-args...
  base="$1"; pfile="$2"; shift 2
  [ -s "$base.mp4" ] && { echo "$base cached"; return 0; }
  attempt=1
  while [ $attempt -le 3 ]; do
    higgsfield generate create "$VMODEL" --prompt "$(cat "$pfile")" "$@" \
      $VOPTS --aspect_ratio 16:9 \
      --wait --wait-timeout 20m --json > "$base.json" 2> "$base.err"
    url=$(geturl "$base.json")
    if [ -n "$url" ]; then
      curl -fsSL "$url" -o "$base.mp4" && { echo "$base ok (attempt $attempt)"; return 0; }
    fi
    echo "$base attempt $attempt failed:"; head -2 "$base.err"; head -c 200 "$base.json"; echo
    attempt=$((attempt+1))
  done
  echo "$base FAIL after 3 attempts"
}

for n in beige crashpad crash glowup finale; do
  gen_vid "dive_$n" "dive_$n.txt" --start-image "still_$n.png" --duration 8 &
done
wait

echo "=== DIVES DONE ==="
for n in beige crashpad crash glowup finale; do
  if [ -s "dive_$n.mp4" ]; then
    ffmpeg -v error -y -ss 0 -i "dive_$n.mp4" -frames:v 1 -q:v 2 "first_$n.png"
    ffmpeg -v error -y -sseof -0.15 -i "dive_$n.mp4" -frames:v 1 -q:v 2 "last_$n.png"
    echo "OK   dive_$n.mp4 $(du -h "dive_$n.mp4" | cut -f1)"
  else
    echo "MISS dive_$n.mp4"
  fi
done
