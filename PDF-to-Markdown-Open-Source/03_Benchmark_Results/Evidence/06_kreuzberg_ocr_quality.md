# Evidence: Kreuzberg — OCR quality on PDF3 (scanned research paper)

**Source:** `02_Tools/kreuzberg/markdown_output/PDF3_Scanned_Research_Paper.md`
**Config:** `ocr=OcrConfig(backend="tesseract", language="eng")`, auto-triggered (no `force_ocr` needed — Kreuzberg correctly detected the page had no text layer)

## Overall

12 pages, 27,031 characters recovered in 25.6s. Full sentences of the
abstract, body text, and "PUBLICATIONS CITED" references section are
legible and substantively correct on manual read-through.

## Two concrete misreads found

1. `Cutting strategies as contro\! measures` — should read "control
   measures"; the exclamation mark is a misread lowercase "l", and the
   literal backslash is a Markdown-escaping artifact of that misread
   character.
2. A garbled `wv"` sequence appears near a US Forest Service seal graphic
   on the last page — the seal/logo image was fed to OCR as if it were
   text and produced nonsense output instead of being recognized as a
   non-text graphic.

## What this demonstrates

Character-level OCR accuracy is high overall (no pervasive garbling), but
Kreuzberg (via Tesseract) does not distinguish "this region is a logo/seal
graphic, don't OCR it as text" — every raster region on the page is
treated as OCR-able text, producing isolated nonsense strings where a
genuine embedded graphic appears. Isolated defects, not a general
reliability problem for this document.
