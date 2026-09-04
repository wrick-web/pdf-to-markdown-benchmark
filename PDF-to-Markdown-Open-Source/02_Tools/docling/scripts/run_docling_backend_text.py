#!/usr/bin/env python3
"""
One-off test: does PdfPipelineOptions(force_backend_text=True, do_ocr=False)
let StandardPdfPipeline skip the (unavailable) layout model for
clean-digital-text PDFs? Same run_docling.py logic, with those two options
added. Not merged into run_docling.py because the answer (see logs) is that
it does not change anything for this pipeline class.
"""
import json
import os
import sys
import time
from pathlib import Path

import docling
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, RapidOcrOptions
from docling.datamodel.base_models import InputFormat


def main() -> None:
    pdf_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    stem = pdf_path.stem
    artifacts_path = os.environ.get("DOCLING_ARTIFACTS_PATH")

    raw_dir = out_dir / "raw_output"
    md_dir = out_dir / "markdown_output"
    img_dir = out_dir / "extracted_images"
    log_dir = out_dir / "logs"
    for d in (raw_dir, md_dir, img_dir, log_dir):
        d.mkdir(parents=True, exist_ok=True)

    log_lines = [
        f"docling version: {docling.__version__}",
        f"input: {pdf_path}",
        "config: StandardPdfPipeline, force_backend_text=True, do_ocr=False, "
        "artifacts_path=" + str(artifacts_path),
        f"started: {time.strftime('%Y-%m-%d %H:%M:%S')}",
    ]

    t0 = time.time()
    error = None
    result = None
    try:
        pipeline_opts = PdfPipelineOptions()
        pipeline_opts.force_backend_text = True
        pipeline_opts.do_ocr = False
        if artifacts_path:
            pipeline_opts.artifacts_path = artifacts_path
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
        print(f"[docling-backend-text] FAILED on {pdf_path.name}: {error}")
        sys.exit(2)

    doc = result.document
    md_text = doc.export_to_markdown()
    (md_dir / f"{stem}.md").write_text(md_text, encoding="utf-8")
    raw_record = {
        "tool": "docling",
        "config": "force_backend_text=True, do_ocr=False",
        "docling_version": docling.__version__,
        "input_file": str(pdf_path),
        "elapsed_seconds": elapsed,
        "content_char_count": len(md_text),
    }
    (raw_dir / f"{stem}.json").write_text(json.dumps(raw_record, indent=2, default=str), encoding="utf-8")
    log_lines.append(f"content_char_count: {len(md_text)}")
    (log_dir / f"{stem}.log").write_text("\n".join(log_lines), encoding="utf-8")
    print(f"[docling-backend-text] OK {pdf_path.name}: {elapsed:.1f}s, {len(md_text)} chars")


if __name__ == "__main__":
    main()
