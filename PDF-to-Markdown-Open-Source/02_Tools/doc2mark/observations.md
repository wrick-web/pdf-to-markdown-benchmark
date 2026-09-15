# doc2mark — Round 1 execution, TC27–TC32/TC115 only (2026-09-15)

Task: `EXEC · doc2mark · PDF-OSS v1 · R1` (`86bbu4wke`). This pass is scoped
strictly to the first 6 scenarios/7 test-case lines (S27–S32, TC27–TC32, plus
TC115 which rides alongside TC32 under S32). **TC33–TC38 and their scenarios
were not touched in this pass.**

Verdicts use only **PASS / FAIL / CAN NOT BE GRADED** — no BLOCKED/PARTIAL.
Full per-TC write-ups are posted directly on each TC observation subtask
under `86bbu4wke`; this file is the local mirror plus the summary table.

## Environment

- doc2mark version: **0.6.1** (PyPI `doc2mark`, github.com/luisleo526/doc2mark,
  author Hao Liang Wen)
- Environment: `.venv_doc2mark` (`python3 -m venv` + `pip install doc2mark`),
  Python 3.11.15, Linux 6.18.44-fc-v33
- Command shape (`scripts/run_doc2mark.py`):
  ```python
  from doc2mark import UnifiedDocumentLoader
  loader = UnifiedDocumentLoader(ocr_provider=None)
  result = loader.load("<input.pdf>", extract_images=False, ocr_images=False, show_progress=False)
  print(result.markdown)
  ```
- `ocr_provider=None` explicitly: doc2mark's default OCR path (`ocr_provider="openai"`)
  calls an external OpenAI API and requires an API key, which is out of scope for this
  open-source benchmark. None of TC27–TC32 need OCR/image interpretation, and the
  loader instantiates and runs cleanly with no API key when `ocr_provider=None`.
- No model download of any kind — pure PyMuPDF-based extraction. All 5 reachable
  fixtures ran cleanly and quickly (0.79s–1.13s each).

## Input PDF mapping (verified fresh against `86bbr4dmu`, not assumed from prior tools)

| Scenario | TC | Capability | Fixture |
|---|---|---|---|
| S27 (`86bbxakqt`) | TC27 (`86bbxartp`) | C10 Text Fidelity | briefing_note_BEP-BN-2026-04.pdf |
| S28 (`86bbxaru6`) | TC28 (`86bbxaruq`) | C11 Reading Order & Layout | bulletin_no_212.pdf |
| S29 (`86bbxarva`) | TC29 (`86bbxarvz`) | C12 Heading & Section Structure | procedure_KAL-SP-06_sample_reception.pdf (43,662-byte canonical fixture) |
| S30 (`86bbxarwp`) | TC30 (`86bbxarxj`) | C12 Heading & Section Structure | croyde_1974_braithe_order_offprint.pdf |
| S31 (`86bbxary1`) | TC31 (`86bbxaryz`) | C13 Table Extraction | schedule_of_analysis_charges_2026.pdf |
| S32 (`86bbxarzz`) | TC32 (`86bbxat0u`) / TC115 (`86bbxat1f`) | C13 Table Extraction | monitoring_station_schedule_2026.pdf |

## Summary

| TC | Capability | Fixture | Verdict |
|---|---|---|---|
| TC27 | C10 Text Fidelity | briefing_note_BEP-BN-2026-04.pdf | PASS |
| TC28 | C11 Reading Order & Layout | bulletin_no_212.pdf | FAIL |
| TC29 | C12 Heading & Section Structure | procedure_KAL-SP-06_sample_reception.pdf (43,662-byte fixture) | FAIL |
| TC30 | C12 Heading & Section Structure | croyde_1974_braithe_order_offprint.pdf | FAIL |
| TC31 | C13 Table Extraction | schedule_of_analysis_charges_2026.pdf | FAIL |
| TC32 / TC115 | C13 Table Extraction | monitoring_station_schedule_2026.pdf | CAN NOT BE GRADED (fixture unreachable) |

