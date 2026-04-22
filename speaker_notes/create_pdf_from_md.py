#!/usr/bin/env python3
"""
Convert a markdown speaker-notes file to PDF.

Defaults:
- input:  speaker_notes_full.md
- output: speaker_notes_full.pdf

The script uses pandoc and automatically tries a few PDF backends so it keeps
working across different local setups.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
DEFAULT_NOTES_MD = SCRIPT_DIR / "speaker_notes_full.md"
DEFAULT_TITLE = "Defense Speaker Notes"
ENGINE_PRIORITY = ("lualatex", "xelatex", "weasyprint", "pdflatex")
LATEX_ENGINES = {"lualatex", "xelatex", "pdflatex"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a markdown notes file to PDF with pandoc."
    )
    parser.add_argument(
        "--notes-md",
        nargs="?",
        const=str(DEFAULT_NOTES_MD),
        default=str(DEFAULT_NOTES_MD),
        help=(
            "Markdown notes file to convert. If passed without a value, defaults "
            f"to {DEFAULT_NOTES_MD.name}."
        ),
    )
    parser.add_argument(
        "--output-pdf",
        default=None,
        help="Output PDF path (default: NOTES_FILE stem + .pdf).",
    )
    parser.add_argument(
        "--pdf-engine",
        choices=ENGINE_PRIORITY,
        default=None,
        help="Force a specific pandoc PDF engine instead of auto-selecting one.",
    )
    parser.add_argument(
        "--title",
        default=DEFAULT_TITLE,
        help="Document title for the generated PDF.",
    )
    parser.add_argument(
        "--toc",
        action="store_true",
        help="Include a table of contents.",
    )
    parser.add_argument(
        "--paper",
        choices=["a4", "letter"],
        default="a4",
        help="PDF page size for LaTeX-based engines (default: a4).",
    )
    parser.add_argument(
        "--font-size",
        default="11pt",
        help="Base font size for LaTeX-based engines (default: 11pt).",
    )
    return parser.parse_args()


def require_binary(name: str) -> str:
    path = shutil.which(name)
    if path:
        return path
    raise SystemExit(f"Could not find required binary in PATH: {name}")


def available_engines(requested: str | None) -> list[str]:
    if requested:
        if shutil.which(requested):
            return [requested]
        raise SystemExit(f"Requested PDF engine is not installed: {requested}")

    engines = [engine for engine in ENGINE_PRIORITY if shutil.which(engine)]
    if engines:
        return engines

    raise SystemExit(
        "No supported PDF engine found. Install one of: "
        + ", ".join(ENGINE_PRIORITY)
    )


def build_pandoc_command(
    pandoc: str,
    input_path: Path,
    output_path: Path,
    *,
    engine: str,
    title: str,
    toc: bool,
    paper: str,
    font_size: str,
) -> list[str]:
    command = [
        pandoc,
        input_path.name,
        "--from=gfm+smart",
        "--standalone",
        "--shift-heading-level-by=-2",
        "--metadata",
        f"title={title}",
        "--output",
        str(output_path),
        f"--pdf-engine={engine}",
    ]

    if toc:
        command.extend(["--toc", "--toc-depth=1"])

    if engine in LATEX_ENGINES:
        command.extend(
            [
                "-V",
                f"papersize:{paper}",
                "-V",
                f"fontsize={font_size}",
                "-V",
                "geometry:margin=0.8in",
                "-V",
                "linestretch=1.08",
                "-V",
                "colorlinks=true",
            ]
        )

    return command


def export_pdf(
    input_path: Path,
    output_path: Path,
    *,
    requested_engine: str | None,
    title: str,
    toc: bool,
    paper: str,
    font_size: str,
) -> str:
    pandoc = require_binary("pandoc")
    errors: list[tuple[str, str]] = []

    for engine in available_engines(requested_engine):
        command = build_pandoc_command(
            pandoc,
            input_path,
            output_path,
            engine=engine,
            title=title,
            toc=toc,
            paper=paper,
            font_size=font_size,
        )
        try:
            subprocess.run(
                command,
                cwd=input_path.parent,
                check=True,
                capture_output=True,
                text=True,
            )
            return engine
        except subprocess.CalledProcessError as exc:
            message = (exc.stderr or exc.stdout or str(exc)).strip()
            errors.append((engine, message))

    detail = "\n\n".join(f"{engine}:\n{message}" for engine, message in errors)
    raise SystemExit(f"PDF export failed with all available engines:\n\n{detail}")


def main() -> None:
    args = parse_args()

    notes_path = Path(args.notes_md).expanduser().resolve()
    if not notes_path.exists():
        raise SystemExit(f"Notes file does not exist: {notes_path}")
    if not notes_path.is_file():
        raise SystemExit(f"Notes path is not a file: {notes_path}")

    output_path = (
        Path(args.output_pdf).expanduser().resolve()
        if args.output_pdf
        else notes_path.with_suffix(".pdf")
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    engine = export_pdf(
        notes_path,
        output_path,
        requested_engine=args.pdf_engine,
        title=args.title,
        toc=args.toc,
        paper=args.paper,
        font_size=args.font_size,
    )
    print(f"[pandoc] Exported {notes_path.name} -> {output_path.name} using {engine}")
    print(f"  -> {output_path}")


if __name__ == "__main__":
    main()
