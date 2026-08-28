# Chandra (Datalab)

- Repo: https://github.com/datalab-to/chandra
- License: Apache-2.0 (code, confirmed via raw `LICENSE`); **model weights
  are a modified OpenRAIL-M** — free for research/personal use and startups
  under $2M funding/revenue; the README explicitly states **"Commercial
  self-hosting requires a license."** Flag this before recommending Chandra
  for any production/commercial deployment.
- Chandra 1 (Oct 2025) -> Chandra 2 (Mar 2026, Qwen-architecture VLM)

## Why it's compelling
The most feature-complete single-model OCR found this cycle: handwriting,
forms/checkboxes, math, complex tables/layouts, 90+ languages, Markdown/
HTML/JSON output in one model.

## Requirements
- GPU (benchmarked on H100 80GB by the authors; CPU not addressed in docs)
- Hugging Face Hub for weights

## Reproduce on an unrestricted GPU machine
```bash
pip install chandra-ocr[hf]
python -m chandra.cli path/to/file.pdf --output-dir out_dir/ --format markdown
# or vLLM server mode — see repo README
```

## Blocked here because
GPU + Hugging Face Hub required, both unavailable in this sandbox.
Regardless of sandbox limits, **the OpenRAIL-M weight license's commercial
carve-out should be reviewed before any production use.**
