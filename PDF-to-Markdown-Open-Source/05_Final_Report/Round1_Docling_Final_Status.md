# Round 1 Final Status — Docling (Rev-2, 2026-09-03)

Task: `EXEC · Docling · PDF-OSS v1 · R1` (ClickUp `86bbu4wm7`), 12
scenario/test-case lines (S27/TC27 … S38/TC38).

## Result

**0 of 12 test cases completed a Docling run. All 12 are BLOCKED.**
This is not an untested/unknown state — every blocker below is backed
by real, reproducible, evidence-gathering work, not assumption.

| | Count |
|---|---|
| Completed (produced Docling output) | 0 |
| PASS | 0 |
| PARTIAL | 0 |
| FAIL | 0 |
| BLOCKED | 12 |

## Why: the exact blocker, precisely isolated

Docling's `StandardPdfPipeline` requires two models on first use — OCR
and layout (object detection for headings/tables/reading order/figures,
used on every document regardless of whether OCR is needed).

- **OCR is solved.** The `rapidocr` PyPI package bundles its own ONNX
  model weights; installing `onnxruntime` and explicitly selecting that
  backend gets OCR working with zero network calls. Verified against all
  5 real TC27–TC31 fixtures.
- **The layout model is not solved**, and this was tried exhaustively,
  not assumed:
  - Every layout preset Docling ships is Hugging Face Hub-only (no
    bundled, PyPI, or GitHub-mirrored alternative exists anywhere this
    sandbox can reach — checked directly, not inferred).
  - Hugging Face Hub itself is blocked by this sandbox's network policy.
  - The user then independently obtained the real model files
    (`config.json`, `preprocessor_config.json`, `model.safetensors`,
    ~312MB) on their own machine, which does have normal internet
    access, and attempted to transfer them in via Git LFS.
    `config.json`/`preprocessor_config.json` transferred correctly and
    are confirmed valid. `model.safetensors` did not: the first copy
    arrived corrupted (a lossy text-encoding artifact from before it
    reached Git), and every subsequent re-download — across 4
    independently implemented transport methods (direct binary
    download, resumable range-based download, chunked small-range
    downloads, and a `git clone` of the actual Hugging Face repo via
    Git's own LFS protocol) — stalled at the identical byte offset,
    171,658,996 of 312,243,345, every time. That consistency across 4
    unrelated implementations points to something specific to the
    user's network path (a corrupted CDN cache entry, or a security
    appliance capping the transfer by content identity), not a bug in
    any of the scripts used.

Full technical account: `../02_Tools/docling/observations.md` and
`../03_Benchmark_Results/Round1_Execution_Status.md`.

**Per explicit instruction, this line of investigation is now closed.**
No further download attempts were made.

## PDFs used

