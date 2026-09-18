# PaddleOCR-VL — Observations

Repo: https://github.com/PaddlePaddle/PaddleOCR · PyPI `paddleocr[doc-parser]==3.7.0` (confirmed latest on PyPI as of 2026-09-18) · Apache-2.0.
**Status: attempted-blocked (reconfirmed fresh, 2026-09-18).** Installs cleanly. Model acquisition for the current `PaddleOCRVL` pipeline (default `pipeline_version="v1.6"` → model name **PaddleOCR-VL-1.6**, VL component **PaddleOCR-VL-1.6-0.9B**, layout model **PP-DocLayoutV3**) is blocked at the network/egress-proxy layer for all 4 documented model-hosting platforms. 0 of 7 canonical benchmark PDFs could be processed.

This file distinguishes two separate execution rounds. **The CURRENT round (2026-09-18) is what TC27–TC38/TC115's ClickUp observations and verdicts are based on.** The historical round is preserved below for context only.

---

## CURRENT EXECUTION — 2026-09-18

### Version/environment (real, checked today — not assumed)
- `paddleocr==3.7.0` — confirmed this is the current latest release on PyPI today via `pip index`/PyPI JSON API (`https://pypi.org/pypi/paddleocr/json`); no newer release exists.
- `paddlex==3.7.2`
- Python 3.11.15, fresh `uv venv .venv_paddleocr`
- OS: Ubuntu 24.04.4 LTS, `Linux vm 6.18.44-fc-v33 x86_64`, 4 CPU cores
- No GPU/CUDA on this host (`nvidia-smi` not found)
- `paddlepaddle` deep-learning framework **not installed** and not required by the `doc-parser` extra (Transformers-style stack instead — confirmed `ModuleNotFoundError: No module named 'paddle'` is expected, not an error)
- No `torch`/`transformers`/`onnxruntime`/`vllm` installed either (native VLM backend dependencies not pulled in until model files are actually resolved)

### Confirming "PaddleOCR-VL-1.6 is current" from source, not from the request's claim
Read `paddleocr/_pipelines/paddleocr_vl.py` directly from the installed 3.7.0 package:
```python
_AVAILABLE_PIPELINE_VERSIONS = ["v1", "v1.5", "v1.6"]
_DEFAULT_PIPELINE_VERSION = "v1.6"
...
if self.pipeline_version == "v1.6":
    return "PaddleOCR-VL-1.6"
```
and `paddlex/inference/utils/official_models.py`, which maps pipeline version `v1.6` to VL recognition model `PaddleOCR-VL-1.6-0.9B` and layout model `PP-DocLayoutV3`. This independently verifies (does not merely trust) that PaddleOCR-VL-1.6 is genuinely the current default in the latest PyPI release as of 2026-09-18.

### Model-acquisition attempts (real, today)
1. **Default construction** (`PaddleOCRVL()`, Hugging Face Hub source):
   ```
   Creating model: ('PP-DocLayoutV3', None, None)
   No model hoster is available! ... HuggingFace / ModelScope / AIStudio / BOS ...
   Exception: No available model hosting platforms detected. Please check your network connection.
   ```
2. **`PADDLE_PDX_MODEL_SOURCE=BOS` fallback** — identical failure, same pre-flight connectivity check fails before any host-specific attempt.
3. **`PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK=True`** (skips the pre-flight check and lets the real per-host download attempts run) — this is the most informative run, genuinely exercising all 4 documented hosts in one execution:
   - HuggingFace: `403 Forbidden`
   - AIStudio (`git.aistudio.baidu.com`): proxy tunnel `403 Forbidden`
   - ModelScope (`modelscope.cn`): proxy tunnel `403 Forbidden`
   - BOS (`paddle-model-ecology.bj.bcebos.com`): `No model source is available! Please check network or use local model files!`
   - Full transcript: `attach_staging/TC27_all4_hosts_exhaustive_bypass_attempt_20260918.log`
