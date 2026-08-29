# Email Templates — Research Access Outreach

Positioning: a genuine research/evaluation request, not mass outreach and
not a paid-collaboration pitch. Each email below has one real,
tool-specific sentence (architecture, OCR approach, table handling, or
Markdown output) — no generic praise. Target length ~120-180 words.

CC on every send: **collaborate@aidemos.com** (verify before each send).

Subject line pattern used: `Evaluation Access Request — PDF-to-Markdown Benchmark ([Tool Name])`

---

## 1. Datalab (Surya + Chandra)

**To:** [pending verified contact]

Subject: Evaluation Access Request — PDF-to-Markdown Benchmark (Surya / Chandra)

Hi [Name/Team],

I'm running a comparative evaluation of open-source, self-hosted PDF-to-Markdown tools, focused specifically on difficult real-world documents rather than clean text-only PDFs — think dense financial tables with merged cells, embedded charts, and scanned pages needing OCR.

Surya's single-model approach to layout, OCR, and table recognition (and its CPU/Metal path via llama.cpp) stood out as a strong fit, as did Chandra's broader handling of complex tables, forms, and multi-language OCR in one pass. We'd like to evaluate both properly against our benchmark set rather than relying on documentation claims alone.

Our current environment is CPU-limited, so we wanted to ask whether you offer a hosted evaluation route, API credits, or a recommended lightweight setup that would let us test both models fairly without building out GPU infrastructure ourselves. Happy to follow whatever process you'd recommend, and glad to acknowledge Datalab in the resulting write-up where relevant.

Thanks for your time,
[Sender name]

---

## 2. NanoNets (docext / Nanonets-OCR2)

**To:** [pending verified contact]

Subject: Evaluation Access Request — PDF-to-Markdown Benchmark (docext / Nanonets-OCR2)

Hi [Name/Team],

I'm running a comparative evaluation of open-source PDF-to-Markdown tools, focused on real-world documents — dense financial tables, embedded charts, and scanned pages — rather than clean text-only PDFs.

docext's semantic tagging stood out to us in particular: handling checkboxes, watermarks, signatures, and rendering flow-charts as Mermaid diagrams is a genuinely different approach to chart handling than anything else we've reviewed. We'd like to test it properly against our three benchmark documents.

Running the 3B model at reasonable speed benefits from GPU access, which our current evaluation environment doesn't have. If NanoNets offers a free tier, trial credits, or a researcher/developer evaluation program for the hosted API, we'd like to use that route rather than standing up our own infrastructure. Happy to follow your recommended setup, and glad to credit NanoNets in the resulting report where appropriate.

Thanks,
[Sender name]

---

## 3. ChatDOC (OCRFlux)

**To:** [pending verified contact]

Subject: Evaluation Access Request — PDF-to-Markdown Benchmark (OCRFlux)

Hi [Name/Team],

I'm running a comparative evaluation of open-source PDF-to-Markdown tools against real-world documents — dense financial tables, embedded charts, and scanned pages — rather than clean, simple PDFs.

OCRFlux's automatic cross-page table and paragraph merging is a genuinely distinctive feature for us — most tools we've tested treat each page independently and lose a table that spans a page break, which is exactly the failure mode our benchmark documents are designed to surface.

The model needs a reasonably capable GPU to run at practical speed, which our current evaluation setup doesn't have. If there's a hosted demo, evaluation credits, or a recommended lightweight configuration you could point us to, we'd like to use that rather than building GPU infrastructure ourselves. Happy to follow your suggested process, and glad to credit OCRFlux/ChatDOC in the resulting write-up.

Thanks,
[Sender name]

---

## 4. Lumina AI Inc (Chunkr)

**To:** [pending verified contact]

Subject: Evaluation Access Request — PDF-to-Markdown Benchmark (Chunkr)

Hi [Name/Team],

I'm running a comparative evaluation of open-source, self-hosted PDF-to-Markdown tools, testing against real-world documents with dense tables, embedded charts, and scanned pages rather than clean text-only PDFs.

Chunkr's breadth of format support and genuine CPU/Mac-ARM compatibility (alongside GPU) stood out among the tools we reviewed — most comparable projects assume GPU-only deployment.

Our current evaluation environment doesn't have container orchestration set up for a multi-service stack, so rather than standing that up ourselves, we wanted to ask whether Chunkr offers evaluation credits on the hosted API, or a trial route, that would let us test it fairly against our benchmark set. Happy to follow your recommended evaluation path, and glad to credit Chunkr in the resulting report where appropriate.

