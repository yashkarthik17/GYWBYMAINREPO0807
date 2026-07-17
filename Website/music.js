/* Theme-song toggle, shared by every page.
   Looks for assets/audio/theme.mp3 — if the file isn't deployed yet, no button
   appears at all, so this ships ahead of the track. Drop the song in, redeploy,
   and the button shows up on its own. Playback starts from a tap (a user gesture,
   so no autoplay policy fights), loops, and the on/off choice sticks for the
   visit (sessionStorage). */
(function () {
  var SRC = 'assets/audio/theme.mp3';
  var KEY = 'sw-music-on';

  fetch(SRC, { method: 'HEAD' })
    .then(function (r) { if (r.ok) build(); })
    .catch(function () { /* no file, no button */ });

  function build() {
    var audio = new Audio(SRC);
    audio.loop = true;
    audio.preload = 'none';

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

    function set(on) {
      if (on) {
        audio.play().then(function () {
          btn.classList.add('is-on');
          btn.setAttribute('aria-pressed', 'true');
          btn.setAttribute('aria-label', 'Pause the theme song');
          try { sessionStorage.setItem(KEY, '1'); } catch (e) {}
        }).catch(function () { /* blocked: stay off, next tap retries */ });
      } else {
        audio.pause();
        btn.classList.remove('is-on');
        btn.setAttribute('aria-pressed', 'false');
        btn.setAttribute('aria-label', 'Play the theme song');
        try { sessionStorage.setItem(KEY, '0'); } catch (e) {}
      }
    }

    btn.addEventListener('click', function () { set(audio.paused); });

    // resume across pages within the visit — needs one tap anyway on strict
    // browsers, so re-arm on the first gesture instead of trying to autoplay
    var wanted = false;
    try { wanted = sessionStorage.getItem(KEY) === '1'; } catch (e) {}
    if (wanted) {
      var once = function () { set(true); };
      window.addEventListener('pointerdown', once, { once: true });
      window.addEventListener('touchend', once, { once: true, passive: true });
    }
  }
})();
