#!/usr/bin/env python3
"""Split the five section files (framing/aero/omnifore/agent/synth) into one
HTML file per slide, named by the authoritative counter shown inside the slide
chrome (``<span class="num">NN</span>`` / ``Bn``).

Run once:
    python3 defense_AI/split_slides.py

Output: ``defense_AI/slides/NN-slug.html`` (e.g. ``02-outline.html``,
``B1-agentedge-s35-defense.html``).  Source section files are archived to
``defense_AI/slides/_archive/`` so nothing is lost.

The builder (``dev.py``) is updated separately to read per-slide files.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLIDES = HERE / "slides"
ARCHIVE = SLIDES / "_archive"

SECTION_FILES = [
    "framing.html",
    "aero.html",
    "omnifore.html",
    "agent.html",
    "synth.html",
]

SECTION_OPEN_RE = re.compile(r'<section\s+class="slide"[^>]*>')
COUNTER_RE = re.compile(r'<span\s+class="num">([^<]+)</span>')
DATA_LABEL_RE = re.compile(r'data-label="([^"]+)"')


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def split_section_file(path: Path) -> list[tuple[str, str]]:
    """Return a list of (counter, html_body) for each slide in *path*.

    - ``counter`` is the authoritative slide number as shown in the deck
      (``01``–``56`` or ``B1``–``B8``).
    - ``html_body`` is the full ``<section …>…</section>`` with a trailing
      newline, trimmed of trailing comments/whitespace between slides.
    """
    raw = path.read_text()
    opens = [m.start() for m in SECTION_OPEN_RE.finditer(raw)]
    if not opens:
        return []

    results: list[tuple[str, str]] = []
    for i, start in enumerate(opens):
        end_boundary = opens[i + 1] if i + 1 < len(opens) else len(raw)
        chunk = raw[start:end_boundary]

        # Keep everything up to and including the LAST </section> before the
        # next slide.  Anything after (blank lines, HTML comments) is section
        # glue and gets discarded.  If no </section> is present in the chunk
        # (the known agent.html bug), append one.
        last_close = chunk.rfind("</section>")
        if last_close == -1:
            body = chunk.rstrip() + "\n</section>"
        else:
            body = chunk[: last_close + len("</section>")]

        counter_match = COUNTER_RE.search(body)
        if not counter_match:
            raise RuntimeError(
                f"No <span class='num'> found in slide starting at byte {start} of {path.name}"
            )
        counter = counter_match.group(1).strip()
        label_match = DATA_LABEL_RE.search(body)
        label = label_match.group(1) if label_match else counter
        results.append((counter, label, body.rstrip() + "\n"))  # type: ignore[arg-type]
    return results  # type: ignore[return-value]


LEADING_NUMBER_RE = re.compile(r"^\s*(?:\d+|B\d+)\s+", re.IGNORECASE)


def label_to_slug(counter: str, label: str) -> str:  # noqa: ARG001
    """Strip any leading numeric/B-prefix token from the data-label and slugify.

    ``"02 Outline"`` → ``"outline"``; ``"11 AERO Problem"`` → ``"aero-problem"``
    (even when the label's leading number disagrees with the counter, which
    happens in the original aero/omnifore/agent files); ``"B1 AgentEdge S35
    defense"`` → ``"agentedge-s35-defense"``.
    """
    rest = LEADING_NUMBER_RE.sub("", label)
    return slugify(rest) or "slide"


def sort_key(counter: str) -> tuple[int, int]:
    """Sort numeric slides ascending, then B-backups ascending."""
    if counter.upper().startswith("B"):
        return (1, int(counter[1:]))
    return (0, int(counter))


def main() -> None:
    ARCHIVE.mkdir(exist_ok=True)

    # Allow idempotent re-runs: when the section files have already been
    # deleted but the archive still exists, split straight from the archive.
    all_slides: list[tuple[str, str, str, str]] = []  # (counter, label, body, source)
    for name in SECTION_FILES:
        src = SLIDES / name
        if not src.exists():
            archived = ARCHIVE / name
            if archived.exists():
                src = archived
            else:
                print(f"[skip] missing {SLIDES / name} (no archive either)")
                continue
        for counter, label, body in split_section_file(src):  # type: ignore[misc]
            all_slides.append((counter, label, body, name))

    # Drop previously emitted per-slide files so renames (e.g. slug fixes) do
    # not leave stale duplicates behind.
    for stale in SLIDES.glob("*.html"):
        if stale.name not in SECTION_FILES:
            stale.unlink()

    # Sanity: counters unique and fully cover expected range.
    counters = [s[0] for s in all_slides]
    if len(counters) != len(set(counters)):
        dupes = [c for c in counters if counters.count(c) > 1]
        raise RuntimeError(f"Duplicate counters: {sorted(set(dupes))}")

    expected = {f"{n:02d}" for n in range(2, 57)} | {f"B{n}" for n in range(1, 9)}
    missing = expected - set(counters)
    extra = set(counters) - expected
    if missing:
        print(f"[warn] missing counters: {sorted(missing)}")
    if extra:
        print(f"[warn] unexpected counters: {sorted(extra)}")

    all_slides.sort(key=lambda s: sort_key(s[0]))

    # Archive old section files then remove from slides/.
    for name in SECTION_FILES:
        src = SLIDES / name
        if src.exists():
            shutil.copy2(src, ARCHIVE / name)

    written: list[str] = []
    for counter, label, body, source in all_slides:
        slug = label_to_slug(counter, label)
        fname = f"{counter}-{slug}.html"
        (SLIDES / fname).write_text(body)
        written.append(fname)
        print(f"[write] {fname}  ({len(body):>6} chars)  ← {source}")

    # Remove the original concatenated files now that per-slide files exist.
    for name in SECTION_FILES:
        src = SLIDES / name
        if src.exists():
            src.unlink()

    print()
    print(f"[done] {len(written)} slides written to {SLIDES}")
    print(f"[done] originals archived at {ARCHIVE}")


if __name__ == "__main__":
    main()
