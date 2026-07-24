#!/bin/bash
# Landscape chain phase 2: 4 connectors endpoint-locked to the dives' actual frames.
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

gen_vid conn_1 conn_1.txt --start-image last_beige.png    --end-image first_crashpad.png --duration 5 &
gen_vid conn_2 conn_2.txt --start-image last_crashpad.png --end-image first_crash.png    --duration 5 &
gen_vid conn_3 conn_3.txt --start-image last_crash.png    --end-image first_glowup.png   --duration 5 &
gen_vid conn_4 conn_4.txt --start-image last_glowup.png   --end-image first_finale.png   --duration 5 &
wait

echo "=== CONNECTORS DONE ==="
for f in conn_1 conn_2 conn_3 conn_4; do
  [ -s "$f.mp4" ] && echo "OK   $f.mp4 $(du -h "$f.mp4"|cut -f1)" || echo "MISS $f.mp4"
done