4. **Direct proxy status check** (`curl $HTTPS_PROXY/__agentproxy/status` + direct `curl` to each of the 4 hosts) — every host returns `curl: (56) CONNECT tunnel failed, response 403` with explicit reason `connect_rejected (the egress proxy denied the CONNECT (organization policy))`. This confirms the block is an organization-level egress policy, not a transient network fault or an application bug.
5. Ran the exact same default-construction attempt against all 7 canonical fixtures individually (TC27, TC28, TC29 [correct 43,662-byte variant], TC30, TC31, TC33/34, TC38) — **every single one fails identically at model construction, before the PDF is ever opened.** Per-fixture logs: `attach_staging/TC*_CURRENT_20260918_BLOCKED.log`.
6. Freshly retested (not assumed from history) the 4 fixtures previously found unreachable via ClickUp's attachment CDN for TC32/TC115, TC35, TC36, TC37 (`monitoring_station_schedule_2026.pdf`, `certificate_of_analysis_KAL-11938.pdf`, `service_report_KAL-ESR-4471.pdf`, `technical_note_TIH-TN-18.pdf`) — all 4 still return `curl: (56) CONNECT tunnel failed, response 403` today. Full transcript: `attach_staging/TC32_TC35_TC36_TC37_fixture_retest_20260918.log`. Note this is a **separate, independent blocker** from model acquisition — even had these fixtures been retrievable, PaddleOCR-VL still could not process them today because the model itself cannot load.

### Local model cache / bundled weights check
No pre-existing model cache found (`~/.paddlex` empty of weights), no `.onnx`/`.safetensors`/`.pdiparams` files bundled inside the installed `paddleocr`/`paddlex` packages. No fallback local-model path is available.

### Conclusion (current round)
All 4 documented model-hosting platforms for the current `PaddleOCR-VL-1.6` pipeline are blocked at the network/egress-proxy layer, confirmed fresh today with genuine, dated evidence — not copied forward from the historical attempt. Because model construction fails before any PDF is touched, **every TC27–TC38/TC115 scenario is CAN NOT BE GRADED** for this round: the tool never executed against any fixture, so no PASS/FAIL verdict is supportable.

---

## HISTORICAL EXECUTION — 2026-08-28 / 2026-09-08 (context only, not the basis for current ClickUp verdicts)

Earlier attempts in this project used the older `PPStructureV3` 6+-model classical structure pipeline (not the dedicated `PaddleOCRVL` class) and the older `PP-DocLayoutV2` layout model (superseded by `PP-DocLayoutV3` in the pipeline's current default). Findings were the same in substance: both the default (Hugging Face) and `PADDLE_PDX_MODEL_SOURCE=BOS` model sources failed identically with `Exception: No available model hosting platforms detected. Please check your network connection.` — 0 of 5 fixtures tested successfully. A 2026-09-08 deep-dive (`logs/model_acquisition_retry_20260908.log`) went further and tried direct `huggingface_hub`/`modelscope`/`aistudio_sdk`/BOS downloads bypassing the `PPStructureV3`/`PaddleOCRVL` wrapper entirely — all 4 routes failed with `403 Forbidden` at the proxy layer, confirming the same conclusion this current round reaches independently.

One fixture used in that historical round, `input/procedure_KAL-SP-06_sample_reception.pdf` (128,546 bytes), was later discovered to be the **wrong, non-canonical variant** — the authoritative TC29 fixture is `procedure_KAL-SP-06_sample_reception_43662.pdf` (43,662 bytes). This has been corrected for the current round (wrong file moved to `input/_wrong_variant_not_used/`, correct file sourced and sha256-verified against the authoritative fixture task).

- `logs/init_attempt_default.log`, `logs/init_attempt_bos_fallback.log` — 2026-08-28 initial attempts
- `logs/*_run_20260908_*.log`, `logs/model_acquisition_retry_20260908.log` — 2026-09-08 extended retry
- `setup/INSTALL.md` — full historical narrative and reproduction instructions

## Reproducing this on an unrestricted machine

```bash
uv venv .venv_paddleocr --python 3.11
source .venv_paddleocr/bin/activate
uv pip install "paddleocr[doc-parser]"
python - <<'EOF'
from paddleocr import PaddleOCRVL
p = PaddleOCRVL()  # default pipeline_version="v1.6"
result = p.predict("path/to/file.pdf")
for res in result:
    res.save_to_markdown("output_dir/")
EOF
```
If Hugging Face Hub is unreachable but Baidu Object Storage is, set
`PADDLE_PDX_MODEL_SOURCE=BOS` before running.
