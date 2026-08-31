# Scenario Coverage Matrix (S27–S38)

## Important caveat before reading this table

The pre-Rev2 benchmark graded **whole documents**, not isolated
scenarios — core rule 2 ("one scenario → one focused verdict, one
evidence unit," each target located precisely and graded separately)
was **not** the methodology used for any of the evidence below. Where an
old observation happens to isolate exactly one scenario's condition
(e.g., "multi-column brand list," "the genuinely scanned document"), that
is noted as **T-iso**. Where old evidence exists only as an aggregate
document-level finding that plausibly touches the scenario but wasn't
isolated to it, it's noted as **T-agg** — real prior evidence, but not a
clean Rev-2-style scenario verdict. This distinction matters more than
usual here because two scenarios have **no real evidence at all** from
any prior cycle — see below.

## Two confirmed real gaps

- **S32 (cross-page table):** none of the three pre-Rev2 test PDFs was
  confirmed to contain a table that starts on one page and continues
  onto the next with a specific isolated test for it — table findings in
  every prior record are about table *complexity* (simple vs. multi-level
  header vs. borderless), not explicitly about page-break continuation.
  Treat S32 as **essentially untested** across the whole tool landscape,
  not just under-isolated.
- **S36 (mixed digital + scanned pages, single document):** PDF3 (the
  scanned research paper) is 100% image-only, and PDF1/PDF2 are 100%
  native-digital (this repository independently confirmed PDF1's
  signature page — originally expected to be the "scanned page" in a
  hybrid document — is actually native digital text, not a scanned
  image, in the uploaded copy; see `02_Tools/kreuzberg/observations.md`).
  **No prior test document actually mixed both page types in one file.**
  S36 has zero real evidence behind it from any tool, in any cycle.

## Tools with real (pre-Rev2) evidence

| Tool | S27 | S28 | S29 | S30 | S31 | S32 | S33 | S34 | S35 | S36 | S37 | S38 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Docling | T-agg good | T-agg one merge defect | T-agg clean | T-agg (footnotes not isolated) | T-agg simple tables good | **NT** | T-agg omitted | T-agg omitted | T-iso good | **NT** | NT | NT |
| PyMuPDF4LLM | T-agg mixed | T-agg mixed | T-agg mixed | T-agg (not isolated) | T-agg preserved (simple doc) | **NT** | T-agg dropped | T-agg degraded | T-iso OCR'd, garbled | **NT** | NT | NT |
| LiteParse | T-agg mostly clean | T-agg mostly correct | T-agg mostly consistent | T-agg (not isolated) | T-agg degraded | **NT** | T-agg partial | T-agg dropped on scan | T-iso garbled | **NT** | NT | NT |
| doc2mark | T-agg good (digital only) | T-agg degraded (digital only) | T-agg degraded (digital only) | T-agg (not isolated) | T-agg inconsistent (digital only) | **NT** | T-agg degraded (digital only) | T-agg degraded (digital only) | **BLOCKED/FAILED** (0-byte) | **NT** | NT | NT |
| MarkItDown | T-agg good (digital only) | T-agg degraded (digital only) | **T-iso zero headings** (digital only) | T-agg (not isolated) | T-agg inconsistent (digital only) | **NT** | T-agg degraded (digital only) | T-agg degraded (digital only) | **BLOCKED/FAILED** (0-byte, silent) | **NT** | NT | NT |
| MinerU | T-agg good, mojibake | T-iso no defect (incl. multi-col) | T-agg correct | T-agg (footnote markers misread — not isolated) | T-agg simple tables correct | **NT** | T-agg dropped (1 doc) | T-agg dropped (1 doc) | T-iso complete/accurate | **NT** | NT | NT |
| PaddleOCR-VL/PP-StructureV3 | T-agg mixed (see note*) | T-agg mostly correct | T-agg inconsistent | T-agg (not isolated) | T-agg mostly correct | **NT** | T-agg real image files kept | T-agg real image files, no data | T-iso good | **NT** | disabled by tester | NT |
| Dolphin v1.5 | T-agg accurate, mojibake | T-iso good (2-col stitch) | T-agg preserved (2 of 3) | T-agg (not isolated) | T-agg degraded | **NT** | T-agg omitted | T-agg omitted (fabricated LaTeX on a signature — see matrix) | T-iso strong | **NT** | incidental misfire only | NT |
| Unstructured | T-agg accurate | T-iso good (incl. scan) | T-agg flattened to 1 level | T-agg (not isolated) | T-agg degraded | **NT** | T-agg "digit-soup" | T-agg "digit-soup" | T-iso accurate | **NT** | NT | NT |
| DocTR | T-agg mixed | T-iso worst-case on scan | **T-iso zero heading markup, every input** | T-agg (not isolated) | T-agg values correct, alignment breaks | **NT** | T-agg dropped/misread | T-agg dropped/misread | T-iso reasonable | **NT** | NT | NT |
| Kreuzberg | T-agg 95-99% | T-iso correct (no multi-col source) | T-iso good on native / **T-iso zero on scan** | T-agg (not isolated) | **T-iso 0 tables detected** | **NT** | T-agg positioned, no captions | T-agg image-only | T-iso good | **NT** | NT | NT |
| open-parse (base) | T-iso crash on complex doc | T-agg page-level ok | **T-iso zero headings** | T-agg (not isolated) | **T-iso scrambled/DEGRADED** | **NT** | T-agg no image path | T-agg no image path | **BLOCKED** (no OCR, silent) | **NT** | NT | NT |

*PaddleOCR-VL's S27 (T-agg) result is the counterintuitive one flagged in
the capability matrix — native-digital text showed more corruption than
the genuine scan, consistent with the pipeline rasterizing pages rather
than reading the text layer directly.

## Tools with documentation-only coverage (no tool in this group has been run by anyone)

huridocs (blocked here by lack of Docker, not by lack of capability — its
own docs claim coverage across all 12 scenarios); dots.ocr, MonkeyOCR,
Chandra, Surya, OCRFlux, Nanonets-OCR-s/docext, GLM-OCR, granite-docling-258M,
RAGFlow/DeepDoc, Chunkr, Marker (v2), olmOCR, pdf-craft — all **DOCUMENTED
only** uniformly across whatever scenarios their own capability claims
cover; see `Tool_Capability_Matrix.md` section D/E for the capability-level
detail (documentation doesn't distinguish scenario granularity any more
than it distinguishes capability granularity, so a per-scenario table for
these would just repeat "DOCUMENTED" 12 times per tool with no new
information).
