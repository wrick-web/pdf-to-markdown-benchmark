# LiteParse

Rust-backed PDF/document parser, PyPI `liteparse` (github.com/run-llama/liteparse), RunLlama/LlamaIndex team. Apache-2.0.

Native Markdown output, no external ML model download for text/table/heading extraction. Scanned-page OCR uses Tesseract; by default it tries to download tessdata from GitHub (blocked in this sandbox), but this project's already-installed `tesseract-ocr-eng` (apt, from the Kreuzberg setup) works via `tessdata_path` - see `scripts/run_liteparse.py`.

Status: genuinely executed against 6 of 13 test cases (TC27-31, TC33-34) — real Markdown output, logs and terminal-capture evidence for each. TC32/TC115/TC35-38 remain BLOCKED: their 6 fixtures aren't retrievable from this sandbox (ClickUp attachment CDN returns 403), re-verified fresh, per-file, this pass. Full per-TC write-up (Input/Execution/Expected/Observed/Output/Evidence/Observation/Verdict) in `observations.md`. Nothing posted to ClickUp yet — pending user review, same as the Docling task's pattern.
