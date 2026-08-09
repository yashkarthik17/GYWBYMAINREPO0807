/* Shared kids-story config for the tap engine. Used by story.html (the
   standalone page) AND by index.html, which mounts the story in-page when the
   kids letter button is tapped — same page means the envelope tap's audio
   unlock carries into the story, so the music never drops.
   Asset paths are root-relative so the config works from any page.

   i18n: every user-facing string forks EN/ES via GYWBT_KIDS_STRINGS below;
   asset paths, rates, and ids stay single-sourced — only strings fork.
   GYWBT_KIDS_CONFIG(lang) takes an optional explicit lang ('en'|'es'); the
   envelope's in-page launch passes the letter toggle's current choice. With
   no argument, it falls back to gywbtLang() — the stored localStorage pick,
   or a ?lang= URL override — for the standalone story.html mount. */
function gywbtLang() {
  var m = /[?&]lang=(en|es)/.exec(location.search);
  if (m) return m[1];
  return 'en';   // no stored preference (user direction): explicit ?lang= only
}

var GYWBT_KIDS_STRINGS = {
  en: {
    chrome: { startLabel: 'Tap to play the story', skipLabel: 'Skip to end »', nextLabel: 'Next scene', resumeLabel: 'Tap to continue the story' },
    beige: {
      eyebrow: 'Right now, somewhere',
      title: 'A birthday nobody noticed.',
      body: 'The candles are lit. The cake is ready. And the room is quiet as a Tuesday.',
      tags: ['Droopy balloons', 'Polite clapping'],
    },
    crashpad: {
      eyebrow: 'But way up in the clouds',
      title: 'Somebody noticed.',
      body: 'The party radar goes off in the Crash Pad, and Starry gives the only order there is: LET’S GO.',
      tags: ['Party radar', 'Confetti cannons'],
    },
    crash: {
      eyebrow: '3… 2… 1…',
      title: 'This party is officially crashed.',
      body: 'Doors fly open. Color pours in. The quiet doesn’t stand a chance.',
      tags: ['Confetti storm', 'Streamer trails'],
    },
    glowup: {
      eyebrow: 'Minutes later',
      title: 'Now THAT’S a birthday.',
      body: 'Cake tower. Balloon arches. And right in the middle, one kid who can’t stop grinning.',
      tags: ['Cake tower', 'Balloon arch', 'Dance floor'],
    },
    finale: {
      eyebrow: 'From Starry & the Crashers',
      title: 'Glad you were born today.',
      body: 'Not the cake. Not the presents. You. That’s the whole party.',
      exploreLabel: 'Explore the world',
      crashers: 'Meet the Crashers',
      again: 'Play it again',
    },
  },
  es: {
    chrome: { startLabel: 'Toca para reproducir la historia', skipLabel: 'Saltar al final »', nextLabel: 'Siguiente escena', resumeLabel: 'Toca para continuar la historia' },
    beige: {
      eyebrow: 'Ahora mismo, en algún lugar',
      title: 'Un cumpleaños que nadie notó.',
      body: 'Las velas están encendidas. El pastel está listo. Y el salón está tan callado como un martes cualquiera.',
      tags: ['Globos desinflados', 'Aplausos de cortesía'],
    },
    crashpad: {
      eyebrow: 'Pero allá arriba, en las nubes',
      title: 'Alguien sí lo notó.',
      body: 'El radar de fiestas se activa en el Crash Pad, y Starry da la única orden que existe: ¡VAMOS!',
      tags: ['Radar de fiestas', 'Cañones de confeti'],
    },
    crash: {
      eyebrow: '3… 2… 1…',
      title: 'Esta fiesta acaba de ser invadida. ¡Oficialmente!',
      body: 'Las puertas se abren de golpe. El color se desborda. El silencio no tiene ninguna oportunidad.',
      tags: ['Tormenta de confeti', 'Estelas de serpentinas'],
    },
    glowup: {
      eyebrow: 'Minutos después',
      title: 'Eso sí es un cumpleaños.',
      body: 'Torre de pastel. Arcos de globos. Y justo en el centro, un niño que no puede dejar de sonreír.',
      tags: ['Torre de pastel', 'Arco de globos', 'Pista de baile'],
    },
    finale: {
      eyebrow: 'De parte de Starry y los Crashers',
      title: 'Feliz que naciste hoy.',
      body: 'No es el pastel. No son los regalos. Eres tú. Esa es toda la fiesta.',
      exploreLabel: 'Explora el mundo',
      crashers: 'Conoce a los Crashers',
      again: 'Verlo de nuevo',
    },
  },
};

