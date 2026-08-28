# Master Results — This Cycle's New Tools

Only tools actually executed this cycle appear with scores. PaddleOCR-VL
(attempted, blocked) and huridocs (prepared, not run) appear with a status
row and no scores — see their `observations.md` for the exact blocker
evidence. Scoring rubric: 0=missing/unusable, 1=very poor, 2=poor,
3=acceptable, 4=good, 5=excellent. Tables are further tagged **OMITTED**
(structurally absent) vs **DEGRADED** (present but broken).

## Kreuzberg (MIT, `kreuzberg==4.10.2`)

| PDF | Runtime | Text chars | Tables detected | Images extracted | Headings | Errors |
|---|---|---|---|---|---|---|
| PDF1 Hybrid Earnings (84pp) | 6.2s | 247,363 (98.7% of native) | 0 | 14 | 289× `###` (over-fragmented) | 26× "Empty page" warnings (benign) |
| PDF2 Financial Report (18pp) | 6.9s | 33,322 (95.3% of native) | 0 | 17 | heavy fragmentation, 0 real tables | none |
| PDF3 Scanned Research Paper (12pp) | 25.6s | 27,031 (OCR) | 0 | 0 | **0 headings at all** | Tesseract ObjectCache leak warnings (benign) |

| Criterion | PDF1 | PDF2 | PDF3 | Overall | Evidence |
|---|---|---|---|---|---|
| Chart Reconstruction | 2 | N/A | N/A | **2** | charts survive only as raster images, no data/description — `02_Tools/kreuzberg/observations.md#pdf-1` |
| Text Preservation | 4 | 4 | 4 | **4** | 95-99% char yield both native PDFs; good OCR with isolated misreads |
| Table Reconstruction | 1 (OMITTED) | 1 (OMITTED) | N/A | **1** | 0 tables detected on any PDF; 0-1 pipe chars total across all output |
| Document Hierarchy | 2 (over-fragmented) | 1 (over-fragmented) | 0 (none at all) | **1** | 289 H3s in PDF1; 0 headings in PDF3 |
| Image Retention | 3 | 3 | N/A (0 images) | **3** | correctly positioned, no captions |
| Reading Order | 4 | 4 | 4 | **4** | correct in all spot checks (no multi-column source to stress-test) |
| Caption/Figure Association | 2 | 2 | N/A | **2** | footnotes stay in place but undistinguished; no image captions |
| Long/Complex Doc Robustness | 3 | — | — | **3** | 84pp processed fully, no crash, same failure modes persist at scale |
| Bonus/Anomalous | — | — | — | **3** | opposite hierarchy failure modes (over- vs under-fragmentation) depending on native vs. OCR input; TATR table model silently no-ops |
| **Overall average** | | | | **≈2.7 / 5** | |

## open-parse (MIT, `openparse==0.7.0`, base mode — no `[ml]` extra)

| PDF | Runtime | Result | Notes |
|---|---|---|---|
| PDF1 Hybrid Earnings (84pp) | 5.6s | **CRASH — 0 output** | `UnidentifiedImageError` (Pillow), uncaught |
| PDF2 Financial Report (18pp) | 1.6s | OK, 37,952 chars, 18 nodes | table values present but scrambled, 0 headings |
| PDF3 Scanned Research Paper (12pp) | 2.3s | **0 chars — silent empty "success"** | no OCR in base mode |

| Criterion | PDF1 | PDF2 | PDF3 | Overall | Evidence |
|---|---|---|---|---|---|
| Chart Reconstruction | 0 (crashed) | N/A | N/A | **0** | only chart-bearing doc crashed outright |
| Text Preservation | 0 (crashed) | 3 | 0 (empty) | **1** | total loss on 2 of 3 docs |
| Table Reconstruction | 0 (crashed) | 1 (DEGRADED) | N/A | **1** | values present but column/row order scrambled, raw `<br>` leaks into "Markdown" |
| Document Hierarchy | — | 0 | 0 | **0** | zero Markdown headings on any output produced |
| Image Retention | 0 (crashed) | 1 | N/A | **1** | no distinct image extraction path found |
| Reading Order | — | 2 | N/A | **2** | page-level order fine; intra-page table order scrambled |
| Caption/Figure Association | — | 1 | N/A | **1** | notes stay near tables but unstructured |
| Long/Complex Doc Robustness | 0 (crashed) | — | — | **0** | hard crash on the longest/most complex benchmark PDF |
| Bonus/Anomalous | — | — | — | **1** | silent-empty "success" on the scanned PDF (no error signal); hidden tiktoken network dependency caused a multi-minute hang before a workaround was applied |
| **Overall average** | | | | **≈0.8 / 5** | |

## PaddleOCR-VL / PP-StructureV3 (Apache-2.0) — attempted, blocked

**Status: attempted-blocked.** Installed cleanly (`paddleocr[doc-parser]==3.7.0`).
0 of 3 PDFs could be tested — `PPStructureV3()` initialization fails with
`Exception: No available model hosting platforms detected` against both
its default (Hugging Face) and documented BOS-fallback model sources, both
blocked by this sandbox's network policy. No score assigned — this is an
environment blocker, not a tool-quality finding. See
`02_Tools/paddleocr-vl/observations.md` and `logs/init_attempt_*.log` for
exact evidence.

## huridocs/pdf-document-layout-analysis (Apache-2.0) — prepared, not run

**Status: prepared-not-run.** Docker-only distribution; this sandbox has
no Docker daemon. 0 of 3 PDFs tested. No score assigned. See
`02_Tools/huridocs-pdf-document-layout-analysis/observations.md`.

## How to read these scores against the prior cycle

This project did not have direct, evidence-based access to re-verify the
prior cycle's numeric scores for Docling/MinerU/Marker/etc. (they were not
re-run this cycle, by design — see duplicate-check rule). The scores above
are internally consistent and evidence-backed for the tools actually run
this cycle; do not treat the ≈2.7 and ≈0.8 overall averages as directly
comparable to a prior cycle's numbers unless that cycle's scoring rubric
and methodology are confirmed identical. `05_Final_Report/Final_Comparison.md`
discusses this explicitly.
