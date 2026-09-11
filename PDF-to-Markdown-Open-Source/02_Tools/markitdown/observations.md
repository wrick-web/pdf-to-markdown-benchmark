# MarkItDown — Round 1 execution (2026-09-10)

Task: `EXEC · MarkItDown · PDF-OSS v1 · R1` (`86bbu4xeb`), 12 scenario lines
(S27–S38), 13 test-case lines total (S32 carries two: TC32 and TC115).

Per this pass's explicit instruction, verdicts use only **PASS / FAIL /
CAN NOT BE GRADED** — no BLOCKED/PARTIAL. Full per-TC write-ups (with the
same Test Objective/Fixture/What Was Tested/What We Observed/Expected/
Verdict/Assessment/Evidence structure) are posted directly on each TC
observation subtask under `86bbu4xeb`; this file is the local mirror plus
the summary table.

## Environment

- MarkItDown version: **0.1.7** (PyPI `markitdown[pdf]`), Microsoft, MIT license
- Environment: `.venv_markitdown` (`uv venv`-equivalent + `pip install`), Python 3.11
- Command shape (`scripts/run_markitdown.py`):
  ```python
  from markitdown import MarkItDown
  md = MarkItDown()
  result = md.convert("<input.pdf>")
  print(result.text_content)
  ```
- No model download of any kind for the plain-PDF path used here — pure
  Python/pdfminer-family extraction, zero network calls, so all 6
  executed TCs ran cleanly the first time.

## Summary

| TC | Capability | Fixture | Verdict |
|---|---|---|---|
| TC27 | C10 Text Fidelity | briefing_note_BEP-BN-2026-04.pdf | FAIL |
| TC28 | C11 Reading Order & Layout | bulletin_no_212.pdf | FAIL |
| TC29 | C12 Heading & Section Structure | procedure_KAL-SP-06_sample_reception.pdf (re-run 2026-09-11 against corrected 43,662-byte fixture) | FAIL |
| TC30 | C12 Heading & Section Structure | croyde_1974_braithe_order_offprint.pdf | PASS |
| TC31 | C13 Table Extraction | schedule_of_analysis_charges_2026.pdf | FAIL |
| TC32 / TC115 | C13 Table Extraction | monitoring_station_schedule_2026.pdf | CAN NOT BE GRADED (fixture unavailable) |
| TC33 | C14 Figures & Charts | intertidal_survey_BEP-SR-2026-11.pdf (p.2) | FAIL |
| TC34 | C14 Figures & Charts | intertidal_survey_BEP-SR-2026-11.pdf (p.3) | FAIL |
| TC35 | C15 Scanned Document OCR | certificate_of_analysis_KAL-11938.pdf | CAN NOT BE GRADED (fixture unavailable) |
| TC36 | C15 Scanned Document OCR | service_report_KAL-ESR-4471.pdf | CAN NOT BE GRADED (fixture unavailable) |
| TC37 | C16 Equations & Mathematical Notation | technical_note_TIH-TN-18.pdf | CAN NOT BE GRADED (fixture unavailable) |
| TC38 | C17 Code Extraction | operations_note_DS-OP-07.pdf | FAIL (executed 2026-09-11, fixture user-supplied) |

**PASS: 1 · FAIL: 6 · CAN NOT BE GRADED: 6** (13 lines total)

## Key findings (detail on each TC subtask in ClickUp)

- **TC27 (FAIL):** all text present, but repeated page header/footer/page-number
  text is injected inline mid-sentence at every one of 7 page breaks, with
  no separator.
- **TC28 (FAIL):** genuine column-interleaving — 3 quotable, verifiable
  sentence displacements across the 2-column fixture.
- **TC29 (FAIL):** zero Markdown heading levels generated anywhere in the
  document; the real 4-level heading hierarchy is completely flattened to
  plain text.
- **TC30 (PASS):** all 13 footnote markers and texts present, correctly
  numbered and grouped out of body flow at each page break — no footnote
  dropped.
- **TC31 (FAIL):** table renders as a malformed 5-column table; the real
  "Charge per sample" column is empty in every row, values shifted into an
  unlabeled trailing column.
- **TC33 (FAIL):** the figure's caption text survives, but the image
  itself is completely absent — no embed, reference, or placeholder.
- **TC34 (FAIL):** the chart is missing even more completely than TC33 —
  no image and not even the chart's title survive.
