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

## 7. What should happen next

Nothing here can be resolved from inside this sandbox. Two independent
things would need to happen, either of which unblocks Docling's 12 TCs:

1. Someone with unrestricted network access supplies the 11 PDF fixture
   bytes directly into this environment (the same way the original
   3-PDF set was supplied earlier in this project), **and**
2. Docling itself runs somewhere that can reach `modelscope.cn` and
   `huggingface.co` — either a different machine, or this same script
   (`scripts/run_docling.py`) pointed at a pre-cached/offline copy of
   Docling's OCR and layout models if one can be supplied through an
   allowed registry.

Until then, this task recommends **not** re-attempting Docling TC28–38
(would just reproduce the same two errors) and **not** starting the
other 5 subjects (no scenario/TC lines exist for them yet — that is
Pradip's `mint_benchmark_board.py` step, not something to do
unprompted).
