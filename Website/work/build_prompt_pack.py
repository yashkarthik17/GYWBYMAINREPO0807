"""Assemble the complete manual-Higgsfield pack on the Desktop.

Prompts for every shot (adult NEW 7-shot chain with revised anti-pop-in
prompts; kids original chain with the keep-moving ending appended), both
orientations, plus every current-cast reference image. Run from Website/.
"""
import io, os, shutil, glob

PACK = r"C:\Users\yashk\Desktop\GYWBT-Higgsfield-Pack"
for sub in ["adult-desktop", "adult-mobile", "kids-desktop", "kids-mobile",
            "reference-images/characters", "reference-images/adult-desktop",
            "reference-images/adult-mobile", "reference-images/kids"]:
    os.makedirs(os.path.join(PACK, sub), exist_ok=True)

STARRY = "STARRY \u2014 a tall golden five-pointed star character with a friendly cartoon face on the star body, large cartoon eyes with white sclera and blue irises, thin black eyebrows, a happy open smile, wearing a pink polka-dot cone party hat, with rainbow-checkered fabric arms and legs, puffy white four-fingered cartoon gloves, and round shiny golden boots"
CRASHERS = "the three CRASHERS \u2014 small toddler-sized creatures whose bodies are simple ROUND hooded onesies, soft round hooded baby-suit silhouettes, NOT shaped like bolts or diamonds or splats, the patterns only the FABRIC PRINT of each onesie: one onesie in orange fabric with a yellow zigzag print, one in blue fabric with a purple diamond print, one in green fabric with a multicolor paint-splatter print, each with a pale round face peeking out of its snug hood, big sparkly jewel-like eyes, rosy round blush cheeks, a tiny happy smile, and a red-and-white striped cone party hat on top of the hood"
GUARD4 = "Throughout the ENTIRE shot there are EXACTLY three Crasher mascots in total (one orange zigzag, one blue diamond, one green paint-splatter) and EXACTLY one star mascot in total \u2014 the same four characters from the first frame to the last; no additional, duplicate, background, distant or partial mascots ever appear anywhere in the frame at any moment. "
HUMANS = "Every human being in the scene is a young adult in their 20s or 30s \u2014 absolutely no human children, no babies, no toddlers, no minors, no middle-aged people, no elderly people, nobody with gray hair, no small human figures of any kind anywhere in frame or background; the only child-sized figures allowed are the three vinyl-toy Crasher mascots in their hooded onesies."
HUMANS_ONLY = "Every human being in the scene is a young adult in their 20s or 30s \u2014 absolutely no human children, no babies, no toddlers, no minors, no middle-aged people, no elderly people, nobody with gray hair, no small human figures of any kind anywhere in frame or background."
OPEN = "Single continuous cinematic camera move, no cuts. Cinematic photorealistic live-action hybrid footage, wide 16:9 landscape, shallow depth of field, real textures. Smooth, graceful, slow camera motion, subtle parallax. Absolutely no text, no captions, no logos, no lettering or writing on any object. "
KEEP = "The camera keeps its slow, steady drift with visible motion through the very last frame \u2014 no slowdown, no settling, no static hold at any point.\n"

