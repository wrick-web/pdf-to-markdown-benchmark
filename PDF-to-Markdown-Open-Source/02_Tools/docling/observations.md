# Docling — Round 1 execution, Rev-2 (2026-09-03)

Task: `EXEC · Docling · PDF-OSS v1 · R1` (`86bbu4wm7`), 12 scenario/TC
lines (S27/TC27 … S38/TC38). This pass: the user manually supplied the 5
real assigned fixtures for TC27–TC31 (the ClickUp attachment CDN is still
blocked in this sandbox — see "Prior attempt" below — so this was the
only way to get the actual bytes this round). **Result: all 5 real,
tool-level executions are BLOCKED.** Docling's own model downloads
(OCR + layout) cannot complete in this sandbox regardless of which PDF
is used — this is a tool/environment blocker, not a fixture-availability
one, and it now applies with the real fixtures in hand, not just a
smoke-test file.

No ClickUp writes made. Nothing pushed to git per instruction pending
review.

## Environment (same for all 5 tests below)

- Docling version: **2.124.0** (`docling-core` 2.93.0, `docling-ibm-models`
  4.0.1, `docling-parse` 7.17.0, `torch` 2.14.0, `rapidocr` 3.9.2)
- Environment: `.venv_docling` (`uv venv` + `uv pip install docling`),
  Python 3.11.15
- Config: default `DocumentConverter()` — `StandardPdfPipeline`, no
  options overridden (OCR on, table structure on)
- Command shape (per file):
  ```python
  from docling.document_converter import DocumentConverter
  conv = DocumentConverter()
  result = conv.convert("<input.pdf>")
  print(result.document.export_to_markdown())
  ```
- Every run fails at the same point regardless of input: `_init_models()`
  tries to load the OCR model (RapidOCR/PyTorch backend), which
  downloads `PP-OCRv6_det_small.pth` from
  `https://www.modelscope.cn/models/RapidAI/RapidOCR/...` — blocked by
  this sandbox's network policy (`DownloadFileException`). Confirmed via
  source review (`docling/pipeline/standard_pdf_pipeline.py`,
  `docling/datamodel/layout_model_specs.py`) that the layout model is
  loaded unconditionally too — every layout preset Docling ships
  (Heron, Heron-101, Egret medium/large/xlarge) is Hugging-Face-hosted
  only, with no bundled/offline alternative — so a config to route
  around both blocked hosts does not exist in this version. This was
  independently re-confirmed the same day, before real fixtures arrived
  (see "Prior attempt" below) and holds identically now.

## TC27 — S27, ordinary digital text (C10)

