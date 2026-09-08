#!/usr/bin/env python3
"""
Run PaddleOCR-VL (PP-StructureV3, PyPI `paddleocr[doc-parser]==3.7.0`)
against a benchmark PDF.

STATUS AS WRITTEN (2026-09-07): PP-StructureV3 downloads its layout/OCR/
table/VL models on first use from one of 4 hoster platforms (Hugging Face,
ModelScope, AIStudio, Baidu Object Storage) - see setup/INSTALL.md for the
full network-probe evidence. All 4 are blocked by this sandbox's egress
policy; this script fails inside PPStructureV3() construction, before any
PDF is touched, for every fixture. Left ready to run as-is the moment
network access to any of those 4 hosts is available.

Usage:
    source .venv_paddleocr/bin/activate
    python run_paddleocr_vl.py <input.pdf> <tool_output_dir>
"""
import json
import os
import sys
import time
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: run_paddleocr_vl.py <input.pdf> <tool_output_dir>")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    stem = pdf_path.stem

    md_dir = out_dir / "markdown_output"
    raw_dir = out_dir / "raw_output"
    log_dir = out_dir / "logs"
    for d in (md_dir, raw_dir, log_dir):
        d.mkdir(parents=True, exist_ok=True)

    log_lines = [
        f"input: {pdf_path}",
        "config: PPStructureV3(), default construction, no overrides",
        f"started: {time.strftime('%Y-%m-%d %H:%M:%S')}",
    ]

    t0 = time.time()
    error = None
    try:
        import paddleocr
        log_lines.insert(0, f"paddleocr version: {paddleocr.__version__}")
        from paddleocr import PPStructureV3

        p = PPStructureV3()
        result = list(p.predict(str(pdf_path)))
        for i, res in enumerate(result):
            res.save_to_markdown(str(md_dir))
            res.save_to_json(str(raw_dir))
    except Exception as exc:  # noqa: BLE001
        error = repr(exc)
    elapsed = time.time() - t0
    log_lines.append(f"elapsed_seconds: {elapsed:.2f}")

    if error:
        log_lines.append(f"ERROR: {error}")
        (log_dir / f"{stem}.log").write_text("\n".join(log_lines), encoding="utf-8")
        print(f"[paddleocr-vl] FAILED on {pdf_path.name}: {error}")
        sys.exit(2)

    (log_dir / f"{stem}.log").write_text("\n".join(log_lines), encoding="utf-8")
    print(f"[paddleocr-vl] OK {pdf_path.name}: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
