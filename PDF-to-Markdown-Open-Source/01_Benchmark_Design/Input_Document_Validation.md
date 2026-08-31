# Input Document Validation

**Source task (confirmed by Ajay via the user):** "pymupdf4llm"
(`86baza16z`), a subtask of "Test Inputs & Artifact Creation"
(`86ban5kka`) under the parent "PDF to markdown using open source
libraries" (`86ban5kjq`). This task is a completed, already-graded
Cycle-I tool report (PyMuPDF4LLM, scored 28–29/35 "Publishable" by the
automated AI Reviewer across several revisions) — its value for this
exercise is the **3 PDF attachments and demo videos it carries**, not its
own tool findings (which are pre-Rev2 and already reflected in
`02_Tools/Tool_Capability_Matrix.md`).

**Important identity finding:** the 3 attached PDFs on this task —
`input1_hybridearnings.pdf` (843,600 bytes), `input2_financialpdf.pdf`
(484,174 bytes), `input3_scannedpaper.pdf` (1,558,983 bytes) — are
**byte-size-identical** to the 3 PDFs already in this repository's
`01_Benchmark_PDFs/` (uploaded directly into this research session
earlier and used for every tool run so far). This strongly indicates they
are the same canonical documents, not new ones. A full checksum
comparison was not possible: this research environment's network egress
policy blocks direct downloads from the ClickUp attachment CDN
(confirmed earlier in this project), so the ClickUp copies could not be
re-fetched and hashed. The match is therefore on **file size only**
(three independent exact matches), not a cryptographic hash — flagged
honestly rather than overstated.

## Document 1

