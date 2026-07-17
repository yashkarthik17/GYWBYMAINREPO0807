import http.server, threading, functools, io
from playwright.sync_api import sync_playwright

SITE = r"C:\Users\yashk\OneDrive\Desktop\Glad You Were Born Today (Repo)\Website"
PORT = 8141
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
    page.wait_for_timeout(2500)
    # hide everything that is NOT the video stage (copy panels, nav, route rail, hint, particles)
    page.evaluate("""() => {
      for (const sel of ['.sw-copylayer', '.sw-topbar', '.sw-nav', '.sw-route', '.sw-hint',
                         '.sw-particles', '.sw-scrollbar']) {
        document.querySelectorAll(sel).forEach(el => el.style.visibility = 'hidden');
      }
    }""")
    vh = 900
    doc_h = page.evaluate("document.body.scrollHeight")
    unit = (doc_h - vh) / sum(widths)
    cum = 0.0
    passed = 0
    for i, w in enumerate(widths[:-1]):
        cum += w
        seam_px = cum * unit
        eps = 0.14 * unit
        page.evaluate(f"window.scrollTo(0, {int(seam_px - eps)})")
        page.wait_for_timeout(1600)
        a = page.screenshot()
        page.evaluate(f"window.scrollTo(0, {int(seam_px + eps)})")
        page.wait_for_timeout(1600)
        b = page.screenshot()
        diff = img_diff(a, b)
        ok = diff < 14
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  seam {labels[i]}>{labels[i+1]}  meandiff={diff:.1f}", flush=True)
        if not ok:
            open(f"seamshot_{labels[i]}_a.png", "wb").write(a)
            open(f"seamshot_{labels[i]}_b.png", "wb").write(b)
    print(f"=== {passed}/8 seams pass (video layer only) ===", flush=True)
    browser.close()
httpd.shutdown()
