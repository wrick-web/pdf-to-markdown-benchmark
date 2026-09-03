# Docling — Round 1 execution, Rev-2 (2026-09-03)

Task: `EXEC · Docling · PDF-OSS v1 · R1` (`86bbu4wm7`), 12 scenario/TC
lines (S27/TC27 … S38/TC38). **Result: 0/12 completed a run.** TC27–TC31
were actually executed against real, user-supplied fixtures and are
BLOCKED at the tool level. TC32–TC38 additionally have no fixture
available this round. **Update (same day, second pass):** built the OCR
path from scratch to genuinely work with zero network calls (see
"Environment build, second pass" below) — this narrows the blocker from
"two model downloads fail" to "exactly one, the layout model, fails,"
confirmed with fresh per-file evidence for all 5 real fixtures. Still
0/12 completed, because layout is not optional in Docling's real
pipeline and has no non-HF source anywhere this sandbox can reach — but
this is now a precisely isolated, exhaustively checked finding, not an
assumption.

## Environment (first pass — superseded by the OCR fix below, kept for the record)

- Docling version: **2.124.0** (`docling-core` 2.93.0, `docling-ibm-models`
  4.0.1, `docling-parse` 7.17.0, `torch` 2.14.0, `rapidocr` 3.9.2)
- Environment: `.venv_docling` (`uv venv` + `uv pip install docling`),
  Python 3.11.15
- Command shape:
  ```python
  from docling.document_converter import DocumentConverter
  conv = DocumentConverter()
  result = conv.convert("<input.pdf>")
  print(result.document.export_to_markdown())
  ```
