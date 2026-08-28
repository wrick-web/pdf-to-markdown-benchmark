# Kreuzberg — Observations

Repo: https://github.com/Goldziher/kreuzberg (rebranding to xberg-io/xberg) · PyPI `kreuzberg==4.10.2` · MIT · Rust core, Python bindings.

## Setup

Installation: `uv venv .venv_kreuzberg && uv pip install kreuzberg` (plain `pip install kreuzberg` also works). Clean, no build errors.
Version: 4.10.2 (PyPI, 2026-08-28)
Dependencies: system `tesseract-ocr` + `tesseract-ocr-eng` (apt) for the OCR backend used in this run; no other system deps needed.
GPU/CPU: CPU only, ran fine on 4 vCPU / 15GB RAM.
Model requirements: **none downloaded** for the configuration used (`layout=LayoutDetectionConfig(apply_heuristics=True, table_model="tatr")`, `ocr=OcrConfig(backend="tesseract")`) — ran fully offline in a sandbox with Hugging Face Hub blocked. Whether the TATR table model silently no-ops without downloaded weights, or genuinely ships bundled ONNX assets, could not be fully confirmed from inside this sandbox — flagged as a follow-up for a machine with HF access (see "Biggest limitation").
Setup difficulty: Low. One `pip install` + one `apt install`, ~2 minutes total.

Exact config used (`04_Scripts/conversion/run_kreuzberg.py`):
```python
kreuzberg.ExtractionConfig(
    output_format=kreuzberg.OutputFormat.MARKDOWN,
    ocr=kreuzberg.OcrConfig(backend="tesseract", language="eng"),
    pdf_options=kreuzberg.PdfConfig(extract_images=True),
    layout=kreuzberg.LayoutDetectionConfig(apply_heuristics=True, table_model="tatr"),
)
```

---

## PDF 1 — Hybrid Earnings Report (Target 2015 Annual Report, 84 pages)

