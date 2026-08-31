# Core Research Rules

Verbatim from the frozen spec (ClickUp doc `8cn1avd-25874` / page
`8cn1avd-66494`). These govern every test run in this research — read
before planning or executing anything.

1. **Capability / scenario / test case / attribute definitions and review
   tests:** the benchmark design standard governs
   (`docs/decisions/BENCHMARK-DESIGN-STANDARD.md` in the workspace repo —
   **not this repository**; that file was not reachable from this
   research environment and its contents are not reproduced here. Check
   any proposed taxonomy change against it before proposing one).
2. **One scenario → one focused verdict, one evidence unit.** One run of
   a compound document may legitimately answer several scenarios — each
   target is located precisely (page/region) and graded separately; one
   failure never contaminates an unrelated scenario's grade.
3. **Always send the complete PDF, never a cropped page.** The target
   region is what gets graded, not what gets sent.
4. **The canonical run condition is each tool's default pipeline, one
   pass, no per-tool flag tuning.** Alternate or premium configurations
   are separate recorded runs, never silently substituted. Always record
   the exact tool version (open-source) or plan/mode (API).
5. **Expectations are written from the source document before any tool is
   run.** We grade against the source, never against whichever tool did
   best.
6. **Every verdict grades four things:** complete (nothing important
   omitted) · accurate (nothing corrupted) · faithful (nothing invented)
   · honest (uncertainty and failure exposed). **Invented content is the
   worst failure** — worse than an honest gap. Silent omission or empty
   output reported as success is recorded on the run wherever it occurs.
7. **Presentation furniture is not content.** Removing repeated running
   headers, page numbers and watermarks is *correct*, not lossy.
8. **HTML table blocks inside Markdown are valid output** where Markdown
   cannot express the structure. We grade whether the information
   survives, not whether the syntax is pure Markdown.
9. **A missing capability scores 0 and stays in the ranking arithmetic**;
   `not_applicable`, `not_measured`, and `blocked` (with the reason —
   never a 0) are distinct states.
10. **At least one strong general-purpose multimodal model runs as a
    reference subject** — selected at execution time, under a versioned
    conversion instruction, a separate subject never blended into any
    product's score.
11. **Own fixtures, never public datasets** — fixture identity is the
    content hash; one artifact serves as many test cases as it naturally
    can.

## How this repository applies them right now (pre-execution)

- No fixtures exist yet, so no rule above is being exercised in
  execution — this stage is planning only (see `01_Benchmark_Design/Input_Status.md`).
- Rule 4 (record exact tool version, default pipeline, no tuning) is
  already reflected in this repository's existing tool setup files
  (`02_Tools/<tool>/setup/`) and should carry forward unchanged once
  Rev-2 execution starts.
- Rule 9's distinction (missing capability = 0, but blocked/not_measured
  ≠ 0) is exactly why this repository's prior PaddleOCR-VL and huridocs
  results are recorded as **BLOCKED** (with the specific reason —
  Hugging Face/BOS unreachable; no Docker daemon), never as a 0 or a
  silent absence. The same discipline carries into the new capability
  matrix.
