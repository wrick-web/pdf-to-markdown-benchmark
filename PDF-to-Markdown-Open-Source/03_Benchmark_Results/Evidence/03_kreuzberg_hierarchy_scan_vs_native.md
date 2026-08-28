# Evidence: Kreuzberg — opposite hierarchy failure modes (native vs. scanned)

**Sources:**
`02_Tools/kreuzberg/markdown_output/PDF1_Hybrid_Earnings_Report_Target2015.md` (native text, 84pp)
`02_Tools/kreuzberg/markdown_output/PDF3_Scanned_Research_Paper.md` (scanned, 12pp, OCR'd)

## Measured heading counts (same tool, same config, run back-to-back)

| PDF | Input type | `#` count | `##` count | `###` count |
|---|---|---|---|---|
| PDF1 | native text | 7 | 19 | **289** |
| PDF3 | scanned (OCR) | 0 | 0 | **0** |

## What this demonstrates

PDF3's source clearly has section titles in all-caps ("ABSTRACT",
"SUMMARY", "PUBLICATIONS CITED" — visible directly in the OCR'd text
stream as plain paragraph text), but **zero of them were promoted to a
Markdown heading.** This is because Kreuzberg's heading heuristic relies on
font-size/boldness metadata from the PDF's native text layer — OCR'd text
has no such metadata, so hierarchy detection has nothing to key off. The
same tool, same config, produces the *opposite* problem (289 spurious
headings) the moment that metadata exists. Anyone scoring "Document
Hierarchy" as one number for this tool should know it depends entirely on
whether the input page has a native text layer or was OCR'd.
