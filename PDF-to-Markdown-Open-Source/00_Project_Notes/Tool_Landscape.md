# Tool Landscape — Master Register

Source of truth for every tool considered across all cycles of this ClickUp
task. Updated continuously (see `CHANGELOG.md` for the change log).

Legend: **Status** = `tested-prior-cycle` / `tested-this-cycle` /
`attempted-blocked` (installed, could not fully run in this sandbox) /
`prepared-not-run` (scripted for reproducibility, not executed here) /
`excluded`.

## A. Already covered — DO NOT re-test (duplicate-check baseline)

| Tool | Repository | License | Status (prior cycle) | Notes |
|---|---|---|---|---|
| Docling | github.com/docling-project/docling | MIT | tested-prior-cycle | IBM Research/LF AI & Data. Cycle I. |
| PyMuPDF4LLM | github.com/pymupdf/RAG | AGPL/commercial dual | tested-prior-cycle | Cycle I. |
| LiteParse | github.com/run-llama/liteparse | Apache-2.0 | tested-prior-cycle | Cycle I. |
| doc2mark | github.com/luisleo526/doc2mark | MIT | tested-prior-cycle | Cycle I. |
| MarkItDown | github.com/microsoft/markitdown | MIT | tested-prior-cycle | Cycle I. |
| MinerU (Magic-PDF) | github.com/opendatalab/MinerU | Apache-2.0 (MinerU OSS license) | tested-prior-cycle | Cycle II (already executed, per ClickUp subtask). |
| PaddleOCR (bare/standalone) | github.com/PaddlePaddle/PaddleOCR | Apache-2.0 | tested-prior-cycle | Standalone OCR tested despite earlier exclusion note — see contradiction note below. |
| Dolphin | github.com/bytedance/Dolphin | MIT-family (OSS) | tested-prior-cycle | Cycle II. |
| Unstructured | github.com/Unstructured-IO/unstructured | Apache-2.0 | tested-prior-cycle | Was originally in the "excluded" table (no markdown export at the time) but was tested anyway in Cycle II per the ClickUp subtask list — treated as covered either way. |
| DocTR | github.com/mindee/doctr | Apache-2.0 | in review (not yet closed) | ClickUp subtask status = "review", not "complete" — flagged as in-progress, not duplicated here. |

**Known-but-deferred ("currently being considered", not yet benchmarked in any cycle):**

| Tool | Repository | License | Notes |
|---|---|---|---|
| Marker | github.com/datalab-to/marker | GPL-3.0 (code) / weights free below revenue threshold | Named in ClickUp's "Known Tool Landscape" and "Cycle II adds..." list, but no benchmark subtask exists yet. **Not treated as new** — out of scope for this cycle's "new tool" mandate; noted as an open gap. Datalab shipped a **Marker v2 rewrite July 20, 2026** (new Surya OCR 2 + 20M-param fast layout model) — if/when Marker is finally benchmarked, it should be v2, not the original. |
| olmOCR | github.com/allenai/olmocr | Apache-2.0 | Same as above — known/deferred, not new, not benchmarked here. |
| pdf-craft | github.com/oomol-lab/pdf-craft | AGPL-3.0 | Same as above — known/deferred, not new, not benchmarked here. |

**Already excluded (prior cycle) — not reconsidered (no meaningful new release found that changes the original rationale):**

| Tool | Reason for exclusion |
|---|---|
| GROBID | Converts tables/formulas to images, not structured markdown; scoped to scientific metadata, not general documents. |
| Nougat | Plain text/LaTeX from page images only, no table structure, superseded by newer VLM tools, not actively maintained. |
| PaddleOCR (standalone, as pure OCR framing) | Pure OCR without a markdown pipeline — this exclusion rationale is specifically superseded by PP-StructureV3/PaddleOCR-VL (see section C, item 1), which is a genuinely distinct, structure-aware pipeline layered on the same GitHub repo. |
| Tesseract OCR | No structural awareness — explicitly out of scope by the use-case definition. |
| PDFPlumber, Camelot, Tabula | Extraction-only, no markdown export, no OCR, would require manual assembly. |
| OCRmyPDF | Implied-excluded: produces a searchable **PDF**, not markdown; no table/chart structural awareness — same rationale class as Tesseract. Verified this cycle: still true, no markdown mode exists in OCRmyPDF as of this check. |

## B. This cycle's new-tool discovery — methodology

