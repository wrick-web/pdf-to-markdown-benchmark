#!/usr/bin/env python3
"""
Run PaddleOCR-VL against a benchmark PDF using the CURRENT (2026-09-18)
top-level `PaddleOCRVL` class from `paddleocr==3.7.0` (paddlex==3.7.2),
default `pipeline_version="v1.6"` (model name "PaddleOCR-VL-1.6", VL
recognition model "PaddleOCR-VL-1.6-0.9B", layout model "PP-DocLayoutV2" --
confirmed by reading paddlex/inference/utils/official_models.py directly,
not assumed).

This is the current, correct, minimal 2-model PaddleOCR-VL pipeline
(distinct from the older 6+-model PPStructureV3 classical pipeline used in
this project's first attempt on 2026-08-28/2026-09-08).

Usage:
    source .venv_paddleocr/bin/activate
    python run_paddleocr_vl.py <input.pdf> <tool_output_dir>
"""
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
        "config: PaddleOCRVL(), default construction (pipeline_version='v1.6' == PaddleOCR-VL-1.6), no overrides",
        f"started: {time.strftime('%Y-%m-%d %H:%M:%S')}",
    ]

    t0 = time.time()
    error = None
    try:
        import paddleocr
        log_lines.insert(0, f"paddleocr version: {paddleocr.__version__}")
        import paddlex
        log_lines.insert(1, f"paddlex version: {paddlex.__version__}")
        from paddleocr import PaddleOCRVL

        p = PaddleOCRVL()
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
