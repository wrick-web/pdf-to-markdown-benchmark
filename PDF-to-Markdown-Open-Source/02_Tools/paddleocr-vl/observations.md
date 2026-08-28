# PaddleOCR-VL / PP-StructureV3 — Observations

Repo: https://github.com/PaddlePaddle/PaddleOCR · PyPI `paddleocr[doc-parser]==3.7.0` · Apache-2.0.
**Status: attempted-blocked** — installed successfully, could not execute against any benchmark PDF in this sandbox.

## Setup

Installation: `uv pip install "paddleocr[doc-parser]"` — succeeded cleanly, no build errors. Notably this backend does **not** require the classic PaddlePaddle deep-learning framework (`paddlepaddle` was not in the resolved dependency set) — installs `paddleocr==3.7.0`, `paddlex==3.7.2`, `huggingface-hub==1.29.0`, `modelscope==1.39.1`, `opencv-contrib-python`, `safetensors`, `tokenizers`, etc. (a Transformers-style stack).
Version: paddleocr 3.7.0
Dependencies: see above — resolved in ~545MB of installed packages.
GPU/CPU: documentation claims CPU support (x64) in addition to NVIDIA/XPU/DCU/NPU.
Model requirements: **This is exactly where this tool is blocked.** PP-StructureV3 downloads its layout/OCR/table models on first use; no weights ship in the pip package itself.
Setup difficulty: Low for the `pip install` step itself; **blocked entirely at first run** in this sandbox.

## What was actually run

```python
from paddleocr import PPStructureV3
p = PPStructureV3()
```

**Result (default Hugging Face model source):**
```
Exception: No available model hosting platforms detected. Please check your network connection.
```
(full traceback in `logs/init_attempt_default.log`)

**Retried with the documented non-Hugging-Face fallback** (`PADDLE_PDX_MODEL_SOURCE=BOS`, which the project documents as an escape hatch that pulls weights from Baidu Object Storage instead of Hugging Face):
```
Exception: No available model hosting platforms detected. Please check your network connection.
```
Same failure — confirmed independently that `bos.bcebos.com` is *also* blocked by this sandbox's egress policy (403 policy denial via direct `curl` test, logged in the project `CHANGELOG.md`), not just `huggingface.co`. Both of PaddleOCR-VL's documented model-hosting paths are unreachable here.

No benchmark PDFs could be processed as a result — **0 of 3 PDFs tested.**

## Why this is still a Tier A candidate (not excluded)

Everything about the pipeline's *design* fits this use case extremely well on paper: a dedicated layout-detection stage (PP-DocLayoutV2) feeding a compact 0.9B VLM (NaViT + ERNIE-4.5-0.3B) per detected element, native Markdown/JSON/Word export, explicit first-class handling of tables, charts (chart-to-table), formulas, and seals, and CPU support. It is architecturally distinct from the already-tested bare PaddleOCR (a classical two-stage detector+recognizer with no VLM and no document-structure output) — this is not a duplicate test of the same thing. The only reason it wasn't benchmarked is this specific sandbox's network policy, not a flaw in the tool.

## Reproducing this on an unrestricted machine

```bash
uv venv .venv_paddleocr --python 3.11
source .venv_paddleocr/bin/activate
uv pip install "paddleocr[doc-parser]"
python - <<'EOF'
from paddleocr import PPStructureV3
p = PPStructureV3()
result = p.predict("path/to/file.pdf")
for res in result:
    res.save_to_markdown("output_dir/")
EOF
```
If Hugging Face Hub is unreachable but Baidu Object Storage is, set
`PADDLE_PDX_MODEL_SOURCE=BOS` before running. See
`02_Tools/paddleocr-vl/setup/INSTALL.md` for the full command set, and
`00_Project_Notes/CHANGELOG.md` for the exact blocked-host evidence.

## Evidence
- `logs/init_attempt_default.log` — full traceback, default (HF) model source
- `logs/init_attempt_bos_fallback.log` — full traceback, `PADDLE_PDX_MODEL_SOURCE=BOS`
- `00_Project_Notes/CHANGELOG.md` — network probe results for `huggingface.co` and `bos.bcebos.com`
