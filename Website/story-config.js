/* Shared kids-story config for the tap engine. Used by story.html (the
   standalone page) AND by index.html, which mounts the story in-page when the
   kids letter button is tapped — same page means the envelope tap's audio
   unlock carries into the story, so the music never drops.
   Asset paths are root-relative so the config works from any page. */
function GYWBT_KIDS_CONFIG() {
  var phone = /[?&]swphone/.test(location.search) || Math.min(screen.width, screen.height) <= 600;
  function still(name) { return phone ? '/assets/' + name + '-p.webp?v=3' : '/assets/' + name + '.webp?v=4'; }
  return {
    playbackRate: 1.15,
    sections: [
      {
        id: 'beige', label: 'The Beige Party',
        still: still('beige'),
        poster: '/assets/beige-poster.webp?v=4',
        clip: '/assets/vid/beige.mp4?v=4',
        clipMobile: '/assets/vid/beige-m.mp4?v=3',
        posterMobile: '/assets/beige-poster-m.webp?v=3',
        accent: '#8B95A6',
        eyebrow: 'Right now, somewhere',
        title: 'A birthday nobody noticed.',
        body: 'The candles are lit. The cake is ready. And the room is quiet as a Tuesday.',
        tags: ['Droopy balloons', 'Polite clapping'],
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
        eyebrow: 'But way up in the clouds',
        title: 'Somebody noticed.',
        body: 'The party radar goes off in the Crash Pad, and Starry gives the only order there is: LET’S GO.',
        tags: ['Party radar', 'Confetti cannons'],
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
        eyebrow: '3… 2… 1…',
        title: 'This party is officially crashed.',
        body: 'Doors fly open. Color pours in. The quiet doesn’t stand a chance.',
        tags: ['Confetti storm', 'Streamer trails'],
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
        eyebrow: 'Minutes later',
        title: 'Now THAT’S a birthday.',
        body: 'Cake tower. Balloon arches. And right in the middle, one kid who can’t stop grinning.',
        tags: ['Cake tower', 'Balloon arch', 'Dance floor'],
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
        eyebrow: 'From Starry & the Crashers',
        title: 'Glad you were born today.',
        body: 'Not the cake. Not the presents. You. That’s the whole party.',
        tags: [],
        explore: { label: 'Explore the world', links: [
          { label: 'Meet the Crashers', href: '/crashers.html' },
          { label: 'Play it again', href: '#top' },
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
