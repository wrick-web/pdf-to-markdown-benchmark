# Test Case Registry (TC27–TC38)

Source: ClickUp doc "PDF → Markdown — research design" (Rev 2, frozen
2026-08-23) — "Minimum fixture requirement" and "Expected behavior"
columns are copied verbatim from that spec, not redesigned. **Candidate
tools** and **Current status** are this repository's own tracking columns
(not part of the frozen spec) — do not read them as part of the frozen
taxonomy.

**Candidate tools** are the tools most plausibly able to exercise that
scenario based on documented capability (see `02_Tools/Tool_Capability_Matrix.md`
for full detail and DOCUMENTED/OBSERVED/TESTED/BLOCKED status per cell) —
listing a tool here is not a test result and does not mean it will
necessarily be run against every TC.

**Current status** for every TC below is **WAITING FOR INPUT**: fixture
authoring is a separate explicit step that has not started (begins only
on Pradip's go, per the frozen spec's "What comes next"), and the actual
input documents are expected from **Pruthviraj & Haresh** — not yet
received as of this writing. No test execution against these TCs has
happened or should be claimed until fixtures exist.

| TC | Capability · Scenario | Required fixture (verbatim from spec) | Expected behaviour (verbatim from spec) | Candidate tools | Current status |
|---|---|---|---|---|---|
| TC27 | C10 Text Fidelity · S27 ordinary digital text | A short digital-text PDF of plain paragraphs | All text is present and unchanged — nothing missing, garbled, or invented | All native-text-capable tools (essentially the whole roster — this is the floor every tool must clear) | WAITING FOR INPUT |
| TC28 | C11 Reading Order & Layout · S28 multiple columns | A short PDF page with two clear text columns | Text is emitted in the natural reading order without interleaving the columns | Layout-aware tools: Docling, MinerU, PaddleOCR-VL, MonkeyOCR, dots.ocr, huridocs, Kreuzberg (heuristic layout) | WAITING FOR INPUT |
| TC29 | C12 Heading & Section Structure · S29 styled headings | A short PDF with styled headings and subheadings over normal body text | Headings become Markdown headings with their hierarchy preserved — not plain or bold text | Docling, MinerU, Kreuzberg (font-metadata dependent — see known scanned-doc failure mode), PaddleOCR-VL, MonkeyOCR | WAITING FOR INPUT |
| TC30 | C12 Heading & Section Structure · S30 footnotes | A PDF page with body text referencing a footnote at the bottom of the page | The footnote text is kept out of the body flow, present, and associated with its reference | huridocs (explicit header/footer handling), Docling, RAGFlow/DeepDoc (explicit footer element type) | WAITING FOR INPUT |
| TC31 | C13 Table Extraction · S31 simple table | A small PDF containing one simple, clearly formatted table | The table is retained as a table with correct headers, rows, columns and values | PaddleOCR-VL, MinerU, Docling, MonkeyOCR, OCRFlux, huridocs, RAGFlow/DeepDoc; Kreuzberg and open-parse observed weak/failing here in prior (pre-Rev2) testing — see Tool_Capability_Matrix | WAITING FOR INPUT |
| TC32 | C13 Table Extraction · S32 cross-page table | A small PDF containing one simple table that starts on one page and continues onto the next | The complete table is retained with correct headers, rows, columns and values | OCRFlux (documented, purpose-built cross-page table/paragraph merging), MinerU, PaddleOCR-VL, Docling | WAITING FOR INPUT |
| TC33 | C14 Figures & Charts · S33 figure with caption | A PDF containing a figure with a caption in normal text | The image is preserved (embedded or referenced) at its position, with its caption | RAGFlow/DeepDoc (explicit figure-caption element type), Docling, huridocs, Kreuzberg (image extraction observed, captions not associated — see matrix) | WAITING FOR INPUT |
| TC34 | C14 Figures & Charts · S34 data chart | A PDF containing a data chart with a title | The chart is preserved as an image at its position with its title; any added textual data is recorded as enrichment, not required | Nanonets/docext (documented chart-to-Mermaid enrichment), dots.ocr (documented chart-to-SVG), Docling, Kreuzberg (image-only, no enrichment — observed) | WAITING FOR INPUT |
| TC35 | C15 Scanned Document OCR · S35 clean scan | A short, clearly scanned image-only PDF containing ordinary text | Visible text is recovered accurately | Kreuzberg (Tesseract, observed good quality in prior testing), PaddleOCR-VL, dots.ocr, MinerU, olmOCR, granite-docling, huridocs | WAITING FOR INPUT |
| TC36 | C15 Scanned Document OCR · S36 mixed pages | A digital PDF that includes one scanned image-only page | The scanned page's text appears in the output like the digital pages — not silently skipped | Kreuzberg (per-page OCR auto-detection observed working in prior testing), MinerU (documented auto-detects scanned/garbled pages), PaddleOCR-VL | WAITING FOR INPUT |
| TC37 | C16 Equations & Mathematical Notation · S37 equations | A PDF containing mathematical equations | Equations are emitted as math markup (LaTeX/MathML) or an honest fallback — not garbled prose | Docling, MinerU, PaddleOCR-VL, huridocs (LaTeX-OCR component), Chandra, Nanonets/docext, olmOCR, pdf-craft — all DOCUMENTED claims only, none observed/tested yet (new capability, not covered by the pre-Rev2 benchmark) | WAITING FOR INPUT |
| TC38 | C17 Code Extraction · S38 code block | A PDF containing a code block | The code is emitted as a preformatted/fenced block with line breaks and indentation intact | Docling (only tool with an explicit documented code-preservation claim found so far) — otherwise largely unknown/untested across the whole roster; see Tool_Capability_Matrix gap note | WAITING FOR INPUT |

## Reading this table honestly

- A tool appearing in "Candidate tools" reflects **documentation or prior
  (pre-Rev2) observation**, not a Rev-2 test result. Most rows — and all
  of TC37/TC38 — currently have **zero actually-observed evidence**; they
  are plausible-fit tools to prioritize once fixtures exist, nothing more.
- **C17 (Code Extraction) is the weakest-covered capability across the
  entire tool landscape researched so far.** Only Docling carries an
  explicit documented claim. This is flagged as a real gap, not
  papered over — see `02_Tools/Tool_Capability_Matrix.md`.
