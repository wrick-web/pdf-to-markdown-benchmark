# olmOCR environment investigation (2026-10-01)

## What olmOCR is
`olmocr` (Allen Institute for AI) is a PDF-linearization toolkit built around a
7-billion-parameter vision-language model (`allenai/olmOCR-2-7B-1025-FP8`,
hosted on Hugging Face Hub). Its CLI (`olmocr <workspace> --pdfs ...`) renders
each PDF page to an image and sends it through the VLM to produce Markdown.

Source: https://github.com/allenai/olmocr , https://pypi.org/project/olmocr/

## Installation actually performed
```
$ python3.11 -m venv .venv_olmocr
$ .venv_olmocr/bin/pip install olmocr
Successfully installed ... olmocr-0.4.27 ...
```
- olmocr version installed: **0.4.27** (latest on PyPI at time of install)
- Python version: **3.11.15** (meets the documented `>=3.11` requirement)
- System dependency `poppler-utils` was missing in this fresh container;
  installed via `apt-get install -y poppler-utils` (confirmed working by
  olmOCR's own startup check: `pdftoppm is installed and working.`)
- Base `pip install olmocr` does **not** include PyTorch (confirmed: first run
  failed with `ModuleNotFoundError: No module named 'torch'`).
- Installed `torch` directly from PyPI (not the CUDA-specific
  `download.pytorch.org` index, which is blocked — see below):
  `torch-2.14.1+cu130`.

## The hard blocker: no GPU in this sandbox
```
$ .venv_olmocr/bin/python -c "import torch; print(torch.cuda.is_available())"
False
```
olmOCR's own pipeline runs a pre-flight check (`check_torch_gpu_available()`)
before touching the model or any PDF content. Real, unedited output from a
genuine run attempt:

```
ERROR:olmocr.check:Torch was not able to find a GPU with at least 15 GB of RAM.
...
RuntimeError: Found no NVIDIA driver on your system. Please check that you
have an NVIDIA GPU and installed a driver from http://www.nvidia.com/Download/index.aspx
```
Full raw log: `gpu_check_failure_20261001.log` (same directory).

This check runs identically regardless of which PDF or scenario is passed —
it happens at startup, before any model download or page processing. It is
not fixture-specific and not something a different PDF would change.

## Why this can't be worked around
- **Official requirement, not a soft recommendation**: the README states the
  tool "is based on a 7B parameter VLM, so it requires a GPU" with a minimum
  of 12 GB VRAM (olmOCR's own check wants ≥15 GB). No documented genuine
  CPU-only inference path exists for actual document processing (the
  `[bench]` extra is for olmOCR's own internal benchmark suite, not for
  running the OCR pipeline on arbitrary PDFs).
- **This sandbox has no NVIDIA GPU at all** (`nvidia-smi` not found; PyTorch's
  own CUDA init reports "no NVIDIA driver").
- **Independently, the model host is also blocked**: `allenai/olmOCR-2-7B-1025-FP8`
  is hosted on Hugging Face Hub, and `huggingface.co` returns the same
  organization-wide `connect_rejected`/403 seen for every other tool this
  session that needed a Hugging Face model download (PaddleOCR-VL, MinerU,
  etc.) — confirmed fresh via the proxy's own status endpoint
  (`recentRelayFailures` entry for `huggingface.co:443`, timestamp
  2026-10-01T04:49:49Z).
- **Remote-server mode** (`olmocr ... --server <url> --api_key <key>`) exists
  and would skip local GPU use, but requires a real, already-running
  vLLM/sglang inference server. No such server is available, authorized, or
  documented as a public endpoint for this benchmark — standing up one would
  itself require a GPU host we don't have, and inventing/using an
  unauthorized third-party endpoint is out of scope.

## Conclusion
Two independent, genuine blockers (no GPU hardware; model host blocked) —
either alone would already prevent real execution. This applies identically
to all six scenarios in this run: **CAN NOT BE GRADED** for every TC, with
this shared evidence cited on each one, since the failure occurs before any
scenario-specific PDF is ever touched.
