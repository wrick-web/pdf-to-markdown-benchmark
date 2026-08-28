# MonkeyOCR (Yuliang-Liu)

- Repo: https://github.com/Yuliang-Liu/MonkeyOCR
- License: Apache-2.0 (confirmed via raw `LICENSE`)
- v1.5 technical report accepted July 2026 — actively maintained, ~6.6k stars

## Why it's compelling
Uses a "Structure-Recognition-Relation" (SRR) triplet paradigm — three
lighter expert modules instead of one monolithic page-captioning VLM.
Claims to beat some larger closed models (Gemini 2.5-Pro, GPT-4o) on
OmniDocBench; reports TableTEDS 76.5-87.5%, directly relevant to this
project's table-fidelity criterion.

## Requirements
- GPU (RTX 3090/4090/A6000/H800/A100 tested by authors); a quantized
  variant reportedly fits 8GB VRAM. No CPU path confirmed.
- Weights via Hugging Face (`echo840/MonkeyOCR-pro-3B`, `-1.2B`) or ModelScope.

## Reproduce on an unrestricted GPU machine
```bash
git clone https://github.com/Yuliang-Liu/MonkeyOCR.git
cd MonkeyOCR
pip install -r requirements.txt
python download_model.py   # pulls from HF or ModelScope
python parse.py --input path/to/file.pdf --output out_dir/ --output-format markdown
```

## Blocked here because
Needs both a GPU (none in this sandbox) and Hugging Face Hub / ModelScope
(both blocked — confirmed via direct curl tests).
