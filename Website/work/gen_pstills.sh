#!/bin/bash
# Portrait (2:3) scene stills — style-locked to each scene's approved landscape still + character refs.
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

gen_pstill() { # name
  [ -s "pstill_$1.png" ] && { echo "pstill $1 cached"; return 0; }
  higgsfield generate create gpt_image_2 --prompt "$(cat "pstill_$1.txt")" \
    --image "still_$1.png" --image ref_starry.png --image ref_crashers.png \
    --aspect_ratio 2:3 --resolution 2k --quality high --wait --wait-timeout 15m --json \
    > "pstill_$1.json" 2> "pstill_$1.err"
  url=$(geturl "pstill_$1.json")
  if [ -n "$url" ]; then
    curl -fsSL "$url" -o "pstill_$1.png" && echo "pstill $1 ok"
  else
    echo "pstill $1 FAIL"; head -3 "pstill_$1.err"
  fi
}

for n in beige crashpad crash glowup finale; do gen_pstill "$n" & done
wait
echo "=== PORTRAIT STILLS DONE ==="
for n in beige crashpad crash glowup finale; do
  [ -s "pstill_$n.png" ] && echo "OK   pstill_$n.png" || echo "MISS pstill_$n.png"
done
