# open-parse — Observations

Repo: https://github.com/Filimoa/open-parse · PyPI `openparse==0.7.0` · MIT · Python (pdfminer.six-based).

## Setup

Installation: `uv venv .venv_openparse && uv pip install openparse` (base install, **no** `[ml]` extra).
Version: 0.7.0
Dependencies: pdfminer.six, pymupdf, pypdf, tiktoken, openai (unused at runtime unless you configure an LLM-based post-processor), pillow, numpy.
GPU/CPU: CPU only; no ML model in base mode at all.
Model requirements: none for base mode. The `[ml]` extra (better table extraction via "unitable"/table-transformer) requires a separate `openparse-download` step that fetches weights from Hugging Face — **not attempted**, blocked in this sandbox, so this evaluation is explicitly of the **base, non-ML** pipeline only.
Setup difficulty: Low for the base install — but see the documented workaround below, which is a real setup gotcha not mentioned in the README.

### Documented workaround required
open-parse's base pipeline (no ML, no OCR) still makes an outbound network call: `tiktoken.get_encoding("cl100k_base")` downloads a BPE file from `openaipublic.blob.core.windows.net` purely to count tokens per parsed node (used only to decide whether a node is a tiny "stub" to discard). In this network-restricted sandbox that call fails, and worse — a naive try/download-then/except-fallback pattern re-attempts (and re-fails, with urllib3 retry/backoff) that network call **once per node**, which turned an 18-page PDF into a multi-minute hang before we fixed it. The final approach (`04_Scripts/conversion/run_openparse.py`) short-circuits `tiktoken.get_encoding` to a local length-based estimate unconditionally, which is both faster and a more honest simulation of a genuinely air-gapped/self-hosted deployment (the "local/self-hosted" requirement this whole use case is built around). **This is a real, undocumented limitation**: a library marketed as a lightweight local PDF parser has a hidden hard dependency on an OpenAI-hosted file for basic operation, with no offline/local encoding fallback shipped.

