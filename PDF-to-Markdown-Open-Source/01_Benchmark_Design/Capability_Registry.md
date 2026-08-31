# Capability Registry (C10–C17)

Source: ClickUp doc "PDF → Markdown — research design"
(`8cn1avd-25874` / page `8cn1avd-66494`), Rev 2, frozen 2026-08-23.

Eight capabilities. Each protects one row of the "preservation contract":
one per distinct type of source information/structure whose loss makes the
downstream result unusable or misleading.

| ID | Capability | What it protects |
|---|---|---|
| C10 | Text Fidelity | Ordinary digital textual content survives completely and correctly. The floor everything downstream stands on; its failure mode reads fine and is invisible. |
| C11 | Reading Order & Layout | The reading sequence — the spatial→linear mapping that conversion is. Content can be fully present and still mislead every consumer because it is assembled in the wrong order. |
| C12 | Heading & Section Structure | The document's organization — what chunking, section-scoped retrieval, citation and navigation run on. Fails independently of order. |
| C13 | Table Extraction | Relational data — values whose meaning lives in row/column association; the one type whose partial failure yields confidently wrong downstream answers rather than gaps. |
| C14 | Figures & Charts | Information living in visual content: the asset preserved, referenced from the correct position, caption/title attached (grounding) and a text-reachable trace (machine use). |
| C15 | Scanned Document OCR | Text that exists only as pixels — a text layer the parser must create. Total, silent failure for a whole document class if absent. Also a future standalone OCR ranking over the same shared scenarios/artifacts. |
| C16 | Equations & Mathematical Notation | Formal notation whose structure is its meaning; degraded math is misstated math. Output contract: LaTeX/MathML or an honest fallback. |
| C17 | Code Extraction | Preformatted code, whose whitespace and line structure ARE meaning. A distinct content type from math with a distinct output contract — a fenced code block, not LaTeX; code reflowed into prose is broken for every downstream use. |

## Frozen as NOT capabilities

- **Failure transparency/honesty** → cross-cutting grading on every run
- **Markdown output quality** → each capability's own output contract
- **Long-document robustness** → later test-case condition
- **Multilingual/script** → later test-case condition + product attribute
- **Chart understanding/data extraction** → enrichment beyond the
  preservation contract (see below)

## The Figures & Charts (C14) contract line

The base conversion contract is **preservation**: the visual asset, its
position/reference, and associated source text (caption/title).
Authoring textual interpretations or extracting chart values that do not
exist as explicit text in the source is **enrichment**: recorded when
observed, graded for accuracy (fabricated values are the worst failure),
never the minimum bar. Enrichment that *replaces* the visual instead of
augmenting it is simultaneously a preservation failure.

## Out of scope for this whole research

Structured field extraction (invoice → `{invoice_number, total, vendor}`
is a different problem family — that's the separate "Extract and Query
Structured Data From Documents" research, C18–C23), web-page conversion,
form filling, handwriting, document classification/routing, PDF creation
or editing.
