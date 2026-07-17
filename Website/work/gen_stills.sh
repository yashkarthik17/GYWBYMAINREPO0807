#!/bin/bash
# Batch remaining scene stills, style-locked to the approved anchor (still_finale.png).
WORK="/c/Users/yashk/OneDrive/Desktop/Glad You Were Born Today (Repo)/Website/work"
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
  higgsfield generate create gpt_image_2 --prompt "$(cat "still_$1.txt")" \
    --image still_finale.png --image ref_starry.png --image ref_crashers.png \
    --aspect_ratio 3:2 --resolution 2k --quality high --wait --wait-timeout 15m --json \
    > "still_$1.json" 2> "still_$1.err"
  url=$(geturl "still_$1.json")
  if [ -n "$url" ]; then
    curl -fsSL "$url" -o "still_$1.png" && echo "still $1 ok"
  else
    echo "still $1 FAIL"; head -3 "still_$1.err"
  fi
}

for n in beige crashpad crash glowup; do gen_still "$n" & done
wait
echo "=== BATCH DONE ==="
for n in beige crashpad crash glowup finale; do
  [ -s "still_$n.png" ] && echo "OK   still_$n.png" || echo "MISS still_$n.png"
done
