# Evidence (Rev 2 — Tool × Test Case × Test Run)

This folder holds **Evidence** in the Rev-2 sense defined by the AI Demos
research model: the main inspectable result of one **Tool × Test Case ×
Test Run**, bringing together tool/model, capability, scenario, test
case, test run, expected behavior, actual output, key observations,
verdict, supporting artifacts, researcher, tested date, and QA status.

## Current status: empty, pending fixtures

No Evidence exists here yet because:
1. Fixture authoring for TC27–TC38 has not started (Pradip's go pending).
2. The actual input documents are expected from Pruthviraj & Haresh and
   have not been received.

See `01_Benchmark_Design/Input_Status.md` for the live per-TC status.

## Planned structure once execution starts

```
04_Evidence/
├── TC27_text_fidelity/
│   ├── <tool>_<date>.md      one Evidence page per Tool x Test Run
│   └── artifacts/            raw output, screenshots, logs for that run
├── TC28_reading_order/
├── ...
└── TC38_code_block/
```

Each Evidence page will follow the Rev-2 Evidence fields: Tool/model,
Capability, Scenario, Test Case, Test Run (version/config/researcher/
date), expected behavior (recorded before the run, per core rule 5),
actual output, Observations, verdict (complete/accurate/faithful/honest
per core rule 6), score where applicable, supporting Artifacts,
QA/current-vs-superseded status.

## Relationship to `03_Benchmark_Results/` (pre-Rev2)

`03_Benchmark_Results/` holds this project's **pre-Rev2** results
(MASTER_RESULTS.md, Scorecards, Comparison_Tables, Evidence excerpts) —
real work, kept as history, graded under the old 9-criteria/3-PDF design.
This folder (`04_Evidence/`) is reserved specifically for Rev-2-conformant
Evidence (TC27–TC38, one scenario → one focused verdict). The two are not
merged, so it stays clear which methodology produced which result — see
`03_Benchmark_Results/REMAP_NOTE.md`.