**PASS: 1 · FAIL: 4 · CAN NOT BE GRADED: 1** (of 6 TCs tested this pass; TC115 shares TC32's verdict/evidence)

## Key findings (detail on each TC subtask in ClickUp)

- **TC27 (PASS):** full text present; character/word counts match a raw
  PyMuPDF extraction of the same PDF almost exactly (3,173 words in the
  Markdown vs. 3,192 raw — the ~0.6% difference is page-footer/`<!-- page N -->`
  marker bookkeeping, not lost content). Page breaks are marked cleanly with
  `<!-- page N -->` HTML comments and standalone `Page N of 7` footer lines;
  no header/footer text is fused into body sentences at any of the 7 page
  breaks (contrast with MarkItDown's confirmed inline fusions on this same
  capability/fixture in the prior round).
- **TC28 (FAIL):** genuine, severe reading-order corruption confirmed against
  the source PDF's own column bounding boxes (via PyMuPDF block coordinates).
  Three concrete, quotable displaced fragments:
  1. Page 1: the sentence-continuation "Rooms at half past nine and is back
     by six." (true right-column top, `x0=307,y0=116`, the direct
     continuation of "The coach leaves the Assembly" at the end of the left
     column) is placed at line 7 of the output — before "Spring lecture
     programme" (line 12), i.e. before the left column's own content even
     starts.
  2. Page 2: "the argument are worth reading. The board's engineer wanted a
     channel of fourteen feet..." (true right-column top, continuing "...and
     the papers of" from the very bottom of the left column) is placed at
     output line 113 — 92 lines before its own logical predecessor, which
     doesn't appear until output line 205–208 ("The estuary in 1926...and
     the papers of").
  3. Page 3: "asked to check their entries before then." (true right-column
     top, continuing "...and the members who took part are" from the bottom
     of the left column) is placed at output line 221 — appearing before its
     own logical predecessor, which doesn't appear until output line 300–302.
