# Nanonets-OCR-s / docext (NanoNets)

- Toolkit repo: https://github.com/NanoNets/docext
- License: Apache-2.0 (confirmed via raw `LICENSE`)
- docext added dedicated PDF-to-Markdown support Dec 6, 2025
- Model: 3B VLM (Qwen2.5-VL-3B-Instruct fine-tune), HF-hosted (`nanonets/Nanonets-OCR-s`)

## Why it's compelling
Richest semantic Markdown tagging found this cycle: LaTeX equations, ☐/☑
checkboxes, explicit watermark/page-number tags, signature detection,
auto image captions, and — uniquely — **flow-charts/org-charts rendered as
Mermaid code**. This is a genuinely different, more structured approach to
"chart reconstruction" than any other tool surveyed (data-as-diagram-code,
not just a raster image or an SVG trace).

## Requirements
- GPU for reasonable 3B-VLM throughput
- Hugging Face Hub for weights

## Reproduce on an unrestricted GPU machine
```bash
git clone https://github.com/NanoNets/docext.git
cd docext
pip install -e .
python -m docext.pdf2md path/to/file.pdf --output out_dir/
```

## Blocked here because
GPU + Hugging Face Hub required; neither available here.
