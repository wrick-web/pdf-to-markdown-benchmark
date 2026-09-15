#!/usr/bin/env python3
"""
Run doc2mark (PyPI `doc2mark`, github.com/luisleo526/doc2mark) against a
benchmark PDF.

Usage:
    source .venv_doc2mark/bin/activate
    python run_doc2mark.py <input.pdf> <tool_output_dir> [--patched] [--extract-images]

No OCR provider is configured (ocr_provider=None) since only OCR-requiring
TCs need one, and doc2mark's default OCR path requires an external OpenAI
API key, which is out of scope for this open-source benchmark.

--patched applies the monkeypatches in scripts/doc2mark_fixes.py (reading
order, heading-level consistency, all-caps byline heuristic, multi-footnote
splitting) before running. Without it, this runs stock, unmodified doc2mark
0.6.1 exactly as in the original TC27-TC32 execution pass.

--extract-images passes extract_images=True so embedded figures/charts are
extracted as base64 PNGs; each is also decoded and saved to
<tool_output_dir>/images/<stem>_image_<n>.png for direct visual inspection
and as attachable evidence, in addition to staying embedded in the .md file
exactly as doc2mark itself produced it.
"""
import base64
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def main() -> None:
    args = sys.argv[1:]
    if len(args) < 2:
        print("Usage: run_doc2mark.py <input.pdf> <tool_output_dir> [--patched] [--extract-images]")
        sys.exit(1)

    pdf_path = Path(args[0])
    out_dir = Path(args[1])
    flags = set(args[2:])
    patched = "--patched" in flags
    extract_images = "--extract-images" in flags
    stem = pdf_path.stem

    md_dir = out_dir / "markdown_output"
    raw_dir = out_dir / "raw_output"
    log_dir = out_dir / "logs"
    img_dir = out_dir / "images"
    for d in (md_dir, raw_dir, log_dir):
        d.mkdir(parents=True, exist_ok=True)

    log_lines = [
        f"input: {pdf_path}",
        f"config: UnifiedDocumentLoader(ocr_provider=None), "
        f"load(extract_images={extract_images}, ocr_images=False), everything else default",
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
            extract_images=extract_images,
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

    saved_images = []
    if result.images:
        img_dir.mkdir(parents=True, exist_ok=True)
        for i, img in enumerate(result.images):
            data = img.get("data")
            if not data:
                continue
            img_path = img_dir / f"{stem}_image_{i}.png"
            img_path.write_bytes(base64.b64decode(data))
            saved_images.append(str(img_path))

    raw_record = {
        "tool": "doc2mark",
        "doc2mark_version": doc2mark.__version__,
        "input_file": str(pdf_path),
        "elapsed_seconds": elapsed,
        "content_char_count": len(md_text),
        "metadata": str(result.metadata),
        "tables_detected": len(result.tables) if result.tables else 0,
        "images_detected": len(result.images) if result.images else 0,
        "images_saved": saved_images,
    }
    (raw_dir / f"{stem}.json").write_text(json.dumps(raw_record, indent=2, default=str), encoding="utf-8")

    log_lines.append(f"content_char_count: {len(md_text)}")
    log_lines.append(f"tables_detected: {raw_record['tables_detected']}")
    log_lines.append(f"images_detected: {raw_record['images_detected']}")
    if saved_images:
        log_lines.append(f"images_saved: {', '.join(saved_images)}")
    (log_dir / f"{stem}.log").write_text("\n".join(log_lines), encoding="utf-8")

    print(f"[doc2mark] OK {pdf_path.name}: {elapsed:.2f}s, {len(md_text)} chars, {len(saved_images)} image(s) saved")


if __name__ == "__main__":
    main()
