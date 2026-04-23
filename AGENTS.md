# Repository Guide

This repository is a thesis-defense presentation workspace, not a typical app.
The main artifact is a custom HTML slide deck in `defense_html/`, supported by
speaker notes, committee feedback, and the LaTeX thesis source used as
reference material.

## Fast Start

Run the local deck server from the repo root:

```bash
python3 dev.py
```

Then open `http://127.0.0.1:8000/Defense.html`.

What to edit most often:

1. `defense_html/_template.html`
2. one HTML file per slide in `defense_html/slides/`
3. shared styling in `defense_html/deck.css`
4. deck runtime behavior in `defense_html/deck-stage.js`
5. `speaker_notes/speaker_notes_full.md` when slide narrative changes

`dev.py` watches the template and slide files, rebuilds `Defense.html`, and
live-reloads the browser.

Important: slide `01` lives in `_template.html`. The per-slide files cover
slides `02` through `53`, plus backup slides `B1` through `B13`.

## Repo Map

- `dev.py`
  - Local rebuild + live-reload server.
  - Run this from the repo root.
  - Concatenates `defense_html/slides/*.html` into the `<!--SLIDES-->` placeholder.

- `defense_html/`
  - `_template.html`: deck shell, title slide, embedded speaker notes JSON, shared JS hooks.
  - `slides/NN-*.html`: one file per main slide.
  - `slides/B*-*.html`: one file per backup/Q&A slide.
  - `deck.css`: global visual system.
  - `deck-stage.js`: runtime deck behavior.
  - `figures/`: images, logos, and PDFs used by slides.
  - `Defense.html`: generated output.
  - `split_slides.py`: one-off utility for splitting older section files into per-slide files.

- `speaker_notes/`
  - `speaker_notes_full.md`: full spoken narrative, slide by slide, including backups.
  - `speaker_notes_pptx.md`: shorter, bulleted presenter-note version for PPTX / LibreOffice presenter view.
  - `update_speaker_notes.py`: syncs `speaker_notes_full.md` into the embedded notes JSON in `defense_html/_template.html` and validates note count against the deck. It does not touch `speaker_notes_pptx.md`.
  - `create_mp3_from_md.py`: optional utility for generating audio from the Markdown notes.

- `feedback_21_april.md`
  - Committee feedback and slide-by-slide fixes.
  - Treat this as active design guidance when polishing slides.

- `dissertation_latex/`
  - Thesis source and reference material.
  - Useful for wording, provenance, terminology, and deeper technical detail.

## Editing Rules That Matter

- The editable source of truth is the per-slide HTML in `defense_html/slides/`
  and the wrapper in `defense_html/_template.html`.
- `Defense.html` is generated. Any manual edits there will be overwritten.
- Slide ordering comes from filename prefixes:
  - `02-...html` to `53-...html` for main slides
  - `B1-...html` to `B13-...html` for backup slides
- `slides/_archive/` is intentionally ignored by the dev server.
- Many slide files are stored as single-line `<section>...</section>` blocks.
  Preserve the section wrapper, slide counter, and `data-*` metadata when editing.
- Global styling changes belong in `deck.css`.
- One-off slide-specific layout changes usually stay inline in that slide's HTML.

## Notes And Sync Gotchas

- The deck embeds its own speaker notes inside `defense_html/_template.html`
  under the `speaker-notes` JSON block.
- `speaker_notes/speaker_notes_full.md` is the authored source of truth for the
  long-form notes.
- `speaker_notes/speaker_notes_pptx.md` is a separate authored source for
  LibreOffice / PowerPoint presenter notes. Keep it short, bulleted, and easy to
  scan while speaking.
- `dev.py` does not sync Markdown notes into the deck. After changing
  `speaker_notes/speaker_notes_full.md`, run
  `python3 speaker_notes/update_speaker_notes.py` to refresh the embedded notes
  in `_template.html`, then let `dev.py` rebuild `Defense.html`.
- `speaker_notes/update_speaker_notes.py` only updates the HTML deck notes. It
  must not overwrite `speaker_notes/speaker_notes_pptx.md`.
