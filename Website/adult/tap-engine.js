/* Tap-through cinema engine — replaces scroll-scrubbing on the story pages.
   Scenes auto-play in sequence (muted), each crossfading into the next when its
   clip ends. Tap anywhere skips to the next scene; "Skip to end" jumps to the
   finale. The last scene holds its final frame and shows the explore links.
   Reuses the exact section config shape the scrub engine used (clip/clipMobile/
   poster/posterMobile/still + eyebrow/title/body/tags/accent/explore), so page
   configs carry over unchanged; journey/scroll keys are simply ignored.
   Phone-class devices (screen short side <= 600 CSS px) get the -m clip tier.
   Autoplay refusal (iOS Low Power Mode) and prefers-reduced-motion fall back to
   a tap-through stills slideshow — the page never dead-ends. */
function mountTapWorld(container, config) {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var phone = Math.min(screen.width, screen.height) <= 600;
  var S = config.sections || [];
  var N = S.length;
  if (!N) return;

  function clipOf(s)   { return (phone && s.clipMobile) ? s.clipMobile : s.clip; }
  function posterOf(s) { return (phone && s.posterMobile) ? s.posterMobile : (s.poster || s.still); }

  // ---- CSS (self-contained, injected) -----------------------------------
  var css = [
    ".tw{position:fixed;inset:0;overflow:hidden;background:var(--sw-bg,#1D2B50);}",
    ".tw video,.tw .tw-still{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;",
    "  opacity:0;transition:opacity .5s ease;}",
    ".tw video.is-on,.tw .tw-still.is-on{opacity:1;}",
    ".tw-tap{position:absolute;inset:0;z-index:4;background:none;border:0;padding:0;cursor:pointer;",
    "  -webkit-tap-highlight-color:transparent;}",
    ".tw-card{position:absolute;left:50%;bottom:max(9vh,env(safe-area-inset-bottom));z-index:5;",
    "  transform:translateX(-50%) translateY(12px);width:min(88vw,540px);text-align:center;",
    "  pointer-events:none;opacity:0;transition:opacity .6s ease,transform .6s ease;",
    "  font-family:'Baloo 2',ui-rounded,'SF Pro Rounded','Segoe UI',system-ui,sans-serif;",
    "  color:#FFF9EE;text-shadow:0 2px 14px rgba(0,0,0,.55);}",
    ".tw-card.is-on{opacity:1;transform:translateX(-50%) translateY(0);}",
    ".tw-card__eyebrow{font-size:12px;font-weight:700;letter-spacing:.24em;text-transform:uppercase;",
    "  color:var(--tw-accent,#FFC93C);margin:0 0 6px;}",
    ".tw-card__title{font-size:clamp(24px,5.4vw,40px);font-weight:800;line-height:1.08;margin:0;}",
    ".tw-card__body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,system-ui,sans-serif;",
    "  font-size:clamp(14px,1.7vw,17px);line-height:1.5;margin:10px auto 0;max-width:46ch;opacity:.92;}",
    ".tw-dots{position:absolute;top:calc(56px + 14px);left:50%;transform:translateX(-50%);z-index:5;",
    "  display:flex;gap:7px;pointer-events:none;}",
    ".tw-dots i{width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,.35);transition:background .3s,transform .3s;}",
    ".tw-dots i.is-here{background:#FFC93C;transform:scale(1.25);}",
    ".tw-skip{position:absolute;top:calc(56px + 10px);right:max(14px,env(safe-area-inset-right));z-index:6;",
    "  border:1px solid rgba(255,255,255,.4);background:rgba(18,27,52,.45);color:#FFF9EE;cursor:pointer;",
    "  font-family:'Baloo 2',ui-rounded,system-ui,sans-serif;font-weight:700;font-size:12px;",
    "  letter-spacing:.14em;text-transform:uppercase;padding:9px 16px;border-radius:999px;",
    "  -webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);}",
    ".tw-skip:hover{background:rgba(18,27,52,.7);}",
    ".tw-skip:focus-visible{outline:3px solid #FFC93C;outline-offset:2px;}",
    ".tw-start{position:absolute;inset:0;z-index:7;display:flex;align-items:center;justify-content:center;",
    "  background:rgba(18,27,52,.35);border:0;cursor:pointer;color:#FFF9EE;",
    "  font-family:'Baloo 2',ui-rounded,system-ui,sans-serif;font-weight:800;font-size:clamp(18px,3vw,24px);",
    "  letter-spacing:.06em;text-shadow:0 2px 14px rgba(0,0,0,.6);}",
    ".tw-explore{position:absolute;left:50%;bottom:max(7vh,env(safe-area-inset-bottom));z-index:6;",
    "  transform:translateX(-50%);width:min(88vw,420px);display:none;flex-direction:column;gap:10px;}",
    ".tw-explore.is-on{display:flex;}",
    ".tw-explore a{display:block;text-align:center;text-decoration:none;color:#1D2B50;",
    "  background:linear-gradient(180deg,#FFFDF6,#F1E3BE);border:1px solid rgba(184,134,46,.55);",
    "  font-family:'Baloo 2',ui-rounded,system-ui,sans-serif;font-weight:700;font-size:15px;",
    "  letter-spacing:.06em;padding:14px 18px;border-radius:13px;",
    "  box-shadow:0 6px 18px rgba(0,0,0,.3);}",
    ".tw-explore a:active{transform:translateY(1px);}",
    "@media (prefers-reduced-motion:reduce){.tw video,.tw .tw-still,.tw-card{transition:none;}}"
  ].join("\n");
  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  document.documentElement.style.overflow = "hidden";
  document.body.style.overflow = "hidden";

  // ---- DOM ---------------------------------------------------------------
  function el(tag, cls) { var n = document.createElement(tag); if (cls) n.className = cls; return n; }

  var stage = el("div", "tw");
  container.innerHTML = "";
  container.appendChild(stage);

  // Two stacked players so scene N+1 can load behind scene N and crossfade in.
  var vids = [document.createElement("video"), document.createElement("video")];
  vids.forEach(function (v) {
    v.muted = true; v.playsInline = true; v.setAttribute("playsinline", "");
    v.preload = "auto";
    stage.appendChild(v);
  });
  var still = el("img", "tw-still");   // stills fallback (reduced motion / LPM)
  still.alt = "";
  stage.appendChild(still);

  var tap = el("button", "tw-tap");
  tap.setAttribute("aria-label", "Next scene");
  stage.appendChild(tap);

  var card = el("div", "tw-card");
  var cEyebrow = el("p", "tw-card__eyebrow");
  var cTitle = el("h2", "tw-card__title");
  var cBody = el("p", "tw-card__body");
  card.appendChild(cEyebrow); card.appendChild(cTitle); card.appendChild(cBody);
  stage.appendChild(card);

  var dots = el("div", "tw-dots");
  var dotEls = [];
  for (var i = 0; i < N; i++) { var d = document.createElement("i"); dots.appendChild(d); dotEls.push(d); }
  stage.appendChild(dots);

  var skip = el("button", "tw-skip");
  skip.type = "button";
  skip.textContent = config.skipLabel || "Skip to end »";
  stage.appendChild(skip);

  var explore = el("nav", "tw-explore");
  stage.appendChild(explore);

  // ---- state -------------------------------------------------------------
  var idx = -1, active = 0, stillsMode = reduce, started = false;

  function showCard(s) {
    cEyebrow.textContent = s.eyebrow || "";
    cTitle.textContent = s.title || "";
    cBody.textContent = s.body || "";
    card.style.setProperty("--tw-accent", s.accent || "#FFC93C");
    card.classList.remove("is-on");
    void card.offsetWidth;               // restart the entrance transition
    card.classList.add("is-on");
  }

  function showExplore(s) {
    explore.innerHTML = "";
    var ex = s.explore;
    if (!ex || !ex.links) return;
    ex.links.forEach(function (l) {
      var a = document.createElement("a");
      a.href = l.href; a.textContent = l.label;
      if (l.href === "#top") {
        a.addEventListener("click", function (e) { e.preventDefault(); explore.classList.remove("is-on"); go(0); });
      }
      explore.appendChild(a);
    });
    explore.classList.add("is-on");
  }

  function markDot(i) {
    dotEls.forEach(function (d, k) { d.className = k === i ? "is-here" : ""; });
  }

  function enterStillsMode() {
    if (stillsMode) return;
    stillsMode = true;
    vids.forEach(function (v) { try { v.pause(); } catch (e) {} v.classList.remove("is-on"); });
    if (idx >= 0) renderStill(S[idx]);
  }

  function renderStill(s) {
    still.src = s.still || posterOf(s);
    still.classList.add("is-on");
  }

  function go(i) {
    if (i < 0 || i >= N || i === idx) { if (i >= N) finish(); return; }
    idx = i;
    var s = S[i];
    markDot(i);
    explore.classList.remove("is-on");
    showCard(s);
    if (i === N - 1) showExploreSoon = true; else showExploreSoon = false;

    if (stillsMode) {
      renderStill(s);
      if (i === N - 1) showExplore(s);
      return;
    }

    var nextV = vids[1 - active], curV = vids[active];
    nextV.src = clipOf(s);
    nextV.poster = posterOf(s) || "";
    try { nextV.currentTime = 0; } catch (e) {}
    var p;
    try { p = nextV.play(); } catch (e) { enterStillsMode(); go(i); return; }
    if (p && p.then) {
      p.then(function () {
        active = 1 - active;
        nextV.classList.add("is-on");
        curV.classList.remove("is-on");
        setTimeout(function () { try { curV.pause(); } catch (e) {} }, 600);
      }).catch(function () {
        // OS refused playback (Low Power Mode / policy): stills + tap-through.
        enterStillsMode(); renderStill(s);
        if (i === N - 1) showExplore(s);
        if (!started) startOverlay();
      });
    }
    nextV.onended = function () {
      if (idx !== i) return;
      if (i === N - 1) finish(); else go(i + 1);
    };
  }

  function finish() {
    // hold the finale's last frame and put the explore links up
    var s = S[N - 1];
    if (idx !== N - 1) { go(N - 1); return; }
    showExplore(s);
  }

  var showExploreSoon = false;

  // First-play overlay for the autoplay-refused path: one real user gesture.
  var startBtn = null;
  function startOverlay() {
    if (startBtn) return;
    startBtn = el("button", "tw-start");
    startBtn.type = "button";
    startBtn.textContent = config.startLabel || "Tap to play the story";
    startBtn.addEventListener("click", function () {
      startBtn.remove(); startBtn = null; started = true;
      stillsMode = reduce;               // retry real playback unless reduced-motion
      still.classList.remove("is-on");
      var at = idx < 0 ? 0 : idx;
      idx = -1; go(at);
    });
    stage.appendChild(startBtn);
  }

  // ---- input -------------------------------------------------------------
  tap.addEventListener("click", function () {
    started = true;
    if (idx >= N - 1) { finish(); return; }
    go(idx + 1);
  });
  skip.addEventListener("click", function () {
    started = true;
    if (stillsMode) { go(N - 1); return; }
    // jump straight into the finale clip
    if (idx === N - 1) { finish(); return; }
    go(N - 1);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight" || e.key === " ") { e.preventDefault(); tap.click(); }
    if (e.key === "ArrowLeft" && idx > 0) { e.preventDefault(); go(idx - 1); }
  });

  // ---- boot --------------------------------------------------------------
  if (reduce) {
    stillsMode = true;
    go(0);
    return;
  }
  go(0);
}
