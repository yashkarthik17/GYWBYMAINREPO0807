#!/bin/bash
# gen_still.sh <name> <prompt.txt> [aspect_ratio] [ref1.png] [ref2.png] ...
#   e.g.: ./gen_still.sh lstill_2 lstill_2.txt refs/ref_starry.png refs/ref_crashers_turnaround.png refs/ref_1.png
#   e.g. (portrait anchor, round 3 task 5): ./gen_still.sh pstill_2 pstill_2.txt 9:16 refs/ref_starry.png refs/ref_crashers_turnaround.png refs/ref_1.png
# aspect_ratio is OPTIONAL and backward-compatible: if the arg right after the
# prompt matches N:N (e.g. "9:16") it's taken as the aspect ratio and
# defaults to 16:9 otherwise, so every existing lstill_*/lleg_1* call (which
# never passes an aspect-ratio-shaped arg there, only ref file paths) keeps
# behaving exactly as before.
# Params mirror redo/still_crash.json job record: that record's internal
# params.model is "videotape-alpha", but "videotape-alpha" is NOT a valid CLI
# job_set_type (`higgsfield model list` has no such entry; `generate create
# videotape-alpha` errors "Unknown model"). The record's job_set_type /
# display_name is gpt_image_2 / "GPT Image 2" -- that is the correct CLI
# argument. 2k resolution.
# Round 2 (landscape tier, task 8): round 1 used a single hardcoded
# --image refs/ref_1.png; the USER rejected round-1 stills for off-model
# characters (plush knockoffs, bead eyes) because no official character refs
# were ever attached. Round 2 takes reference image paths as trailing CLI
# args instead of hardcoding one, so every generation can attach the
# canonical character refs (refs/ref_starry.png, refs/ref_crashers_turnaround.png)
# plus any scene-specific extra (refs/ref_1.png for the cloud clubhouse, scene
# 2 only). `higgsfield generate cost gpt_image_2 --image a --image b` confirmed
# the CLI/API accept multiple --image flags on one job (medias is an array
# param per `higgsfield model get gpt_image_2`).
set -u
NAME="$1"; PROMPT="$2"; shift 2
AR="16:9"
if [[ "${1:-}" =~ ^[0-9]+:[0-9]+$ ]]; then AR="$1"; shift; fi
REF_ARGS=()
for ref in "$@"; do REF_ARGS+=(--image "$ref"); done
higgsfield generate create gpt_image_2 \
  --prompt "$(cat "$PROMPT")" \
  "${REF_ARGS[@]}" \
  --resolution 2k --aspect_ratio "$AR" \
  --wait --wait-timeout 10m --json > "$NAME.json" 2> "$NAME.err"
url=$(python -c "
import json,sys
try:
    d=json.load(open('$NAME.json')); d=d[0] if isinstance(d,list) else d
    print(d.get('result_url') or (d.get('results') or [{}])[0].get('url') or '')
except Exception: print('')")
[ -n "$url" ] && curl -fsSL "$url" -o "$NAME.png" && echo "OK $NAME.png" || { echo "FAIL $NAME"; head -c 300 "$NAME.json"; head -2 "$NAME.err"; }
