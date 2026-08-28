# Evidence: Kreuzberg — table omission on PDF2 (Sumitomo financial report)

**Source:** `02_Tools/kreuzberg/markdown_output/PDF2_Financial_Report_Sumitomo.md`
**Tool version:** kreuzberg 4.10.2, config: `output_format=markdown, table_model=tatr`
**Quantitative signal:** `n_tables_detected: 0` (in `raw_output/PDF2_Financial_Report_Sumitomo.json`); **0 pipe (`|`) characters in the entire output file.**

## Original table (source PDF, "1. FY2025 First Quarter Consolidated Results")

A 2-period, 5-metric comparison table with columns: Metric | Q1 2025 | Q1
2024 | % change.

## Kreuzberg's actual output for this table

```
(Units: millions of yen) **First Quarter January 1 to March 31, 2025 First
Quarter January 1 to March 31, 2024** % change % change Net sales 241,536
(5.2) 254,811
```

## What this demonstrates

The metric name ("Net sales"), both period values (241,536 / 254,811), and
the percent change (5.2) are all *present* in the text — but every row of
what should be a clean 2x5 grid is concatenated into one run-on sentence,
with no way to tell, from the Markdown alone, which number belongs to
which period without cross-checking the source PDF. This is the same
pattern across every financial table in PDF1 and PDF2 — classified as
**OMITTED** structurally (no table markup exists at all), even though the
underlying values are not literally deleted.
