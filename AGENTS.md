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
p

1. `defense_html/_template.html`
2. one HTML file per slide in `defense_html/slides/`
3. shared styling in `defense_html/deck.css`
4. deck runtime behavior in `defense_html/deck-stage.js`

`dev.py` watches the template and slide files, rebuilds `Defense.html`, and
live-reloads the browser.

Important: slide `01` lives in `_template.html`. The per-slide files mostly
cover slides `02` through `56`, plus backup slides `B1` through `B13`.

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

- `DEFENSE_SPEAKER_NOTES_FULL.md`
  - Full spoken narrative, slide by slide.

- `DEFENSE_POWERPOINT_NOTES.md`
  - Shorter presenter-note version for glanceable delivery.

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
  - `02-...html` to `56-...html` for main slides
  - `B1-...html` to `B13-...html` for backup slides
- `slides/_archive/` is intentionally ignored by the dev server.
- Many slide files are stored as single-line `<section>...</section>` blocks.
  Preserve the section wrapper, slide counter, and `data-*` metadata when editing.
- Global styling changes belong in `deck.css`.
- One-off slide-specific layout changes usually stay inline in that slide's HTML.

## Notes And Sync Gotchas

- The deck embeds its own speaker notes inside `defense_html/_template.html`
  under the `speaker-notes` JSON block.
- The Markdown notes files are useful authoring/reference docs, but they are not
  automatically synced into the rendered deck by `dev.py`.
- If a narrative change matters both on-slide and in notes, update both places.

## Working Conventions

- Optimize for projection readability first: fewer words, larger type, clearer spacing.
- Use the contribution colors consistently:
  - AERO
  - OmniFORE
  - AgentEdge
- Keep generic infrastructure/framing elements neutral unless a slide is making
  a deliberate contribution-specific point.
- Prefer small, local edits over broad rewrites when adjusting slide copy/layout.
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
2. Confirm the target slide rebuilds into `Defense.html`.
3. Check the slide in-browser for overflow, spacing, and readability.
4. Make sure slide numbering, ordering, and section color semantics still make sense.

## Known Sources Of Confusion

- Some prose/docstrings still reference older paths such as `defense_AI` or
  external working directories. The active deck in this repo is `defense_html/`.
- Slide `01` is not a separate file in `slides/`; it lives in `_template.html`.
- The browser preview depends on external CDNs for Google Fonts and `pdf.js`, so
  offline rendering may differ.

If you are new here, start with `dev.py`, `defense_html/_template.html`, one or
two representative files under `defense_html/slides/`, and `feedback_21_april.md`.
