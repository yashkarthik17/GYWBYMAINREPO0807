#!/bin/bash
# Generate the 5 dive-in clips on seedance_2_0, start-image = scene still. 3 attempts each (NSFW re-roll ladder).
WORK="/c/Users/yashk/OneDrive/Desktop/Glad You Were Born Today (Repo)/Website/work"
cd "$WORK" || exit 1
VMODEL=seedance_2_0
VOPTS="--mode std --resolution 1080p"
DIVE_DUR=8

geturl() { python -c "
import json,sys
try:
    d=json.load(open(sys.argv[1]))
    print(d[0].get('result_url') or '')
except Exception:
    print('')
" "$1"; }

gen_dive() { # name
  [ -s "dive_$1.mp4" ] && { echo "dive $1 cached"; return 0; }
  attempt=1
  while [ $attempt -le 3 ]; do
    higgsfield generate create "$VMODEL" --prompt "$(cat "dive_$1.txt")" \
      --start-image "still_$1.png" \
      $VOPTS --aspect_ratio 16:9 --duration "$DIVE_DUR" \
      --wait --wait-timeout 20m --json > "dive_$1.json" 2> "dive_$1.err"
    url=$(geturl "dive_$1.json")
    if [ -n "$url" ]; then
      curl -fsSL "$url" -o "dive_$1.mp4" && { echo "dive $1 ok (attempt $attempt)"; return 0; }
    fi
    echo "dive $1 attempt $attempt failed:"; head -2 "dive_$1.err"; head -c 300 "dive_$1.json"; echo
    attempt=$((attempt+1))
  done
  echo "dive $1 FAIL after 3 attempts"
}

for n in beige crashpad crash glowup finale; do gen_dive "$n" & done
wait
echo "=== DIVES DONE ==="
for n in beige crashpad crash glowup finale; do
  [ -s "dive_$n.mp4" ] && echo "OK   dive_$n.mp4 $(du -h "dive_$n.mp4" | cut -f1)" || echo "MISS dive_$n.mp4"
done
