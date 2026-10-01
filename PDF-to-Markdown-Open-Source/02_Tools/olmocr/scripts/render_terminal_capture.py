#!/usr/bin/env python3
"""
Render REAL, already-captured terminal text (command + actual stdout/stderr)
into a terminal-styled PNG image.

This environment has no GUI/screen-capture capability, so a literal OS-level
screenshot cannot be taken. This renders the exact captured text verbatim -
no line is invented or altered - into an image for visual evidence, in place
of a native screen-grab. The source text file is always kept alongside it.

Usage:
    python render_terminal_capture.py <input_text_file> <output_png>
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_SIZE = 16
PAD = 20
BG = (13, 17, 23)
FG = (201, 209, 217)
LINE_HEIGHT = 22


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: render_terminal_capture.py <input_text_file> <output_png>")
        sys.exit(1)
    text_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    lines = text_path.read_text(encoding="utf-8", errors="replace").splitlines()
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    max_chars = max((len(l) for l in lines), default=80)
    width = PAD * 2 + int(max_chars * FONT_SIZE * 0.62)
    height = PAD * 2 + len(lines) * LINE_HEIGHT

    img = Image.new("RGB", (max(width, 400), max(height, 100)), BG)
    draw = ImageDraw.Draw(img)
    y = PAD
    for line in lines:
        draw.text((PAD, y), line, font=font, fill=FG)
        y += LINE_HEIGHT

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    print(f"rendered {len(lines)} lines -> {out_path}")


if __name__ == "__main__":
    main()
