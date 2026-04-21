#!/usr/bin/env python3
"""Dev server for the defense deck.

    python3 dev.py               # serve on http://localhost:8000/
    python3 dev.py --port 5500

What it does
------------
* Rebuilds ``Defense.html`` from ``_template.html`` + ``slides/*.html``
  whenever a slide (or the template) changes on disk.
* Serves the folder via HTTP.
* When you request ``Defense.html``, a tiny live-reload snippet is injected
  into the response (the file on disk stays untouched), so the browser
  auto-reloads as soon as a rebuild completes.

Source of truth: one HTML file per slide under ``slides/``, named
``NN-slug.html`` (e.g. ``02-outline.html``) for numbered main slides and
``Bn-slug.html`` (e.g. ``B1-agentedge-s35-defense.html``) for Q&A backups.
Files are concatenated in natural sort order (``02 … 56 B1 … B8``) into the
single ``<!--SLIDES-->`` placeholder in ``_template.html``.

The ``_archive/`` subfolder inside ``slides/`` is ignored.
"""

from __future__ import annotations

import argparse
import http.server
import os
import queue
import re
import socketserver
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).parent.resolve()
SLIDES_DIR = HERE / "slides"
ARCHIVE_DIR = SLIDES_DIR / "_archive"
OUTPUT = HERE / "Defense.html"
TEMPLATE = HERE / "_template.html"

SLIDES_PLACEHOLDER = "<!--SLIDES-->"

# NN-slug.html (numeric, 1-2 digits) or Bn-slug.html (B1..B9, backups).
_SLIDE_FILENAME_RE = re.compile(r"^(B?\d+)-[^/]+\.html$")


def slide_sort_key(path: Path) -> tuple[int, int]:
    """Sort numeric slides first (ascending), then backups (B1..B8 ascending)."""
    m = _SLIDE_FILENAME_RE.match(path.name)
    if not m:
        return (2, 0)
    prefix = m.group(1)
    if prefix.upper().startswith("B"):
        return (1, int(prefix[1:]))
    return (0, int(prefix))


def discover_slides() -> list[Path]:
    """All per-slide files in ``slides/``, natural-sorted, excluding archive."""
    if not SLIDES_DIR.exists():
        return []
    files = [
        p for p in SLIDES_DIR.glob("*.html")
        if ARCHIVE_DIR not in p.parents and _SLIDE_FILENAME_RE.match(p.name)
    ]
    return sorted(files, key=slide_sort_key)

LIVE_RELOAD_SNIPPET = """
<!-- injected by dev.py -->
<script>
(function () {
  var retry = 0;
  function connect() {
    var es = new EventSource('/__livereload');
    es.onopen = function () { retry = 0; };
    es.onmessage = function (ev) { if (ev.data === 'reload') location.reload(); };
    es.onerror = function () {
      es.close();
      setTimeout(connect, Math.min(15000, 500 * Math.pow(2, retry++)));
    };
  }
  connect();
})();
</script>
"""


# ----------------------------- template handling -----------------------------

def ensure_template() -> None:
    """Create ``_template.html`` from the current ``Defense.html`` if missing."""
    if TEMPLATE.exists():
        return
    if not OUTPUT.exists():
        sys.exit(f"error: {TEMPLATE} missing and no Defense.html to seed from.")

    src = OUTPUT.read_text(encoding="utf-8")

    # The first </section> closes the title slide.
    head_end = src.find("</section>")
    if head_end == -1:
        sys.exit("error: could not find opening </section> in Defense.html")
    head_end += len("</section>")

    # The last </section> before </deck-stage> closes the final backup slide.
    deck_end = src.rfind("</deck-stage>")
    if deck_end == -1:
        sys.exit("error: could not find </deck-stage> in Defense.html")
    foot_start = src.rfind("</section>", 0, deck_end) + len("</section>")

    TEMPLATE.write_text(
        src[:head_end] + "\n\n" + SLIDES_PLACEHOLDER + "\n\n" + src[foot_start:],
        encoding="utf-8",
    )
    print(f"[init] wrote {TEMPLATE.name} from current Defense.html")


