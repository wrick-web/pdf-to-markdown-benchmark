# Round 1 Execution Status (Rev-2, 2026-09-03)

Per Ajay's instruction relayed for this phase — *"check first the
execution tasks only... check for which tools sir has created those
execution tasks"* — before running anything. **No ClickUp writes were
made this phase** (no comments, no status changes, no subtasks). Every
finding below is stored here first, per instruction; ClickUp gets
updated later, on a separate go.

## 1. Execution tasks found (confirmed live in ClickUp, not taken on Gmail's word)

| Subject | Task ID | Scenario/TC lines | Status |
|---|---|---|---|
| EXEC · Round 1 coordinator | `86bbu4wjn` | 6 subject episodes (overview only, not itself an execution unit) | to do |
| EXEC · doc2mark · PDF-OSS v1 · R1 | `86bbu4wke` | 0 | to do |
| **EXEC · Docling · PDF-OSS v1 · R1** | `86bbu4wm7` | **12** (S27/TC27 … S38/TC38) | to do |
| EXEC · GPT-5.6 terra · PDF-OSS v1 · R1 | `86bbu4xck` | 0 | to do |
| EXEC · LiteParse · PDF-OSS v1 · R1 | `86bbu4xdd` | 0 | to do |
| EXEC · MarkItDown · PDF-OSS v1 · R1 | `86bbu4xeb` | 0 | to do |
| EXEC · PyMuPDF4LLM · PDF-OSS v1 · R1 | `86bbu4xf5` | 0 | to do |

