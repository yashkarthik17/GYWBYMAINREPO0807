# Spanish-language support for both journeys — task report

Branch: `adult-overhaul` (verified before starting — no push, no `main` touched, no deploy).

Status: **DONE**

**Controller review round (2 fixes applied, separate small commit):**
1. Adult `quiet` eyebrow — "Sé honesto" was masculine-gendered for an unknown reader; replaced with the gender-neutral rhetorical idiom **"Seamos honestos"** ("let's be honest").
2. Kids `glowup` — body said "Torre de pasteles" while the tag said "Torre de pastel"; unified both to the singular **"Torre de pastel"** (matching the EN singular "Cake tower" concept).

Both fixes are reflected in the table below. `node --check` clean on both touched files; `git diff` confirmed exactly these two string edits, nothing else changed.

---

## 1. EN → ES string table (complete, for controller review)

Every field below is a real key in `story-config.js` / `adult-config.js` /
`index.html` / `music.js`. Where a joke/idiom needed adaptation rather than
literal translation, the adaptation is noted.

### 1.1 Envelope letter (`index.html`) — the only strings the live toggle re-renders

| Key | EN | ES | Note |
|---|---|---|---|
| grown choice | Glad You Were Born Today | Glad You Were Born Today | Kept English — functions as the site's brand wordmark here, not a sentence. Judgment call (see §4). |
| kids choice | Glad You Were Born Today (Kids) | Glad You Were Born Today (Para Niños) | Brand name kept, qualifier translated. |
| toggle (shown while page is EN) | — | Español | Shows the OTHER language, per spec. |
| toggle (shown while page is ES) | English | — | " |
| toggle aria-label (EN state) | Switch to Spanish | — | |
| toggle aria-label (ES state) | — | Cambiar a inglés | |

### 1.2 Shared chrome (identical text in both `story-config.js` and `adult-config.js`)

| Key | EN | ES |
|---|---|---|
| startLabel | Tap to play the story | Toca para reproducir la historia |
| skipLabel | Skip to end » | Saltar al final » |
| nextLabel (aria, "next scene" tap button) | Next scene | Siguiente escena |

### 1.3 Kids journey (`story-config.js`)

| Scene | Field | EN | ES |
|---|---|---|---|
| beige | eyebrow | Right now, somewhere | Ahora mismo, en algún lugar |
| beige | title | A birthday nobody noticed. | Un cumpleaños que nadie notó. |
| beige | body | The candles are lit. The cake is ready. And the room is quiet as a Tuesday. | Las velas están encendidas. El pastel está listo. Y el salón está tan callado como un martes cualquiera. |
| beige | tags | Droopy balloons / Polite clapping | Globos desinflados / Aplausos de cortesía |
| crashpad | eyebrow | But way up in the clouds | Pero allá arriba, en las nubes |
| crashpad | title | Somebody noticed. | Alguien sí lo notó. |
| crashpad | body | The party radar goes off in the Crash Pad, and Starry gives the only order there is: LET'S GO. | El radar de fiestas se activa en el Crash Pad, y Starry da la única orden que existe: ¡VAMOS! |
| crashpad | tags | Party radar / Confetti cannons | Radar de fiestas / Cañones de confeti |
| crash | eyebrow | 3… 2… 1… | 3… 2… 1… (unchanged — numerals) |
| crash | title | This party is officially crashed. | Esta fiesta acaba de ser invadida. ¡Oficialmente! |
| crash | body | Doors fly open. Color pours in. The quiet doesn't stand a chance. | Las puertas se abren de golpe. El color se desborda. El silencio no tiene ninguna oportunidad. |
| crash | tags | Confetti storm / Streamer trails | Tormenta de confeti / Estelas de serpentinas |
| glowup | eyebrow | Minutes later | Minutos después |
| glowup | title | Now THAT'S a birthday. | Eso sí es un cumpleaños. |
| glowup | body | Cake tower. Balloon arches. And right in the middle, one kid who can't stop grinning. | Torre de pastel. Arcos de globos. Y justo en el centro, un niño que no puede dejar de sonreír. |
| glowup | tags | Cake tower / Balloon arch / Dance floor | Torre de pastel / Arco de globos / Pista de baile |
| finale | eyebrow | From Starry & the Crashers | De parte de Starry y los Crashers |
| finale | title | Glad you were born today. | Qué bueno que naciste. |
| finale | body | Not the cake. Not the presents. You. That's the whole party. | No es el pastel. No son los regalos. Eres tú. Esa es toda la fiesta. |
| finale | explore.label | Explore the world | Explora el mundo |
| finale | explore link 1 | Meet the Crashers | Conoce a los Crashers |
| finale | explore link 2 | Play it again | Verlo de nuevo |

