# granite-docling-258M (IBM)

- Model: `ibm-granite/granite-docling-258M` on Hugging Face (companion orgs:
  `docling-project`, `ibm-granite-community` on GitHub)
- License: Apache-2.0
- Productionized Sept 17, 2025, evolving IBM's experimental
  SmolDocling-256M-preview (Mar 2025)

## Why it's compelling — and distinct from already-tested Docling
Docling (already benchmarked in a prior cycle) is a **multi-model ensemble**
pipeline: a separate layout model + TableFormer + a separate OCR engine,
orchestrated by the Docling library. granite-docling-258M is the opposite
design: **one small (258M) end-to-end VLM** (Idefics3 architecture, siglip2
vision encoder + Granite-165M LLM) that replaces that whole ensemble,
emitting "DocTags" convertible to Markdown/HTML/JSON — usable standalone
or plugged back into the Docling library. This is a genuinely different
architecture bet, not a re-test of the same tool.

## Requirements — compute-wise the best story on this list
258M parameters is genuinely tiny. Community **ONNX**
(`onnx-community/granite-docling-258M-ONNX`) and **GGUF**
(`ggml-org/granite-docling-258M-GGUF`) conversions exist, enabling
`onnxruntime`/`llama.cpp` **CPU** inference — this would likely have been
executable in this very sandbox's CPU/RAM budget.

## The actual blocker: distribution, not compute
Every distribution channel found — the official HF repo, both community
conversions, and Ollama's listing (`ibm/granite-docling:258m`) — is
Hugging-Face-hosted or requires an Ollama registry pull. Both are blocked
in this sandbox. No GitHub-releases or PyPI-bundled weight path was found.
**This is the one Tier B tool most worth re-attempting first** if HF
access becomes available, since the compute requirement is trivial.

## Reproduce on an unrestricted machine
```bash
# ONNX / CPU path
pip install onnxruntime huggingface_hub
huggingface-cli download onnx-community/granite-docling-258M-ONNX --local-dir ./granite-docling-onnx
python -m docling_core.granite_runner path/to/file.pdf --model ./granite-docling-onnx --output out_dir/

# or GGUF / llama.cpp path
huggingface-cli download ggml-org/granite-docling-258M-GGUF --local-dir ./granite-docling-gguf
llama-server -m ./granite-docling-gguf/granite-docling-258M.gguf
```

## Blocked here because
Hugging Face Hub and the Ollama registry are both blocked; there is no
GitHub/PyPI-native weight source for this model.