Exact invocation: `openparse.DocumentParser().parse(path, ocr=False)` (base mode; `ocr=True` would use PyMuPDF-driven OCR, explicitly marked "not recommended... slower and less accurate" by the library's own docstring, so left off).

---

## PDF 1 — Hybrid Earnings Report (Target 2015 Annual Report, 84 pages)

### Text
**Observed:** **Hard crash, zero output.** `UnidentifiedImageError('cannot identify image file <_io.BytesIO object at 0x...>')` raised from inside Pillow, invoked by open-parse's own image-node processing while walking this PDF's embedded images (this file has JPEG2000/mixed-colorspace images typical of a professionally-typeset annual report). open-parse has no fallback/try-except around this internal image-decode step, so the entire document — not just the offending image — fails to parse. No markdown, no JSON, nothing was produced for this PDF.

### Tables / Charts / Images / Reading Order / Hierarchy / Captions / OCR
N/A — no output was produced at all for this PDF (see Text above).

### Errors / Artifacts
`UnidentifiedImageError` (Pillow), uncaught, terminates the whole-document parse. Full traceback saved in `logs/PDF1_Hybrid_Earnings_Report_Target2015.log`.

---

## PDF 2 — Financial Report (Sumitomo Heavy Industries, 18 pages)

### Text
**Observed:** Ran successfully, 1.6s, 18 "nodes" produced, 37,952 characters of output — actually *more* raw characters than Kreuzberg's 33,322 on the same file, because open-parse preserves the HTML-ish `<br><br>` markers it inserts between wrapped lines (see Tables below) rather than collapsing them, inflating the character count without adding information.

### Tables
**Documentation claim:** table extraction via `table_args` (unitable/table-transformer in `[ml]` mode; base mode falls back to a simpler pdfminer-based heuristic — the maintainer's own docs call the fallback "subpar").
**Observed:** Confirms the maintainer's own "subpar" caveat directly. No node is tagged with a distinct "table" variant at all in base mode — every one of the 18 nodes is tagged `{'text', 'image'}` (checked directly against `raw_output/PDF2_Financial_Report_Sumitomo.json`), meaning open-parse's base pipeline does not structurally distinguish a table from a text block. Concretely, the "Business Results" table becomes:
> `**January 1 to March 31, 2024** **First Quarter**<br><br>**January 1 to March 31, 2024**<br><br>% change  % change <br><br>241,536  254,811  2.6  Net sales  (5.2) <br><br>11,182  18,434  14.1  Operating profit  (39.3)`
Values (`241,536`, `254,811`), the row label (`Net sales`), and the percent changes (`2.6`, `(5.2)`) are all present but **reordered relative to the source** (percent-change values appear both before and after the row, out of their true left-to-right column position) and joined with raw `<br><br>` HTML tags rather than Markdown row/column syntax. This is a clear **DEGRADED** table (data survives, but column-to-value association is actively wrong/ambiguous, not merely flattened in original order) — arguably a worse failure mode than pure omission, since a reader could misread `254,811` as belonging to the wrong period without cross-checking the source.
Also notable: the output is not valid clean Markdown — embedding literal `<br>` HTML tags inside what's presented as Markdown output is inconsistent with a "Markdown" deliverable.

### Charts
N/A — no charts in this document.

### Images
**Observed:** Images are represented as inline nodes mixed into text nodes (variant `{'text','image'}`) rather than extracted to separate files — no `extracted_images/` output exists for this tool (no dedicated image-export path was found in the base API).

### Reading Order
**Observed:** Broadly correct page-to-page order (18 nodes for 18 pages — appears to be one node per page rather than fine-grained block-level ordering), but **within** a page, table cell order is scrambled as shown above.

### Hierarchy
**Observed:** **Zero Markdown headings anywhere in the output** (`grep -c "^#"` = 0). open-parse's base mode emits bold/italic emphasis (`**text**`, `***text***`) for what looks like title-styled text, but never promotes anything to an actual `#`/`##`/`###` heading. For a use case that explicitly requires "headings and sectioning preserved as genuine markdown heading levels, not flattened to plain text," this is a full miss in base mode.

### Captions / Footnotes
**Observed:** "Note 1:", "Note:" annotations remain adjacent to their tables in the raw text stream (reading order preserved at the note-to-table level), but with the same `<br>`-joined, unstructured formatting as the rest of the document.

### OCR / Scanned Page
N/A — no scanned content in this file, and OCR was intentionally left off per the library's own recommendation.

### Errors / Artifacts
Clean run, no errors, 1.6s.

---

## PDF 3 — Scanned Research Paper (image-only, 12 pages, 0 native text layer)

### Text
**Documentation claim:** none — open-parse does not claim built-in OCR (the base pipeline has no OCR model; `ocr=True` uses a basic PyMuPDF-driven path explicitly marked "not recommended" in the library's own docstring, which we did not enable, consistent with treating this as a genuine "no-OCR" baseline).
**Observed:** **Completely empty output: 0 characters, `n_nodes: 12`** (one empty node per page, no error raised — the parse "succeeds" while returning nothing usable). This is the starkest possible OMITTED result for a scanned document: the tool ran without complaint and silently produced a 12-node, zero-content document.

### Tables / Charts / Images / Reading Order / Hierarchy / Captions
N/A — no content was extracted at all.

### OCR / Scanned Page
**Observed:** Confirmed base-mode open-parse has **no usable path for scanned/image-only PDFs whatsoever** — this rules it out entirely for this project's "mixed digital + scanned PDF handling" requirement unless paired with a separate OCR pre-processing step (which would then be a different, composite pipeline, not "open-parse" on its own).

### Errors / Artifacts
No error/exception — the silent-empty-success behavior is arguably worse than a hard failure for a production pipeline, since nothing in the tool's own output signals that OCR was needed and didn't happen.

---

## Overall

### What worked well
- Extremely fast (1.6-2.6s per document when it doesn't crash) and dependency-light for pure native-text extraction — genuinely zero ML/GPU/Hugging Face dependency in base mode (once the tiktoken workaround is applied).
- Text values from tables are not silently dropped in base mode — the numbers are present in the output, just not in structured table form.

### What failed
- **Crashed outright on the most complex benchmark PDF** (PDF1, the hybrid earnings report) with an uncaught Pillow `UnidentifiedImageError` — 0% usable output on 1 of 3 benchmark documents.
- **Zero markdown headings produced on any PDF** — no document-hierarchy support at all in base mode.
- **Zero OCR capability** — silently returns empty content on the scanned PDF rather than erroring or falling back.
- Table structure is present as raw values but column/row association is actively scrambled, and raw `<br>` HTML leaks into the "Markdown" output.

### Unexpected behaviour
- A pure local-parsing library depends on a remote OpenAI-hosted file (tiktoken's BPE data) for a completely unrelated internal token-counting heuristic — the kind of hidden network dependency that specifically undermines the "local/self-hosted" pitch this whole use case is built around, and it fails silently-slow (multi-minute hang) rather than fast, before our workaround.
- Silent, no-error, zero-content "success" on the scanned PDF is a worse failure mode than a hard crash, because nothing in the tool's return value flags that OCR was needed.

### Missing content
Entire PDF1 (crash). All heading/hierarchy structure on every PDF. All chart handling. All OCR/scanned-page content.

### Manual cleanup
Not viable as a primary tool for this use case in base mode — would need the `[ml]` extra (blocked here) at minimum for usable tables, plus an entirely separate OCR pipeline for scanned pages, plus manual heading re-insertion.

### Best use case
As shown here, this is best framed as a **lightweight baseline for simple, clean, native-digital-text PDFs with no charts, no scans, and no complex tables** — e.g., a quick text-only extraction of a plain-prose document. It is not a credible full contender for this project's stated use case (complex tables + charts + scans + hierarchy), which is exactly why it is scored as a lightweight baseline in `MASTER_RESULTS.md`, not a top contender.

### Biggest limitation
No OCR and no document-hierarchy output at all, plus an outright crash on one of the three real-world benchmark documents — three of the nine evaluation criteria (Text Preservation on scans, Document Hierarchy, Long/Complex Document Robustness) are hard failures in base mode.

### Evidence
- Markdown outputs: `markdown_output/PDF2_Financial_Report_Sumitomo.md` (PDF1 and PDF3 produced no usable markdown — see logs)
- Structured node dump: `raw_output/PDF2_Financial_Report_Sumitomo.json`, `raw_output/PDF3_Scanned_Research_Paper.json`
- Crash traceback: `logs/PDF1_Hybrid_Earnings_Report_Target2015.log`
- Run logs: `logs/*.log`
