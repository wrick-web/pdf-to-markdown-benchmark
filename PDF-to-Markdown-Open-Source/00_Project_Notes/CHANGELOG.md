# Changelog

Chronological log of every meaningful action this cycle. Newest entries at
top.

---

**2026-08-28** — Environment
Tool: N/A (infrastructure)
Action: Probed sandbox network/GPU/Docker capabilities.
What changed: Confirmed 4 vCPU/15GB RAM, no GPU, no Docker daemon (CLI
present, no `/var/run/docker.sock`). Confirmed egress allowlist = PyPI,
npm, Ubuntu archive, GitHub domains (`github.com`, `raw.githubusercontent.com`,
`api.github.com`, `objects.githubusercontent.com`). Confirmed egress BLOCKS
(403 policy denial, tested directly): `huggingface.co`, `cdn-lfs.huggingface.co`,
`arxiv.org`, `archive.org`, `bos.bcebos.com`, `modelscope.cn`,
`registry.ollama.ai`, `ollama.com`, `corporate.target.com`, `www.shi.co.jp`,
`t9014651757.p.clickup-attachments.com`.
Why: Needed to know what could actually be installed/run before shortlisting.
Result: Shaped the entire Tier A/B/C split — see `Tool_Landscape.md`.

**2026-08-28** — Benchmark inputs
Tool: N/A
Action: Attempted to fetch the 3 original benchmark PDFs from their source
URLs and from the ClickUp attachment CDN; both blocked by egress policy
(confirmed via curl and WebFetch, both returned `EGRESS_BLOCKED`/403).
Why: These are the same 3 PDFs used in the prior hosted-API cycle;
cross-comparability requires the identical files, not recreations.
Result: Asked the user via `AskUserQuestion`; user chose to upload the 3
PDFs directly into this session rather than use synthetic stand-ins.
Status: awaiting upload.

**2026-08-28** — Research
Tool: N/A (discovery phase)
Action: Ran a dedicated research agent to find new, previously-uncovered
open-source PDF→Markdown tools, cross-checked against the existing
ClickUp task's already-tested/known/excluded lists to avoid duplication.
Why: Phase 1 of the task — "Discover new tools" — required before any
shortlisting/installation.
Result: 9 new tools verified (license, repo, last update confirmed
against raw `LICENSE` files where reachable): PaddleOCR-VL/PP-StructureV3,
huridocs/pdf-document-layout-analysis, Kreuzberg, open-parse (Tier A);
dots.ocr, MonkeyOCR, Chandra, Surya, OCRFlux, Nanonets-OCR-s/docext,
GLM-OCR, granite-docling-258M, RAGFlow/DeepDoc, Chunkr (Tier B); plus 8
Tier C exclusions with confirmed reasons. Full detail in `Research_Notes.md`
and `Tool_Landscape.md`.

**2026-08-28** — PaddleOCR-VL / PP-StructureV3
Action: Installed `paddleocr[doc-parser]` (v3.7.0) via `uv pip` in a
dedicated venv; attempted to initialize `PPStructureV3()`.
What changed: Install succeeded cleanly (no paddlepaddle framework
required for this backend — uses a HF-transformers-style backend).
Runtime init failed: `Exception: No available model hosting platforms
detected. Please check your network connection.` Retried with
`PADDLE_PDX_MODEL_SOURCE=BOS` (the documented non-HF fallback) — same
failure, because `bos.bcebos.com` is also blocked in this sandbox.
Why: Verify whether the documented Baidu-Object-Storage fallback could
route around the Hugging Face block.
Result: Confirmed **attempted-blocked** status with hard evidence (exact
exception text captured). Tool remains a strong Tier A candidate on any
machine with normal internet access.

**2026-08-28** — Kreuzberg
Action: Installed `kreuzberg==4.10.2` (MIT, Rust core) via `uv pip` in a
dedicated venv; installed system `tesseract-ocr` + `tesseract-ocr-eng` via
apt (reachable — Ubuntu archive is not on the egress blocklist) to back
its OCR path.
What changed: Clean install, both `kreuzberg` and `tesseract --version`
verified working.
Why: Kreuzberg was the strongest Tier A candidate on paper (MIT, CPU-first,
native Markdown, pluggable OCR) — first tool to fully validate.
Result: Ready to run against the 3 benchmark PDFs once uploaded.

**2026-08-28** — open-parse
Action: Installed `openparse==0.7.0` (MIT) in base mode (no `[ml]` extra)
via `uv pip`.
What changed: Clean install. Confirmed the `[ml]` extra (better table
extraction via "unitable"/table-transformer) requires an
`openparse-download` step that pulls weights from Hugging Face — blocked
here, so only base mode (pdfminer.six-driven, no OCR) is usable in this
sandbox.
Why: Wanted at least one lightweight, zero-ML-dependency baseline for
native-digital-text PDFs, explicitly framed as a "best lightweight" style
candidate rather than a full contender (no OCR, weaker tables).
Result: Ready to run against the 3 benchmark PDFs once uploaded, base mode
only.

**2026-08-28** — huridocs/pdf-document-layout-analysis
Action: Checked feasibility — this tool ships only as a Docker image.
What changed: N/A (not attempted — `docker ps` confirmed no daemon
available in this sandbox before spending time on it).
Why: Docker-only tools cannot run here regardless of network status.
Result: **prepared-not-run**. Exact `docker run` commands documented in
`02_Tools/huridocs-pdf-document-layout-analysis/setup/` for the user to
run on their own machine (which has Docker).

**2026-08-28** — Project scaffold
Action: Created `PDF-to-Markdown-Open-Source/` folder tree per the
required structure; wrote `README.md` and `Tool_Landscape.md`.
Why: Phase 13 requirement — one organized, reproducible project folder.
Result: Scaffold in place; population in progress.
