#!/usr/bin/env python3
"""Export the HTML deck as a screenshot-based `.pptx`.

Workflow:
1. rebuild `defense_html/Defense.html`
2. serve the deck locally
3. print it to a one-slide-per-page PDF with headless Chrome
4. rasterize each page to a PNG
5. generate a temporary Markdown deck with one image per slide plus notes
6. let `pandoc` create the `.pptx`
7. patch the resulting slide XML so every image is full-bleed

Expected notes format in `speaker_notes/speaker_notes_pptx.md`:
- `### Slide 01 · Title`
- `### Backup B1 · Short label`
- freeform Markdown/plaintext below each heading

Only the slide token is used for matching (`01`, `02`, ..., `B1`, `B2`, ...).
"""

from __future__ import annotations

import argparse
import http.server
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import zipfile
from contextlib import contextmanager
from functools import partial
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DEFENSE_HTML_DIR = ROOT / "defense_html"
OUTPUT_HTML = DEFENSE_HTML_DIR / "Defense.html"
DEFAULT_NOTES_PATH = ROOT / "speaker_notes" / "speaker_notes_pptx.md"
DEFAULT_OUTPUT_PATH = ROOT / "Defense_screenshots.pptx"

sys.path.insert(0, str(ROOT))
from dev import build, discover_slides, ensure_template  # type: ignore  # noqa: E402

CHROME_CANDIDATES = [
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
]

SLIDE_FILENAME_RE = re.compile(r"^(B?\d+)-[^/]+\.html$", re.IGNORECASE)
NOTE_HEADING_RE = re.compile(
    r"^###\s+(?:Slide\s+(\d+)|Backup\s+(B\d+))(?:\s*[·:-]\s*.*)?$",
    re.IGNORECASE,
)
PNG_NAME_RE = re.compile(r"^slide-(\d+)\.png$")

P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"

NS = {"p": P_NS, "a": A_NS}
ET.register_namespace("a", A_NS)
ET.register_namespace("p", P_NS)
ET.register_namespace("r", "http://schemas.openxmlformats.org/officeDocument/2006/relationships")


def normalize_slide_key(raw: str) -> str:
    value = raw.strip().upper()
    if value.startswith("B"):
        return f"B{int(value[1:])}"
    return f"{int(value):02d}"


def slide_sort_key(key: str) -> tuple[int, int]:
    if key.startswith("B"):
        return (1, int(key[1:]))
    return (0, int(key))


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


def discover_slide_keys() -> list[str]:
    keys = ["01"]
    for path in discover_slides():
        match = SLIDE_FILENAME_RE.match(path.name)
        if not match:
            continue
        keys.append(normalize_slide_key(match.group(1)))
    return keys


def parse_notes(path: Path) -> dict[str, str]:
    if not path.exists():
        print(f"[warn] Notes file not found, exporting without notes: {path}")
        return {}

    notes: dict[str, str] = {}
    current_key: str | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal current_key, buffer
        if current_key is None:
            buffer = []
            return

        body = "\n".join(buffer).strip()
        if current_key in notes:
            raise ValueError(f"Duplicate notes block for slide {current_key} in {path}")
        notes[current_key] = body
        current_key = None
        buffer = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = NOTE_HEADING_RE.match(raw_line.strip())
        if match:
            flush()
            current_key = normalize_slide_key(match.group(1) or match.group(2))
            continue
        if current_key is not None:
            buffer.append(raw_line.rstrip())

    flush()
    return notes


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


def render_pdf(chrome: str, url: str, pdf_path: Path, virtual_time_ms: int) -> None:
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
            f"--virtual-time-budget={virtual_time_ms}",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={pdf_path}",
            url,
        ]
    )