- **TC29 (FAIL):** doc2mark does produce real Markdown heading syntax here
  (unlike MarkItDown, which fully flattened this same fixture), but the
  hierarchy is objectively wrong. Verified against the source PDF's own font
  sizes (via PyMuPDF span metadata): all 15 top-level section headers
  ("Scope", "Reception", "Storage", "Retention and disposal", "Records",
  "Responsibilities", "Identification and booking in", "Storage capacity",
  "Weekly clearance", "Transport boxes and returns", "Out-of-hours
  deliveries", "Deviations", "Complaints", "Training", "Revision history")
  are identically 16pt in the source — the same single heading level
  throughout. doc2mark renders the 4 that fall on page 1 as `#` (H1) and the
  11 that fall on page 2 onward as `##` (H2) — an inconsistency driven by
  page position, not by the document's actual structure. In addition, the
  real second- and third-level subsection headers (13pt: "Chain of custody",
  "Condition on arrival", "Refrigerated storage", "Frozen storage",
  "Reception staff", "The duty chemist", "The laboratory number", "Splitting
  a submission", "Sub-samples for microbiology"; 12pt: "Temperature",
  "Container integrity") are not marked as headings anywhere — they appear as
  plain paragraph-opening text indistinguishable from body content.
- **TC30 (FAIL):** two footnotes present and verifiable in the source PDF —
  footnote 9 ("Notably Prosser, 'Consent and its conditions', 7, who calls
  the deletion 'tidying'.") and footnote 10 ("Minutes of the fourth meeting,
  9 July 1973 (Braithe Record Office, BHB/3/19), 2-6.") — are completely
  absent from the generated Markdown, even though their inline reference
  markers ("a formality. 9", "at length.10") do survive in the body text.
  Confirmed by grepping the output for both footnotes' distinctive text
  (`Notably Prosser`, `fourth meeting, 9 July`, `BHB/3/19`) — zero matches.
  This is a genuine content-loss defect, not merely a formatting one.
  Separately, the author byline "HELENA M. CROYDE" (9.6pt, clearly not a
  section heading in the source) is rendered as an `##` (H2) heading.
- **TC31 (FAIL):** the 8-row × 4-column pricing table (Determination /
  Method / Turnaround / Charge per sample) is not rendered as a Markdown
  table at all — no pipes, no header separator row. Every cell instead
  becomes its own standalone line of plain text (column headers as bold
  standalone lines, then each row's 4 values as 4 consecutive bare lines
  with no delimiter tying them to their row), so a reader cannot
  mechanically associate "Total suspended solids" with "KAL-M04", "2 days",
  and "£18.40" as one row without inferring position from the original PDF.
- **TC32/TC115 (CAN NOT BE GRADED):** `monitoring_station_schedule_2026.pdf`
  re-confirmed unreachable today via a fresh `clickup_download_task_attachment`
  call against the authoritative input task `86bbr4dmu`, followed by an
  immediate `curl` on the returned signed URL — identical
  `curl: (56) CONNECT tunnel failed, response 403` to every prior attempt
  across the Docling, LiteParse, and MarkItDown rounds. No new route into
  this sandbox has opened.

Evidence for every TC (input PDF, terminal-capture screenshot, generated
Markdown, execution log) is attached directly to its ClickUp subtask and
also committed under `input/`, `output/`, and
`screenshots/terminal_captures/` in this directory.

## Scope note

Per explicit instruction, **only TC27–TC32/TC115 were executed or touched in
this pass.** TC33–TC38 and their scenario tasks (S33–S38) were not inspected,
not modified, and not executed. No recommendation is made here about
TC33–TC38; that is deferred to a future round.

## Fix/improvement pass (2026-09-15, second pass)

Per explicit instruction, investigated whether any of the FAILs above could
be genuinely improved through small, legitimate, reproducible code-level
fixes — not by hand-editing generated Markdown. Read doc2mark 0.6.1's own
source directly
(`.venv_doc2mark/lib/python3.11/site-packages/doc2mark/pipelines/pymupdf_advanced_pipeline.py`)
to find the actual root cause of each FAIL, then wrote
`scripts/doc2mark_fixes.py`: a set of monkeypatches applied at runtime (via
`run_doc2mark.py ... --patched`) on top of the unmodified installed package —
no files inside doc2mark itself are edited, and every patch wraps and
delegates to doc2mark's own original method first, so all of its existing
extraction/classification/table logic is reused unchanged. The full
reasoning, the exact doc2mark bug each patch targets (with source line
references), and the regression-check failures caught and fixed along the
way are documented in that file's module docstring.

**Every fixture was re-run through the patch, including TC27 and TC31, purely
as a regression check** (`output_patched/<stem>/`, distinct from the original
`output/<stem>/` evidence, which is preserved unchanged).

### Audit table

| TC | Previous Verdict | New Verdict | What Changed |
|---|---|---|---|
| TC27 | PASS | **PASS (unchanged)** | Regression-checked only: patched output is byte-identical to the original (`diff` exit 0). No new evidence needed beyond the regression-check capture. |
| TC28 | FAIL | **PASS** | Root cause found: `_process_page` sorted all page content purely by `position_y`, with no column/x-awareness at all (confirmed: `doc2mark.core.types.SimpleContent` never stores an x-coordinate). Patched with a column-aware sort that only activates when a page's blocks show real two-cluster x0 evidence (avoiding false positives on single-column pages — caught and fixed twice during regression-checking, see below). Re-run against `bulletin_no_212.pdf`: all 3 previously-quoted displaced fragments now appear in the correct position, and a full manual read-through of the patched output top-to-bottom confirms genuinely correct column-major reading order on all 3 pages, verified line-by-line against the source PDF's own block coordinates. |
| TC29 | FAIL | **FAIL (unchanged, but improved)** | Root cause found: `_convert_block_to_markdown_with_type` only assigns the H1-equivalent `text:title` type when `page_num == self._get_first_text_page_num()` — a page-position gate, not a font-size one. Patched so a block classified `text:section` (H2) is promoted to `text:title` (H1) whenever its font size matches the single largest heading-candidate size anywhere in the document (computed once, memoized), regardless of page. Re-run: all 15 identically-16pt section headers ("Scope" through "Revision history") now render consistently as `#` instead of 4 as `#` and 11 as `##`. **Verdict stays FAIL** because the scenario objective is the full heading/section structure, and the document's real second- and third-level subsection headers (13pt/12pt: "Chain of custody", "Temperature", etc.) still receive zero Markdown heading markup after the fix — confirmed by grep against the patched output. The fix resolves a genuine, confirmed inconsistency bug but does not make the output satisfy the TC objective. |
| TC30 | FAIL | **PASS** | Two root causes found and fixed. (1) `_has_heading_layout_signal` treats any all-caps text as a heading signal regardless of font size; patched to require all-caps text be at least body-sized (`size_ratio >= 1.0`) — the byline "HELENA M. CROYDE" (9.6pt vs. a ~10.15pt page-1 average) is no longer misclassified as a heading. (2) When PyMuPDF merges several tightly-spaced footnotes into one block (confirmed: footnotes 8, 9, 10 are one block on page 3), `pdf_to_markdown()`'s footnote-regex only converts the block's first line, silently discarding the rest; patched `_extract_text_as_markdown` to split a merged footnote block into one item per footnote before it ever reaches the unmodified `pdf_to_markdown()`. Re-run: footnotes 9 and 10 are recovered (`[^9]:`, `[^10]:`), and footnotes 12 and 13 — genuinely present on page 4 of the source PDF but also silently dropped in the original run, not previously flagged — are recovered too. All 13 footnotes' content is now present somewhere in the output (footnotes 1–7 remain as plain unbracketed lines, a pre-existing, separate classification path this pass did not touch, but their full text was never lost either way) and the byline is no longer a spurious heading. |
| TC31 | FAIL | **FAIL (unchanged)** | Investigated: doc2mark already calls `page.find_tables()` (default `strategy="lines"`), which finds 0 tables here because the pricing table is borderless (no ruling lines for PyMuPDF's default detector to see). Tested falling back to `strategy="text"` on the whole page: it does detect *something*, but a 74-row/11-col false positive spanning the entire page — ordinary body paragraphs (e.g. "The charges below apply to samples...") get split into the same number of populated pseudo-columns (10) as the real table's own data rows, so density-based filtering cannot tell them apart on this fixture. A hand-picked clip rectangle around just the table's own coordinates does produce a clean, correct 4-column table via `strategy="text"` — but that requires already knowing where the table is, which is not a legitimate general Doc2Mark workflow change, only a per-file hack. No safe, general, non-regressive fix was found within scope, so **no table-extraction patch was applied** and TC31 remains FAIL, unchanged. |
| TC32 / TC115 | CAN NOT BE GRADED | **CAN NOT BE GRADED (unchanged)** | One permitted retry: fresh `clickup_download_task_attachment` + immediate `curl`, identical `curl: (56) CONNECT tunnel failed, response 403`. No local copy of this fixture exists anywhere in the repository. Left as CAN NOT BE GRADED per instruction, without further attempts. |

**Updated totals: PASS: 3 · FAIL: 2 · CAN NOT BE GRADED: 1** (previously PASS: 1 · FAIL: 4 · CAN NOT BE GRADED: 1)

### Regression check detail (why this matters)

The reading-order patch (TC28) went through two real, caught-and-fixed
regressions before being adopted, both found only because *every* fixture —
not just TC28's own — was re-run through the patch:

1. An initial version classified column membership by block width alone
   ("narrow" vs. "full-width"), which mis-split `schedule_of_analysis_charges_2026.pdf`
   (TC31, genuinely single-column): its short heading lines ("How to submit
   samples", "Containers and preservation") are narrower than its body
   paragraphs at the *same* x0, and got wrongly treated as a second column,
   corrupting TC31's (already-FAIL, but differently-shaped) output. Fixed by
   requiring two-cluster x0 evidence (a large, centrally-located gap) before
   committing to column-aware reordering at all.
2. A second version added that clustering check but still mis-fired on
   `briefing_note_BEP-BN-2026-04.pdf` (TC27, genuinely single-column and
   already PASSing): a single narrow, isolated "Page N of 7" footer sitting
   to the right of the body text was enough to manufacture a spurious
   "two-cluster" gap. Fixed by additionally requiring at least 2 blocks on
   *each* side of the gap, which a lone footer can never satisfy.

Both were only caught because TC27 and TC31 were re-run as part of this
pass's regression check, not because they were the TCs being fixed — exactly
why the instruction to re-run every fixture, not just the one under repair,
mattered here.

## Second batch: TC33–TC38 (2026-09-15)

Scope strictly limited to S33–S38 / TC33–TC38 per instruction. TC27–TC32/TC115
were not touched (no execution, no ClickUp changes) except where noted above.
No later TCs exist beyond TC38 for this tool.

### Fixture mapping (verified against `86bbxat2g`–`86bbxatb3` in ClickUp and
against `01_Benchmark_Design/Fixture_Validation_R1.md`, not assumed)

| Scenario | TC | Capability | Fixture |
|---|---|---|---|
| S33 (`86bbxat2g`) | TC33 (`86bbxat3r`) | C14 Figures & Charts | intertidal_survey_BEP-SR-2026-11.pdf, page 2 (figure + caption) |
| S34 (`86bbxat4j`) | TC34 (`86bbxat57`) | C14 Figures & Charts | intertidal_survey_BEP-SR-2026-11.pdf, page 3 (data chart) — same file as TC33 |
| S35 (`86bbxat62`) | TC35 (`86bbxat6z`) | C15 Scanned Document OCR | certificate_of_analysis_KAL-11938.pdf |
| S36 (`86bbxat7x`) | TC36 (`86bbxat8k`) | C15 Scanned Document OCR | service_report_KAL-ESR-4471.pdf |
| S37 (`86bbxat9e`) | TC37 (`86bbxatad`) | C16 Equations & Mathematical Notation | technical_note_TIH-TN-18.pdf |
| S38 (`86bbxatb3`) | TC38 (`86bbxatc8`) | C17 Code Extraction | operations_note_DS-OP-07.pdf |

Per `Fixture_Validation_R1.md`, TC38's fixture carries 3 monospace blocks
(a Python function, a shell invocation, a block-header example); only the
indented Python function under "The fix" is the graded region — the shell
command and header example are explicitly not graded.

### Summary

| TC | Capability | Fixture | Verdict |
|---|---|---|---|
| TC33 | C14 Figures & Charts | intertidal_survey_BEP-SR-2026-11.pdf (p.2) | PASS |
| TC34 | C14 Figures & Charts | intertidal_survey_BEP-SR-2026-11.pdf (p.3) | PASS |
| TC35 | C15 Scanned Document OCR | certificate_of_analysis_KAL-11938.pdf | CAN NOT BE GRADED (fixture unreachable) |
| TC36 | C15 Scanned Document OCR | service_report_KAL-ESR-4471.pdf | CAN NOT BE GRADED (fixture unreachable) |
| TC37 | C16 Equations & Mathematical Notation | technical_note_TIH-TN-18.pdf | CAN NOT BE GRADED (fixture unreachable) |
| TC38 | C17 Code Extraction | operations_note_DS-OP-07.pdf | FAIL |

**PASS: 2 · FAIL: 1 · CAN NOT BE GRADED: 3** (of 6 TCs this batch)

### Key findings

- **TC33/TC34 (both PASS):** ran with `extract_images=True` (stock, unpatched
  doc2mark — the reading-order/heading fixes from the first fix pass are
  unrelated to image handling and were not applied here). Both images
  extract as real, undamaged, correctly-positioned base64 PNGs (1886×877 and
  2970×1765, decoded and visually inspected directly, not assumed from a
  placeholder): the transect-map figure lands immediately after the
  `<!-- page 2 -->` marker, right after its lead-in sentence ("The plan
  below shows the four lines..."), followed immediately by its actual
  caption ("*Figure 1. Survey transects at Kellow Sands and Thrimby
  Point...*"). The chart lands immediately after the `<!-- page 3 -->`
  marker and its own section intro, followed by real explanatory text about
  the plotted rates. Visual inspection of the chart image itself confirms
  its title ("Mean sediment accretion by transect, winters 2023/24 to
  2025/26"), both axis labels ("Accretion (mm/yr)", "Transect"), and its
  3-entry legend are all intact within the image — consistent with this
  fixture's design intent per `Fixture_Validation_R1.md` ("the chart's
  twelve values appear nowhere in the text", i.e. a genuine image-only chart
  that a tool cannot pass by copying visible text).
- **TC38 (FAIL):** the graded code block — the indented Python function
  under "The fix" — is rendered with **zero Markdown code-fence markup and
  zero indentation preserved**. Every line of the function body (`export =
  Export.open(station)`, `for block in export.blocks(window):`, `if
  block.checksum_ok():`, etc.) starts at column 0, indistinguishable from
  surrounding prose; as plain text this is not valid, readable Python. The
  2 non-graded monospace blocks (shell invocation, block-header example)
  show the identical pattern (flattened, no fence), for reference.
- **TC35/TC36/TC37 (CAN NOT BE GRADED):** all 3 required fixtures
  (`certificate_of_analysis_KAL-11938.pdf`, `service_report_KAL-ESR-4471.pdf`,
  `technical_note_TIH-TN-18.pdf`) were attempted fresh via
  `clickup_download_task_attachment` + immediate `curl` — identical
  `curl: (56) CONNECT tunnel failed, response 403` for all 3, the same
  organization-policy block confirmed in every prior round of this project.
  **Separately investigated whether OCR itself would even be usable if the
  fixtures were reachable:** doc2mark supports 4 OCR providers (`openai`,
  `vertex_ai`, `gemini`, `tesseract`). The system `tesseract` binary (5.3.4)
  was already present in this environment; only the `pytesseract` Python
  wrapper was missing, and was installed (`pip install pytesseract`) as a
  legitimate, small, reproducible dependency fix. A synthetic, locally-made,
  image-only test page (no real benchmark content, never used as TC
  evidence) confirmed `UnifiedDocumentLoader(ocr_provider="tesseract")`
  genuinely performs local, offline OCR end-to-end with no API key. **This
  means the TC35/TC36/TC37 blocker is fixture access specifically, not an
  OCR/model/dependency limitation** — if any of the 3 fixtures becomes
  reachable in a future round, real OCR grading against it is possible in
  this same environment.

Evidence for every TC this batch (input PDF where obtained, terminal-capture
screenshots, generated Markdown, extracted images, execution logs) is
attached directly to its ClickUp subtask and committed under `input/`,
`output/`, and `screenshots/terminal_captures/` in this directory.

### Scope note

Per explicit instruction, only TC33–TC38 were executed or touched in this
batch. TC27–TC32/TC115 were not re-executed or modified. There are no TCs
beyond TC38 for this tool/round.
