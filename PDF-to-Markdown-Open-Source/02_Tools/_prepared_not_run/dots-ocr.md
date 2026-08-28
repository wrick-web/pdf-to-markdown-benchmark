# dots.ocr (rednote-hilab)

- Repo: https://github.com/rednote-hilab/dots.ocr
- License: MIT (code and weights)
- ~9.1k GitHub stars, actively updated into 2026
- Single 1.7B-parameter VLM unifying layout detection + content recognition
  in one pass; outputs structured JSON, Markdown, and chart-to-SVG
  visualizations; claims SOTA-for-size on OmniDocBench/olmOCR-Bench.

## Why it's compelling for this use case
One model does layout + OCR + reading order + chart-as-SVG in a single
pass — directly targets this project's "layout awareness + OCR + chart
handling + reading order" criteria in one step, rather than a multi-model
pipeline.

## Requirements
- GPU (no confirmed CPU/quantized path)
- Hugging Face Hub access for weights (blocked in this sandbox)
- Served via vLLM (officially integrated since vLLM 0.11.0) or HF Transformers

## Reproduce on an unrestricted GPU machine
```bash
git clone https://github.com/rednote-hilab/dots.ocr.git
cd dots.ocr
pip install -r requirements.txt
# Option A: vLLM server
docker run --gpus all -p 8000:8000 vllm/vllm-openai:v0.11.0 \
  --model rednote-hilab/dots.ocr
# Option B: direct HF Transformers inference — see repo README for the
# exact `predict.py`-style invocation and Markdown export flag.
```

## Blocked here because
`huggingface.co` returns 403 in this sandbox (confirmed via direct curl
test — see `00_Project_Notes/CHANGELOG.md`), and no GPU is available.