**Only Docling has a tool that Sir has actually set up execution
work-items for.** The other 5 subjects exist as containers but carry no
scenario/TC lines to execute against — per the user's own instruction
("only test tools for which Sir has actually created execution tasks —
do not expand the tool list independently"), nothing was run for them.
This is not something this pass fixed or worked around; per Pradip, the
other 5 episodes get their 12 lines each only when
`scripts/mint_benchmark_board.py` is re-run (owned outside this task).

## 2. Docling execution map (the only populated subject)

| TC | Fixture (`86bbr4dmu`) | Fixture available here? | Execution attempted? | Result |
|---|---|---|---|---|
| TC27 | briefing_note_BEP-BN-2026-04.pdf | No — CDN + Gmail both blocked | **Yes** | Blocked (see §3) |
| TC28 | bulletin_no_212.pdf | No | No | Not attempted — same blockers apply |
| TC29 | procedure_KAL-SP-06_sample_reception.pdf | No | No | Not attempted |
| TC30 | croyde_1974_braithe_order_offprint.pdf | No | No | Not attempted |
| TC31 | schedule_of_analysis_charges_2026.pdf | No | No | Not attempted |
| TC32 | monitoring_station_schedule_2026.pdf | No | No | Not attempted |
| TC33 | intertidal_survey_BEP-SR-2026-11.pdf (p.2) | No | No | Not attempted |
| TC34 | intertidal_survey_BEP-SR-2026-11.pdf (p.3) | No | No | Not attempted |
| TC35 | certificate_of_analysis_KAL-11938.pdf | No | No | Not attempted |
| TC36 | service_report_KAL-ESR-4471.pdf | No | No | Not attempted |
| TC37 | technical_note_TIH-TN-18.pdf | No | No | Not attempted |
| TC38 | operations_note_DS-OP-07.pdf | No | No | Not attempted |

TC27 was picked first because it's listed first on the board and had no
open clarification flag from `Fixture_Validation_R1.md` (unlike
TC28/TC31/TC38). The other 11 were not separately attempted once TC27
established that **both** the fixture-retrieval blocker and Docling's
own model-download blocker are structural to this sandbox, independent
of which of the 11 PDFs is targeted — repeating the attempt would
reproduce the same two errors 11 more times without new information.

## 3. What was actually run, and what happened

Full detail: `../02_Tools/docling/observations.md`. Summary:

1. Installed `docling==2.124.0` cleanly (`uv venv` + `uv pip install`).
2. Could not retrieve `briefing_note_BEP-BN-2026-04.pdf` — ClickUp's
   attachment CDN (`t9014651757.p.clickup-attachments.com`) returns 403
   from this sandbox (confirmed via direct fetch and via
   `clickup_download_task_attachment`'s signed URL — same 403, a
   host-level block). Gmail's notification email for the same task
   carries no attachment either.
3. Built a one-line throwaway smoke-test PDF (clearly labeled, never
   treated as a fixture substitute) purely to see how far Docling's
   pipeline gets.
4. Default pipeline (OCR on): failed downloading RapidOCR's PyTorch
   weights from `modelscope.cn` (blocked). Real traceback captured.
5. Retried with `do_ocr=False`: failed downloading the
   `docling-project/docling-layout-heron` layout model from the Hugging
   Face Hub (blocked — layout is not optional in Docling's standard
   pipeline). Real traceback captured.

**Both real tracebacks, a real rasterized page, and text-to-image
renderings of both failures are saved under
`../02_Tools/docling/{logs,screenshots}/`.**

## 4. Tasks already tested vs. still pending

- **Tested (attempted, with real evidence of the outcome): TC27 —
  blocked, not scored.**
- **Pending: TC28–TC38 (11 of 12)** — not attempted, for the reason in
  §2. Would need the same two blockers resolved first.
- **Pending (no execution unit yet): doc2mark, GPT-5.6 terra,
  LiteParse, MarkItDown, PyMuPDF4LLM** — 0 scenario/TC lines each.

## 5. Blockers (both evidence-backed, not inferred)

1. **Fixture retrieval.** The 11-PDF set on `86bbr4dmu` is not reachable
   from this sandbox by any path tried: ClickUp's attachment CDN (403,
   confirmed twice — raw fetch and the tool's own signed URL) and Gmail
   notification emails (HTML template, zero attachments, confirmed by
   opening one in full).
2. **Docling's own model downloads.** Even given a substitute PDF,
   Docling's standard pipeline cannot initialize in this sandbox at all:
   OCR weights come from `modelscope.cn` (blocked) and the layout model
   comes from `huggingface.co` (blocked), and layout is not skippable.
3. Neither blocker is specific to TC27 or to the smoke-test file — both
   are sandbox network-policy limits that would affect every one of the
   12 Docling TCs identically.

## 6. Files/evidence created this phase

```
02_Tools/docling/
├── setup/INSTALL.md
├── scripts/run_docling.py          (ready to run, not yet executed successfully)
├── input/README.md                 (empty — fixture not retrievable)
├── raw_output/README.md            (empty — no run completed)
├── markdown_output/README.md       (empty — no run completed)
├── logs/pipeline_init_default_ocr.log
├── logs/pipeline_init_ocr_disabled.log
├── screenshots/01_smoketest_pdf_page.png
├── screenshots/02_error_default_ocr.png
├── screenshots/03_error_ocr_disabled.png
├── screenshots/README.md
└── observations.md
```

## 6b. Second verification pass (same day, this session — re-checked before further execution)

Ajay relayed that approval had moved from planning to execution, with an
explicit instruction to re-verify the live ClickUp state before running
anything further (not assume last pass's findings still hold) and to
retrieve the 11 PDFs via ClickUp/Gmail rather than ask for manual
uploads. Re-checked everything live rather than reusing the prior
pass's conclusions:

1. **Subject board re-fetched (`86bbu4wjn` + its 6 children).** Unchanged
   from §1: still 6 subjects, still only Docling (`86bbu4wm7`) has
   scenario/TC lines (12). No new subject has execution work minted.
2. **Input task re-fetched with attachments (`86bbr4dmu`).** This time
   the fetch returned full attachment records for all 11 PDFs (id,
   title, exact byte size) — confirming the files genuinely exist on
   the task, not just referenced in comments. This is new information
   since the last pass (which had not pulled attachment metadata this
   directly).
3. **Attempted a real download of the TC27 fixture** using a freshly
   issued signed URL (`clickup_download_task_attachment` on
   `86bbr4dmu` / `briefing_note_BEP-BN-2026-04.pdf`, 105,012 bytes) and
   `curl`'d it immediately. Result: `connect_rejected`, gateway answered
   403 to CONNECT — confirmed via the egress proxy's own status endpoint
   as an organization policy denial on
   `t9014651757.p.clickup-attachments.com`, not an expired/malformed
   URL. No partial or empty file was left behind.
4. **Searched Gmail directly for the PDFs as real attachments** (not
   ClickUp notification templates) — by filename
   (`briefing_note_BEP-BN-2026-04`, `bulletin_no_212`, etc.) and by
   sender (Pruthviraj, Haresh). Zero results both ways. Confirms Gmail
   carries no path to the actual bytes, not just that one sampled
   notification email lacked one.
5. **Re-tested Docling's own two model dependencies directly** (not
   through Docling — a plain `curl` to the exact URLs from last pass's
   tracebacks): `www.modelscope.cn` (RapidOCR weights) and
   `huggingface.co` (docling-layout-heron) both still `connect_rejected`
   / 403. Even given the real fixture, Docling's standard pipeline still
   cannot initialize in this sandbox.
6. **Checked whether the formal validation gate or the 3 flagged
   clarifications had moved.** `86bbk6p7k` (VALIDATION GATE) is still
   status "to do" with 2 open dependencies. The 3 comments this project
   flagged on TC28/TC31/TC38 (`86bbu4wqv`, `86bbu4wwq`, `86bbu4xbx`)
   each still show 0 replies. Noted as a real discrepancy, not resolved
   quietly: Ajay's relayed approval to move into execution is being
   treated as authoritative for this phase per the user's explicit
   instruction, even though the ClickUp gate task itself has not been
   formally closed.

**Conclusion: nothing changed materially.** Both blockers from §5 are
reproduced fresh, with concrete new evidence (a live attachment listing,
a freshly issued and immediately attempted signed URL, a live proxy
status log, a live Gmail attachment search, and live re-checks of both
of Docling's model-download hosts). No execution completed this pass.
No new screenshots were generated this pass, since nothing new actually
ran — this phase's instructions explicitly prohibit text-to-image
renderings as a screenshot substitute, so rather than reuse that
workaround again, this is simply documented as: no genuine execution
evidence exists yet to screenshot.

## 6c. Real-fixture execution, TC27–TC31 (same day, this session)

The user manually supplied the 5 real assigned fixtures for TC27–TC31
(`briefing_note_BEP-BN-2026-04.pdf`, `bulletin_no_212.pdf`,
`procedure_KAL-SP-06_sample_reception.pdf`,
`croyde_1974_braithe_order_offprint.pdf`,
`schedule_of_analysis_charges_2026.pdf`) directly into this session,
since §6b's attempt to retrieve them via ClickUp/Gmail was still
blocked. Byte sizes matched the ClickUp attachment records for 4 of the
5; `procedure_KAL-SP-06_sample_reception.pdf` did not (128,546 bytes
here vs. 43,662 bytes reported earlier), though page count and content
matched — flagged, not resolved, in
`../02_Tools/docling/observations.md`.

**This removed the fixture-retrieval blocker for these 5 TCs, but not
the tool-level one.** Ran Docling's real default pipeline against each
real file. All 5 failed identically and reproducibly: RapidOCR's weight
download from `modelscope.cn` is blocked, confirmed per-file with a
fresh traceback for each
(`../02_Tools/docling/logs/TC2{7,8,9}_*_default.log`,
`TC3{0,1}_*_default.log`). Also confirmed via direct source review
(`docling/datamodel/layout_model_specs.py`) that every layout-model
preset Docling ships is Hugging-Face-hosted only, with no bundled/
offline alternative — so the second-stage failure already proven for
TC27 (`TC27_briefing_note_do_ocr_false.log`) applies to all 5 by
construction, not by assumption.

Produced genuine (non-fabricated, non-text-to-image) evidence for all
5: real `pymupdf` rasterizations of the actual source pages
(`../02_Tools/docling/screenshots/TC2{7,8,9}*.png`,
`TC3{0,1}*.png`) plus the real per-file tracebacks. Full 13-point
evidence record per TC: `../02_Tools/docling/observations.md`.

Two of the fixture-validation clarifications flagged earlier in this
project were resolved by actually looking at the rendered pages this
time (not by assumption): TC28's "which page(s) are graded" — all 3
pages of `bulletin_no_212.pdf` are two-column; and TC31's "is the extra
length non-table" — confirmed yes, the table is wholly on page 1 of
`schedule_of_analysis_charges_2026.pdf`. TC38's clarification remains
open (no TC38 fixture supplied this round).

Nothing was written to ClickUp in that same-day pass — per instruction
at the time, pending the user's review. Both the git push and the
ClickUp updates happened in the next pass, once the user reviewed this
evidence and authorized both (§8).

## 8. ClickUp updated; TC32–TC38 attempted and also blocked (same day, next pass)

The user reviewed the TC27–TC31 evidence above and explicitly authorized
executing and updating ClickUp for the Docling task only. Before posting
anything, re-read all 12 scenario lines and TC leaf tasks directly from
ClickUp (not from memory) to confirm IDs, frozen spec text, and capability
mappings — all matched this repo's `Test_Case_Registry.md` verbatim, no
drift found. No existing ClickUp comments had been added by anyone else
since the last check.

**TC32–TC38 (the remaining 7):** attempted to retrieve their fixtures.
Re-fetched the input task's attachments (all 11 PDFs still listed with
real IDs/sizes — one, `intertidal_survey_BEP-SR-2026-11.pdf`, now shows
308,601 bytes, up from the 165,324 bytes recorded in the original
Fixture_Validation_R1.md pass — flagged, not investigated further, since
this TC wasn't reachable anyway). Requested a fresh signed URL for
`monitoring_station_schedule_2026.pdf` (TC32) and attempted the download
immediately: `connect_rejected`/403, identical to every prior attempt.
Per the user's own instruction not to waste time repeating a proven
common blocker, did not repeat the download attempt for the other 5 —
the same CDN block applies uniformly. **TC32–TC38 marked BLOCKED**: no
fixture obtained, and — independently — the same Docling model-download
blocker proven on TC27–TC31 would block them regardless.

**ClickUp updated:** posted one comment each on all 12 TC leaf tasks
(the "retest anchor" tasks — matching the pattern already established
for the 3 fixture-validation clarification comments earlier in this
project), in the Execution / Observation / Result / Evidence format
requested: TC27 (`86bbu4wnw`), TC28 (`86bbu4wqv`), TC29 (`86bbu4wtf`),
TC30 (`86bbu4wv1`), TC31 (`86bbu4wwq`), TC32 (`86bbu4wyp`), TC33
(`86bbu4x0n`), TC34 (`86bbu4x24`), TC35 (`86bbu4x3c`), TC36
(`86bbu4x8d`), TC37 (`86bbu4xah`), TC38 (`86bbu4xbx`). All 12 posted
successfully. Nothing else was touched: no status changes, no
descriptions edited, no other tool's tasks, no parent/input task, no
benchmark design.

Local evidence restructured to match the exact per-TC template the user
specified (Input / Execution / Expected / Observed / Output / Evidence /
Observation / Verdict / Notes) for all 12 TCs:
`../02_Tools/docling/observations.md`. Git pushed to
`claude/pdf-markdown-tools-research-59gyda` so the paths referenced in
the ClickUp comments resolve to real files.

## 9. Environment built from scratch; OCR solved, layout isolated as the sole blocker (same day, third pass)

The user pushed back on treating "Docling's model downloads are
blocked" as a stopping point, and asked for the minimum viable
environment to be built by hand rather than assumed unbuildable. Took
that seriously rather than re-asserting the prior finding:

- **OCR: solved, genuinely, with zero network calls.** The `rapidocr`
  PyPI wheel already bundles ONNX copies of its models
  (`PP-OCRv6_det_small.onnx` etc. under `site-packages/rapidocr/
  models/`). Docling's own `RapidOcrOptions` already defaults to the
  `onnxruntime` backend — it just wasn't taking effect because the
  `onnxruntime` package itself wasn't installed. `uv pip install
  onnxruntime` (plain PyPI, no model download) plus explicitly passing
  `RapidOcrOptions(backend="onnxruntime")` fixed it. Re-ran all 5
  TC27–TC31 fixtures with this config: every one now gets measurably
  further, past OCR construction entirely (confirmed via the real log
  line "File exists and is valid" for the bundled `.onnx` file), before
  hitting the next stage.
- **Layout: checked exhaustively, not assumed, and confirmed
  genuinely unavailable.** 7 independent checks — full detail in
  `../02_Tools/docling/setup/INSTALL.md` — source review (every layout
  preset Docling ships is Hugging-Face-hosted only), no bundled weights
  in any installed package, not on PyPI (404), no GitHub mirror (404,
  a real response — `raw.githubusercontent.com` is otherwise reachable,
  confirmed by pulling Docling's actual public README), `huggingface.co`
  itself blocked, and a different mirror domain entirely
  (`hf-mirror.com`) also blocked — confirming this sandbox enforces an
  allowlist of approved registries, not a blocklist of named-bad hosts,
  so no untried alternative host is likely to work either.

**Net effect:** the blocker for all 12 TCs narrows from "two model
downloads fail" to "exactly one, non-optional, HF-only model fails" —
a materially more precise and more thoroughly checked finding, not a
repeat of the prior one. Per instruction not to weaken the benchmark,
layout was not bypassed or monkey-patched — it underlies reading order,
headings, tables and figures, i.e. most of what S27–S38 test, so a
run without it would not be genuine Docling output.

Corrected two ClickUp comments (TC35, TC36) that had claimed OCR
specifically as their blocker — that claim no longer holds and was
fixed rather than left standing. Posted a brief progress update to
TC27–TC31 as well, since the underlying technical picture materially
changed even though the verdict (BLOCKED) did not.

## 10. Setup script written and run; no legitimate route found (same day, fourth pass)

Per instruction to write and actually run a setup/download script rather
than describe manual steps, created
`../02_Tools/docling/scripts/setup_layout_model.py`. It: (1) checks every
local/HF-cache location for an existing copy before attempting anything
— none found, confirmed not assumed; (2) attempts exactly one real
download per route, no retry loops — the real `huggingface_hub` path
Docling uses, `hf.co` (a genuinely different HF-owned hostname, not the
same URL retried), and `cdn-lfs.huggingface.co` (HF's separate large-file
CDN host). Ran it for real: routes 1–2 both `ProxyError('403
Forbidden')`; route 3's hostname doesn't even resolve via DNS from this
sandbox — a harder block than a proxy rejection. Real output:
`../02_Tools/docling/logs/setup_layout_model_run.log`. Left an empty,
correctly-named drop folder at `../02_Tools/docling/models/
docling-project--docling-layout-heron/` (with its own README) ready for
the 3 required files, but created nothing fabricated in it.

**Conclusion unchanged, now backed by a real, re-runnable script rather
than restated reasoning: no legitimate route from this sandbox reaches
the model.** No ClickUp writes this pass, no new TC executions attempted
— nothing changed materially enough to justify running TC27/28/29/31
again (would just reproduce the same layout failure already on record).

## 7. What should happen next

Fixture access is no longer the blocker for TC27–TC31. OCR is no longer
a blocker for any of the 12. The single remaining blocker, for all 12,
is the layout model — confirmed to have exactly one source (Hugging
Face Hub) with no bundled, PyPI, or GitHub alternative reachable from
this sandbox. Two things would unblock full execution:

1. For TC32–TC38 only: the remaining 6 PDF bytes supplied directly into
   this environment (as was done for TC27–TC31), **and**
2. For all 12 TCs: the layout model made reachable — either this
   environment gets Hugging Face Hub access, or someone with real
   internet access runs `docling-tools models download` (or lets
   Docling run once normally) elsewhere and supplies the resulting
   model directory into this session, so `PdfPipelineOptions.
   artifacts_path` can point at it with no download at all. (2) alone
   would already unblock real output for TC27–TC31 — their fixtures are
   already here.

Until then, this task recommends **not** re-attempting TC27–TC38 with
the same configuration again (would just reproduce the same layout
error) and **not** starting the other 5 subjects (no scenario/TC lines
exist for them yet — that is Pradip's `mint_benchmark_board.py` step,
not something to do unprompted).
