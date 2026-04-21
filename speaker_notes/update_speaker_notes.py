from pathlib import Path
import json
import re


ROOT = Path("/home/berend-gort/Code/LaTeX/Dissertation-Defense-Presentation")
MD_PATH = ROOT / "speaker_notes" / "speaker_notes_full.md"
TEMPLATE_PATH = ROOT / "defense_html" / "_template.html"
SLIDES_DIR = ROOT / "defense_html" / "slides"

SECTION_RE = re.compile(r"^###\s+(.*?)\n\n(.*?)(?=^###\s+|\Z)", flags=re.M | re.S)
JSON_BLOCK_RE = re.compile(
    r'(<script type="application/json" id="speaker-notes">)(.*?)(</script>)',
    flags=re.S,
)


def parse_markdown_sections(text: str) -> list[str]:
    sections = []
    for title, body in SECTION_RE.findall(text.strip()):
        clean_body = body.strip()
        if not clean_body:
            raise RuntimeError(f"Empty speaker note section: {title}")
        sections.append(f"{title}\n\n{clean_body}")
    return sections


def expected_slide_count() -> int:
    slide_files = [path for path in SLIDES_DIR.glob("*.html") if path.is_file()]
    return 1 + len(slide_files)


def sync_embedded_notes(notes: list[str]) -> None:
    html = TEMPLATE_PATH.read_text()
    match = JSON_BLOCK_RE.search(html)
    if not match:
        raise RuntimeError("Could not find speaker-notes JSON block in _template.html")

    new_json = json.dumps(notes, ensure_ascii=False)
    html_new = html[: match.start(2)] + new_json + html[match.end(2) :]
    TEMPLATE_PATH.write_text(html_new)


def main() -> None:
    markdown = MD_PATH.read_text()
    notes = parse_markdown_sections(markdown)
    expected = expected_slide_count()

    if len(notes) != expected:
        raise RuntimeError(
            f"speaker_notes_full.md has {len(notes)} sections, but defense_html contains {expected} slides"
        )

    sync_embedded_notes(notes)
    print(
        "Updated defense_html/_template.html from speaker_notes/speaker_notes_full.md "
        f"with {len(notes)} slide notes"
    )


if __name__ == "__main__":
    main()
