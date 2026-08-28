# Surya (datalab-to, standalone)

- Repo: https://github.com/datalab-to/surya
- License: Apache-2.0 (code, PyPI-confirmed); model weights: modified "AI
  Pubs Open Rail-M" (free research/personal/startups <$5M)
- Surya 2 collapses layout+OCR+table recognition into one 650M-param VLM

## Why it's compelling
This is the engine underneath Marker (already known/deferred from an
earlier cycle) — but it has a genuine **CPU/Apple Silicon path via
llama.cpp**, unusual among the VLM-OCR tools surveyed this cycle. Outputs
JSON/HTML for layout, OCR, and table detail — Marker itself does the final
Markdown assembly on top, so Surya alone is a component, not a one-shot
PDF-to-Markdown tool.

## Requirements
- Hugging Face Hub for weights (blocked here)
- GPU via vLLM, or CPU/Metal via llama.cpp (the interesting option once HF
  access exists)

## Reproduce on an unrestricted machine
```bash
pip install surya-ocr
surya_ocr path/to/file.pdf --output_dir out_dir/
# Combine with Marker for final Markdown assembly, or consume Surya's
# JSON/HTML output directly for a custom pipeline.
```

## Blocked here because
Hugging Face Hub is required for weights regardless of the CPU/GPU choice;
blocked in this sandbox.
