# Research Notes — Raw Discovery Pass

This is the full raw output of the Phase 1 discovery pass (a dedicated
research pass over GitHub/PyPI/web coverage of 2025-2026 document-AI
releases, cross-checked against the existing ClickUp task's already-
tested/known/excluded lists to avoid duplication). `Tool_Landscape.md` is
the curated, normalized version of this material or organized into the
project's Tier A/B/C register — read that first for the working
reference; this file is kept for full traceability of how each
license/repo/date claim was sourced.

**Methodology used for this pass:** GitHub's REST API was not usable for
arbitrary third-party repos from this project's authenticated session
(scoped to the project's own repo only), so repo facts were gathered via
(a) direct fetch of `raw.githubusercontent.com/<repo>/<branch>/LICENSE`
files — authoritative, used wherever possible — and (b) web search /
page-summary fetches of the public GitHub HTML pages — best-effort,
occasionally imprecise on exact star counts/dates, flagged inline where
unconfirmed. `huggingface.co`, `arxiv.org`, and `archive.org` were
confirmed unreachable from this environment throughout.

---

## Tier A candidates (strong fit, realistically installable CPU-only / no-HF sandbox)

### 1. PaddleOCR-VL / PP-StructureV3 (PaddlePaddle / Baidu)
- Repo: https://github.com/PaddlePaddle/PaddleOCR (docs: `docs/version3.x/pipeline_usage/PaddleOCR-VL.md`) — same repo as the already-tested bare "PaddleOCR," but a genuinely distinct pipeline.
- License: Apache-2.0 (confirmed from repo's raw `LICENSE`).
- Latest update: PaddleOCR 3.0 shipped 2025-05-20; PaddleOCR-VL-1.6 (0.9B) is a more recent point release claiming 96.3% on OmniDocBench v1.6.
- Language: Python. Install: `pip install "paddleocr[doc-parser]"`.
- Distinctness from already-tested PaddleOCR: base PaddleOCR/PP-OCR is a classical two-stage detector+recognizer. PaddleOCR-VL is architecturally different: a layout detector (PP-DocLayoutV2) feeds a compact VLM (PaddleOCR-VL-0.9B = NaViT dynamic-resolution vision encoder + ERNIE-4.5-0.3B language model) that processes each detected element.
- PDF input: native. Markdown output: native (+ JSON, Word). OCR: hybrid classical-layout + small VLM. Tables/charts/formulas/seals: all first-class element types. Layout/reading order: yes, dedicated first stage.
- Local feasibility: explicitly supports x64 CPU, plus NVIDIA GPU (CC>=7.0), XPU/DCU/NPU; multiple backends (PaddlePaddle, Transformers, vLLM, SGLang, FastDeploy).
- Standout finding: model weights default to HuggingFace, but PaddleOCR documents an explicit non-HF fallback: `PADDLE_PDX_MODEL_SOURCE="BOS"` pulls weights from Baidu Object Storage (`bos.bcebos.com`) instead. **This project actually tested this fallback — see `02_Tools/paddleocr-vl/observations.md` — and confirmed `bos.bcebos.com` is also blocked in this sandbox.**
- Known limitation: docs stress the full pipeline (layout+VLM) must run together — the VLM alone "produces hallucinated text" without the layout stage first.

### 2. huridocs/pdf-document-layout-analysis
- Repo: https://github.com/huridocs/pdf-document-layout-analysis
- License: Apache-2.0 (confirmed from raw `LICENSE`).
- Language: Python 3.10+. Install: Docker only (`docker run ... huridocs/pdf-document-layout-analysis:v0.0.31`), CPU or GPU compose profiles.
- PDF input: native. Markdown/HTML/JSON output: native.
- OCR/layout: dual-model design — VGT (Vision Grid Transformer, GPU-preferred, ~1.75s/page on GPU, ~13.5s/page on CPU i7-8700) or LightGBM (classical gradient-boosted ensemble of token classifiers, CPU-only, ~0.42s/page).
- Tables/formulas: RapidTable for HTML tables, LaTeX-OCR for formula recognition. OCR languages: 150+ via Tesseract. Reading order: via Poppler, header-first/footer-last heuristic.
- Local feasibility: real CPU story via LightGBM + Tesseract, no GPU strictly required. Some models noted as hosted on Hugging Face; reachability of that specific path unconfirmed.
- Known limitations: translation feature depends on an external Ollama service (optional); model file sizes not fully itemized in docs.
- **This project confirmed the actual blocker is one level lower than network: no Docker daemon exists in this sandbox at all** — see `02_Tools/huridocs-pdf-document-layout-analysis/observations.md`.

### 3. Kreuzberg / Xberg (Goldziher -> xberg-io)
- Repo: https://github.com/Goldziher/kreuzberg (now shows as xberg-io/xberg, ~9.2k stars per live page — appears to be a rename/rebrand-in-progress; the PyPI package is still published as `kreuzberg`, currently v4.10.2).
- License: MIT (confirmed via PyPI metadata and raw `LICENSE`).
- Language: Rust core with bindings (Python, Ruby, Java, Go, PHP, Elixir, C#, TS...). Install: `pip install kreuzberg`.
- PDF input: native (built on Pandoc, PDFium, Tesseract). Markdown output: native ("Readable, structured, RAG-friendly").
- OCR: pluggable — Tesseract (C FFI), PaddleOCR-ONNX (mobile-optimized), Candle (pure-Rust, CPU-only), or VLM fallback (165 providers via a router) — CPU by default, no GPU required.
- Layout/tables: ML layout models (PP-DocLayout-V3, RT-DETR) + table structure (TATR, SLANet) for reading order and cell grids.
- Known limitation (as documented pre-testing): the in-flux Kreuzberg->Xberg rebrand makes long-term repo/URL stability slightly uncertain; exact source of the RT-DETR/TATR/PP-DocLayout-V3 model weights (HF vs bundled) wasn't independently confirmed at research time.
- **This project actually ran it — see `02_Tools/kreuzberg/observations.md` for the real results (0 tables detected on all 3 PDFs despite requesting `table_model="tatr"`, no network calls observed/needed).**

### 4. open-parse (Filimoa) — partial Tier A
- Repo: https://github.com/Filimoa/open-parse
- License: MIT (confirmed from raw `LICENSE`, copyright Sergey Filimonov).
- Language: Python. Install: `pip install openparse` (core, no ML deps) or `pip install "openparse[ml]"`.
- PDF input: native via pdfminer.six. Markdown-ish output: native chunk/node structure serializable to markdown-like text/JSON.
- OCR: none built-in for the base install — optional Tesseract wiring only.
- Tables: "unitable" (best) or table-transformer (developers themselves call this "subpar") — both optional `[ml]` extras requiring a Hugging-Face weight download.
- At research time: base install (no OCR, no ML) looked fully CPU/offline-capable. **This project actually ran it and found an additional, undocumented network dependency not caught during research** — `tiktoken.get_encoding("cl100k_base")` downloads from `openaipublic.blob.core.windows.net` even in base mode, purely for an internal token-count heuristic. See `02_Tools/open-parse/observations.md` for the full finding and the workaround applied.

---

## Tier B candidates (promising, but need GPU and/or HuggingFace Hub access)

### 5. dots.ocr (rednote-hilab)
MIT (code+weights). ~9.1k stars, active into 2026. Single 1.7B VLM unifying
layout+OCR+reading order in one pass, charts->SVG. Served via vLLM
(integrated since v0.11.0) or HF Transformers. GPU + HF required, no
confirmed CPU/quantized path.

### 6. MonkeyOCR (Yuliang-Liu)
Apache-2.0. ~6.6k stars, v1.5 (July 2026). "Structure-Recognition-Relation"
(SRR) triplet paradigm — three lighter expert modules rather than one
monolithic VLM. Claims to beat some larger closed models on OmniDocBench.
Weights via HF or ModelScope; GPU (8GB+ VRAM quantized) required.

### 7. Chandra (Datalab)
Code: Apache-2.0. Weights: modified OpenRAIL-M — free for research/
personal/startups <$2M, **"Commercial self-hosting requires a license."**
Chandra 1 (Oct 2025) -> Chandra 2 (Mar 2026, Qwen-architecture). Handles
handwriting, forms/checkboxes, math, 90+ languages. Benchmarked on H100
80GB; CPU not addressed.

### 8. Surya (VikParuchuri -> datalab-to) — the engine under Marker
Code: Apache-2.0. Weights: modified "AI Pubs Open Rail-M" (free research/
personal/startups <$5M). Surya 2 collapses layout+OCR+table recognition
into one 650M-param VLM, served via vLLM (GPU) or **llama.cpp (CPU/Apple
Silicon)** — a real CPU differentiator vs. peers. Outputs JSON/HTML; full
Markdown assembly is actually done by Marker (already known/deferred).

### 9. OCRFlux (chatdoc-com / ChatDOC)
Apache-2.0. v0.1.0 (June 2025) — last clearly-dated release found, less
actively updated than 2026-era peers. OCRFlux-3B (Qwen2.5-VL-3B-Instruct
fine-tune, via HF), needs ~12GB+ VRAM. **Unique claimed feature: automatic
cross-page table/paragraph merging** (0.986 F1 detection, 0.950 TEDS on
merged reconstruction).

### 10. Nanonets-OCR-s / docext (NanoNets)
Apache-2.0 (docext toolkit). docext added dedicated PDF->Markdown support
Dec 6, 2025. 3B VLM (Qwen2.5-VL-3B-Instruct fine-tune). Rich semantic
Markdown tagging: LaTeX equations, checkboxes, watermark/page-number tags,
signature detection, auto image captions, and **flow-charts/org-charts
rendered as Mermaid code**.

### 11. GLM-OCR (Zhipu AI / zai-org)
Apache-2.0 (both stages, confirmed via raw LICENSE and PyPI `glmocr` v0.1.5
metadata). 2026 release, ~7.4k stars. Compact 0.9B (GLM-V CogViT vision
encoder + GLM-0.5B decoder), two-stage layout->parallel-recognition;
layout stage CPU-capable.

### 12. granite-docling-258M (IBM)
Apache-2.0. Productionized Sept 17, 2025, evolving SmolDocling-256M-preview
(Mar 2025) into one 258M end-to-end VLM (Idefics3 architecture) replacing
Docling's whole classical ensemble. Community ONNX/GGUF conversions exist
for CPU inference; Ollama also lists it. **Compute-wise Tier A, distribution-
wise Tier B** in this sandbox — every channel (official + conversions +
Ollama) is HF- or Ollama-registry-hosted, both blocked here.

### 13. RAGFlow / DeepDoc (infiniflow)
Apache-2.0. DeepDoc = RAGFlow's document-understanding module: OCR +
layout (10 element types) + table-structure recognition (5 cell-role
labels) + auto page-rotation correction for scans. Models served from HF
(README notes a mirror-endpoint workaround for HF-blocked users). Not
fully documented as a standalone tool outside RAGFlow.

### 14. Chunkr (lumina-ai-inc)
**AGPL-3.0** (confirmed from raw LICENSE), paid commercial-license
alternative offered. v2.2.1 (July 2025) — replaced VGT with a YOLO-based
model "more practical for consumer hardware." Rust core; Docker Compose
install (GPU, CPU, Mac-ARM profiles all provided). Converts PDF/DOCX/PPT/
XLSX/images into "Structured HTML & Markdown."

---

## Tier C candidates (poor fit / excluded, confirmed reasons)

### 15. Zerox (getomni-ai)
MIT, ~12.3k stars. Converts pages to images then ships them to a remote
vision-LLM API (OpenAI/Azure/Bedrock/Gemini/Vertex) for Markdown. **No
local/offline model option found.** Excluded: fails "self-hosted, not
SaaS/API-only" outright.

### GOT-OCR2.0 (Ucas-HaoranWei)
Code Apache-2.0, training data CC-BY-NC-4.0. ~8.2k stars. Needs HF weights
+ CUDA 11.8+/Flash-Attention GPU. No distinct 2025/2026 successor found
despite targeted search — dots.ocr/MonkeyOCR/GLM-OCR/Chandra appear to be
the spiritual successors instead.

### mPLUG-DocOwl2 (Alibaba X-PLUG)
Apache-2.0, ~2.4k stars, ACL 2025 (May 2025). 8B params, HF-hosted. It's an
OCR-free multi-page **VQA** model (each page compressed to 324 tokens) —
optimized for answering questions about a document, not reconstructing its
Markdown structure. Excluded: wrong tool class for this use case.

### Kosmos-2.5 (Microsoft)
Part of microsoft/unilm — MIT, code/checkpoint open-sourced May 2024,
minor VQA variant added Aug 2024, no major update since. Image-only input
(no native PDF), needs Flash-Attention GPU, HF-hosted. Superseded by the
2025-2026 wave, offers no clear advantage.

### PDF-Extract-Kit (OpenDataLab)
AGPL-3.0, ~10k stars, last tagged release Oct 2024. The repo's own README
states: "If you are interested in ... converting PDFs to Markdown, please
use MinerU, which combines the high-quality predictions from
PDF-Extract-Kit with specialized engineering optimizations." Excluded as
effectively duplicative of already-tested MinerU, by the project's own
admission.

### LOCR (Location-Guided Transformer for OCR)
Paper: arXiv:2403.02127 / ACL Anthology 2024.findings-emnlp.314. No public
GitHub code release was found despite targeted searches. Cannot confirm
this is installable/runnable at all — excluded pending a real code
release.

### Extractous (yobix-ai)
Apache-2.0, ~1.8k stars, Rust core + Python bindings, Tesseract-based OCR,
Apache Tika (via GraalVM) for other formats. CPU-only and lightweight, but
output is plain text/XML, no native Markdown, no documented table/layout
structure preservation. Same core OCR engine (Tesseract) as the already-
excluded standalone-Tesseract case.

### oar-ocr (GreatV)
Apache-2.0, ~160 stars (very new/small community), Rust, `cargo add
oar-ocr`. Classical PP-OCR-style ONNX models and a native-Rust Candle-based
VLM path (0.6B-2.5B, including PaddleOCR-VL), CPU/CUDA/Metal. Images-only
input (no native PDF — would need a thin PDF->image pre-processing layer);
models auto-download from ModelScope (also blocked in this sandbox), not
Hugging Face or GitHub.

### Context-only notes (not new candidates)
- **Marker v2** (datalab-to) — a full rewrite released July 20, 2026
  (Surya OCR 2 + a new 20M-param fast layout model + rebuilt `pdftext`).
  This is an update to the already-known/deferred Marker, not a new
  discovery — noted since it changes what "benchmark Marker" would mean
  going forward.
- **PaddleOCR bare/already-tested** — distinguished above from
  PaddleOCR-VL/PP-StructureV3, which is the genuinely new pipeline.
