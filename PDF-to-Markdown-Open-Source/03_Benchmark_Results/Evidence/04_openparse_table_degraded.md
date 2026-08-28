# Evidence: open-parse — DEGRADED (scrambled) table on PDF2

**Source:** `02_Tools/open-parse/markdown_output/PDF2_Financial_Report_Sumitomo.md`
**Tool version:** open-parse 0.7.0, base mode (no `[ml]` extra)

## open-parse's actual output for the "Business Results" table

```
**January 1 to March 31, 2024** **First Quarter**<br><br>**January 1 to March 31, 2024**<br><br>% change  % change <br><br>241,536  254,811  2.6  Net sales  (5.2) <br><br>11,182  18,434  14.1  Operating profit  (39.3)
```

## What this demonstrates

Two distinct, more serious problems than Kreuzberg's flattening on the
same table:
1. **Column/value order is actively scrambled**, not just flattened in
   original reading order — `241,536` and `254,811` (the two period
   values) appear *before* their row label ("Net sales") and the percent
   changes appear both before and after, making the row genuinely
   ambiguous to reconstruct correctly without the source PDF, rather than
   merely unstructured.
2. **Raw `<br><br>` HTML tags are embedded directly in what's presented as
   Markdown output** — inconsistent with a clean-Markdown deliverable.

This is classified as **DEGRADED** (data present, structure actively
wrong) rather than OMITTED (structure simply absent, as with Kreuzberg on
the same table) — arguably a worse failure mode, since a reader could
misattribute a value to the wrong period without independently verifying
against the source.