def render_pngs(pdftoppm: str, pdf_path: Path, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = output_dir / "slide"
    run_command(
        [
            pdftoppm,
            "-png",
            "-scale-to-x",
            "1920",
            "-scale-to-y",
            "1080",
            str(pdf_path),
            str(prefix),
        ]
    )

    pngs = sorted(
        output_dir.glob("slide-*.png"),
        key=lambda path: int(PNG_NAME_RE.match(path.name).group(1)) if PNG_NAME_RE.match(path.name) else 10**9,
    )
    if not pngs:
        raise RuntimeError("PDF rasterization produced no slide PNGs.")
    return pngs


def write_markdown_deck(
    markdown_path: Path,
    pngs: list[Path],
    slide_keys: list[str],
    notes_by_key: dict[str, str],
) -> None:
    sections: list[str] = []
    for slide_key, png_path in zip(slide_keys, pngs, strict=True):
        rel_path = png_path.relative_to(markdown_path.parent).as_posix()
        lines = [f"![]({rel_path}){{width=13.333333in height=7.5in}}"]

        notes = escape_note_text(notes_by_key.get(slide_key, "").strip())
        if notes:
            lines.extend(["", ":::::::: notes", notes, "::::::::"])

        sections.append("\n".join(lines))

    markdown_path.write_text("\n\n---\n\n".join(sections) + "\n", encoding="utf-8")


def escape_note_text(text: str) -> str:
    escaped: list[str] = []
    for line in text.splitlines():
        stripped = line.lstrip()
        indent = line[: len(line) - len(stripped)]

        if not stripped:
            escaped.append("")
            continue

        if stripped.startswith(("- ", "* ", "+ ", "#", ">")):
            escaped.append(f"{indent}\\{stripped}")
            continue

        number_match = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if number_match:
            escaped.append(f"{indent}{number_match.group(1)}\\. {number_match.group(2)}")
            continue

        escaped.append(line)

    return "\n".join(escaped)


def read_slide_size(pptx_path: Path) -> tuple[str, str]:
    with zipfile.ZipFile(pptx_path) as archive:
        presentation_xml = archive.read("ppt/presentation.xml")

    root = ET.fromstring(presentation_xml)
    size = root.find("p:sldSz", NS)
    if size is None:
        raise RuntimeError("Could not find slide size in generated PPTX.")
    return size.attrib["cx"], size.attrib["cy"]


def patch_slide_xml(xml_bytes: bytes, *, cx: str, cy: str) -> bytes:
    root = ET.fromstring(xml_bytes)
    for xfrm in root.findall(".//p:pic/p:spPr/a:xfrm", NS):
        off = xfrm.find("a:off", NS)
        ext = xfrm.find("a:ext", NS)
        if off is not None:
            off.set("x", "0")
            off.set("y", "0")
        if ext is not None:
            ext.set("cx", cx)
            ext.set("cy", cy)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def patch_pptx_full_bleed(pptx_path: Path) -> None:
    cx, cy = read_slide_size(pptx_path)
    patched_path = pptx_path.with_suffix(".patched.pptx")

    with zipfile.ZipFile(pptx_path, "r") as src, zipfile.ZipFile(
        patched_path, "w", compression=zipfile.ZIP_DEFLATED
    ) as dst:
        for item in src.infolist():
            if item.is_dir():
                dst.writestr(item, b"")
                continue

            data = src.read(item.filename)
            if item.filename.startswith("ppt/slides/slide") and item.filename.endswith(".xml"):
                data = patch_slide_xml(data, cx=cx, cy=cy)
            dst.writestr(item, data)

    patched_path.replace(pptx_path)


def make_temp_root(keep_temp: bool) -> tuple[Path, bool]:
    if keep_temp:
        path = Path(tempfile.mkdtemp(prefix="pptx-export-"))
        return path, False
    return Path(tempfile.mkdtemp(prefix="pptx-export-")), True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Where to write the generated PPTX.",
    )
    parser.add_argument(
        "--notes",
        type=Path,
        default=DEFAULT_NOTES_PATH,
        help="Markdown file that contains slide-mapped speaker notes.",
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
        "--keep-temp",
        action="store_true",
        help="Keep intermediate PDF, PNG, and Markdown files for debugging.",
    )
    args = parser.parse_args()

    chrome = resolve_binary(args.chrome, CHROME_CANDIDATES, "Chrome/Chromium")
    pandoc = resolve_binary(None, ["pandoc"], "pandoc")
    pdftoppm = resolve_binary(None, ["pdftoppm"], "pdftoppm")

    notes_path = args.notes.expanduser().resolve()
    output_path = args.output.expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("[1/5] Rebuilding Defense.html")
    ensure_template()
    build()

    slide_keys = discover_slide_keys()
    notes_by_key = parse_notes(notes_path)
    unknown_note_keys = sorted(set(notes_by_key) - set(slide_keys), key=slide_sort_key)
    if unknown_note_keys:
        print(f"[warn] Notes exist for unknown slide keys: {', '.join(unknown_note_keys)}")

    temp_root, cleanup = make_temp_root(args.keep_temp)
    try:
        pdf_path = temp_root / "deck.pdf"
        png_dir = temp_root / "png"
        markdown_path = temp_root / "deck.md"
        raw_pptx = temp_root / "deck_raw.pptx"

        print("[2/5] Printing deck to PDF")
        with serve_directory(DEFENSE_HTML_DIR) as url:
            render_pdf(chrome, url, pdf_path, args.virtual_time_ms)

        print("[3/5] Rendering slide PNGs")
        pngs = render_pngs(pdftoppm, pdf_path, png_dir)
        if len(pngs) != len(slide_keys):
            raise RuntimeError(
                f"Rendered {len(pngs)} slide images, but the deck source contains {len(slide_keys)} slides."
            )

        print("[4/5] Building PPTX via pandoc")
        write_markdown_deck(markdown_path, pngs, slide_keys, notes_by_key)
        run_command([pandoc, str(markdown_path), "-o", str(raw_pptx)], cwd=temp_root)
        patch_pptx_full_bleed(raw_pptx)

        shutil.copy2(raw_pptx, output_path)
        print(f"[5/5] Wrote {output_path}")
        if args.keep_temp:
            print(f"[info] Kept intermediates in {temp_root}")
    finally:
        if cleanup:
            shutil.rmtree(temp_root, ignore_errors=True)


if __name__ == "__main__":
    main()
