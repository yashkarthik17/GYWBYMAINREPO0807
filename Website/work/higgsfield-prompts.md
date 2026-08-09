# Higgsfield prompt pack — Glad You Were Born Today journeys

Model: **Seedance 2.0** for every clip. Resolution per section header. Durations ~8s
(connectors ~5s) — match the existing clip you're replacing.

> **IMPORTANT — the seam-pause fix.** The old renders eased into a static hover at the
> end (and some started slow). That settle is what read as a "pause" at every stitched
> seam. If you re-render, append this to EVERY prompt:
>
> *"The camera keeps moving through the entire shot — it is still traveling with
> visible motion on the very last frame. No slowdown, no settling, no static hold at
> the beginning or end."*
>
> Clips whose ends stay in motion need no trims at all and every seam lands cleanly.
>
> **Also DELETE the settle instruction that's already in these prompts.** Most end with a
> sentence like *"In the final second, all motion eases and the camera settles into a
> slow, steady drift…"* — that line is what created the hover endings (the pauses) in
> the first place. Remove it wherever it appears and use the keep-moving line instead.

Some clips were generated with reference/anchor images (listed under the prompt where
used — the files live in the repo's work folders). After replacing any clip, re-run:
`python work/stitch_tap_journeys.py` then `python work/hls_package.py` (spans print out
for the configs).


---

## KIDS — DESKTOP (landscape 1920x1080)

### beige.mp4 (scene 1)

```
Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the whole dull beige birthday party diorama from outside like a tiny model. The camera slowly glides forward and descends toward it, sweeping in toward the round cake table with its plain white sheet cake and the bored birthday kid figure, as if flying inside. As the camera pushes in, the roof and upper structure gently lift and open away to reveal the muted gray-beige interior. Glossy vinyl-toy miniature diorama world, smooth shiny plastic shading, soft rim light, tilt-shift miniature, palette of star gold #FFC93C, sky blue #5BB8F0, crash pink #E84A9B, party purple #8B5CF6, confetti green #4CC96B, cream #FFF4E0. Smooth, graceful, slow motion, subtle parallax. No text, no captions.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### conn1.mp4

```
Single continuous cinematic camera move, no cuts. The camera smoothly pulls up and back out of the dull beige birthday party room, rising into the sky, then glides forward across the connected miniature world and up through puffy white vinyl clouds, arriving above Starry's golden star-shaped cloud clubhouse, beginning to descend toward it. One connected miniature vinyl-toy world, seamless flowing aerial transition. Glossy vinyl-toy miniature diorama world, smooth shiny plastic shading, soft rim light, tilt-shift miniature, palette of star gold #FFC93C, sky blue #5BB8F0, crash pink #E84A9B, party purple #8B5CF6, confetti green #4CC96B, cream #FFF4E0. Smooth graceful slow motion. No text, no captions.
```

*Duration: 5s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### crashpad.mp4 (scene 2)

```
Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the whole golden star-shaped cloud clubhouse diorama from outside like a tiny model. The camera slowly glides forward and descends through the puffy white clouds toward it, sweeping in toward the big round party-radar dish where Starry the golden star character stands pointing, as if flying inside. As the camera pushes in, the roof of the star clubhouse gently lifts and opens away to reveal the warm interior where the small hooded Crasher characters load confetti cannons and stack gifts. Glossy vinyl-toy miniature diorama world, smooth shiny plastic shading, soft rim light, tilt-shift miniature, palette of star gold #FFC93C, sky blue #5BB8F0, crash pink #E84A9B, party purple #8B5CF6, confetti green #4CC96B, cream #FFF4E0. Smooth, graceful, slow motion, subtle parallax. No text, no captions.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### conn2.mp4

```
Single continuous cinematic camera move, no cuts. The camera smoothly pulls up and back out of the golden star-shaped cloud clubhouse, rising above the puffy clouds, then dives forward and down out of the sky, gliding across the connected miniature world and arriving above the beige living room diorama just as the small hooded Crasher characters streak toward it on streamer trails, beginning to descend toward its open roof. One connected miniature vinyl-toy world, seamless flowing aerial transition. Glossy vinyl-toy miniature diorama world, smooth shiny plastic shading, soft rim light, tilt-shift miniature, palette of star gold #FFC93C, sky blue #5BB8F0, crash pink #E84A9B, party purple #8B5CF6, confetti green #4CC96B, cream #FFF4E0. Smooth graceful slow motion. No text, no captions.
```

*Duration: 5s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### crash.mp4 (scene 3)

```
Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the beige living room diorama at the exact moment of the joyful party crash, from outside like a tiny model. The camera slowly glides forward and descends toward it, flying in through the open roof amid drifting confetti, sweeping in toward the cake table where the small birthday kid figure leaps up with arms raised while the three hooded Crasher characters ride streamer trails in through the window, confetti cannons firing, a wave of bright gold, pink, purple and green color flooding across the muted beige room. Glossy vinyl-toy miniature diorama world, smooth shiny plastic shading, soft rim light, tilt-shift miniature, palette of star gold #FFC93C, sky blue #5BB8F0, crash pink #E84A9B, party purple #8B5CF6, confetti green #4CC96B, cream #FFF4E0. Smooth, graceful, slow motion, subtle parallax. No text, no captions.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### conn3.mp4

```
Single continuous cinematic camera move, no cuts. The camera smoothly pulls up and back out of the living room mid-crash, rising into the sky with confetti drifting past, then glides forward in a gentle arc across the connected miniature world toward the same room now fully transformed into a glowing rainbow birthday party, and ends HIGH AND FAR from it: the final frame shows the whole party house tiny and distant, small in the center of the frame surrounded by open sky blue background, the camera still drifting slowly toward it. One connected miniature vinyl-toy world, seamless flowing aerial transition. Glossy vinyl-toy miniature diorama world, smooth shiny plastic shading, soft rim light, tilt-shift miniature, palette of star gold #FFC93C, sky blue #5BB8F0, crash pink #E84A9B, party purple #8B5CF6, confetti green #4CC96B, cream #FFF4E0. Smooth graceful slow motion. No text, no captions.
```

*Duration: 5s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### glowup.mp4 (scene 4)

```
Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the fully transformed birthday party diorama from outside like a tiny model. The camera slowly glides forward and descends toward it, sweeping in toward the towering five-layer rainbow cake at the center, as if flying inside. As the camera pushes in, the roof and upper structure gently lift and open away to reveal the party in full swing — balloon arches, a checkered dance floor with a glossy disco ball, the birthday kid figure dancing with the three hooded Crasher characters, garlands and confetti everywhere. Glossy vinyl-toy miniature diorama world, smooth shiny plastic shading, soft rim light, tilt-shift miniature, palette of star gold #FFC93C, sky blue #5BB8F0, crash pink #E84A9B, party purple #8B5CF6, confetti green #4CC96B, cream #FFF4E0. Smooth, graceful, slow motion, subtle parallax. No text, no captions.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### conn4.mp4

```
Single continuous cinematic camera move, no cuts. The camera smoothly pulls up and back out of the glowing rainbow birthday party room, rising into the soft sky, and the miniature world gently dissolves toward a celebration stage floating in soft sky blue space, where Starry, the big golden five-pointed star character, takes a joyful bow surrounded by the three small hooded Crasher characters tossing confetti, the camera arriving in front of the stage and beginning to descend toward Starry. One connected miniature vinyl-toy world, seamless flowing aerial transition. Glossy vinyl-toy miniature diorama world, smooth shiny plastic shading, soft rim light, tilt-shift miniature, palette of star gold #FFC93C, sky blue #5BB8F0, crash pink #E84A9B, party purple #8B5CF6, confetti green #4CC96B, cream #FFF4E0. Smooth graceful slow motion. No text, no captions.
```

*Duration: 5s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### finale.mp4 (scene 5)

```
Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the whole celebration stage diorama from outside like a tiny model. The camera slowly glides forward and descends toward it, flying low across the ringed stage toward Starry, the big cheerful golden five-pointed star character with a pink polka-dot party hat and rainbow checkered arms and legs, taking a joyful bow at center stage while the three small hooded Crasher characters toss confetti and hold balloon strings around him, sweeping in until Starry nearly fills the frame with confetti drifting past. Glossy vinyl-toy miniature diorama world, smooth shiny plastic shading, soft rim light, tilt-shift miniature, palette of star gold #FFC93C, sky blue #5BB8F0, crash pink #E84A9B, party purple #8B5CF6, confetti green #4CC96B, cream #FFF4E0. Smooth, graceful, slow motion, subtle parallax. No text, no captions.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

---

## KIDS — MOBILE (portrait 1080x1920)

### beige-m.mp4

```
Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the whole dull beige birthday party diorama from outside like a tiny model. The camera slowly glides forward and descends toward it, sweeping in toward the round cake table with its plain white sheet cake and the bored birthday kid figure, as if flying inside. As the camera pushes in, the roof and upper structure gently lift and open away to reveal the muted gray-beige interior. Glossy vinyl-toy miniature diorama world, smooth shiny plastic shading, soft rim light, tilt-shift miniature, palette of star gold #FFC93C, sky blue #5BB8F0, crash pink #E84A9B, party purple #8B5CF6, confetti green #4CC96B, cream #FFF4E0. Smooth, graceful, slow motion, subtle parallax. No text, no captions. Tall vertical portrait framing throughout, the scene always fully composed within the tall frame.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### conn1-m.mp4

```
Single continuous cinematic camera move, no cuts. The camera smoothly pulls up and back out of the dull beige birthday party room, rising into the sky, then glides forward across the connected miniature world and up through puffy white vinyl clouds, arriving above Starry's golden star-shaped cloud clubhouse, beginning to descend toward it. One connected miniature vinyl-toy world, seamless flowing aerial transition. Glossy vinyl-toy miniature diorama world, smooth shiny plastic shading, soft rim light, tilt-shift miniature, palette of star gold #FFC93C, sky blue #5BB8F0, crash pink #E84A9B, party purple #8B5CF6, confetti green #4CC96B, cream #FFF4E0. Smooth graceful slow motion. No text, no captions. Tall vertical portrait framing throughout, the scene always fully composed within the tall frame.
```

*Duration: 5s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### crashpad-m.mp4

```
Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the whole golden star-shaped cloud clubhouse diorama from outside like a tiny model. The camera slowly glides forward and descends through the puffy white clouds toward it, sweeping in toward the big round party-radar dish where Starry the golden star character stands pointing, as if flying inside. As the camera pushes in, the roof of the star clubhouse gently lifts and opens away to reveal the warm interior where the small hooded Crasher characters load confetti cannons and stack gifts. Glossy vinyl-toy miniature diorama world, smooth shiny plastic shading, soft rim light, tilt-shift miniature, palette of star gold #FFC93C, sky blue #5BB8F0, crash pink #E84A9B, party purple #8B5CF6, confetti green #4CC96B, cream #FFF4E0. Smooth, graceful, slow motion, subtle parallax. No text, no captions. Tall vertical portrait framing throughout, the scene always fully composed within the tall frame.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### conn2-m.mp4

```
Single continuous cinematic camera move, no cuts. The camera smoothly pulls up and back out of the golden star-shaped cloud clubhouse, rising above the puffy clouds, then dives forward and down through open empty sky — nothing below but soft sky blue background and a few drifting white vinyl clouds, NO landscape, NO hills, NO ground — and arrives high above the small beige living room house diorama floating on its own cloud, the house small and distant in the frame, the camera still descending gently toward it. One connected miniature vinyl-toy world, seamless flowing aerial transition. Glossy vinyl-toy miniature diorama world, smooth shiny plastic shading, soft rim light, tilt-shift miniature, palette of star gold #FFC93C, sky blue #5BB8F0, crash pink #E84A9B, party purple #8B5CF6, confetti green #4CC96B, cream #FFF4E0. Smooth graceful slow motion. No text, no captions. Tall vertical portrait framing throughout, the scene always fully composed within the tall frame.
```

*Duration: 5s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### crash-m.mp4

```
Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the beige living room diorama at the exact moment of the joyful party crash, from outside like a tiny model. The camera slowly glides forward and descends toward it, flying in through the open roof amid drifting confetti, sweeping in toward the cake table where the small birthday kid figure leaps up with arms raised while the three hooded Crasher characters ride streamer trails in through the window, confetti cannons firing, a wave of bright gold, pink, purple and green color flooding across the muted beige room. Glossy vinyl-toy miniature diorama world, smooth shiny plastic shading, soft rim light, tilt-shift miniature, palette of star gold #FFC93C, sky blue #5BB8F0, crash pink #E84A9B, party purple #8B5CF6, confetti green #4CC96B, cream #FFF4E0. The plain solid sky blue background stays constant and unchanged behind and around the floating diorama at all times, never shifting color. Smooth, graceful, slow motion, subtle parallax. No text, no captions. Tall vertical portrait framing throughout, the scene always fully composed within the tall frame.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### conn3-m.mp4

```
Single continuous cinematic camera move, no cuts. The camera smoothly pulls up and back out of the living room mid-crash, rising into the sky with confetti drifting past, then glides forward in a gentle arc across the connected miniature world toward the same room now fully transformed into a glowing rainbow birthday party, and descends toward it, arriving close so the glowing party diorama fills most of the tall frame, centered, the camera settling into a slow gentle drift toward it. One connected miniature vinyl-toy world, seamless flowing aerial transition. Glossy vinyl-toy miniature diorama world, smooth shiny plastic shading, soft rim light, tilt-shift miniature, palette of star gold #FFC93C, sky blue #5BB8F0, crash pink #E84A9B, party purple #8B5CF6, confetti green #4CC96B, cream #FFF4E0. Smooth graceful slow motion. No text, no captions. Tall vertical portrait framing throughout, the scene always fully composed within the tall frame.
```

*Duration: 5s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### glowup-m.mp4

```
Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the fully transformed birthday party diorama from outside like a tiny model. The camera slowly glides forward and descends toward it, sweeping in toward the towering five-layer rainbow cake at the center, as if flying inside. As the camera pushes in, the roof and upper structure gently lift and open away to reveal the party in full swing — balloon arches, a checkered dance floor with a glossy disco ball, the birthday kid figure dancing with the three hooded Crasher characters, garlands and confetti everywhere. Glossy vinyl-toy miniature diorama world, smooth shiny plastic shading, soft rim light, tilt-shift miniature, palette of star gold #FFC93C, sky blue #5BB8F0, crash pink #E84A9B, party purple #8B5CF6, confetti green #4CC96B, cream #FFF4E0. Smooth, graceful, slow motion, subtle parallax. No text, no captions. Tall vertical portrait framing throughout, the scene always fully composed within the tall frame.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### conn4-m.mp4

```
Single continuous cinematic camera move, no cuts. The camera smoothly pulls up and back out of the glowing rainbow birthday party room, rising into the soft sky, and the miniature world gently dissolves toward a celebration stage floating in soft sky blue space, where Starry, the big golden five-pointed star character, takes a joyful bow surrounded by the three small hooded Crasher characters tossing confetti, the camera arriving in front of the stage and beginning to descend toward Starry. One connected miniature vinyl-toy world, seamless flowing aerial transition. Glossy vinyl-toy miniature diorama world, smooth shiny plastic shading, soft rim light, tilt-shift miniature, palette of star gold #FFC93C, sky blue #5BB8F0, crash pink #E84A9B, party purple #8B5CF6, confetti green #4CC96B, cream #FFF4E0. Smooth graceful slow motion. No text, no captions. Tall vertical portrait framing throughout, the scene always fully composed within the tall frame.
```

*Duration: 5s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### finale-m.mp4

```
Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the whole celebration stage diorama from outside like a tiny model. The camera slowly glides forward and descends toward it, flying low across the ringed stage toward Starry, the big cheerful golden five-pointed star character with a pink polka-dot party hat and rainbow checkered arms and legs, taking a joyful bow at center stage while the three small hooded Crasher characters toss confetti and hold balloon strings around him, sweeping in until Starry nearly fills the frame with confetti drifting past. Glossy vinyl-toy miniature diorama world, smooth shiny plastic shading, soft rim light, tilt-shift miniature, palette of star gold #FFC93C, sky blue #5BB8F0, crash pink #E84A9B, party purple #8B5CF6, confetti green #4CC96B, cream #FFF4E0. Smooth, graceful, slow motion, subtle parallax. No text, no captions. Tall vertical portrait framing throughout, the scene always fully composed within the tall frame.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

---

## ADULT — DESKTOP (landscape 1920x1080)

### quiet.mp4 (scene 1)

```
Single continuous cinematic camera move, no cuts. Cinematic photorealistic live-action hybrid footage, wide 16:9 landscape, shallow depth of field, real textures. Smooth, graceful, slow camera motion, subtle parallax. Absolutely no text, no captions, no logos, no lettering or writing on any object. The camera begins inside a modest, quiet backyard birthday dinner for a GROWN ADULT in late golden afternoon light — a small circle of young adult friends in their 20s and 30s making polite conversation around the picnic table with its plain white sheet cake, one guest checking their watch, a lone half-deflated pastel balloon tied to the fence post. Ordinary real humans only — absolutely no cartoon characters, no mascots, no costumed figures, no toys, no animated creatures of any kind anywhere in the scene. The camera glides gently forward through the flat little party and drifts slowly among the guests as the quiet dinner winds down, conversation trailing off, the golden light softening toward dusk. Nothing in the sky above the rooftops for most of the shot — only ordinary dusk clouds and darkening blue. In the final second, all motion eases into a slow, steady, perfectly level drift, and a faint warm golden shimmer quietly begins to glow low in the dusk sky above the rooftops — subtle, distant, and unexplained: a soft diffuse glow only, no characters, no cloud shape, no clubhouse, no object or figure of any kind in the sky beyond that gentle glow.
Every human being in the scene is a young adult in their 20s or 30s — absolutely no human children, no babies, no toddlers, no minors, no middle-aged people, no elderly people, nobody with gray hair, no small human figures of any kind anywhere in frame or background; the only child-sized figures allowed are the three vinyl-toy Crasher mascots in their hooded onesies.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### glowup.mp4 (scene 2)

```
Single continuous cinematic camera move, no cuts. Cinematic photorealistic live-action hybrid footage, wide 16:9 landscape, shallow depth of field, real textures. Smooth, graceful, slow camera motion, subtle parallax. Absolutely no text, no captions, no logos, no lettering or writing on any object. The camera opens on the warm golden glow pulsing low over the dark rooftops of a quiet neighborhood at dusk, and the glow suddenly flares and breaks open as the magical cloud clubhouse BURSTS through it above the rooftops, already descending, banking gently toward us with its golden sparkle trail streaming behind it, paper lanterns rushing up past the camera and warm string lights flickering on below as the little backyard party grows steadily closer beneath the cloud's fluffy edge, until the cloud sweeps in over the wooden fence like a parade float and settles into a majestic hover above the backyard: STARRY — a tall golden five-pointed star character with a friendly cartoon face on the star body, large cartoon eyes with white sclera and blue irises, thin black eyebrows, a happy open smile, wearing a pink polka-dot cone party hat, with rainbow-checkered fabric arms and legs, puffy white four-fingered cartoon gloves, and round shiny golden boots — waves from the balcony rail, and the three CRASHERS — small toddler-sized creatures whose bodies are simple ROUND hooded onesies, soft round hooded baby-suit silhouettes, NOT shaped like bolts or diamonds or splats, the patterns only the FABRIC PRINT of each onesie: one onesie in orange fabric with a yellow zigzag print, one in blue fabric with a purple diamond print, one in green fabric with a multicolor paint-splatter print, each with a pale round face peeking out of its snug hood, big sparkly jewel-like eyes, rosy round blush cheeks, a tiny happy smile, and a red-and-white striped cone party hat on top of the hood — ride the front deck of the cloud waving down, a small purple confetti cannon firing a soft arc of colorful confetti, the young adult friends below standing on the lawn pointing up and cheering, confetti and ribbon streamers raining gently down. The gold clubhouse is plain and smooth with no writing on it. In the final second, all motion eases and the camera settles into a slow, steady, perfectly straight forward drift, holding on the majestic hovering arrival, ready to continue.
Throughout the ENTIRE shot there are EXACTLY three Crasher mascots in total (one orange zigzag, one blue diamond, one green paint-splatter) and EXACTLY one star mascot in total — the same four characters from the first frame to the last; no additional, duplicate, background, distant or partial mascots ever appear anywhere in the frame at any moment. Every human being in the scene is a young adult in their 20s or 30s — absolutely no human children, no babies, no toddlers, no minors, no middle-aged people, no elderly people, nobody with gray hair, no small human figures of any kind anywhere in frame or background; the only child-sized figures allowed are the three vinyl-toy Crasher mascots in their hooded onesies.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### photo.mp4 (scene 3)

```
Single continuous cinematic camera move, no cuts. Cinematic photorealistic live-action hybrid footage, wide 16:9 landscape, shallow depth of field, real textures. Smooth, graceful, slow camera motion, subtle parallax. Absolutely no text, no captions, no logos, no lettering or writing on any object. The camera continues the exact same slow, steady forward drift it was already in, descending gently from the hovering cloud into the heart of the glowing backyard party as the three CRASHERS — small toddler-sized creatures whose bodies are simple ROUND hooded onesies, soft round hooded baby-suit silhouettes, NOT shaped like bolts or diamonds or splats, the patterns only the FABRIC PRINT of each onesie: one onesie in orange fabric with a yellow zigzag print, one in blue fabric with a purple diamond print, one in green fabric with a multicolor paint-splatter print, each with a pale round face peeking out of its snug hood, big sparkly jewel-like eyes, rosy round blush cheeks, a tiny happy smile, and a red-and-white striped cone party hat on top of the hood — LEAP one after another off the cloud's front deck and land softly on the lawn in little bounces, tumbling into a playful run, chasing each other in circles around the laughing young adult friends and diving through drifts of confetti, active and free — nobody holds or carries them — while STARRY — a tall golden five-pointed star character with a friendly cartoon face on the star body, large cartoon eyes with white sclera and blue irises, thin black eyebrows, a happy open smile, wearing a pink polka-dot cone party hat, with rainbow-checkered fabric arms and legs, puffy white four-fingered cartoon gloves, and round shiny golden boots — hops down last with puffy white gloves spread wide and dances behind the group, phone flashes popping softly as the friends laugh and snap photos of the chaos, confetti still drifting down through the warm string-light glow, the cloud drifting up and out of frame overhead. The camera eases back and glides forward across the lawn as the friends and the four characters gather together facing the camera. In the final second, all motion eases and the camera settles into a slow, steady, perfectly straight forward drift onto the settled group-photo moment, ready to continue.
Throughout the ENTIRE shot there are EXACTLY three Crasher mascots in total (one orange zigzag, one blue diamond, one green paint-splatter) and EXACTLY one star mascot in total — the same four characters from the first frame to the last; no additional, duplicate, background, distant or partial mascots ever appear anywhere in the frame at any moment. Every human being in the scene is a young adult in their 20s or 30s — absolutely no human children, no babies, no toddlers, no minors, no middle-aged people, no elderly people, nobody with gray hair, no small human figures of any kind anywhere in frame or background; the only child-sized figures allowed are the three vinyl-toy Crasher mascots in their hooded onesies.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### patio.mp4 (scene 4)

```
Single continuous cinematic camera move, no cuts. Cinematic photorealistic live-action hybrid footage, wide 16:9 landscape, shallow depth of field, real textures. Smooth, graceful, slow camera motion, subtle parallax. Absolutely no text, no captions, no logos, no lettering or writing on any object. The camera continues the exact same slow, steady, perfectly straight forward drift it was already in, gliding in under a pergola wrapped in warm string lights, where a young adult host in his 20s carries a big birthday cake topped with lit sparklers to the long table while a lively circle of young adult friends in their 20s and 30s around the table cheer and clap. The three CRASHERS — small toddler-sized creatures whose bodies are simple ROUND hooded onesies, soft round hooded baby-suit silhouettes, NOT shaped like bolts or diamonds or splats, the patterns only the FABRIC PRINT of each onesie: one onesie in orange fabric with a yellow zigzag print, one in blue fabric with a purple diamond print, one in green fabric with a multicolor paint-splatter print, each with a pale round face peeking out of its snug hood, big sparkly jewel-like eyes, rosy round blush cheeks, a tiny happy smile, and a red-and-white striped cone party hat on top of the hood — bounce excitedly at the table edge, one proudly holding up a stack of paper plates. No cloud or clubhouse is in frame. In the final second, all motion eases and the camera settles into a slow, steady, perfectly straight forward drift facing the cake table, holding on the candlelight, ready to continue.
Throughout the ENTIRE shot there are EXACTLY three Crasher mascots in total (one orange zigzag, one blue diamond, one green paint-splatter) and EXACTLY one star mascot in total — the same four characters from the first frame to the last; no additional, duplicate, background, distant or partial mascots ever appear anywhere in the frame at any moment. Every human being in the scene is a young adult in their 20s or 30s — absolutely no human children, no babies, no toddlers, no minors, no middle-aged people, no elderly people, nobody with gray hair, no small human figures of any kind anywhere in frame or background; the only child-sized figures allowed are the three vinyl-toy Crasher mascots in their hooded onesies.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### sendoff.mp4 (scene 5)

```
Single continuous cinematic camera move, no cuts. Cinematic photorealistic live-action hybrid footage, wide 16:9 landscape, shallow depth of field, real textures. Smooth, graceful, slow camera motion, subtle parallax. Absolutely no text, no captions, no logos, no lettering or writing on any object. The camera continues the exact same slow, steady, perfectly straight forward drift it was already in, drifting over the lawn as the party winds down into deep blue dusk, where STARRY — a tall golden five-pointed star character with a friendly cartoon face on the star body, large cartoon eyes with white sclera and blue irises, thin black eyebrows, a happy open smile, wearing a pink polka-dot cone party hat, with rainbow-checkered fabric arms and legs, puffy white four-fingered cartoon gloves, and round shiny golden boots — waves goodbye with a puffy white glove, and the three CRASHERS — small toddler-sized creatures whose bodies are simple ROUND hooded onesies, soft round hooded baby-suit silhouettes, NOT shaped like bolts or diamonds or splats, the patterns only the FABRIC PRINT of each onesie: one onesie in orange fabric with a yellow zigzag print, one in blue fabric with a purple diamond print, one in green fabric with a multicolor paint-splatter print, each with a pale round face peeking out of its snug hood, big sparkly jewel-like eyes, rosy round blush cheeks, a tiny happy smile, and a red-and-white striped cone party hat on top of the hood — wave with both hands beside him on the grass. Facing them, a lively circle of young adult friends in their 20s and 30s stand together on the lawn waving back, a faint golden sparkle trail rising off the group into the night sky behind Starry and the Crashers. No cloud or clubhouse is in frame. In the final second, all motion eases and the camera settles into a slow, steady, perfectly straight upward drift gazing at the faint sparkle trail rising into the starry sky, ready to continue.
Throughout the ENTIRE shot there are EXACTLY three Crasher mascots in total (one orange zigzag, one blue diamond, one green paint-splatter) and EXACTLY one star mascot in total — the same four characters from the first frame to the last; no additional, duplicate, background, distant or partial mascots ever appear anywhere in the frame at any moment. Every human being in the scene is a young adult in their 20s or 30s — absolutely no human children, no babies, no toddlers, no minors, no middle-aged people, no elderly people, nobody with gray hair, no small human figures of any kind anywhere in frame or background; the only child-sized figures allowed are the three vinyl-toy Crasher mascots in their hooded onesies.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

---

## ADULT — MOBILE (portrait 1080x1920)

### quiet-m.mp4

```
Single continuous cinematic camera move, no cuts. Cinematic photorealistic live-action hybrid footage, vertical 9:16, shallow depth of field, real textures. Smooth, graceful, slow camera motion, subtle parallax. Absolutely no text, no captions, no logos, no lettering or writing on any object. The camera begins inside a modest, quiet backyard birthday dinner for a GROWN ADULT in late golden afternoon light — a small circle of young adult friends in their 20s and 30s making polite conversation around the picnic table with its plain white sheet cake, one guest checking their watch, a lone half-deflated pastel balloon tied to the fence post. Ordinary real humans only — absolutely no cartoon characters, no mascots, no costumed figures, no toys, no animated creatures of any kind anywhere in the scene. The camera glides gently forward through the flat little party and drifts slowly among the guests as the quiet dinner winds down, conversation trailing off, the golden light softening toward dusk. Nothing in the sky above the rooftops for most of the shot — only ordinary dusk clouds and darkening blue. In the final second, all motion eases into a slow, steady, perfectly level drift, and a faint warm golden shimmer quietly begins to glow low in the dusk sky above the rooftops — subtle, distant, and unexplained: a soft diffuse glow only, no characters, no cloud shape, no clubhouse, no object or figure of any kind in the sky beyond that gentle glow.
Every human being in the scene is a young adult in their 20s or 30s — absolutely no human children, no babies, no toddlers, no minors, no middle-aged people, no elderly people, nobody with gray hair, no small human figures of any kind anywhere in frame or background; the only child-sized figures allowed are the three vinyl-toy Crasher mascots in their hooded onesies.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### glowup-m.mp4

```
Single continuous cinematic camera move, no cuts. Cinematic photorealistic live-action hybrid footage, vertical 9:16, shallow depth of field, real textures. Smooth, graceful, slow camera motion, subtle parallax. Absolutely no text, no captions, no logos, no lettering or writing on any object. The camera opens on the warm golden glow pulsing low over the dark rooftops of a quiet neighborhood at dusk, and the glow suddenly flares and breaks open as the magical cloud clubhouse BURSTS through it above the rooftops, already descending, banking gently toward us with its golden sparkle trail streaming behind it, paper lanterns rushing up past the camera and warm string lights flickering on below as the little backyard party grows steadily closer beneath the cloud's fluffy edge, until the cloud sweeps in over the wooden fence like a parade float — a purple confetti cannon on the cloud deck already blasting a continuous thick jet of confetti out over the fence during the sweep, confetti cascading off the cloud's edges in sheets — and settles into a majestic hover above the backyard, the sky all around the cloud filled with drifting confetti: STARRY — a tall golden five-pointed star character with a friendly cartoon face on the star body, large cartoon eyes with white sclera and blue irises, thin black eyebrows, a happy open smile, wearing a pink polka-dot cone party hat, with rainbow-checkered fabric arms and legs, puffy white four-fingered cartoon gloves, and round shiny golden boots — waves from the balcony rail, and the three CRASHERS — small toddler-sized creatures whose bodies are simple ROUND hooded onesies, soft round hooded baby-suit silhouettes, NOT shaped like bolts or diamonds or splats, the patterns only the FABRIC PRINT of each onesie: one onesie in orange fabric with a yellow zigzag print, one in blue fabric with a purple diamond print, one in green fabric with a multicolor paint-splatter print, each with a pale round face peeking out of its snug hood, big sparkly jewel-like eyes, rosy round blush cheeks, a tiny happy smile, and a red-and-white striped cone party hat on top of the hood — ride the front deck of the cloud waving down, the confetti cannon still blasting its continuous thick jet of confetti, more confetti cascading off the cloud deck in sheets, the young adult friends below standing on the lawn pointing up and cheering through the drifting confetti filling the sky around the cloud. The gold clubhouse is plain and smooth with no writing on it. In the final second, all motion eases and the camera settles into a slow, steady, perfectly straight forward drift, holding on the majestic hovering arrival, the cannon still firing and confetti still drifting thick around the cloud, ready to continue.
Throughout the ENTIRE shot there are EXACTLY three Crasher mascots in total (one orange zigzag, one blue diamond, one green paint-splatter) and EXACTLY one star mascot in total — the same four characters from the first frame to the last; no additional, duplicate, background, distant or partial mascots ever appear anywhere in the frame at any moment. Every human being in the scene is a young adult in their 20s or 30s — absolutely no human children, no babies, no toddlers, no minors, no middle-aged people, no elderly people, nobody with gray hair, no small human figures of any kind anywhere in frame or background; the only child-sized figures allowed are the three vinyl-toy Crasher mascots in their hooded onesies.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### photo-m.mp4

```
Single continuous cinematic camera move, no cuts. Cinematic photorealistic live-action hybrid footage, vertical 9:16, shallow depth of field, real textures. Smooth, graceful, slow camera motion, subtle parallax. Absolutely no text, no captions, no logos, no lettering or writing on any object. The camera continues the exact same slow, steady forward drift it was already in, descending gently from the hovering cloud into the heart of the glowing backyard party, the air already completely filled edge-to-edge with an overwhelming, screen-filling blizzard of colorful confetti so dense and constant it never lets up for a single moment of the shot, as the three CRASHERS — small toddler-sized creatures whose bodies are simple ROUND hooded onesies, soft round hooded baby-suit silhouettes, NOT shaped like bolts or diamonds or splats, the patterns only the FABRIC PRINT of each onesie: one onesie in orange fabric with a yellow zigzag print, one in blue fabric with a purple diamond print, one in green fabric with a multicolor paint-splatter print, each with a pale round face peeking out of its snug hood, big sparkly jewel-like eyes, rosy round blush cheeks, a tiny happy smile, and a red-and-white striped cone party hat on top of the hood — LEAP one after another off the cloud's front deck and land softly on the lawn in little bounces, tumbling into a playful run, chasing each other in circles around the laughing young adult friends, massive volumes of confetti swirling thick and heavy around the leaping Crashers in every direction and blanketing the entire lawn in deep drifts underfoot, active and free — nobody holds or carries them — while STARRY — a tall golden five-pointed star character with a friendly cartoon face on the star body, large cartoon eyes with white sclera and blue irises, thin black eyebrows, a happy open smile, wearing a pink polka-dot cone party hat, with rainbow-checkered fabric arms and legs, puffy white four-fingered cartoon gloves, and round shiny golden boots — hops down last with puffy white gloves spread wide and dances behind the group as thick unbroken torrents of confetti keep pouring down all around him, phone flashes popping softly as the friends laugh and snap photos of the chaos through a dense, ever-falling curtain of confetti raining down nonstop through the entire shot with no letup at any point, swirling and glittering through the warm string-light glow; the cloud drifts up and out of frame overhead, but the enormous blizzard of confetti it already released keeps falling like heavy snow for the rest of the shot, completely unaffected by the cloud leaving. Then, in the same single unbroken camera move with absolutely no cut, no jump, and no scene change, the camera glides smoothly across the lawn toward the wooden picnic table as the friends and the four characters all walk over together and gather behind it facing the camera, the near edge of the picnic table rising gently into the bottom foreground of the frame as the camera arrives in one continuous motion, that same heavy snowfall of confetti still pouring down through the air all around and between every person in the group without a single break, several pieces tumbling right past the camera lens in the foreground, on top of the deep drifts of confetti already carpeting the ground underfoot. In the final second, all motion eases and the camera settles into a slow, steady, perfectly straight forward drift onto the settled group-photo moment — even as everyone holds the pose and smiles for the photo, that same heavy snowfall of confetti keeps falling steadily through the entire frame right up to the very last frame, thick and unbroken, never thinning, never clearing, ready to continue.
Throughout the ENTIRE shot there are EXACTLY three Crasher mascots in total (one orange zigzag, one blue diamond, one green paint-splatter) and EXACTLY one star mascot in total — the same four characters from the first frame to the last; no additional, duplicate, background, distant or partial mascots ever appear anywhere in the frame at any moment. Every human being in the scene is a young adult in their 20s or 30s — absolutely no human children, no babies, no toddlers, no minors, no middle-aged people, no elderly people, nobody with gray hair, no small human figures of any kind anywhere in frame or background; the only child-sized figures allowed are the three vinyl-toy Crasher mascots in their hooded onesies.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### patio-m.mp4

```
Single continuous cinematic camera move, no cuts. Cinematic photorealistic live-action hybrid footage, vertical 9:16, shallow depth of field, real textures. Smooth, graceful, slow camera motion, subtle parallax. Absolutely no text, no captions, no logos, no lettering or writing on any object. The camera continues the exact same slow, steady, perfectly straight forward drift it was already in, gliding in under a pergola wrapped in warm string lights, where a young adult host in his 20s carries a big birthday cake topped with lit sparklers to the long table while a lively circle of young adult friends in their 20s and 30s around the table cheer and clap. The three CRASHERS — small toddler-sized creatures whose bodies are simple ROUND hooded onesies, soft round hooded baby-suit silhouettes, NOT shaped like bolts or diamonds or splats, the patterns only the FABRIC PRINT of each onesie: one onesie in orange fabric with a yellow zigzag print, one in blue fabric with a purple diamond print, one in green fabric with a multicolor paint-splatter print, each with a pale round face peeking out of its snug hood, big sparkly jewel-like eyes, rosy round blush cheeks, a tiny happy smile, and a red-and-white striped cone party hat on top of the hood — bounce excitedly at the table edge, one proudly holding up a stack of paper plates. Already well before this moment, Starry has quietly taken up a spot far in the background, over by the string-light fence line, well behind and off to the side of the seated crowd — a small, distant, person-sized figure, the same height as the adult guests, partly hidden behind the standing friends. He stays planted in that one distant background spot, completely still, for the entire rest of the shot: he does not step, walk, hop, lean, reach, or move toward the table or toward the camera at any point, and he never crosses near the lens. The camera itself only ever pushes straight forward and slightly downward toward the cake and candles, tilting away from the sky and away from Starry's distant spot, so his small distant figure simply falls outside the shrinking frame edges on its own as the shot tightens — by the tightest candle close-up he has already been outside the frame for some time, with no part of him — no face, no eyes, no mouth, no hat, no gloved hand — visible anywhere in that shot. That tightest close-up shows only the cake, the candles, their sparkler and flames, and the blurred hands/shoulders of the nearest seated adults, with soft dark out-of-focus foliage and fence above the cake — never a golden star shape of any size anywhere in that framing. At no point does Starry ever appear large, close, behind the cake, above the cake, or looming — he is a small, still, distant background figure the whole time, then simply off-camera. No cloud or clubhouse is in frame. In the final second, all motion eases and the camera settles into a slow, steady, perfectly straight forward drift facing the cake table, holding on the candlelight, ready to continue.
Every human being in the scene is a young adult in their 20s or 30s — absolutely no human children, no babies, no toddlers, no minors, no middle-aged people, no elderly people, nobody with gray hair, no small human figures of any kind anywhere in frame or background; the only child-sized figures allowed are the three vinyl-toy Crasher mascots in their hooded onesies.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*

### sendoff-m.mp4

```
Single continuous cinematic camera move, no cuts. Cinematic photorealistic live-action hybrid footage, vertical 9:16, shallow depth of field, real textures. Smooth, graceful, slow camera motion, subtle parallax. Absolutely no text, no captions, no logos, no lettering or writing on any object. The camera continues the exact same slow, steady, perfectly straight forward drift it was already in, drifting over the lawn as the party winds down into deep blue dusk, where STARRY — a tall golden five-pointed star character with a friendly cartoon face on the star body, large cartoon eyes with white sclera and blue irises, thin black eyebrows, a happy open smile, wearing a pink polka-dot cone party hat, with rainbow-checkered fabric arms and legs, puffy white four-fingered cartoon gloves, and round shiny golden boots — waves goodbye with a puffy white glove, and the three CRASHERS — small toddler-sized creatures whose bodies are simple ROUND hooded onesies, soft round hooded baby-suit silhouettes, NOT shaped like bolts or diamonds or splats, the patterns only the FABRIC PRINT of each onesie: one onesie in orange fabric with a yellow zigzag print, one in blue fabric with a purple diamond print, one in green fabric with a multicolor paint-splatter print, each with a pale round face peeking out of its snug hood, big sparkly jewel-like eyes, rosy round blush cheeks, a tiny happy smile, and a red-and-white striped cone party hat on top of the hood — wave with both hands beside him on the grass. Facing them, a lively circle of young adult friends in their 20s and 30s stand together on the lawn waving back, a faint golden sparkle trail rising off the group into the night sky behind Starry and the Crashers. No cloud or clubhouse is in frame. In the final second, all motion eases and the camera settles into a slow, steady, perfectly straight upward drift gazing at the faint sparkle trail rising into the starry sky, ready to continue.
Every human being in the scene is a young adult in their 20s or 30s — absolutely no human children, no babies, no toddlers, no minors, no middle-aged people, no elderly people, nobody with gray hair, no small human figures of any kind anywhere in frame or background; the only child-sized figures allowed are the three vinyl-toy Crasher mascots in their hooded onesies.
```

*Duration: 8s*
*Uses reference image(s) — exact files are in the matching .json job record and the PNGs beside it in the same work folder.*
