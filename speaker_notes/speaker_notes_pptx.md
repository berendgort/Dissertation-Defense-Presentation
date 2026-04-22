<!--
PPTX notes format:
- Start each block with `### Slide 01 · Title` or `### Backup B1 · Short label`.
- The exporter matches on the slide token only: `01`, `02`, ..., `B1`, `B2`, ...
- Put plain presenter text below the heading. Literal `- ` list markers are kept in the exported notes.
- Leave the body empty if a slide should have no speaker notes in the exported `.pptx`.
-->

### Slide 01 · Title

Good morning. These notes are a placeholder example for the PPTX export.

- Introduce the thesis title.
- Mention the supervisors and industrial partner.

### Slide 25 · Training the model

Phase two has two steps.

- S5 equal scale: rescale each trace so large services do not dominate training.
- S6 efficient attention: scan the full window, keep the strongest matches, then drop weak links so long windows stay cheap.
- Generalization comes from matching patterns rather than service identity.
