# Evidence: Kreuzberg — heading over-fragmentation on PDF2

**Source:** `02_Tools/kreuzberg/markdown_output/PDF2_Financial_Report_Sumitomo.md` (near the top of the file)

## Original source text (one title, wrapped across several lines in the PDF)

"CONSOLIDATED FINANCIAL REPORT For the Three-Month Period from January 1
to March 31, 2025"

## Kreuzberg's actual Markdown output for this single title

```
### CONSOLIDATED FINANCIAL REPORT
### For the Three
- **-**
### Month Period from January 1 to March 31, 2025
```

## What this demonstrates

One title becomes 4 separate blocks: two spurious `###` headings, and the
hyphen in "Three-Month" is split onto its own line and misread as a
Markdown list item. Kreuzberg's heading heuristic is keying off line
breaks/short-line-length in the source PDF's text layer rather than
semantic title detection. Quantitatively, this pattern repeats badly
enough across the document that **PDF1 (84 pages) ends up with 289
separate `###` headings** — implausible for genuine section structure in
that document.
