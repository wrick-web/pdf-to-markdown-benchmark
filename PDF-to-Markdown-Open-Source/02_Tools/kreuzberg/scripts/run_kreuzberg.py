#!/usr/bin/env python3
"""
Run Kreuzberg (MIT, github.com/Goldziher/kreuzberg -> xberg-io/xberg, PyPI
package `kreuzberg`) against a benchmark PDF and save every artifact the
project needs: markdown output, raw JSON metadata, extracted images, a log,
and timing.

Usage:
    source .venv_kreuzberg/bin/activate
    python run_kreuzberg.py <input.pdf> <tool_output_dir>

Requires: `pip install kreuzberg` + system `tesseract-ocr` + `tesseract-ocr-eng`
(installed via apt in this project; see 02_Tools/kreuzberg/setup/).
"""
import json
import sys
import time
from pathlib import Path

import kreuzberg


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: run_kreuzberg.py <input.pdf> <tool_output_dir>")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    stem = pdf_path.stem

    raw_dir = out_dir / "raw_output"
    md_dir = out_dir / "markdown_output"
    img_dir = out_dir / "extracted_images" / stem
    log_dir = out_dir / "logs"
    for d in (raw_dir, md_dir, img_dir, log_dir):
        d.mkdir(parents=True, exist_ok=True)

    config = kreuzberg.ExtractionConfig(
        output_format=kreuzberg.OutputFormat.MARKDOWN,
        ocr=kreuzberg.OcrConfig(backend="tesseract", language="eng"),
        pdf_options=kreuzberg.PdfConfig(extract_images=True),
        layout=kreuzberg.LayoutDetectionConfig(apply_heuristics=True, table_model="tatr"),
    )

    log_lines = [
        f"kreuzberg version: {kreuzberg.version if hasattr(kreuzberg, 'version') else 'unknown'}",
        f"input: {pdf_path}",
        f"config: output_format=markdown, ocr.backend=tesseract, ocr.language=eng, "
        f"pdf_options.extract_images=True, layout.table_model=tatr, layout.apply_heuristics=True",
        f"started: {time.strftime('%Y-%m-%d %H:%M:%S')}",
    ]

    t0 = time.time()
    error = None
    result = None
    try:
        result = kreuzberg.extract_file_sync(str(pdf_path), config=config)
    except Exception as exc:  # noqa: BLE001 - we want to record any failure, not crash the batch
        error = repr(exc)
    elapsed = time.time() - t0

    log_lines.append(f"elapsed_seconds: {elapsed:.2f}")

    if error:
        log_lines.append(f"ERROR: {error}")
        (log_dir / f"{stem}.log").write_text("\n".join(log_lines), encoding="utf-8")
        print(f"[kreuzberg] FAILED on {pdf_path.name}: {error}")
        sys.exit(2)

    # Markdown output
    md_text = result.content or ""
    (md_dir / f"{stem}.md").write_text(md_text, encoding="utf-8")

    # Extracted images
    n_images = 0
    if result.images:
        for i, image in enumerate(result.images):
            # kreuzberg returns each image as a plain dict, not an object
            data = image.get("data") if isinstance(image, dict) else getattr(image, "data", None)
            fmt = (image.get("format") if isinstance(image, dict) else getattr(image, "format", None)) or "png"
            if data:
                (img_dir / f"image_{i}.{fmt}").write_bytes(data)
                n_images += 1

    # Tables (if any structurally detected)
    n_tables = len(result.tables) if result.tables else 0
    tables_dump = []
    if result.tables:
        for i, t in enumerate(result.tables):
            if isinstance(t, dict):
                tables_dump.append({"index": i, **t})
            else:
                tables_dump.append(
                    {
                        "index": i,
                        "text": getattr(t, "text", None),
                        "markdown": getattr(t, "to_markdown", lambda: None)()
                        if hasattr(t, "to_markdown")
                        else None,
                    }
                )

    raw_record = {
        "tool": "kreuzberg",
        "input_file": str(pdf_path),
        "elapsed_seconds": elapsed,
        "page_count": result.metadata.get("page_count") if result.metadata else None,
        "metadata": dict(result.metadata) if result.metadata else {},
        "content_char_count": len(md_text),
        "n_images_extracted": n_images,
        "n_tables_detected": n_tables,
        "tables": tables_dump,
        "processing_warnings": list(result.processing_warnings or []),
        "detected_languages": result.detected_languages,
        "output_format": str(result.output_format),
    }
    (raw_dir / f"{stem}.json").write_text(json.dumps(raw_record, indent=2, default=str), encoding="utf-8")

    log_lines.append(f"page_count: {raw_record['page_count']}")
    log_lines.append(f"content_char_count: {raw_record['content_char_count']}")
    log_lines.append(f"n_images_extracted: {n_images}")
    log_lines.append(f"n_tables_detected: {n_tables}")
    log_lines.append(f"processing_warnings: {raw_record['processing_warnings']}")
    (log_dir / f"{stem}.log").write_text("\n".join(log_lines), encoding="utf-8")

    print(
        f"[kreuzberg] OK {pdf_path.name}: {elapsed:.1f}s, "
        f"{raw_record['content_char_count']} chars, {n_images} images, {n_tables} tables"
    )


if __name__ == "__main__":
    main()
