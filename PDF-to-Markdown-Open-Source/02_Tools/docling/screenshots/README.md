# Screenshots — Docling (Round 1 execution)

## TC27–TC31 (2026-09-03, real fixtures, this round)

Every `TC2*`/`TC3*` file below is a **genuine rasterization of the real,
user-supplied source PDF** (`pymupdf` `page.get_pixmap()`, 150 DPI) — not
a screen capture (this sandbox has no GUI/browser), not a simulation,
and not a text-to-image representation. No Docling output screenshots
exist for these because every run failed before producing output — see
`../observations.md` for the real error captured for each.

| File | What it actually is |
|---|---|
| `TC27_01_input_pages1-2.png` | Real render of `briefing_note_BEP-BN-2026-04.pdf` pages 1–2, side by side — shows the paragraph continuing across the page break. |
| `TC28_01_input_page1.png`, `TC28_02_input_page2.png`, `TC28_03_input_page3.png` | Real renders of all 3 pages of `bulletin_no_212.pdf` — each page's two-column layout is directly visible. |
| `TC29_01_input_page1.png`, `TC29_02_input_page3.png` | Real renders of `procedure_KAL-SP-06_sample_reception.pdf` — page 1 shows the multi-level heading hierarchy (title / section / subsection / italic sub-subheading). |
| `TC30_01_input_page1.png` | Real render of `croyde_1974_braithe_order_offprint.pdf` page 1 — in-text footnote markers and the footnote block are both visible. |
| `TC31_01_input_page1.png` | Real render of `schedule_of_analysis_charges_2026.pdf` page 1 — the full simple table is visible. |

## Prior attempt (smoke-test only, before real fixtures arrived)

| File | What it actually is |
|---|---|
| `01_smoketest_pdf_page.png` | Real rasterization of a one-page throwaway smoke-test PDF used only to exercise Docling's pipeline-init code path before real fixtures were available. **Not a benchmark fixture.** |
| `02_error_default_ocr.png`, `03_error_ocr_disabled.png` | Text-to-image renderings of two real captured tracebacks, made when no real fixture existed yet. Kept for the record; **not repeated this round** — this phase's instructions rule out text-to-image renderings as a screenshot substitute, so TC27–TC31's evidence is genuine PDF renders only, with the real error text left in the `.log` files instead. |

## What is NOT here, and why

- **Docling Markdown output** — no run completed for any of TC27–TC31 (or
  the earlier smoke test); Docling's pipeline cannot initialize in this
  sandbox (see `../observations.md`). There is nothing to screenshot.
- **Input → output comparison** — not producible without a completed
  run.
- **Table/figure-specific rendered evidence** — the real table (TC31) and
  heading hierarchy (TC29) are visible in the real input-page renders
  above; there is no Docling-side rendering to compare them against.

These are documented gaps, not omissions to be quietly filled with
placeholders.
