# LiteParse

Rust-backed PDF/document parser, PyPI `liteparse` (github.com/run-llama/liteparse), RunLlama/LlamaIndex team. Apache-2.0.

Native Markdown output, no external ML model download for text/table/heading extraction. Scanned-page OCR uses Tesseract; by default it tries to download tessdata from GitHub (blocked in this sandbox), but this project's already-installed `tesseract-ocr-eng` (apt, from the Kreuzberg setup) works via `tessdata_path` - see `scripts/run_liteparse.py`.

Status: genuinely executed against all 5 available TC27-31 fixtures. See `logs/`, `markdown_output/`, `raw_output/` for real evidence, and ClickUp TC27-31 observation subtasks under the LiteParse execution task for the scored write-up.
