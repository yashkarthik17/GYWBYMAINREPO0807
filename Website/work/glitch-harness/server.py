"""Throttleable static server for the tap-engine glitch harness.

Serves the Website/ directory (two levels up) with URL-prefix behaviors:
  /slow/<ms>/<path>       -> serve <path> after a <ms> delay (whole response)
  /drip/<kbps>/<path>     -> serve <path> rate-limited to <kbps> KB/s
  /stall/<frac>/<path>    -> send first <frac> of bytes, then hang ~120s
  /<path>                 -> serve normally

Threaded so a stalled request never blocks the rest of the page.
Run: python server.py [port]   (default 8123)
"""
import sys, time, mimetypes, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]   # .../Website
LOCK = threading.Lock()


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def do_POST(self):
        # harness state reports: POST /report?s=<scenario>, JSON body per line
        q = urlsplit(self.path)
        if q.path == "/report":
            scen = (q.query.split("s=")[-1].split("&")[0]) or "unknown"
            n = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(n).decode("utf-8", "replace")
            out = Path(__file__).with_name(f"reports-{scen}.jsonl")
            with LOCK:
                with out.open("a", encoding="utf-8") as fh:
                    fh.write(body.rstrip("\n") + "\n")
            self.send_response(204)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        self.send_response(404)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_HEAD(self):
        # music.js existence-probes its track with HEAD before building
        path = unquote(urlsplit(self.path).path)
        f = (ROOT / path.lstrip("/")).resolve()
        ok = str(f).startswith(str(ROOT)) and f.is_file()
        self.send_response(200 if ok else 404)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        path = unquote(urlsplit(self.path).path)
        delay_ms, drip_kbps, stall_frac = 0, 0, None
        parts = path.lstrip("/").split("/")
        if len(parts) >= 3 and parts[0] in ("slow", "drip", "stall"):
            mode, arg = parts[0], parts[1]
            path = "/" + "/".join(parts[2:])
            if mode == "slow":
                delay_ms = int(arg)
            elif mode == "drip":
                drip_kbps = int(arg)
            else:
                stall_frac = float(arg)

        f = (ROOT / path.lstrip("/")).resolve()
        if not str(f).startswith(str(ROOT)) or not f.is_file():
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        data = f.read_bytes()
        ctype = mimetypes.guess_type(str(f))[0] or "application/octet-stream"
        if delay_ms:
            time.sleep(delay_ms / 1000)

        # Range support (video elements ask for ranges; 200-with-full-body also
        # works for mp4 but honoring ranges keeps behavior browser-realistic).
        start, end = 0, len(data) - 1
        rng = self.headers.get("Range")
        status = 200
        if rng and rng.startswith("bytes="):
            spec = rng[6:].split(",")[0]
            a, _, b = spec.partition("-")
            if a:
                start = int(a)
                end = int(b) if b else end
            elif b:
                start = max(0, len(data) - int(b))
            status = 206

        body = data[start:end + 1]
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Accept-Ranges", "bytes")
        if status == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{len(data)}")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

        try:
            if stall_frac is not None:
                cut = int(len(body) * stall_frac)
                self.wfile.write(body[:cut])
                self.wfile.flush()
                time.sleep(120)          # hang: never send the rest
                return
            if drip_kbps:
                chunk = 1024
                per_chunk = 1.0 / drip_kbps    # seconds per KB
                for i in range(0, len(body), chunk):
                    self.wfile.write(body[i:i + chunk])
                    self.wfile.flush()
                    time.sleep(per_chunk)
                return
            self.wfile.write(body)
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8123
    print(f"serving {ROOT} on http://localhost:{port}")
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