### 1.4 Adult journey (`adult-config.js`)

| Scene | Field | EN | ES |
|---|---|---|---|
| (top-level) | hint *(inert — see §3)* | scroll to crash the party | haz scroll para colarte en la fiesta |
| quiet | eyebrow | Be honest | Seamos honestos |
| quiet | title | Birthdays got smaller, didn't they. | Los cumpleaños se hicieron más pequeños, ¿verdad? |
| quiet | body | Somewhere between ten and forty, the parties turned into polite dinners that end by nine. | En algún punto entre los diez y los cuarenta, las fiestas se convirtieron en cenas educadas que terminan a las nueve. |
| quiet | tags | Polite toasts / Early goodbyes | Brindis de compromiso / Despedidas tempranas |
| glowup | eyebrow | Then the sky RSVPs | Entonces el cielo confirma asistencia |
| glowup | title | The Crashers crash in. | Los Crashers se cuelan. |
| glowup | body | One little cloud clears the fence. Nobody checks their phone again all night. | Una nubecita salta la cerca. Nadie vuelve a revisar su teléfono en toda la noche. |
| glowup | tags | Confetti included | Confeti incluido |
| photo | eyebrow | Say cheese | Digan "whisky" |
| photo | title | Photos worth fighting over. | Fotos por las que vale la pena pelear. |
| photo | body | Your friends are laughing in every single frame. | Tus amigos se ríen en cada foto. |
| patio | eyebrow | And 25ths. And 30ths. | Y los 25. Y los 30. |
| patio | title | Yes, they crash 20ths. | Sí, también se cuelan en los 20. |
| patio | body | **Enchantment doesn't card.** | **El encanto no pide identificación.** |
| sendoff | eyebrow | From Starry & the Crashers | De parte de Starry y los Crashers |
| sendoff | title | Glad you were born today. | Qué bueno que naciste. |
| sendoff | body | They wave until the lawn goes dark. And they never forget a date. | Se despiden con la mano hasta que el jardín se oscurece. Y jamás olvidan una fecha. |
| sendoff | explore.label | Explore | Explora |
| sendoff | explore link 1 | Hire the Crew | Contrata a la Tripulación |
| sendoff | explore link 2 | Meet the Crew | Conoce a la Tripulación |
| sendoff | explore link 3 | The Party Store | La Tienda de Fiestas |
| sendoff | explore link 4 | Our Mission | Nuestra Misión |
| sendoff | explore link 5 | Play it again | Verlo de nuevo |

### 1.5 Music button aria-labels (`music.js`, static per-page-load read — see §3)

| Key | EN | ES |
|---|---|---|
| aria-label (paused) | Play the theme song | Reproducir la canción |
| aria-label (playing) | Pause the theme song | Pausar la canción |

**~64 distinct string fields translated** (30 kids config + 28 adult config + 4 letter + 2 music aria-labels).

### Pun/joke adaptations (not literal translations)
- **"Enchantment doesn't card."** → **"El encanto no pide identificación."** — "to card" (check ID at the door) has no direct Spanish verb; "pedir identificación" (ask for ID) lands the same "no age limit on the magic" joke.
- **"Say cheese"** → **"Digan 'whisky'"** — the actual Latin-American photo-smile idiom (whisky's mouth-shape mimics a smile the way "cheese" does in English); a literal "di queso" would read as a mistranslation to native speakers.
- **"Then the sky RSVPs"** → **"Entonces el cielo confirma asistencia"** — "confirma asistencia" is the standard Spanish phrase for RSVP-ing yes, preserving the personification joke (the sky itself accepts the invitation).
- **"The Crashers crash in." / "they crash 20ths." / "This party is officially crashed."** → verb family built on **colarse** (to gatecrash/sneak in without invitation) and **invadir** (to invade, for passive titles) — the natural Spanish verbs for gatecrashing, used consistently everywhere the English pun on "crash" appears, instead of forcing literal "crashear" throughout.
- **"the Crashers"** kept as the proper-noun crew name (**"los Crashers"**) everywhere, exactly like **Starry** stays untranslated — both are character/brand names, not descriptions.
- **"Glad you were born today."** — this is the site's central refrain and appears as a heartfelt sign-off sentence at the end of BOTH journeys (kids finale, adult sendoff). Translated identically both places as **"Qué bueno que naciste."** (colloquial, warm — "how good that you were born") to keep the refrain consistent site-wide. The button-label instances of the same phrase ("Glad You Were Born Today" as the adult journey's CTA text) were judged to function as the brand wordmark instead, and were kept in English — see §4.

