# Tool Capability Matrix (mapped to C10–C17)

Every cell is one of:
- **TESTED** — actually run and observed (this repository or a prior
  cycle's own hands-on testing), with a one-line qualifier. All current
  TESTED entries are **pre-Rev2**: real observed evidence, but against
  the old 3-PDF/9-criteria benchmark design, not against TC27–TC38
  fixtures/grading. Treat as prior evidence to re-map, not a Rev-2 result.
- **DOCUMENTED** — a vendor/project claim only, never run by anyone in
  this research. Never treated as a test result.
- **NOT TESTED** — no evidence either way (not claimed, not run).
- **BLOCKED** — attempted, could not complete, with the specific reason
  (never scored as 0, per core rule 9).
- **N/A** — capability doesn't apply to this tool's design.

Source for the 10 pre-Rev2 "already tested" tools: the original ClickUp
task records for each (`Test Inputs & Artifact Creation` subtasks),
read in full for this update. Source for Kreuzberg/open-parse/PaddleOCR-VL/
huridocs: this repository's own `02_Tools/<tool>/observations.md`. Source
for all DOCUMENTED-only tools: `00_Project_Notes/Tool_Landscape.md` /
`Research_Notes.md`, themselves checked against each project's own repo.

## A. Already tested — prior cycle (pre-Rev2, real observed evidence)

| Tool | C10 Text Fidelity | C11 Reading Order | C12 Headings | C13 Tables | C14 Figures/Charts | C15 Scanned OCR | C16 Equations | C17 Code |
|---|---|---|---|---|---|---|---|---|
| Docling | TESTED — accurate, minor cell-spacing/word-merge issues | TESTED — mostly coherent, one column-merge defect | TESTED — clean H2/H3 hierarchy, consistent | TESTED — high fidelity simple tables; multi-level headers duplicate/flatten; one complex table severely garbled | TESTED — **charts/images uniformly omitted on every input**, `<!-- image -->` placeholder only | TESTED — accurate, minor word-merging + injected stamp artifacts | NOT TESTED (no equation content in the 3 test PDFs) | NOT TESTED (no code content in the 3 test PDFs) |
| PyMuPDF4LLM | TESTED — accurate on simple docs; major silent omissions on the dense financial report | TESTED — correct on simple docs; TOC lost + column interleaving on the financial report | TESTED — correct H2–H6 on simple docs; degraded on the financial report | TESTED — preserved on simple docs; **completely omitted/garbled** on the financial report | TESTED — degraded to raw text in comment blocks; standalone images silently dropped, no placeholder | TESTED — OCR'd but spelling errors + severe column interleaving | NOT TESTED | NOT TESTED |
| LiteParse | TESTED — clean on 2 of 3; OCR substitutions/word-splitting on the scan | TESTED — correct on 2 of 3; one fragmentation on the scan | TESTED — consistent on 2 of 3; title fragmented, headers left plain on the scan | TESTED — degraded on all 3 (flattened/misaligned; one table fails to form at all) | TESTED — one chart placeholder+data survives; images retained as unresolvable placeholders; dropped entirely on the scan | TESTED — OCR garbling, character substitutions confirmed | NOT TESTED | NOT TESTED |
| doc2mark | TESTED — accurate on 2 digital docs; **zero output (0-byte file)** on the scan | TESTED (digital docs only) — degraded on a 2-column letter | TESTED (digital docs only) — degraded, inconsistent levels on one doc | TESTED (digital docs only) — inconsistent, mixes flat/Markdown/HTML arbitrarily | TESTED (digital docs only) — degraded to broken HTML/fragments; images omitted, no placeholder | **BLOCKED/FAILED** — confirmed no standalone OCR support (needs external OpenAI API, out of open-source scope); 0-byte output | NOT TESTED | NOT TESTED |
| MarkItDown | TESTED — accurate on 2 digital docs; **zero output (0-byte file)** on the scan | TESTED (digital docs only) — degraded (2-col merge into jumbled table) on one doc | TESTED (digital docs only) — **zero heading levels generated on either digital doc** | TESTED (digital docs only) — inconsistent, some valid/some plain/misaligned | TESTED (digital docs only) — degraded to jumbled numeric strings; images omitted entirely | **BLOCKED/FAILED** — no standalone OCR; silently skips without an `llm_client` configured, 0-byte output, no error surfaced | NOT TESTED | NOT TESTED |
| MinerU | TESTED — complete narrative on all 3, but pervasive recoverable mojibake; signature graphic OCR'd into invented text on one doc | TESTED — no defect found on any of the 3 | TESTED — correct on all 3; one TOC page (itself table-shaped) breaks down | TESTED — simple tables correct on all 3; complex/borderless/wide tables show row-cascade drift or column collapse | TESTED — charts dropped (captions survive only) on one doc despite extractable data; correctly kept as captioned image refs on the scan | TESTED — complete/accurate; superscript footnote markers misread; two dense tables show density-linked failures | NOT TESTED | NOT TESTED |
| PaddleOCR-VL / PP-StructureV3 | TESTED — **counterintuitive finding: native-digital pages showed MORE OCR-style corruption than the genuine scan**, consistent with rasterizing pages rather than reading the text layer | TESTED — mostly correct; one column-interleaving defect, one paragraph-boundary loss | TESTED — inconsistent heading-level application (same style gets 3 different treatments) | TESTED — correct values in the large majority of cells; structural issues scale with table complexity | TESTED — **charts retained as real cropped image files** (not placeholders), but zero chart data ever recovered | TESTED — genuine scan OCR'd well, main defect is dropped spacing not dropped words | **explicitly disabled by the tester** (`use_formula_recognition=False`) — not exercised, not "not tested" by omission | NOT TESTED |
| Dolphin (v1.5, 0.3B) | TESTED — accurate prose; systematic "—"→"â" mojibake on 2 of 3 docs; checkbox states (☒/☐) both misread identically | TESTED — preserved on all 3, including a genuine 2-column stitch | TESTED — preserved on 2 of 3; degraded on the financial report (repeating header inconsistently classified) | TESTED — degraded on all 3 — wrapped-label row cascades, header-merge/undercounting tied to structural complexity | TESTED — charts uniformly omitted even with extractable bar values; **hand-written signature misclassified as formula, rendered as fabricated LaTeX (`$$ \pi $$`, `$$ \sim $$`)** | TESTED — strong prose-level OCR; one complex 12-column table breaks down | **Incidental only** — no genuine equations existed; the tool's formula-recognition head mis-fired on a signature, confirming a formula pathway exists but it was never legitimately exercised | NOT TESTED |
| Unstructured | TESTED — accurate, incl. exact checkbox reproduction; one OCR misread (superscript "²"→"?") | TESTED — preserved on all 3, incl. correct 2-column linearization on the scan | TESTED — headings detected but **nesting flattened to one level** on all 3 | TESTED — degraded on all 3 (dropped rows/columns, one severely garbled table) | TESTED — charts never converted/cleanly dropped; chart labels OCR'd character-by-character into "digit-soup" | TESTED — accurate at word level; one chart region becomes pure OCR noise | NOT TESTED | NOT TESTED |
| DocTR | TESTED — digits/figures reliably correct; letter-level substitutions in prose; scanned-OCR digit/letter confusions | TESTED — degraded (2-col "zippered" line-by-line) on one doc; preserved on another; **severely degraded** (worst case found) on the scan | **TESTED — zero heading markup on every input; hard tool ceiling** (plain per-page text dump, no Markdown export at all) | TESTED — numeric values generally correct; blank/dash cells have no placeholder, silently breaking column alignment | TESTED — never reconstructed; labels dropped/misread | TESTED — reasonable recognition; worst reading-order/heading collapse of any tool tested | NOT TESTED | NOT TESTED |

**Status label correction from this repository's own prior work:** the
Cycle-II research notes previously described "PaddleOCR-VL / PP-StructureV3"
as a newly-identified Tier A candidate that was installed but blocked at
model-download time in this sandbox. Reading the actual prior-cycle
ClickUp record for the first time (above) shows the earlier research team
**already tested this exact pipeline** (with real observed results, formula/
chart recognition explicitly disabled as out-of-scope for their inputs).
**This is a duplicate, not a new candidate** — see
`00_Project_Notes/Decisions_and_Exclusions.md` for the correction. This
repository's own blocked run is kept as a record of what happens in a
network-restricted environment, relabeled **RE-TEST attempt (blocked)**,
not a first test.

## B. Tested this cycle (pre-Rev2, this repository's own runs)

| Tool | C10 Text Fidelity | C11 Reading Order | C12 Headings | C13 Tables | C14 Figures/Charts | C15 Scanned OCR | C16 Equations | C17 Code |
|---|---|---|---|---|---|---|---|---|
| Kreuzberg | TESTED — 95–99% of native char count recovered; good OCR with isolated misreads | TESTED — correct in all spot checks | TESTED — real headings on native-text docs but badly over-fragmented (289 H3s/84pp); **zero headings at all on the scanned doc** | TESTED — **0 tables detected on any of 3 PDFs**, values flattened to plain text (OMITTED) | TESTED — images extracted, correctly positioned, no captions; charts retained only as raster images | TESTED — auto-triggered, good quality, isolated misreads | NOT TESTED (no equation content in the 3 test PDFs) | NOT TESTED (no code content in the 3 test PDFs) |
| open-parse (base mode) | TESTED — crashed (0 output) on the complex doc; OK on the simple doc; 0 chars on the scan | TESTED — page-level order fine; intra-page table order scrambled | TESTED — **zero headings on any output produced** | TESTED — present but actively scrambled column/value order (DEGRADED); raw HTML leaks into output | TESTED — no dedicated image-export path found | **BLOCKED/no capability** — no OCR in base mode, silent empty output on the scan | NOT TESTED | NOT TESTED |

## C. Attempted, blocked by this sandbox's infrastructure (not tool failure)

| Tool | Reason blocked | What's known (documented only) |
|---|---|---|
| huridocs/pdf-document-layout-analysis | No Docker daemon in this research sandbox | DOCUMENTED: dedicated layout+OCR+table pipeline, LaTeX-OCR component for C16, header/footer handling relevant to C12/S30 |

## D. Tier B — researched, script-prepared, never run by anyone (DOCUMENTED claims only)

| Tool | C10 | C11 | C12 | C13 | C14 | C15 | C16 | C17 |
|---|---|---|---|---|---|---|---|---|
| dots.ocr | DOCUMENTED | DOCUMENTED | DOCUMENTED | DOCUMENTED | DOCUMENTED (chart→SVG) | DOCUMENTED | NOT TESTED — no documented claim found | NOT TESTED |
| MonkeyOCR | DOCUMENTED | DOCUMENTED | DOCUMENTED | DOCUMENTED (TableTEDS 76.5–87.5% claimed) | DOCUMENTED | DOCUMENTED | NOT TESTED — no documented claim found | NOT TESTED |
| Chandra | DOCUMENTED | DOCUMENTED | DOCUMENTED | DOCUMENTED (complex tables) | DOCUMENTED | DOCUMENTED (90+ languages) | DOCUMENTED ("math") | NOT TESTED — no documented claim found |
| Surya (standalone) | DOCUMENTED | DOCUMENTED (layout engine) | N/A — component engine, no full Markdown assembly of its own | DOCUMENTED | NOT TESTED | DOCUMENTED | NOT TESTED | NOT TESTED |
| OCRFlux | DOCUMENTED | DOCUMENTED | DOCUMENTED | DOCUMENTED (unique cross-page table merging, TEDS 0.861 claimed) | NOT TESTED | DOCUMENTED | NOT TESTED — no documented claim found | NOT TESTED |
| Nanonets-OCR-s / docext | DOCUMENTED | DOCUMENTED | DOCUMENTED | DOCUMENTED | DOCUMENTED (chart→Mermaid) | DOCUMENTED | DOCUMENTED ("LaTeX equations" explicitly listed) | NOT TESTED — no documented claim found |
| GLM-OCR | DOCUMENTED | DOCUMENTED (layout stage) | DOCUMENTED | DOCUMENTED | NOT TESTED | DOCUMENTED | NOT TESTED — no documented claim found | NOT TESTED |
| granite-docling-258M | DOCUMENTED | DOCUMENTED | DOCUMENTED | DOCUMENTED | DOCUMENTED | DOCUMENTED | NOT TESTED — no documented claim found | NOT TESTED |
| RAGFlow / DeepDoc | DOCUMENTED | DOCUMENTED (10-element layout classes) | DOCUMENTED (explicit header/footer element types) | DOCUMENTED | DOCUMENTED (explicit figure-caption/table-caption element types) | DOCUMENTED | DOCUMENTED (explicit "equation" element type) | NOT TESTED — no documented claim found |
| Chunkr | DOCUMENTED | DOCUMENTED | DOCUMENTED | DOCUMENTED | DOCUMENTED | NOT TESTED | NOT TESTED — no documented claim found | NOT TESTED |

## E. Known but never benchmarked by anyone (real gap, carried from an earlier cycle)

| Tool | C10 | C11 | C12 | C13 | C14 | C15 | C16 | C17 |
|---|---|---|---|---|---|---|---|---|
| Marker (now v2, 2026-07-20 rewrite) | DOCUMENTED | DOCUMENTED | DOCUMENTED | DOCUMENTED | DOCUMENTED | DOCUMENTED | NOT TESTED — no documented claim found | NOT TESTED |
| olmOCR | DOCUMENTED | DOCUMENTED | DOCUMENTED | DOCUMENTED ("lists" mentioned) | NOT TESTED | DOCUMENTED (strong on scanned/degraded docs) | DOCUMENTED ("equations" explicitly listed in original claim) | NOT TESTED |
| pdf-craft | DOCUMENTED | NOT TESTED | DOCUMENTED (footnotes) | DOCUMENTED | NOT TESTED | DOCUMENTED (DeepSeek OCR based) | DOCUMENTED ("formulas") | NOT TESTED |

## F. Excluded — not mapped to capabilities (out of scope, see Decisions_and_Exclusions.md)

GROBID, Nougat, Tesseract (standalone), PDFPlumber, Camelot, Tabula,
OCRmyPDF, Zerox, GOT-OCR2.0, mPLUG-DocOwl2, Kosmos-2.5, PDF-Extract-Kit,
LOCR, Extractous, oar-ocr.

---

## What this matrix says about C16/C17 coverage right now

**C16 (Equations) and C17 (Code) are the two least-covered capabilities
in the entire tool landscape researched across every cycle so far.**

- **C16:** documented claims exist for Docling, MinerU, PaddleOCR-VL,
  huridocs (LaTeX-OCR component), Chandra, Nanonets/docext, RAGFlow/DeepDoc,
  olmOCR, pdf-craft — **none of these claims have ever actually been
  tested**, because no test document in any prior cycle contained real
  equation content (Dolphin's one incidental, non-representative
  misfire is the closest thing to observed evidence, and it's a failure
  mode, not a success).
- **C17 (Code):** only Docling carries even a documented claim
  ("preserves ... code"). No other tool researched across any cycle — not
  even a documentation-only claim — was found to address code-block
  preservation specifically. This is the single biggest blind spot in the
  tool landscape as currently understood.

This is exactly why TC37 and TC38 matter: they're the two test cases with
essentially zero real evidence behind any tool's readiness, and fixture
availability for them should be treated as high-priority once authoring
starts.
