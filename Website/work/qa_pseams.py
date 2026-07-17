import http.server, threading, functools, io
from playwright.sync_api import sync_playwright

SITE = r"C:\Users\yashk\OneDrive\Desktop\Glad You Were Born Today (Repo)\Website"
PORT = 8151
URL = f"http://127.0.0.1:{PORT}/index.html"

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SITE)
httpd = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()

widths = [1.5, 0.9, 1.3, 0.9, 1.3, 0.9, 1.6, 0.9, 1.8]
labels = ["beige", "conn1", "crashpad", "conn2", "crash", "conn3", "glowup", "conn4", "finale"]

def img_diff(a_bytes, b_bytes):
    from PIL import Image, ImageChops
    a = Image.open(io.BytesIO(a_bytes)).convert("L").resize((195, 422))
    b = Image.open(io.BytesIO(b_bytes)).convert("L").resize((195, 422))
    d = ImageChops.difference(a, b)
    h = d.histogram()
    return sum(i * c for i, c in enumerate(h)) / sum(h)

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True,
                              screen={"width": 390, "height": 844})
    page = ctx.new_page()
    reqs = []
    page.on("request", lambda r: reqs.append(r.url))
    page.goto(URL)
    page.wait_for_timeout(3500)
    page.evaluate("""() => {
      for (const sel of ['.sw-copylayer', '.sw-topbar', '.sw-nav', '.sw-route', '.sw-hint',
                         '.sw-particles', '.sw-scrollbar']) {
        document.querySelectorAll(sel).forEach(el => el.style.visibility = 'hidden');
      }
    }""")
    vh = 844
    doc_h = page.evaluate("document.body.scrollHeight")
    unit = (doc_h - vh) / sum(widths)

    def shot_at(px):
        page.evaluate(f"window.scrollTo(0, {int(px)})")
        page.wait_for_timeout(1800)
        return page.screenshot()

    d = 0.025 * unit
    cum = 0.0
    passed = 0
    for i, w in enumerate(widths[:-1]):
        cum += w
        seam = cum * unit
        s_m3 = shot_at(seam - 3 * d)
        s_m1 = shot_at(seam - d)
        s_p1 = shot_at(seam + d)
        s_p3 = shot_at(seam + 3 * d)
        base_a = img_diff(s_m3, s_m1)
        base_b = img_diff(s_p1, s_p3)
        cross  = img_diff(s_m1, s_p1)
        base = max(base_a, base_b, 1.0)
        ratio = cross / base
        ok = ratio < 2.5 or cross < 6
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  seam {labels[i]}>{labels[i+1]}  cross={cross:.1f} baseA={base_a:.1f} baseB={base_b:.1f} ratio={ratio:.2f}", flush=True)
        if not ok:
            open(f"ppop_{labels[i]}_a.png", "wb").write(s_m1)
            open(f"ppop_{labels[i]}_b.png", "wb").write(s_p1)
    m = [u for u in reqs if "-m.mp4" in u]
    full = [u for u in reqs if ".mp4" in u and "-m.mp4" not in u]
    print(f"clip tier: mobile={len(m)} master={len(full)}", flush=True)
    print(f"=== {passed}/8 portrait seams continuous ===", flush=True)
    browser.close()
httpd.shutdown()
