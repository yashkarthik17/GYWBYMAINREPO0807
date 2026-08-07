/* Shared adult-journey config for the tap engine. Used by adult/index.html
   (the standalone page) AND by index.html, which mounts the journey in-page
   when the grown-ups letter button is tapped — same page means the envelope
   tap's audio unlock carries into the journey, so the music never drops.
   Asset paths are root-relative (/adult/...) so the config works from any page.

   i18n: every user-facing string forks EN/ES via GYWBT_ADULT_STRINGS below;
   asset paths, rates, and ids stay single-sourced — only strings fork.
   GYWBT_ADULT_CONFIG(lang) takes an optional explicit lang ('en'|'es'); the
   envelope's in-page launch passes the letter toggle's current choice. With
   no argument, it falls back to gywbtLang() — the stored localStorage pick,
   or a ?lang= URL override — for the standalone adult/index.html mount.

   Note: hint/diveScroll/crossfade/scrollMobileFactor/journeyMobile and each
   section's scroll/linger keys are leftovers from the retired scroll-scrub
   engine (scrub-engine.js, not loaded by any page anymore) — tap-engine.js
   ignores them today. `hint` still gets an ES string below for a complete
   table/future-proofing, even though nothing currently renders it. */
function gywbtLang() {
  var m = /[?&]lang=(en|es)/.exec(location.search);
  if (m) { try { localStorage.setItem('gywbt-lang', m[1]); } catch (e) {} return m[1]; }
  var s = null; try { s = localStorage.getItem('gywbt-lang'); } catch (e) {}
  return s === 'es' ? 'es' : 'en';
}

var GYWBT_ADULT_STRINGS = {
  en: {
    hint: 'scroll to crash the party',
    chrome: { startLabel: 'Tap to play the story', skipLabel: 'Skip to end »', nextLabel: 'Next scene', resumeLabel: 'Tap to continue the story' },
    quiet: {
      eyebrow: 'Be honest',
      title: 'Birthdays got smaller, didn’t they.',
      body: 'Somewhere between ten and forty, the parties turned into polite dinners that end by nine.',
      tags: ['Polite toasts', 'Early goodbyes'],
    },
    glowup: {
      eyebrow: 'Then the sky RSVPs',
      title: 'The Crashers crash in.',
      body: 'One little cloud clears the fence. Nobody checks their phone again all night.',
      tags: ['Confetti included'],
    },
    photo: {
      eyebrow: 'Say cheese',
      title: 'Photos worth fighting over.',
      body: 'Your friends are laughing in every single frame.',
    },
    patio: {
      eyebrow: 'And 25ths. And 30ths.',
      title: 'Yes, they crash 20ths.',
      body: 'Enchantment doesn’t card.',
    },
    sendoff: {
      eyebrow: 'From Starry & the Crashers',
      title: 'Glad you were born today.',
      body: 'They wave until the lawn goes dark. And they never forget a date.',
      exploreLabel: 'Explore',
      hire: 'Hire the Crew',
      crew: 'Meet the Crew',
      store: 'The Party Store',
      mission: 'Our Mission',
      again: 'Play it again',
    },
  },
  es: {
    hint: 'haz scroll para colarte en la fiesta',
    chrome: { startLabel: 'Toca para reproducir la historia', skipLabel: 'Saltar al final »', nextLabel: 'Siguiente escena', resumeLabel: 'Toca para continuar la historia' },
    quiet: {
      eyebrow: 'Seamos honestos',
      title: 'Los cumpleaños se hicieron más pequeños, ¿verdad?',
      body: 'En algún punto entre los diez y los cuarenta, las fiestas se convirtieron en cenas educadas que terminan a las nueve.',
      tags: ['Brindis de compromiso', 'Despedidas tempranas'],
    },
    glowup: {
      eyebrow: 'Entonces el cielo confirma asistencia',
      title: 'Los Crashers se cuelan.',
      body: 'Una nubecita salta la cerca. Nadie vuelve a revisar su teléfono en toda la noche.',
      tags: ['Confeti incluido'],
    },
    photo: {
      eyebrow: 'Digan “whisky”',
      title: 'Fotos por las que vale la pena pelear.',
      body: 'Tus amigos se ríen en cada foto.',
    },
    patio: {
      eyebrow: 'Y los 25. Y los 30.',
      title: 'Sí, también se cuelan en los 20.',
      body: 'El encanto no pide identificación.',
    },
    sendoff: {
      eyebrow: 'De parte de Starry y los Crashers',
      title: 'Feliz que naciste hoy.',
      body: 'Se despiden con la mano hasta que el jardín se oscurece. Y jamás olvidan una fecha.',
      exploreLabel: 'Explora',
      hire: 'Contrata a la Tripulación',
      crew: 'Conoce a la Tripulación',
      store: 'La Tienda de Fiestas',
      mission: 'Nuestra Misión',
      again: 'Verlo de nuevo',
    },
  },
};

