# Benchmark Design (Rev 2 — FROZEN 2026-08-23)

This folder is a working-copy reference of the **authoritative, frozen
benchmark specification** maintained in ClickUp:

> **PDF → Markdown — research design**
> https://app.clickup.com/9014651757/v/dc/8cn1avd-25874/8cn1avd-66494

That ClickUp doc page is the source of truth. The files in this folder
are a synced, offline-readable copy for this repository's own use (so
tool/capability mapping and test planning can cite exact IDs without a
live ClickUp session) — **they are not a fork of the spec**. If this
folder ever disagrees with the ClickUp page, the ClickUp page wins, and
this folder should be re-synced, not argued with.

## What changed

Rev 2 (frozen 2026-08-23) supersedes Rev 1 (12 capabilities, 56
prioritized scenarios, wave labels). Rev 1 material is history only —
nothing in this repository should be built on it going forward. Rev 2 is:

- **8 capabilities** — `C10`–`C17`
- **12 scenarios** — `S27`–`S38`
- **12 frozen first test cases** — `TC27`–`TC38`

These canonical registry IDs are shared with the AI Demos research
registry (`admin.aidemos.com/v2/research/id/<ID>`) and are used by two
published rankings that share this same research:

- **R1 — PDF to Markdown, Open-Source Libraries** — ClickUp
  [`86ban5kjq`](https://app.clickup.com/t/9014651757/86ban5kjq) (this
  repository)
- **R3 — PDF to Markdown, APIs** — ClickUp
  [`86b9h7t37`](https://app.clickup.com/t/9014651757/86b9h7t37) (separate
  research, not this repository)

Same test documents, same scenarios, same grading — each tool still gets
its own run and its own evidence.

## Files in this folder

- `Capability_Registry.md` — C10–C17, what each protects
- `Scenario_Registry.md` — S27–S38, grouped under their capability
- `Test_Case_Registry.md` — TC27–TC38: capability, scenario, minimum
  fixture requirement, expected behavior, candidate tools, current status
- `Core_Research_Rules.md` — the 11 rules that govern every run
- `Input_Status.md` — fixture/input availability per test case (as of this
  writing: **fixture authoring has not started** — it begins only on
  Pradip's go — and the actual input documents are expected from
  **Pruthviraj & Haresh**, not yet received)

## Relationship to this repository's existing (pre-Rev2) research

The 3-PDF, 9-criteria benchmark already in `00_Project_Notes/`,
`02_Tools/`, `03_Benchmark_Results/`, and `05_Final_Report/` (Kreuzberg,
open-parse, PaddleOCR-VL, huridocs, plus the earlier-cycle tools and the
research-access outreach) was run **before** Rev 2 was frozen, against a
different, ad-hoc scenario design (chart reconstruction, text
preservation, table reconstruction, hierarchy, images, reading order,
captions, robustness, bonus — not the same taxonomy as C10–C17). That
work is **not discarded** — it is real, valuable prior evidence about
several of these same tools — but it does not automatically satisfy any
TC27–TC38 test case, because the scenarios, fixtures, and grading rules
differ. Where a prior observation is directly relevant to a new capability
or scenario, it is cited as **prior evidence to re-map**, never silently
presented as if it were a Rev-2 test run. See
`02_Tools/Tool_Capability_Matrix.md` for exactly which prior observations
map to which new capability, and how.