5 of the 11 benchmark PDFs were obtained (supplied directly by the user
after ClickUp's attachment CDN proved unreachable from this sandbox) and
were genuinely inspected — real page renders were made, real content
characteristics confirmed by rendering the actual pages, not assumed
from filenames:

| TC | Scenario | PDF | Fixture confirmed |
|---|---|---|---|
| TC27 | Ordinary digital text | `briefing_note_BEP-BN-2026-04.pdf` | Yes — clean single-column prose, paragraphs continue across page breaks |
| TC28 | Multiple columns | `bulletin_no_212.pdf` | Yes — all 3 pages genuinely two-column, column break splits sentences |
| TC29 | Styled headings | `procedure_KAL-SP-06_sample_reception.pdf` | Yes — real 4-level heading hierarchy (title/section/subsection/italic sub-subheading) |
| TC30 | Footnotes | `croyde_1974_braithe_order_offprint.pdf` | Yes — genuine numbered in-text markers + foot-of-page citations |
| TC31 | Simple table | `schedule_of_analysis_charges_2026.pdf` | Yes — 4-column, 8-row table wholly on page 1, no merged cells |

The remaining 6 PDFs (for TC32–TC38) were never obtained this round —
the ClickUp CDN is blocked from this sandbox and no manual upload was
made for those.

## TC27–TC31 scenario records

Each entry below reflects the source PDF as actually rendered and
inspected. "Actual tool observation" is BLOCKED for all 5 — Docling
never produced output, so there is nothing to evaluate structurally;
recording anything else would be fabrication.

---

**TC27 — Text Fidelity / ordinary digital text**
- Input: `briefing_note_BEP-BN-2026-04.pdf`, target page 1
- Source/input observation: clean digital text, normal paragraphs under
  section headings; confirmed by rendering the page directly
- Actual tool observation: **BLOCKED** — Docling's pipeline could not
  initialize (layout model unavailable); no Markdown was produced
- Verdict: **BLOCKED**
- Rationale: tool-level blocker, not a content/fixture issue — see
  "Why" above
- Evidence: `../02_Tools/docling/screenshots/TC27_01_input_pages1-2.png`
  (real source-page render); `../02_Tools/docling/logs/TC27_*` (real
  captured tracebacks, 4 separate attempts across the investigation)

**TC28 — Reading Order & Layout / multiple columns**
- Input: `bulletin_no_212.pdf`, target page 1
- Source/input observation: page visibly two-column; confirmed by
  rendering all 3 pages, all genuinely two-column, column break splits
  sentences mid-thought
- Actual tool observation: **BLOCKED** — same pipeline-initialization
  failure
- Verdict: **BLOCKED**
- Rationale: tool-level blocker
- Evidence: `../02_Tools/docling/screenshots/TC28_01_input_page1.png`
  (+ `TC28_02`, `TC28_03` for pages 2–3); `../02_Tools/docling/logs/TC28_*`

**TC29 — Heading & Section Structure / styled headings**
- Input: `procedure_KAL-SP-06_sample_reception.pdf`, target page 1
- Source/input observation: real 4-level heading hierarchy confirmed by
  rendering page 1 — document title, section headings (Scope,
  Reception, Storage), subsection headings (Chain of custody, Condition
  on arrival), and an italic sub-subheading level (Temperature,
  Container integrity)
- Actual tool observation: **BLOCKED** — same pipeline-initialization
  failure
- Verdict: **BLOCKED**
- Rationale: tool-level blocker
- Evidence: `../02_Tools/docling/screenshots/TC29_01_input_page1.png`
  (+ `TC29_02` for page 3); `../02_Tools/docling/logs/TC29_*`

**TC30 — Heading & Section Structure / footnotes**
- Input: `croyde_1974_braithe_order_offprint.pdf`, target page 1
- Source/input observation: genuine academic-article footnote layout
  confirmed by rendering page 1 — 4 superscript in-text markers, a
  horizontal rule, full citation text at the foot of the page
- Actual tool observation: **BLOCKED** — same pipeline-initialization
  failure
- Verdict: **BLOCKED**
- Rationale: tool-level blocker
- Evidence: `../02_Tools/docling/screenshots/TC30_01_input_page1.png`;
  `../02_Tools/docling/logs/TC30_*`

**TC31 — Table Extraction / simple table**
- Input: `schedule_of_analysis_charges_2026.pdf`, target page 1
- Source/input observation: real 4-column table (Determination / Method
  / Turnaround / Charge per sample), 8 data rows, confirmed by rendering
  page 1 — wholly contained on that page, no merged cells
- Actual tool observation: **BLOCKED** — same pipeline-initialization
  failure
- Verdict: **BLOCKED**
- Rationale: tool-level blocker
- Evidence: `../02_Tools/docling/screenshots/TC31_01_input_page1.png`;
  `../02_Tools/docling/logs/TC31_*`

---

## TC32–TC38

Not attempted. No fixture was obtained for any of these 6 (the ClickUp
CDN is blocked from this sandbox), and independently, the same
tool-level layout-model blocker would apply regardless of fixture
availability. Documented, not silently skipped:
`../02_Tools/docling/observations.md` (TC32–TC38 sections).

## Evidence and repository locations

- Real source-page screenshots (genuine `pymupdf` renders, never
  text-to-image or simulated): `../02_Tools/docling/screenshots/`
- Real captured error logs (every execution attempt, every config
  tried): `../02_Tools/docling/logs/`
- Full per-TC records (Input/Execution/Expected/Observed/Output/
  Evidence/Observation/Verdict/Notes): `../02_Tools/docling/observations.md`
- Install notes, exact offline model spec, and the full model-transfer
  account: `../02_Tools/docling/setup/INSTALL.md`
- Complete execution-phase history across every pass this round:
  `../03_Benchmark_Results/Round1_Execution_Status.md`
- Ready-to-run conversion script (works the moment a valid model
  arrives): `../02_Tools/docling/scripts/run_docling.py`

## Remaining limitations

1. **The layout model** — the sole remaining technical blocker for all
   12 TCs. Not fixable from inside this sandbox; the one attempted
   transfer of a real, user-obtained copy failed for reasons outside
   this session's control (see "Why" above).
2. **6 of 11 benchmark PDFs** (for TC32–TC38) were never obtained this
   round.
3. Two minor items noted along the way, neither blocking: a byte-size
   discrepancy on the TC29 fixture between what ClickUp reported and
   what was supplied (flagged, not resolved — page count and content
   otherwise match); and the TC38 grading-key ambiguity (which of 3
   monospace blocks is graded) flagged during the original fixture
   validation, still unanswered.

## What this deliverable is, honestly

A complete, evidence-backed account of why Docling could not be
benchmarked in this environment this round — real fixtures genuinely
inspected, every technical avenue toward a working layout model
genuinely attempted and documented, nothing fabricated. No PASS,
PARTIAL, or FAIL verdict is recorded anywhere in this document, because
none was earned by an actual Docling run.
