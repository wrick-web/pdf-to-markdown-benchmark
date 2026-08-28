# Evidence

This is a CLI-only sandbox with no browser/GUI, so this project could not
capture actual screen-recorded screenshots itself (per the task brief, the
user is doing the final screen recording manually). What's here instead is
**textual evidence** — verbatim excerpts from real tool output, each
labeled with exactly what it demonstrates and where the full file lives —
so the user can quickly find and re-capture the same moments visually
during their recording (e.g., open the referenced `.md` file at the quoted
line and screen-record scrolling to it).

| File | Demonstrates |
|---|---|
| `01_kreuzberg_table_omission.md` | Kreuzberg completely failing to reconstruct a dense financial table (PDF2) — numbers/labels present, structure gone |
| `02_kreuzberg_heading_fragmentation.md` | Kreuzberg over-fragmenting a single title into 4 spurious heading/list blocks (PDF2) |
| `03_kreuzberg_hierarchy_scan_vs_native.md` | Same tool, opposite hierarchy failure modes: 289 headings on native-text PDF1 vs. 0 headings on scanned PDF3 |
| `04_openparse_table_degraded.md` | open-parse producing DEGRADED (scrambled, not omitted) table data with leaked HTML tags (PDF2) |
| `05_openparse_pdf1_crash.md` | open-parse's uncaught crash on the most complex benchmark PDF |
| `06_kreuzberg_ocr_quality.md` | Kreuzberg/Tesseract OCR output quality on the scanned research paper (PDF3), including two concrete misread examples |

Each per-tool `02_Tools/<tool>/evidence/` folder cross-references the same
excerpts plus points back at the exact source `.md`/`.json`/`.log` file
for anyone who wants to verify a claim independently.
