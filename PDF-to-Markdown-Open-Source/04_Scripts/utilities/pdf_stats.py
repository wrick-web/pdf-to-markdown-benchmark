#!/usr/bin/env python3
"""
Quick sanity-check utility: page count + native-text character count per
PDF, using PyMuPDF. Used to independently verify the benchmark PDFs'
archetype claims (e.g. confirming PDF3 is genuinely 0% native text /
image-only) rather than trusting the ClickUp description at face value.

Usage:
    python pdf_stats.py <path/to/*.pdf ...>
"""
import sys

import pymupdf


def main() -> None:
    for path in sys.argv[1:]:
        doc = pymupdf.open(path)
        total_chars = sum(len(page.get_text()) for page in doc)
        print(
            f"{path}: pages={doc.page_count}, "
            f"total_text_chars={total_chars}, "
            f"avg_chars_per_page={total_chars / doc.page_count:.1f}"
        )


if __name__ == "__main__":
    main()
