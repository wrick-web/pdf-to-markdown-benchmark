# Outreach Tracker

Master tracking table for the research-access outreach track. Cross-check
against `00_Project_Notes/Tool_Landscape.md` and
`00_Project_Notes/Decisions_and_Exclusions.md` before adding any tool —
only Tier A/B "included" tools from that research belong here. This is
**not** the AIDemos paid-collaboration outreach pipeline.

## Prioritization

**Priority 1 — blocked previously specifically by GPU/model/hosted-access
requirements, where access would materially improve the benchmark:**
PaddleOCR-VL / PP-StructureV3, huridocs/pdf-document-layout-analysis,
MonkeyOCR, Chandra, OCRFlux, Nanonets-OCR-s/docext, GLM-OCR,
granite-docling-258M, RAGFlow/DeepDoc, dots.ocr.

**Priority 2 — strong table/OCR/chart/layout capability with a realistic
hosted/free/premium evaluation route:** Datalab (Surya + Chandra),
NanoNets (docext), ChatDOC (OCRFlux), Zhipu AI/Z.ai (GLM-OCR), InfiniFlow
(RAGFlow/DeepDoc), Lumina AI Inc (Chunkr), HuriDocs, PaddlePaddle/Baidu.

**Priority 3 — local-only / no external access would materially help (not
part of this outreach):** Kreuzberg, open-parse, Surya as a standalone
component.

## First batch — sent 2026-08-29

Full contact verification detail: `Contact_Research.md`. Full sent email
copies: `Sent/`.

| Tool | Maintainer/Company | Contact | Access Requested | Current Access Model | Date Contacted | Status | CC Confirmed | Response | Access Granted? | Credentials/Credits Received? | Next Action |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Surya + Chandra | Datalab | hi@datalab.to | Evaluation credits / guidance on hosted playground-API testing | Open-source (Apache-2.0 / OpenRAIL-M) + hosted API | 2026-08-29 | **Sent** | Yes | Awaiting reply | No | No | Wait for reply; follow up if none by ~1 week |
| docext / Nanonets-OCR2 | NanoNets | support@nanonets.com | Free-tier/trial credits for hosted API | Commercial OCR co. with OSS toolkit | 2026-08-29 | **Sent** | Yes | Awaiting reply | No | No | Wait for reply; follow up if none by ~1 week |
| PaddleOCR-VL / PP-StructureV3 | PaddlePaddle / Baidu | paddleocr@baidu.com | Access route via Baidu AI Studio hosted demo | Open-source (Apache-2.0) | 2026-08-29 | **Sent** | Yes | Awaiting reply | No | No | Wait for reply; follow up if none by ~1 week |
| granite-docling-258M | IBM / Docling project | deepsearch-core@zurich.ibm.com | Alternate (non-HF/Ollama) route to obtain model weights | Open-source (Apache-2.0), no hosted product | 2026-08-29 | **Sent** | Yes | Awaiting reply | No | No | Wait for reply; follow up if none by ~1 week |
| RAGFlow / DeepDoc | InfiniFlow | yingfeng.zhang@infiniflow.org | Evaluation access to cloud/demo environment | Open-source (Apache-2.0) + managed cloud | 2026-08-29 | **Sent** | Yes | Awaiting reply | No | No | Wait for reply; follow up if none by ~1 week |
| Chunkr | Lumina AI Inc | mehul@chunkr.ai | Evaluation credits on hosted Cloud API | Open-source (AGPL-3.0) core + paid cloud | 2026-08-29 | **Sent** | Yes | Awaiting reply | No | No | Wait for reply; follow up if none by ~1 week |
| pdf-document-layout-analysis | HuriDocs | hello@huridocs.org | Hosted instance/demo, or guidance on evaluating without local Docker infra | Open-source (Apache-2.0), Docker-only, nonprofit | 2026-08-29 | **Sent** | Yes | Awaiting reply | No | No | Wait for reply; follow up if none by ~1 week |
| dots.ocr | rednote-hilab | yanqing4@xiaohongshu.com | Evaluation access via hosted demo or research collaboration route | Open-source (MIT) | 2026-08-29 | **Sent** | Yes | Awaiting reply | No | No | Wait for reply; follow up if none by ~1 week |

## Held / not contacted this batch

| Tool | Maintainer/Company | Reason not contacted |
|---|---|---|
| MonkeyOCR | VLRLab, HUST (Prof. Xiang Bai / Yuliang Liu) | Published contact (xbai@hust.edu.cn, ylliu@hust.edu.cn) is explicitly scoped in their own README to commercial licensing inquiries, not research-access requests — holding for a differently-framed ask in a later round rather than emailing the wrong request to that address. |
| OCRFlux | ChatDOC | No verified official email — the project's own GitHub README lists Discord, not an email; a Gmail address found in secondary sources was not confirmed on any first-party ChatDOC page, so it was not used. |
| GLM-OCR | Zhipu AI / Z.ai | No verified official email — both the GitHub README and org page list Discord only; an "enterprise.support@z.ai" address found in secondary sources could not be confirmed on any first-party z.ai/bigmodel.cn page. |

## Not part of this outreach (Priority 3)

Kreuzberg, open-parse, Surya-as-standalone-component — already fully open
and local; no external access would materially change what can be tested.
