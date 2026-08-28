# Methodology

## Scope of this cycle

This cycle's mandate was **new open-source tool discovery**, not re-testing
tools already benchmarked in earlier cycles. See `Tool_Landscape.md` section
A for the full duplicate-check baseline (already tested / known-deferred /
excluded) pulled directly from the ClickUp parent task (`86ban5kjq`) and its
"Tool List & Access Outreach" (`86ban5kk5`) and "Test Inputs & Artifact
Creation" (`86ban5kka`) subtasks before any new research began.

## Benchmark inputs

The exact 3 PDFs from the ClickUp "Test Inputs & Artifact Creation" subtask
were used — uploaded directly by the user into this session (the original
hosting domains, `corporate.target.com` and `www.shi.co.jp`, plus the
ClickUp attachment CDN, are all blocked by this sandbox's network egress
policy, so they could not be re-downloaded here; using the user's own copies
preserves byte-for-byte comparability with the prior hosted-API cycle,
which was the whole point of reusing the same 3 files).

| File | Archetype | Pages | Native text? |
|---|---|---|---|
| `PDF1_Hybrid_Earnings_Report_Target2015.pdf` | Hybrid earnings report (Target 2015 Annual Report) | 84 | Yes — 250,546 characters of extractable text (~2,983/page avg) |
| `PDF2_Financial_Report_Sumitomo.pdf` | Financial report (Sumitomo Heavy Industries consolidated financial report) | 18 | Yes — 34,981 characters (~1,943/page avg) |
| `PDF3_Scanned_Research_Paper.pdf` | Scanned research paper (image-only, no OCR layer) | 12 | **No — 0 extractable characters**, confirmed via PyMuPDF `page.get_text()` on every page. This is the intentional OCR stress test; it must be run in this image-only form, not the OCR-applied original. |

Page/character counts verified directly with PyMuPDF (`pymupdf.open(path)`,
sum of `page.get_text()` length per page) — not taken from the ClickUp
description, in case the uploaded copies differ slightly from the original
description (PDF1 is described there as 80 pages; the actual uploaded file
has 84).

## Environment

- 4 vCPU, 15GB RAM, CPU-only (no GPU), sandboxed cloud container.
- No Docker daemon (CLI present, no socket).
- Network egress allowlist: PyPI, npm, the Ubuntu package archive, and
  GitHub (`github.com`, `raw.githubusercontent.com`, `api.github.com`,
  `objects.githubusercontent.com`). Everything else — Hugging Face Hub,
  ModelScope, Ollama's registry, Baidu Object Storage, arXiv, archive.org,
  and arbitrary corporate hosts — returns a 403 policy denial, confirmed by
  direct test, not assumed.
- This was treated as a **hard constraint to work within and document
  honestly**, not a reason to fabricate results. Every tool below states
  plainly whether it was actually executed here or only prepared for
  execution elsewhere.

## Pipeline (per tool, per PDF)

```
INPUT PDF (01_Benchmark_PDFs/)
  -> TOOL (installed in its own uv/pip virtualenv under the repo)
  -> raw_output/<pdf_stem>.json      (full structured result: metadata, timing, warnings, table/image counts)
  -> markdown_output/<pdf_stem>.md   (the tool's markdown text)
  -> extracted_images/<pdf_stem>/    (any images the tool pulled out)
  -> logs/<pdf_stem>.log             (config used, timing, warnings, errors)
  -> manual read-through of the .md + spot-checks against the source PDF
  -> observations.md (qualitative, evidence-based findings per the 9 criteria)
  -> scored 0-5 per criterion in 03_Benchmark_Results/MASTER_RESULTS.md
```

Every run is scripted (`04_Scripts/conversion/run_<tool>.py`) and reproducible
— no manual/GUI steps, no hand-edited outputs.

## Where a tool doesn't natively output Markdown

Not applicable to the two tools actually executed this cycle — both
(Kreuzberg, open-parse) have a native Markdown/markdown-serializable output
path used as-is, no extra conversion layer inserted.

## Observation discipline

Every `observations.md` separates **documentation claim** from **observed
result**, and is written against the actual output file plus a manual
comparison to the source PDF (Read tool spot-checks, not just automated
metrics) — per the project's "GOOD vs BAD observation" quality bar. Where a
tool could not be run at all (blocked by network/GPU/Docker), the
`observations.md` for that tool records the *exact* failure evidence
(error text, blocked host) rather than a guess.

## Scoring rubric

0 = missing/unusable, 1 = very poor, 2 = poor, 3 = acceptable, 4 = good,
5 = excellent, scored independently for: Chart Reconstruction, Text
Preservation, Table Reconstruction, Document Hierarchy, Image Retention,
Reading Order, Caption/Figure Association, Long/Complex Document
Robustness, and Bonus/anomalous behaviour. Tables are further tagged
OMITTED (absent) vs DEGRADED (present but structurally broken). See
`03_Benchmark_Results/MASTER_RESULTS.md` for the populated rubric and
`Scorecards/` for the per-tool breakdown.
