# open-parse

MIT · Python (pdfminer.six-based) · https://github.com/Filimoa/open-parse

**Status: tested-this-cycle** (base mode only, as a lightweight native-text baseline — not a full contender for this use case).

- `setup/` — install instructions
- `scripts/` — `run_openparse.py` (also in `04_Scripts/conversion/`) — includes a documented tiktoken-offline workaround, see the script docstring
- `config/` — exact extraction config used
- `raw_output/` — structured JSON per PDF
- `markdown_output/` — Markdown produced (PDF2 only — PDF1 crashed, PDF3 produced empty output)
- `logs/` — per-PDF run logs, including the PDF1 crash traceback
- `observations.md` — full qualitative findings (read this first)

One-line summary: fast and dependency-light, but crashed outright on the
most complex benchmark PDF, produced zero headings on every PDF, and
returned silently empty output on the scanned PDF (no OCR in base mode).
Scored explicitly as a lightweight baseline, not a top contender — see
`03_Benchmark_Results/MASTER_RESULTS.md`.
