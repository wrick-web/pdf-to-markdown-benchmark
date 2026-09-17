import sys
import time
import datetime
import pathlib

import pymupdf
import pymupdf4llm


def main():
    if len(sys.argv) < 3:
        print("usage: run_pymupdf4llm.py <input.pdf> <output_dir> [--extract-images]")
        sys.exit(1)

    input_pdf = pathlib.Path(sys.argv[1])
    output_dir = pathlib.Path(sys.argv[2])
    extract_images = "--extract-images" in sys.argv[3:]
    md_dir = output_dir / "markdown_output"
    log_dir = output_dir / "logs"
    md_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    stem = input_pdf.stem
    md_path = md_dir / f"{stem}.md"
    log_path = log_dir / f"{stem}.log"

    doc = pymupdf.open(input_pdf)
    page_count = doc.page_count
    doc.close()

    kwargs = {}
    config_desc = "pymupdf4llm.to_markdown(input_pdf) -- default, no extra options"
    if extract_images:
        image_dir = output_dir / "images"
        image_dir.mkdir(parents=True, exist_ok=True)
        kwargs = {"embed_images": True}
        config_desc = "pymupdf4llm.to_markdown(input_pdf, embed_images=True) -- images embedded as base64 in the Markdown"

    log_lines = []
    log_lines.append(f"pymupdf4llm version: {pymupdf4llm.__version__}")
    log_lines.append(f"pymupdf (fitz) version: {pymupdf.__version__}")
    log_lines.append(f"python version: {sys.version.split()[0]}")
    log_lines.append(f"input: {input_pdf}")
    log_lines.append(f"input_page_count: {page_count}")
    log_lines.append(f"config: {config_desc}")
    log_lines.append(f"started: {datetime.datetime.now().isoformat(timespec='seconds')}")

    start = time.time()
    try:
        md_text = pymupdf4llm.to_markdown(str(input_pdf), **kwargs)
        elapsed = time.time() - start
        md_path.write_text(md_text, encoding="utf-8")
        log_lines.append(f"elapsed_seconds: {elapsed:.2f}")
        log_lines.append("result: OK")
        log_lines.append(f"output_markdown_path: {md_path}")
        log_lines.append(f"content_char_count: {len(md_text)}")
        print(f"[pymupdf4llm] OK {input_pdf.name}: {elapsed:.2f}s, {len(md_text)} chars -> {md_path}")
    except Exception as exc:
        elapsed = time.time() - start
        log_lines.append(f"elapsed_seconds: {elapsed:.2f}")
        log_lines.append("result: FAILED")
        log_lines.append(f"error: {exc!r}")
        print(f"[pymupdf4llm] FAILED on {input_pdf.name}: {exc!r}")
        raise
    finally:
        log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
