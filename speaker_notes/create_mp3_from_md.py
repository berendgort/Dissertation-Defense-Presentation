#!/usr/bin/env python3
"""
Transcribe audio files to text, or convert markdown speaker notes to MP3.

Modes:
1. Default: transcribe audio files from a folder to .txt files.
2. `--notes-md`: turn a markdown notes file into spoken audio.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import re
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).parent
SUPPORTED_EXTENSIONS = {".mp3", ".ogg", ".m4a", ".wav", ".mp4"}
DEFAULT_NOTES_MD = SCRIPT_DIR / "speaker_notes_full.md"

# Edge-TTS defaults (fallback engine).
DEFAULT_EDGE_VOICE = "en-US-AndrewMultilingualNeural"
DEFAULT_EDGE_RATE = "-4%"

# OpenAI TTS defaults (preferred engine for notes mode).
DEFAULT_TTS_ENGINE = "openai"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini-tts"
DEFAULT_OPENAI_VOICE = "verse"      # PLEASE USE VERSE FOR THE DEFENSE
DEFAULT_OPENAI_INSTRUCTIONS = (
    "You are delivering a doctoral thesis defense at Universitat Politècnica de "
    "Catalunya. Speak in a calm, confident, academic tone — warm but authoritative, "
    "measured pace, clear articulation, natural sentence rhythm with brief pauses "
    "between clauses. Do not sound robotic or overly enthusiastic. Imagine a senior "
    "PhD candidate walking a dissertation committee through their contributions."
)
# OpenAI's /v1/audio/speech accepts up to ~4096 characters per request.
DEFAULT_OPENAI_MAX_CHARS = 3800

NOTES_SEPARATOR_RE = re.compile(r"^-{10,}\s*$")
SLIDE_HEADER_RE = re.compile(r"^Slide\s+(\d+)\s+-\s+(.+)$")
# Markdown-heading format: e.g. "### Slide 01 · Title" or "### Backup B1 · Title".
SLIDE_HEADING_RE = re.compile(
    r"^#{1,6}\s*(?:Slide\s+0*(\d+)|Backup\s+(B\d+))\s*[\u2014\u2013\-:\u00B7]\s*(.+?)\s*$",
    re.IGNORECASE,
)

ASSEMBLYAI_API_KEY_ENV = "ASSEMBLYAI_API_KEY"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


@dataclass
class SlideNotes:
    number: str
    title: str
    say: list[str]
    notes: list[str]
    next_lines: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Transcribe audio files in INPUT_DIR to .txt files, or convert a "
            "markdown speaker-notes file to a male-voice MP3."
        )
    )
    parser.add_argument(
        "input_dir",
        nargs="?",
        default=str(SCRIPT_DIR / "mp3"),
        help="Folder containing audio files for transcription mode.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output folder for .txt transcripts (default: INPUT_DIR/../transcriptions).",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively scan INPUT_DIR for audio files.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Number of files to transcribe concurrently (default: 8).",
    )
    parser.add_argument(
        "--notes-md",
        nargs="?",
        const=str(DEFAULT_NOTES_MD),
        default=None,
        help=(
            "Markdown notes file to convert to MP3. If passed without a value, "
            f"defaults to {DEFAULT_NOTES_MD.name}."
        ),
    )
    parser.add_argument(
        "--output-mp3",
        default=None,
        help="Output MP3 path for notes mode (default: NOTES_FILE stem + .mp3).",
    )
    parser.add_argument(
        "--engine",
        choices=["openai", "edge"],
        default=DEFAULT_TTS_ENGINE,
        help=(
            "TTS engine for notes mode. 'openai' uses the OpenAI /v1/audio/speech "
            f"endpoint (default). 'edge' uses edge-tts (free, lower quality)."
        ),
    )
    parser.add_argument(
        "--openai-voice",
        default=DEFAULT_OPENAI_VOICE,
        help=(
            "OpenAI TTS voice. Male/neutral options good for a defense: "
            "onyx, echo, ash, ballad, sage, verse. "
            f"Default: {DEFAULT_OPENAI_VOICE}."
        ),
    )
    parser.add_argument(
        "--openai-model",
        default=DEFAULT_OPENAI_MODEL,
        help=(
            "OpenAI TTS model. 'gpt-4o-mini-tts' supports --openai-instructions for "
            "style steering and is the most natural. 'tts-1-hd' is the previous "
            f"generation, still high quality. Default: {DEFAULT_OPENAI_MODEL}."
        ),
    )
    parser.add_argument(
        "--openai-instructions",
        default=DEFAULT_OPENAI_INSTRUCTIONS,
        help=(
            "Style/tone instructions for the OpenAI TTS model "
            "(only used when model supports it, i.e. gpt-4o-mini-tts)."
        ),
    )
    parser.add_argument(
        "--voice",
        default=DEFAULT_EDGE_VOICE,
        help=(
            "edge-tts voice (only used when --engine edge). "
            f"Default: {DEFAULT_EDGE_VOICE}."
        ),
    )
    parser.add_argument(
        "--rate",
        default=DEFAULT_EDGE_RATE,
        help=(
            "edge-tts speech rate (only used when --engine edge). "
            f"Default: {DEFAULT_EDGE_RATE}."
        ),
    )
    parser.add_argument(
        "--say-only",
        action="store_true",
        help="Speak only the 'Say' blocks from the markdown notes.",
    )
    parser.add_argument(
        "--no-slide-titles",
        action="store_true",
        help="Do not announce slide numbers and slide titles in notes mode.",
    )
    parser.add_argument(
        "--max-chars-per-chunk",
        type=int,
        default=None,
        help=(
            "Maximum characters per TTS request chunk. Default: 3800 for OpenAI, "
            "2500 for edge."
        ),
    )
    return parser.parse_args()


def require_env(name: str) -> str:
    value = os.getenv(name)
    if value:
        return value
    raise RuntimeError(f"Set {name} in your environment before running this script.")


def get_openai_api_key() -> str:
    return require_env(OPENAI_API_KEY_ENV)


def get_assemblyai_api_key() -> str:
    return require_env(ASSEMBLYAI_API_KEY_ENV)


def build_transcription_config():
    # Import lazily so `--help` works even if deps aren't installed yet.
    import assemblyai as aai

    aai.settings.api_key = get_assemblyai_api_key()

    # Dissertation / PhD feedback vocabulary
    keyterms = [
        # Academic / dissertation
        "dissertation",
        "thesis",
        "PhD",
        "doctorate",
        "doctoral",
        "supervisor",
        "advisor",
        "committee",
        "defense",
        "defence",
        "viva",
        "abstract",
        "introduction",
        "conclusion",
        "chapter",
        "section",
        "subsection",
        "bibliography",
        "references",
        "citation",
        "figure",
        "table",
        "equation",
        "appendix",
        "methodology",
        "literature review",
        "state of the art",
        "contribution",
        "hypothesis",
        "manuscript",
        "draft",
        "revision",
        "feedback",
        "reviewer",
        "peer review",
        # Institution-specific
        "UPC",
        "Universitat Politecnica de Catalunya",
        "Barcelona",
        "Catalonia",
        # Technical writing
        "LaTeX",
        "BibTeX",
        "PDF",
        "overleaf",
        # Research terms
        "dataset",
        "benchmark",
        "baseline",
        "experiment",
        "evaluation",
        "validation",
        "metric",
        "parameter",
        "algorithm",
        "model",
        "framework",
        "approach",
        "contribution",
        "novelty",
    ]

    # Universal is AssemblyAI's flagship transcription model.
    config = aai.TranscriptionConfig(
        speech_model=aai.SpeechModel.universal,
        punctuate=True,
        format_text=True,
        word_boost=keyterms,
    )
    return aai, config


def transcribe_file(aai, config, audio_path: Path, output_path: Path) -> bool:
    """Transcribe a single audio file to txt."""
    print(f"Transcribing: {audio_path.name}", flush=True)

    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(str(audio_path))

    if transcript.status == aai.TranscriptStatus.error:
        print(f"  ERROR [{audio_path.name}]: {transcript.error}", flush=True)
        return False

    output_path.write_text(transcript.text or "", encoding="utf-8")
    print(f"  -> {output_path.name}", flush=True)
    return True


def normalize_spoken_line(line: str) -> str:
    cleaned = re.sub(r"^\s*-\s*", "", line.strip())
    cleaned = cleaned.replace("->", " to ")
    cleaned = cleaned.replace("<=", " less than or equal to ")
    cleaned = cleaned.replace(">=", " greater than or equal to ")
    cleaned = cleaned.replace("&", " and ")
    cleaned = cleaned.replace("Q&A", "Q and A")
    cleaned = cleaned.replace("vs.", "versus")
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    return cleaned


def parse_slide_block(block_lines: list[str]) -> SlideNotes | None:
    lines = [line.rstrip() for line in block_lines if line.strip()]
    if not lines:
        return None

    match = SLIDE_HEADER_RE.match(lines[0].strip())
    if not match:
        return None

    slide = SlideNotes(
        number=match.group(1),
        title=match.group(2).strip(),
        say=[],
        notes=[],
        next_lines=[],
    )

    current_section: str | None = None
    for raw_line in lines[1:]:
        line = raw_line.strip()
        if not line or line.startswith("Time:"):
            continue
        if line == "Say:":
            current_section = "say"
            continue
        if line == "Notes:":
            current_section = "notes"
            continue
        if line == "Next:":
            current_section = "next"
            continue
        if current_section is None:
            continue

        spoken_line = normalize_spoken_line(raw_line)
        if not spoken_line:
            continue

        if current_section == "say":
            slide.say.append(spoken_line)
        elif current_section == "notes":
            slide.notes.append(spoken_line)
        elif current_section == "next":
            slide.next_lines.append(spoken_line)

    return slide


def parse_notes_markdown(markdown_text: str) -> list[SlideNotes]:
    blocks: list[list[str]] = []
    current_block: list[str] = []

    for line in markdown_text.splitlines():
        if NOTES_SEPARATOR_RE.match(line.strip()):
            if current_block:
                blocks.append(current_block)
                current_block = []
            continue
        current_block.append(line)

    if current_block:
        blocks.append(current_block)

    slides = []
    for block in blocks:
        slide = parse_slide_block(block)
        if slide is not None:
            slides.append(slide)

    if not slides:
        slides = parse_heading_style_markdown(markdown_text)

    return slides


def clean_markdown_for_speech(text: str) -> str:
    """Strip common Markdown decorations so TTS reads prose cleanly."""
    cleaned = re.sub(r"`([^`]+)`", r"\1", text)
    cleaned = re.sub(r"\*\*([^*]+)\*\*", r"\1", cleaned)
    cleaned = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\1", cleaned)
    cleaned = re.sub(r"_([^_\n]+)_", r"\1", cleaned)
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    cleaned = cleaned.replace("—", ", ").replace("–", ", ")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def spoken_slide_label(number: str) -> str:
    value = number.strip().upper()
    if value.startswith("B"):
        return f"Backup B {int(value[1:])}"
    return f"Slide {int(value)}"


def parse_heading_style_markdown(markdown_text: str) -> list[SlideNotes]:
    """Parse a file shaped like:

        ### Slide 01 — Title
        free-form paragraph(s)

        ### Slide 02 — Title
        ...

    Everything between one slide heading and the next becomes the spoken body.
    """
    lines = markdown_text.splitlines()
    slides: list[SlideNotes] = []

    current: SlideNotes | None = None
    body_buffer: list[str] = []

    def flush() -> None:
        nonlocal current, body_buffer
        if current is None:
            return
        paragraphs: list[str] = []
        paragraph: list[str] = []
        for raw in body_buffer:
            stripped = raw.strip()
            if not stripped:
                if paragraph:
                    paragraphs.append(" ".join(paragraph))
                    paragraph = []
                continue
            paragraph.append(stripped)
        if paragraph:
            paragraphs.append(" ".join(paragraph))

        for paragraph_text in paragraphs:
            spoken = clean_markdown_for_speech(paragraph_text)
            if spoken:
                current.say.append(spoken)

        if current.say:
            slides.append(current)
        current = None
        body_buffer = []

    for raw_line in lines:
        stripped = raw_line.strip()
        heading_match = SLIDE_HEADING_RE.match(stripped)
        if heading_match:
            flush()
            number = heading_match.group(1) or heading_match.group(2)
            if number is None:
                continue
            current = SlideNotes(
                number=number.upper(),
                title=clean_markdown_for_speech(heading_match.group(3)),
                say=[],
                notes=[],
                next_lines=[],
            )
            continue

        if current is None:
            continue
        body_buffer.append(raw_line)

    flush()
    return slides


def build_spoken_script(
    notes_path: Path,
    *,
    say_only: bool,
    include_slide_titles: bool,
) -> str:
    markdown_text = notes_path.read_text(encoding="utf-8")
    slides = parse_notes_markdown(markdown_text)
    if not slides:
        raise SystemExit(f"No slide blocks found in {notes_path}")

    spoken_slides = []
    for slide in slides:
        parts = []
        if include_slide_titles:
            parts.append(f"{spoken_slide_label(slide.number)}. {normalize_spoken_line(slide.title)}.")
        if slide.say:
            parts.append(" ".join(slide.say) + ".")
        if not say_only and slide.notes:
            parts.append(" ".join(slide.notes) + ".")
        if not say_only and slide.next_lines:
            parts.append("Next. " + " ".join(slide.next_lines) + ".")

        slide_text = "\n\n".join(part.strip() for part in parts if part.strip())
        if slide_text:
            spoken_slides.append(slide_text)

    if not spoken_slides:
        raise SystemExit(f"No speakable text found in {notes_path}")

    return "\n\n".join(spoken_slides)


def split_long_text(text: str, max_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]

    chunks = []
    current = ""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())

    for sentence in sentences:
        if not sentence:
            continue

        if len(sentence) > max_chars:
            words = sentence.split()
            word_chunk = ""
            for word in words:
                candidate = word if not word_chunk else f"{word_chunk} {word}"
                if len(candidate) <= max_chars:
                    word_chunk = candidate
                else:
                    if current:
                        chunks.append(current)
                        current = ""
                    if word_chunk:
                        chunks.append(word_chunk)
                    word_chunk = word
            if word_chunk:
                if current:
                    chunks.append(current)
                    current = ""
                chunks.append(word_chunk)
            continue

        candidate = sentence if not current else f"{current} {sentence}"
        if len(candidate) <= max_chars:
            current = candidate
        else:
            chunks.append(current)
            current = sentence

    if current:
        chunks.append(current)
    return chunks


def split_text_for_tts(text: str, max_chars: int) -> list[str]:
    paragraphs = [paragraph.strip() for paragraph in re.split(r"\n\s*\n", text) if paragraph.strip()]
    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        subparts = split_long_text(paragraph, max_chars)
        for subpart in subparts:
            candidate = subpart if not current else f"{current}\n\n{subpart}"
            if len(candidate) <= max_chars:
                current = candidate
            else:
                if current:
                    chunks.append(current)
                current = subpart

    if current:
        chunks.append(current)
    return chunks


def copy_or_concatenate_mp3_files(part_files: list[Path], output_path: Path, temp_dir: Path) -> None:
    if not part_files:
        raise SystemExit("No MP3 parts were generated.")

    if len(part_files) == 1:
        shutil.copyfile(part_files[0], output_path)
        return

    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        concat_file = temp_dir / "concat_inputs.txt"
        concat_file.write_text(
            "".join(f"file '{part_file.as_posix()}'\n" for part_file in part_files),
            encoding="utf-8",
        )
        subprocess.run(
            [
                ffmpeg,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-c",
                "copy",
                str(output_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return

    # Fallback: concatenate MP3 frames directly. This is widely supported and
    # avoids requiring ffmpeg for a simple offline merge.
    with output_path.open("wb") as destination:
        for part_file in part_files:
            destination.write(part_file.read_bytes())


async def save_edge_tts_chunk(text: str, voice: str, rate: str, output_path: Path) -> None:
    try:
        import edge_tts
    except ImportError as exc:
        raise SystemExit(
            "edge-tts engine requires `edge-tts`. Install it with: pip install edge-tts"
        ) from exc

    communicator = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    await communicator.save(str(output_path))


def _build_openai_client():
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise SystemExit(
            "openai engine requires the `openai` package. "
            "Install it with: pip install --user openai"
        ) from exc

    return OpenAI(api_key=get_openai_api_key())


# Models that accept the `instructions` parameter for style steering.
_OPENAI_MODELS_WITH_INSTRUCTIONS = {"gpt-4o-mini-tts"}


def save_openai_tts_chunk(
    client,
    text: str,
    *,
    voice: str,
    model: str,
    instructions: str | None,
    output_path: Path,
) -> None:
    create_kwargs: dict = {
        "model": model,
        "voice": voice,
        "input": text,
        "response_format": "mp3",
    }
    if instructions and model in _OPENAI_MODELS_WITH_INSTRUCTIONS:
        create_kwargs["instructions"] = instructions

    with client.audio.speech.with_streaming_response.create(**create_kwargs) as response:
        response.stream_to_file(str(output_path))


async def synthesize_with_edge(
    chunks: list[str],
    output_path: Path,
    *,
    voice: str,
    rate: str,
) -> None:
    print(
        f"[edge-tts] Synthesizing {len(chunks)} chunk(s) with voice {voice} at rate {rate}",
        flush=True,
    )
    with tempfile.TemporaryDirectory(prefix="notes_to_mp3_edge_") as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        part_files: list[Path] = []

        for index, chunk in enumerate(chunks, start=1):
            part_file = temp_dir / f"chunk_{index:03d}.mp3"
            print(f"  edge chunk {index}/{len(chunks)}", flush=True)
            await save_edge_tts_chunk(chunk, voice, rate, part_file)
            part_files.append(part_file)

        copy_or_concatenate_mp3_files(part_files, output_path, temp_dir)


def synthesize_with_openai(
    chunks: list[str],
    output_path: Path,
    *,
    voice: str,
    model: str,
    instructions: str | None,
) -> None:
    client = _build_openai_client()

    style_note = " (with style instructions)" if (
        instructions and model in _OPENAI_MODELS_WITH_INSTRUCTIONS
    ) else ""
    print(
        f"[openai] Synthesizing {len(chunks)} chunk(s) with model={model} voice={voice}{style_note}",
        flush=True,
    )

    with tempfile.TemporaryDirectory(prefix="notes_to_mp3_openai_") as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        part_files: list[Path] = []

        for index, chunk in enumerate(chunks, start=1):
            part_file = temp_dir / f"chunk_{index:03d}.mp3"
            print(
                f"  openai chunk {index}/{len(chunks)} ({len(chunk)} chars)",
                flush=True,
            )
            save_openai_tts_chunk(
                client,
                chunk,
                voice=voice,
                model=model,
                instructions=instructions,
                output_path=part_file,
            )
            part_files.append(part_file)

        copy_or_concatenate_mp3_files(part_files, output_path, temp_dir)


def run_notes_mode(args: argparse.Namespace) -> None:
    notes_path = Path(args.notes_md or DEFAULT_NOTES_MD).expanduser().resolve()
    if not notes_path.exists():
        raise SystemExit(f"Notes file does not exist: {notes_path}")
    if not notes_path.is_file():
        raise SystemExit(f"Notes path is not a file: {notes_path}")

    output_path = (
        Path(args.output_mp3).expanduser().resolve()
        if args.output_mp3
        else notes_path.with_suffix(".mp3")
    )

    spoken_text = build_spoken_script(
        notes_path,
        say_only=args.say_only,
        include_slide_titles=not args.no_slide_titles,
    )

    default_max = DEFAULT_OPENAI_MAX_CHARS if args.engine == "openai" else 2500
    max_chars = args.max_chars_per_chunk if args.max_chars_per_chunk is not None else default_max
    max_chars = max(250, max_chars)

    chunks = split_text_for_tts(spoken_text, max_chars)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.engine == "openai":
        synthesize_with_openai(
            chunks,
            output_path,
            voice=args.openai_voice,
            model=args.openai_model,
            instructions=args.openai_instructions,
        )
    else:
        asyncio.run(
            synthesize_with_edge(
                chunks,
                output_path,
                voice=args.voice,
                rate=args.rate,
            )
        )

    print(f"  -> {output_path}", flush=True)


def run_transcription_mode(args: argparse.Namespace) -> None:
    input_dir = Path(args.input_dir).expanduser().resolve()
    output_dir = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else (input_dir.parent / "transcriptions")
    )

    if not input_dir.exists():
        raise SystemExit(f"Input directory does not exist: {input_dir}")
    if not input_dir.is_dir():
        raise SystemExit(f"Input path is not a directory: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    aai, config = build_transcription_config()

    if args.recursive:
        audio_files = [
            file_path
            for file_path in input_dir.rglob("*")
            if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS
        ]
    else:
        audio_files = [
            file_path
            for file_path in input_dir.iterdir()
            if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS
        ]

    if not audio_files:
        print(f"No audio files found in {input_dir}")
        return

    print(f"Found {len(audio_files)} audio file(s)")
    print(f"Using {args.workers} parallel workers\n", flush=True)

    pending: list[tuple[Path, Path]] = []
    already_done = 0
    for audio_file in sorted(audio_files):
        output_file = output_dir / f"{audio_file.stem}.txt"
        if output_file.exists():
            print(f"Skipping (already exists): {audio_file.name}", flush=True)
            already_done += 1
        else:
            pending.append((audio_file, output_file))

    success = already_done
    if pending:
        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            futures = {
                pool.submit(transcribe_file, aai, config, src, dst): src
                for src, dst in pending
            }
            for future in as_completed(futures):
                src = futures[future]
                try:
                    if future.result():
                        success += 1
                except Exception as exc:
                    print(f"  EXCEPTION transcribing {src.name}: {exc}", flush=True)

    print(f"\nDone: {success}/{len(audio_files)} transcribed")
    print(f"Output directory: {output_dir}")


def main() -> None:
    args = parse_args()
    if args.notes_md:
        run_notes_mode(args)
        return
    run_transcription_mode(args)


if __name__ == "__main__":
    main()