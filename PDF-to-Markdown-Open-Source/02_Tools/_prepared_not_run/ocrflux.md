# OCRFlux (chatdoc-com / ChatDOC)

- Repo: https://github.com/chatdoc-com/OCRFlux
- License: Apache-2.0 (confirmed via raw `LICENSE`)
- v0.1.0 (June 2025) is the last clearly-dated release found — less
  actively updated than 2026-era peers on this list.

## Why it's compelling
**Unique claimed feature: automatic cross-page table/paragraph merging**
(0.986 F1 detection, 0.950 TEDS on merged reconstruction) — most other
tools treat each page independently and never re-stitch a table that spans
a page break. This directly matters for PDF1/PDF2 in this project's
benchmark set, both of which contain multi-page financial tables.

## Requirements
- OCRFlux-3B (Qwen2.5-VL-3B-Instruct fine-tune), ~12GB+ VRAM, multi-GPU
  tensor-parallel supported
- Hugging Face Hub for weights
- Heavier install than most peers: Conda + `pip install -e .` with a
  pinned CUDA-12.4 `flashinfer` wheel

## Reproduce on an unrestricted GPU machine
```bash
git clone https://github.com/chatdoc-com/OCRFlux.git
cd OCRFlux
conda create -n ocrflux python=3.11 && conda activate ocrflux
pip install -e .
# follow repo README for the pinned CUDA-12.4 flashinfer wheel step
python -m ocrflux.pipeline path/to/file.pdf --output_dir out_dir/
```

## Blocked here because
GPU (12GB+ VRAM) + Hugging Face Hub required; neither available here.
