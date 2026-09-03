# ClickUp Task Map — Round 1 (PDF→Markdown, Open Source)

Built by cross-referencing Gmail notifications against live ClickUp data
(every task below was opened directly, not taken on the email's word).
Source of truth for the design: the frozen spec doc. Source of truth for
inputs: the input-pdfs task. Neither was edited to produce this map.

## A. Complete task inventory

### Design & inputs (read-only, never modified)
| Task | ID | Note |
|---|---|---|
| PDF → Markdown — research design (Rev 2, frozen 2026-08-23) | doc `8cn1avd-25874` / page `8cn1avd-66494` | 8 capabilities, 12 scenarios, 12 TCs |
| input pdfs | `86bbr4dmu` | 11 current PDFs; superseded set from an earlier upload still attached (Pruthviraj notes it can't be deleted via API, needs manual cleanup) |

### Parent research task and its Cycle-I/II subtasks (untouched, unrelated to Round 1 execution)
| Task | ID | Status |
|---|---|---|
| PDF to markdown using open source libraries (parent) | `86ban5kjq` | in progress |
| Use Case Definition, Criteria & Examples | `86ban5kjy` | complete |
| Tool List & Access Outreach | `86ban5kk5` | complete |
| Test Inputs & Artifact Creation | `86ban5kka` | complete — carries the pre-Rev2 3-PDF benchmark + Pradip's 2026-09-03 reply to my WAITING FOR INPUT APPROVAL comment |
| — docling / pymupdf4llm / liteparse / doc2mark / markitdown / MinerU / Paddlerocr / Dolphin / Unstructured / DocTR | (10 sub-subtasks, IDs already on file) | Cycle-I/II evidence, pre-Rev2, not carried forward |
| Observations & Screenshots | `86bbp9qmb` | complete |
| Included Tools & Rationale | `86bbp9qva` | complete |
| Research Access Outreach (Tool Maintainers) | `86bbpvd4c` | to do |

### Implementation / validation gate (owns whether Round 1 can run)
| Task | ID | Assignee | Status |
|---|---|---|---|
| IMPL · PDF→Markdown — fixture corpus + ground truth (12 TCs) | `86bbk6p45` | Pruthviraj Mahalunge | to do |
| — Fixture corpus — smallest normal input per TC27–TC38 | `86bbk6p4w` | Pruthviraj | to do |
| — Ground truth — expected source truth per tested region | `86bbk6p5j` | Pruthviraj | to do |
| — Hash + register artifacts | `86bbk6p6a` | Pruthviraj | to do |
| — Scanned pages — VERIFIED to carry no text layer | `86bbu4vhw` | Pruthviraj | to do |
| — Rubrics — one per scoped scenario (12), pinned to benchmark_scope | `86bbu4vj5` | Pruthviraj | to do |
| — **VALIDATION GATE — all 12 TCs executable** | `86bbk6p7k` | Haresh Nichite | to do, 2 open dependencies |

**Every one of these is still "to do."** Nothing under the IMPL task is closed. The validation gate specifically (`86bbk6p7k`) has 2 unresolved dependencies.

### Round 1 execution board (assignee: Wrick)
| Task | ID | Subtasks | Status |
|---|---|---|---|
| EXEC · Round 1 coordinator (overview only) | `86bbu4wjn` | 6 subject episodes | to do |
| — EXEC · doc2mark · PDF-OSS v1 · R1 | `86bbu4wke` | 0 (episode not yet built out) | to do |
| — EXEC · Docling · PDF-OSS v1 · R1 (reference subject for the checklist) | `86bbu4wm7` | 12 scenario lines, each with 1 TC line | to do |
| — EXEC · GPT-5.6 terra · PDF-OSS v1 · R1 | `86bbu4xck` | 0 | to do |
| — EXEC · LiteParse · PDF-OSS v1 · R1 | `86bbu4xdd` | 0 | to do |
| — EXEC · MarkItDown · PDF-OSS v1 · R1 | `86bbu4xeb` | 0 | to do |
| — EXEC · PyMuPDF4LLM · PDF-OSS v1 · R1 | `86bbu4xf5` | 0 | to do |

Confirmed directly from Pradip's two Gmail replies (both re-opened and
cross-checked in ClickUp, not taken on faith): **Round 1 = the 5 Cycle-I
libraries (doc2mark, Docling, LiteParse, MarkItDown, PyMuPDF4LLM) +
GPT-5.6 terra as the mandated general-purpose reference subject** — never
scored as a competing product. Marker, olmOCR, pdf-craft are Round 2
candidates, not registered as subjects yet. MinerU and Dolphin are typed
as "tools" rather than "libraries" in the new system (Pradip's phrasing;
what that distinction changes procedurally wasn't spelled out and isn't
guessed at here).

Only Docling's episode has scenario/TC lines minted. The other 5 are
empty — per Pradip, this is because the checklist was built against
Docling as the reference subject first, not because something is broken.
The board is minted by `scripts/mint_benchmark_board.py`, which "adds only
what is missing and never duplicates a line" — i.e. re-running it is how
the other 5 episodes would get their 12 lines each, not manual creation.

### Docling's 12 scenario × test-case lines
| Scenario | Test case | Fixture (from input task) | This validation pass |
|---|---|---|---|
| S27 `86bbu4wn7` | TC27 `86bbu4wnw` | briefing_note_BEP-BN-2026-04.pdf | Pass |
| S28 `86bbu4wpw` | TC28 `86bbu4wqv` | bulletin_no_212.pdf | Needs clarification (flagged on the line) |
| S29 `86bbu4wrn` | TC29 | procedure_KAL-SP-06_sample_reception.pdf | Pass, lower confidence |
| S30 `86bbu4wua` | TC30 | croyde_1974_braithe_order_offprint.pdf | Pass, lower confidence |
| S31 `86bbu4ww2` | TC31 `86bbu4wwq` | schedule_of_analysis_charges_2026.pdf | Needs clarification (flagged on the line) |
| S32 `86bbu4wy1` | TC32 | monitoring_station_schedule_2026.pdf | Pass |
| S33 `86bbu4wzj` | TC33 | intertidal_survey_BEP-SR-2026-11.pdf (p.2) | Pass |
| S34 `86bbu4x1h` | TC34 | intertidal_survey_BEP-SR-2026-11.pdf (p.3) | Pass |
| S35 `86bbu4x2t` | TC35 | certificate_of_analysis_KAL-11938.pdf | Pass |
| S36 `86bbu4x43` | TC36 | service_report_KAL-ESR-4471.pdf | Pass |
| S37 `86bbu4x9a` | TC37 | technical_note_TIH-TN-18.pdf | Pass |
| S38 `86bbu4xb7` | TC38 `86bbu4xbx` | operations_note_DS-OP-07.pdf | Needs clarification (flagged on the line) |

TC29/30/32–37's individual task IDs weren't re-fetched this pass (already
verified once against the frozen spec text in the prior validation —
TC27/28/38 were spot-checked again here and matched verbatim, so the
pattern is trusted, not re-confirmed line by line).

## B. Scenario → PDF mapping

Unchanged from the prior validation pass — see `Fixture_Validation_R1.md`
for the full table. 11 PDFs cover all 12 scenarios (one PDF, the
intertidal survey, covers two: S33 and S34).

## C. Tool → scenario/test-case mapping

Round 1 has 6 subjects. Only Docling's 12 lines exist to work against
right now — the other 5 subjects (doc2mark, GPT-5.6 terra, LiteParse,
MarkItDown, PyMuPDF4LLM) have no scenario/TC lines yet, so there is
nothing to map or execute for them until their episodes are built out
(not something to do unprompted — that is presumably also gated behind
`mint_benchmark_board.py`, owned outside this task).

## D. Validation blockers

1. **Implementation gate open.** All 6 IMPL subtasks (`86bbk6p45` and its
   5 children, including the validation gate `86bbk6p7k` itself) are
   status "to do." Two dependencies on the gate are unresolved.
2. **TC28** — which page(s) of the now-3pp bulletin hold the graded
   two-column region. Flagged on `86bbu4wqv`, unanswered as of this
   check.
3. **TC31** — why the "simple table" fixture tripled in page count.
   Flagged on `86bbu4wwq`, unanswered as of this check.
4. **TC38** — whether the ground-truth key identifying which of 3
   monospace blocks is graded will actually be reachable at execution
   time. Flagged on `86bbu4xbx`, unanswered as of this check.
5. **Scanned-page verification** (`86bbu4vhw`) is itself still "to do" —
   Pruthviraj's comment asserts both scanned fixtures carry no text
   layer, but the dedicated verification task tracking that hasn't been
   closed either.

## E. Execution readiness

**Not ready. Gate is open.** Nothing should run.

Once the gate closes: Docling × TC27, TC29, TC30, TC32–TC37 (9 of 12)
have no open question on this end and would be the first candidates to
execute. TC28/TC31/TC38 need their flagged answers first, independent of
the gate. The other 5 subjects have no lines to execute against at all
yet.
