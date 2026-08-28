# PDF → Markdown: Open-Source Tool Research (Cycle II — New Tool Discovery)

This folder is the working project space for the ClickUp task
["PDF to markdown using open source libraries"](https://app.clickup.com/t/9014651757/86ban5kjq)
(parent task `86ban5kjq`). It covers **new** open-source PDF→Markdown tool
discovery, verification, installation, benchmarking, and comparison —
building on top of (not duplicating) the tools already tested/excluded in
earlier cycles.

## What this cycle adds

Earlier cycles already benchmarked: Docling, PyMuPDF4LLM, LiteParse, doc2mark,
MarkItDown, MinerU, PaddleOCR (bare), Dolphin, Unstructured, DocTR (in review).
They already excluded: GROBID, Nougat, Tesseract (standalone), PDFPlumber,
Camelot, Tabula. They already identified-but-deferred: Marker, olmOCR,
pdf-craft.

This cycle's job was to find **genuinely new** candidates not on any of
those lists, verify them against primary sources (not marketing copy),
install/run what is actually executable in this environment, and document
everything — including what could *not* be run and exactly why.

## Environment constraints that shaped this cycle (read this first)

This research was executed inside a sandboxed cloud container with:
- **No GPU** (4 vCPU / 15GB RAM / CPU-only)
- **No Docker daemon** (the `docker` CLI is present but there is no daemon to
  connect to — Docker-based tools cannot be started here)
- **Restricted network egress** — only PyPI, npm, the Ubuntu package
  archive, and GitHub (`github.com`, `raw.githubusercontent.com`,
  `api.github.com`, `objects.githubusercontent.com`) are reachable.
  **Hugging Face Hub, ModelScope, Ollama's registry, Baidu Object Storage
  (BOS), arXiv, and archive.org are all blocked** (confirmed via direct
  `curl`/proxy tests — 403 policy denials, not transient failures).

This matters enormously for this specific use case, because almost every
2025-2026 state-of-the-art document-parsing tool is VLM-based and downloads
its model weights from Hugging Face Hub at first run. Those tools were
still fully researched, verified, and script-prepared (installation
scripts, exact CLI commands, model IDs) so they are **one command away**
from running on a machine with normal internet access and/or a GPU — but
they could not be executed end-to-end inside *this* sandbox. This is
documented tool-by-tool rather than glossed over; see
`00_Project_Notes/Tool_Landscape.md` and each tool's `observations.md`.

Tools that genuinely have no Hugging Face/GPU/Docker dependency for their
core path (Kreuzberg, open-parse) **were** installed and run end-to-end
against the real benchmark PDFs.

## Folder structure

```
PDF-to-Markdown-Open-Source/
├── 00_Project_Notes/        Master notes, tool register, methodology, changelog
├── 01_Benchmark_PDFs/       The 3 benchmark input PDFs (uploaded by the user)
├── 02_Tools/<Tool>/         Per-tool setup, scripts, raw/markdown output, evidence, observations.md
├── 03_Benchmark_Results/    MASTER_RESULTS.md, scorecards, comparison tables, evidence
├── 04_Scripts/              Reusable installation/conversion/evaluation/utility scripts
└── 05_Final_Report/         Final_Comparison.md, Recommendations.md, Reproducibility_Guide.md
```

## How to pick this back up

1. Read `00_Project_Notes/Tool_Landscape.md` for the full tool register.
2. Read `00_Project_Notes/CHANGELOG.md` for a chronological log of every
   action taken.
3. Read `05_Final_Report/Final_Comparison.md` for the end-state conclusions.
4. Read `05_Final_Report/Reproducibility_Guide.md` to re-run anything,
   including the tools that were prepared but not executed here (e.g. on a
   GPU machine with normal internet access).
