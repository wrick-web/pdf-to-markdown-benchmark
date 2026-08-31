# Test Plan — Rev 2 (C10–C17 / TC27–TC38)

**No execution happens from this plan until fixtures exist** (see
`01_Benchmark_Design/Input_Status.md`). This is the plan to execute
immediately once they do, per core rule 4 (default pipeline, one pass,
record exact version) and rule 2 (one scenario, one focused verdict).

## Priority ranking

**Priority 1 — close the two real capability gaps (C16, C17).** Almost
nothing in the entire researched landscape has ever been tested for
equations or code (see `Tool_Capability_Matrix.md` closing section). Once
TC37/TC38 fixtures exist, run:
1. **Docling** — RE-TEST/RE-MAP (already installed, already tested for
   C10–C15 pre-Rev2; its own docs claim both formula and code
   preservation, making it the single tool with a documented claim on
   *both* of the weakest-covered capabilities — a natural first target).
2. **Kreuzberg** — RE-TEST/RE-MAP (already installed and working in this
   environment with zero GPU/HF dependency; no documented equation/code
   claim, so this specifically tests "does the default pipeline handle it
   gracefully or ignore it silently" rather than confirming a claim).
3. **PaddleOCR-VL / PP-StructureV3** — RE-TEST/RE-MAP, with
   `use_formula_recognition=True` this time (the prior cycle explicitly
   disabled it as out-of-scope for their inputs — TC37 is exactly the
   input that makes re-enabling it meaningful). Same Hugging Face/BOS
   access blocker noted before applies unless run outside this sandbox.
4. **huridocs/pdf-document-layout-analysis** — has a dedicated LaTeX-OCR
   component per its own docs; needs a machine with Docker.

**Priority 2 — strong documented table/OCR/layout capability with a
realistic path to actually running once fixtures exist:**
MinerU (RE-TEST/RE-MAP — already installed/tested pre-Rev2, strong
existing table/reading-order evidence), MonkeyOCR and OCRFlux (both
documented strong table claims, both need GPU+model access — evaluate
once the research-access outreach responses land, see
`06_Access_Outreach/`), RAGFlow/DeepDoc (documented explicit
figure-caption/table-caption element types — directly targets S33/TC33
better than anything else researched).

**Priority 3 — re-map existing pre-Rev2 evidence rather than re-running.**
Docling, PyMuPDF4LLM, LiteParse, doc2mark, MarkItDown, MinerU, PaddleOCR-VL,
Dolphin, Unstructured, DocTR, Kreuzberg, and open-parse all already have
real observed evidence for C10–C15 (see `Tool_Capability_Matrix.md`
section A/B). Once fixtures exist and expected source truth is recorded
(core rule 5), the fastest path to real TC27–TC36 coverage is checking
whether the *existing* pre-Rev2 outputs already answer a given TC
(core rule 11: one artifact can serve several test cases) before spending
a new run — but only where the existing document genuinely satisfies that
TC's minimum fixture requirement; this is a decision for the fixture-
authoring step, not assumed here.

## Per-tool technical requirements

| Tool | Deps | CPU/GPU | Docker | Internet/model DL | Native Markdown? | OCR | Table method | Chart/Image | Equation | Code |
|---|---|---|---|---|---|---|---|---|---|---|
| Docling | Python, pip | CPU or GPU | No | Yes, first run (HF) | Yes, native | Tesseract/EasyOCR/RapidOCR (pluggable) | TableFormer model | Image classification model; docs claim charts/formulas/code | LaTeX (documented) | Fenced blocks (documented) |
| Kreuzberg | Python, pip + system tesseract | CPU | No | No (ran fully offline) | Yes, native | Tesseract (used), also PaddleOCR-ONNX/Candle/VLM-router | TATR requested, 0 tables ever detected | Raster image extraction only | Not supported (no claim found) | Not supported (no claim found) |
| open-parse | Python, pip | CPU | No | No (base mode) | Chunk/node structure, markdown-ish | None in base mode | pdfminer heuristic (base) / unitable+HF (`[ml]` extra) | No dedicated path | Not supported | Not supported |
| PaddleOCR-VL/PP-StructureV3 | Python, pip (`paddleocr[doc-parser]`) | CPU or GPU | No | Yes, required (HF or BOS) — **blocked in this sandbox, both sources** | Yes, native | Built-in VLM-based | Native table element type | Real cropped image files kept; charts as images, no data | Built-in, explicitly disable-able | Not documented |
| huridocs/pdf-document-layout-analysis | Docker image only | CPU (LightGBM) or GPU (VGT) | **Yes, required — blocked in this sandbox (no daemon)** | Model weights noted as HF-hosted for some components | Yes, native (+HTML/JSON) | Tesseract, 150+ languages | RapidTable | Documented layout classes | LaTeX-OCR component (documented) | Not documented |
| MinerU | Python, pip/Docker | CPU or GPU | Optional | Yes, model download | Yes, native | Auto-detects scanned/garbled pages | Native table detection | Documented; observed dropping charts with extractable data | LaTeX (documented, "converts formulas to LaTeX") | Not documented |
| PyMuPDF4LLM | Python, pip | CPU only | No | No | Yes, native | None (no OCR) | PyMuPDF layout heuristic | Degrades to raw text; drops standalone images | Not supported | Not supported |
| LiteParse | Python, pip | CPU/GPU (OCR component) | No | Likely (OCR models) | Yes, native | Yes | Unclear method, degrades on complexity | Placeholder-based, unresolvable in test run | Not documented | Not documented |
| doc2mark | Python, pip | CPU | No | Needs external OpenAI API for OCR | Yes, native | **None standalone — requires external API, confirmed failed without it** | Inconsistent (flat/MD/HTML mixed) | Degrades to broken HTML | Not documented | Not documented |
| MarkItDown | Python, pip | CPU | No | Needs `llm_client`/OpenAI API for OCR | Yes, native | **None standalone — silently skips without config, confirmed failed** | Inconsistent | Degrades to jumbled numeric strings | Not documented | Not documented |
| Dolphin (v1.5) | Python, model weights | GPU preferred | No | Yes, model download | Yes, native | Yes (strong on scans) | Two-stage table/text/formula architecture | Charts uniformly omitted; has a mis-firing formula-recognition head | Architecture exists, never legitimately exercised | Not documented |
| Unstructured | Python, pip (`hi_res` strategy) | CPU/GPU | No | Likely (detection models) | Via `partition_pdf` elements | Yes | Detected but degrades with complexity | Chart labels OCR'd into "digit-soup" | Not documented | Not documented |
| DocTR | Python, pip (`det_arch`/`reco_arch`) | CPU/GPU | No | Yes, model download | **No — plain per-page text dump only, no Markdown/table/heading export** | Yes, core function | None — no table structure at all | None — no image/chart handling | Not documented | Not documented |
| dots.ocr | HF Transformers or vLLM | GPU (no confirmed CPU path) | Optional (vLLM server) | Yes, required (HF) | Yes, native + JSON | Built-in VLM | Documented | Chart→SVG (documented) | Not documented | Not documented |
| MonkeyOCR | Python, model weights | GPU (8GB+ quantized) | No | Yes, required (HF/ModelScope) | Yes, native | Built-in | SRR triplet architecture (documented strong) | Documented | Not documented | Not documented |
| Chandra | `pip install chandra-ocr` or vLLM | GPU (H100 in vendor benchmarks) | Optional | Yes, required (HF) | Yes, native/HTML/JSON | Built-in, 90+ languages | Documented complex-table support | Documented | Documented ("math") | Not documented |
| Surya (standalone) | `pip install surya-ocr` | GPU (vLLM) or CPU/Metal (llama.cpp) | No | Yes, required (HF) | No — JSON/HTML layout+OCR+table detail only, Marker does final MD | N/A (feeds Marker) | Documented table recognition | Not documented | Not documented | Not documented |
| OCRFlux | Conda + pinned CUDA 12.4 build | GPU (12GB+) | No | Yes, required (HF) | Yes, native | Built-in | Documented (TEDS 0.861); unique cross-page merging | Not documented | Not documented | Not documented |
| Nanonets-OCR-s/docext | `pip install -e .` | GPU | No | Yes, required (HF) | Yes, native | Built-in | Documented | Chart→Mermaid (documented) | LaTeX (documented) | Not documented |
| GLM-OCR | `pip install glmocr` | CPU (layout stage) + GPU (recognition) | Optional (vLLM/SGLang) | Yes, required (HF) | Yes, native + JSON | Built-in | Documented | Not documented | Not documented | Not documented |
| granite-docling-258M | ONNX/GGUF community builds, or HF | CPU-feasible (258M) | No | Yes, required (HF or Ollama registry) — **both blocked in this sandbox** | Via DocTags → MD/HTML/JSON | Built-in | Documented (replaces Docling's ensemble) | Documented | Not documented | Not documented |
| RAGFlow/DeepDoc | Python, part of RAGFlow | CPU/GPU unspecified | Optional (full platform is Docker-based) | Yes, required (HF) | Via structured chunks, not one-shot MD | Built-in | Documented, 5 cell-role labels | Explicit figure-caption/table-caption element types (documented) | Explicit "equation" element type (documented) | Not documented |
| Chunkr | Docker Compose | CPU/GPU/Mac-ARM profiles | **Yes, required — blocked in this sandbox (no daemon)** | Community/OSS models, unspecified source | Yes, native (+HTML) | Unspecified | Documented | Documented | Not documented | Not documented |
| Marker (v2) | `pip install marker-pdf` | GPU preferred, CPU possible | No | Yes, required (Surya 2 weights) | Yes, native | Yes (Surya-based) | Documented | Documented | Not documented (not found in this research) | Not documented |
| olmOCR | vLLM/SGLang | GPU | Optional | Yes, required (HF) | Yes, native (linearized text) | Built-in, strong on degraded scans | Documented ("tables") | Not documented | Documented ("equations" explicitly listed) | Not documented |
| pdf-craft | Python, DeepSeek OCR weights | GPU preferred | No | Yes, required | Yes, native (or EPUB) | Built-in (DeepSeek OCR) | Documented | Not documented | Documented ("formulas") | Not documented |

## Honest summary for planning purposes

Most of the tools that could plausibly close the C16/C17 gap need GPU and
Hugging Face Hub access this research sandbox does not have. The 8
research-access outreach emails already sent (`06_Access_Outreach/`)
directly target this — a positive response from Datalab (Surya/Chandra),
PaddlePaddle/Baidu, or IBM/Docling would be the fastest realistic path to
actually testing C16 with a tool that has a genuine documented claim,
rather than relying only on Docling and Kreuzberg (both already
CPU-runnable here, neither has a *documented* equation/code claim beyond
Docling's own).
