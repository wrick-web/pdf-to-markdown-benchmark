# Reproducibility Guide

Everything below reproduces this cycle's results exactly, or extends them
to the tools this sandbox couldn't run.

## 0. Prerequisites

- Python 3.11, `uv` (or plain `pip`)
- `apt-get install tesseract-ocr tesseract-ocr-eng` (for Kreuzberg's OCR backend)
- The 3 benchmark PDFs in `01_Benchmark_PDFs/` (already present in this repo)

## 1. Re-run Kreuzberg (tested this cycle)

```bash
cd PDF-to-Markdown-Open-Source
uv venv .venv_kreuzberg --python 3.11
source .venv_kreuzberg/bin/activate
uv pip install -r 02_Tools/kreuzberg/setup/requirements.txt

for f in 01_Benchmark_PDFs/*.pdf; do
  python 04_Scripts/conversion/run_kreuzberg.py "$f" 02_Tools/kreuzberg
done
```
Outputs land in `02_Tools/kreuzberg/{markdown_output,raw_output,extracted_images,logs}/`.

## 2. Re-run open-parse (tested this cycle, base mode)

```bash
cd PDF-to-Markdown-Open-Source
uv venv .venv_openparse --python 3.11
source .venv_openparse/bin/activate
uv pip install openparse

for f in 01_Benchmark_PDFs/*.pdf; do
  python 04_Scripts/conversion/run_openparse.py "$f" 02_Tools/open-parse
done
```
Note: `run_openparse.py` includes a documented `tiktoken.get_encoding`
monkeypatch (see the script's docstring) needed in any network-restricted
environment; harmless to leave in place on an unrestricted machine too
(it only changes an internal token-count heuristic, not extraction
behavior), or remove it if you have working internet access to
`openaipublic.blob.core.windows.net`.

## 3. Extend to PaddleOCR-VL (needs Hugging Face Hub or BOS access)

```bash
uv venv .venv_paddleocr --python 3.11
source .venv_paddleocr/bin/activate
uv pip install "paddleocr[doc-parser]"
python - <<'EOF'
from paddleocr import PPStructureV3
p = PPStructureV3()
for pdf in ["01_Benchmark_PDFs/PDF1_Hybrid_Earnings_Report_Target2015.pdf",
            "01_Benchmark_PDFs/PDF2_Financial_Report_Sumitomo.pdf",
            "01_Benchmark_PDFs/PDF3_Scanned_Research_Paper.pdf"]:
    for res in p.predict(pdf):
        res.save_to_markdown("02_Tools/paddleocr-vl/markdown_output/")
EOF
```
If Hugging Face is unreachable but Baidu Object Storage is:
`PADDLE_PDX_MODEL_SOURCE=BOS` before running.

## 4. Extend to huridocs/pdf-document-layout-analysis (needs Docker)

See `02_Tools/huridocs-pdf-document-layout-analysis/setup/RUN.md` for the
exact `docker run` + `curl` sequence.

## 5. Extend to any Tier B tool (needs GPU + Hugging Face Hub, at minimum)

Each has a ready install/run command block in
`02_Tools/_prepared_not_run/<tool>.md` — copy the commands, point them at
the 3 files in `01_Benchmark_PDFs/`, and save outputs into a new
`02_Tools/<tool>/{markdown_output,raw_output,logs}/` following the same
folder convention as Kreuzberg/open-parse above, so results stay directly
comparable.

## 6. Regenerate the scoring/comparison docs

There is no separate "scoring script" — scores in
`03_Benchmark_Results/MASTER_RESULTS.md` were assigned manually against
the 0-5 rubric in `00_Project_Notes/Methodology.md`, backed by the
quantitative signals each `run_<tool>.py` script already saves (character
counts, table/image counts, warnings) plus a manual read-through of the
Markdown output against the source PDF. To reproduce a score, re-read the
relevant `observations.md` section and the underlying `raw_output/*.json`
and `markdown_output/*.md` files referenced there.

## 7. Environment notes if you hit different results

- Kreuzberg version pin: `kreuzberg==4.10.2`. The upstream project is
  actively rebranding to "Xberg" — a later version might change default
  behavior (e.g., table detection). Re-check `docs.xberg.io` if results
  drift from what's recorded here.
- open-parse version pin: `openparse==0.7.0`.
- Tesseract version used: 5.3.4 (Ubuntu 24.04/"noble" apt package).
