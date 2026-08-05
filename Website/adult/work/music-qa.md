# Adult page music QA — Task 2

## Method

Live Chrome QA per the task brief's Step 6 was attempted first, as instructed:

- Started a local server: `cd Website && python -m http.server 8000` (confirmed serving —
  `GET /adult/index.html` returned HTTP 200).
- Attempted browser automation via the `claude-in-chrome` MCP tools
  (`tabs_context_mcp`, `navigate`, `computer`, `read_page`, etc.).
- Result: `tabs_context_mcp` returned "Browser extension is not connected. Please
  ensure the Claude browser extension is installed and running
  (https://claude.ai/chrome)..." — the extension is not available in this
  environment, so no interactive tab could be opened.

Per the task's fallback instructions, **no row below was verified in a live
browser**. Every row is instead justified by a static code walkthrough of
`Website/music.js` (post-Task-2 edit) and `Website/adult/index.html` line 43,
citing the exact lines that implement the expected behavior. All rows are
marked **PENDING live QA (Task 10 preview)** and must be re-verified by hand
in a real Chrome profile before ship.

Also note: even when browser automation *is* available, the brief's own
caveat applies — automated Chrome tabs (via the MCP extension) may apply
different (often looser or differently-timed) autoplay heuristics than a
real user profile, since the autoplay heuristic is partly based on the
site-engagement score / per-profile history that an automation-driven,
just-launched profile won't have. Rows 1–3 in particular (autoplay-blocked
vs. autoplay-allowed) should be re-checked in the actual shipping browser
profile(s), not just automation, even at Task 10.

## Config under test

`Website/adult/index.html:43`
```html
<script src="../music.js?v=14" data-autostart data-once data-start="11"></script>
```
→ `AUTO=true`, `ONCE=true`, `START=11`, `SRC` defaults to
`assets/audio/theme.wav?v=3` (no `data-src` override on the adult page).

## Matrix

