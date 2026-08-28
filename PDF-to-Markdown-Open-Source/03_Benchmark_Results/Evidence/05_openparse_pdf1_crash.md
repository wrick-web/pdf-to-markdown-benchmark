# Evidence: open-parse — uncaught crash on PDF1

**Source:** `02_Tools/open-parse/logs/PDF1_Hybrid_Earnings_Report_Target2015.log`

## Exact error

```
[open-parse] FAILED on PDF1_Hybrid_Earnings_Report_Target2015.pdf:
UnidentifiedImageError('cannot identify image file <_io.BytesIO object at 0x...>')
```

Raised from inside Pillow, invoked by open-parse's own image-node
processing while walking this PDF's embedded images (a typical
professionally-typeset annual report with JPEG2000/mixed-colorspace
images). There is no try/except around this internal decode step in
open-parse's base pipeline.

## What this demonstrates

**Total, whole-document failure from one unreadable embedded image** — not
a degraded-but-usable partial result. 0 characters, 0 nodes, 0 markdown,
0 JSON were produced for the single most complex benchmark PDF (84 pages,
native text + tables + charts + a signature block). This is the clearest
"Long/Complex Document Robustness" failure recorded this cycle for any
tool tested.
