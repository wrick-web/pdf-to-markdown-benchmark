# Kreuzberg

MIT · Rust core / Python bindings · https://github.com/Goldziher/kreuzberg (rebranding to xberg-io/xberg) · docs: https://docs.xberg.io/

**Status: tested-this-cycle** (flagship new-tool candidate, fully executed against all 3 benchmark PDFs).

- `setup/` — install instructions, requirements.txt
- `scripts/` — `run_kreuzberg.py` (also in `04_Scripts/conversion/`)
- `config/` — exact extraction config used
- `raw_output/` — structured JSON per PDF (metadata, timing, warnings, table/image counts)
- `markdown_output/` — the actual Markdown produced per PDF
- `extracted_images/` — images pulled from each PDF
- `logs/` — per-PDF run logs
- `observations.md` — full qualitative findings (read this first)

See `observations.md` for the detailed, evidence-based write-up. One-line
summary: excellent, dependency-light, fully-local text/OCR extraction;
**no usable table reconstruction on any of the 3 benchmark PDFs** despite
that being a headline documented capability — see scoring in
`03_Benchmark_Results/MASTER_RESULTS.md`.