---

## 2. Architecture

**One-line summary:** Config-driven i18n — `GYWBT_KIDS_CONFIG(lang)` / `GYWBT_ADULT_CONFIG(lang)` now pick every user-facing string from an internal EN/ES table (assets/rates/ids untouched, single-sourced), the two tap-engines read their chrome text from `config.startLabel/skipLabel/nextLabel` instead of hardcoding it, and a ~5-line `gywbtLang()` helper (duplicated per file, reading `localStorage['gywbt-lang']` with `?lang=` URL override) resolves the active language everywhere with no shared new file.

Details:
- **State**: `localStorage['gywbt-lang']` = `'en'` (default) or `'es'`. `?lang=en|es` in the URL always wins and re-writes the stored value. Implemented as a tiny duplicated helper `gywbtLang()` in `index.html`'s inline script, `story-config.js`, and `adult-config.js` (identical ~6-line body in each, per the "duplicated is fine" guidance — no new shared file).
- **Letter toggle** (`index.html`): a new `.sheet-lang` button lives inside `#sheet` (the existing `.sheet-actions` container), styled smaller/lighter than the two `.sheet-btn` choices, showing the *other* language. Click toggles a `let lang` closure variable, writes it to `localStorage`, and calls `renderLetter()` which updates the two choice labels + the toggle's own text/aria-label in place — no reload. That same `lang` variable is passed straight into `GYWBT_KIDS_CONFIG(lang)` / `GYWBT_ADULT_CONFIG(lang)` at the in-page launch call sites, so the mounted journey always matches whatever the letter is currently showing.
- **Config strings**: `GYWBT_KIDS_STRINGS`/`GYWBT_ADULT_STRINGS` are `{en:{...}, es:{...}}` tables keyed by scene id, sitting above each `CONFIG(lang)` function. `CONFIG(lang)` resolves `lang` (explicit arg wins; otherwise `gywbtLang()`), picks `T = STRINGS[lang]`, and builds the same object shape as before with every `eyebrow/title/body/tags`, `explore.label`, and explore-link `label` pulled from `T`. Every asset path (`still/poster/clip/clipMobile/posterMobile`), every `rate/scroll/linger`, every `href`, and every scene `id` is untouched, unconditional code — verified byte-identical between the EN and ES config output (see §5 traces).
- **Engine chrome**: both `tap-engine.js` and `adult/tap-engine.js` already read `config.startLabel`/`config.skipLabel` with English hardcoded fallbacks; I added the missing `config.nextLabel || "Next scene"` for the tap button's aria-label (previously hardcoded unconditionally). The engines themselves stay 100% lang-agnostic — zero English/Spanish literals were added to either engine file.
- **Music button** (`music.js`): aria-labels ("Play/Pause the theme song") read `localStorage['gywbt-lang']`/`?lang=` once at button-build time and pick an EN/ES label pair. This is a **static, load-time-only** read — it does not react to the letter toggle being clicked later on the same page load, per the design brief's "only if trivial" instruction. Documented inline in `music.js` and in §3 below.
- **SEO blocks** (`data-sw-seo` in `story.html`/`adult/index.html`): left in English, deliberately — see §3.

---

## 3. Decisions and things intentionally left alone