- After changing `speaker_notes/speaker_notes_pptx.md`, regenerate the PPTX with
  `python3 defense_html/extract_to_pptx.py --output defense.pptx`. If you keep a
  second copy under `defense_html/`, regenerate that one too.
- If a narrative change matters both on-slide and in notes, update both places.

## Working Conventions

- Optimize for projection readability first: fewer words, larger type, clearer spacing.
- Use the contribution colors consistently:
  - AERO
  - OmniFORE
  - AgentEdge
- Color-to-contribution mapping for this deck:
  - Blue = AERO (chapter3 material in dissertation slides)
  - Orange = OmniFORE (chapter4 material in dissertation slides)
  - Pink = AgentEdge (chapter5 material in dissertation slides)
- Keep generic infrastructure/framing elements neutral unless a slide is making
  a deliberate contribution-specific point.
- Prefer small, local edits over broad rewrites when adjusting slide copy/layout.
- Prefer fast iteration and avoid asking many questions; if details are ambiguous,
  proceed with the safest minimal change and refine by visual check.
- Multiple agents are often editing slides in parallel, so avoid broad automatic
renumbering or bulk search/replace operations unless they are scoped and
reconciled first.
- Math is absolutely not allowed anywhere in this presentation.
- After any slide content change, update
  `speaker_notes/speaker_notes_full.md` so slide notes remain synchronized.
- After editing notes, run `python3 speaker_notes/update_speaker_notes.py` to
  sync the embedded presenter notes in the deck.
- Verify visual changes in the browser; this repo is presentation-first, so
  manual review matters more than automated testing.

## Common Tasks

### Edit a normal slide

Update the matching file in `defense_html/slides/`, for example
`defense_html/slides/03-operational-setting.html`.

### Edit the title slide or global shell

Update `defense_html/_template.html`.

This is also where shared scripts, the `<!--SLIDES-->` insertion point, and the
embedded speaker notes live.

### Edit speaker notes

Update `speaker_notes/speaker_notes_full.md`.

Then run `python3 speaker_notes/update_speaker_notes.py` so the embedded notes
inside `defense_html/_template.html` stay in sync with the Markdown source.

### Edit PPTX / LibreOffice speaker notes

Update `speaker_notes/speaker_notes_pptx.md`.

Keep these notes concise and bulleted for presenter view. They are intentionally
separate from `speaker_notes_full.md`.

Then regenerate the PPTX with
`python3 defense_html/extract_to_pptx.py --output defense.pptx` (and
`defense_html/defense.pptx` too if you keep both exports in sync).

### Change the global look

Update `defense_html/deck.css`.

### Add or replace an asset

Put the asset in `defense_html/figures/` and reference it with a relative path
from the slide/template HTML.

### Re-split slides from older section files

Use `defense_html/split_slides.py` only if you intentionally need to regenerate
per-slide files from the older grouped section sources. This is not part of the
normal editing loop.

## Verification Checklist

After making changes:

1. Run `python3 dev.py` from the repo root.
2. If `speaker_notes/speaker_notes_full.md` changed, run
   `python3 speaker_notes/update_speaker_notes.py`.
3. If `speaker_notes/speaker_notes_pptx.md` changed, regenerate the PPTX with
   `python3 defense_html/extract_to_pptx.py --output defense.pptx`.
4. Confirm the target slide rebuilds into `Defense.html`.
5. Thoroughly check in-browser that every slide block still fits: text overflow is the most common regression.
6. Check the slide for overflow, spacing, and readability.
7. Prefer fast iteration loops: rerun/reload quickly and visually verify each slide change before moving on.
8. Make sure slide numbering, ordering, and section color semantics still make sense.

## Known Sources Of Confusion

- Some prose/docstrings still reference older paths such as `defense_AI` or
  external working directories. The active deck in this repo is `defense_html/`.
- Older docs may still reference top-level notes files. The active notes live in
  `speaker_notes/`.
- Slide `01` is not a separate file in `slides/`; it lives in `_template.html`.
- The browser preview depends on external CDNs for Google Fonts and `pdf.js`, so
  offline rendering may differ.

If you are new here, start with `dev.py`, `defense_html/_template.html`, one or
two representative files under `defense_html/slides/`, and `feedback_21_april.md`.
