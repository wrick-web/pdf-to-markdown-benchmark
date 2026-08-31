# Remap Note — Pre-Rev2 vs Rev 2 Benchmark Results

**Everything else in this folder** (`MASTER_RESULTS.md`, `Scorecards/`,
`Comparison_Tables/`, `Evidence/`) was produced **before** the frozen Rev
2 benchmark specification (`01_Benchmark_Design/`) existed, against a
different, ad-hoc 9-criteria/3-PDF design:

Chart Reconstruction, Text Preservation, Table Reconstruction, Document
Hierarchy, Image Retention, Reading Order, Caption/Figure Association,
Long/Complex Document Robustness, Bonus/Anomalous — scored 0–5, run against
3 real documents (hybrid earnings report, financial report, scanned
research paper).

## This is not discarded

That work is real, is not being deleted or rewritten, and remains useful
prior evidence — several of its findings (e.g. Kreuzberg's 0-tables-detected
result, Docling's uniform chart omission, MinerU's density-linked table
failures) are directly cited in `02_Tools/Tool_Capability_Matrix.md` as
pre-Rev2 evidence for the corresponding new capability.

## Why it isn't the same as a Rev-2 result

1. **Grading unit differs.** The old benchmark graded whole documents
   holistically; Rev 2's core rule 2 requires one scenario → one focused
   verdict, located to a specific page/region, graded separately. Old
   evidence is mostly `T-agg` (aggregate) rather than `T-iso` (isolated to
   one scenario) — see `02_Tools/Tool_Scenario_Matrix.md` for which is
   which.
2. **Taxonomy differs.** "Document Hierarchy" and "Reading Order" map
   reasonably cleanly to C12/C11. "Chart Reconstruction" partly maps to
   C14, but Rev 2 explicitly separates *preservation* (the minimum bar)
   from *enrichment* (chart data extraction, never required) — the old
   scoring didn't make that distinction, so an old "Chart Reconstruction"
   score is not directly reusable as a C14 verdict without re-reading the
   underlying observation.
3. **Two capabilities have no old-benchmark equivalent at all.** C16
   (Equations) and C17 (Code) were never scenarios in the old design —
   none of the 3 old test PDFs contained equations or code, confirmed
   independently two ways (see `01_Benchmark_Design/Input_Status.md`).
4. **Fixtures differ.** Rev 2 requires purpose-authored fixtures per TC
   (core rule 11); the old 3 PDFs were real-world documents chosen for
   realism, not built to isolate one condition each.

## What to do instead of treating old scores as new ones

Use `02_Tools/Tool_Capability_Matrix.md` and `Tool_Scenario_Matrix.md` —
they already carry the honest TESTED (pre-Rev2) / DOCUMENTED / NOT TESTED
/ BLOCKED labeling per tool per capability/scenario, with the aggregate-vs-
isolated caveat built in. Do not port a 0–5 score from `MASTER_RESULTS.md`
directly into a TC27–TC38 Evidence page.
