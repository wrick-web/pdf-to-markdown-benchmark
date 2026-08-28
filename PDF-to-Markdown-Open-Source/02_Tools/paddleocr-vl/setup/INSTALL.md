# PaddleOCR-VL / PP-StructureV3 — Setup

- Repo: https://github.com/PaddlePaddle/PaddleOCR
- License: Apache-2.0
- Version tested: `paddleocr==3.7.0`, `paddlex==3.7.2`

## Install (works in any environment, including this sandbox)

```bash
uv venv .venv_paddleocr --python 3.11
source .venv_paddleocr/bin/activate
uv pip install "paddleocr[doc-parser]"
```

No `paddlepaddle` deep-learning framework required for this backend — it
resolves a Transformers-style stack instead (`huggingface-hub`,
`modelscope`, `safetensors`, `tokenizers`, etc.).

## Run (requires Hugging Face Hub or Baidu Object Storage access — BLOCKED in this sandbox)

```python
from paddleocr import PPStructureV3
p = PPStructureV3()
for res in p.predict("path/to/file.pdf"):
    res.save_to_markdown("output_dir/")
```

If Hugging Face Hub is unreachable but Baidu Object Storage is:
```bash
PADDLE_PDX_MODEL_SOURCE=BOS python your_script.py
```

Both were tested in this project and both failed identically:
`Exception: No available model hosting platforms detected. Please check
your network connection.` — see `../logs/init_attempt_default.log` and
`../logs/init_attempt_bos_fallback.log` for the full tracebacks.