# ---------------------------------- build ----------------------------------

def build() -> int:
    template = TEMPLATE.read_text(encoding="utf-8")
    if SLIDES_PLACEHOLDER not in template:
        raise RuntimeError(
            f"template is missing {SLIDES_PLACEHOLDER} placeholder; regenerate it"
        )

    files = discover_slides()
    if not files:
        print("[warn] no slide files found in slides/")

    bodies = [path.read_text(encoding="utf-8").rstrip() + "\n" for path in files]
    injected = "\n".join(bodies)
    html = template.replace(SLIDES_PLACEHOLDER, injected)
    OUTPUT.write_text(html, encoding="utf-8")
    return len(html)


# ----------------------------- live-reload SSE -----------------------------

_clients: list[queue.Queue[str]] = []
_clients_lock = threading.Lock()


def broadcast(msg: str) -> None:
    with _clients_lock:
        for q in list(_clients):
            try:
                q.put_nowait(msg)
            except queue.Full:
                pass


class Handler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):  # noqa: N802
        if self.path.split("?")[0] == "/__livereload":
            return self._serve_sse()

        # Inject live-reload into Defense.html responses.
        norm = self.path.split("?")[0].lstrip("/")
        if norm in ("", "Defense.html") and OUTPUT.exists():
            return self._serve_defense_html()

        return super().do_GET()

    def _serve_defense_html(self) -> None:
        body = OUTPUT.read_text(encoding="utf-8")
        if "</body>" in body:
            body = body.replace("</body>", LIVE_RELOAD_SNIPPET + "\n</body>", 1)
        else:
            body += LIVE_RELOAD_SNIPPET
        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _serve_sse(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "keep-alive")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()
        q: queue.Queue[str] = queue.Queue(maxsize=16)
        with _clients_lock:
            _clients.append(q)
        try:
            self.wfile.write(b": connected\n\n")
            self.wfile.flush()
            while True:
                try:
                    msg = q.get(timeout=15)
                except queue.Empty:
                    self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
                    continue
                self.wfile.write(f"data: {msg}\n\n".encode("utf-8"))
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            with _clients_lock:
                if q in _clients:
                    _clients.remove(q)

    def log_message(self, fmt: str, *args) -> None:  # noqa: A003
        if self.path.startswith("/__livereload"):
            return
        sys.stderr.write("[http] %s - %s\n" % (self.address_string(), fmt % args))


class ThreadedServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


# ---------------------------------- watch ----------------------------------

def watch_loop(debounce_s: float = 0.25) -> None:
    def snapshot() -> dict[Path, float]:
        paths: list[Path] = [TEMPLATE]
        paths += discover_slides()
        return {p: p.stat().st_mtime for p in paths if p.exists()}

    last = snapshot()
    while True:
        time.sleep(debounce_s)
        cur = snapshot()
        changed = [p for p, m in cur.items() if last.get(p) != m]
        gone = [p for p in last if p not in cur]
        if changed or gone:
            names = ", ".join(p.name for p in changed + gone) or "?"
            print(f"[watch] changed: {names}")
            try:
                size = build()
                print(f"[build] Defense.html ({size:,} chars)")
                broadcast("reload")
            except Exception as e:  # noqa: BLE001
                print(f"[error] build failed: {e}")
            last = cur


# ---------------------------------- main ----------------------------------

def main() -> None:
    try:
        sys.stdout.reconfigure(line_buffering=True)  # type: ignore[attr-defined]
    except Exception:  # noqa: BLE001
        pass

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--no-open", action="store_true", help="skip initial build")
    args = ap.parse_args()

    os.chdir(HERE)
    ensure_template()

    if not args.no_open:
        size = build()
        print(f"[build] Defense.html ({size:,} chars)")

    threading.Thread(target=watch_loop, daemon=True).start()

    server = ThreadedServer((args.host, args.port), Handler)
    print(f"[dev] http://{args.host}:{args.port}/Defense.html")
    print("[dev] editing slides/*.html triggers rebuild + browser reload. Ctrl-C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[dev] bye")


if __name__ == "__main__":
    main()
