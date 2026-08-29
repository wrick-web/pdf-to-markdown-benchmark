# Outreach Tracker

Master tracking table for the research-access outreach track. Cross-check
against `00_Project_Notes/Tool_Landscape.md` and
`00_Project_Notes/Decisions_and_Exclusions.md` before adding any tool —
only Tier A/B "included" tools from that research belong here. This is
**not** the AIDemos paid-collaboration outreach pipeline.

## Prioritization

**Priority 1 — blocked yesterday specifically by GPU/model/hosted-access
requirements, and access would materially improve the benchmark:**
PaddleOCR-VL / PP-StructureV3, huridocs/pdf-document-layout-analysis,
MonkeyOCR, Chandra, OCRFlux, Nanonets-OCR-s/docext, GLM-OCR,
granite-docling-258M, RAGFlow/DeepDoc, dots.ocr.

**Priority 2 — strong table/OCR/chart/layout capability with a realistic
hosted/free/premium evaluation route (real company behind the tool, likely
to have a support/evaluation channel):** Datalab (Surya + Chandra),
NanoNets (docext), ChatDOC (OCRFlux), Zhipu AI/Z.ai (GLM-OCR), InfiniFlow
(RAGFlow/DeepDoc), Lumina AI Inc (Chunkr), HuriDocs, PaddlePaddle/Baidu.

**Priority 3 — local-only / no external access would materially help:**
Kreuzberg, open-parse, Surya as a standalone component (weights are
already open, the gap is a full pipeline, not access). Not part of this
outreach batch.

First batch (this round), selected as the 6-8 highest-value candidates
where Priority 1 and Priority 2 overlap and a legitimate contact route
could plausibly exist:

1. Datalab (Surya + Chandra) — combined, one company
2. NanoNets (docext / Nanonets-OCR2)
3. ChatDOC (OCRFlux)
4. Lumina AI Inc (Chunkr)
5. InfiniFlow (RAGFlow/DeepDoc)
6. HuriDocs (pdf-document-layout-analysis)
7. PaddlePaddle/Baidu (PaddleOCR-VL)
8. Zhipu AI/Z.ai (GLM-OCR)

MonkeyOCR, granite-docling-258M, and dots.ocr are held for a possible
follow-up batch pending what `Contact_Research.md` finds — these are
more likely to have no direct contact route beyond GitHub.

## Tracking table

| Tool | Maintainer/Company | Contact | Email/Contact Method | Access Requested | Current Access Model | Date Contacted | Status | CC Confirmed | Response | Access Granted? | Credentials/Credits Received? | Next Action |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Surya + Chandra | Datalab | _pending research_ | _pending research_ | Evaluation/API credits or recommended CPU setup | Open-source (Apache-2.0/OpenRAIL-M) + hosted API | — | Not yet contacted | — | — | No | No | Await Contact_Research.md |
| docext / Nanonets-OCR2 | NanoNets | _pending research_ | _pending research_ | Free-tier/trial API access | Commercial OCR co. with OSS toolkit | — | Not yet contacted | — | — | No | No | Await Contact_Research.md |
| OCRFlux | ChatDOC | _pending research_ | _pending research_ | Evaluation access / recommended GPU setup | Open-source (Apache-2.0) | — | Not yet contacted | — | — | No | No | Await Contact_Research.md |
| Chunkr | Lumina AI Inc | _pending research_ | _pending research_ | Evaluation credits on hosted API | Open-source (AGPL-3.0) core + paid cloud | — | Not yet contacted | — | — | No | No | Await Contact_Research.md |
| RAGFlow / DeepDoc | InfiniFlow | _pending research_ | _pending research_ | Hosted demo/trial access | Open-source (Apache-2.0) | — | Not yet contacted | — | — | No | No | Await Contact_Research.md |
| pdf-document-layout-analysis | HuriDocs | _pending research_ | _pending research_ | Guidance on running/evaluating without heavy local infra | Open-source (Apache-2.0), Docker-only | — | Not yet contacted | — | — | No | No | Await Contact_Research.md |
| PaddleOCR-VL / PP-StructureV3 | PaddlePaddle / Baidu | _pending research_ | _pending research_ | Model access route / recommended eval environment | Open-source (Apache-2.0) | — | Not yet contacted | — | — | No | No | Await Contact_Research.md |
| GLM-OCR | Zhipu AI / Z.ai | _pending research_ | _pending research_ | Evaluation/API credits | Open-source (Apache-2.0) + hosted platform | — | Not yet contacted | — | — | No | No | Await Contact_Research.md |
| MonkeyOCR | Yuliang-Liu / academic lab | _pending research_ | _pending research_ | — | Open-source (Apache-2.0) | — | Held for batch 2 | — | — | No | No | Await Contact_Research.md |
| granite-docling-258M | IBM / Docling project | _pending research_ | _pending research_ | — | Open-source (Apache-2.0) | — | Held for batch 2 | — | — | No | No | Await Contact_Research.md |
| dots.ocr | rednote-hilab | _pending research_ | _pending research_ | — | Open-source (MIT) | — | Held for batch 2 | — | — | No | No | Await Contact_Research.md |

Kreuzberg, open-parse, and Surya-as-standalone-component are intentionally
**not** included above — see Priority 3 rationale.
