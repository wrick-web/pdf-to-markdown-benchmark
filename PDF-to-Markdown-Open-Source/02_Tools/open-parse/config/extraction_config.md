# open-parse extraction config used in this benchmark

Base mode only (no `[ml]` extra):
```python
openparse.DocumentParser().parse(path, ocr=False)
```
`ocr=True` was intentionally NOT used — open-parse's own docstring says
"Not recommended unless necessary - inherently slower and less accurate."
Table quality in base mode uses open-parse's built-in pdfminer-based
heuristic, not the unitable/table-transformer models (those require the
`[ml]` extra + a Hugging-Face weight download, blocked in this sandbox).

Required workaround: `tiktoken.get_encoding` monkey-patched to an offline
length-based fallback — see script docstring and observations.md for why.
