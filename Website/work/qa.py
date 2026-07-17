import http.server, threading, functools, os, io, statistics
from playwright.sync_api import sync_playwright

SITE = r"C:\Users\yashk\OneDrive\Desktop\Glad You Were Born Today (Repo)\Website"
PORT = 8137
URL = f"http://127.0.0.1:{PORT}/index.html"

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SITE)
httpd = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()

# scroll widths must mirror index.html config (desktop)
widths = [1.5, 0.9, 1.3, 0.9, 1.3, 0.9, 1.6, 0.9, 1.8]  # beige c1 crashpad c2 crash c3 glowup c4 finale
labels = ["beige", "conn1", "crashpad", "conn2", "crash", "conn3", "glowup", "conn4", "finale"]

def img_diff(a_bytes, b_bytes):
    from PIL import Image, ImageChops
    a = Image.open(io.BytesIO(a_bytes)).convert("L").resize((480, 270))
    b = Image.open(io.BytesIO(b_bytes)).convert("L").resize((480, 270))
    d = ImageChops.difference(a, b)
    h = d.histogram()
    total = sum(h)
    mean = sum(i * c for i, c in enumerate(h)) / total
    return mean  # 0..255

results = []
def report(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}", flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch()

    # ---------- Desktop pass ----------
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    reqs = []
    page.on("request", lambda r: reqs.append(r.url))
    page.goto(URL)
    page.wait_for_timeout(2500)

    shot0 = page.screenshot()
    report("desktop: first paint renders", len(shot0) > 20000)

    vh = 900
    total_units = sum(widths)
    doc_h = page.evaluate("document.body.scrollHeight")
    scrollable = doc_h - vh
    report("desktop: scroll run exists", scrollable > 5 * vh, f"docH={doc_h}")

    seek_ok = page.evaluate("""() => {
      const vids = [...document.querySelectorAll('video')];
      return vids.length > 0 && vids.some(v => v.seekable && v.seekable.length && v.seekable.end(0) > 0);
    }""")
    report("desktop: blob video seekable", bool(seek_ok))

    # currentTime tracks scroll inside first dive
    page.evaluate(f"window.scrollTo(0, {int(0.4 * 1.5 * vh)})")
    page.wait_for_timeout(1200)
    t1 = page.evaluate("Math.max(...[...document.querySelectorAll('video')].map(v=>v.currentTime||0))")
    page.evaluate(f"window.scrollTo(0, {int(0.8 * 1.5 * vh)})")
    page.wait_for_timeout(1200)
    t2 = page.evaluate("Math.max(...[...document.querySelectorAll('video')].map(v=>v.currentTime||0))")
    report("desktop: currentTime tracks scroll", t2 > t1 + 0.5, f"t1={t1:.2f} t2={t2:.2f}")

    # seam continuity screenshots
    unit = scrollable / total_units  # px of scroll per configured unit (approx)
    cum = 0.0
    band = 0.15  # crossfade config
    for i, w in enumerate(widths[:-1]):
        cum += w
        seam_px = cum * unit
        eps = (band / 2 + 0.06) * unit
        page.evaluate(f"window.scrollTo(0, {int(seam_px - eps)})")
        page.wait_for_timeout(1400)
        a = page.screenshot()
        page.evaluate(f"window.scrollTo(0, {int(seam_px + eps)})")
        page.wait_for_timeout(1400)
        b = page.screenshot()
        diff = img_diff(a, b)
        report(f"desktop: seam {labels[i]}>{labels[i+1]} continuity", diff < 14, f"meandiff={diff:.1f}")

    report("desktop: no console errors", not errors, "; ".join(errors[:3]))
    ctx.close()

    # ---------- Reduced motion ----------
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    page = ctx.new_page()
    rreqs = []
    page.on("request", lambda r: rreqs.append(r.url))
    page.goto(URL)
    page.wait_for_timeout(2000)
    page.evaluate("window.scrollTo(0, 2000)")
    page.wait_for_timeout(1000)
    mp4s = [u for u in rreqs if ".mp4" in u]
    report("reduced-motion: no clip fetches", len(mp4s) == 0, f"{len(mp4s)} mp4 reqs")
    report("reduced-motion: stills shown", page.evaluate("!!document.querySelector('img')"))
    ctx.close()

    # ---------- Data saver ----------
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'connection', {value: {saveData: true, effectiveType: '4g'}})")
    dreqs = []
    page.on("request", lambda r: dreqs.append(r.url))
    page.goto(URL)
    page.wait_for_timeout(2000)
    mp4s = [u for u in dreqs if ".mp4" in u]
    report("data-saver: no clip fetches", len(mp4s) == 0, f"{len(mp4s)} mp4 reqs")
    ctx.close()

    # ---------- Phone tier ----------
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True,
                              screen={"width": 390, "height": 844},
                              user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")
    page = ctx.new_page()
    preqs = []
    page.on("request", lambda r: preqs.append(r.url))
    page.goto(URL)
    page.wait_for_timeout(2500)
    page.evaluate("window.scrollTo(0, 1500)")
    page.wait_for_timeout(1500)
    m_m = [u for u in preqs if "-m.mp4" in u]
    m_full = [u for u in preqs if ".mp4" in u and "-m.mp4" not in u]
    report("phone: mobile encodes served", len(m_m) > 0 and len(m_full) == 0, f"mobile={len(m_m)} master={len(m_full)}")
    shot = page.screenshot()
    report("phone: page renders", len(shot) > 15000)
    ctx.close()

    # ---------- Tablet tier ----------
    ctx = browser.new_context(viewport={"width": 834, "height": 1194}, is_mobile=True, has_touch=True,
                              screen={"width": 834, "height": 1194})
    page = ctx.new_page()
    treqs = []
    page.on("request", lambda r: treqs.append(r.url))
    page.goto(URL)
    page.wait_for_timeout(2500)
    t_m = [u for u in treqs if "-m.mp4" in u]
    t_full = [u for u in treqs if ".mp4" in u and "-m.mp4" not in u]
    report("tablet: master clips served", len(t_full) > 0 and len(t_m) == 0, f"mobile={len(t_m)} master={len(t_full)}")
    ctx.close()

    browser.close()

httpd.shutdown()
fails = [r for r in results if not r[1]]
print(f"=== QA DONE: {len(results)-len(fails)}/{len(results)} passed ===", flush=True)
