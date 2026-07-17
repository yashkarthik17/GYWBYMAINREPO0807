#!/bin/bash
# Generate the 4 connector clips: start = previous dive's LAST frame, end = next dive's FIRST frame.
WORK="/c/Users/yashk/OneDrive/Desktop/Glad You Were Born Today (Repo)/Website/work"
cd "$WORK" || exit 1
VMODEL=seedance_2_0
VOPTS="--mode std --resolution 1080p"
CONN_DUR=5

geturl() { python -c "
import json,sys
try:
    d=json.load(open(sys.argv[1]))
    print(d[0].get('result_url') or '')
except Exception:
    print('')
" "$1"; }

gen_conn() { # i startPng endPng
  [ -s "conn_$1.mp4" ] && { echo "conn $1 cached"; return 0; }
  attempt=1
  while [ $attempt -le 3 ]; do
    higgsfield generate create "$VMODEL" --prompt "$(cat "conn_$1.txt")" \
      --start-image "$2" --end-image "$3" \
      $VOPTS --aspect_ratio 16:9 --duration "$CONN_DUR" \
      --wait --wait-timeout 20m --json > "conn_$1.json" 2> "conn_$1.err"
    url=$(geturl "conn_$1.json")
    if [ -n "$url" ]; then
      curl -fsSL "$url" -o "conn_$1.mp4" && { echo "conn $1 ok (attempt $attempt)"; return 0; }
    fi
    echo "conn $1 attempt $attempt failed:"; head -2 "conn_$1.err"; head -c 300 "conn_$1.json"; echo
    attempt=$((attempt+1))
  done
  echo "conn $1 FAIL after 3 attempts"
}

gen_conn 1 last_beige.png    first_crashpad.png &
gen_conn 2 last_crashpad.png first_crash.png    &
gen_conn 3 last_crash.png    first_glowup.png   &
gen_conn 4 last_glowup.png   first_finale.png   &
wait
echo "=== CONNECTORS DONE ==="
for i in 1 2 3 4; do
  [ -s "conn_$i.mp4" ] && echo "OK   conn_$i.mp4 $(du -h "conn_$i.mp4" | cut -f1)" || echo "MISS conn_$i.mp4"
done
