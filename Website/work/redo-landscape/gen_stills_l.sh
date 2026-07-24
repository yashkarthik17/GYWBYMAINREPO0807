#!/bin/bash
# Landscape (3:2) scene stills for the desktop tier — content/style-locked to the
# approved redo portrait stills (same scene, same characters, same light).
# Usage: gen_stills_l.sh beige            -> anchor only
#        gen_stills_l.sh crashpad crash … -> batch the rest
WORK="/c/Users/yashk/OneDrive/Desktop/Glad You Were Born Today (Repo)/Website/work/redo-landscape"
cd "$WORK" || exit 1

geturl() { python -c "
import json,sys
try:
    d=json.load(open(sys.argv[1]))
    print(d[0].get('result_url') or '')
except Exception:
    print('')
" "$1"; }

gen_still() { # name
  [ -s "still_$1.png" ] && { echo "still $1 cached"; return 0; }
  attempt=1
  while [ $attempt -le 3 ]; do
    higgsfield generate create gpt_image_2 --prompt "$(cat "still_$1.txt")" \
      --image "../redo/pstill_$1.png" \
      --aspect_ratio 3:2 --resolution 2k --quality high \
      --wait --wait-timeout 15m --json > "still_$1.json" 2> "still_$1.err"
    url=$(geturl "still_$1.json")
    if [ -n "$url" ]; then
      curl -fsSL "$url" -o "still_$1.png" && { echo "still $1 ok (attempt $attempt)"; return 0; }
    fi
    echo "still $1 attempt $attempt failed:"; head -2 "still_$1.err"; head -c 200 "still_$1.json"; echo
    attempt=$((attempt+1))
  done
  echo "still $1 FAIL after 3 attempts"
}

for n in "$@"; do gen_still "$n" & done
wait
echo "=== STILLS DONE ==="
for n in "$@"; do
  [ -s "still_$n.png" ] && echo "OK   still_$n.png" || echo "MISS still_$n.png"
done
