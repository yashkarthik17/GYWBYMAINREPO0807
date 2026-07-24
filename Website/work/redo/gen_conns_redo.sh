#!/bin/bash
# Redo portrait chain, phase 2: 4 connectors endpoint-locked to the dives' actual frames.
WORK="/c/Users/yashk/OneDrive/Desktop/Glad You Were Born Today (Repo)/Website/work/redo"
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
      $VOPTS --aspect_ratio 9:16 \
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

gen_vid pconn_1 pconn_1.txt --start-image plast_beige.png    --end-image pfirst_crashpad.png --duration 5 &
gen_vid pconn_2 pconn_2.txt --start-image plast_crashpad.png --end-image pfirst_crash.png    --duration 5 &
gen_vid pconn_3 pconn_3.txt --start-image plast_crash.png    --end-image pfirst_glowup.png   --duration 5 &
gen_vid pconn_4 pconn_4.txt --start-image plast_glowup.png   --end-image pfirst_finale.png   --duration 5 &
wait

echo "=== CONNECTORS DONE ==="
for f in pconn_1 pconn_2 pconn_3 pconn_4; do
  [ -s "$f.mp4" ] && echo "OK   $f.mp4 $(du -h "$f.mp4" | cut -f1)" || echo "MISS $f.mp4"
done
