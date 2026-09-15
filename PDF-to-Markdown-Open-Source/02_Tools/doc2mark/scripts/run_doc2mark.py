#!/usr/bin/env python3
"""
Run doc2mark (PyPI `doc2mark`, github.com/luisleo526/doc2mark) against a
benchmark PDF.

Usage:
    source .venv_doc2mark/bin/activate
    python run_doc2mark.py <input.pdf> <tool_output_dir>

No OCR provider is configured (ocr_provider=None) since none of the TCs run
in this pass require OCR/image interpretation and doc2mark's default OCR
path requires an external OpenAI API key, which is out of scope for this
open-source benchmark.
"""
import json
import sys
import time
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: run_doc2mark.py <input.pdf> <tool_output_dir>")
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
        "config: UnifiedDocumentLoader(ocr_provider=None), "
        "load(extract_images=False, ocr_images=False), everything else default",
        f"started: {time.strftime('%Y-%m-%d %H:%M:%S')}",
    ]

    t0 = time.time()
    error = None
    result = None
    try:
        import doc2mark
        log_lines.insert(0, f"doc2mark version: {doc2mark.__version__}")
        from doc2mark import UnifiedDocumentLoader

        loader = UnifiedDocumentLoader(ocr_provider=None)
        result = loader.load(
            str(pdf_path),
            extract_images=False,
            ocr_images=False,
            show_progress=False,
        )
    except Exception as exc:  # noqa: BLE001
        error = repr(exc)
    elapsed = time.time() - t0
    log_lines.append(f"elapsed_seconds: {elapsed:.2f}")

    if error:
        log_lines.append(f"ERROR: {error}")
        (log_dir / f"{stem}.log").write_text("\n".join(log_lines), encoding="utf-8")
        print(f"[doc2mark] FAILED on {pdf_path.name}: {error}")
        sys.exit(2)

    md_text = result.markdown or ""
    (md_dir / f"{stem}.md").write_text(md_text, encoding="utf-8")

    raw_record = {
        "tool": "doc2mark",
        "doc2mark_version": doc2mark.__version__,
        "input_file": str(pdf_path),
        "elapsed_seconds": elapsed,
        "content_char_count": len(md_text),
        "metadata": str(result.metadata),
        "tables_detected": len(result.tables) if result.tables else 0,
        "images_detected": len(result.images) if result.images else 0,
    }
    (raw_dir / f"{stem}.json").write_text(json.dumps(raw_record, indent=2, default=str), encoding="utf-8")

    log_lines.append(f"content_char_count: {len(md_text)}")
    log_lines.append(f"tables_detected: {raw_record['tables_detected']}")
    log_lines.append(f"images_detected: {raw_record['images_detected']}")
    (log_dir / f"{stem}.log").write_text("\n".join(log_lines), encoding="utf-8")

    print(f"[doc2mark] OK {pdf_path.name}: {elapsed:.2f}s, {len(md_text)} chars")


if __name__ == "__main__":
    main()