ADULT = {
    "01-quiet": OPEN + "The camera begins inside a modest, quiet backyard birthday dinner for a GROWN ADULT in late golden afternoon light \u2014 a small circle of young adult friends in their 20s and 30s making polite conversation around the picnic table with its plain white sheet cake, one guest checking their watch, a lone half-deflated pastel balloon tied to the fence post. Ordinary real humans only \u2014 absolutely no cartoon characters, no mascots, no costumed figures, no toys, no animated creatures of any kind anywhere in the scene. The camera glides gently forward through the flat little party and drifts slowly among the guests as the quiet dinner winds down, conversation trailing off, the golden light softening toward dusk. Nothing in the sky above the rooftops for most of the shot \u2014 only ordinary dusk clouds and darkening blue. Near the end, a faint warm golden shimmer quietly begins to glow low in the dusk sky above the rooftops \u2014 subtle, distant, and unexplained: a soft diffuse glow only, no characters, no cloud shape, no clubhouse, no object or figure of any kind in the sky beyond that gentle glow. " + KEEP + "Strict continuity: the lighting stays constant with no flashes, flickers or strobing; apart from the sky shimmer's gradual appearance, no object, prop, person or light source appears, disappears, duplicates or changes anywhere in the frame mid-shot.\n" + HUMANS,
    "02-glowup": OPEN + "The camera opens on the warm golden glow pulsing low over the dark rooftops of a quiet neighborhood at dusk, and the glow suddenly flares and breaks open as the magical cloud clubhouse BURSTS through it above the rooftops, already descending, banking gently toward us with its golden sparkle trail streaming behind it. In one smooth continuous approach, the cloud glides in over the wooden fence and eases into a stately hover above the backyard. On the balcony rail stands " + STARRY + " \u2014 waving one puffy glove, while " + CRASHERS + " \u2014 stand together on the cloud's front deck. Below, the young adult friends look up from the lawn, smiling and pointing. One single soft burst of colorful confetti drifts slowly down from the cloud through the warm string-light glow. The gold clubhouse is plain and smooth with no writing on it. " + KEEP + "Strict continuity: the lighting stays constant with no flashes, flickers or strobing; apart from the cloud clubhouse's single scripted arrival and the one confetti burst, no object, prop, character or light source appears, disappears, duplicates or changes anywhere in the frame mid-shot.\n" + GUARD4 + HUMANS,
    "03-conn-jump": OPEN + "The camera continues the exact same slow, steady forward drift it was already in, watching the cloud clubhouse hovering above the glowing backyard as " + CRASHERS + " \u2014 leap one after another off the cloud's front deck and land softly on the lawn in gentle little bounces, and " + STARRY + " \u2014 hops down last, spreading his puffy white gloves wide as he lands. This is the only action in the shot: four characters descending from the cloud to the lawn, one at a time, while the young adult friends watch smiling from beside the table. As the last character lands, the empty cloud drifts slowly upward out of the top of the frame. " + KEEP + "Strict continuity: the lighting stays constant with no flashes, flickers or strobing; no object, prop, character or light source appears, disappears, duplicates or changes anywhere in the frame mid-shot; the only movements are the four scripted landings and the cloud's single slow exit upward.\n" + GUARD4 + HUMANS,
    "04-photo": OPEN + "The camera continues the exact same slow, steady forward drift it was already in, gliding across the warmly lit lawn where the whole group is already gathered together: the young adult friends stand in a loose happy cluster, and with them are " + STARRY + " \u2014 standing tall at the center with his gloves spread wide, and " + CRASHERS + " \u2014 posing playfully at the front of the group. This is the only action in the shot: two of the friends hold their phones up with softly glowing screens \u2014 absolutely NO camera flashes, no flash pops, no strobing, the warm string-light glow stays perfectly constant \u2014 and everyone laughs and settles shoulder-to-shoulder into a loose group-photo pose facing the camera, a few pieces of leftover confetti drifting gently down. " + KEEP + "Strict continuity: the lighting stays constant with no flashes, flickers or strobing; no object, prop, character or light source appears, disappears, duplicates or changes anywhere in the frame mid-shot; no cloud or clubhouse is in frame at any point.\n" + GUARD4 + HUMANS,
    "05-conn-cake": OPEN + "The camera glides slowly alongside a young adult host in his 20s as he carries a big birthday cake topped with tall lit birthday candles \u2014 steady, warm, unwavering little flames, no sparklers, no fireworks \u2014 walking carefully in under a pergola wrapped in warm string lights toward a long wooden table. This is the only action in the shot: the candlelit cake traveling through the warm evening light, the young adult friends at the table turning their heads to watch it arrive, faces lighting up with smiles. No cartoon characters, no mascots, no costumed figures anywhere in this shot \u2014 ordinary real humans only. " + KEEP + "Strict continuity: the lighting stays constant with no flashes, flickers or strobing \u2014 the candle flames burn steadily; no object, prop, person or light source appears, disappears, duplicates or changes anywhere in the frame mid-shot.\n" + HUMANS_ONLY,
    "06-patio": OPEN + "The camera continues the exact same slow, steady forward drift it was already in, moving in over a long wooden table under a pergola wrapped in warm string lights, where the big birthday cake now sits at the center of the table, its tall birthday candles burning with steady, warm, unwavering little flames \u2014 no sparklers, no fireworks. This is the only action in the shot: the lively circle of young adult friends in their 20s and 30s around the table clap and cheer for the birthday moment, " + STARRY + " \u2014 stands tall behind the circle clapping his puffy white gloves, and " + CRASHERS + " \u2014 stand together at the table edge bouncing gently on their toes with excitement, hands free, holding nothing. No cloud or clubhouse is in frame. " + KEEP + "Strict continuity: the lighting stays constant with no flashes, flickers or strobing \u2014 the candle flames burn steadily; no object, prop, character or light source appears, disappears, duplicates or changes anywhere in the frame mid-shot.\n" + GUARD4 + HUMANS,
    "07-sendoff": OPEN + "The camera continues the exact same slow, steady, perfectly straight forward drift it was already in, drifting over the lawn as the party winds down into deep blue dusk, where " + STARRY + " \u2014 waves goodbye with a puffy white glove, and " + CRASHERS + " \u2014 wave with both hands beside him on the grass. Facing them, a lively circle of young adult friends in their 20s and 30s stand together on the lawn waving back, a faint golden sparkle trail rising off the group into the night sky behind Starry and the Crashers. No cloud or clubhouse is in frame. In the final second, all motion eases and the camera settles into a slow, steady, perfectly straight upward drift gazing at the faint sparkle trail rising into the starry sky, ready to continue.\nStrict continuity: the lighting stays constant with no flashes, flickers or strobing; no object, prop, character or light source appears, disappears, duplicates or changes anywhere in the frame mid-shot.\n" + GUARD4 + HUMANS,
}