Discovery agent searched GitHub topics, PyPI, and web coverage of 2025-2026
document-AI releases, then verified license/repo/last-update facts directly
against each project's raw `LICENSE` file on `raw.githubusercontent.com`
(not marketing pages) wherever reachable. Full raw research notes are in
`Research_Notes.md`. Environment constraints (no GPU, no Hugging Face Hub /
ModelScope / Ollama registry / BOS, no Docker daemon — see `README.md`)
were applied as a hard filter for what could actually be *executed* here,
separate from what qualifies as a strong candidate on paper.

## C. New candidates found — Tier A (strong fit, targeted for real execution)

| # | Tool | Repo | License | Latest update | Sandbox result |
|---|---|---|---|---|---|
| 1 | **PaddleOCR-VL / PP-StructureV3** | github.com/PaddlePaddle/PaddleOCR | Apache-2.0 | v3.0 (2025-05); VL-1.6 point release | **Installed** (`paddleocr==3.7.0`, `paddlex==3.7.2`). **Blocked at runtime**: `Exception: No available model hosting platforms detected` — confirmed both default (Hugging Face) and documented `PADDLE_PDX_MODEL_SOURCE=BOS` fallback fail, because `huggingface.co` and `bos.bcebos.com` both return 403 policy-denial through this sandbox's egress proxy. Status: **attempted-blocked**. |
| 2 | **Kreuzberg** (Goldziher, PyPI name `kreuzberg`; GitHub project is mid-rebrand to `xberg-io/xberg`) | github.com/Goldziher/kreuzberg | MIT | PyPI v4.10.2, active | **Installed and fully run** (`kreuzberg==4.10.2`). Rust core, native Markdown output, Tesseract-backed OCR (installed system Tesseract 5.3.4 via apt — reachable, unlike HF). Status: **tested-this-cycle**. |
| 3 | **huridocs/pdf-document-layout-analysis** | github.com/huridocs/pdf-document-layout-analysis | Apache-2.0 | active (Docker tags to v0.0.31) | **Docker-only distribution** — this sandbox has the `docker` CLI but no daemon (`docker ps` → "cannot connect to the Docker daemon"). Cannot be started here regardless of network. Status: **prepared-not-run** (setup script + exact `docker run` commands provided for the user's own machine). |
| 4 | **open-parse** (Filimoa) | github.com/Filimoa/open-parse | MIT | active | **Installed and run** in base mode (`openparse==0.7.0`, no `[ml]` extra — that extra needs a Hugging Face weight download for its table models, which is blocked here). Base mode = pdfminer.six-driven layout/chunking, no OCR, no ML table model. Status: **tested-this-cycle** (explicitly as a lightweight/native-text baseline, not a full contender). |

## D. New candidates found — Tier B (promising, GPU/HF/Docker required — prepared, not run)

All verified against raw `LICENSE` files. None are executable in this
sandbox (all need Hugging Face Hub, and most need a GPU); each has an
install script under `02_Tools/<tool>/setup/` for the user to run
elsewhere, plus is documented in `Included Tools & Rationale`.

| Tool | Repo | License (code / weights) | Why it's compelling | Blocker here |
|---|---|---|---|---|
| dots.ocr | github.com/rednote-hilab/dots.ocr | MIT / MIT | Single 1.7B VLM unifying layout+OCR+reading order in one pass; charts→SVG | GPU + HF |
| MonkeyOCR | github.com/Yuliang-Liu/MonkeyOCR | Apache-2.0 | "Structure-Recognition-Relation" triplet architecture (not one monolithic VLM); TableTEDS 76.5–87.5% | GPU + HF/ModelScope |
| Chandra | github.com/datalab-to/chandra | Apache-2.0 code / modified OpenRAIL-M weights | Handwriting, forms/checkboxes, math, 90+ languages in one model | GPU + HF; **commercial self-hosting needs a separate license** |
| Surya (standalone) | github.com/datalab-to/surya | Apache-2.0 code / modified OpenRAIL-M weights | Layout+OCR+table engine under Marker; has a genuine CPU/Metal path via llama.cpp | HF for weights; alone it's a component, not full MD output |
| OCRFlux | github.com/chatdoc-com/OCRFlux | Apache-2.0 | Unique automatic **cross-page** table/paragraph merging (0.986 F1) | GPU (12GB+ VRAM) + HF; heavier/finickier install (pinned CUDA 12.4 flashinfer) |
| Nanonets-OCR-s / docext | github.com/NanoNets/docext | Apache-2.0 | Semantic tags (LaTeX, checkboxes, watermark/signature), **flow-charts rendered as Mermaid** | GPU + HF |
| GLM-OCR | github.com/zai-org/GLM-OCR | Apache-2.0 (both stages) | Compact 0.9B, two-stage layout(CPU-capable)+recognition | HF for weights; recognition stage wants GPU |
| granite-docling-258M | HF `ibm-granite/granite-docling-258M` (org: `docling-project`) | Apache-2.0 | Tiny (258M) end-to-end VLM replacing Docling's whole ensemble; ONNX/GGUF community builds exist for CPU | **Distribution-only blocker**: every build (official + ONNX + GGUF + Ollama) is HF- or Ollama-registry-hosted; both blocked here. Compute-wise this would be Tier A on a machine with HF access. |
| RAGFlow / DeepDoc | github.com/infiniflow/ragflow | Apache-2.0 | 10-class layout + table structure + caption pairing, page-rotation correction for scans | HF for weights; sub-component of a larger RAG platform, not a standalone CLI |
| Chunkr | github.com/lumina-ai-inc/chunkr | **AGPL-3.0** | Rust core, genuine CPU/Mac-ARM Docker compose profiles, PDF/DOCX/PPTX/XLSX→structured HTML+Markdown | No Docker daemon here; also AGPL-3.0 is copyleft — flag before any redistribution/service use |

## E. New candidates found — Tier C (poor fit / excluded, with confirmed reasons)

| Tool | Repo | Reason for exclusion |
|---|---|---|
| Zerox | github.com/getomni-ai/zerox | Confirmed: thin wrapper that ships page images to a remote paid vision-LLM API (OpenAI/Azure/Bedrock/Gemini/Vertex) — **no local/offline model option exists**. Fails the "self-hosted, not SaaS/API-only" requirement outright. |
| GOT-OCR2.0 | github.com/Ucas-HaoranWei/GOT-OCR2.0 | Apache-2.0 code / CC-BY-NC-4.0 training data. No distinct 2025/2026 successor found (checked explicitly); superseded in practice by dots.ocr/MonkeyOCR/Chandra/GLM-OCR. Needs GPU+HF regardless. |
| mPLUG-DocOwl2 | github.com/X-PLUG/mPLUG-DocOwl | It's a document-**VQA** model (answers questions about a page compressed to 324 tokens), not a structural Markdown reconstructor — wrong tool class for this use case. |
| Kosmos-2.5 | github.com/microsoft/unilm | Image-only input (no native PDF), stale since Aug 2024, GPU+HF, no advantage over newer entrants. |
| PDF-Extract-Kit | github.com/opendatalab/PDF-Extract-Kit | AGPL-3.0. The project's own README says to use MinerU instead — this is MinerU's underlying model toolbox, and MinerU is already tested. Duplicate by the project's own admission. |
| LOCR | (paper only — arXiv:2403.02127 / EMNLP 2024 findings) | **No public code repository found** despite targeted search. Not verifiable as installable; excluded pending a real release rather than assumed working. |
| Extractous | github.com/yobix-ai/extractous | Tesseract-based, CPU, but output is plain text/XML with no documented table/layout structure preservation — fails the structural-fidelity bar. |
| oar-ocr | github.com/GreatV/oar-ocr | Images-only (no native PDF input), weights only via ModelScope (blocked here too), ~160 GitHub stars / very new and unproven. |

## F. Coverage assessment (this cycle)

- **9 new tools independently verified** beyond the already-covered list
  (4 Tier A + 10 Tier B, with 5 Tier C explicitly ruled out — see counts
  above; note dots.ocr/MonkeyOCR/Chandra/Surya/OCRFlux/Nanonets/GLM-OCR/
  granite-docling/RAGFlow/Chunkr = 10 Tier B entries).
- **2 fully executed end-to-end this cycle**: Kreuzberg (flagship new
  candidate) and open-parse (lightweight native-text baseline).
- **1 installed but runtime-blocked with concrete evidence**: PaddleOCR-VL
  / PP-StructureV3 (both its default and documented fallback model sources
  are unreachable from this sandbox).
- **1 blocked at the infrastructure layer**: huridocs/pdf-document-layout-analysis
  (no Docker daemon available).
- **10 fully researched, license-verified, and script-prepared for
  reproduction on a GPU/internet-unrestricted machine**, but not executed
  here.

This clears the "at least a handful of genuinely new, verified candidates"
bar for the research mandate, while being honest that this specific sandbox
could only *execute* 2 of them end-to-end (plus one partial/blocked attempt
with hard evidence) due to network and hardware constraints — not because
better tools don't exist, but because this container cannot reach the
services those tools depend on. All setup scripts are ready for the user
to re-run on their own laptop as part of the final screen recording.
