# GLM-OCR (zai-org)

- Repo: https://github.com/zai-org/GLM-OCR
- License: Apache-2.0 (confirmed via raw `LICENSE` and PyPI `glmocr` v0.1.5 metadata); layout stage (PP-DocLayoutV3) also Apache-2.0
- 2026 release, ~7.4k stars

## Why it's compelling
Compact (0.9B params: GLM-V CogViT vision encoder + GLM-0.5B decoder),
two-stage layout->parallel-recognition pipeline. The layout stage can run
on CPU; only the recognition VLM stage benefits from GPU. Dual-license-clean
(both stages Apache-2.0) — no OpenRAIL-style commercial carve-out to worry
about, unlike Chandra/Surya.

## Requirements
- Hugging Face Hub for weights
- GPU recommended for the recognition stage (vLLM/SGLang deployment offered); layout stage alone is CPU-capable

## Reproduce on an unrestricted machine
```bash
pip install glmocr[selfhosted]
glmocr convert path/to/file.pdf --output out_dir/ --format markdown
```

## Blocked here because
Hugging Face Hub required for weights; blocked in this sandbox.