for name, text in ADULT.items():
    io.open(os.path.join(PACK, "adult-desktop", name + ".txt"), "w",
            encoding="utf-8", newline="\n").write(text + "\n")
    io.open(os.path.join(PACK, "adult-mobile", name + ".txt"), "w",
            encoding="utf-8", newline="\n").write(
        text.replace("wide 16:9 landscape", "vertical 9:16") + "\n")

KIDS_KEEP = " The camera keeps moving through the entire shot \u2014 it is still traveling with visible motion on the very last frame. No slowdown, no settling, no static hold at the beginning or end."
KIDS = [("01-beige", "dive_beige"), ("02-conn1", "conn_1"), ("03-crashpad", "dive_crashpad"),
        ("04-conn2", "conn_2"), ("05-crash", "dive_crash"), ("06-conn3", "conn_3"),
        ("07-glowup", "dive_glowup"), ("08-conn4", "conn_4"), ("09-finale", "dive_finale")]
for out, base in KIDS:
    t = io.open(f"work/{base}.txt", encoding="utf-8").read().strip()
    io.open(os.path.join(PACK, "kids-desktop", out + ".txt"), "w",
            encoding="utf-8", newline="\n").write(t + KIDS_KEEP + "\n")
    tp = io.open(f"work/p{base}.txt", encoding="utf-8").read().strip()
    io.open(os.path.join(PACK, "kids-mobile", out + ".txt"), "w",
            encoding="utf-8", newline="\n").write(tp + KIDS_KEEP + "\n")

def cp(src, dstdir, newname=None):
    shutil.copy2(src, os.path.join(PACK, dstdir, newname or os.path.basename(src)))

for f in glob.glob("adult/work/redo2/refs/*.png"):
    cp(f, "reference-images/characters")
AD = {"lstill_1.png": "scene1-quiet-still.png", "lstill_2.png": "scene2-glowup-still.png",
      "lstill_2b.png": "scene2b-glowup-alt-still.png", "lstill_3.png": "scene3-photo-still.png",
      "lstill_4.png": "scene4-patio-still.png", "lstill_5.png": "scene5-sendoff-still.png",
      "lstart_3.png": "scene3-start-frame.png", "lstart_4.png": "scene4-start-frame.png",
      "lstart_5.png": "scene5-start-frame.png", "lpstill_4.png": "scene4-alt-still.png",
      "lpstill_5.png": "scene5-alt-still.png"}