- **TC32/TC115, TC35–38 (CAN NOT BE GRADED):** all 5 remaining fixtures
  re-confirmed unreachable today via fresh `clickup_download_task_attachment`
  + immediate `curl`, identical `403`/CONNECT-tunnel rejection each time —
  same organization-policy block on the ClickUp attachment CDN documented
  throughout this project's Docling/LiteParse rounds.

Evidence for every TC (input PDF where obtained, terminal-capture screenshot,
generated Markdown) is attached directly to its ClickUp subtask and also
committed under `input/`, `output/`, and `screenshots/terminal_captures/`
in this directory.

## Re-audit (2026-09-11)

Per explicit instruction, re-examined every TC's existing evidence a second
time looking specifically for legitimate PASS upgrades and for
CAN NOT BE GRADED cases that could now genuinely be executed — not to
inflate the count, but to check the first pass didn't grade anything
unfairly harshly.

**Result: no verdict changed.** For the 6 executed TCs, each output file was
re-read directly against its objective a second time:
- TC27 was the closest call — re-reading the raw output at the page-break
  boundaries found two concrete, verbatim fusions where the running header
  is directly adjacent (no blank line) to unrelated body text, e.g.
  "Braithe Estuary Partnership have shown so far." This is genuine
  text-level corruption, not merely cosmetic extra lines, so FAIL is
  confirmed with sharper evidence than the first pass had.
- TC28/29/31/33/34 were re-checked against their original quoted evidence
  (column displacement, absent heading markup, misaligned table, absent
  image) and every one reproduced identically — no reason found to reverse
  any of them.
- TC30 was re-checked specifically looking for a reason to *downgrade* the
  existing PASS (all 13 footnotes individually re-verified) — none found.

For the 6 CAN NOT BE GRADED TCs, fresh signed URLs were requested again
today and the direct download was re-attempted for all 5 underlying
fixtures — identical `curl: (56) CONNECT tunnel failed, response 403` each
time. No new route into this sandbox has opened up since the first pass.

**PASS: 1 · FAIL: 6 · CAN NOT BE GRADED: 6 — unchanged from the first pass.**

## Retry with user-supplied fixtures (2026-09-11, second pass)

The user manually uploaded 3 PDFs directly into this session:
`operations_note_DS-OP-07.pdf`, `procedure_KAL-SP-06_sample_reception.pdf`,
and `intertidal_survey_BEP-SR-2026-11.pdf`. Checked each by SHA256 against
what was already in hand before deciding what to do with it:

- **`operations_note_DS-OP-07.pdf` (80,041 bytes) — genuinely new.**
  Real MarkItDown execution against it. All 3 monospace blocks in the
  fixture (a Python function, a shell command, a raw block-header example)
  survive with line breaks and indentation intact, but **zero Markdown
  code-fence/preformatting markup is produced anywhere** — the same
  "content survives, the specific Markdown construct never appears"
  pattern already found on TC29's headings. **TC38: CAN NOT BE GRADED →
  FAIL** (now genuinely executed and gradeable; the result is a real FAIL,
  not a PASS).
- **`procedure_KAL-SP-06_sample_reception.pdf` (43,662 bytes) — a
  different file than the one originally used for TC29.** The original
  TC29 run used a 128,546-byte file with a different SHA256 — a real
  fixture-size discrepancy, not noticed until this pass. Re-ran against
  the correct, canonical-sized file. Result: identical — zero heading
  markup either way. **TC29: FAIL → FAIL** (verdict unchanged, but now
  backed by the correct fixture; original run's evidence preserved
  alongside the corrected run's).
- **`intertidal_survey_BEP-SR-2026-11.pdf` — byte-identical (SHA256
  verified) to the file already used for TC33/TC34.** No new information;
  not re-executed. TC33/TC34 verdicts stand as already graded.

None of the 3 uploads corresponded to TC32/TC115 (`monitoring_station_schedule_2026.pdf`),
TC35 (`certificate_of_analysis_KAL-11938.pdf`), TC36
(`service_report_KAL-ESR-4471.pdf`), or TC37 (`technical_note_TIH-TN-18.pdf`)
— those 5 test-case lines remain **CAN NOT BE GRADED**, unchanged.

**Updated totals: PASS: 1 · FAIL: 7 · CAN NOT BE GRADED: 5.**