- **`data-sw-seo` blocks stay English.** Single-URL site, no `/es/` route, so this is the only crawlable text search engines see. Localizing it would require a real URL split (hreflang, separate routes) which is out of scope for a client-rendered toggle.
- **`<html lang="en">` was left static on all three pages** (`index.html`, `story.html`, `adult/index.html`). Not explicitly requested, and dynamically flipping it would conflict with the SEO blocks staying English on the two standalone pages (the document would claim `lang="es"` while its only crawlable/no-JS content is English) — judged not worth the inconsistency for an unrequested feature. Flagging this as a deliberate omission, not an oversight.
- **Envelope page chrome outside the letter** — "Tap to Open" / "Seal it back" button text+aria-labels, the "Folding the paper…" loading text, and the two cinematic intro lines — was **left in English**. Design point 5 scopes "the letter's own visible text" to the two choice buttons (there is no separate body/greeting text on the sheet — verified by reading the full markup, `#sheet` contains only the two `<a>` tags), and the verification checklist in the task brief only exercises the letter/journey strings, not this page chrome. Trade-off noted: since the "Seal it back" button and the letter are visible simultaneously once the envelope is open, a Spanish visitor will see one English button next to a Spanish letter. This is a reasonable, contained follow-up if broader envelope-chrome localization is wanted later.
- **`hint` field in `adult-config.js`** and per-scene `label`/`scroll`/`linger` fields are leftovers from the retired scroll-scrubbing engine (`scrub-engine.js`, confirmed unused — not `<script src>`'d by any HTML file in the repo). `tap-engine.js` never reads `config.hint` or `section.label`. I translated `hint` anyway for table completeness/future-proofing (noted inline in `adult-config.js`) but left `section.label` (e.g. `'The Beige Party'`) as English-only since it's not in the design's enumerated field list and is dev-only/inert.
- **Music aria-labels are static, not live-reactive** to the in-page toggle click (see §2). Explicitly permitted by the design brief ("localize ONLY if trivial... otherwise leave English and note it") — full reactivity would need a `window.swMusic.setLang()` hook wired from the toggle handler, which is more than "trivial."
- **Shared-file side effect**: `music.js` is loaded by several out-of-scope pages too (`crashers.html`, `cards.html`, `games.html`, `adult/crew.html`, `store.html` — confirmed via repo-wide grep). Because it's the same physical file (only the `?v=` query differs, and those pages' queries were **not** bumped), my aria-label change is live at that URL for every consumer, not just the pages I own. Effect is limited to two aria-label strings (no visible text, no functional change) and only activates if a visitor has explicitly set `gywbt-lang=es` via the letter toggle or a `?lang=es` URL — this was the file's only owned touch-point available for the feature, so this reach was accepted rather than avoided. Called out here per the instructions.

### Brand-name judgment call ("Glad You Were Born Today")
Per the design brief's instruction to flag this: the phrase is used in **two different roles** on the site:
1. As a **sign-off sentence** directed at the reader (kids finale body-adjacent title, adult sendoff title) — translated: **"Qué bueno que naciste."**
2. As the **adult-journey CTA button label** on the letter (`.sheet-btn.grown`), where it reads as the site's brand wordmark rather than a sentence being spoken to the visitor — kept in **English** in both letter states.

I judged (1) as "reads as a sentence" and (2) as "functions as a logo/brand," per the brief's own disambiguation rule. This is a judgment call, not a certainty — an alternative reading would translate the button too (e.g. "Qué Bueno Que Naciste Hoy" as a title-cased CTA). Flagging for controller review.

---

## 4. Out-of-scope inventory (follow-up only — nothing here was touched)

Per the design brief, `hire.html`, `store.html`, `mission.html`, `crashers.html`, `adult/crew.html`, `cards.html`, `games.html` were not opened or edited. `nav.js` (site-wide nav bar, not in the owned-files list) links to them; its current English labels, for a future i18n pass:

| nav.js label | Target |
|---|---|
| Home | `index.html` / `adult/` |
| Story | `story.html` |
| Crashers | `crashers.html` |
| Party Store | `store.html` |
| Hire the Crew | `hire.html` |
| Our Mission | `mission.html` |
| In Real Life | `adult/` |
| The Crew | `crew.html` / `adult/crew.html` |

`nav.js` was not touched; these labels remain English on every page that loads it, independent of `gywbt-lang`.

---

## 5. Verification

### 5.1 `node --check` — all touched JS, 0 errors
```
story-config.js       OK
adult-config.js       OK
tap-engine.js          OK
adult/tap-engine.js    OK
music.js               OK
index.html (inline <script> extracted and checked separately)   OK
```

### 5.2 Functional trace — real source files executed in a stubbed browser context (Node `vm`, not a re-implementation)
A no-browser-extension environment meant I couldn't drive Chrome directly, so I loaded the **actual** `story-config.js`/`adult-config.js` source into a `vm.Context` stubbed with `location`/`localStorage`/`screen`, and called the real exported functions. All traces below passed:

