# Final Comparison — PDF to Markdown, Open-Source (New-Tool Cycle)

## 1. Executive Summary

This cycle searched broadly for open-source PDF-to-Markdown tools beyond
what earlier cycles already tested/excluded, verified 22 new candidates
against primary sources (license files, not marketing pages), and actually
executed the two that could run in this project's CPU-only, no-GPU,
no-Hugging-Face-Hub, no-Docker-daemon sandbox — **Kreuzberg** and
**open-parse** — against the same 3 benchmark PDFs used throughout this
whole project. Kreuzberg is the clear winner of the two (≈2.7/5 overall),
strong on text/OCR completeness and setup simplicity, but with a
disqualifying weakness for this specific use case: **zero usable table
reconstruction on any of the 3 benchmark documents.** open-parse (base
mode, ≈0.8/5) crashed on the most complex benchmark PDF and produced no
usable output on the scanned one — it is documented here as a lightweight
native-text baseline, not a contender. A further 12 tools (PaddleOCR-VL,
huridocs, and 10 modern VLM-based parsers) were fully researched and
script-prepared but could not be executed in this sandbox — see section 17.

## 2. Problem Definition

See the ClickUp parent task (`86ban5kjq`) / `00_Project_Notes/README.md`
for the full use-case brief: convert complex PDFs (native text + scanned
pages + complex tables + charts + images + multi-column layout) into
clean Markdown, using a self-hosted, open-source library — not a
commodity text extractor, not a hosted API.

## 3. What IS included

Open-source, self-hostable PDF-to-Markdown tools/pipelines not already
tested or excluded by an earlier cycle. See `00_Project_Notes/Tool_Landscape.md`.

## 4. What is NOT included

Hosted SaaS/API-only tools (Zerox — confirmed no local model option),
pure document-VQA models (mPLUG-DocOwl2), tools without native PDF support
(oar-ocr), tools with no public code (LOCR), tools that are explicitly
duplicative of an already-tested tool by the project's own admission
(PDF-Extract-Kit vs. MinerU). See `00_Project_Notes/Decisions_and_Exclusions.md`.

## 5. Benchmark Inputs

