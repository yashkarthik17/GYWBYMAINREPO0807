import http.server, threading, functools, io
from playwright.sync_api import sync_playwright

SITE = r"C:\Users\yashk\OneDrive\Desktop\Glad You Were Born Today (Repo)\Website"
PORT = 8143
URL = f"http://127.0.0.1:{PORT}/index.html"

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SITE)
httpd = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()

widths = [1.5, 0.9, 1.3, 0.9, 1.3, 0.9, 1.6, 0.9, 1.8]
labels = ["beige", "conn1", "crashpad", "conn2", "crash", "conn3", "glowup", "conn4", "finale"]

def img_diff(a_bytes, b_bytes):
    from PIL import Image, ImageChops
    a = Image.open(io.BytesIO(a_bytes)).convert("L").resize((480, 270))
    b = Image.open(io.BytesIO(b_bytes)).convert("L").resize((480, 270))
    d = ImageChops.difference(a, b)
    h = d.histogram()
    return sum(i * c for i, c in enumerate(h)) / sum(h)

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(URL)
    page.wait_for_timeout(3000)
    page.evaluate("""() => {
      for (const sel of ['.sw-copylayer', '.sw-topbar', '.sw-nav', '.sw-route', '.sw-hint',
                         '.sw-particles', '.sw-scrollbar']) {
        document.querySelectorAll(sel).forEach(el => el.style.visibility = 'hidden');
      }
    }""")
    vh = 900
    doc_h = page.evaluate("document.body.scrollHeight")
    unit = (doc_h - vh) / sum(widths)

    def shot_at(px):
        page.evaluate(f"window.scrollTo(0, {int(px)})")
        page.wait_for_timeout(1500)
        return page.screenshot()

    d = 0.025 * unit  # tiny step: ~0.1s of video time
    cum = 0.0
    passed = 0
    for i, w in enumerate(widths[:-1]):
        cum += w
        seam = cum * unit
        s_m3 = shot_at(seam - 3 * d)
        s_m1 = shot_at(seam - d)
        s_p1 = shot_at(seam + d)
        s_p3 = shot_at(seam + 3 * d)
        base_a = img_diff(s_m3, s_m1)          # normal motion inside clip A (2d apart)
        base_b = img_diff(s_p1, s_p3)          # normal motion inside clip B (2d apart)
        cross  = img_diff(s_m1, s_p1)          # across the seam (2d apart)
        base = max(base_a, base_b, 1.0)
        ratio = cross / base
        ok = ratio < 2.5 or cross < 6
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  seam {labels[i]}>{labels[i+1]}  cross={cross:.1f} baseA={base_a:.1f} baseB={base_b:.1f} ratio={ratio:.2f}", flush=True)
        if not ok:
            open(f"popshot_{labels[i]}_a.png", "wb").write(s_m1)
            open(f"popshot_{labels[i]}_b.png", "wb").write(s_p1)
    print(f"=== {passed}/8 seams continuous (pop-ratio metric) ===", flush=True)
    browser.close()
httpd.shutdown()
