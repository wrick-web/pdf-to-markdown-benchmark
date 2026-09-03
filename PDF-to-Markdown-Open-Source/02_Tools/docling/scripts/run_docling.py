#!/usr/bin/env python3
"""
Run Docling (docling==2.124.0, github.com/docling-project/docling) against
a benchmark PDF.

STATUS AS WRITTEN (2026-09-03): this script has never completed a
successful run in this sandbox. Docling's StandardPdfPipeline loads two
models on first use. OCR is fixed here (RapidOCR's bundled ONNX weights
+ onnxruntime, both from PyPI, zero downloads — see setup/INSTALL.md
"OCR fix"). The layout model (docling-layout-heron) still has to come
from the Hugging Face Hub with no bundled/PyPI/GitHub-mirrored
alternative anywhere this sandbox can reach — see setup/INSTALL.md
"Layout: confirmed unavailable" for the full, exhaustive check. This
script is left ready to run as-is the moment either (a) HF access is
available, or (b) an offline artifacts_path (see INSTALL.md) is
supplied.

Usage:
    source .venv_docling/bin/activate
    python run_docling.py <input.pdf> <tool_output_dir>
"""
import json
import sys
import time
from pathlib import Path

import docling
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, RapidOcrOptions
from docling.datamodel.base_models import InputFormat


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
        "config: StandardPdfPipeline, ocr_options=RapidOcrOptions(backend='onnxruntime') "
        "(bundled ONNX weights, no download); everything else default (layout model "
        "still requires Hugging Face Hub access - see setup/INSTALL.md)",
        f"started: {time.strftime('%Y-%m-%d %H:%M:%S')}",
    ]

    t0 = time.time()
    error = None
    result = None
    try:
        pipeline_opts = PdfPipelineOptions()
        pipeline_opts.ocr_options = RapidOcrOptions(backend="onnxruntime")
        converter = DocumentConverter(
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_opts)}
        )
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
