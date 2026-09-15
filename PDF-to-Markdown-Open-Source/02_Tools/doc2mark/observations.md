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
