// ==== CONFETTI (verbatim, saved from the pre-video index.html, lines 618-697) ====
// Depends on: `reduced` (prefers-reduced-motion match) and the #confetti <canvas>
// element already existing in the DOM. `isMobile` is included here so the
// snippet is self-contained wherever it's pasted.
const isMobile = window.matchMedia("(max-width: 760px), (pointer: coarse)").matches;

// ---- Confetti --------------------------------------------------------
const confettiCanvas = document.getElementById("confetti");
const cctx = confettiCanvas.getContext("2d");
let cdpr = Math.min(window.devicePixelRatio, 2);
function sizeConfetti() {
  cdpr = Math.min(window.devicePixelRatio, 2);
  confettiCanvas.width = Math.floor(window.innerWidth * cdpr);
  confettiCanvas.height = Math.floor(window.innerHeight * cdpr);
  confettiCanvas.style.width = window.innerWidth + "px";
  confettiCanvas.style.height = window.innerHeight + "px";
}
sizeConfetti();

const CONFETTI_COLORS = ["#f973ab", "#ff9ec7", "#e9b949", "#f4d06f", "#8fdcc0", "#c9a7f5", "#fff6fb", "#a23a2e"];
let confetti = [];
let confettiRAF = 0, confettiLast = 0;

function fireConfetti() {
  const cw = window.innerWidth, chh = window.innerHeight;
  const ox = cw * 0.5, oy = chh * 0.5;
  const n = reduced ? 36 : (isMobile ? 90 : 170);
  const vscale = reduced ? 0.5 : 1;
  for (let i = 0; i < n; i++) {
    const ang = -Math.PI / 2 + (Math.random() - 0.5) * Math.PI * 1.15;
    const sp = (reduced ? 180 : 520) + Math.random() * (reduced ? 150 : 760);
    confetti.push({
      x: ox + (Math.random() - 0.5) * 60,
      y: oy + (Math.random() - 0.5) * 30,
      vx: Math.cos(ang) * sp * vscale,
      vy: Math.sin(ang) * sp * vscale,
      w: 6 + Math.random() * 6,
      h: 9 + Math.random() * 9,
      rot: Math.random() * Math.PI,
      vr: (Math.random() - 0.5) * 12,
      tilt: Math.random() * Math.PI * 2,
      vt: 4 + Math.random() * 6,
      sway: 1 + Math.random() * 2,
      phase: Math.random() * Math.PI * 2,
      color: CONFETTI_COLORS[(Math.random() * CONFETTI_COLORS.length) | 0],
      life: 0,
      max: (reduced ? 1.6 : 2.6) + Math.random() * 1.2,
      round: Math.random() < 0.18,
    });
  }
  if (!confettiRAF) { confettiLast = performance.now(); confettiRAF = requestAnimationFrame(confettiStep); }
}

function confettiStep(now) {
  let dt = (now - confettiLast) / 1000; confettiLast = now;
  if (dt > 0.05) dt = 0.05;
  const chh = window.innerHeight;
  const grav = reduced ? 600 : 1500;
  cctx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
  cctx.save();
  cctx.scale(cdpr, cdpr);
  for (let i = confetti.length - 1; i >= 0; i--) {
    const c = confetti[i];
    c.life += dt;
    c.vy += grav * dt;
    c.vx *= 0.99;
    c.x += c.vx * dt + Math.sin(c.life * c.sway + c.phase) * 0.6;
    c.y += c.vy * dt;
    c.rot += c.vr * dt;
    c.tilt += c.vt * dt;
    if (c.life > c.max || c.y > chh + 60) { confetti.splice(i, 1); continue; }
    const fade = c.life > c.max - 0.8 ? Math.max(0, (c.max - c.life) / 0.8) : 1;
    cctx.save();
    cctx.translate(c.x, c.y);
    cctx.rotate(c.rot);
    cctx.scale(1, Math.cos(c.tilt));
    cctx.globalAlpha = fade;
    cctx.fillStyle = c.color;
    if (c.round) { cctx.beginPath(); cctx.arc(0, 0, c.w * 0.5, 0, Math.PI * 2); cctx.fill(); }
    else { cctx.fillRect(-c.w / 2, -c.h / 2, c.w, c.h); }
    cctx.restore();
  }
  cctx.restore();
  if (confetti.length) { confettiRAF = requestAnimationFrame(confettiStep); }
  else { cctx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height); confettiRAF = 0; }
}
