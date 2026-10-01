# doc2mark attachment rename checklist

Convention: `doc2mark_S{##}_TC{##}_{scenario-slug}_{evidence-kind}.{ext}`
Status/progress is untouched — this is renaming only. Items marked **(stale leftover)**
are old artifacts from before a fixture issue was resolved elsewhere — rename them too
if you want full consistency, or skip them, your call.

How to rename in ClickUp: open the task → Attachments → hover the file → "⋯" → Rename.

---

## TC27 — [Ordinary digital text — complete and unchanged](https://app.clickup.com/t/86bbxartp)
Slug: `ordinary-digital-text-complete-unchanged`

| Current name | New name |
|---|---|
| doc2mark_s27_tc27_briefing_note_BEP-BN-2026-04 (.pdf) | doc2mark_S27_TC27_ordinary-digital-text-complete-unchanged_input-pdf.pdf |
| doc2mark_s27_tc27_briefing_note_BEP-BN-2026-04_capture (.png) | doc2mark_S27_TC27_ordinary-digital-text-complete-unchanged_terminal-capture.png |
| doc2mark_s27_tc27_breifingnote (.md) | doc2mark_S27_TC27_ordinary-digital-text-complete-unchanged_markdown-output.md |
| doc2mark_s27_tc27_briefingnote (.log) | doc2mark_S27_TC27_ordinary-digital-text-complete-unchanged_execution-log.log |
| doc2mark_s27_tc27_screencapture (.png) | doc2mark_S27_TC27_ordinary-digital-text-complete-unchanged_regression-check-terminal-capture.png |

---

## TC28 — [Two-column page — natural reading order](https://app.clickup.com/t/86bbxaruq)
Slug: `two-column-reading-order`

| Current name | New name |
|---|---|
| bulletin_no_212 (.pdf) | doc2mark_S28_TC28_two-column-reading-order_input-pdf.pdf |
| bulletin_no_212_capture (.png) | doc2mark_S28_TC28_two-column-reading-order_terminal-capture-stock.png |
| bulletin_no_212 (.md, size 12353, earliest) | doc2mark_S28_TC28_two-column-reading-order_markdown-output-stock-v1.md |
| bulletin_no_212 (.log, size 291, earliest) | doc2mark_S28_TC28_two-column-reading-order_execution-log-stock-v1.log |
| bulletin_no_212_ORIGINAL_STOCK_RUN_FAIL (.md) | doc2mark_S28_TC28_two-column-reading-order_markdown-output-stock-v2.md |
| bulletin_no_212_ORIGINAL_STOCK_RUN_FAIL (.log) | doc2mark_S28_TC28_two-column-reading-order_execution-log-stock-v2.log |
| bulletin_no_212 (.md, size 12353, mid-date ~465157) | doc2mark_S28_TC28_two-column-reading-order_markdown-output-patched-reference-v1.md |
| bulletin_no_212 (.log, size 340, mid-date ~465162) | doc2mark_S28_TC28_two-column-reading-order_execution-log-patched-reference-v1.log |
| bulletin_no_212_patched_capture (.png) | doc2mark_S28_TC28_two-column-reading-order_terminal-capture-patched-reference.png |
| doc2mark_fixes (.py) | doc2mark_S28_TC28_two-column-reading-order_fix-source-reference.py |
| bulletin_no_212_PATCHED_RUN_PASS (.md) | doc2mark_S28_TC28_two-column-reading-order_markdown-output-patched-reference-v2.md |
| bulletin_no_212_PATCHED_RUN_PASS (.log) | doc2mark_S28_TC28_two-column-reading-order_execution-log-patched-reference-v2.log |

Note: "patched" versions here are reference-only (the graded verdict is the stock run = FAIL).

---

## TC29 — [Styled headings — hierarchy preserved](https://app.clickup.com/t/86bbxarvz)
Slug: `styled-headings-hierarchy-preserved`