- **Name:** `input1_hybridearnings.pdf` (ClickUp) = `PDF1_Hybrid_Earnings_Report_Target2015.pdf` (this repo)
- **Source:** attachment on ClickUp task `86baza16z`; matches (by size) the file already in `01_Benchmark_PDFs/`
- **Type:** Hybrid — native digital text throughout (84 pages, confirmed independently via PyMuPDF: 250,546 native text characters)
- **Key characteristics (cross-confirmed by this repo's own Kreuzberg/open-parse runs AND Mahreen's independent PyMuPDF4LLM report):**
  - Genuine multi-column sections ("Owned Brands"/"Exclusive Brands", "Growth Story Again") — confirmed working multi-column reading order in Mahreen's report
  - Financial tables with footnotes explicitly associated below them (footnotes a–i under the "Financial Summary" table)
  - Embedded charts (sales/EBIT chart, comparison chart) and images (CEO photo, CEO signature)
  - Real section headings/hierarchy (Item 1, PART I/II, etc.)
  - No equations, no code blocks (confirmed independently twice — this repo's own grep of Kreuzberg's output, and no mention anywhere in Mahreen's report)
- **Capabilities covered:** C10 (Text Fidelity), C11 (Reading Order — has real multi-column), C12 (Heading & Section Structure), C13 (Table Extraction), C14 (Figures & Charts)
- **Scenarios covered:** S27 (ordinary text), S28 (multi-column — confirmed, not merely plausible), S29 (styled headings), S30 (footnotes — confirmed with a concrete example), S31 (simple table, e.g. properties table), S33 (figure with caption — CEO photo/signature, caption association not yet confirmed), S34 (data chart)
- **Applicable test cases (candidate, pending formal fixture sign-off):** TC27, TC28, TC29, TC30, TC31, TC33, TC34
- **Gaps/issues:** No equations (C16/TC37) or code (C17/TC38) content. S32 (cross-page table) not confirmed — Mahreen's report describes tables as reconstructed within a page, not explicitly spanning a page break; would need a specific check before treating this document as a TC32 fixture.

## Document 2

- **Name:** `input2_financialpdf.pdf` (ClickUp) = `PDF2_Financial_Report_Sumitomo.pdf` (this repo)
- **Source:** attachment on ClickUp task `86baza16z`; matches (by size) the file already in `01_Benchmark_PDFs/`
- **Type:** Native digital text (18 pages, confirmed independently via PyMuPDF: 34,981 native text characters)
- **Key characteristics:**
  - Dense financial tables (Consolidated Balance Sheet, quarterly results, dividends) — explicitly described as a "multi-column Consolidated Balance Sheet" in Mahreen's report, i.e. multiple data columns per row, not a page-layout column
  - **No charts** ("N/A — source has no charts," confirmed independently in this repo's own Kreuzberg observations)
  - **No captioned figures/tables** ("no captioned figures/tables exist in source; section headers used instead," again independently consistent with this repo's own findings)
  - Table of Contents present (both prior reports note it — Mahreen's PyMuPDF4LLM run omitted it; this repo's Kreuzberg run rendered it, badly fragmented)
  - No equations, no code blocks (confirmed independently twice)
- **Capabilities covered:** C10, C11, C12, C13
- **Scenarios covered:** S27, S29, S31, S32 (candidate — this is the densest table-per-page document of the three and the most likely to contain a genuine page-spanning table, but this has **not been explicitly confirmed** by either prior report; needs a direct check, not assumed)
- **Not covered:** C14/S33/S34 (no figures or charts in this document at all — confirmed twice, independently)
- **Applicable test cases (candidate):** TC27, TC29, TC31, possibly TC32 pending confirmation
- **Gaps/issues:** No figure/chart content at all, so cannot serve TC33/TC34. No equations/code. S32 candidacy needs direct verification before being registered as a fixture for it.

## Document 3

- **Name:** `input3_scannedpaper.pdf` (ClickUp) = `PDF3_Scanned_Research_Paper.pdf` (this repo)
- **Source:** attachment on ClickUp task `86baza16z`; matches (by size) the file already in `01_Benchmark_PDFs/`
- **Type:** Scanned / image-only (12 pages, confirmed independently via PyMuPDF: 0 native text characters — genuinely no text layer)
- **Key characteristics:**
  - **Multi-column layout — flagged as a discrepancy, see below**
  - Multiple tables (at least "Table 4" and "Table 6" referenced), figures (Figure 2, Figure 4), a USDA logo/seal graphic, references/citations section
  - No equations, no code blocks (confirmed independently twice)
- **Capabilities covered:** C10 (via OCR), C11, C12 (partially — see gaps), C13, C14, C15 (this is the dedicated OCR test document)
- **Scenarios covered:** S35 (clean scan — this document is the project's designated clean-scan fixture) and, per Mahreen's report, **S28 (multi-column)** as well
- **Applicable test cases (candidate):** TC35 (strong fit — already independently tested by this repo's own Kreuzberg run with good OCR results), TC28 (see discrepancy below), TC29 (candidate — headings exist but inconsistently rendered by both tools tested so far)
- **Not covered:** S36 (mixed digital+scanned in one document) — this document is 100% scanned, cannot serve TC36 on its own
- **Gaps/issues:** No equations/code.

### ⚠️ Discrepancy requiring clarification (flagged, not silently resolved)

This repository's own `Tool_Scenario_Matrix.md` (written after this
repo's Kreuzberg run) states: *"This particular research note appears to
be single-column in the scanned source (not the two-column academic
layout the general archetype description implies), so multi-column
reading-order reconstruction was not meaningfully stress-tested by this
specific file."*

Mahreen's independent PyMuPDF4LLM report — which includes page-level
screenshots (`pymupdf4llm_input3_scannedpaper_multicolumn_layout.png` and
a matching "_parsed_failure" screenshot) — directly documents **multi-column
text with horizontal interleaving on pages 1–3** of this same document.

**These two observations conflict.** Rather than pick one silently, this
is flagged as exactly the kind of ambiguity the frozen spec says to
surface, not resolve unilaterally, during fixture registration ("If
authoring exposes a genuine ambiguity in a test case, flag only that
ambiguity — never redesign the benchmark"). Before Document 3 is
registered as an S28/TC28 fixture, someone should open the actual PDF
pages and settle this directly — it may be that only some pages are
multi-column and each report looked at a different part of the document.

## Overall Assessment

- **Collective benchmark coverage:** these 3 documents, taken together,
  plausibly cover 8 of the 12 scenarios: S27, S28 (with the discrepancy
  above), S29, S30, S31, S33, S34, S35. Confidence varies per scenario —
  see per-document notes above; none of this is a confirmed fixture
  registration, only a plausibility read pending the approval gate and
  formal sign-off.
- **Missing entirely — no document, no combination of documents, can
  cover these:**
  - **S32 (cross-page table)** — candidate but unconfirmed (Document 2
    most likely, per its Consolidated Balance Sheet), needs direct
    verification.
  - **S36 (mixed digital + scanned single document)** — none of the 3
    documents mixes both page types in one file. This is a hard gap: no
    existing document can satisfy TC36, regardless of approval outcome.
  - **S37 (equations) / S38 (code block)** — confirmed absent from all 3
    documents by two independent testing passes. TC37 and TC38 cannot be
    satisfied by this document set at all.
- **Test cases these 3 documents can plausibly support (pending
  confirmation + approval):** TC27, TC28 (pending the discrepancy above),
  TC29, TC30, TC31, TC32 (pending confirmation), TC33, TC34, TC35.
- **Test cases these 3 documents cannot support, under any
  circumstances:** TC36, TC37, TC38 — new fixtures are needed for these
  three regardless of what happens with this document set.
- **Clarification required before registration:**
  1. The S28/Document-3 multi-column discrepancy above.
  2. Whether Document 2's Consolidated Balance Sheet (or any other table)
     genuinely spans a page break (S32/TC32) — not yet directly verified
     by either prior report.
  3. Whether reusing these exact pre-Rev2 documents as the *frozen* Rev-2
     fixtures is acceptable given they weren't purpose-built to isolate
     one scenario each (core rule 11 allows one artifact to serve many
     test cases, but core rule 2 still requires each scenario's target
     region to be precisely located and graded separately — doable here,
     just not yet done).

**No benchmarking, scoring, or fixture registration has been performed
against these documents as part of this validation pass — see the
approval gate below.**
