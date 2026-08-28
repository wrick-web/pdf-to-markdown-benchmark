# Recommendations

## If you need this working today, self-hosted, CPU-only

Use **Kreuzberg** for text extraction, headings (on native-text PDFs),
image extraction, and OCR fallback on scanned pages. Do **not** trust it
for tables — every table in this benchmark came out as flattened,
unstructured text. Pair it with a dedicated table pipeline (e.g., a
classical table-detection library, or manual review) for any document
where table fidelity matters, which is most real financial/report PDFs.

Do not use **open-parse** (base mode) as a primary tool for this use case:
it crashed on the most complex benchmark document and has no OCR or
heading support at all. It's fine as a fast fallback for simple, clean,
native-text-only PDFs with no charts and no scans — nothing else.

## If you have a GPU and normal internet access

Prioritize testing, in this order, based on what each documents as its
strongest differentiator (none of these claims were verified by this
project — see the caveat in `Final_Comparison.md` section 17):

1. **PaddleOCR-VL / PP-StructureV3** — the only Tier A candidate this
   cycle with a real CPU story on paper *and* a documented (if also
   blocked-here) non-Hugging-Face model source; likely the best first
   re-test once you have HF or BOS access.
2. **MonkeyOCR** or **OCRFlux** — both specifically target table fidelity
   (TableTEDS 76.5-87.5% claimed for MonkeyOCR; OCRFlux's unique
   cross-page table-merging is directly relevant to PDF1/PDF2's multi-page
   financial statements).
3. **granite-docling-258M** — smallest model on the whole list (258M
   params) with community ONNX/GGUF builds; worth trying first if your
   only real constraint was this project's *distribution* blocker (no HF/
   Ollama access) rather than a genuine hardware limit, since the compute
   footprint is trivial.
4. **huridocs/pdf-document-layout-analysis** — if you have Docker, its
   LightGBM CPU path is one of the only genuinely classical (non-neural)
   options found this cycle, worth a quick spike even without a GPU.

## What NOT to do

Don't adopt Chandra or Chunkr into a commercial/production pipeline
without reviewing their license terms first — Chandra's model weights are
OpenRAIL-M with an explicit "commercial self-hosting requires a license"
clause, and Chunkr is AGPL-3.0 (copyleft, network-use clause).

## For the next research cycle

- Re-run PaddleOCR-VL, huridocs, and the 10 Tier B tools on a machine with
  GPU + normal internet access, using the exact same 3 benchmark PDFs, to
  get real (not documentation-claimed) scores comparable to this cycle's
  Kreuzberg/open-parse numbers.
- Clear the existing gap: Marker (now v2, released 2026-07-20), olmOCR,
  and pdf-craft were named as "known" tools in the ClickUp task since an
  earlier cycle but have never actually been benchmarked by anyone.
- Consider building a small, dedicated table-extraction supplement to pair
  with Kreuzberg for a realistic production pipeline (Kreuzberg's own
  text/OCR/hierarchy handling is otherwise solid).