function GYWBT_ADULT_CONFIG(lang) {
  lang = (lang === 'es' || lang === 'en') ? lang : gywbtLang();
  var T = GYWBT_ADULT_STRINGS[lang];
  // Music enters at scene 2 (user direction) — same pattern as the kids
  // config, pointed at the adult tracks (its own files under /adult/, a
  // different song despite the shared filename). See story-config.js for the
  // full rationale on swap() + the first-tap retry.
  var themeSrc = lang === 'es' ? '/adult/assets/audio/theme-es.wav?v=1' : '/adult/assets/audio/theme.wav?v=3';
  var themeStart = lang === 'es' ? 20 : 11;
  var musicStarted = false;
  function themeAtSceneTwo(si) {
    if (musicStarted || si < 1) return;
    if (!window.swMusic || !window.swMusic.swap) return;
    musicStarted = true;
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
  }
  return {
    hint: T.hint,
    startLabel: T.chrome.startLabel,
    skipLabel: T.chrome.skipLabel,
    nextLabel: T.chrome.nextLabel,
    resumeLabel: T.chrome.resumeLabel,
    onScene: themeAtSceneTwo,
    diveScroll: 1.5,
    crossfade: 0.12,
    // longer mobile track: same scroll speed demands ~30% less playback rate,
    // so chase-play keeps up instead of racing/skipping (scroll-skip fix)
    scrollMobileFactor: 2.6,
    // Continuous journey: ONE stitched file per tier (crossfades + the tuned
    // per-scene pacing baked in — the file plays at rate 1). spans mirror the
    // 5-scene chain below (no connectors) in stitched-timeline seconds.
    // Regenerate with work/stitch_tap_journeys.py (prints these values).
    // (Replaces the retired scroll-engine journeyMobile block.)
    journey: {
      clip: '/adult/assets/vid/journey-tap.mp4?v=3',
      clipMobile: '/adult/assets/vid/journey-tap-m.mp4?v=2',
      poster: '/adult/assets/journey-tap-poster.webp?v=1',
      posterMobile: '/adult/assets/journey-tap-m-poster.webp?v=1',
      spans: [[0.0,6.436],[6.436,13.178],[13.178,20.339],[20.339,27.499],[27.499,34.683]],
      spansMobile: [[0.0,6.436],[6.436,13.62],[13.62,20.326],[20.326,27.486],[27.486,34.683]],
    },
    sections: [
      { id:'quiet', label:'The Quiet Party',
        still:'/adult/assets/quiet.webp?v=7', poster:'/adult/assets/quiet-poster.webp?v=6', posterMobile:'/adult/assets/quiet-poster-m.webp?v=7',
        clip:'/adult/assets/vid/quiet.mp4?v=6', clipMobile:'/adult/assets/vid/quiet-m.mp4?v=7',
        scroll:1.4, rate:1.235,
        accent:'#b9a27a', eyebrow: T.quiet.eyebrow,
        title: T.quiet.title,
        body: T.quiet.body,
        tags: T.quiet.tags },
      { id:'glowup', label:'The Crash',
        still:'/adult/assets/glowup.webp?v=10', poster:'/adult/assets/glowup-poster.webp?v=7', posterMobile:'/adult/assets/glowup-poster-m.webp?v=10',
        clip:'/adult/assets/vid/glowup.mp4?v=7', clipMobile:'/adult/assets/vid/glowup-m.mp4?v=10',
        scroll:1.6, linger:0.35, rate:1.0,
        accent:'#E84A9B', eyebrow: T.glowup.eyebrow,
        title: T.glowup.title,
        body: T.glowup.body,
        tags: T.glowup.tags },
      { id:'photo', label:'Say Cheese',
        still:'/adult/assets/photo.webp?v=11', poster:'/adult/assets/photo-poster.webp?v=7', posterMobile:'/adult/assets/photo-poster-m.webp?v=11',
        clip:'/adult/assets/vid/photo.mp4?v=7', clipMobile:'/adult/assets/vid/photo-m.mp4?v=11',
        scroll:1.8, linger:0.5, rate:1.1,
        accent:'#8B5CF6', eyebrow: T.photo.eyebrow,
        title: T.photo.title,
        body: T.photo.body,
        tags: [] },
      { id:'patio', label:'The Patio Party',
        still:'/adult/assets/patio.webp?v=8', poster:'/adult/assets/patio-poster.webp?v=6', posterMobile:'/adult/assets/patio-poster-m.webp?v=8',
        clip:'/adult/assets/vid/patio.mp4?v=6', clipMobile:'/adult/assets/vid/patio-m.mp4?v=8',
        scroll:1.6, linger:0.35, rate:1.1,
        accent:'#FFC93C', eyebrow: T.patio.eyebrow,
        title: T.patio.title,
        body: T.patio.body,
        tags: [] },
      { id:'sendoff', label:'The Send-Off',
        still:'/adult/assets/sendoff.webp?v=7', poster:'/adult/assets/sendoff-poster.webp?v=6', posterMobile:'/adult/assets/sendoff-poster-m.webp?v=7',
        clip:'/adult/assets/vid/sendoff.mp4?v=6', clipMobile:'/adult/assets/vid/sendoff-m.mp4?v=7',
        scroll:2, linger:0.45, rate:1.1,
        accent:'#5BB8F0', eyebrow: T.sendoff.eyebrow,
        title: T.sendoff.title,
        body: T.sendoff.body,
        explore:{ label: T.sendoff.exploreLabel, links:[
          { label: T.sendoff.hire, href:'/hire.html' },
          { label: T.sendoff.crew, href:'/adult/crew.html' },
          { label: T.sendoff.store, href:'/store.html' },
          { label: T.sendoff.mission, href:'/mission.html' },
          { label: T.sendoff.again, href:'#top' },
        ] } },
    ],
    connectors: [],
  };
}
