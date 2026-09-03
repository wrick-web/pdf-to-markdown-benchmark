# Empty — drop the model here

Created by `../../scripts/setup_layout_model.py`, which could not obtain
the model from this sandbox (see `../../logs/setup_layout_model_run.log`
for the real, unedited run output).

Put these 3 files directly in this folder:
- `config.json`
- `preprocessor_config.json`
- `model.safetensors` (or `pytorch_model.bin`)

from Hugging Face repo `docling-project/docling-layout-heron` (revision
`main`), then set `DOCLING_ARTIFACTS_PATH` to this folder's parent
directory (`.../docling/models`) and run
`scripts/run_docling.py` as normal — no other change needed.