| Current name | New name |
|---|---|
| procedure_KAL-SP-06_sample_reception_43662 (.pdf) | doc2mark_S29_TC29_styled-headings-hierarchy-preserved_input-pdf.pdf |
| procedure_KAL-SP-06_sample_reception_43662_capture (.png) | doc2mark_S29_TC29_styled-headings-hierarchy-preserved_terminal-capture-original.png |
| procedure_KAL-SP-06_sample_reception_43662 (.md, earliest ~459420) | doc2mark_S29_TC29_styled-headings-hierarchy-preserved_markdown-output-original-v1.md |
| procedure_KAL-SP-06_sample_reception_43662 (.log, earliest ~459424) | doc2mark_S29_TC29_styled-headings-hierarchy-preserved_execution-log-original-v1.log |
| procedure_KAL-SP-06_sample_reception_43662_ORIGINAL_STOCK_RUN_FAIL (.md) | doc2mark_S29_TC29_styled-headings-hierarchy-preserved_markdown-output-original-v2.md |
| procedure_KAL-SP-06_sample_reception_43662_ORIGINAL_STOCK_RUN_FAIL (.log) | doc2mark_S29_TC29_styled-headings-hierarchy-preserved_execution-log-original-v2.log |
| procedure_KAL-SP-06_sample_reception_43662 (.md, mid-date ~465199) | doc2mark_S29_TC29_styled-headings-hierarchy-preserved_markdown-output-patched-v1.md |
| procedure_KAL-SP-06_sample_reception_43662 (.log, mid-date ~465203) | doc2mark_S29_TC29_styled-headings-hierarchy-preserved_execution-log-patched-v1.log |
| procedure_KAL-SP-06_sample_reception_43662_patched_capture (.png) | doc2mark_S29_TC29_styled-headings-hierarchy-preserved_terminal-capture-patched.png |
| procedure_KAL-SP-06_sample_reception_43662_PATCHED_RUN_STILL_FAIL (.md) | doc2mark_S29_TC29_styled-headings-hierarchy-preserved_markdown-output-patched-v2.md |
| procedure_KAL-SP-06_sample_reception_43662_PATCHED_RUN_STILL_FAIL (.log) | doc2mark_S29_TC29_styled-headings-hierarchy-preserved_execution-log-patched-v2.log |

Note: verdict is FAIL (unchanged) even after the patch — patched files are a real re-run, not reference-only here.

---

## TC30 — [Footnote — out of body flow, associated](https://app.clickup.com/t/86bbxarxj)
Slug: `footnote-out-of-body-flow`

| Current name | New name |
|---|---|
| croyde_1974_braithe_order_offprint (.pdf) | doc2mark_S30_TC30_footnote-out-of-body-flow_input-pdf.pdf |
| croyde_1974_braithe_order_offprint_capture (.png) | doc2mark_S30_TC30_footnote-out-of-body-flow_terminal-capture-original.png |
| croyde_1974_braithe_order_offprint (.md, earliest ~459444) | doc2mark_S30_TC30_footnote-out-of-body-flow_markdown-output-original-v1.md |
| croyde_1974_braithe_order_offprint (.log, earliest ~459451) | doc2mark_S30_TC30_footnote-out-of-body-flow_execution-log-original-v1.log |
| croyde_1974_braithe_order_offprint_ORIGINAL_STOCK_RUN_FAIL (.md) | doc2mark_S30_TC30_footnote-out-of-body-flow_markdown-output-original-v2.md |
| croyde_1974_braithe_order_offprint_ORIGINAL_STOCK_RUN_FAIL (.log) | doc2mark_S30_TC30_footnote-out-of-body-flow_execution-log-original-v2.log |
| croyde_1974_braithe_order_offprint (.md, mid-date ~465237) | doc2mark_S30_TC30_footnote-out-of-body-flow_markdown-output-patched-v1.md |
| croyde_1974_braithe_order_offprint (.log, mid-date ~465240) | doc2mark_S30_TC30_footnote-out-of-body-flow_execution-log-patched-v1.log |
| croyde_1974_braithe_order_offprint_patched_capture (.png) | doc2mark_S30_TC30_footnote-out-of-body-flow_terminal-capture-patched.png |
| croyde_1974_braithe_order_offprint_PATCHED_RUN_PASS (.md) | doc2mark_S30_TC30_footnote-out-of-body-flow_markdown-output-patched-v2.md |
| croyde_1974_braithe_order_offprint_PATCHED_RUN_PASS (.log) | doc2mark_S30_TC30_footnote-out-of-body-flow_execution-log-patched-v2.log |
| TC30_croyde_1974_braithe_source_page3_footnotes9-10 (.png) | doc2mark_S30_TC30_footnote-out-of-body-flow_source-page3-footnotes9-10.png |
| TC30_croyde_1974_braithe_source_page4_footnotes11-13 (.png) | doc2mark_S30_TC30_footnote-out-of-body-flow_source-page4-footnotes11-13.png |

Note: verdict is FAIL → PASS after the patch, so both original and patched are genuine graded evidence here.

---

## TC31 — [Simple table — structure retained](https://app.clickup.com/t/86bbxaryz)
Slug: `simple-table-structure-retained`

