# Kreuzberg extraction config used in this benchmark

```python
kreuzberg.ExtractionConfig(
    output_format=kreuzberg.OutputFormat.MARKDOWN,
    ocr=kreuzberg.OcrConfig(backend="tesseract", language="eng"),
    pdf_options=kreuzberg.PdfConfig(extract_images=True),
    layout=kreuzberg.LayoutDetectionConfig(apply_heuristics=True, table_model="tatr"),
)
```
No `force_ocr` set — relies on Kreuzberg's automatic per-page detection of
whether a text layer exists (confirmed correct on PDF3, which is 100%
image-only).
