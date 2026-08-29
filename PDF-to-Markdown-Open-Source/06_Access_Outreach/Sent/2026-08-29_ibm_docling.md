**Sent:** 2026-08-29
**To:** deepsearch-core@zurich.ibm.com
**CC:** collaborate@aidemos.com
**Subject:** Evaluation Access Request — PDF-to-Markdown Benchmark (granite-docling-258M)
**Gmail message ID:** 1a04e18667dbb47b

Hi Docling maintainers,

I'm running a comparative evaluation of open-source PDF-to-Markdown tools, focused on real-world documents — dense tables, embedded charts, and scanned pages — rather than clean text-only PDFs.

granite-docling-258M stood out to us as a rare case of a genuinely small (258M-parameter) end-to-end model replacing a whole classical layout+OCR+table ensemble in one pass — a strong fit for a lightweight, CPU-friendly evaluation.

Our current environment can't reach Hugging Face Hub or the Ollama registry, which are the only distribution channels we could find for the model (including the community ONNX/GGUF builds). Is there an alternate way to obtain the weights for evaluation purposes — a direct download link, a mirror, or another supported route? Happy to follow whatever process you'd recommend, and glad to credit the Docling project in the resulting report.

Thanks,
Wrick
