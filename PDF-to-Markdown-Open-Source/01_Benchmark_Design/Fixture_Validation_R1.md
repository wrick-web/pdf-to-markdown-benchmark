# Fixture/Scenario Validation — Round 1 (pre-execution gate)

**Status: validation only. No tool has been executed. No evidence slots
have been filled. No fixtures have been approved by this pass — that
decision belongs to the implementation/validation gate Pradip owns.**

## Method and a hard limitation, stated upfront

This validation is based on:
1. The frozen Rev-2 spec (`01_Benchmark_Design/Test_Case_Registry.md`),
   cross-checked directly against each TC line's own "Environment must
   provide" / "Expected behaviour" text on the Docling episode
   (`86bbu4wm7` → its 12 scenario lines → their 12 TC lines) — these
   matched the frozen spec verbatim, no drift found.
2. Pruthviraj Mahalunge's own comments on the input task (`86bbr4dmu`),
   which map each of the 11 PDFs to a scenario and describe, in detail,
   the specific property each fixture was built to test (e.g. "no LaTeX
   is liftable from the equations," "both scans carry no text layer at
   all," "542 checks pass, and a rebuild is byte-identical").

**What this validation could NOT do: open any of the 11 PDFs directly.**
This environment's network egress is locked to PyPI/npm/GitHub; the
ClickUp attachment CDN returns a 403 (confirmed again this session via
both a direct download-URL fetch and `clickup_download_task_attachment`).
Every finding below that depends on a PDF's actual content is therefore
**Pruthviraj's own self-reported build-time assertion, not independently
re-verified against the file bytes.** Where he gave no specific
build-note for a fixture, this is flagged as lower-confidence rather than
assumed fine.

## Per-scenario/test-case validation

| TC | PDF (current, today's upload) | Verdict | Exact issue | What needs confirming |
|---|---|---|---|---|
| **TC27** — S27 ordinary digital text (C10) | briefing_note_BEP-BN-2026-04.pdf, 7pp (grew from 2pp) | **Pass** | None — but the fixture requirement says "a **short** PDF," and 7pp is a real jump from the original 2pp. Deliberate: Pruthviraj's note says the extra length exists specifically so paragraphs "run across the page boundaries," testing running-head splicing into body text — a real, on-capability trap (C10 text fidelity + core rule 7 page-furniture handling), not padding. | Whether 7pp still counts as "short" per Pradip's intent — a judgment call, not a defect. |
| **TC28** — S28 multiple columns (C11) | bulletin_no_212.pdf, 3pp (grew from 1pp) | **Needs clarification** | TC's fixture requirement is "a short PDF **page** with two clear text columns" (singular page). The file grew from 1pp to 3pp; Pruthviraj confirms the columns "divide mid-sentence" (a real, on-point trap for C11), but doesn't say whether all 3 pages are two-column or only one. | Which specific page(s) constitute the graded S28/TC28 region — needed so whoever executes this locates the target precisely (core rule 2). Flagged on the ClickUp line. |
| **TC29** — S29 styled headings (C12) | procedure_KAL-SP-06_sample_reception.pdf, 4pp (grew from 2pp) | **Pass (lower confidence)** | No specific build-note from Pruthviraj describing the heading-hierarchy trap for this file specifically (his named traps list covers bulletin, station table, briefing note, and code note — not this one). Thematically a strong natural fit (SOP-style procedure docs genuinely have multi-level headings). | Nothing blocking — noting only that this one wasn't called out with the same explicit build-time assertion as the others. |
| **TC30** — S30 footnotes (C12) | croyde_1974_braithe_order_offprint.pdf, 4pp (grew from 2pp) | **Pass (lower confidence)** | Same as TC29 — no specific build-note for this file. An academic offprint is a very plausible genre for genuine footnotes. | Nothing blocking, same caveat as TC29. |
| **TC31** — S31 simple table (C13) | schedule_of_analysis_charges_2026.pdf, 3pp (grew from 1pp) | **Needs clarification (mild)** | Fixture requirement is "a **small** PDF containing **one simple** table." Growing 1pp→3pp for what should be a single simple table is a bigger relative jump than most of the other fixtures and has no specific build-note explaining it. | Confirm the extra 2 pages are non-table supporting content (e.g. terms/cover) and don't turn this into a multi-table or complex-table fixture that would overshoot "simple." |
| **TC32** — S32 cross-page table (C13) | monitoring_station_schedule_2026.pdf, 4pp (grew from 2pp) | **Pass** | None. Pruthviraj's note is explicit and on-point: "The station table's split across pages is now the page's decision rather than a fixed one, recorded per page in the build record and checked against the built file." This directly targets the TC32 requirement. | Nothing — this is also the strongest-evidenced fixture in the set. |
| **TC33** — S33 figure with caption (C14) | intertidal_survey_BEP-SR-2026-11.pdf, 3pp, unchanged | **Pass** | None. Page 2 confirmed as figure+caption in both comment batches. | Nothing. |
| **TC34** — S34 data chart (C14) | intertidal_survey_BEP-SR-2026-11.pdf (same file as TC33), page 3, unchanged | **Pass** | None. Pruthviraj: "the chart's twelve values appear nowhere in the text" — confirms this is a genuine image-only chart, not one where a tool could cheat by just copying visible text. Directly on-point for the C14 preservation-vs-enrichment distinction. | Nothing. |
| **TC35** — S35 clean scan (C15) | certificate_of_analysis_KAL-11938.pdf, 1pp, unchanged | **Pass** | None. Pruthviraj: "both scans carry no text layer at all" — this is exactly the property TC35 needs (genuine OCR test, not a fake one with hidden text). | This is Pruthviraj's assertion, not independently confirmed by opening the file — see the method note above. Worth an independent spot-check once file access exists. |
| **TC36** — S36 mixed digital+scanned (C15) | service_report_KAL-ESR-4471.pdf, 3pp, unchanged | **Pass** | None. Page 2 confirmed image-only/no text layer, pages 1 and 3 digital — this closes a real gap flagged in this project's earlier planning work (`Tool_Scenario_Matrix.md`), where no prior document actually mixed both page types in one file. | Same independent-verification caveat as TC35. |
| **TC37** — S37 equations (C16) | technical_note_TIH-TN-18.pdf, 3pp (grew from 2pp), now 6 equations | **Pass** | None. Pruthviraj: "no LaTeX is liftable from the equations" — confirms the equations are genuinely rendered (image/vector/font), not hidden copy-pasteable markup that would make the test trivially gameable. | Independent-verification caveat, same as TC35/36. |
| **TC38** — S38 code block (C17) | operations_note_DS-OP-07.pdf, 3pp (grew from 1pp) | **Needs clarification** | Pruthviraj: the fixture "now carries **three** monospace blocks... The graded one is the indented Python under 'The fix'; the shell invocation and the block-header excerpt are listed in the key as **not graded**." The TC38 ClickUp line itself only says "Environment must provide: A PDF containing a code block" — it does not itself say which of the 3 blocks is the graded target. That information currently lives only in an informal ClickUp comment and, presumably, the ground-truth answer key in `markdown_benchmark/ground_truth/` (a location outside this repo that this environment could not reach). | Confirm the executor of TC38 will actually have access to the ground-truth/answer key identifying "the indented Python under 'The fix'" as the sole graded region — otherwise 3 candidate blocks create a real risk of grading the wrong one. Flagged on the ClickUp line. |

## Summary

- **9 of 12 pass outright** (TC27, TC29\*, TC30\*, TC32, TC33, TC34, TC35, TC36, TC37) — \*TC29/TC30 pass on thematic plausibility only, with no explicit build-note confirming the specific trap (lower confidence than the others).
- **3 need clarification before this reviewer would call the gate closed:** TC28 (which page(s) are graded), TC31 (why the page count tripled for a "simple" table), TC38 (whether the grading key for "which of 3 code blocks" is actually accessible at execution time).
- **None outright fail** a fixture requirement based on what's known.
- **Independent re-verification was not possible** for any fixture (network block) — every "no text layer," "no liftable LaTeX," etc. claim above is Pruthviraj's own build-time assertion, carried over faithfully, not confirmed against file bytes by this reviewer.

## Ready for execution?

**Not yet — matches the user's own framing.** Two separate gates are open:
1. The implementation/validation gate (Pradip's), which this report feeds.
2. The three clarifications above (TC28, TC31, TC38), which don't need to
   block the whole set — TC32–TC37 (6 of 12) have no open questions and
   would be ready to execute the moment the gate closes and file access
   exists.

## ClickUp

Comments posted (issue-flagging only, per instruction — not on the 9
passing lines) on:
- S28 line (`86bbu4wpw`) / TC28 (`86bbu4wqv`)
- S31 line (`86bbu4ww2`) / TC31 (`86bbu4wwq`)
- S38 line (`86bbu4xb7`) / TC38 (`86bbu4xbx`)

No status changes, no evidence slots filled, no scores recorded. Input
task (`86bbr4dmu`) was read only — not edited.
