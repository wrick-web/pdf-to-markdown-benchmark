# Kreuzberg — Setup

- **Repo:** https://github.com/Goldziher/kreuzberg (project is mid-rebrand to `xberg-io/xberg` on GitHub; PyPI package name is still `kreuzberg`)
- **Docs:** https://docs.xberg.io/
- **License:** MIT
- **Version tested:** `kreuzberg==4.10.2` (PyPI, 2026-08-28)
- **Language:** Rust core, Python bindings (also Ruby/Java/Go/PHP/Elixir/C#/TS)

## System dependency

Kreuzberg's Tesseract OCR backend shells out to a real `tesseract` binary —
install it via the OS package manager (this does **not** need Hugging Face
or any blocked host, just the Ubuntu/Debian archive):

```bash
apt-get update
apt-get install -y tesseract-ocr tesseract-ocr-eng
tesseract --version   # sanity check — this project used 5.3.4
```

## Python environment

```bash
uv venv .venv_kreuzberg --python 3.11
source .venv_kreuzberg/bin/activate
uv pip install -r requirements.txt   # kreuzberg==4.10.2
```

(Plain `pip install kreuzberg` also works if you're not using `uv`.)

## Notes from this run

- No Hugging Face Hub access was required for the configuration used in
  this benchmark (`layout=LayoutDetectionConfig(apply_heuristics=True,
  table_model="tatr")` ran successfully fully offline in this sandbox —
  it either bundles its ONNX assets in the wheel or the TATR path silently
  no-ops without downloaded weights; table detection returned 0 tables on
  every benchmark PDF here, which is itself a recorded finding — see
  `observations.md`; on a machine with Hugging Face access it is worth
  re-testing whether TATR performs differently once its weights are
  actually fetched).
- Kreuzberg also supports PaddleOCR-ONNX, a pure-Rust "Candle" backend, and
  a VLM-router backend (165+ providers) as alternative OCR engines — only
  the Tesseract backend was exercised in this cycle.
- The exact extraction config used is saved in `../config/extraction_config.md`
  and the runnable script is `04_Scripts/conversion/run_kreuzberg.py`
  (also copied to `../scripts/run_kreuzberg.py`).
