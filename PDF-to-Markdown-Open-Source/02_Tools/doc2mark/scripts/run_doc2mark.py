#!/usr/bin/env python3
"""
Run doc2mark (PyPI `doc2mark`, github.com/luisleo526/doc2mark) against a
benchmark PDF.

Usage:
    source .venv_doc2mark/bin/activate
    python run_doc2mark.py <input.pdf> <tool_output_dir> [--patched]

No OCR provider is configured (ocr_provider=None) since none of the TCs run
in this pass require OCR/image interpretation and doc2mark's default OCR
path requires an external OpenAI API key, which is out of scope for this
open-source benchmark.

--patched applies the monkeypatches in scripts/doc2mark_fixes.py (reading
order, heading-level consistency, all-caps byline heuristic, multi-footnote
splitting) before running. Without it, this runs stock, unmodified doc2mark
0.6.1 exactly as in the original TC27-TC32 execution pass.
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def main() -> None:
    if len(sys.argv) not in (3, 4):
        print("Usage: run_doc2mark.py <input.pdf> <tool_output_dir> [--patched]")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    patched = len(sys.argv) == 4 and sys.argv[3] == "--patched"
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
        f"patches applied: {'yes (scripts/doc2mark_fixes.py)' if patched else 'no (stock doc2mark 0.6.1)'}",
        f"started: {time.strftime('%Y-%m-%d %H:%M:%S')}",
    ]

    t0 = time.time()
    error = None
    result = None
    try:
        import doc2mark
        log_lines.insert(0, f"doc2mark version: {doc2mark.__version__}")
        from doc2mark import UnifiedDocumentLoader

        if patched:
            import doc2mark_fixes
            doc2mark_fixes.apply()

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