The same 3 PDFs used throughout this whole project (uploaded directly by
the user this cycle, since their original hosts and the ClickUp attachment
CDN are blocked by this sandbox's egress policy):
- PDF1: Hybrid Earnings Report (Target 2015 Annual Report, 84pp, native text)
- PDF2: Financial Report (Sumitomo Heavy Industries, 18pp, native text, dense tables)
- PDF3: Scanned Research Paper (12pp, confirmed 0 native text — pure OCR test)

See `00_Project_Notes/Methodology.md` for verification details.

## 6. Methodology

Scripted, reproducible pipeline per tool per PDF: install -> configure ->
run -> save raw JSON + Markdown + images + logs -> manual read-through
against the source PDF -> qualitative observations -> 0-5 scoring per
criterion. Full detail in `00_Project_Notes/Methodology.md`.

## 7. New Tools (this cycle)

22 verified: 4 Tier A (Kreuzberg, open-parse, PaddleOCR-VL, huridocs),
10 Tier B (dots.ocr, MonkeyOCR, Chandra, Surya, OCRFlux, Nanonets/docext,
GLM-OCR, granite-docling-258M, RAGFlow/DeepDoc, Chunkr), 8 Tier C
(excluded, confirmed reasons). Full detail in `00_Project_Notes/Tool_Landscape.md`
and `00_Project_Notes/Research_Notes.md`.

## 8. Setup

Kreuzberg: `pip install kreuzberg` + `apt install tesseract-ocr` — ~2
minutes, no GPU/HF needed. open-parse: `pip install openparse` (base mode)
— fast, but required a documented workaround for a hidden tiktoken network
dependency (see `02_Tools/open-parse/observations.md`). PaddleOCR-VL:
installs cleanly, blocked at first model-load (evidence in
`02_Tools/paddleocr-vl/logs/`). huridocs: Docker-only, no daemon available
here.

## 9. Benchmark Results

See `03_Benchmark_Results/MASTER_RESULTS.md` for the full per-PDF,
per-criterion table.

## 10. Observations

See `02_Tools/kreuzberg/observations.md` and `02_Tools/open-parse/observations.md`
for the complete, evidence-quoted qualitative findings, and
`03_Benchmark_Results/Evidence/` for standalone excerpt files.

## 11. Scorecard

| Tool | Chart | Text | Table | Hierarchy | Image | Reading Order | Captions | Robustness | Bonus | **Overall** |
|---|---|---|---|---|---|---|---|---|---|---|
| Kreuzberg | 2 | 4 | 1 (OMITTED) | 1 | 3 | 4 | 2 | 3 | 3 | **2.7** |
| open-parse (base) | 0 | 1 | 1 (DEGRADED) | 0 | 1 | 2 | 1 | 0 | 1 | **0.8** |

## 12. Overall Ranking (this cycle's tested tools)

1. **Kreuzberg** — only tool with a coherent, complete pass across all 3
   PDFs; strong text/OCR, weak-to-absent tables/hierarchy/charts.
2. **open-parse (base mode)** — usable only as a fallback for the single
   simplest, cleanest, native-text, non-scanned, chart-free document type.

(PaddleOCR-VL and huridocs are not ranked — they were not executed here;
see sections 8-9 and 17.)

## 13. Strengths

Kreuzberg: dependency-light, fast, fully automatic OCR fallback, correct
image positioning, genuinely good heading detection *when* a native text
layer with font metadata exists. open-parse: fastest of the two when it
works, zero ML dependency footprint in base mode.

## 14. Weaknesses

Kreuzberg: 0 usable tables on any of 3 benchmark PDFs (this project's core
evaluation criterion), heading detection badly over/under-fires depending
on input type, no chart data extraction. open-parse: crashes on complex
PDFs, zero heading support, zero OCR/scanned-page support, table cell
order can be actively scrambled (not just flattened), and a hidden
internet dependency for basic operation.

## 15. Best Tool by Category (this cycle's evidence only)

- **Best OCR (of tools tested this cycle):** Kreuzberg — the only one with
  any OCR capability at all; open-parse has none in base mode.
- **Best Tables:** Neither — both failed this criterion (OMITTED for
  Kreuzberg, DEGRADED for open-parse). On paper, PaddleOCR-VL, MonkeyOCR,
  and OCRFlux (all Tier B, unverified here) claim the strongest documented
  table fidelity of everything researched this cycle.
- **Best Charts:** Neither tested tool handles charts meaningfully.
  Nanonets/docext's Mermaid-diagram approach is the most interesting
  documented (unverified) approach found.
- **Best Images:** Kreuzberg (correct in-place extraction and positioning;
  open-parse has no distinct image-export path).
- **Best Reading Order:** Kreuzberg (correct in all spot checks; open-parse
  scrambles intra-page table order).
- **Best Lightweight:** open-parse base mode, for the narrow case of a
  clean, native-text-only, chart-free, non-scanned PDF — with the caveat
  that it crashes outside that narrow case.
- **Best RAG/LLM suitability:** Kreuzberg — clean Markdown text stream,
  works fully offline, no vendor API dependency; the missing tables would
  still need a separate extraction step before RAG ingestion.
- **Best All-Rounder (this cycle):** Kreuzberg.

## 16. Recommended Pipeline

For this specific use case today, **no single tool tested this cycle is
sufficient on its own** given the hard requirement for table fidelity. A
realistic pipeline: Kreuzberg for text/OCR/heading/image extraction,
combined with a dedicated table extractor for the table regions (outside
this cycle's scope to build) — or, better, re-test PaddleOCR-VL,
MonkeyOCR, or OCRFlux on a GPU/internet-unrestricted machine, since each
explicitly targets end-to-end layout+OCR+table+chart understanding in one
model. See `05_Final_Report/Recommendations.md`.

## 17. Limitations

This sandbox has no GPU, no Docker daemon, and blocks Hugging Face Hub /
ModelScope / Ollama registry / Baidu Object Storage / arXiv / archive.org
at the network layer (confirmed via direct tests, not assumed). This
stopped 12 of the 22 new tools found from being executed at all. Every one
of them is fully researched, license-verified, and script-prepared in
`02_Tools/_prepared_not_run/` and `02_Tools/paddleocr-vl/` /
`02_Tools/huridocs-pdf-document-layout-analysis/` for the user to run on
an unrestricted machine. Scores in this report should not be read as "the
best open-source tools score this low" — they reflect only the two tools
that could actually be executed here.

## 18. Reproducibility

See `05_Final_Report/Reproducibility_Guide.md`.

## 19. Excluded Tools

See `00_Project_Notes/Decisions_and_Exclusions.md` for the full list with
reasons (both already-excluded-prior-cycle and this cycle's 8 Tier C
tools).