for src, dst in AD.items():
    p = "adult/work/redo2/" + src
    if os.path.exists(p):
        cp(p, "reference-images/adult-desktop", dst)
AM = {"pstill_1.png": "scene1-quiet-still.png", "pstill_2.png": "scene2-glowup-still.png",
      "pstill_2b.png": "scene2b-glowup-alt-still.png", "pstill_3.png": "scene3-photo-still.png",
      "pstill_3b.png": "scene3b-photo-alt-still.png", "pstill_5.png": "scene5-sendoff-still.png",
      "start_leg2.png": "scene2-start-frame.png", "start_leg3.png": "scene3-start-frame.png",
      "start_leg4.png": "scene4-start-frame.png", "start_leg5.png": "scene5-start-frame.png"}
for src, dst in AM.items():
    p = "adult/work/redo2/" + src
    if os.path.exists(p):
        cp(p, "reference-images/adult-mobile", dst)
for n in ["beige", "crashpad", "crash", "glowup", "finale"]:
    for suffix, tag in [(".webp", "-landscape"), ("-p.webp", "-portrait")]:
        p = f"assets/{n}{suffix}"
        if os.path.exists(p):
            cp(p, "reference-images/kids", n + tag + ".webp")

README = """# GYWBT Higgsfield Pack \u2014 regenerate the journey clips manually

## Settings (every clip)
- Model: **Seedance 2.0**
- Scenes: **8 s** \u00b7 Connectors (kids conns + adult conn-jump / conn-cake): **6\u20138 s**
- adult-desktop + kids-desktop prompts: 1920x1080 \u00b7 *-mobile prompts: 1080x1920
- No audio needed (the site strips it)

## What changed vs the old renders (why re-run)
1. Every prompt now DEMANDS motion through the last frame \u2014 the old "eases and
   settles" endings are what created the pause at every stitched seam.
2. Adult scenes 2/3/4 are de-crammed \u2014 one action per shot \u2014 and the adult
   journey is now 7 shots: quiet, glowup, conn-jump (NEW wordless), photo,
   conn-cake (NEW wordless), patio, sendoff.
3. Anti-artifact rules are baked in: no camera flashes (steady phone-screen
   glow instead), candles instead of sparklers, and a strict-continuity clause
   against pop-in/pop-out of objects and characters.

## Reference images
- reference-images/characters/ \u2014 Starry + Crashers turnaround sheets: attach to
  ANY shot that contains the mascots for consistent character design.
- reference-images/adult-desktop|adult-mobile/ \u2014 the anchor stills/start frames
  the current shipped adult clips were generated from. Use the matching one as
  the image reference to keep each scene's world consistent.
- reference-images/kids/ \u2014 the kids scene artwork (landscape + portrait).
- CONTINUITY TIP: for each shot after the first, the strongest anchor is the
  LAST FRAME of your new render of the previous shot \u2014 export it and attach it
  as the start reference. (Claude can extract these frames for you.)

## Delivering the new renders
Drop everything in one folder using these names (add -m for mobile versions):
- Adult: quiet.mp4 glowup.mp4 conn-jump.mp4 photo.mp4 conn-cake.mp4 patio.mp4 sendoff.mp4
- Kids:  beige.mp4 conn1.mp4 crashpad.mp4 conn2.mp4 crash.mp4 conn3.mp4 glowup.mp4 conn4.mp4 finale.mp4
Partial drops are fine \u2014 whatever you replace gets zero trims; the rest keeps
the current motion-derived trims. Claude re-stitches, rebuilds the adaptive
HLS ladders, rewires the timings, and deploys.
"""
io.open(os.path.join(PACK, "README.md"), "w", encoding="utf-8", newline="\n").write(README)
print("pack built at", PACK)
