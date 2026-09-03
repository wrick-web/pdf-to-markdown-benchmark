# Docling — install notes (Round 1, Rev-2 execution attempt)

Installed cleanly. Nothing below failed at install time — the failures
documented in `../logs/` happen later, at first pipeline use (model
download), not during `pip install`.

## Commands run

```bash
cd /home/user/pdf-to-markdown-benchmark
uv venv .venv_docling
uv pip install docling --python .venv_docling/bin/python
```

## Versions actually installed (2026-09-03)

| Package | Version |
|---|---|
| docling | 2.124.0 |
| docling-core | 2.93.0 |
| docling-ibm-models | 4.0.1 |
| docling-parse | 7.17.0 |
| docling-slim | 2.124.0 |
| torch | 2.14.0 |
| torchvision | 0.29.0 |
| transformers | 5.16.1 |
| rapidocr | 3.9.2 |

Python: 3.11.15 (the environment's system interpreter, via `uv venv`).

## What Docling needs at runtime beyond the pip install

Docling's `StandardPdfPipeline` does not ship its models — it downloads
them the first time a pipeline is constructed:

1. **OCR** (default engine, RapidOCR/PyTorch backend): downloads
   `PP-OCRv6_det_small.pth` and related weights from
   `https://www.modelscope.cn/models/RapidAI/RapidOCR/...`.
2. **Layout** (object detection, always used regardless of
   `do_ocr`): downloads `docling-project/docling-layout-heron`
   (revision `main`) from the Hugging Face Hub via
   `huggingface_hub.snapshot_download` / `hf_api.model_info`.

Both hosts are unreachable from this sandbox (network egress is limited
to PyPI/npm/GitHub-style registries). See `../logs/` for the two real
tracebacks. This is a runtime/network blocker, not an install problem —
`pip install docling` itself has no issue.

## Fixture status

The assigned TC27 fixture (`briefing_note_BEP-BN-2026-04.pdf`, from
ClickUp task `86bbr4dmu`) could not be retrieved either: the ClickUp
attachment CDN (`t9014651757.p.clickup-attachments.com`) is also blocked
by this sandbox's network policy, and ClickUp's own notification emails
carry no file attachments (confirmed by reading one in full via Gmail).

A throwaway PDF (`smoketest.pdf`, one line of plain text, created locally
via `pymupdf`) was used only to exercise Docling's pipeline-initialization
code path far enough to observe *which* dependency fails and how. It is
not a benchmark fixture and was never treated as a substitute for
`briefing_note_BEP-BN-2026-04.pdf`.
