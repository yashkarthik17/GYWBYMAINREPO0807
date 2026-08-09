/* Theme-song toggle, shared by every page.
   Looks for assets/audio/theme.mp3 — if the file isn't deployed yet, no button
   appears at all, so this ships ahead of the track. Drop the song in, redeploy,
   and the button shows up on its own. Playback starts from a tap (a user gesture,
   so no autoplay policy fights), loops, and the on/off choice sticks for the
   visit (sessionStorage). */
(function () {
  var KEY = 'sw-music-on';
  // <script src="music.js" data-autostart> arms playback on the first tap of the
  // visit (unless the visitor already muted) — used by pages that should have
  // music without an explicit "start" moment, like the adult site.
  // data-src overrides the track for that page (the envelope page plays the
  // classical strings; everything else gets its site's theme).
  var tag = document.currentScript;
  var AUTO = !!(tag && tag.hasAttribute('data-autostart'));
  var ONCE = !!(tag && tag.hasAttribute('data-once'));
  var SRC = (tag && tag.getAttribute('data-src')) || 'assets/audio/theme.wav?v=3';
  // data-start="8" skips a dead-air intro: playback begins this many seconds in
  // and every loop restarts there too, so the delay never plays. Pages without
  // the attribute (the envelope's classical strings) play from 0:00 as before.
  var START = parseFloat(tag && tag.getAttribute('data-start')) || 0;

  // Spanish track override: data-src-es / data-start-es on the script tag.
  // Resolved once at load, from the same lang source (?lang= URL override /
  // localStorage['gywbt-lang']) the aria-label text below reads — this has to
  // happen BEFORE the existence-check fetch below, since SRC drives that fetch.
  // EN path is untouched: SRC/START only change when lang is 'es' AND
  // data-src-es is present on the tag.
  try {
    var qLang0 = /[?&]lang=(en|es)/.exec(location.search);
    var pageLang0 = qLang0 ? qLang0[1] : 'en';   // no stored preference
    var srcEs0 = tag && tag.getAttribute('data-src-es');
    if (pageLang0 === 'es' && srcEs0) {
      SRC = srcEs0;
      START = parseFloat(tag.getAttribute('data-start-es') || '0');
    }
  } catch (e) {}

  fetch(SRC, { method: 'HEAD' })
    .then(function (r) { if (r.ok) build(); })
    .catch(function () { /* no file, no button */ });

  function build() {
    var audio = new Audio(SRC);
    audio.preload = 'none';

    // i18n: aria-label text only, read once at build time from the same
    // ?lang= URL / localStorage['gywbt-lang'] the letter toggle writes.
    // Static, not live — this button can exist before the toggle's own
    // script runs, and re-wiring it to react to a later toggle click isn't
    // "trivial," so it's out of scope here (see task-spanish-report.md).
    var mLang = 'en';
    try {
      var qm = /[?&]lang=(en|es)/.exec(location.search);
      mLang = qm ? qm[1] : 'en';   // no stored preference
    } catch (e) {}
    var M = mLang === 'es'
      ? { play: 'Reproducir la canción', pause: 'Pausar la canción' }
      : { play: 'Play the theme song', pause: 'Pause the theme song' };

    // Seek past the intro. With an offset we can't use native looping (it always
    // rewinds to 0), so loop by hand on 'ended'. preload='none' means metadata
    // isn't ready until the first play() kicks off a load, so seek at every
    // readiness stage — iOS ignores seeks issued before the stream can play,
    // silently starting at 0:00; the timeupdate guard snaps it forward if
    // playback still begins at the top. START is mutable (swMusic.swap changes
    // track mid-page), so every handler re-reads it.
    function seekIntoTrack() {
      if (START > 0 && audio.currentTime < START - 0.05) {
        try { audio.currentTime = START; } catch (e) {}
      }
    }
    audio.loop = (START === 0) && !ONCE;
    audio.addEventListener('loadedmetadata', seekIntoTrack);
    audio.addEventListener('canplay', seekIntoTrack);
    audio.addEventListener('timeupdate', function () {
      if (START > 0 && audio.currentTime < START - 0.5) seekIntoTrack();
    });
    audio.addEventListener('ended', function () {
      if (ONCE) { setUi(false); try { audio.currentTime = START; } catch (e) {} return; }
      if (START > 0) { seekIntoTrack(); audio.play().catch(function () {}); }
    });

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.id = 'sw-music';
    btn.setAttribute('aria-label', M.play);
    btn.setAttribute('aria-pressed', 'false');
    btn.textContent = '♪';

    var css = document.createElement('style');
    css.textContent =
      '#sw-music{position:fixed;right:calc(16px + env(safe-area-inset-right));' +
      'bottom:calc(16px + env(safe-area-inset-bottom));z-index:72;width:48px;height:48px;' +
      'border-radius:50%;border:0;cursor:pointer;font-size:1.25rem;line-height:1;color:#fff;' +
      'background:#1D2B50;box-shadow:0 8px 22px rgba(29,43,80,.38);' +
      'transition:transform .2s ease,background .2s ease;}' +
      '#sw-music:hover{transform:scale(1.08);}' +
      '#sw-music:focus-visible{outline:3px solid #FFC93C;outline-offset:2px;}' +
      '#sw-music.is-on{background:#E84A9B;animation:sw-music-bob 1.6s ease-in-out infinite;}' +
      '@keyframes sw-music-bob{0%,100%{transform:rotate(-6deg)}50%{transform:rotate(6deg)}}' +
      '@media (prefers-reduced-motion:reduce){#sw-music.is-on{animation:none;}}';
    document.head.appendChild(css);
    document.body.appendChild(btn);

    function setUi(on) {
      btn.classList.toggle('is-on', on);
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      btn.setAttribute('aria-label', on ? M.pause : M.play);
    }

    function set(on) {
      if (on) {
        seekIntoTrack();
        audio.play().then(function () {
          setUi(true);
          try { sessionStorage.setItem(KEY, '1'); } catch (e) {}
        }).catch(function () { setUi(false); /* blocked: stay off, next tap retries */ });
      } else {
        audio.pause();
        setUi(false);
        try { sessionStorage.setItem(KEY, '0'); } catch (e) {}
      }
    }

    btn.addEventListener('click', function () { set(audio.paused); });

    // Page lifecycle: iOS lets a pure-audio element keep playing when Safari
    // is backgrounded or swiped away (it treats it like a music app). Pause
    // the song whenever the page hides and resume only if WE paused it; a
    // real exit (pagehide) stops it outright.
    var pausedByHide = false;
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) {
        if (!audio.paused) { pausedByHide = true; audio.pause(); }
      } else if (pausedByHide) {
        pausedByHide = false;
        audio.play().catch(function () { setUi(false); });
      }
    });
    window.addEventListener('pagehide', function () {
      pausedByHide = false;
      try { audio.pause(); } catch (e) {}
    });

    // Public hook: pages can start/stop the theme inside their own user-gesture
    // handlers (the envelope page starts it the moment the seal is tapped).
    // Respects an explicit mute from earlier in the visit.
    window.swMusic = {
      on: function () { var s = null; try { s = sessionStorage.getItem(KEY); } catch (e) {} if (s !== '0') set(true); },
      off: function () { set(false); },
      // Pause WITHOUT recording a mute: off() writes '0' and would veto every
      // later on()/swap() for the visit. The journey launches use hush() to
      // silence the envelope strings for the quiet first scene while leaving
      // scene 2's music entrance allowed.
      hush: function () { audio.pause(); setUi(false); },
      // Switch tracks WITHOUT leaving the page (the audio element stays
      // gesture-unlocked, so the new track plays instantly — this is how the
      // in-page kids story keeps music from the envelope tap onward).
      swap: function (src, start) {
        START = start || 0;
        audio.loop = (START === 0) && !ONCE;
        audio.src = src;
        try { audio.load(); } catch (e) {}
        var s = null; try { s = sessionStorage.getItem(KEY); } catch (e) {}
        if (s !== '0') set(true);
      },
      // Public replay hook: restarts the CURRENT track from its configured
      // start offset (START — whatever swap() last set, or the page's own
      // data-start if swap was never called) and plays it through the same
      // honest path as on()/set(true): the UI (♪ button + aria-pressed) only
      // flips once the play() promise actually resolves, and a successful
      // play stores '1' in sessionStorage exactly like a normal on(). Works
      // from any state — mid-play (seeks back without stopping), ended/
      // stopped (data-once tracks land here after their natural 'ended'),
      // or never-started. Doesn't touch audio.loop, so a data-once track
      // still plays once and stops after this replay, same as before.
      // This is a raw "restart from the top" primitive like set(true) — it
      // does not itself consult the mute key, matching set(true)'s
      // contract; callers that want to respect an explicit earlier mute
      // (see adult/tap-engine.js and tap-engine.js's "Play it again"
      // handlers) check sessionStorage themselves before calling this.
      replay: function () {
        try { audio.currentTime = START; } catch (e) {}
        set(true);
      }
    };

    // resume across pages within the visit — needs one tap anyway on strict
    // browsers, so re-arm on the first gesture instead of trying to autoplay.
    // data-autostart pages also arm on a fresh visit (stored choice unset).
    var stored = null;
    try { stored = sessionStorage.getItem(KEY); } catch (e) {}
    var wanted = stored === '1' || (AUTO && stored !== '0');
    if (wanted) {
      // Try immediately — browsers permit it once the visitor has interacted
      // with the site (e.g. tapping open the envelope a page ago). The story
      // pages auto-play with no guaranteed tap, so waiting for a gesture
      // alone left the music silent. If blocked, set() fails quietly and the
      // first-gesture listeners below pick it up.
      set(true);   // real autoplay attempt at load; works when the visit already had a gesture
      var once = function (e) {
        window.removeEventListener('pointerdown', once);
        window.removeEventListener('touchend', once);
        if (e && e.target && e.target.closest && e.target.closest('#sw-music')) return; // their first tap IS the mute button — respect it
        if (audio.paused) set(true);
      };
      window.addEventListener('pointerdown', once);
      window.addEventListener('touchend', once, { passive: true });
    }
  }
})();