1. **Fixture:** `briefing_note_BEP-BN-2026-04.pdf` (real, user-supplied;
   105,012 bytes, matches the ClickUp attachment's size)
2. **Scenario/TC:** S27 / TC27
3. **Tool:** Docling 2.124.0
4. **Command:** as above, run against this file, no config overrides
5. **Input characteristics:** 7 pages, 18,850 native text characters
   (confirmed via `pymupdf`). Single-column running prose, a repeated
   header/footer (org name, doc ref, page number) on every page.
   Paragraphs genuinely continue across page boundaries — page 1 ends
   "...the winter surveys" and page 2 opens "have shown so far.",
   confirmed by rendering both pages (see evidence).
6. **What the source PDF contains:** an internal briefing note —
   background, consent position, dredging programme, this winter's
   placement, financial outlook — plain paragraphs under bold section
   headings, no tables/figures/equations/code.
7. **Actual generated Markdown:** none — execution failed before any
   content was produced.
8. **What Docling preserved / lost:** not applicable — no run completed.
9. **Verdict: BLOCKED.** Real traceback:
   `logs/TC27_briefing_note_default.log` — `RapidOCR`/`rapidocr.utils.
   download_file.DownloadFileException: Failed to download
   https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/v3.9.2/
   torch/PP-OCRv6/det/PP-OCRv6_det_small.pth`. Also re-ran with
   `PdfPipelineOptions(do_ocr=False)` against this same real file to
   confirm the second (layout) blocker independently —
   `logs/TC27_briefing_note_do_ocr_false.log` — fails downloading
   `docling-project/docling-layout-heron` from Hugging Face Hub
   (`httpx.ProxyError: 403 Forbidden`).
10. **Limitations:** this is an environment/network blocker (both
    `modelscope.cn` and `huggingface.co` are unreachable from this
    sandbox), not a defect in the fixture or a capability finding about
    Docling's text handling.
11. **Evidence:** `screenshots/TC27_01_input_pages1-2.png` (real render
    of the actual source pages, `pymupdf.get_pixmap()`);
    `logs/TC27_briefing_note_default.log`,
    `logs/TC27_briefing_note_do_ocr_false.log` (real tracebacks).

## TC28 — S28, multiple columns (C11)

1. **Fixture:** `bulletin_no_212.pdf` (real, user-supplied; 146,389
   bytes, matches ClickUp)
2. **Scenario/TC:** S28 / TC28
3. **Tool:** Docling 2.124.0
4. **Command:** as above
5. **Input characteristics:** 3 pages, 12,188 native text characters.
   Visually confirmed by rendering all 3 pages: **every page is
   two-column**, and the column break genuinely splits sentences
   mid-thought (e.g. page 1: left column ends "...the coach leaves the
   Assembly", right column opens "Rooms at half past nine and is back by
   six."). This resolves the clarification flagged during fixture
   validation ("which page(s) hold the graded region") — it's all 3, not
   a single page, based on what was actually rendered this time.
6. **What the source PDF contains:** a members' society bulletin —
   lecture programme, archive notes, book review, letters, notices — in
   two newspaper-style columns per page throughout.
7. **Actual generated Markdown:** none — execution failed.
8. **What Docling preserved / lost:** not applicable — no run completed.
9. **Verdict: BLOCKED.** Same root cause as TC27, confirmed against this
   file specifically: `logs/TC28_bulletin_default.log` — identical
   `DownloadFileException` on the RapidOCR weight download. The
   do_ocr=False/layout-model failure was not re-run separately for this
   file — it was already proven file-independent by TC27's two runs
   plus the source-code review above, so repeating it here would add no
   new information (stated plainly rather than silently skipped).
10. **Limitations:** same as TC27 — environment blocker, not a finding
    about Docling's multi-column handling.
11. **Evidence:** `screenshots/TC28_01_input_page1.png`,
    `TC28_02_input_page2.png`, `TC28_03_input_page3.png` (real renders,
    all 3 pages, so the two-column layout is directly visible);
    `logs/TC28_bulletin_default.log`.

## TC29 — S29, styled headings (C12)

1. **Fixture:** `procedure_KAL-SP-06_sample_reception.pdf` (real,
   user-supplied; 128,546 bytes)
2. **Scenario/TC:** S29 / TC29
3. **Tool:** Docling 2.124.0
4. **Command:** as above
5. **Input characteristics:** 4 pages, 8,155 native text characters.
   Visually confirmed a genuine multi-level heading hierarchy: a title
   (largest, bold), section headings ("Scope", "Reception", "Storage" —
   large bold), subsection headings ("Chain of custody", "Condition on
   arrival" — smaller bold), and a fourth, italic sub-subheading level
   ("Temperature", "Container integrity"). This is a stronger, more
   specific match to TC29 than the earlier validation pass could confirm
   (that pass had no file access and called it "thematically plausible,
   lower confidence" — now directly confirmed by rendering the page).
6. **What the source PDF contains:** a laboratory SOP — sample
   reception, chain of custody, storage, retention/disposal, splitting
   submissions, complaints, training — under the heading levels above.
7. **Actual generated Markdown:** none — execution failed.
8. **What Docling preserved / lost:** not applicable — no run completed.
9. **Verdict: BLOCKED.** `logs/TC29_procedure_default.log` — identical
   `DownloadFileException`.
10. **Limitations:** environment blocker, not a finding about Docling's
    heading-level detection.

    **Byte-size discrepancy, flagged not resolved:** this file is
    128,546 bytes; a `clickup_get_task` fetch of the input task earlier
    this session reported the same-named attachment at 43,662 bytes.
    Page count (4) and content match this project's prior fixture
    validation, so this is very unlikely to be a different document —
    more likely the ClickUp attachment was updated between that fetch
    and this upload (its attachment record did carry the most recent
    `date` timestamp of all 11 files). Not silently resolved either way;
    proceeding on the user's direct, explicit instruction to use this
    file as the TC29 fixture.
11. **Evidence:** `screenshots/TC29_01_input_page1.png`,
    `TC29_02_input_page3.png` (real renders showing the heading levels);
    `logs/TC29_procedure_default.log`.

## TC30 — S30, footnotes (C12)

1. **Fixture:** `croyde_1974_braithe_order_offprint.pdf` (real,
   user-supplied; 155,308 bytes, matches ClickUp)
2. **Scenario/TC:** S30 / TC30
3. **Tool:** Docling 2.124.0
4. **Command:** as above
5. **Input characteristics:** 4 pages, 10,683 native text characters.
   Visually confirmed a genuine academic-article footnote layout: page 1
   carries 4 superscript in-text markers (¹–⁴), a horizontal rule, and
   full citation-style footnote text at the foot of the page. Journal
   header ("Estuarine Policy Review, 41.2 (2026), 143-158"), running
   page-top author/title, page numbers.
6. **What the source PDF contains:** a law-journal article on a 1974
   harbour order, single-column body text with numbered footnotes citing
   archival and case-law sources.
7. **Actual generated Markdown:** none — execution failed.
8. **What Docling preserved / lost:** not applicable — no run completed.
9. **Verdict: BLOCKED.** `logs/TC30_croyde_default.log` — identical
   `DownloadFileException`.
10. **Limitations:** environment blocker, not a finding about Docling's
    footnote handling.
11. **Evidence:** `screenshots/TC30_01_input_page1.png` (real render,
    footnote markers and footnote block both visible);
    `logs/TC30_croyde_default.log`.

## TC31 — S31, simple table (C13)

1. **Fixture:** `schedule_of_analysis_charges_2026.pdf` (real,
   user-supplied; 93,825 bytes, matches ClickUp)
2. **Scenario/TC:** S31 / TC31
3. **Tool:** Docling 2.124.0
4. **Command:** as above
5. **Input characteristics:** 3 pages, 8,578 native text characters.
   Visually confirmed: the table itself is wholly on page 1 — 4 columns
   (Determination / Method / Turnaround / Charge per sample), 8 data
   rows, no merged cells, no continuation onto page 2. Pages 2–3 are
   narrative-only ("How to submit samples", "Containers and
   preservation", proficiency scheme, confidentiality) — no additional
   table content. This directly resolves the clarification flagged
   during fixture validation ("confirm the extra 2 pages are non-table
   supporting content") — confirmed yes, based on what was actually
   rendered this time.
6. **What the source PDF contains:** a laboratory price schedule — one
   simple rate table plus surrounding policy text (submission,
   containers, turnaround terms).
7. **Actual generated Markdown:** none — execution failed.
8. **What Docling preserved / lost:** not applicable — no run completed.
9. **Verdict: BLOCKED.** `logs/TC31_schedule_default.log` — identical
   `DownloadFileException`.
10. **Limitations:** environment blocker, not a finding about Docling's
    table-structure recognition.
11. **Evidence:** `screenshots/TC31_01_input_page1.png` (real render,
    full table visible); `logs/TC31_schedule_default.log`.

## Why every one of the 5 is BLOCKED rather than scored

Docling's `StandardPdfPipeline` cannot initialize in this sandbox under
any configuration tried, independent of which PDF is supplied: the OCR
engine (RapidOCR/PyTorch) needs a weight file from `modelscope.cn`, and
the layout/object-detection model (every preset Docling ships) needs a
download from `huggingface.co`. Both hosts are unreachable here. This
was fully re-confirmed today against real fixtures, not inferred from
the earlier smoke test. No score, capability judgement, or Cycle-I
comparison is recorded for TC27–TC31 — there is no Docling output to
judge.

## Prior attempt (same day, before real fixtures arrived) — fixture retrieval was ALSO blocked

Before the user manually supplied the 5 real PDFs above, this project
tried repeatedly to retrieve the 11-PDF set from ClickUp/Gmail directly,
and could not:

1. `86bbr4dmu`'s attachment CDN (`t9014651757.p.clickup-attachments.com`)
   returned 403 on every attempt, including a freshly issued
   `clickup_download_task_attachment` signed URL fetched and `curl`'d
   immediately — confirmed via the egress proxy's own status log as an
   organization-policy denial, not an expired-URL problem.
2. Gmail carries no path to the bytes either — searched directly for all
   11 filenames and for messages from Pruthviraj/Haresh with an
   attachment; zero results.
3. A one-line throwaway smoke-test PDF (`smoketest.pdf`, built locally
   via `pymupdf`, clearly labeled as not a fixture) was used only to
   confirm Docling's own model-download blocker exists independent of
   fixture access — both failure modes (`logs/pipeline_init_default_
   ocr.log`, `logs/pipeline_init_ocr_disabled.log`) were captured this
   way before real fixtures existed.

This history is kept for the record; TC27–TC31 above supersede it now
that real fixtures are in hand — the conclusion (BLOCKED, tool-level) is
unchanged, but now proven against the actual assigned inputs rather than
a substitute.

## Not done, and why

- TC32–TC38 (7 of 12): not attempted — no fixture supplied for these yet
  this round, and the same tool-level blocker would apply regardless.
- No new screenshots are text-to-image renderings this round, per
  instruction — every image under `screenshots/TC2{7,8,9}*` and
  `TC3{0,1}*` is a genuine `pymupdf` rasterization of the real source
  PDF page(s). (The two text-to-image error renders from the prior,
  smoke-test-only attempt — `screenshots/02_error_default_ocr.png`,
  `03_error_ocr_disabled.png` — remain from that earlier, clearly
  separate attempt and were not recreated this round.)

## What would unblock this

Unchanged from the prior attempt: Docling needs to run somewhere that
can reach `modelscope.cn` and `huggingface.co` (or with its OCR/layout
models pre-downloaded and pointed at via `--artifacts-path`/
`artifacts_path`, which this sandbox cannot populate either, for the
same reason). Fixture access is no longer the blocker for TC27–TC31 —
the tool itself is.