| # | Steps (Chrome, fresh profile/incognito) | Expected | Result | Justification (music.js line refs, post-edit) |
|---|---|---|---|---|
| 1 | Open `/adult/` directly, touch nothing, wait | Music blocked; ♪ shows OFF (never lies "on") | PENDING live QA (Task 10 preview) | On load, `wanted = stored==='1' \|\| (AUTO && stored!=='0')` (line 122) is true on a fresh visit (no sessionStorage entry). `set(true)` is called immediately (line 129) — a real `audio.play()` attempt, not a fake one. On a fresh incognito profile with no prior gesture/engagement, the browser's autoplay policy rejects the promise, so `.catch` in `set()` (line 88) fires `setUi(false)` and does **not** write `sessionStorage`. `setUi` (lines 76-80) only ever toggles `is-on`/`aria-pressed` from these two truth points (the `.then`/`.catch` of `set`, and `ended`), never optimistically, so the button never shows "on" while actually blocked. |
| 2 | From row 1, click anywhere on the page | Music starts at 0:11; ♪ ON | PENDING live QA (Task 10 preview) | The `pointerdown`/`touchend` listeners registered at lines 136-137 fire on any page click. The handler `once` (lines 130-135) first unregisters both listeners (lines 131-132), then checks `e.target.closest('#sw-music')` (line 133) — for a click anywhere else this is null, so it falls through to `if (audio.paused) set(true)` (line 134). `set(true)` calls `seekIntoTrack()` (line 84, uses `START=11` to seek past the intro per lines 38-42) then `audio.play()`; inside a real click handler this is a user gesture so the play promise resolves, `setUi(true)` runs (line 86) and `sessionStorage` is set to `'1'` (line 87). |
| 3 | From row 1 (blocked, ♪ off), tap ♪ FIRST | ♪ is a normal toggle, not hijacked by the generic first-gesture fallback: tapping ♪ while off starts music, ♪ turns ON. Tapping ♪ again pauses, ♪ OFF, sessionStorage `sw-music-on=0`; later page clicks do not restart it. (Symmetrically, if music is already playing when the first tap lands on ♪, that tap mutes and it sticks.) | Consistent with code (static trace). PENDING live QA (Task 10 preview) | Two independent listeners fire on the first tap, in order: (a) the window `pointerdown` capture (`once`, lines 130-135) fires first — it unconditionally removes both fallback listeners (lines 131-132), then sees `e.target.closest('#sw-music')` is truthy (line 133) and returns *without* calling `set(true)` itself, correctly declining to hijack the button's own control; (b) the button's own `click` listener (line 96: `set(audio.paused)`) then fires as the ordinary toggle — since `audio.paused` is `true` (blocked at row 1), this evaluates to `set(true)`, and a synchronous `audio.play()` call from inside a real button `click` handler (line 85) is a reliable user-activation gesture, so it resolves: `setUi(true)` and `sessionStorage.setItem(KEY,'1')` (lines 86-87) fire — ♪ turns ON. Tapping ♪ again while playing calls `set(audio.paused)` → `set(false)` (line 96), which pauses (line 90), calls `setUi(false)` (line 91), and writes `sessionStorage.setItem(KEY,'0')` (line 92); because both fallback listeners were already removed on the very first `pointerdown` (lines 131-132, unconditionally, regardless of where it landed), later clicks elsewhere on the page do not re-arm the fallback or restart playback. Symmetrically, if music is already playing when the first tap lands on ♪ (`audio.paused` false), `set(audio.paused)` → `set(false)` mutes on that very tap and, being a direct user click on the mute control, that choice sticks (`sessionStorage` `'0'`, no auto-restart). |
| 4 | Let the song play to the end | Playback stops (no loop), ♪ flips OFF | PENDING live QA (Task 10 preview) | `audio.loop = (START === 0) && !ONCE` (line 43) evaluates to `(11===0) && !true` = `false`, so the native loop never re-triggers. The `ended` listener (lines 49-52) checks `if (ONCE)` first (line 50) — true on the adult page — and calls `setUi(false)` plus resets `audio.currentTime = START` (i.e. 11), then `return`s before reaching the old hand-loop branch (line 51). No `.play()` is called, so playback genuinely stops and the button visibly flips off via the single `setUi` truth point. |
| 5 | After row 4, click ♪ | Song replays from 0:11 | PENDING live QA (Task 10 preview) | After row 4, `audio.currentTime` was reset to `START` (11) by the `ended` handler (line 50) and `audio.paused` is true (playback stopped, nothing calls `.play()` again). Clicking ♪ fires `set(audio.paused)` → `set(true)` (line 96), which calls `seekIntoTrack()` (line 84) — a no-op since currentTime is already at 11 — then `audio.play()`, resuming from 0:11. `setUi(true)` fires on success (line 86). |
| 6 | Open `/` (envelope), tap open, choose grown-ups | Music carries into `/adult/` and starts without a new tap | PENDING live QA (Task 10 preview) | This is a cross-page behavior outside `music.js` itself (envelope page's own JS starts/continues playback via `swMusic.on`/`swap`, then navigates to `/adult/`; `sessionStorage` key `sw-music-on` persists across same-origin navigation within the tab). On the adult page, if `stored==='1'` (line 122) from the envelope page's playback, `wanted` is true and `set(true)` fires at load (line 129) as a real, gesture-warmed play attempt — since the visitor already interacted on the envelope page in this tab, most browsers' autoplay heuristics grant this a pass; no re-tap needed. This mechanism is unchanged by Task 2 versus pre-existing `music.js` behavior — Task 2 only added `ONCE`/`setUi` and did not touch the `stored==='1'` autoplay path. Should still be spot-checked live because it depends on real per-browser autoplay heuristics, not just code logic. |
| 7 | Envelope page: let strings play 2+ minutes | Strings still loop (envelope unaffected) | PENDING live QA (Task 10 preview) | `Website/index.html:176` script tag has no `data-once` attribute, so on the envelope page `ONCE = !!(tag && tag.hasAttribute('data-once'))` (music.js line 16) is `false`. Its script tag also has no `data-start`, so initial `START` is `0` (line 21), making `audio.loop = (START===0) && !ONCE` → `(true) && (true)` → `true` (line 43): native looping, unaffected by Task 2. If the page later calls `swMusic.swap(...)` (as `Website/index.html:365` does, `swap("assets/audio/theme.wav?v=2", 11)`, for the in-page kids-story track), `swap()` sets `START=11` and recomputes `audio.loop = (START===0) && !ONCE` → `(false) && (true)` → `false` (music.js line 109) — same as pre-Task-2 behavior (`audio.loop = (START===0)` alone was already `false` for `START=11`). With `loop` false and `ONCE` false, the `ended` handler's `if (ONCE)` branch (line 50) is skipped, falling through to `if (START > 0) { seekIntoTrack(); audio.play()... }` (line 51) — the pre-existing hand-loop path, unchanged. So both the classical strings (native loop) and the swapped kids-story track (hand-loop) behave identically to before Task 2. |

## Summary of what Task 2 statically changed vs. what it did not

- Changed: `ONCE` flag (music.js:16), `audio.loop` now also gates on `!ONCE`
  (music.js:43, and inside `swap()` at music.js:109), `ended` handler gains a
  `ONCE` branch that stops playback and resets position instead of relooping
  (music.js:49-52), UI updates centralized into `setUi()` so the button only
  ever reflects real `play()`/`pause()` outcomes or `ended` (music.js:76-94),
  and the first-gesture fallback listeners are now removable (not
  `{once:true}`) and explicitly ignore clicks on `#sw-music` itself
  (music.js:130-137).
- Verified unchanged for the envelope page: with no `data-once` attribute on
  `Website/index.html:176`'s script tag, `ONCE` is always `false` there, so
  `audio.loop` and the `ended` handler behave exactly as before Task 2 for
  both the native-loop classical strings and the hand-looped, `swap()`-ed
  kids-story track.
- Verified via grep: `Website/adult/index.html:43` is the only HTML file
  under `Website/` with `data-once` — see command below.

```
$ grep -rn "data-once" Website/ --include=*.html
Website/adult/index.html:43:<script src="../music.js?v=14" data-autostart data-once data-start="11"></script>
```

## Environment note

Interactive Chrome automation (`claude-in-chrome` MCP tools) was unavailable
in this environment (extension not connected — see error text under
"Method" above). `node --check Website/music.js` passed (exit 0), confirming
syntax validity, but that is not a substitute for the live QA matrix above.
This file's rows must be re-run by hand (or via working browser automation)
before the adult-journey-overhaul work ships, per Task 10's preview QA pass.
