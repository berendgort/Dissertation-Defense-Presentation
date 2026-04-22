#!/usr/bin/env python3
"""Export the HTML deck as a PDF.

Workflow:
1. rebuild `defense_html/Defense.html`
2. serve the deck locally
3. print it to a one-slide-per-page PDF with headless Chrome
"""

from __future__ import annotations

import argparse
import http.server
import shutil
import subprocess
import sys
import threading
import time
from contextlib import contextmanager
from functools import partial
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFENSE_HTML_DIR = ROOT / "defense_html"
OUTPUT_HTML = DEFENSE_HTML_DIR / "Defense.html"
DEFAULT_OUTPUT_PATH = ROOT / "Defense.pdf"
DEFAULT_VIEWPORT_WIDTH = 1920
DEFAULT_VIEWPORT_HEIGHT = 1080
DEFAULT_DEVICE_SCALE_FACTOR = 2.0

CHROME_CANDIDATES = [
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
]

sys.path.insert(0, str(ROOT))
from dev import build, ensure_template  # type: ignore  # noqa: E402


def resolve_binary(explicit: str | None, candidates: list[str], label: str) -> str:
    if explicit:
        resolved = shutil.which(explicit)
        if resolved:
            return resolved
        path = Path(explicit).expanduser()
        if path.exists():
            return str(path.resolve())
        raise FileNotFoundError(f"Could not find {label} binary: {explicit}")

    for candidate in candidates:
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    raise FileNotFoundError(
        f"Could not find {label}. Install it or pass an explicit path."
    )


def run_command(cmd: list[str], *, cwd: Path | None = None) -> None:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return

    detail = result.stderr.strip() or result.stdout.strip() or "no output"
    raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(cmd)}\n{detail}")


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        return

    def copyfile(self, source, outputfile) -> None:
        try:
            super().copyfile(source, outputfile)
        except (BrokenPipeError, ConnectionResetError):
            return


@contextmanager
def serve_directory(directory: Path):
    handler = partial(QuietHandler, directory=str(directory))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/Defense.html"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def wait_for_url(url: str, timeout_s: float = 5.0) -> None:
    deadline = time.time() + timeout_s
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            with urlopen(url, timeout=1) as response:
                if 200 <= response.status < 400:
                    return
        except URLError as exc:
            last_error = exc
        except Exception as exc:  # noqa: BLE001
            last_error = exc
        time.sleep(0.1)
    raise RuntimeError(f"Local deck server did not become ready: {last_error}")


def render_pdf(
    chrome: str,
    url: str,
    pdf_path: Path,
    virtual_time_ms: int,
    *,
    viewport_width: int,
    viewport_height: int,
    device_scale_factor: float,
) -> None:
    wait_for_url(url)
    run_command(
        [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--hide-scrollbars",
            "--no-sandbox",
            "--no-first-run",
            "--no-default-browser-check",
            "--run-all-compositor-stages-before-draw",
            f"--window-size={viewport_width},{viewport_height}",
            f"--force-device-scale-factor={device_scale_factor}",
            f"--virtual-time-budget={virtual_time_ms}",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={pdf_path}",
            url,
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Where to write the generated PDF.",
    )
    parser.add_argument(
        "--chrome",
        help="Optional path to a Chrome/Chromium binary.",
    )
    parser.add_argument(
        "--virtual-time-ms",
        type=int,
        default=20_000,
        help="How long headless Chrome waits for assets before printing.",
    )
    parser.add_argument(
        "--viewport-width",
        type=int,
        default=DEFAULT_VIEWPORT_WIDTH,
        help="Headless Chrome viewport width in CSS pixels before printing.",
    )
    parser.add_argument(
        "--viewport-height",
        type=int,
        default=DEFAULT_VIEWPORT_HEIGHT,
        help="Headless Chrome viewport height in CSS pixels before printing.",
    )
    parser.add_argument(
        "--device-scale-factor",
        type=float,
        default=DEFAULT_DEVICE_SCALE_FACTOR,
        help="Headless Chrome device scale factor for higher-density rendering before PDF export.",
    )
    args = parser.parse_args()

    chrome = resolve_binary(args.chrome, CHROME_CANDIDATES, "Chrome/Chromium")
    output_path = args.output.expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.viewport_width <= 0 or args.viewport_height <= 0:
        raise ValueError("Viewport dimensions must be positive integers.")
    if args.device_scale_factor <= 0:
        raise ValueError("Device scale factor must be greater than zero.")

    print(f"[1/3] Rebuilding {OUTPUT_HTML.name}")
    ensure_template()
    build()

    print("[2/3] Printing deck to PDF")
    with serve_directory(DEFENSE_HTML_DIR) as url:
        render_pdf(
            chrome,
            url,
            output_path,
            args.virtual_time_ms,
            viewport_width=args.viewport_width,
            viewport_height=args.viewport_height,
            device_scale_factor=args.device_scale_factor,
        )

    print(f"[3/3] Wrote {output_path}")


if __name__ == "__main__":
    main()
