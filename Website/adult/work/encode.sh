#!/bin/bash
# Encode the 5 legs for scrubbing + extract posters + SSIM seam gate.
# Idempotent: skips outputs that already exist. Run from work/.
set -u
cd "$(dirname "$0")"
A="../assets"
declare LEGS="1:quiet 2:glowup 3:photo 4:patio 5:sendoff"

for pair in $LEGS; do
  n="${pair%%:*}"; id="${pair##*:}"
  src="leg_${n}.mp4"
  [ -f "$src" ] || { echo "MISSING $src"; continue; }
  # desktop/tablet master: native 1080x1920, crf 20, GOP 8
  [ -f "$A/vid/${id}.mp4" ] || ffmpeg -y -v error -i "$src" -an \
    -vf "unsharp=5:5:0.8:5:5:0.0" -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p \
    -g 8 -keyint_min 8 -sc_threshold 0 -movflags +faststart "$A/vid/${id}.mp4"
  # phone encode: 720x1280, crf 23, GOP 4 (cheap seeks)
  [ -f "$A/vid/${id}-m.mp4" ] || ffmpeg -y -v error -i "$src" -an \
    -vf "scale=720:1280,unsharp=5:5:0.8:5:5:0.0" -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p \
    -g 4 -keyint_min 4 -sc_threshold 0 -movflags +faststart "$A/vid/${id}-m.mp4"
  # posters = first frames of the ENCODED clips (not the stills)
  [ -f "$A/${id}-poster.webp" ]   || ffmpeg -y -v error -i "$A/vid/${id}.mp4"   -frames:v 1 -qscale:v 75 "$A/${id}-poster.webp"
  [ -f "$A/${id}-poster-m.webp" ] || ffmpeg -y -v error -i "$A/vid/${id}-m.mp4" -frames:v 1 -qscale:v 75 "$A/${id}-poster-m.webp"
  echo "encoded $id"
done

echo "--- SSIM seam gate (encoded masters) ---"
prev=""
for pair in $LEGS; do
  id="${pair##*:}"
  if [ -n "$prev" ]; then
    ffmpeg -y -v error -sseof -0.05 -i "$A/vid/${prev}.mp4" -frames:v 1 -q:v 2 _seam_a.png
    ffmpeg -y -v error -i "$A/vid/${id}.mp4" -frames:v 1 -q:v 2 _seam_b.png
    ssim=$(ffmpeg -i _seam_a.png -i _seam_b.png -lavfi ssim -f null - 2>&1 | grep -o 'All:[0-9.]*' | cut -d: -f2)
    echo "seam ${prev}->${id}: SSIM=${ssim}"
  fi
  prev="$id"
done
rm -f _seam_a.png _seam_b.png