| Current name | New name |
|---|---|
| schedule_of_analysis_charges_2026 (.pdf) | doc2mark_S31_TC31_simple-table-structure-retained_input-pdf.pdf |
| schedule_of_analysis_charges_2026_capture (.png) | doc2mark_S31_TC31_simple-table-structure-retained_terminal-capture.png |
| schedule_of_analysis_charges_2026 (.md) | doc2mark_S31_TC31_simple-table-structure-retained_markdown-output.md |
| schedule_of_analysis_charges_2026 (.log) | doc2mark_S31_TC31_simple-table-structure-retained_execution-log.log |
| schedule_of_analysis_charges_2026_investigation_capture (.png) | doc2mark_S31_TC31_simple-table-structure-retained_table-investigation-terminal-capture-v1.png |
| TC31_schedule_of_analysis_charges_investigation_capture_CLEAN (.png) | doc2mark_S31_TC31_simple-table-structure-retained_table-investigation-terminal-capture-v2-clean.png |

---

## TC32 — [Cross-page table — one table, complete](https://app.clickup.com/t/86bbxat0u)
Slug: `cross-page-table-one-table-complete` — **CAN NOT BE GRADED (fixture unreachable)**

| Current name | New name |
|---|---|
| monitoring_station_schedule_2026_capture (.png) | doc2mark_S32_TC32_cross-page-table-one-table-complete_fixture-blocked-terminal-capture-v1.png |
| monitoring_station_schedule_2026_retry2_capture (.png) | doc2mark_S32_TC32_cross-page-table-one-table-complete_fixture-blocked-terminal-capture-v2-retry.png |

(No input PDF or markdown output exists — the fixture was never obtained, so nothing to rename there.)

---

## TC115 — [Cross-page table — continuation without a repeated header](https://app.clickup.com/t/86bbxat1f)
Slug: `cross-page-table-continuation-no-repeated-header`

| Current name | New name |
|---|---|
| TC115_sampling_visits_winter_2026_20260930 (.png) | doc2mark_S32_TC115_cross-page-table-continuation-no-repeated-header_terminal-capture.png |
| sampling_visits_winter_2026 (.md) | doc2mark_S32_TC115_cross-page-table-continuation-no-repeated-header_markdown-output.md |
| monitoring_station_schedule_2026_capture (.png) | doc2mark_S32_TC115_cross-page-table-continuation-no-repeated-header_stale-monitoring-station-leftover-v1.png **(stale leftover)** |
| monitoring_station_schedule_2026_retry2_capture (.png) | doc2mark_S32_TC115_cross-page-table-continuation-no-repeated-header_stale-monitoring-station-leftover-v2.png **(stale leftover)** |

Note: the two "monitoring_station" files are leftovers from before the TC32/TC115 fixture mix-up was
corrected — they're not real TC115 evidence (TC115's real fixture is sampling_visits_winter_2026.pdf).
Flagged clearly rather than silently relabeled as if they were genuine evidence.

---

## TC33 — [Figure with caption — preserved in place](https://app.clickup.com/t/86bbxat3r)
Slug: `figure-with-caption-preserved-in-place` — graded verdict is the **default-config** run (FAIL)

| Current name | New name |
|---|---|
| intertidal_survey_BEP-SR-2026-11 (.pdf) | doc2mark_S33_TC33_figure-with-caption-preserved-in-place_input-pdf.pdf |
| intertidal_survey_BEP-SR-2026-11_capture (.png) | doc2mark_S33_TC33_figure-with-caption-preserved-in-place_terminal-capture-nondefault-extractimages-reference.png |
| intertidal_survey_BEP-SR-2026-11 (.md, 339785 bytes) | doc2mark_S33_TC33_figure-with-caption-preserved-in-place_markdown-output-nondefault-extractimages-reference.md |
| intertidal_survey_BEP-SR-2026-11 (.log, size 550) | doc2mark_S33_TC33_figure-with-caption-preserved-in-place_execution-log-nondefault-extractimages-reference.log |
| intertidal_survey_BEP-SR-2026-11_image_0 (.png) | doc2mark_S33_TC33_figure-with-caption-preserved-in-place_extracted-figure-nondefault-reference.png |
| intertidal_survey_BEP-SR-2026-11_DEFAULT_RUN_FAIL (.md) | doc2mark_S33_TC33_figure-with-caption-preserved-in-place_markdown-output-default-config.md |
| intertidal_survey_BEP-SR-2026-11_DEFAULT_RUN_FAIL (.log) | doc2mark_S33_TC33_figure-with-caption-preserved-in-place_execution-log-default-config.log |
| intertidal_survey_BEP-SR-2026-11_default_rerun_capture (.txt) | doc2mark_S33_TC33_figure-with-caption-preserved-in-place_terminal-capture-default-config.txt |

---

## TC34 — [Data chart — preserved with title](https://app.clickup.com/t/86bbxat57)
Slug: `data-chart-preserved-with-title` (PASS — intentionally run with `extract_images=True`)

