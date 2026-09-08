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

## Exhaustive model-acquisition retry (2026-09-08)

Before accepting the blocker again, identified the exact tool and exact
models this benchmark actually targets, then tried every documented
download route directly (not just via `PPStructureV3`'s own wrapper).

**Correct tool identity.** The installed package (`paddleocr==3.7.0`)
exposes a class literally named `PaddleOCRVL`, distinct from
`PPStructureV3` (the older, six--plus-model classical structure
pipeline). `PaddleOCRVL` is the actual "PaddleOCR-VL" architecture this
project's earlier research described (one small end-to-end VLM
replacing the ensemble) and only needs **two** models:

| Model | Role | Hugging Face | ModelScope | AIStudio | BOS |
|---|---|---|---|---|---|
| `PP-DocLayoutV2` | layout detection | `PaddlePaddle/PP-DocLayoutV2` | `PaddlePaddle/PP-DocLayoutV2` | `PaddleX/PP-DocLayoutV2` | `.../official_inference_model/paddle3.0.0/PP-DocLayoutV2_infer.tar` |
| `PaddleOCR-VL-0.9B` | vision-language recognition | `PaddlePaddle/PaddleOCR-VL-0.9B` | `PaddlePaddle/PaddleOCR-VL-0.9B` | `PaddleX/PaddleOCR-VL-0.9B` | same base URL pattern |

(Exact repo IDs/URLs read directly from
`paddlex/inference/utils/official_models.py`, not guessed.)

**Every route tried, for real, today:**
1. `PaddleOCRVL()` construction (paddlex's own orchestration) — fails at
   `PP-DocLayoutV2` resolution: `Exception: No available model hosting
   platforms detected.`
2. `PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK=True` — skips the pre-flight
   check, but the real download attempt that follows fails the same way.
3. Direct `huggingface_hub.snapshot_download(repo_id="PaddlePaddle/PP-DocLayoutV2")`
   — `ProxyError 403 Forbidden`.
4. Direct `modelscope.snapshot_download(repo_id="PaddlePaddle/PP-DocLayoutV2")`
   — proxy tunnel to `modelscope.cn` returns `403 Forbidden`.
5. Direct `aistudio_sdk.snapshot_download(repo_id="PaddleX/PP-DocLayoutV2")`
   — proxy tunnel to `git.aistudio.baidu.com` returns `403 Forbidden`.
6. Direct BOS tar download
   (`https://paddle-model-ecology.bj.bcebos.com/paddlex/official_inference_model/paddle3.0.0/PP-DocLayoutV2_infer.tar`
   via plain `requests.get`) — proxy tunnel returns `403 Forbidden`.
7. Checked for any bundled model weights inside the installed
   `paddleocr`/`paddlex` packages themselves (the way Docling's RapidOCR
   bundles ONNX weights) — none exist; checked for any pre-existing local
   model cache (`~/.paddlex`, `~/.cache`) — none exists beyond empty lock
   files.

**Conclusion:** all 4 documented model-hosting platforms are blocked at
the network/proxy layer specifically, not by any paddlex application
logic — the same organization-wide egress policy documented elsewhere in
this project (Docling's Hugging Face block, etc.). This is a network
reachability fact, not a bug in PaddleOCR-VL or a configuration mistake
on this project's part. No fabricated output was produced; no bundled
or cached model substitute exists to fall back on.

**What would unblock this:** the same mechanism already explored for
Docling's layout model — someone with unrestricted network access
downloads `PP-DocLayoutV2` and `PaddleOCR-VL-0.9B` (repo IDs above) and
supplies the resulting model directories into this environment (e.g. via
Git LFS), then `model_dir` in `paddlex/configs/pipelines/PaddleOCR-VL.yaml`
(or the equivalent init kwarg) is pointed at them directly, skipping the
download step entirely. Not attempted in this pass without being asked,
given the earlier Docling model-transfer attempt's difficulties this
session.
