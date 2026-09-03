#!/usr/bin/env python3
"""
Run Docling (docling==2.124.0, github.com/docling-project/docling) against
a benchmark PDF.

STATUS AS WRITTEN (2026-09-03): this script has never completed a
successful run in this sandbox. Docling's StandardPdfPipeline downloads
its models on first use — RapidOCR/PyTorch OCR weights from
modelscope.cn, and the docling-layout-heron layout model from the
Hugging Face Hub — and both hosts are blocked by this environment's
network egress policy. See ../logs/pipeline_init_default_ocr.log and
../logs/pipeline_init_ocr_disabled.log for the two real tracebacks this
produces. This script is left ready to run as-is the moment either (a)
model access is available, or (b) a machine with unrestricted egress
runs it.

Usage:
    source .venv_docling/bin/activate
    python run_docling.py <input.pdf> <tool_output_dir>
"""
import json
import sys
import time
from pathlib import Path

import docling
from docling.document_converter import DocumentConverter


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: run_docling.py <input.pdf> <tool_output_dir>")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    stem = pdf_path.stem

    raw_dir = out_dir / "raw_output"
    md_dir = out_dir / "markdown_output"
    img_dir = out_dir / "extracted_images"
    log_dir = out_dir / "logs"
    for d in (raw_dir, md_dir, img_dir, log_dir):
        d.mkdir(parents=True, exist_ok=True)

    log_lines = [
        f"docling version: {docling.__version__}",
        f"input: {pdf_path}",
        "config: default StandardPdfPipeline (no options overridden)",
        f"started: {time.strftime('%Y-%m-%d %H:%M:%S')}",
    ]

    t0 = time.time()
    error = None
    result = None
    try:
        converter = DocumentConverter()
        result = converter.convert(str(pdf_path))
    except Exception as exc:  # noqa: BLE001
        error = repr(exc)
    elapsed = time.time() - t0
    log_lines.append(f"elapsed_seconds: {elapsed:.2f}")

    if error:
        log_lines.append(f"ERROR: {error}")
        (log_dir / f"{stem}.log").write_text("\n".join(log_lines), encoding="utf-8")
        print(f"[docling] FAILED on {pdf_path.name}: {error}")
        sys.exit(2)

    doc = result.document
    md_text = doc.export_to_markdown()
    (md_dir / f"{stem}.md").write_text(md_text, encoding="utf-8")

    raw_record = {
        "tool": "docling",
        "docling_version": docling.__version__,
        "input_file": str(pdf_path),
        "elapsed_seconds": elapsed,
        "num_pages": doc.num_pages() if hasattr(doc, "num_pages") else None,
        "content_char_count": len(md_text),
    }
    (raw_dir / f"{stem}.json").write_text(json.dumps(raw_record, indent=2, default=str), encoding="utf-8")

    n_images = 0
    for i, pic in enumerate(getattr(doc, "pictures", []) or []):
        try:
            image = pic.get_image(doc)
        except Exception:  # noqa: BLE001
            continue
        if image is None:
            continue
        image.save(img_dir / f"{stem}_image_{i}.png")
        n_images += 1

    log_lines.append(f"content_char_count: {len(md_text)}")
    log_lines.append(f"n_images_extracted: {n_images}")
    (log_dir / f"{stem}.log").write_text("\n".join(log_lines), encoding="utf-8")

    print(f"[docling] OK {pdf_path.name}: {elapsed:.1f}s, {len(md_text)} chars, {n_images} images")


if __name__ == "__main__":
    main()