| Current name | New name |
|---|---|
| intertidal_survey_BEP-SR-2026-11 (.pdf) | doc2mark_S34_TC34_data-chart-preserved-with-title_input-pdf.pdf |
| intertidal_survey_BEP-SR-2026-11_capture (.png) | doc2mark_S34_TC34_data-chart-preserved-with-title_terminal-capture.png |
| intertidal_survey_BEP-SR-2026-11 (.md) | doc2mark_S34_TC34_data-chart-preserved-with-title_markdown-output.md |
| intertidal_survey_BEP-SR-2026-11 (.log) | doc2mark_S34_TC34_data-chart-preserved-with-title_execution-log.log |
| intertidal_survey_BEP-SR-2026-11_image_1 (.png) | doc2mark_S34_TC34_data-chart-preserved-with-title_extracted-chart.png |

---

## TC35 — [Clean scan — text recovered](https://app.clickup.com/t/86bbxat6z)
Slug: `clean-scan-text-recovered` — **CAN NOT BE GRADED (fixture unreachable)**

| Current name | New name |
|---|---|
| certificate_of_analysis_KAL-11938_capture (.png) | doc2mark_S35_TC35_clean-scan-text-recovered_fixture-blocked-terminal-capture.png |
| ocr_capability_check_capture (.png) | doc2mark_S35_TC35_clean-scan-text-recovered_ocr-capability-check-terminal-capture.png |

---

## TC36 — [Mixed pages — scanned page not skipped](https://app.clickup.com/t/86bbxat8k)
Slug: `mixed-pages-scanned-page-not-skipped`

| Current name | New name |
|---|---|
| service_report_KAL-ESR-4471_capture (.png, early date ~475011) | doc2mark_S36_TC36_mixed-pages-scanned-page-not-skipped_stale-fixture-blocked-leftover-capture.png **(stale leftover)** |
| ocr_capability_check_capture (.png, early date ~475016) | doc2mark_S36_TC36_mixed-pages-scanned-page-not-skipped_stale-ocr-capability-check-leftover.png **(stale leftover)** |
| service_report_KAL-ESR-4471 (.pdf) | doc2mark_S36_TC36_mixed-pages-scanned-page-not-skipped_input-pdf.pdf |
| service_report_KAL-ESR-4471 (.md) | doc2mark_S36_TC36_mixed-pages-scanned-page-not-skipped_markdown-output.md |
| TC36_run_20260929_102740 (.log) | doc2mark_S36_TC36_mixed-pages-scanned-page-not-skipped_execution-log.log |
| TC36_service_report_reuse_capture (.png) | doc2mark_S36_TC36_mixed-pages-scanned-page-not-skipped_terminal-capture.png |

Note: the two "stale" files are leftovers from when this fixture was still blocked, before it was
reused from PyMuPDF4LLM's session. The real evidence is the other 4 files.

---

## TC37 — [Equations — math markup or honest fallback](https://app.clickup.com/t/86bbxatad)
Slug: `equations-math-markup-or-honest-fallback` — **CAN NOT BE GRADED (fixture unreachable)**

| Current name | New name |
|---|---|
| technical_note_TIH-TN-18_capture (.png) | doc2mark_S37_TC37_equations-math-markup-or-honest-fallback_fixture-blocked-terminal-capture-v1.png |
| TC37_admin_cdn_reconfirmation_20260930 (.log) | doc2mark_S37_TC37_equations-math-markup-or-honest-fallback_admin-cdn-reconfirmation-log.log |
| TC37_admin_cdn_reconfirmation_20260930 (.png) | doc2mark_S37_TC37_equations-math-markup-or-honest-fallback_admin-cdn-reconfirmation-terminal-capture.png |

---

## TC38 — [Code block — fenced, structure intact](https://app.clickup.com/t/86bbxatc8)
Slug: `code-block-fenced-structure-intact`

| Current name | New name |
|---|---|
| operations_note_DS-OP-07 (.pdf) | doc2mark_S38_TC38_code-block-fenced-structure-intact_input-pdf.pdf |
| operations_note_DS-OP-07_capture (.png) | doc2mark_S38_TC38_code-block-fenced-structure-intact_terminal-capture.png |
| operations_note_DS-OP-07 (.md) | doc2mark_S38_TC38_code-block-fenced-structure-intact_markdown-output.md |
| operations_note_DS-OP-07 (.log) | doc2mark_S38_TC38_code-block-fenced-structure-intact_execution-log.log |
| TC38_operations_note_source_page2 (.png) | doc2mark_S38_TC38_code-block-fenced-structure-intact_source-page2-screenshot.png |
