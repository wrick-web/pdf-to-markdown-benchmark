#!/usr/bin/env python3
"""
Run MarkItDown (PyPI `markitdown`, github.com/microsoft/markitdown) against a
benchmark PDF.

Usage:
    source .venv_markitdown/bin/activate
    python run_markitdown.py <input.pdf> <tool_output_dir>
"""
import json
import sys
import time
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: run_markitdown.py <input.pdf> <tool_output_dir>")
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
        "config: MarkItDown(), default convert() call, everything else default",
        f"started: {time.strftime('%Y-%m-%d %H:%M:%S')}",
    ]

    t0 = time.time()
    error = None
    result = None
    try:
        import markitdown
        log_lines.insert(0, f"markitdown version: {markitdown.__version__}")
        from markitdown import MarkItDown

        md = MarkItDown()
        result = md.convert(str(pdf_path))
    except Exception as exc:  # noqa: BLE001
        error = repr(exc)
    elapsed = time.time() - t0
    log_lines.append(f"elapsed_seconds: {elapsed:.2f}")

    if error:
        log_lines.append(f"ERROR: {error}")
        (log_dir / f"{stem}.log").write_text("\n".join(log_lines), encoding="utf-8")
        print(f"[markitdown] FAILED on {pdf_path.name}: {error}")
        sys.exit(2)

    md_text = result.text_content
    (md_dir / f"{stem}.md").write_text(md_text, encoding="utf-8")

    raw_record = {
        "tool": "markitdown",
        "markitdown_version": markitdown.__version__,
        "input_file": str(pdf_path),
        "elapsed_seconds": elapsed,
        "content_char_count": len(md_text),
        "title": getattr(result, "title", None),
    }
    (raw_dir / f"{stem}.json").write_text(json.dumps(raw_record, indent=2, default=str), encoding="utf-8")

    log_lines.append(f"content_char_count: {len(md_text)}")
    (log_dir / f"{stem}.log").write_text("\n".join(log_lines), encoding="utf-8")

    print(f"[markitdown] OK {pdf_path.name}: {elapsed:.2f}s, {len(md_text)} chars")


if __name__ == "__main__":
    main()