function GYWBT_KIDS_CONFIG(lang) {
  lang = (lang === 'es' || lang === 'en') ? lang : gywbtLang();
  var T = GYWBT_KIDS_STRINGS[lang];
  var phone = /[?&]swphone/.test(location.search) || Math.min(screen.width, screen.height) <= 600;
  function still(name) { return phone ? '/assets/' + name + '-p.webp?v=3' : '/assets/' + name + '.webp?v=4'; }
  // Music enters at scene 2 (user direction): the beige party stays quiet, the
  // theme starts when Starry's world appears. swap() covers every entry path —
  // story.html direct (sets the same src and starts it) and the envelope's
  // in-page launch (replaces the hushed strings on the gesture-unlocked
  // element). A gesture-less direct visit can reach scene 2 with audio still
  // locked (muted video autoplay needs no tap; audio does) — retry on the
  // first tap, respecting the ♪ button's mute.
  var themeSrc = lang === 'es' ? '/assets/audio/theme-es.wav?v=1' : '/assets/audio/theme.wav?v=3';
  var themeStart = lang === 'es' ? 20 : 11;
  // Full quiet-scene-1 cycle, replays included: entering scene 1 hushes
  // whatever is playing (pause WITHOUT recording a mute), entering scene 2
  // starts the theme - swap() on the first run, replay() (same track, same
  // start offset, mute respected) on every later run. "Play it again" no
  // longer touches the music itself; this hook owns the whole cycle.
  var themeArmed = false, themeThisRun = false;
  function themeAtSceneTwo(si) {
    if (!window.swMusic) return;
    if (si === 0) {
      themeThisRun = false;
      if (window.swMusic.hush) window.swMusic.hush();
      return;
    }
    if (si < 1 || themeThisRun) return;
    themeThisRun = true;
    if (!themeArmed) {
      themeArmed = true;
      if (!window.swMusic.swap) return;
      window.swMusic.swap(themeSrc, themeStart);
      var retry = function (e) {
        window.removeEventListener('pointerdown', retry);
        window.removeEventListener('touchend', retry);
        if (e && e.target && e.target.closest && e.target.closest('#sw-music')) return;
        var s = null; try { s = sessionStorage.getItem('sw-music-on'); } catch (err) {}
        if (s === '0') return;
        if (!document.querySelector('#sw-music.is-on')) window.swMusic.on();
      };
      window.addEventListener('pointerdown', retry);
      window.addEventListener('touchend', retry, { passive: true });
      return;
    }
    var s = null; try { s = sessionStorage.getItem('sw-music-on'); } catch (err) {}
    if (s === '0') return;
    if (typeof window.swMusic.replay === 'function') window.swMusic.replay();
  }
  function LNG(h) { return lang === 'es' ? h + '?lang=es' : h; }
  // Music enters at the SIX-SECOND mark on every journey (user direction):
  // time-driven in video mode; the scene hook remains the stills-mode
  // fallback and the replay reset (scene 1 re-entry hushes + re-arms).
  function themeAtSix(t) { if (t >= 6.0) themeAtSceneTwo(1); }

  return {
    playbackRate: 1.15,
    startLabel: T.chrome.startLabel,
    skipLabel: T.chrome.skipLabel,
    nextLabel: T.chrome.nextLabel,
    resumeLabel: T.chrome.resumeLabel,
    onScene: themeAtSceneTwo,
    onTime: themeAtSix,
    // Continuous journey: ONE stitched file per tier (crossfades + the tuned
    // per-scene pacing baked in — the file plays at rate 1). spans mirror the
    // 9-item chain below (scene,conn,…scene) in stitched-timeline seconds.
    // Regenerate with work/stitch_tap_journeys.py (prints these values).
    journey: {
      // Adaptive delivery: the HLS ladder starts low and shifts up with the
      // connection (Safari native / hls.js elsewhere); the MP4s below remain
      // the no-MSE fallback. Regenerate with work/hls_package.py.
      hls: '/assets/vid/hls/journey-tap/journey.m3u8',
      hlsMobile: '/assets/vid/hls/journey-tap-m/journey.m3u8',
      clip: '/assets/vid/journey-tap.mp4?v=4',
      clipMobile: '/assets/vid/journey-tap-m.mp4?v=5',
      poster: '/assets/journey-tap-poster.webp?v=1',
      posterMobile: '/assets/journey-tap-m-poster.webp?v=1',
      spans: [[0.0,6.734],[6.734,10.601],[10.601,16.559],[16.559,20.208],[20.208,26.166],[26.166,29.308],[29.308,34.806],[34.806,37.368],[37.368,42.4]],
      spansMobile: [[0.0,6.734],[6.734,9.949],[9.949,15.907],[15.907,19.991],[19.991,25.751],[25.751,29.292],[29.292,34.789],[34.789,38.221],[38.221,44.0]],
    },
    sections: [
      {
        id: 'beige', label: 'The Beige Party',
        still: still('beige'),
        poster: '/assets/beige-poster.webp?v=4',
        clip: '/assets/vid/beige.mp4?v=4',
        clipMobile: '/assets/vid/beige-m.mp4?v=3',
        posterMobile: '/assets/beige-poster-m.webp?v=3',
        accent: '#8B95A6',
        eyebrow: T.beige.eyebrow,
        title: T.beige.title,
        body: T.beige.body,
        tags: T.beige.tags,
      },
      {
        id: 'crashpad', label: 'The Crash Pad',
        still: still('crashpad'),
        poster: '/assets/crashpad-poster.webp?v=4',
        clip: '/assets/vid/crashpad.mp4?v=4',
        clipMobile: '/assets/vid/crashpad-m.mp4?v=3',
        posterMobile: '/assets/crashpad-poster-m.webp?v=3',
        rate: 1.10,
        accent: '#FFC93C',
        eyebrow: T.crashpad.eyebrow,
        title: T.crashpad.title,
        body: T.crashpad.body,
        tags: T.crashpad.tags,
      },
      {
        id: 'crash', label: 'The Crash',
        still: still('crash'),
        poster: '/assets/crash-poster.webp?v=4',
        clip: '/assets/vid/crash.mp4?v=4',
        clipMobile: '/assets/vid/crash-m.mp4?v=3',
        posterMobile: '/assets/crash-poster-m.webp?v=3',
        rate: 1.10,
        accent: '#E84A9B',
        eyebrow: T.crash.eyebrow,
        title: T.crash.title,
        body: T.crash.body,
        tags: T.crash.tags,
      },
      {
        id: 'glowup', label: 'The Glow-Up',
        still: still('glowup'),
        poster: '/assets/glowup-poster.webp?v=4',
        clip: '/assets/vid/glowup.mp4?v=4',
        clipMobile: '/assets/vid/glowup-m.mp4?v=3',
        posterMobile: '/assets/glowup-poster-m.webp?v=3',
        rate: 1.15,
        accent: '#8B5CF6',
        eyebrow: T.glowup.eyebrow,
        title: T.glowup.title,
        body: T.glowup.body,
        tags: T.glowup.tags,
      },
      {
        id: 'finale', label: 'Starry’s Send-Off',
        still: still('finale'),
        poster: '/assets/finale-poster.webp?v=4',
        clip: '/assets/vid/finale.mp4?v=4',
        clipMobile: '/assets/vid/finale-m.mp4?v=3',
        posterMobile: '/assets/finale-poster-m.webp?v=3',
        rate: 1.15,
        accent: '#FFC93C',
        eyebrow: T.finale.eyebrow,
        title: T.finale.title,
        body: T.finale.body,
        tags: [],
        explore: { label: T.finale.exploreLabel, links: [
          { label: T.finale.crashers, href: LNG('/crashers.html') },
          { label: T.finale.again, href: '#top' },
        ] },
      },
    ],
    connectors: [
      '/assets/vid/conn1.mp4?v=4',
      '/assets/vid/conn2.mp4?v=4',
      '/assets/vid/conn3.mp4?v=4',
      '/assets/vid/conn4.mp4?v=4',
    ],
    connectorsMobile: [
      '/assets/vid/conn1-m.mp4?v=3',
      '/assets/vid/conn2-m.mp4?v=3',
      '/assets/vid/conn3-m.mp4?v=3',
      '/assets/vid/conn4-m.mp4?v=3',
    ],
  };
}
