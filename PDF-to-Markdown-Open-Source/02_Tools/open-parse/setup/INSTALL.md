# open-parse — Setup

- Repo: https://github.com/Filimoa/open-parse
- License: MIT
- Version tested: `openparse==0.7.0` (base mode, no `[ml]` extra)

## Install

```bash
uv venv .venv_openparse --python 3.11
source .venv_openparse/bin/activate
uv pip install openparse
```

## Important: documented workaround needed

Even in base mode, open-parse's node-processing pipeline calls
`tiktoken.get_encoding("cl100k_base")`, which downloads a BPE file from
`openaipublic.blob.core.windows.net`. In any network-restricted
environment this fails, and a naive try/except-per-call pattern makes it
fail SLOWLY (repeated retries per node). `04_Scripts/conversion/run_openparse.py`
patches `tiktoken.get_encoding` to skip the network attempt entirely and
use a cheap offline length-based estimate instead — this only affects an
internal "is this node too short to matter" heuristic, not actual PDF
parsing. See that script's docstring and `../observations.md` for detail.

## Notes from this run

- The `[ml]` extra (better tables via unitable/table-transformer) was
  deliberately not installed — it requires an `openparse-download` step
  that pulls weights from Hugging Face, blocked in this sandbox.
- Crashed with `PIL.UnidentifiedImageError` on the most complex benchmark
  PDF (see `../observations.md` and `../logs/`) — a real, reproducible bug
  in this version's image-handling path, not an environment artifact.
