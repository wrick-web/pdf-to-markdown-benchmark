# Scenario Registry (S27–S38)

Source: ClickUp doc "PDF → Markdown — research design" (Rev 2, frozen
2026-08-23). Twelve scenarios — the smallest natural set. No stored
priorities or waves: a scenario's status is derived (does a test case
exist, has it run), not assigned.

**C10 · Text Fidelity**

| ID | Scenario | What it tests |
|---|---|---|
| S27 | An ordinary digital text document | The baseline: every paragraph arrives complete and unchanged — nothing silently missing, garbled, or invented |

*Repeating headers, footers and page numbers are NOT a scenario — page
furniture appears naturally in many test documents and is checked as part
of the relevant test cases (removing it is correct, splicing it into the
body is a failure).*

**C11 · Reading Order & Layout**

| ID | Scenario | What it tests |
|---|---|---|
| S28 | A page laid out in multiple columns | Reads down each column in turn, not straight across the page |

**C12 · Heading & Section Structure**

| ID | Scenario | What it tests |
|---|---|---|
| S29 | A document with styled headings and subheadings | Headings become real Markdown heading levels with their nesting intact — not bold paragraphs, not one flat level |
| S30 | Footnotes at the bottom of the page | The structural relationship survives: kept out of the body flow and attached to the content they annotate |

**C13 · Table Extraction**

| ID | Scenario | What it tests |
|---|---|---|
| S31 | A simple, clearly formatted table | The baseline: rows, columns and headers survive with every value under the right header |
| S32 | A table that continues across a page break | Recognised as one table, not two — the second half keeping its headers |

**C14 · Figures & Charts**

| ID | Scenario | What it tests |
|---|---|---|
| S33 | A document with figures and captions | Asset survives, referenced from the correct position, caption attached |
| S34 | A document with a data chart | What representation the tool produces — image, image + title/caption, added textual data (the last recorded as enrichment, never required) |

**C15 · Scanned Document OCR**

| ID | Scenario | What it tests |
|---|---|---|
| S35 | A cleanly scanned document | The OCR baseline: image-only pages become accurate text |
| S36 | A document mixing digital and scanned pages | Per-page detection — the scanned page inside a digital PDF is processed, not silently skipped |

**C16 · Equations & Mathematical Notation**

| ID | Scenario | What it tests |
|---|---|---|
| S37 | A document containing mathematical equations | Math survives as LaTeX/MathML or an honest fallback, not mangled prose |

**C17 · Code Extraction**

| ID | Scenario | What it tests |
|---|---|---|
| S38 | A document containing a code block | Code survives as a preformatted/fenced code block with its line structure and indentation intact — not reflowed into a paragraph |

## Recorded near-miss (do not silently re-promote)

*Sidebar/pull-quote interrupting the text* was the closest demotion — a
"content outside the main flow" question at rarer occurrence than
footnotes; if execution shows magazine-style layouts discriminate, it
returns as a test case first, not a new scenario.

Everything else from Rev 1's 56 scenarios became later test-case
variations (fonts, merged cells, borderless/nested tables, scan quality,
orientation, special characters, length, scripts, fabrication probes,
indentation-sensitive/paginated code), cross-cutting grading (all of
Failure Transparency), output contracts (the rest of Markdown Integrity),
or product attributes (limits, language support). Repeating page
furniture is checked in passing wherever fixtures carry it.
