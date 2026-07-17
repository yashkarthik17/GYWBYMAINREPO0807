#!/bin/bash
# Encode dive clips for scrubbing (1080p g8 master + 720p g4 mobile) and extract posters.
WORK="/c/Users/yashk/OneDrive/Desktop/Glad You Were Born Today (Repo)/Website/work"
ASSETS="/c/Users/yashk/OneDrive/Desktop/Glad You Were Born Today (Repo)/Website/assets"
cd "$WORK" || exit 1

enc() { ffmpeg -v error -y -i "$1" -an -vf "unsharp=5:5:0.8:5:5:0.0" \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p \
  -g 8 -keyint_min 8 -sc_threshold 0 -movflags +faststart "$2" && echo "enc $2 $(du -h "$2"|cut -f1)"; }

encm() { ffmpeg -v error -y -i "$1" -an -vf "scale=-2:720,unsharp=5:5:0.6:5:5:0.0" \
  -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p \
  -g 4 -keyint_min 4 -sc_threshold 0 -movflags +faststart "$2" && echo "encm $2 $(du -h "$2"|cut -f1)"; }

towebp() { ffmpeg -v error -y -i "$1" -c:v libwebp -quality 84 "$2"; }

for n in beige crashpad crash glowup finale; do
  enc  "dive_$n.mp4" "$ASSETS/vid/$n.mp4"
  encm "dive_$n.mp4" "$ASSETS/vid/$n-m.mp4"
  ffmpeg -v error -y -ss 0 -i "$ASSETS/vid/$n.mp4"   -frames:v 1 -q:v 2 "poster_$n.png"
  towebp "poster_$n.png" "$ASSETS/$n-poster.webp"
  ffmpeg -v error -y -ss 0 -i "$ASSETS/vid/$n-m.mp4" -frames:v 1 -q:v 2 "poster_${n}_m.png"
  towebp "poster_${n}_m.png" "$ASSETS/$n-poster-m.webp"
done
echo "=== DIVE ENCODES DONE ==="
ls -la "$ASSETS/vid" "$ASSETS" | grep -E "mp4|webp"
