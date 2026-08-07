/* Tap-through cinema engine — replaces scroll-scrubbing on the story pages.
   Scenes auto-play in sequence and crossfade into each other; where the config
   provides connector clips (the aerial flights that bridged scenes in the
   scroll version) they play between scenes as wordless transitions, so every
   cut lands on the frame-matched footage the world was built with. In video
   mode scenes advance on their own via crossfade — ArrowRight/Space step
   forward a scene at a time, and "Skip to end" jumps to the finale — while a
   stage tap is a passive gesture surface only, since accidental taps
   mid-video caused jittery skips. In the tap-through stills fallback
   (below), tapping the stage IS how you advance (connectors are skipped,
   not replayed); "Skip to end" always jumps to the finale, which holds its
   last frame and shows the explore links.
   Reuses the scrub engine's section config shape unchanged (clip/clipMobile/
   poster/posterMobile/still + eyebrow/title/body/tags/accent/explore,
   connectors/connectorsMobile); journey/scroll keys are ignored.
   Phone-class devices (screen short side <= 600 CSS px) get the -m tier.
   Autoplay refusal (iOS Low Power Mode) and prefers-reduced-motion fall back
   to a tap-through stills slideshow — the page never dead-ends. */
function mountTapWorld(container, config) {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var phone = Math.min(screen.width, screen.height) <= 600;
  var S = config.sections || [];
  var N = S.length;
  if (!N) return;

  function clipOf(s)   { return (phone && s.clipMobile) ? s.clipMobile : s.clip; }
  function posterOf(s) { return (phone && s.posterMobile) ? s.posterMobile : (s.poster || s.still); }

  // Optional pacing: config.playbackRate (e.g. 1.15) speeds every clip up.
  // Optional per-scene pacing: section.rate (e.g. 1.10) multiplies RATE for
  // that scene only — connectors always play at the plain RATE.
  var RATE = config.playbackRate || 1;

  // ---- playlist: scene, connector, scene, connector, … scene -------------
  var CONNS = (phone && config.connectorsMobile && config.connectorsMobile.length) ?
              config.connectorsMobile : (config.connectors || []);
  var PL = [];
  S.forEach(function (s, k) {
    PL.push({ kind: "scene", si: k });
    if (k < N - 1 && CONNS[k]) PL.push({ kind: "conn", src: CONNS[k] });
  });
  var LAST = PL.length - 1;   // always the finale scene

  function nextSceneAt(p) { for (var q = p + 1; q < PL.length; q++) if (PL[q].kind === "scene") return q; return LAST; }
  function prevSceneAt(p) { for (var q = p - 1; q >= 0; q--) if (PL[q].kind === "scene") return q; return -1; }
  function srcOf(item)    { return item.kind === "scene" ? clipOf(S[item.si]) : item.src; }
  function posterFor(item){ return item.kind === "scene" ? (posterOf(S[item.si]) || "") : ""; }

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
    // Resume pill: the runtime-stills (Low Power Mode) recovery affordance —
    // ghost-pill recipe like .tw-skip, pinned bottom-center clear of the card.
    ".tw-resume{position:absolute;left:50%;bottom:max(3.5vh,env(safe-area-inset-bottom));z-index:6;",
    "  transform:translateX(-50%) translateY(8px);opacity:0;pointer-events:none;",
    "  border:1px solid rgba(255,255,255,.45);background:rgba(18,27,52,.62);color:#FFF9EE;cursor:pointer;",
    "  font-family:'Baloo 2',ui-rounded,system-ui,sans-serif;font-weight:700;font-size:12px;",
    "  letter-spacing:.12em;text-transform:uppercase;padding:11px 20px;border-radius:999px;",
    "  -webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);transition:opacity .3s ease,transform .3s ease;}",
    ".tw-resume.is-on{opacity:1;pointer-events:auto;transform:translateX(-50%) translateY(0);}",
    "@media (prefers-reduced-motion:reduce){.tw video,.tw .tw-still,.tw-card,.tw-resume{transition:none;}}"
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

  var vids = [document.createElement("video"), document.createElement("video")];
  vids.forEach(function (v) {
    // muted as BOTH property and attribute: the property is what play() checks,
    // the attribute is what some Android WebView autoplay heuristics look at.
    v.muted = true; v.setAttribute("muted", "");
    v.playsInline = true; v.setAttribute("playsinline", "");
    v.preload = "auto";
    v.defaultPlaybackRate = RATE;
    // No cast button / PiP hijack surfaces over the story (Android Chrome
    // offers both on bare <video> elements).
    try { v.disableRemotePlayback = true; } catch (e) {}
    v.setAttribute("disableremoteplayback", "");
    try { v.disablePictureInPicture = true; } catch (e) {}
    stage.appendChild(v);
  });
  var still = el("img", "tw-still");
  still.alt = "";
  stage.appendChild(still);

  var tap = el("button", "tw-tap");
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
  // Runtime-stills bookkeeping: stills mode entered because the OS refused
  // play() at runtime (Low Power Mode, battery savers) is a TEMPORARY device
  // state — recoverable, never a teardown. runtimeStills marks that case
  // (never set for prefers-reduced-motion visitors); resumeArmedIdx /
  // resumeFailedIdx let taps alternate resume-attempt → advance so a device
  // that keeps refusing still steps through the slideshow instead of jamming
  // on one scene.
  var runtimeStills = false, resumeArmedIdx = -1, resumeFailedIdx = -1;

  // Accessibility: the tap catcher's nextLabel only means something in
  // stills mode, where tapping the stage is the sole way through the
  // slideshow (see the tap click handler near the bottom of this file). In
  // video mode the catcher is a passive gesture surface with no advance
  // action, so it's hidden from assistive tech and pulled out of the tab
  // order instead of announcing a "Next scene" affordance that no longer
  // does anything. Called once at init (covers reduce:true booting straight
  // into stills mode) and on every stillsMode transition — enterStillsMode()
  // and the start overlay's `stillsMode = reduce` reset.
  function updateTapA11y() {
    if (stillsMode) {
      tap.setAttribute("aria-label", config.nextLabel || "Next scene");
      tap.removeAttribute("aria-hidden");
      tap.removeAttribute("tabindex");
    } else {
      tap.removeAttribute("aria-label");
      tap.setAttribute("aria-hidden", "true");
      tap.setAttribute("tabindex", "-1");
    }
  }
  updateTapA11y();

  function showCard(s) {
    cEyebrow.textContent = s.eyebrow || "";
    cTitle.textContent = s.title || "";
    cBody.textContent = s.body || "";
    card.style.setProperty("--tw-accent", s.accent || "#FFC93C");
    card.classList.remove("is-on");
    void card.offsetWidth;
    card.classList.add("is-on");
  }

  function hideCard() { card.classList.remove("is-on"); }

  function showExplore(s) {
    hideCard();               // the card and the buttons share the bottom of
    explore.innerHTML = "";   // the screen — never show both at once
    hideResumePill();         // ...nor the pill under the explore stack
    var ex = s.explore;
    if (!ex || !ex.links) return;
    ex.links.forEach(function (l) {
      var a = document.createElement("a");
      a.href = l.href; a.textContent = l.label;
      if (l.href === "#top") {
        a.addEventListener("click", function (e) {
          e.preventDefault();
          explore.classList.remove("is-on");
          // Restart the theme in sync with the journey restart below. This
          // engine otherwise has no music coupling at all — kept minimal and
          // self-contained: no-ops if music.js never loaded (window.swMusic
          // absent), if a cached music.js pre-dates replay(), or if the
          // visitor explicitly muted earlier (same sessionStorage key
          // music.js writes) — mirrors the guard used in
          // adult/tap-engine.js's "Play it again" handler.
          try {
            if (window.swMusic && typeof window.swMusic.replay === "function") {
              var muted = null;
              try { muted = sessionStorage.getItem("sw-music-on"); } catch (e2) {}
              if (muted !== "0") window.swMusic.replay();
            }
          } catch (err) {}
          go(0);
        });
      }
      explore.appendChild(a);
    });
    explore.classList.add("is-on");
  }

  function markDot(si) {
    dotEls.forEach(function (d, k) { d.className = k === si ? "is-here" : ""; });
  }

  function enterStillsMode(runtime) {
    if (stillsMode) return;
    stillsMode = true;
    runtimeStills = !!runtime && !reduce;
    updateTapA11y();
    vids.forEach(function (v) { try { v.pause(); } catch (e) {} v.classList.remove("is-on"); });
    if (idx >= 0) {
      var item = PL[idx];
      renderStill(S[item.kind === "scene" ? item.si : nextSceneIdxOfConn(idx)]);
    }
    if (runtimeStills && started) showResumePill();
  }

  // Resume pill: the visible affordance for the runtime-stills state (mirrors
  // scrub-engine's motion pill). The actual retry runs in the tap handler /
  // pill click — a real user activation, which is exactly what LPM-class
  // playback policies accept.
  var resumePill = null;
  function showResumePill() {
    if (!resumePill) {
      resumePill = el("button", "tw-resume");
      resumePill.type = "button";
      resumePill.textContent = config.resumeLabel || "Tap to continue the story";
      resumePill.addEventListener("click", function () { started = true; gestureResume(); });
      stage.appendChild(resumePill);
    }
    resumePill.classList.add("is-on");
  }
  function hideResumePill() { if (resumePill) resumePill.classList.remove("is-on"); }

  // In-gesture video retry from runtime stills: flip back to video mode and
  // re-run the CURRENT item, so play() executes inside the user's tap. If the
  // OS refuses again, go()'s catch drops us straight back to stills (pill
  // re-shown, resumeFailedIdx recorded) — this can never dead-end.
  function gestureResume() {
    if (!stillsMode || !runtimeStills || reduce) return;
    stillsMode = false; runtimeStills = false;
    updateTapA11y();
    hideResumePill();
    still.classList.remove("is-on");
    var at = idx < 0 ? 0 : idx;
    resumeArmedIdx = at;
    idx = -1; prepared = -1;
    go(at);
  }

  function nextSceneIdxOfConn(p) { var q = nextSceneAt(p); return PL[q].si; }

  function renderStill(s) {
    still.src = s.still || posterOf(s);
    still.classList.add("is-on");
  }

  // The inactive player buffers the NEXT playlist item while the current one
  // plays; a transition is: play the already-loaded clip, wait for its FIRST
  // PAINTED FRAME, then crossfade. (Fading on play()'s promise alone flashes
  // poster/black — playback can begin before a frame is decoded.)
  var prepared = -1;
  function prepare(p) {
    if (stillsMode || p < 0 || p > LAST || prepared === p) return;
    var v = vids[1 - active];
    v.src = srcOf(PL[p]);
    v.poster = posterFor(PL[p]);
    v.load();
    prepared = p;
  }

  function onFirstFrame(v, fn) {
    if (v.requestVideoFrameCallback) v.requestVideoFrameCallback(fn);
    else v.addEventListener("playing", fn, { once: true });
  }

  function go(p) {
    if (p < 0 || p > LAST || p === idx) { if (p > LAST) finish(); return; }
    idx = p;
    var item = PL[p];
    var scene = item.kind === "scene" ? S[item.si] : null;

    explore.classList.remove("is-on");
    if (scene) { markDot(item.si); showCard(scene); }
    else hideCard();
    // Page hook: fires on every SCENE entry, video and stills mode alike
    // (config.onScene(sceneIndex)). Used to start the theme music at scene 2 —
    // the handler latches itself, so re-entries (replay, resume) are its call.
    if (scene && config.onScene) { try { config.onScene(item.si); } catch (e) {} }

    if (stillsMode) {
      if (!scene) { go(nextSceneAt(p)); return; }   // stills skip connectors
      renderStill(scene);
      if (p === LAST) showExplore(scene);
      return;
    }

    var nextV = vids[1 - active], curV = vids[active];
    if (prepared !== p) {
      nextV.src = srcOf(item);
      nextV.poster = posterFor(item);
      nextV.load();
      prepared = p;
    }
    try { if (nextV.currentTime > 0.05) nextV.currentTime = 0; } catch (e) {}

    var swapped = false;
    function swap() {
      if (swapped || idx !== p) return;
      swapped = true;
      active = 1 - active;
      prepared = -1;
      // rVFC can fire for a PAUSED first frame (poster paint) — only treat a
      // swap as "video works again" when we're actually in video mode.
      if (!stillsMode) {
        resumeArmedIdx = -1; resumeFailedIdx = -1;
        still.classList.remove("is-on");           // clear any stall-watchdog still
      }
      nextV.classList.add("is-on");
      curV.classList.remove("is-on");
      // let the crossfade finish before parking the old player and handing it
      // the following item to buffer (setting src earlier would black out the
      // outgoing side of the fade)
      setTimeout(function () {
        try { curV.pause(); } catch (e) {}
        // Kick the NEXT item's download only once the clip ON STAGE can play
        // through (or is well underway): two multi-MB downloads sharing one
        // phone connection was starving the active clip mid-scene.
        whenSafeToPrefetch(nextV, function () { if (idx === p) prepare(p + 1); });
      }, 700);
    }

    try { nextV.playbackRate = RATE * ((scene && scene.rate) || 1); } catch (e) {}
    var pr;
    try { pr = nextV.play(); } catch (e) { enterStillsMode(true); go(p); return; }
    onFirstFrame(nextV, swap);
    if (pr && pr.then) {
      pr.catch(function (err) {
        // A load()/pause() landing on an element whose play() is still pending
        // rejects that play() with AbortError — a benign teardown race (skip
        // tap or rapid advance mid-start), NOT an OS block. Treating it as one
        // was permanently stranding the journey on stills (scrub-engine has
        // filtered this same race all along).
        if (err && err.name === "AbortError") return;
        if (idx !== p) return;   // stale: the journey already moved on
        if (p === resumeArmedIdx) { resumeArmedIdx = -1; resumeFailedIdx = p; }
        // OS refused playback (Low Power Mode / policy): stills + tap-through,
        // recoverably — the resume pill / next tap retries in-gesture.
        enterStillsMode(true);
        if (started) showResumePill();   // covers re-entry while already in stills
        var s = scene || S[nextSceneIdxOfConn(p)];
        renderStill(s);
        if (p === LAST) showExplore(s);
        if (!started) startOverlay();
      });
    }
    nextV.onended = function () {
      if (idx !== p) return;
      if (p === LAST) finish(); else go(p + 1);
    };

    // Stall watchdog: a starving connection must never freeze the show with
    // no exit (there was NO recovery path at all before — a mid-clip network
    // stall held a half-frame forever). No playback progress for 6s → put the
    // scene's still up (real artwork + copy, not a frozen frame) while the
    // decoder keeps trying; if progress resumes the still comes straight back
    // down. 12s more with nothing, or a fatal media error → advance: later
    // items may be cached/buffered, and the finale must stay reachable.
    var lastT = -1, lastMove = performance.now(), stallStill = false;
    function stallNext() {
      if (idx !== p) return;
      if (p === LAST) { renderStill(S[N - 1]); showExplore(S[N - 1]); return; }
      go(p + 1);
    }
    var wd = setInterval(function () {
      if (idx !== p || stillsMode || nextV.ended) { clearInterval(wd); return; }
      var t = nextV.currentTime;
      if (t !== lastT) {
        lastT = t; lastMove = performance.now();
        if (stallStill) { stallStill = false; still.classList.remove("is-on"); }
        return;
      }
      var dead = performance.now() - lastMove;
      if (dead > 6000 && !stallStill) {
        stallStill = true;
        renderStill(scene || S[nextSceneIdxOfConn(p)]);
      } else if (dead > 18000) {
        clearInterval(wd);
        stallNext();
      }
    }, 500);
    nextV.onerror = function () {
      if (idx !== p) return;
      clearInterval(wd);
      renderStill(scene || S[nextSceneIdxOfConn(p)]);
      setTimeout(stallNext, 1200);
    };
  }

  // Prefetch gate for swap(): fire cb once the active clip is safe to share
  // bandwidth with — buffered to the end (readyState 4) or 60% played.
  function whenSafeToPrefetch(v, cb) {
    if (v.readyState >= 4) { cb(); return; }
    var done = false;
    function fire() {
      if (done) return; done = true;
      v.removeEventListener("canplaythrough", fire);
      v.removeEventListener("timeupdate", part);
      cb();
    }
    function part() {
      if (v.duration && v.currentTime > v.duration * 0.6) fire();
    }
    v.addEventListener("canplaythrough", fire);
    v.addEventListener("timeupdate", part);
  }

  function finish() {
    var s = S[N - 1];
    if (idx !== LAST) { go(LAST); return; }
    showExplore(s);
  }

  // First-play overlay for the autoplay-refused path: one real user gesture.
  var startBtn = null;
  function startOverlay() {
    if (startBtn) return;
    startBtn = el("button", "tw-start");
    startBtn.type = "button";
    startBtn.textContent = config.startLabel || "Tap to play the story";
    startBtn.addEventListener("click", function () {
      startBtn.remove(); startBtn = null; started = true;
      stillsMode = reduce;
      runtimeStills = false; resumeFailedIdx = -1;
      hideResumePill();
      updateTapA11y();
      still.classList.remove("is-on");
      var at = idx < 0 ? 0 : idx;
      idx = -1; prepared = -1; go(at);
    });
    stage.appendChild(startBtn);
  }

  // Advance to the next scene (connectors are skipped, not replayed), or
  // finish() at the finale. Shared by stills-mode tap and ArrowRight/Space —
  // extracted so keyboard can drive it directly instead of proxying through
  // tap.click(), since tap.click() no longer advances in video mode (see
  // below) but deliberate keypresses should still step scenes there.
  function advance() {
    if (idx >= LAST) { finish(); return; }
    go(nextSceneAt(idx));
  }

  // ---- input ---------------------------------------------------------------
  // Tap only advances in stills mode (the autoplay-refused / reduced-motion
  // fallback, where it's the sole way through the slideshow — "the page
  // never dead-ends"). In video mode the full-stage tap catcher stays in the
  // DOM as a passive gesture surface but no longer advances scenes —
  // accidental taps during video playback were causing jittery skips/pauses.
  tap.addEventListener("click", function () {
    started = true;
    if (stillsMode) {
      // Runtime stills (LPM-class refusal): this tap is a fresh user
      // activation — use it to try video again for the scene on stage. If the
      // last attempt at THIS scene already failed, advance the slideshow
      // instead, so a device that keeps refusing still moves forward (taps
      // alternate retry → advance → retry …).
      if (runtimeStills && !reduce && idx !== resumeFailedIdx) { gestureResume(); return; }
      advance();
    }
  });
  skip.addEventListener("click", function () {
    started = true;
    if (idx === LAST) { finish(); return; }
    go(LAST);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight" || e.key === " ") { e.preventDefault(); advance(); }
    if (e.key === "ArrowLeft") {
      var q = prevSceneAt(idx);
      if (q >= 0) { e.preventDefault(); go(q); }
    }
  });

  // ---- boot --------------------------------------------------------------
  go(0);
}