### Text
**Documentation claim:** "clean, structured, RAG-friendly" Markdown extraction.
**Observed:** 247,363 characters extracted vs. 250,546 characters PyMuPDF finds natively in the same file (~98.7%) — text completeness is very good, no large blocks of missing narrative content found in spot checks (Item 1 Business, Item 1A Risk Factors, MD&A, and the signature/certifications section near the end all present and readable). Runtime logged 26 `Empty page!!` console warnings out of 84 pages during processing; these correspond to pages Tesseract found nothing to OCR on (consistent with an 84-page 10-K's genuine mostly-blank section-divider/blank-verso pages, given overall text yield stayed at 98.7% of native — not evidence of large-scale content loss, but not independently confirmed page-by-page either).

### Tables
**Documentation claim:** repo README lists "Layout & tables — ML layout models (PP-DocLayout-V3, RT-DETR) and table structure (TATR, SLANet) reconstruct reading order and cell grids for clean Markdown."
**Observed:** `n_tables_detected: 0` on all three benchmark PDFs, and the rendered Markdown contains only **1 pipe (`|`) character across the entire 1,725-line PDF1 output** — i.e., essentially zero real Markdown tables were produced anywhere, despite PDF1 containing multiple dense financial tables (Item 6 Selected Financial Data, Item 7 MD&A, Item 8 Financial Statements) with merged cells and multi-row headers. Table content is not silently dropped — the numbers and labels are present as flattened paragraph/heading text — but the row/column structure is **completely lost** (structurally, this is closer to OMITTED than DEGRADED: there is no table markup at all to call "degraded"). Example from the "Item 2. Properties" section: a location/square-footage table collapsed into the heading `### Total 1,792 239,539`, merging a table's total row into a spurious H3.

### Charts
**Documentation claim:** none specific to charts; general layout/image handling claimed.
**Observed:** Performance charts (bar/line charts in the "Financial Highlights"/MD&A sections) were not reconstructed as data or described in text — they were captured as raster images only (see Images below) with no chart-specific handling (no data table, no alt-text description of the chart's content).

### Images
**Documentation claim:** image extraction supported via `pdf_options.extract_images`.
**Observed:** 14 images extracted and saved to `extracted_images/PDF1_Hybrid_Earnings_Report_Target2015/` (PNG). Images are placed inline in the Markdown at roughly the right position in reading order (e.g., `![](image_0.png)` appears right after the relevant heading in the PDF2 run — same mechanism applies to PDF1). No captions are auto-associated with the images; the `![]()` alt text is always empty, so a reader gets no indication of what an embedded image is without opening it.

### Reading Order
**Observed:** Single-column body pages preserved correct top-to-bottom order in spot checks (cover page → letter to shareholders → Item 1 → Item 1A → ... → signatures). No multi-column layout in this particular filing to stress-test column-interleaving.

### Hierarchy
**Documentation claim:** implied by "clean, structured... Markdown" positioning.
**Observed:** Mixed. Genuine section markers (PART I/II/III/IV, "Item 1. Business", "Item 1A. Risk Factors", "TABLE OF CONTENTS") are correctly promoted to real Markdown headings (`###`). However, the heading-detection heuristic (font-size/boldness based, not semantic) also promotes many non-headings to H3 — e.g. `### If we are unable to positively differentiate ourselves from other retailers, our results of operations could be adversely affected.` (a full risk-factor sentence, not a title) and the table-row example above. Net effect: **289 total `###` headings detected in an 84-page document** — implausibly high for genuine section structure, confirming over-fragmentation rather than faithful hierarchy. Table-of-contents entries that spanned two lines in the source were also merged into single run-on headings, e.g. `### Item 6 Selected Financial Data 16 Item 7 Management's Discussion and Analysis of Financial Condition and Results of Operations`.

### Captions / Footnotes
**Observed:** Footnote markers and footnote text remain in the body text stream in their original reading position (not stripped), but are not visually or structurally distinguished from body text (no blockquote/footnote markdown convention applied).

### OCR / Scanned Page
**Observed:** The signature/certification pages (e.g. "Brian C. Cornell Chairman and Chief Executive Officer March 11, 2016 Catherine R. Smith Executive Vice President and Chief Financial Officer") came through as clean plain text in the output — this specific filing's signature page in the uploaded copy is a native, digitally-typed signature block (not a scanned image), so this did not exercise Kreuzberg's Tesseract OCR path; see PDF 3 for the dedicated OCR test.

### Errors / Artifacts
`Empty page!!` printed to stderr 26 times (harmless log noise, not a crash) — see Text section above.

---

## PDF 2 — Financial Report (Sumitomo Heavy Industries, 18 pages)

### Text
**Observed:** 33,322 characters extracted vs. 34,981 native (PyMuPDF) — ~95.3%, essentially complete. Run time 6.9s.

### Tables
**Documentation claim:** as above ("table structure... reconstruct... cell grids for clean Markdown").
**Observed:** **`n_tables_detected: 0`, 0 pipe characters anywhere in the output.** This is the clearest, worst-case table failure of the three PDFs, because PDF2 is almost entirely dense financial tables with multi-row/multi-level headers (Business Results, Financial Position, Dividends, Segment Information). Concretely, this is what the "First Quarter Results" table becomes:
> `(Units: millions of yen) **First Quarter January 1 to March 31, 2025 First Quarter January 1 to March 31, 2024** % change % change Net sales 241,536 (5.2) 254,811`
Six data points, two period labels, and a metric name are run together as one paragraph, with no row/column separation at all — a reader cannot recover which number belongs to which period without going back to the source PDF. This is a **DEGRADED-to-OMITTED** table failure (structure is not present in any recoverable form) on the single PDF where table fidelity matters most.

### Charts
**Observed:** No standalone charts in this document (Sumitomo's report is table/text only) — N/A for this PDF.

### Images
**Observed:** 17 images extracted (mostly small logos/letterhead graphics rasterized from the original, based on file sizes in `extracted_images/`).

### Reading Order
**Observed:** Correct top-to-bottom order maintained across the 18 pages; no column-interleaving issues (single-column financial-statement layout).

### Hierarchy
**Observed:** Same fragmentation pattern as PDF1 but worse relative to content density — because almost every line in this document is short, bold, tabular text, the heading heuristic fires constantly. Concrete example of sentence-level fragmentation (not table-related, pure heading over-triggering) from the cover section:
```
### CONSOLIDATED FINANCIAL REPORT
### For the Three
- **-**
### Month Period from January 1 to March 31, 2025
```
A single title, "CONSOLIDATED FINANCIAL REPORT For the Three-Month Period from January 1 to March 31, 2025," is split across 4 separate blocks (2 spurious headings, one broken into a false list item for the em-dash) purely because the source PDF wraps this text across multiple short lines. This is a real, reproducible Markdown-quality defect, not a one-off.

### Captions / Footnotes
**Observed:** "Note 1:", "Note:" style footnotes remain attached in-place after their referring table content, in correct reading order, but as plain paragraph text (not visually distinguished).

### OCR / Scanned Page
N/A — PDF2 has no scanned pages.

### Errors / Artifacts
None (clean run, 6.9s, no warnings).

---

## PDF 3 — Scanned Research Paper (image-only, 12 pages, 0 native text layer)

### Text
**Documentation claim:** Tesseract-backed OCR "on demand," 150+ languages (via the underlying engine).
**Observed:** OCR triggered automatically (no `force_ocr` flag needed — Kreuzberg correctly detected the page had no extractable text layer and fell back to OCR). 27,031 characters recovered in 25.6s for 12 pages. Overall text quality is **good** — full sentences of the abstract, body, and "PUBLICATIONS CITED" section are readable and substantively correct. Concrete OCR errors found on manual inspection: `contro\!` for "control" (the exclamation mark is a misread lowercase "l", and the literal backslash is a Markdown-escaping artifact of that misread character), and a garbled `wv"` sequence near a US Forest Service seal graphic on the last page. Overall character-level accuracy is high; these are minor, isolated defects, not pervasive garbling.

### Tables
**Observed:** No explicit data tables in this document to test (it is a short USDA research note, not a table-heavy document) — N/A.

### Charts
**Observed:** N/A — this specific research note does not contain charts (despite the general archetype description mentioning charts, this uploaded copy is primarily narrative + a references list).

### Images
**Observed:** `n_images_extracted: 0` — no images extracted from this PDF, consistent with it being a scanned/rasterized document where the whole page is one image (Kreuzberg treats the OCR'd page as text output, not as an extractable embedded "image" in the object sense) rather than a source with separately embedded figures.

### Reading Order
**Observed:** Correct front-to-back order maintained (title → author affiliations → abstract → body → summary → "PUBLICATIONS CITED" → back-matter about the Intermountain Station). This particular research note appears to be single-column in the scanned source (not the two-column academic layout the general archetype description implies), so **multi-column reading-order reconstruction was not meaningfully stress-tested by this specific file** — noted as a gap in this cycle's evidence, worth a follow-up test with a genuinely multi-column scanned source.

### Hierarchy
**Documentation claim:** implied general Markdown structuring.
**Observed:** **Zero Markdown headings (`#`/`##`/`###`) anywhere in the 621-line output**, even though the source clearly has section titles in all-caps ("ABSTRACT", "KEYWORDS", "SUMMARY", "PUBLICATIONS CITED"). This is because Kreuzberg's heading heuristic relies on font-size/boldness metadata from the PDF's text layer — OCR'd text from a scanned page has no such metadata, so section titles are indistinguishable from body text and all hierarchy is lost. This is a **stark, direct contrast with PDF1/PDF2** (native-text documents), where the same tool over-produces headings; on this scanned document it produces none at all. Confirms hierarchy quality is entirely dependent on whether the source PDF has a native text/font layer, not on the OCR text quality itself.

### Captions / Figure Association
**Observed:** No distinguishable figure captions recovered as such (this file's OCR'd text stream doesn't tag any image regions to associate captions with, consistent with 0 images extracted above).

### OCR / Scanned Page
See Text section — good overall accuracy, isolated character-level misreads, correctly auto-triggered without manual configuration.

### Errors / Artifacts
`ObjectCache` leak warnings printed to stderr on every Tesseract-backed run (`WARNING! LEAK! object ... still has count N`) — appears to be a benign internal Tesseract/Leptonica resource-tracking log message rather than a functional bug (output content was still correct and complete), but worth flagging as console noise a production pipeline would want to suppress.

---

## Overall

### What worked well
- Clean, fast, single-`pip install` setup with no Hugging Face/GPU dependency for the configuration tested — the standout practical advantage over almost every other new 2025-2026 candidate found this cycle.
- Strong raw text completeness on both native-text PDFs (95-99% of PyMuPDF's own extraction) and good OCR accuracy on the scanned PDF, fully automatic (no manual "this page needs OCR" flagging required).
- Genuine, correct section-heading promotion on well-structured native-text documents (10-K style Item/Part headers) when the source has real font/size signals to key off.
- Image extraction works and preserves in-place positioning.

### What failed
- **Table reconstruction is the tool's clearest weakness for this use case**: 0 of the many dense financial tables across all 3 PDFs were rendered as structured Markdown tables (0 pipe characters in 2 of 3 outputs, 1 stray pipe in the third) — this is disqualifying for the "financial report" and "hybrid earnings report" archetypes specifically, where table fidelity is a primary evaluation criterion.
- Heading detection over-fires badly on short/bold/tabular native-text content (289 H3s in an 84-page document; multi-line titles split into several spurious headings-plus-list-item fragments), and under-fires completely (zero headings) on OCR'd/scanned content because it depends on font metadata that OCR can't supply.

### Unexpected behaviour
- The same tool produces *opposite* hierarchy failure modes depending on input type: over-fragmentation on native-text PDFs vs. zero structure on scanned PDFs — worth remembering when interpreting "hierarchy" scores as a single number.
- Requesting the TATR table model (`table_model="tatr"`) neither errored nor produced any tables — behaves as a silent no-op in this sandbox rather than a hard failure, which could mislead a user into thinking table detection ran when it effectively didn't (undetermined whether this is because required weights weren't fetched, or because TATR genuinely found no qualifying table regions in these three documents).

### Missing content
- No table structure, anywhere, on any of the 3 PDFs (see Tables sections above) — this is the single biggest content-fidelity gap.
- No chart-specific handling (charts survive only as flat raster images with no data/description).

### Manual cleanup
A user taking this output as-is would need to manually rebuild every financial table by hand from the flattened text, and manually demote/merge roughly a third of the H3 headings on native-text documents back into body paragraphs.

### Best use case
Fast, dependency-light bulk text/OCR extraction of narrative-heavy or single-column documents where table fidelity is not the primary need — e.g., feeding long-form report narrative sections into a RAG index, or getting a first-pass readable transcript of a scanned document.

### Biggest limitation
No usable table reconstruction on any of the three benchmark documents, despite table structure preservation being one of this project's core evaluation criteria and a headline claim in Kreuzberg's own documentation ("table structure... reconstruct... cell grids"). Whether this is fixable by supplying TATR's real model weights (blocked by Hugging Face access in this sandbox) is an open, flagged question for re-testing on an internet-unrestricted machine.

### Evidence
- Markdown outputs: `markdown_output/PDF1_Hybrid_Earnings_Report_Target2015.md`, `PDF2_Financial_Report_Sumitomo.md`, `PDF3_Scanned_Research_Paper.md`
- Structured metadata/timing/warnings: `raw_output/*.json`
- Run logs: `logs/*.log`
- Extracted images: `extracted_images/<pdf_stem>/`
