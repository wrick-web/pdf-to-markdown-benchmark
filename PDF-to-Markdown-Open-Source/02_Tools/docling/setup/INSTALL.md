# Docling — install notes (Round 1, Rev-2 execution attempt)

Installed cleanly. Nothing below failed at install time — the failures
documented in `../logs/` happen later, at first pipeline use (model
download), not during `pip install`.

## Commands run

```bash
cd /home/user/pdf-to-markdown-benchmark
uv venv .venv_docling
uv pip install docling --python .venv_docling/bin/python
uv pip install onnxruntime --python .venv_docling/bin/python   # see "OCR fix" below
```

## Versions actually installed (2026-09-03)

| Package | Version |
|---|---|
| docling | 2.124.0 |
| docling-core | 2.93.0 |
| docling-ibm-models | 4.0.1 |
| docling-parse | 7.17.0 |
| docling-slim | 2.124.0 |
| torch | 2.14.0 |
| torchvision | 0.29.0 |
| transformers | 5.16.1 |
| rapidocr | 3.9.2 |
| onnxruntime | 1.29.0 |

Python: 3.11.15 (the environment's system interpreter, via `uv venv`).

## What Docling needs at runtime beyond the pip install

Docling's `StandardPdfPipeline` does not ship its models — it loads two
of them the first time a pipeline is constructed, and by default both
require an internet download:

1. **OCR** — see "OCR fix" below; **solved**, no download needed.
2. **Layout** (object detection — headings, tables, reading order,
   figures; always loaded regardless of `do_ocr`): needs
   `docling-project/docling-layout-heron` (or any of its sibling
   presets — Heron-101, Egret medium/large/xlarge, all equally
   HF-hosted) from the Hugging Face Hub via
   `huggingface_hub.snapshot_download` / `hf_api.model_info`. **Not
   solved** — see "Layout: confirmed unavailable" below.

### OCR fix (solved, 2026-09-03)

Docling's default OCR path uses RapidOCR's **PyTorch** backend, which
downloads `PP-OCRv6_det_small.pth` from
`https://www.modelscope.cn/models/RapidAI/RapidOCR/...` — blocked here.
But the `rapidocr` PyPI wheel (already installed, from PyPI, which
works fine in this sandbox) **bundles ONNX versions of the same models
directly in the package**:

```
.venv_docling/lib/python3.11/site-packages/rapidocr/models/
├── ch_ppocr_mobile_v2.0_cls_mobile.onnx
├── PP-OCRv6_det_small.onnx
└── PP-OCRv6_rec_small.onnx
```

`RapidOcrOptions` (Docling's own options class) already defaults its
`backend` field to `'onnxruntime'` — Docling just wasn't using that
default in practice because the `onnxruntime` Python package itself
wasn't installed, so RapidOCR fell through to its `torch` engine
instead. Installing `onnxruntime` (a plain PyPI package, no external
model download) and explicitly passing the option fixes it completely,
with **zero network calls**:

```python
from docling.datamodel.pipeline_options import PdfPipelineOptions, RapidOcrOptions
opts = PdfPipelineOptions()
opts.ocr_options = RapidOcrOptions(backend="onnxruntime")
```

Verified real: running this against the real `briefing_note_BEP-BN-2026-04.pdf`
fixture, OCR model construction now succeeds and execution proceeds
past it — the pipeline gets measurably further than before. See
`../logs/TC27_briefing_note_ocr_fixed_still_blocked_layout.log`.

### Exact offline model spec (2026-09-03, requested by the user)

Derived by reading Docling's own source — `docling/datamodel/
stage_model_specs.py` (the `OBJECT_DETECTION_LAYOUT_HERON` preset,
which is `layout_heron_default`, the one `DocumentConverter()` uses by
default), `docling/models/inference_engines/common/hf_vision_base.py`,
and `docling/models/inference_engines/vlm/_utils.py`
(`resolve_model_artifacts_path`) — not guessed, not inferred from docs.

- **Exact model**: Hugging Face repo `docling-project/docling-layout-heron`
  (an RT-DETR object-detection model, ResNet50 backbone), revision `main`.
- **Exact files actually read by the code that runs** (confirmed by
  tracing every call in `transformers_engine.py`'s `initialize()`):
  - `config.json` — read by `AutoConfig.from_pretrained()` for the
    model's label mapping (`id2label`) and by
    `AutoModelForObjectDetection.from_pretrained()` for the model
    architecture.
  - `preprocessor_config.json` — read by `AutoImageProcessor.
    from_pretrained()`; `hf_vision_base.py` raises `FileNotFoundError`
    immediately if this is missing.
  - The model weights — `model.safetensors` (transformers' current
    default format) or `pytorch_model.bin` (older format; either
    works, `from_pretrained` auto-detects).
  - Nothing else is read by the code path this pipeline actually
    exercises (no tokenizer files — this is vision-only; no custom
    `trust_remote_code` — RT-DETR is natively supported in
    `transformers`, confirmed by a comment in Docling's own source
    referencing "RT-DETRv2 in transformers 5.x").
- **Exact directory structure `artifacts_path` must have** (from
  `resolve_model_artifacts_path`'s literal logic:
  `artifacts_path / repo_id.replace("/", "--")`):
  ```
  <artifacts_path>/
  └── docling-project--docling-layout-heron/
      ├── config.json
      ├── preprocessor_config.json
      └── model.safetensors        (or pytorch_model.bin)
  ```
- **How to obtain it** (needs a machine with real Hugging Face access —
  this sandbox does not have one): `huggingface-cli download
  docling-project/docling-layout-heron --local-dir
  docling-project--docling-layout-heron`, or simply let Docling run
  once normally on any unrestricted machine and copy the resulting
  cache folder. Either way, the folder just needs to end up named
  exactly `docling-project--docling-layout-heron` inside whatever
  directory gets passed as `artifacts_path`.
- **How to use it here**: `scripts/run_docling.py` now reads a
  `DOCLING_ARTIFACTS_PATH` env var and passes it straight through as
  `PdfPipelineOptions.artifacts_path` — supply the model directory into
  this session, set that env var to its parent folder, and the script
  needs no other change.
- **Smaller alternative**: an ONNX export also exists at
  `docling-project/docling-layout-heron-onnx` (`model.onnx` instead of
  `.safetensors`, same `config.json`/`preprocessor_config.json`
  requirement, folder name `docling-project--docling-layout-heron-onnx`)
  — usable via `ObjectDetectionEngineType.ONNXRUNTIME`, which
  `onnxruntime` (already installed here) can run. Either variant works;
  the safetensors one is simpler since `DocumentConverter()` uses it
  with zero extra configuration beyond `artifacts_path`.

### Layout: confirmed unavailable (2026-09-03)

With the OCR fix in place, the pipeline's next (and last) step —
loading the layout model — is where every run now fails. This was
checked exhaustively rather than assumed, across every source this
sandbox can reach:

1. **Source review**: `docling/datamodel/layout_model_specs.py` lists
   every layout preset Docling ships (Heron, Heron-101, Egret
   medium/large/xlarge) — every single one has `repo_id` pointing at
   `docling-project/docling-layout-*` on the Hugging Face Hub. No
   preset has a non-HF source.
2. **No bundled weights**: searched every installed package
   (`docling`, `docling-core`, `docling-ibm-models`, `docling-parse`,
   `docling-slim`) for `.onnx`/`.pt`/`.pth`/`.safetensors`/`.bin` files
   — only RapidOCR's 3 OCR files exist; nothing for layout.
   `docling-ibm-models` ships `tableformer` (table structure) code only,
   no layout module at all.
3. **Not on PyPI**: `https://pypi.org/pypi/docling-layout-heron/json` →
   404. No package mirrors the weights.
4. **Not on GitHub**: tried the model as a standalone GitHub repo under
   `docling-project/` and `DS4SD/` (IBM's original org) via
   `raw.githubusercontent.com` — all 404 (a real "repo/branch doesn't
   exist" response, not a proxy block; `raw.githubusercontent.com` and
   `github.com` are otherwise reachable from this sandbox — confirmed
   by successfully fetching Docling's actual public README).
5. **huggingface.co itself**: blocked — `httpx.ProxyError: 403
   Forbidden` (confirmed repeatedly this project, including today).
6. **hf-mirror.com** (a known third-party HF mirror, a completely
   different domain): also blocked (`connect_rejected` at the proxy).
   This confirms the sandbox's policy is an **allowlist** of specific
   package registries (PyPI, npm, crates, Go proxy, GitHub content),
   not a blocklist of named-bad hosts — so no as-yet-untried mirror
   domain is likely to work either.
7. **Live re-test**: ran the OCR-fixed pipeline against the real TC27
   fixture end-to-end — confirmed it now fails specifically and only at
   `huggingface_hub.snapshot_download` for the layout model, not OCR.

**Conclusion:** the layout model has exactly one source (Hugging Face
Hub) and that host is blocked by this sandbox's organization network
policy, with no bundled, PyPI, or GitHub-mirrored alternative anywhere
this environment can reach. This is not a missing-dependency or
missing-configuration problem — it's a genuine, structural requirement
of Docling's real pipeline that this specific sandbox cannot satisfy.

## What would fully unblock this

`docling`'s own CLI supports exactly this situation:
```bash
docling-tools models download --output-dir /models   # needs HF access — can't run here
docling report.pdf --artifacts-path /models --output /tmp/
```
If someone with real internet access runs `docling-tools models
download` (or just lets Docling run once normally) on any machine that
can reach Hugging Face, zips the resulting model cache, and supplies it
into this session the same way the benchmark PDFs were supplied, this
sandbox could point `PdfPipelineOptions.artifacts_path` at it and skip
the download step entirely — for OCR (already solved) and layout both.

## Fixture status

The 11 benchmark PDFs live in ClickUp task `86bbr4dmu`; the attachment
CDN (`t9014651757.p.clickup-attachments.com`) is blocked from this
sandbox (confirmed repeatedly, most recently this session), and Gmail
carries no attachment path either. 5 of the 11 (TC27–TC31's fixtures)
were supplied directly into this session by the user and are the real
files under `../input/`. The remaining 6 (TC32–TC38) have not been
supplied.
