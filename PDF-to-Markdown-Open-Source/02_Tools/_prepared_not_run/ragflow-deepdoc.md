# RAGFlow / DeepDoc (infiniflow)

- Repo: https://github.com/infiniflow/ragflow (component: `/deepdoc`)
- License: Apache-2.0 (confirmed via raw `LICENSE`)

## Why it's compelling
DeepDoc is RAGFlow's document-understanding module: OCR + layout
recognition across 10 element types (text/title/figure/figure-caption/
table/table-caption/header/footer/reference/equation) + table-structure
recognition (5 cell-role labels) + automatic page-rotation correction for
scans. The explicit figure<->caption and table<->caption pairing is
directly relevant to this project's "Caption/Figure Association" criterion,
which most other tools handle poorly or not at all.

## Requirements
- Models served from Hugging Face (the README notes a mirror-endpoint
  workaround for HF-blocked users, implying the maintainers anticipated
  this exact problem)
- GPU/CPU specifics not fully detailed in available docs

## Caveat
DeepDoc is a sub-component of a much larger RAG platform (RAGFlow), not a
lightweight standalone converter — it's designed to feed RAGFlow's own
indexing pipeline, and how cleanly it separates for pure PDF->Markdown use
outside RAGFlow isn't fully documented.

## Reproduce on an unrestricted machine
```bash
git clone https://github.com/infiniflow/ragflow.git
cd ragflow
# see deepdoc/README or ragflow's docker-compose for the minimal DeepDoc-only path
pip install -r deepdoc/requirements.txt
python -m deepdoc.parser.pdf_parser path/to/file.pdf --output out_dir/
```

## Blocked here because
Hugging Face Hub required for model weights; blocked in this sandbox.
