#!/bin/bash
# gen_leg.sh <name> <prompt.txt> <aspect> <start.png|-> <end.png|->
#   e.g. (anchored from frame 1):  ./gen_leg.sh leg_2 leg_2.txt 9:16 pstill_2.png -
#   e.g. (anchored on last frame): ./gen_leg.sh leg_3 leg_3.txt 9:16 - pstill_3.png
#   e.g. (chained continuity):     ./gen_leg.sh leg_4 leg_4.txt 9:16 start_leg4.png -
# Params mirror redo/leg_3.json: seedance_2_0, mode std, 1080p, 8s.
# Pass "-" (or leave empty) for either slot to omit that flag entirely.
#
# === ROUND 3 FINDING (definitive, empirically confirmed) ===
# Task: attach the canonical Starry/Crashers reference sheets to every leg
# so character models stop drifting. Diagnosed via real `generate create`
# calls against the live API (not just `generate cost`, which does NOT
# perform this validation and gives false confidence):
#
# 1. Two or three --image flags together (with or without --start-image)
#    -> hard validation error, no job created, no credits spent:
#      Error: Value error, 'medias' can contain at most one start_image
#    The higgsfield-generate skill's references/media-inputs.md claims
#    seedance_2_0 has an independent `image` role distinct from
#    `start_image` -- that is WRONG for this account/CLI version. Confirmed
#    by inspecting a submitted job's params: a lone --image (no
#    --start-image at all) comes back from `generate get` tagged
#    `"role": "start_image"`. --image is a plain alias for --start-image
#    here. At most ONE image total (across --image/--start-image combined)
#    can ever be attached to a seedance_2_0 job via this CLI.
#
# 2. --end-image IS a genuinely separate role (start_image + end_image
#    together validates and submits fine -- confirmed via `generate get`
#    showing two distinct media entries). But both are literal video
#    keyframes, not style/character references. Confirmed with two real
#    diagnostic renders (~144 credits, see redo2/diag_r3_*_test.mp4 +
#    audit/diag_r3_*/): a raw white-background character-sheet image used
#    as a keyframe renders as a near-static shot of that flat product photo
#    (or the clip visibly dissolves INTO it) -- never usable directly.
#
# === ROUND 3 RESOLUTION: anchor-still pipeline (controller-approved) ===
# Since raw reference sheets can't be used as keyframes, on-model influence
# is achieved one level up: gen_still.sh (gpt_image_2, which DOES support
# true multi-image references) pre-composes a real in-scene anchor still
# with the canonical refs attached (see pstill_2.txt/pstill_3.txt, and
# `./gen_still.sh pstillN pstillN.txt 9:16 refs/ref_starry.png
# refs/ref_crashers_turnaround.png [refs/ref_1.png]`). That composed,
# already-on-model still is then fed into THIS script as a normal
# --start-image or --end-image -- a legitimate keyframe, not a bare
# character cutout, so it doesn't corrupt the shot. Recipe used for legs
# 2-5: leg_2 start=pstill_2.png (anchored on-model from frame 1), leg_3
# end=pstill_3.png with no start (free descent-through-sparkles opening
# resolves onto the on-model group-photo keyframe, which also protects the
# leg_4 chain), leg_4/leg_5 start=extracted chain frame as before (round
# 1/2 mechanism, unchanged -- the chain frame is already on-model because
# it descends from leg_3's on-model end keyframe).
set -u
NAME="$1"; PROMPT="$2"; AR="$3"; START="${4:-}"; END="${5:-}"
START_ARGS=()
[ -n "$START" ] && [ "$START" != "-" ] && START_ARGS=(--start-image "$START")
END_ARGS=()
[ -n "$END" ] && [ "$END" != "-" ] && END_ARGS=(--end-image "$END")
higgsfield generate create seedance_2_0 \
  --prompt "$(cat "$PROMPT")" \
  "${START_ARGS[@]}" "${END_ARGS[@]}" \
  --mode std --resolution 1080p --aspect_ratio "$AR" --duration 8 \
  --wait --wait-timeout 20m --json > "$NAME.json" 2> "$NAME.err"
url=$(python -c "
import json,sys
try:
    d=json.load(open('$NAME.json')); d=d[0] if isinstance(d,list) else d
    print(d.get('result_url') or (d.get('results') or [{}])[0].get('url') or '')
except Exception: print('')")
[ -n "$url" ] && curl -fsSL "$url" -o "$NAME.mp4" && echo "OK $NAME.mp4" || { echo "FAIL $NAME"; head -c 300 "$NAME.json"; head -2 "$NAME.err"; }
