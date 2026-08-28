# Tier B tools — researched and script-prepared, not executed in this sandbox

All 10 tools below were independently verified this cycle (license, repo,
last update — checked against raw `LICENSE` files on
`raw.githubusercontent.com` where reachable, not marketing pages). None
could be executed end-to-end in this project's sandbox because every one
of them needs **Hugging Face Hub** (blocked here) and most also need a
**GPU** (none available here — 4 vCPU/15GB RAM, CPU-only). Each file below
gives the exact install/run commands so the user can reproduce them on a
machine with normal internet access and, where noted, a GPU — as part of
the final screen recording or a later cycle.

| File | Tool | License | Needs |
|---|---|---|---|
| `dots-ocr.md` | dots.ocr (rednote-hilab) | MIT | GPU + HF |
| `monkeyocr.md` | MonkeyOCR (Yuliang-Liu) | Apache-2.0 | GPU + HF/ModelScope |
| `chandra.md` | Chandra (Datalab) | Apache-2.0 code / OpenRAIL-M weights | GPU + HF; commercial-use license caveat |
| `surya.md` | Surya (datalab-to, standalone) | Apache-2.0 code / OpenRAIL-M weights | HF; CPU possible via llama.cpp |
| `ocrflux.md` | OCRFlux (chatdoc-com) | Apache-2.0 | GPU (12GB+) + HF |
| `nanonets-docext.md` | Nanonets-OCR-s / docext | Apache-2.0 | GPU + HF |
| `glm-ocr.md` | GLM-OCR (zai-org) | Apache-2.0 | HF; layout stage CPU-capable |
| `granite-docling.md` | granite-docling-258M (IBM) | Apache-2.0 | HF/Ollama registry only (compute-wise CPU-feasible) |
| `ragflow-deepdoc.md` | RAGFlow / DeepDoc (infiniflow) | Apache-2.0 | HF |
| `chunkr.md` | Chunkr (lumina-ai-inc) | AGPL-3.0 | Docker daemon (unavailable here) |

See `00_Project_Notes/Tool_Landscape.md` section D for the comparison
table and section E for Tier C tools that were verified and explicitly
excluded (not just deferred).
