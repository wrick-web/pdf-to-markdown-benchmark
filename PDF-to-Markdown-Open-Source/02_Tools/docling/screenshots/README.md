# Screenshots — Docling (Round 1 execution attempt)

This sandbox has no GUI or browser, so nothing here is a screen capture.
Everything below is either a real rasterization of a real file, or a
real captured log rendered to an image, per the instruction to use "the
best available local method to render the PDF and Markdown/output into
image evidence" when a genuine screenshot can't be taken, and to
document plainly what can't be produced rather than fake it.

| File | What it actually is |
|---|---|
| `01_smoketest_pdf_page.png` | Real rasterization (`pymupdf` `page.get_pixmap()`) of the one-page throwaway smoke-test PDF used to exercise Docling's pipeline-init code path. **Not the benchmark fixture** — the real TC27 input (`briefing_note_BEP-BN-2026-04.pdf`) could not be retrieved (see `../observations.md`). |
| `02_error_default_ocr.png` | The tail of the real captured traceback in `../logs/pipeline_init_default_ocr.log`, rendered to an image with PIL so failure evidence exists as an image file, not only as a `.log` text file. |
| `03_error_ocr_disabled.png` | Same treatment for `../logs/pipeline_init_ocr_disabled.log`. |

## What is NOT here, and why

- **Original input PDF (real fixture)** — not retrievable in this
  sandbox (ClickUp CDN blocked, Gmail carries no attachment). No
  substitute was screenshotted in its place.
- **Markdown output** — no run completed, so there is no output to
  show.
- **Input → output comparison** — not producible without a completed
  run.
- **Table/figure-specific evidence** — not applicable; no run reached
  content extraction.

These are documented gaps, not omissions to be quietly filled with
placeholders.
