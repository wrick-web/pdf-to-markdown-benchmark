#!/usr/bin/env python3
"""
Run LiteParse (PyPI `liteparse`, github.com/run-llama/liteparse - Rust-backed
PDF/document parser with native Markdown output, RunLlama/LlamaIndex team)
against a benchmark PDF.

Usage:
    source .venv_liteparse/bin/activate
    python run_liteparse.py <input.pdf> <tool_output_dir>
"""
import json
import sys
import time
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: run_liteparse.py <input.pdf> <tool_output_dir>")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    stem = pdf_path.stem

    md_dir = out_dir / "markdown_output"
    raw_dir = out_dir / "raw_output"
    log_dir = out_dir / "logs"
    img_dir = out_dir / "extracted_images"
    for d in (md_dir, raw_dir, log_dir, img_dir):
        d.mkdir(parents=True, exist_ok=True)

    log_lines = [
        f"input: {pdf_path}",
        "config: LiteParse(output_format='markdown'), everything else default",
        f"started: {time.strftime('%Y-%m-%d %H:%M:%S')}",
    ]

    t0 = time.time()
    error = None
    result = None
    try:
        import liteparse
        log_lines.insert(0, f"liteparse version: {liteparse.__version__}")
        from liteparse import LiteParse

        # LiteParse's default OCR path tries to download tessdata from
        # GitHub on first use, which is blocked in this sandbox
        # (HTTP 403). tesseract-ocr-eng is already installed via apt for
        # Kreuzberg; pointing tessdata_path at it avoids the download
        # entirely - a local config fix, not a workaround.
        import os
        tessdata_path = "/usr/share/tesseract-ocr/5/tessdata"
        parser = LiteParse(
            output_format="markdown",
            tessdata_path=tessdata_path if os.path.isdir(tessdata_path) else None,
            extract_images=True,
            image_output_dir=str(img_dir),
            image_mode="embed",
        )
        result = parser.parse(str(pdf_path))
    except Exception as exc:  # noqa: BLE001
        error = repr(exc)
    elapsed = time.time() - t0
    log_lines.append(f"elapsed_seconds: {elapsed:.2f}")

    if error:
        log_lines.append(f"ERROR: {error}")
        (log_dir / f"{stem}.log").write_text("\n".join(log_lines), encoding="utf-8")
        print(f"[liteparse] FAILED on {pdf_path.name}: {error}")
        sys.exit(2)

    md_text = result.text
    (md_dir / f"{stem}.md").write_text(md_text, encoding="utf-8")

    raw_record = {
        "tool": "liteparse",
        "liteparse_version": liteparse.__version__,
        "input_file": str(pdf_path),
        "elapsed_seconds": elapsed,
        "total_pages": result.total_pages,
        "content_char_count": len(md_text),
    }
    (raw_dir / f"{stem}.json").write_text(json.dumps(raw_record, indent=2, default=str), encoding="utf-8")

    log_lines.append(f"total_pages: {result.total_pages}")
    log_lines.append(f"content_char_count: {len(md_text)}")
    (log_dir / f"{stem}.log").write_text("\n".join(log_lines), encoding="utf-8")

    print(f"[liteparse] OK {pdf_path.name}: {elapsed:.1f}s, {result.total_pages} pages, {len(md_text)} chars")


if __name__ == "__main__":
    main()
