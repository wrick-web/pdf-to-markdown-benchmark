# Docling — Round 1 execution attempt, Rev-2 (2026-09-03)

**Result: BLOCKED. No TC produced a completed run.** Task:
`EXEC · Docling · PDF-OSS v1 · R1` (`86bbu4wm7`), 12 scenario/TC lines
(S27/TC27 through S38/TC38). Attempted TC27 first per the fixture table;
the same two blockers apply to all 12, so the other 11 were not
separately attempted.

## What was actually done

1. Confirmed `86bbu4wm7` is the only Round 1 subject with populated
   scenario/TC lines (the other 5 — doc2mark, GPT-5.6 terra, LiteParse,
   MarkItDown, PyMuPDF4LLM — have 0 subtasks each).
2. Tried to obtain the assigned TC27 fixture,
   `briefing_note_BEP-BN-2026-04.pdf`, from ClickUp task `86bbr4dmu`.
   Blocked: the attachment CDN
   (`t9014651757.p.clickup-attachments.com`) returns 403 from this
   sandbox, confirmed both by a direct curl and by
   `clickup_download_task_attachment`'s signed URL (same 403 — a
   host-level network block, not a signing problem).
3. Checked whether the PDF bytes might be reachable via Gmail instead.
   Opened a ClickUp notification email for this task in full: it is a
   link-back HTML template with no attachments. Ruled out.
4. Installed Docling (`docling==2.124.0`) via `uv venv .venv_docling` +
   `uv pip install docling`. Installed cleanly — see `setup/INSTALL.md`.
5. Built a one-line throwaway PDF (`smoketest.pdf`, via `pymupdf`) purely
   to see how far Docling's pipeline gets before failing, since the real
   fixture wasn't available. Labeled everywhere as a smoke test, never
   used as a stand-in benchmark result.
6. Ran `DocumentConverter().convert()` (default pipeline) against
   `smoketest.pdf`. Failed: RapidOCR tries to download
   `PP-OCRv6_det_small.pth` from
   `https://www.modelscope.cn/models/RapidAI/RapidOCR/...`, which this
   sandbox's network policy blocks. Full traceback:
   `logs/pipeline_init_default_ocr.log`.
7. Retried with `PdfPipelineOptions(do_ocr=False)`. Still failed —
   Docling's layout model (`docling-project/docling-layout-heron`) is
   loaded regardless of the OCR setting, and its download from the
   Hugging Face Hub also hits a blocked host
   (`httpx.ProxyError: 403 Forbidden`). Full traceback:
   `logs/pipeline_init_ocr_disabled.log`.

## Why this is reported as blocked rather than skipped

Two independent network blocks compound here: the fixture itself
couldn't be retrieved, and separately, Docling's own runtime model
downloads (OCR + layout) can't complete in this sandbox under any
pipeline configuration tried. Neither blocker is a workaround-able
config choice on Docling's side — layout is not optional in
`StandardPdfPipeline`, and no offline/cached model path was available.

## Evidence

- `logs/pipeline_init_default_ocr.log` — real captured traceback, default
  pipeline, OCR enabled.
- `logs/pipeline_init_ocr_disabled.log` — real captured traceback,
  `do_ocr=False`, layout model download.
- `screenshots/01_smoketest_pdf_page.png` — real rasterization
  (`pymupdf` `get_pixmap()`) of the smoke-test PDF's single page, labeled
  as not a benchmark fixture.
- `screenshots/02_error_default_ocr.png`,
  `screenshots/03_error_ocr_disabled.png` — the tail of each real log
  rendered to an image file, so image evidence of the actual failures
  exists. Both are explicitly labeled as text-to-image renderings, not
  screen captures — this sandbox has no GUI/browser to capture from. See
  `screenshots/README.md`.
- `input/` is empty — the assigned fixture could not be retrieved and
  nothing was substituted into it.
- `raw_output/`, `markdown_output/` are empty — no run produced output.
- `setup/INSTALL.md` — exact install commands and installed versions.
- `scripts/run_docling.py` — ready to run once a fixture and model
  access exist; not yet executed successfully against a real fixture.

## Not done, and why

- TC28–TC38 were not separately attempted: both blockers (fixture
  retrieval, model download) apply identically regardless of which of
  the 11 PDFs is targeted, so repeating the attempt 11 more times would
  reproduce the same two errors without new information.
- No score, rating, or capability judgement is recorded for Docling
  here — there is no output to judge. This is a blocked-execution report,
  not a tool evaluation.

## What would unblock this

- Someone with unrestricted network access supplying the 11 PDF fixture
  bytes directly into this environment (as was done for the original
  3-PDF set earlier in this project), and/or
- Running `scripts/run_docling.py` on a machine that can reach
  `modelscope.cn` and `huggingface.co` (or with Docling's models
  pre-downloaded/cached locally), and/or
- An offline/local model path for Docling's OCR and layout models, if
  one exists and can be supplied into this sandbox via an allowed
  registry (PyPI/npm/GitHub) instead of modelscope.cn/huggingface.co.
