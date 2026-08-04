/* Tap-through cinema engine — replaces scroll-scrubbing on the story pages.
   Scenes auto-play in sequence and crossfade into each other; where the config
   provides connector clips (the aerial flights that bridged scenes in the
   scroll version) they play between scenes as wordless transitions, so every
   cut lands on the frame-matched footage the world was built with. Tap skips
   to the next scene (connectors are skipped, not replayed); "Skip to end"
   jumps to the finale, which holds its last frame and shows the explore links.
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

  // Optional pacing: config.playbackRate (e.g. 1.15) is the base rate every
  // clip plays at. Individual scenes can further multiply it via `rate`
  // (e.g. rate:1.3 on a scene plays that clip at RATE*1.3); connectors
  // always use the plain base RATE. go() computes and applies the effective
  // per-item rate on every play() — see `effRate` there.
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
    "  opacity:0;transition:opacity .5s ease;will-change:opacity;}",
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
    // Scrim: sits behind the explore stack (above the video, below the links)
    // so the finale's busy night-sky frame doesn't fight the buttons for
    // contrast. Non-interactive; only shown while .tw-explore is shown.
    ".tw-scrim{position:absolute;inset:0;z-index:5;pointer-events:none;",
    "  background:linear-gradient(180deg,transparent,rgba(18,27,52,.78) 55%);",
    "  opacity:0;transition:opacity .6s ease;}",
    ".tw-scrim.is-on{opacity:1;}",
    ".tw-skip.is-hidden{display:none;}",
    ".tw-explore{position:absolute;left:50%;bottom:max(7vh,env(safe-area-inset-bottom));z-index:6;",
    "  transform:translateX(-50%);width:min(92vw,560px);display:none;flex-direction:column;",
    "  align-items:center;gap:14px;}",
    ".tw-explore.is-on{display:flex;}",
    // The 4 nav links (Hire/Meet/Store/Mission) sit in a 2x2 grid — same
    // cream-gradient card style as before, just half-width now.
    ".tw-explore__grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;width:100%;}",
    ".tw-explore__grid a{display:flex;align-items:center;justify-content:center;text-align:center;",
    "  text-decoration:none;color:#1D2B50;line-height:1.25;",
    "  background:linear-gradient(180deg,#FFFDF6,#F1E3BE);border:1px solid rgba(184,134,46,.55);",
    "  font-family:'Baloo 2',ui-rounded,system-ui,sans-serif;font-weight:700;font-size:14px;",
    "  letter-spacing:.04em;padding:13px 10px;border-radius:13px;",
    "  box-shadow:0 6px 18px rgba(0,0,0,.3);}",
    ".tw-explore__grid a:active{transform:translateY(1px);}",
    // "Play it again" reads as a lighter, secondary action below the grid —
    // mirrors .tw-skip's ghost-pill recipe (dark translucent + blur) instead
    // of the nav links' solid cream cards.
    ".tw-explore__replay{display:inline-block;text-align:center;text-decoration:none;color:#FFF9EE;",
    "  background:rgba(18,27,52,.45);border:1px solid rgba(255,255,255,.4);cursor:pointer;",
    "  font-family:'Baloo 2',ui-rounded,system-ui,sans-serif;font-weight:700;font-size:13px;",
    "  letter-spacing:.12em;text-transform:uppercase;padding:10px 22px;border-radius:999px;",
    "  -webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);}",
    ".tw-explore__replay:hover{background:rgba(18,27,52,.7);}",
    ".tw-explore__replay:active{transform:translateY(1px);}",
    "@media (prefers-reduced-motion:reduce){.tw video,.tw .tw-still,.tw-card,.tw-scrim{transition:none;}}"
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
    v.muted = true; v.setAttribute("muted", "");
    v.playsInline = true; v.setAttribute("playsinline", "");
    v.preload = "auto";
    v.defaultPlaybackRate = RATE;   // base rate only; go() sets the actual
                                     // per-item rate (RATE * (scene.rate||1))
                                     // on nextV.playbackRate before each play()
    stage.appendChild(v);
  });
  var still = el("img", "tw-still");
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

  var scrim = el("div", "tw-scrim");
  stage.appendChild(scrim);

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
    void card.offsetWidth;
    card.classList.add("is-on");
  }

  function hideCard() { card.classList.remove("is-on"); }

  // Clears the explore stack + its scrim and restores the skip control.
  // Called on every go() (a no-op unless the finale was showing) and from
  // the "Play it again" handler before it replays.
  function hideExplore() {
    explore.classList.remove("is-on");
    scrim.classList.remove("is-on");
    skip.classList.remove("is-hidden");
  }

  function showExplore(s) {
    hideCard();               // the card and the buttons share the bottom of
    explore.innerHTML = "";   // the screen — never show both at once
    var ex = s.explore;
    if (!ex || !ex.links) return;
    // 4 nav links render in a 2x2 grid; "Play it again" (href #top) renders
    // as a lighter ghost pill below it — generalized so any non-#top link
    // lands in the grid regardless of position/count in config.
    var grid = el("div", "tw-explore__grid");
    explore.appendChild(grid);
    ex.links.forEach(function (l) {
      var a = document.createElement("a");
      a.href = l.href; a.textContent = l.label;
      if (l.href === "#top") {
        a.className = "tw-explore__replay";
        a.addEventListener("click", function (e) { e.preventDefault(); hideExplore(); go(0); });
        explore.appendChild(a);
      } else {
        grid.appendChild(a);
      }
    });
    explore.classList.add("is-on");
    scrim.classList.add("is-on");
    skip.classList.add("is-hidden");
  }

  function markDot(si) {
    dotEls.forEach(function (d, k) { d.className = k === si ? "is-here" : ""; });
  }

  function enterStillsMode() {
    if (stillsMode) return;
    stillsMode = true;
    vids.forEach(function (v) { try { v.pause(); } catch (e) {} v.classList.remove("is-on"); });
    if (idx >= 0) {
      var item = PL[idx];
      renderStill(S[item.kind === "scene" ? item.si : nextSceneIdxOfConn(idx)]);
    }
  }

  function nextSceneIdxOfConn(p) { var q = nextSceneAt(p); return PL[q].si; }

  function renderStill(s) {
    // Phones keep the portrait `still` (falling back to a poster only if one
    // is missing); everyone else prefers the landscape-appropriate poster so
    // a portrait still is never cover-cropped on a wide viewport — falling
    // back to `still` only if no poster exists at all.
    still.src = phone ? (s.still || posterOf(s)) : (posterOf(s) || s.still);
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
    // Both <video> elements already get preload="auto" once at creation
    // (see vids.forEach above) and that attribute is never touched again —
    // src reassignment + load() doesn't reset it — so this is a no-op today.
    // Set explicitly anyway so eager buffering is a property of prepare()
    // itself, not an inherited side effect that a future edit near element
    // creation could silently drop.
    v.preload = "auto";
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

    hideExplore();
    if (scene) { markDot(item.si); showCard(scene); }
    else hideCard();

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
      nextV.classList.add("is-on");
      curV.classList.remove("is-on");
      if (startBtn) {
        // A recovery retry (silent canplay/visibilitychange OR a gesture
        // that raced ahead of its own synchronous cleanup) just produced a
        // real playing frame: the autoplay-refusal dead end is over.
        startBtn.remove(); startBtn = null;
        started = true;
        removeRecoveryListeners();
      }
      // let the crossfade finish before parking the old player and handing it
      // the following item to buffer (setting src earlier would black out the
      // outgoing side of the fade)
      setTimeout(function () {
        try { curV.pause(); } catch (e) {}
        prepare(p + 1);
      }, 700);
    }

    // Effective playback rate: scenes may carry a `rate` multiplier (e.g.
    // rate:1.3) on top of the config-wide base RATE; connectors always play
    // at the plain base RATE.
    var effRate = scene ? RATE * (scene.rate || 1) : RATE;
    try { nextV.playbackRate = effRate; } catch (e) {}
    var pr;
    try { pr = nextV.play(); } catch (e) { enterStillsMode(); go(p); return; }
    onFirstFrame(nextV, swap);
    if (pr && pr.then) {
      pr.catch(function () {
        // OS refused playback (Low Power Mode / policy / cold-load Data
        // Saver): stills + tap-through, same as before. A rejection at
        // mount (idx 0, nothing has happened yet) additionally arms silent
        // + gesture recovery so the journey can resume without the visitor
        // specifically hunting down the overlay button.
        enterStillsMode();
        var s = scene || S[nextSceneIdxOfConn(p)];
        renderStill(s);
        if (p === LAST) showExplore(s);
        if (!started) {
          startOverlay();
          if (p === 0) armRecoveryListeners(nextV);
        }
      });
    }

    // Early-handoff crossfade: begin the transition to the NEXT item ~0.8s
    // of WALL-CLOCK time before this clip's natural end, instead of waiting
    // for `ended`. That trailing gap (decode/settle + the `ended` event's
    // own latency) is what reads as a dead pause between chained scenes.
    // `duration - currentTime` is media time; at effRate the wall-clock
    // remaining is that divided by effRate, so a rate:1.1 clip (which burns
    // through media-seconds faster than real time) doesn't fade early by an
    // inflated wall-clock margin. Guards: only the still-current item, only
    // when actually in video mode, only before the finale (p===LAST must
    // still reach a real `ended` to unlock the explore grid), a finite
    // duration (guards NaN/Infinity mid-load), and the `advanced` flag so a
    // ~4Hz timeupdate stream can't fire this twice for one play.
    //
    // Readiness gate: firing the crossfade only moves the STALL, it doesn't
    // remove it, if the next item hasn't actually buffered — the fade would
    // still land on a starved video and hitch. So at the 0.8s mark we also
    // require `prepared === p + 1` (prepare() targeted the right item) and
    // the prepared, still-inactive element's readyState >= HAVE_FUTURE_DATA
    // (3) — enough buffered to play forward without immediately stalling.
    // If that's not true yet, don't advance: arm a one-shot
    // canplaythrough/canplay listener on the prepared element and advance
    // the instant readiness arrives, instead of waiting out the full ~0.8s
    // gap to `ended`. `advanced` is shared by both paths (timeupdate poll
    // and the armed listener) so whichever gets there first wins and the
    // other is inert; `readinessListener` tracks the armed listener so it
    // can be torn down the moment the transition happens by ANY path
    // (early-ready poll, armed-listener fire, or the `ended` fallback)
    // instead of lingering on an element that gets reused for later items.
    var advanced = false;
    var readinessListener = null;
    function clearReadinessListener() {
      if (!readinessListener) return;
      var v = vids[1 - active];
      v.removeEventListener("canplaythrough", readinessListener);
      v.removeEventListener("canplay", readinessListener);
      readinessListener = null;
    }
    function tryAdvance() {
      if (advanced || idx !== p || stillsMode || p >= LAST) return;
      advanced = true;
      nextV.ontimeupdate = null;
      clearReadinessListener();
      go(p + 1);
    }
    nextV.ontimeupdate = function () {
      if (advanced || idx !== p || stillsMode || p >= LAST) return;
      var d = nextV.duration, ct = nextV.currentTime;
      if (!isFinite(d)) return;
      if ((d - ct) / effRate > 0.8) return;
      var prepV = vids[1 - active];
      if (prepared === p + 1 && prepV.readyState >= 3) { tryAdvance(); return; }
      if (readinessListener) return;   // already armed, waiting on it
      readinessListener = function () { clearReadinessListener(); tryAdvance(); };
      prepV.addEventListener("canplaythrough", readinessListener, { once: true });
      prepV.addEventListener("canplay", readinessListener, { once: true });
    };

    // Fallback: if the early handoff above never gets a ready next item
    // (e.g. duration never resolved, or the connection never buffers ahead
    // in time), `ended` still advances — this is the final safety net, same
    // as before. Once early-handoff HAS fired (either path), idx has
    // already moved to p+1 by the time `ended` would arrive, so the
    // `idx !== p` guard makes this a no-op — it never double-advances. It
    // also tears down any still-armed readiness listener so a canplay-class
    // event on a later-repurposed element can't fire a stale advance.
    nextV.onended = function () {
      if (idx !== p) return;
      clearReadinessListener();
      if (p === LAST) finish(); else go(p + 1);
    };
  }

  function finish() {
    var s = S[N - 1];
    if (idx !== LAST) { go(LAST); return; }
    showExplore(s);
  }

  // First-play overlay for the autoplay-refused path: still the visible
  // affordance, but no longer the ONLY way out — see restart() below.
  var startBtn = null;
  function startOverlay() {
    if (startBtn) return;
    startBtn = el("button", "tw-start");
    startBtn.type = "button";
    startBtn.textContent = config.startLabel || "Tap to play the story";
    startBtn.addEventListener("click", function () { restart(true); });
    stage.appendChild(startBtn);
  }

  // Shared recovery path: the overlay button, a real window gesture
  // (pointerdown/touchend), and the silent canplay/visibilitychange retries
  // all funnel through here — one restart flow instead of three copies.
  // `gesture` is true only for genuine user activation. Gesture-triggered
  // restarts are trusted to succeed (autoplay policy essentially guarantees
  // a play() called from a real activation), exactly like the original
  // overlay tap always was, so they drop the overlay / declare `started`
  // immediately and nudge the site music. Silent retries have no such
  // guarantee — they attempt play() without touching the overlay/`started`
  // up front; swap() (in go()) only tears the overlay down once a first
  // frame has actually painted, so a silent retry that fails leaves the
  // overlay exactly where it was, with the other recovery listeners still
  // armed (each is one-shot for ITSELF, not for the whole recovery system).
  function restart(gesture) {
    if (started) return;
    if (gesture) {
      removeRecoveryListeners();
      if (startBtn) { startBtn.remove(); startBtn = null; }
      started = true;
      startMusicOnGesture();   // this gesture IS the visitor's first real one
    }
    stillsMode = reduce;
    still.classList.remove("is-on");
    var at = idx < 0 ? 0 : idx;
    idx = -1; prepared = -1;
    go(at);
  }

  // Arms the one-shot recovery listeners after the initial (mount-time)
  // autoplay rejection. `failedV` is the video element whose play() was
  // just refused — canplay is watched on that same element. Each listener
  // fires at most once (native `once:true`, or a manual self-removal for
  // visibilitychange since only the -> visible transition should count);
  // if a silent retry fails, go()'s pr.catch re-arms a fresh set for the
  // next attempt.
  var recoveryOff = null;
  function removeRecoveryListeners() {
    if (recoveryOff) { recoveryOff(); recoveryOff = null; }
  }
  function armRecoveryListeners(failedV) {
    removeRecoveryListeners();
    var onGesture = function () { restart(true); };
    var onCanplay = function () { restart(false); };
    var onVisible = function () {
      if (document.visibilityState !== "visible") return;
      document.removeEventListener("visibilitychange", onVisible);
      restart(false);
    };
    window.addEventListener("pointerdown", onGesture, { once: true });
    window.addEventListener("touchend", onGesture, { once: true });
    failedV.addEventListener("canplay", onCanplay, { once: true });
    document.addEventListener("visibilitychange", onVisible);
    recoveryOff = function () {
      window.removeEventListener("pointerdown", onGesture);
      window.removeEventListener("touchend", onGesture);
      failedV.removeEventListener("canplay", onCanplay);
      document.removeEventListener("visibilitychange", onVisible);
    };
  }

  // Start the site music on the first real journey gesture (mirrors the
  // envelope page's window.swMusic.on() pattern). Guarded so it: respects an
  // explicit earlier mute (same sessionStorage key music.js writes), never
  // restarts/seeks a track that's already playing, and no-ops on pages where
  // music.js hasn't loaded (tap-engine is shared by index.html/story.html).
  // Latched to at most one attempt per page load: the adult page's music
  // loads with data-once, and music.js's own 'ended' handler for a
  // data-once track clears #sw-music.is-on WITHOUT writing the mute key
  // (see music.js:49-52) — so once the track finishes naturally, the
  // is-on/mute checks above alone can't distinguish "played once, done" from
  // "never started," and every later tap/skip would resurrect a track that
  // was designed to play once. The latch closes that hole while still
  // covering the original goal (nudge music going if load-time autoplay was
  // blocked). The music toggle button remains the only replay path, by
  // design — this function never fires again after its one attempt.
  var musicNudged = false;
  function startMusicOnGesture() {
    if (musicNudged) return;
    musicNudged = true;
    try {
      if (!window.swMusic) return;
      var muted = null;
      try { muted = sessionStorage.getItem("sw-music-on"); } catch (e) {}
      if (muted === "0") return;
      if (document.querySelector("#sw-music.is-on")) return;
      window.swMusic.on();
    } catch (e) {}
  }

  // ---- input: tap = next scene (connectors are skipped, not replayed) -----
  tap.addEventListener("click", function () {
    started = true;
    startMusicOnGesture();
    if (idx >= LAST) { finish(); return; }
    go(nextSceneAt(idx));
  });
  skip.addEventListener("click", function () {
    started = true;
    startMusicOnGesture();
    if (idx === LAST) { finish(); return; }
    go(LAST);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight" || e.key === " ") { e.preventDefault(); tap.click(); }
    if (e.key === "ArrowLeft") {
      var q = prevSceneAt(idx);
      if (q >= 0) { e.preventDefault(); go(q); }
    }
  });

  // ---- boot --------------------------------------------------------------
  go(0);
}
