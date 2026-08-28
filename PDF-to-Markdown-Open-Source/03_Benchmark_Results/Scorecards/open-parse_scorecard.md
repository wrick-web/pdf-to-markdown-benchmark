# Scorecard — open-parse (base mode)

See `03_Benchmark_Results/MASTER_RESULTS.md` for the full table with
per-PDF breakdown and evidence pointers, and
`02_Tools/open-parse/observations.md` for the full qualitative write-up.

| Criterion | Score /5 |
|---|---|
| Chart Reconstruction | 0 |
| Text Preservation | 1 |
| Table Reconstruction (DEGRADED where it ran at all) | 1 |
| Document Hierarchy | 0 |
| Image Retention | 1 |
| Reading Order | 2 |
| Caption/Figure Association | 1 |
| Long/Complex Document Robustness | 0 |
| Bonus/Anomalous | 1 |
| **Overall** | **≈0.8** |

**One-line verdict:** Fast and dependency-light for the single simplest
benchmark PDF, but crashed outright on the most complex one, produced zero
headings anywhere, and returned silently-empty output on the scanned PDF —
scored here explicitly as a lightweight native-text baseline, not a
contender for this use case's complex/mixed-PDF requirement.