Thanks,
[Sender name]

---

## 5. InfiniFlow (RAGFlow / DeepDoc)

**To:** [pending verified contact]

Subject: Evaluation Access Request — PDF-to-Markdown Benchmark (RAGFlow / DeepDoc)

Hi [Name/Team],

I'm running a comparative evaluation of open-source PDF-to-Markdown/document-parsing tools, focused on real-world documents — dense tables, embedded charts, scanned pages — rather than clean text-only PDFs.

DeepDoc's explicit figure-caption and table-caption pairing is particularly relevant to our benchmark, since caption/figure association is one of our evaluation criteria and something most tools we've tested handle poorly.

We'd like to evaluate DeepDoc properly rather than relying on documentation alone. If there's a hosted demo or trial route for RAGFlow that would let us test this without setting up the full platform ourselves, we'd appreciate being pointed to it. Happy to follow whatever setup you'd recommend, and glad to credit RAGFlow/DeepDoc in the resulting report where relevant.

Thanks,
[Sender name]

---

## 6. HuriDocs (pdf-document-layout-analysis)

**To:** [pending verified contact]

Subject: Evaluation Access Request — PDF-to-Markdown Benchmark (pdf-document-layout-analysis)

Hi [Name/Team],

I'm running a comparative evaluation of open-source PDF-to-Markdown/document-parsing tools against real-world documents — dense tables, embedded charts, and scanned pages.

Your project's dual approach — a classical, CPU-only LightGBM path alongside the GPU-preferred VGT model — is one of the only genuinely non-neural, CPU-first options we found in this space, which made it stand out for our benchmark.

We'd like to evaluate it properly across our three benchmark documents. Our current environment doesn't have container orchestration available, so we wanted to ask whether there's a hosted demo, an existing evaluation instance, or another supported way to test the tool without us standing up the full Docker service. Happy to follow your recommended setup, and glad to credit HURIDOCS in the resulting report where relevant.

Thanks,
[Sender name]

---

## 7. PaddlePaddle / Baidu (PaddleOCR-VL / PP-StructureV3)

**To:** [pending verified contact — likely GitHub Discussions/Issues rather than email]

Subject: Evaluation Access Request — PDF-to-Markdown Benchmark (PaddleOCR-VL / PP-StructureV3)

Hi PaddleOCR team,

I'm running a comparative evaluation of open-source PDF-to-Markdown tools against real-world documents — dense financial tables, embedded charts, and scanned pages — rather than clean text-only PDFs.

PP-StructureV3's dedicated layout-detection stage feeding a compact vision-language model, with native handling of tables, charts, formulas, and both CPU and GPU execution, made it one of the strongest candidates in our review.

We were able to install the package, but full model execution requires downloading weights, and our current environment doesn't have that access. Is there a recommended lightweight evaluation route (a hosted demo, AI Studio project, or alternate model-download path) you'd suggest for testing PP-StructureV3 fairly? Happy to follow whatever process works best, and glad to credit the project in the resulting report.

Thanks,
[Sender name]

---

## 8. Zhipu AI / Z.ai (GLM-OCR)

**To:** [pending verified contact]

Subject: Evaluation Access Request — PDF-to-Markdown Benchmark (GLM-OCR)

Hi [Name/Team],

I'm running a comparative evaluation of open-source PDF-to-Markdown tools against real-world documents — dense tables, embedded charts, and scanned pages — rather than clean text-only PDFs.

GLM-OCR's compact two-stage design (a CPU-capable layout stage feeding a small recognition model) stood out to us as an efficient alternative to the larger VLM-based tools we've reviewed.

Running the recognition stage at practical speed benefits from GPU access, which our current evaluation environment doesn't have. If Z.ai offers API credits, a free tier, or a researcher evaluation program we could use to test GLM-OCR properly, we'd appreciate being pointed to it. Happy to follow your recommended process, and glad to credit GLM-OCR/Z.ai in the resulting report.

Thanks,
[Sender name]

---

## Notes

- `[Sender name]` and exact recipient details are filled in from
  `Contact_Research.md` before any email is sent — no email goes out with
  placeholder text.
- Where research finds no verifiable email and GitHub Discussions/Issues
  is the only legitimate channel, the "email" is not sent — instead this
  is recorded in `Outreach_Tracker.md` as a recommended manual channel for
  the project owner, consistent with "never guess an email address."