- **(a) Envelope default EN → toggle ES → letter re-renders, kids/adult launch mount Spanish**: isolated the exact `index.html` letter-toggle code block (byte-diffed against the live file first) against a minimal DOM stub. Default render is EN; one click flips `lang`, re-renders `grownLink`/`kidsLink`/`langBtn` text+aria live, writes `localStorage`; two clicks round-trips back to EN. Confirmed `GYWBT_KIDS_CONFIG(lang)`/`GYWBT_ADULT_CONFIG(lang)` calls at both in-page launch sites reference the same `let lang` the toggle mutates (no shadowing — grepped the whole file for `\blang\b`).
- **(b) Direct `/adult/?lang=es` → Spanish; direct `/adult/` with stored `es` → Spanish; fresh visitor → English everywhere**: ran `GYWBT_ADULT_CONFIG()` (no-arg, exactly how `adult/index.html` calls it) against `search='?lang=es', stored=null` → Spanish + confirmed the URL param wrote `localStorage`; against `search='', stored='es'` → Spanish; against `search='', stored=null` → English. Same pattern verified for `story.html`'s no-arg `GYWBT_KIDS_CONFIG()` call.
- **(c) `story.html` both langs**: confirmed above (fresh → EN; `?lang=en` overriding a stored `es` → EN, proving URL always wins and re-writes storage).
- **(d) Toggle persists across a reload**: simulated by running the toggle logic once (writing to a stub store), then constructing a fresh instance reading that same store — picks up `es` and renders the kids label in Spanish immediately on the "reload."
- **(e) No engine/asset/rate/version regression**: `git diff` on both config files, filtered to lines containing `.webp`/`.mp4`/`rate:`/`scroll:`/`linger:`/`href:`/`spans`, shows **zero** changed asset paths, playback rates, or hrefs — only `label:`/`title:`/`body:`/`eyebrow:`/`tags:` values became `T.xxx` references. Additionally, the functional trace directly asserts `JSON.stringify()` equality of asset-path arrays and rate arrays between the EN and ES config output (see trace B in the script) — not just a diff-based inference. `tap-engine.js`/`adult/tap-engine.js` diffs are exactly one line each (the new `config.nextLabel ||` fallback).
- **Garbage input**: `?lang=fr` (unsupported) falls back cleanly to English default rather than erroring.

Verification scripts (kept for reference, not part of the deliverable):
`C:\Users\yashk\AppData\Local\Temp\claude\C--Users-yashk\5d42695e-b0aa-4367-9d31-85bd8592c1d1\scratchpad\verify-i18n.js`
`C:\Users\yashk\AppData\Local\Temp\claude\C--Users-yashk\5d42695e-b0aa-4367-9d31-85bd8592c1d1\scratchpad\verify-letter-toggle.js`

I was not able to do a pixel-level visual QA pass (no Chrome extension connection in this environment) to confirm the new `.sheet-lang` toggle doesn't visually overflow the letter's blank zone on every viewport — flagging as a follow-up visual check before shipping, though the toggle was deliberately sized small (11px font, 6px/10px padding) specifically to minimize that risk within the existing `.sheet-actions` scale logic.

---

## 6. Version bump accounting

| File | Old → New | Referenced from |
|---|---|---|
| `story-config.js` | `?v=1` → `?v=2` | `index.html`, `story.html` |
| `adult-config.js` | `?v=1` → `?v=2` | `index.html`, `adult/index.html` |
| `tap-engine.js` (kids/root) | `?v=8` → `?v=9` | `index.html`, `story.html` |
| `adult/tap-engine.js` | `?v=10` → `?v=11` | `index.html` (dynamic `<script>` injection), `adult/index.html` |
| `music.js` | `?v=15` → `?v=16` | `index.html`, `story.html`, `adult/index.html` |

`index.html`/`story.html`/`adult/index.html` themselves carry no version query param (they're entry HTML, not `<script src>`'d elsewhere) — no bump applicable. Confirmed via grep that all references to each bumped file were updated consistently (no stale `?v=` left pointing at an old, pre-i18n cached copy) within the 3 files I own; `music.js`'s five out-of-scope consumers (`crashers.html`, `cards.html`, `games.html`, `adult/crew.html`, `store.html`) were deliberately left at `?v=15` per "do not touch" — see the shared-file note in §3.

---

## 7. Files touched

- `C:\Users\yashk\gywbt-site\Website\index.html`
- `C:\Users\yashk\gywbt-site\Website\story.html`
- `C:\Users\yashk\gywbt-site\Website\story-config.js`
- `C:\Users\yashk\gywbt-site\Website\adult-config.js`
- `C:\Users\yashk\gywbt-site\Website\adult\index.html`
- `C:\Users\yashk\gywbt-site\Website\tap-engine.js`
- `C:\Users\yashk\gywbt-site\Website\adult\tap-engine.js`
- `C:\Users\yashk\gywbt-site\Website\music.js`
