# New-Tools Comparison — This Cycle

## Tested with real evidence (executed against all 3 benchmark PDFs)

| | Kreuzberg | open-parse (base) |
|---|---|---|
| License | MIT | MIT |
| Setup difficulty | Low (1 pip install + 1 apt install) | Low, but hidden network dependency (tiktoken) needed a workaround |
| GPU/HF required | No | No (base mode) |
| Text preservation | 95-99% char yield, good OCR | Crashes on complex PDF, empty on scanned PDF |
| Tables | 0 tables on any PDF (OMITTED) | Present but scrambled (DEGRADED) on the 1 doc that ran |
| Charts | Raster image only | Crashed on the only chart-bearing doc |
| Hierarchy | Real but over/under-fragmented | None at all |
| OCR (scanned PDF) | Works well, auto-triggered | Not supported in base mode — silent empty output |
| Robustness (84pp doc) | Completed fully | Hard crash |
| **Overall score** | **≈2.7/5** | **≈0.8/5** |

**Verdict for this cycle's real testing:** Kreuzberg is the clear winner of
the two tools actually executed, and the one worth carrying forward as a
lightweight, dependency-free text/OCR extraction option — with the
explicit, evidence-backed caveat that it cannot be trusted for table
reconstruction in its current default configuration. open-parse (base
mode) is not a credible contender for this project's use case; it is only
useful as a very fast, simple-document baseline.

## Full landscape (including Tier B tools prepared but not run, and Tier C exclusions)

See `00_Project_Notes/Tool_Landscape.md` sections C-E for the complete
table with license/repo/blocker detail on all 22 new tools researched this
cycle (4 Tier A, 10 Tier B, 8 Tier C).

## What would likely change on an unrestricted machine

Every Tier B tool (dots.ocr, MonkeyOCR, Chandra, PaddleOCR-VL, GLM-OCR,
OCRFlux, Nanonets/docext, granite-docling-258M) is a modern VLM-based
document parser explicitly designed around unified layout+OCR+table
understanding, and each publishes benchmark numbers (OmniDocBench,
TableTEDS, etc.) claiming to substantially beat classical pipelines on
exactly the table/chart/layout criteria where Kreuzberg and open-parse
scored worst here. **None of those claims were independently re-verified
by this project** (they could not be executed in this sandbox) — they are
reported in `Tool_Landscape.md` as documentation claims, not observed
results, and should be treated with the same "verify, don't just believe
the docs" discipline applied everywhere else in this project once someone
runs them on a GPU machine with Hugging Face access.
