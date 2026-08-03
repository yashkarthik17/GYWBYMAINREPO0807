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

  fetch(SRC, { method: 'HEAD' })
    .then(function (r) { if (r.ok) build(); })
    .catch(function () { /* no file, no button */ });

  function build() {
    var audio = new Audio(SRC);
    audio.preload = 'none';

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
    btn.setAttribute('aria-label', 'Play the theme song');
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
      btn.setAttribute('aria-label', on ? 'Pause the theme song' : 'Play the theme song');
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

    // Public hook: pages can start/stop the theme inside their own user-gesture
    // handlers (the envelope page starts it the moment the seal is tapped).
    // Respects an explicit mute from earlier in the visit.
    window.swMusic = {
      on: function () { var s = null; try { s = sessionStorage.getItem(KEY); } catch (e) {} if (s !== '0') set(true); },
      off: function () { set(false); },
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
