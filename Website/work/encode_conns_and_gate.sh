#!/bin/bash
# Encode connectors (desktop + mobile) then run the SSIM seam gate over the whole chain.
WORK="/c/Users/yashk/OneDrive/Desktop/Glad You Were Born Today (Repo)/Website/work"
ASSETS="/c/Users/yashk/OneDrive/Desktop/Glad You Were Born Today (Repo)/Website/assets"
cd "$WORK" || exit 1

enc() { ffmpeg -v error -y -i "$1" -an -vf "unsharp=5:5:0.8:5:5:0.0" \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p \
  -g 8 -keyint_min 8 -sc_threshold 0 -movflags +faststart "$2" && echo "enc $2 $(du -h "$2"|cut -f1)"; }

encm() { ffmpeg -v error -y -i "$1" -an -vf "scale=-2:720,unsharp=5:5:0.6:5:5:0.0" \
  -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p \
  -g 4 -keyint_min 4 -sc_threshold 0 -movflags +faststart "$2" && echo "encm $2 $(du -h "$2"|cut -f1)"; }

for i in 1 2 3 4; do
  enc  "conn_$i.mp4" "$ASSETS/vid/conn$i.mp4"
  encm "conn_$i.mp4" "$ASSETS/vid/conn$i-m.mp4"
done

echo "=== SSIM SEAM GATE ==="
seam_ssim() { # fileA fileB
  ffmpeg -v error -y -sseof -0.05 -i "$1" -frames:v 1 "_sa.png"
  ffmpeg -v error -y -ss 0      -i "$2" -frames:v 1 "_sb.png"
  ffmpeg -v info -i "_sa.png" -i "_sb.png" -lavfi ssim -f null - 2>&1 \
    | grep -o 'All:[0-9.]*' | cut -d: -f2
}
check() { # fileA fileB label
  s=$(seam_ssim "$1" "$2")
  case $(awk -v s="${s:-0}" 'BEGIN{ if (s>=0.90) print "pass"; else if (s>=0.75) print "warn"; else print "fail" }') in
    pass) echo "PASS  $3  ssim=$s" ;;
    warn) echo "WARN  $3  ssim=$s (crossfade will mostly hide it - eyeball this seam)" ;;
    *)    echo "FAIL  $3  ssim=$s - endpoints are NOT the neighbours' frames; redo this connector" ;;
  esac
}
V="$ASSETS/vid"
check "$V/beige.mp4"    "$V/conn1.mp4"    "beige>conn1"
check "$V/conn1.mp4"    "$V/crashpad.mp4" "conn1>crashpad"
check "$V/crashpad.mp4" "$V/conn2.mp4"    "crashpad>conn2"
check "$V/conn2.mp4"    "$V/crash.mp4"    "conn2>crash"
check "$V/crash.mp4"    "$V/conn3.mp4"    "crash>conn3"
check "$V/conn3.mp4"    "$V/glowup.mp4"   "conn3>glowup"
check "$V/glowup.mp4"   "$V/conn4.mp4"    "glowup>conn4"
check "$V/conn4.mp4"    "$V/finale.mp4"   "conn4>finale"
echo "=== GATE DONE ==="