- Failure point: `_init_models()` tries to load the OCR engine
  (RapidOCR/**PyTorch** backend by default), which downloads
  `PP-OCRv6_det_small.pth` from `https://www.modelscope.cn/models/
  RapidAI/RapidOCR/...` — blocked. With `do_ocr=False`, the failure
  moves to the layout/object-detection model instead — every layout
  preset Docling ships (Heron, Heron-101, Egret medium/large/xlarge,
  confirmed via `docling/datamodel/layout_model_specs.py`) is
  Hugging-Face-hosted only, so that fails too (`httpx.ProxyError: 403
  Forbidden`). No configuration in the first-pass setup avoided both.

## Environment build, second pass — OCR solved, layout exhaustively confirmed unavailable

Per instruction to build the minimum viable environment myself rather
than stop at the first blocker, dug into *why* the OCR download was
required at all, rather than accepting it as fixed.

**Found:** the `rapidocr` PyPI wheel (already installed, from PyPI —
which works fine here) bundles ONNX copies of the exact same models
directly in the package:
```
.venv_docling/lib/python3.11/site-packages/rapidocr/models/
├── ch_ppocr_mobile_v2.0_cls_mobile.onnx
├── PP-OCRv6_det_small.onnx
└── PP-OCRv6_rec_small.onnx
```
Docling's own `RapidOcrOptions` already defaults `backend` to
`'onnxruntime'` — it just wasn't taking effect because the `onnxruntime`
Python package wasn't installed (a one-line PyPI install, `uv pip
install onnxruntime`, no model download). With that installed and
`ocr_options=RapidOcrOptions(backend="onnxruntime")` passed explicitly,
**OCR now works with zero network calls** — verified against all 5 real
TC27–TC31 fixtures (`logs/TC2{7,8,9}_*_ocr_fixed_*.log`,
`logs/TC3{0,1}_*_ocr_fixed_*.log`): each one now gets measurably
further, past OCR entirely, and fails specifically and only at
`huggingface_hub.snapshot_download` for the layout model
(`ProxyError('403 Forbidden')`).

**Then checked, exhaustively, whether layout has any equivalent
workaround** — not assumed, checked:
1. Every layout preset in `docling/datamodel/layout_model_specs.py`
   (Heron, Heron-101, Egret medium/large/xlarge) is HF-hosted only.
2. No installed package (`docling`, `docling-core`,
   `docling-ibm-models`, `docling-parse`, `docling-slim`) bundles any
   layout weight file — only RapidOCR's 3 OCR files exist anywhere.
   `docling-ibm-models` ships `tableformer` (table structure) only, no
   layout module.
3. `https://pypi.org/pypi/docling-layout-heron/json` → 404. Not on
   PyPI.
4. Checked for a GitHub mirror via `raw.githubusercontent.com` (which
   is genuinely reachable from this sandbox — confirmed by fetching
   Docling's real public README successfully) under both
   `docling-project/` and `DS4SD/` (IBM's original org) — all 404, real
   "doesn't exist" responses, not proxy blocks.
5. `huggingface.co` itself: blocked (`403 Forbidden`).
6. `hf-mirror.com` (a different domain entirely, a known third-party HF
   mirror): also blocked (`connect_rejected`) — this confirms the
   sandbox enforces an **allowlist** of approved registries, not a
   blocklist of specific bad hostnames, so no untried mirror is likely
   to work either.

Full writeup: `setup/INSTALL.md`. **Conclusion: layout has exactly one
source (Hugging Face Hub), and this sandbox cannot reach it through any
channel — bundled, PyPI, or GitHub — that it can reach anything else
through.** This was not left as an assumption from the first pass; it
was re-derived and checked from first principles this pass.

Per the instruction not to weaken the benchmark by disabling a
capability a scenario is testing: layout was **not** bypassed or
monkey-patched around. It underlies reading order, headings, tables,
and figures — i.e. most of what S27–S38 actually test — so forcing a
degraded run without it would not be Docling's real output, and every
verdict below stays BLOCKED rather than a fabricated PASS on a hacked
pipeline.

## Best-known working configuration (used for every TC27–TC31 re-run below)

```python
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, RapidOcrOptions
from docling.datamodel.base_models import InputFormat

opts = PdfPipelineOptions()
opts.ocr_options = RapidOcrOptions(backend="onnxruntime")
conv = DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)})
result = conv.convert("<input.pdf>")
```
This is `scripts/run_docling.py`'s current default. Table structure and
everything else stays at Docling's real defaults — nothing scenario-relevant
was disabled to get this far.

---

# TC27 — An ordinary digital text document

## Input
- PDF: `briefing_note_BEP-BN-2026-04.pdf` (105,012 bytes — real, user-supplied)
- Pages: 7 (18,850 native text characters)
- Scenario: S27 (`86bbu4wn7`)
- Capability: C10 Text Fidelity

## Execution
- Docling version: 2.124.0
- Environment: `.venv_docling`; 3 configs tried — default, `do_ocr=False`, and the OCR-fixed config (`RapidOcrOptions(backend="onnxruntime")` + `onnxruntime` installed)
- Command/configuration: see "best-known working configuration" above

## Expected
All text is present and unchanged — nothing missing, garbled, or invented (frozen TC27 spec).

## Observed
Pipeline construction fails before any page is processed, in all 3 configs. Default fails downloading RapidOCR's PyTorch weights; `do_ocr=False` fails downloading the layout model instead. With the OCR fix applied, OCR succeeds (bundled ONNX weights, zero downloads, confirmed via log line "File exists and is valid") and the run gets measurably further — but then fails at the same layout-model download. No Markdown was produced under any config.

## Output
None — no Markdown file exists for this run.

## Evidence
- `screenshots/TC27_01_input_pages1-2.png` — real render of source pages 1–2
- `logs/TC27_briefing_note_default.log`, `logs/TC27_briefing_note_do_ocr_false.log` — real tracebacks, first pass
- `logs/TC27_briefing_note_ocr_fixed_still_blocked_layout.log`, `logs/TC27_briefing_note_ocr_fixed_layout_blocked_summary.log` — real tracebacks, OCR-fixed config, confirming OCR now passes and only layout remains blocked

## Observation
Never got far enough to say anything about Docling's actual text handling here. The source itself is a clean, single-column briefing note where paragraphs genuinely continue across page breaks (page 1 ends "...the winter surveys", page 2 opens "have shown so far.") — a fair C10 fixture, just untested.

## Verdict
BLOCKED

## Notes
Same root cause as every TC below — see the environment section. Not scored; no output to judge.

---

# TC28 — A page laid out in multiple columns

## Input
- PDF: `bulletin_no_212.pdf` (146,389 bytes — real, user-supplied)
- Pages: 3 (12,188 native text characters)
- Scenario: S28 (`86bbu4wpw`)
- Capability: C11 Reading Order & Layout

## Execution
- Docling version: 2.124.0
- Environment: `.venv_docling`; default config, then the OCR-fixed config
- Command/configuration: see "best-known working configuration" above

## Expected
Text is emitted in the natural reading order without interleaving the columns (frozen TC28 spec).

## Observed
Default config fails downloading RapidOCR's weights. With the OCR fix applied, OCR succeeds and the run gets further, then fails at the same layout-model download every other TC hits. No Markdown produced either way.

## Output
None.

## Evidence
- `screenshots/TC28_01_input_page1.png`, `TC28_02_input_page2.png`, `TC28_03_input_page3.png` — real renders, all 3 pages
- `logs/TC28_bulletin_default.log`, `logs/TC28_bulletin_ocr_fixed_layout_blocked.log`

## Observation
Confirmed by rendering all 3 pages: every page is two-column, and the column break genuinely splits sentences mid-thought (e.g. page 1: "...the coach leaves the Assembly" / "Rooms at half past nine..."). This resolves the earlier fixture-validation question about which page(s) are graded — it's all three. Untested against Docling itself.

## Verdict
BLOCKED

## Notes
—

---

# TC29 — A document with styled headings and subheadings

## Input
- PDF: `procedure_KAL-SP-06_sample_reception.pdf` (128,546 bytes as supplied)
- Pages: 4 (8,155 native text characters)
- Scenario: S29 (`86bbu4wrn`)
- Capability: C12 Heading & Section Structure

## Execution
- Docling version: 2.124.0
- Environment: `.venv_docling`; default config, then the OCR-fixed config
- Command/configuration: see "best-known working configuration" above

## Expected
Headings become Markdown headings with hierarchy preserved — not plain or bold text (frozen TC29 spec).

## Observed
Default config fails downloading RapidOCR's weights. OCR-fixed config gets past OCR, then fails at the same layout-model download. No Markdown produced either way.

## Output
None.

## Evidence
- `screenshots/TC29_01_input_page1.png`, `TC29_02_input_page3.png`
- `logs/TC29_procedure_default.log`, `logs/TC29_procedure_ocr_fixed_layout_blocked.log`

## Observation
Confirmed a genuine 4-level heading hierarchy by rendering page 1: document title, section headings ("Scope", "Reception", "Storage"), subsection headings ("Chain of custody", "Condition on arrival"), and an italic sub-subheading level ("Temperature", "Container integrity"). Untested against Docling itself.

## Verdict
BLOCKED

## Notes
Flagged, not resolved: this file is 128,546 bytes; the same-named ClickUp attachment was recorded at 43,662 bytes earlier this session. Page count (4) and content match this project's prior fixture validation, so this reads as a ClickUp-side update between fetches rather than a different document — proceeding on the user's direct instruction to use this file.

---

# TC30 — Footnotes at the bottom of the page

## Input
- PDF: `croyde_1974_braithe_order_offprint.pdf` (155,308 bytes)
- Pages: 4 (10,683 native text characters)
- Scenario: S30 (`86bbu4wua`)
- Capability: C12 Heading & Section Structure

## Execution
- Docling version: 2.124.0
- Environment: `.venv_docling`; default config, then the OCR-fixed config
- Command/configuration: see "best-known working configuration" above

## Expected
The footnote text is kept out of the body flow, present, and associated with its reference (frozen TC30 spec).

## Observed
Default config fails downloading RapidOCR's weights. OCR-fixed config gets past OCR, then fails at the same layout-model download. No Markdown produced either way.

## Output
None.

## Evidence
- `screenshots/TC30_01_input_page1.png`
- `logs/TC30_croyde_default.log`, `logs/TC30_croyde_ocr_fixed_layout_blocked.log`

## Observation
Source is a genuine law-journal article layout: 4 superscript in-text markers on page 1, a horizontal rule, and full citation text at the foot of the page. Untested against Docling itself.

## Verdict
BLOCKED

## Notes
—

---

# TC31 — A simple, clearly formatted table

## Input
- PDF: `schedule_of_analysis_charges_2026.pdf` (93,825 bytes)
- Pages: 3 (8,578 native text characters)
- Scenario: S31 (`86bbu4ww2`)
- Capability: C13 Table Extraction

## Execution
- Docling version: 2.124.0
- Environment: `.venv_docling`; default config, then the OCR-fixed config
- Command/configuration: see "best-known working configuration" above

## Expected
The table is retained as a table with correct headers, rows, columns and values (frozen TC31 spec).

## Observed
Default config fails downloading RapidOCR's weights. OCR-fixed config gets past OCR, then fails at the same layout-model download. No Markdown produced either way.

## Output
None.

## Evidence
- `screenshots/TC31_01_input_page1.png`
- `logs/TC31_schedule_default.log`, `logs/TC31_schedule_ocr_fixed_layout_blocked.log`

## Observation
Confirmed by rendering: the table (4 columns, 8 rows, no merged cells) is wholly on page 1; pages 2–3 are narrative-only policy text (submission, containers, turnaround terms), not additional table content. Resolves the earlier fixture-validation question about the extra page count. Untested against Docling itself.

## Verdict
BLOCKED

## Notes
—

---

# TC32 — A table that continues across a page break

## Input
- PDF: `monitoring_station_schedule_2026.pdf` — **not retrieved this round**
- Pages: unknown (not opened)
- Scenario: S32 (`86bbu4wy1`)
- Capability: C13 Table Extraction

## Execution
- Docling version: 2.124.0 (installed; not invoked for this TC)
- Environment: `.venv_docling`
- Command/configuration: n/a — no input

## Expected
The complete table is retained with correct headers, rows, columns and values (frozen TC32 spec).

## Observed
Fixture not obtained. Fresh attempt today: requested a signed download URL from the input task (`86bbr4dmu`) and `curl`'d it immediately — `connect_rejected`/403 at the organization-policy level, identical to every other attempt this session against this CDN.

## Output
None.

## Evidence
- none producible — no source render, no run

## Observation
Not attempted, for lack of input — not guessed, not substituted. Independently, TC27–31 already proved Docling's layout model (the one remaining blocker after the OCR fix) can't load in this sandbox regardless of which PDF is supplied, so this would be BLOCKED either way.

## Verdict
BLOCKED

## Notes
Would need either (a) the file supplied directly into this session, as was done for TC27–31, or (b) Docling's model-download blocker resolved.

---

# TC33 — A document with figures and captions

## Input
- PDF: `intertidal_survey_BEP-SR-2026-11.pdf`, page 2 — **not retrieved this round**
- Pages: unknown (not opened)
- Scenario: S33 (`86bbu4wzj`)
- Capability: C14 Figures & Charts

## Execution
- Docling version: 2.124.0 (installed; not invoked)
- Environment: `.venv_docling`
- Command/configuration: n/a — no input

## Expected
The image is preserved (embedded or referenced) at its position, with its caption (frozen TC33 spec).

## Observed
Fixture not obtained — same ClickUp CDN block as TC32.

## Output
None.

## Evidence
- none producible

## Observation
Not attempted, for lack of input. Same tool-level blocker as TC27–31 would apply regardless — OCR is now solved (bundled ONNX weights), but the layout model (exhaustively confirmed as HF-only, no bundled/PyPI/GitHub alternative) would still block it.

## Verdict
BLOCKED

## Notes
Same file as TC34 (different page) — a single retrieval would unblock both.

---

# TC34 — A document with a data chart

## Input
- PDF: `intertidal_survey_BEP-SR-2026-11.pdf`, page 3 — **not retrieved this round**
- Pages: unknown (not opened)
- Scenario: S34 (`86bbu4x1h`)
- Capability: C14 Figures & Charts

## Execution
- Docling version: 2.124.0 (installed; not invoked)
- Environment: `.venv_docling`
- Command/configuration: n/a — no input

## Expected
The chart is preserved as an image at its position with its title (frozen TC34 spec).

## Observed
Fixture not obtained — same ClickUp CDN block as TC32/33.

## Output
None.

## Evidence
- none producible

## Observation
Not attempted, for lack of input. Same tool-level blocker as TC27–31 would apply regardless — OCR is now solved (bundled ONNX weights), but the layout model (exhaustively confirmed as HF-only, no bundled/PyPI/GitHub alternative) would still block it.

## Verdict
BLOCKED

## Notes
Same file as TC33 (different page).

---

# TC35 — A cleanly scanned document

## Input
- PDF: `certificate_of_analysis_KAL-11938.pdf` — **not retrieved this round**
- Pages: unknown (not opened)
- Scenario: S35 (`86bbu4x2t`)
- Capability: C15 Scanned Document OCR

## Execution
- Docling version: 2.124.0 (installed; not invoked)
- Environment: `.venv_docling`
- Command/configuration: n/a — no input

## Expected
Visible text is recovered accurately (frozen TC35 spec).

## Observed
Fixture not obtained — same ClickUp CDN block.

## Output
None.

## Evidence
- none producible

## Observation
Not attempted, for lack of input. **Correction from the ClickUp comment posted earlier today**: OCR itself is no longer blocked (see "Environment build, second pass" above — RapidOCR's bundled ONNX weights work with zero downloads). This scenario would still be BLOCKED, but by the layout model, same as every other TC, not by OCR specifically.

## Verdict
BLOCKED

## Notes
—

---

# TC36 — A document mixing digital and scanned pages

## Input
- PDF: `service_report_KAL-ESR-4471.pdf` — **not retrieved this round**
- Pages: unknown (not opened)
- Scenario: S36 (`86bbu4x43`)
- Capability: C15 Scanned Document OCR

## Execution
- Docling version: 2.124.0 (installed; not invoked)
- Environment: `.venv_docling`
- Command/configuration: n/a — no input

## Expected
The scanned page's text appears in the output like the digital pages — not silently skipped (frozen TC36 spec).

## Observed
Fixture not obtained — same ClickUp CDN block.

## Output
None.

## Evidence
- none producible

## Observation
Not attempted, for lack of input. **Correction from the ClickUp comment posted earlier today**: OCR itself is no longer blocked (bundled ONNX weights work with zero downloads). This scenario would still be BLOCKED, but by the layout model, same as every other TC, not by OCR specifically.

## Verdict
BLOCKED

## Notes
—

---

# TC37 — A document containing mathematical equations

## Input
- PDF: `technical_note_TIH-TN-18.pdf` — **not retrieved this round**
- Pages: unknown (not opened)
- Scenario: S37 (`86bbu4x9a`)
- Capability: C16 Equations & Mathematical Notation

## Execution
- Docling version: 2.124.0 (installed; not invoked)
- Environment: `.venv_docling`
- Command/configuration: n/a — no input

## Expected
Equations are emitted as math markup (LaTeX/MathML) or an honest fallback — not garbled prose (frozen TC37 spec).

## Observed
Fixture not obtained — same ClickUp CDN block.

## Output
None.

## Evidence
- none producible

## Observation
Not attempted, for lack of input. Same tool-level blocker as TC27–31 would apply regardless — OCR is now solved (bundled ONNX weights), but the layout model (exhaustively confirmed as HF-only, no bundled/PyPI/GitHub alternative) would still block it.

## Verdict
BLOCKED

## Notes
—

---

# TC38 — A document containing a code block

## Input
- PDF: `operations_note_DS-OP-07.pdf` — **not retrieved this round**
- Pages: unknown (not opened)
- Scenario: S38 (`86bbu4xb7`)
- Capability: C17 Code Extraction

## Execution
- Docling version: 2.124.0 (installed; not invoked)
- Environment: `.venv_docling`
- Command/configuration: n/a — no input

## Expected
The code is emitted as a preformatted/fenced block with line breaks and indentation intact (frozen TC38 spec).

## Observed
Fixture not obtained — same ClickUp CDN block.

## Output
None.

## Evidence
- none producible

## Observation
Not attempted, for lack of input. Also still open from the earlier fixture-validation pass on this line: which of the fixture's 3 monospace blocks is the graded one isn't confirmed here either way, since nothing was run.

## Verdict
BLOCKED

## Notes
—

---

## Prior attempt (same day, before real fixtures arrived for TC27–31)

Before the user manually supplied the 5 real PDFs for TC27–31, this
project tried repeatedly to retrieve the full 11-PDF set from
ClickUp/Gmail directly, and could not — the attachment CDN
(`t9014651757.p.clickup-attachments.com`) returned 403 on every attempt,
including freshly issued signed URLs, and Gmail carries no attachment
path either. A one-line throwaway smoke-test PDF (`smoketest.pdf`,
clearly labeled as not a fixture) was used only to confirm Docling's
own model-download blocker exists independent of fixture access —
`logs/pipeline_init_default_ocr.log`, `logs/pipeline_init_ocr_disabled.log`.
Kept for the record; TC27–TC38 above supersede it.

## What would unblock the remaining 7 (TC32–TC38), and the other 5's real output

OCR is solved — it no longer needs anything external. The single
remaining blocker for all 12 TCs is the layout model. To fully unblock:

1. The 6 remaining PDFs (`monitoring_station_schedule_2026.pdf`,
   `intertidal_survey_BEP-SR-2026-11.pdf`,
   `certificate_of_analysis_KAL-11938.pdf`,
   `service_report_KAL-ESR-4471.pdf`, `technical_note_TIH-TN-18.pdf`,
   `operations_note_DS-OP-07.pdf`) supplied directly into this session,
   the same way TC27–31's fixtures were — needed for TC32–38 only,
   **and**
2. The layout model (`docling-project/docling-layout-heron` or any
   sibling preset) made reachable — either this environment gets
   Hugging Face Hub access, or someone with real internet access runs
   `docling-tools models download --output-dir /models` (or lets
   Docling run once normally) elsewhere and supplies the resulting
   model directory into this session, so `PdfPipelineOptions.
   artifacts_path` can point at it directly with no download at all.
   Needed for all 12 TCs, including the 5 whose fixtures are already in
   hand.

(2) alone would already unblock real output for TC27–31 — their
fixtures are already here.
