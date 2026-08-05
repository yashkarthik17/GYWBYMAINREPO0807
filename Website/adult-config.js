/* Shared adult-journey config for the tap engine. Used by adult/index.html
   (the standalone page) AND by index.html, which mounts the journey in-page
   when the grown-ups letter button is tapped — same page means the envelope
   tap's audio unlock carries into the journey, so the music never drops.
   Asset paths are root-relative (/adult/...) so the config works from any page. */
function GYWBT_ADULT_CONFIG() {
  return {
    hint: 'scroll to crash the party',
    diveScroll: 1.5,
    crossfade: 0.12,
    // longer mobile track: same scroll speed demands ~30% less playback rate,
    // so chase-play keeps up instead of racing/skipping (scroll-skip fix)
    scrollMobileFactor: 2.6,
    journeyMobile: {
      clip: '/adult/assets/vid/journey-m.mp4?v=8',
      poster: '/adult/assets/journey-poster-m.webp?v=7',
      spans: [[0.0, 8.042], [8.042, 16.042], [16.042, 24.042], [24.042, 32.042], [32.042, 40.042]],
    },
    sections: [
      { id:'quiet', label:'The Quiet Party',
        still:'/adult/assets/quiet.webp?v=7', poster:'/adult/assets/quiet-poster.webp?v=6', posterMobile:'/adult/assets/quiet-poster-m.webp?v=7',
        clip:'/adult/assets/vid/quiet.mp4?v=6', clipMobile:'/adult/assets/vid/quiet-m.mp4?v=7',
        scroll:1.4, rate:1.235,
        accent:'#b9a27a', eyebrow:'Be honest',
        title:'Birthdays got smaller, didn’t they.',
        body:'Somewhere between ten and forty, the parties turned into polite dinners that end by nine.',
        tags:['Polite toasts','Early goodbyes'] },
      { id:'glowup', label:'The Crash',
        still:'/adult/assets/glowup.webp?v=8', poster:'/adult/assets/glowup-poster.webp?v=7', posterMobile:'/adult/assets/glowup-poster-m.webp?v=8',
        clip:'/adult/assets/vid/glowup.mp4?v=7', clipMobile:'/adult/assets/vid/glowup-m.mp4?v=8',
        scroll:1.6, linger:0.35, rate:1.0,
        accent:'#E84A9B', eyebrow:'Then the sky RSVPs',
        title:'The Crashers crash in.',
        body:'One little cloud clears the fence. Nobody checks their phone again all night.',
        tags:['Confetti included'] },
      { id:'photo', label:'Say Cheese',
        still:'/adult/assets/photo.webp?v=8', poster:'/adult/assets/photo-poster.webp?v=7', posterMobile:'/adult/assets/photo-poster-m.webp?v=8',
        clip:'/adult/assets/vid/photo.mp4?v=7', clipMobile:'/adult/assets/vid/photo-m.mp4?v=8',
        scroll:1.8, linger:0.5, rate:1.1,
        accent:'#8B5CF6', eyebrow:'Say cheese',
        title:'Photos worth fighting over.',
        body:'Your friends are laughing in every single frame.',
        tags:[] },
      { id:'patio', label:'The Patio Party',
        still:'/adult/assets/patio.webp?v=7', poster:'/adult/assets/patio-poster.webp?v=6', posterMobile:'/adult/assets/patio-poster-m.webp?v=7',
        clip:'/adult/assets/vid/patio.mp4?v=6', clipMobile:'/adult/assets/vid/patio-m.mp4?v=7',
        scroll:1.6, linger:0.35, rate:1.1,
        accent:'#FFC93C', eyebrow:'And 25ths. And 30ths.',
        title:'Yes, they crash 20ths.',
        body:'Enchantment doesn’t card.',
        tags:[] },
      { id:'sendoff', label:'The Send-Off',
        still:'/adult/assets/sendoff.webp?v=7', poster:'/adult/assets/sendoff-poster.webp?v=6', posterMobile:'/adult/assets/sendoff-poster-m.webp?v=7',
        clip:'/adult/assets/vid/sendoff.mp4?v=6', clipMobile:'/adult/assets/vid/sendoff-m.mp4?v=7',
        scroll:2, linger:0.45, rate:1.1,
        accent:'#5BB8F0', eyebrow:'From Starry & the Crashers',
        title:'Glad you were born today.',
        body:'They wave until the lawn goes dark. And they never forget a date.',
        explore:{ label:'Explore', links:[
          { label:'Hire the Crew', href:'/hire.html' },
          { label:'Meet the Crew', href:'/adult/crew.html' },
          { label:'The Party Store', href:'/store.html' },
          { label:'Our Mission', href:'/mission.html' },
          { label:'Play it again', href:'#top' },
        ] } },
    ],
    connectors: [],
  };
}
