#!/bin/bash
# gen_still.sh <name> <prompt.txt>   e.g.: ./gen_still.sh lstill_1 lstill_1.txt
# Params mirror redo/still_crash.json job record: that record's internal
# params.model is "videotape-alpha", but "videotape-alpha" is NOT a valid CLI
# job_set_type (`higgsfield model list` has no such entry; `generate create
# videotape-alpha` errors "Unknown model"). The record's job_set_type /
# display_name is gpt_image_2 / "GPT Image 2" -- that is the correct CLI
# argument. 2k resolution, plus the reference image refs/ref_1.png for
# on-model character consistency (that historical record used --image, the
# still-image reference flag; --start-image/--end-image are video-only roles,
# confirmed via `higgsfield generate create --help`, which documents --image
# as the still reference flag distinct from --start-image used by
# gen_leg.sh for video).
set -u
NAME="$1"; PROMPT="$2"
higgsfield generate create gpt_image_2 \
  --prompt "$(cat "$PROMPT")" \
  --image refs/ref_1.png \
  --resolution 2k --aspect_ratio 16:9 \
  --wait --wait-timeout 10m --json > "$NAME.json" 2> "$NAME.err"
url=$(python -c "
import json,sys
try:
    d=json.load(open('$NAME.json')); d=d[0] if isinstance(d,list) else d
    print(d.get('result_url') or (d.get('results') or [{}])[0].get('url') or '')
except Exception: print('')")
[ -n "$url" ] && curl -fsSL "$url" -o "$NAME.png" && echo "OK $NAME.png" || { echo "FAIL $NAME"; head -c 300 "$NAME.json"; head -2 "$NAME.err"; }
