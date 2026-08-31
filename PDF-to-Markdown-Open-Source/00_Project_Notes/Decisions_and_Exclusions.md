# Decisions & Exclusions Log

## ⚠️ Correction (Rev 2 transition, see `01_Benchmark_Design/`)

While mapping tools to the new frozen capability taxonomy (C10–C17), this
repository read the actual prior-cycle ClickUp records in full for the
first time (previously only their names/status had been checked, not
their content). This surfaced a genuine duplicate that the earlier
Cycle-II research did not catch:

**"PaddleOCR-VL / PP-StructureV3" was already tested in the prior cycle**
under the ClickUp subtask named "Paddlerocr" — with real, detailed,
observed results across text fidelity, reading order, headings, tables,
and figures/charts (formula and chart recognition were explicitly disabled
by that tester as out-of-scope for their inputs). This repository's own
Cycle-II section below describes PP-StructureV3 as a newly-identified Tier
A candidate that was "installed but blocked at model-download time" — that
description is **not wrong about this repository's own run**, but it
should not have been presented as a first test of the tool. It's a
duplicate. See `02_Tools/Tool_Capability_Matrix.md` section A for the full
real evidence, and relabel any future work on this tool **RE-TEST/RE-MAP**,
never "new."

This is left as a visible correction rather than silently edited into the
original text below, consistent with this project's own rule never to
overwrite prior research.

A single place to see every "did we test/include this or not, and why"
decision made this cycle, without digging through `Tool_Landscape.md`'s
full tables.

## Not re-tested (already covered by a prior cycle)

Docling, PyMuPDF4LLM, LiteParse, doc2mark, MarkItDown, MinerU, PaddleOCR
(bare/standalone), Dolphin, Unstructured — all marked "complete" on the
"Test Inputs & Artifact Creation" ClickUp subtask before this cycle began.
**Decision: do not duplicate.** DocTR is marked "review" (not yet closed)
on that same subtask — also not duplicated, since it's actively in
progress elsewhere.

## Known but still not benchmarked by anyone (a real gap, flagged not filled)

Marker, olmOCR, pdf-craft are named in the ClickUp task's own "Known Tool
Landscape" and "Cycle II adds..." text, but no benchmark subtask exists for
any of them yet. **Decision: this cycle's mandate was new-tool discovery,
not clearing a backlog of already-known-but-undone tools, so these three
were left alone** rather than adopted as "new" — that would have been a
mislabeled duplicate of an existing, already-identified to-do. Flagged
explicitly in `Tool_Landscape.md` section A as an open gap for whoever
picks up the backlog next. One relevant fact surfaced in passing during
this cycle's research: Marker shipped a **v2 rewrite on 2026-07-20**
(new Surya OCR 2 + a 20M-param fast layout model) — if/when Marker is
finally benchmarked, it should be v2, not the version implied by the
original ClickUp note.

## Already excluded (prior cycle) — re-confirmed, not overturned

GROBID, Nougat, Tesseract (standalone), PDFPlumber, Camelot, Tabula — the
original exclusion reasons in "Tool List & Access Outreach" were checked
against current information and still hold; no meaningful new release was
found that changes any of them. OCRmyPDF (named in "Known Tool Landscape"
but absent from both the tested and excluded lists) was independently
checked this cycle: it still only produces a searchable **PDF**, not
Markdown, and has no table/chart structural awareness — same exclusion
class as Tesseract, now recorded explicitly rather than left as a gap.

**One partial exception, explained:** PaddleOCR was previously excluded
*as a standalone pure-OCR engine* under the reasoning "no markdown-export
pipeline." That exact standalone tool was separately marked "tested" on
the Test Inputs subtask in a later part of the same prior cycle — both
facts are recorded in `Tool_Landscape.md` without trying to resolve the
apparent contradiction (not this cycle's call to make). This cycle
identified and separately evaluated **PaddleOCR-VL / PP-StructureV3**,
which is architecturally distinct (adds a dedicated layout stage + a
compact VLM + native Markdown/table/chart handling) — not a re-test of
either prior PaddleOCR result, and not excluded by the original
"standalone pure-OCR" rationale.

## New tools found this cycle — included (Tier A, executed)

**Kreuzberg** and **open-parse** (base mode) — see
`Tool_Landscape.md` section C and each tool's `observations.md` for full
rationale. Both qualify under "What This IS" (open-source, self-hostable,
local, PDF input, Markdown output). Kreuzberg is the stronger candidate by
a wide margin on the actual evidence gathered.

## New tools found this cycle — attempted but blocked (Tier A, not by choice)

**PaddleOCR-VL / PP-StructureV3** — installed, but both its default
(Hugging Face) and documented fallback (Baidu Object Storage) model
sources are blocked by this sandbox's network policy. **Not excluded on
merit** — flagged for re-testing on an unrestricted machine.

**huridocs/pdf-document-layout-analysis** — Docker-only distribution; no
Docker daemon available in this sandbox. **Not excluded on merit** —
flagged for re-testing on a machine with Docker.

## New tools found this cycle — prepared, not run (Tier B)

dots.ocr, MonkeyOCR, Chandra, Surya (standalone), OCRFlux, Nanonets-OCR-s/
docext, GLM-OCR, granite-docling-258M, RAGFlow/DeepDoc, Chunkr — all need
a GPU and/or Hugging Face Hub (all blocked here); Chunkr additionally
needs Docker. **Not excluded on merit** — each has a `02_Tools/_prepared_not_run/<tool>.md`
with exact install/run commands, license caveats (Chandra's OpenRAIL-M
commercial carve-out, Chunkr's AGPL-3.0), and the specific reason it
couldn't run here.

## New tools found this cycle — excluded (Tier C, confirmed reasons)

| Tool | Reason |
|---|---|
| Zerox | Confirmed: no local/offline model option exists at all — thin wrapper around a paid remote vision-LLM API. Fails "self-hosted, not SaaS/API-only" outright. |
| GOT-OCR2.0 | No 2025/2026 successor found (checked explicitly); superseded in practice by newer entrants; GPU+HF regardless. |
| mPLUG-DocOwl2 | Wrong tool class — it's a document-VQA model (answers questions about a page), not a structural Markdown reconstructor. |
| Kosmos-2.5 | Image-only input, stale since Aug 2024, no advantage over 2025/2026 entrants. |
| PDF-Extract-Kit | The project's own README says to use MinerU instead — this is MinerU's underlying toolbox, and MinerU is already tested. Duplicate by the project's own admission. |
| LOCR | No public code repository found despite targeted search — unverifiable as installable, excluded pending a real release. |
| Extractous | Tesseract-based plain text/XML output, no documented table/layout structure preservation. |
| oar-ocr | Images-only (no native PDF input), weights only via ModelScope (also blocked here), ~160 GitHub stars / very new and unproven. |

## Benchmark input decision

The 3 exact PDFs from "Test Inputs & Artifact Creation" were required for
comparability with the prior hosted-API cycle. Their original hosts
(`corporate.target.com`, `www.shi.co.jp`) and the ClickUp attachment CDN
are all blocked by this sandbox's egress policy. **Decision (user-directed):**
the user uploaded the exact same 3 PDF files directly into this session
rather than having synthetic stand-ins built — preserving byte-for-byte
comparability. See `00_Project_Notes/CHANGELOG.md` for the full timeline.
