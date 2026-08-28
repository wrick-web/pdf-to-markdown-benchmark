#!/usr/bin/env python3
"""
Run open-parse (MIT, github.com/Filimoa/open-parse, PyPI `openparse`) in
BASE mode (no `[ml]` extra — that extra needs a Hugging Face weight
download for its table model, which is blocked in this sandbox) against a
benchmark PDF.

IMPORTANT DOCUMENTED WORKAROUND: open-parse's base pipeline calls
`tiktoken.get_encoding("cl100k_base")` purely to count tokens per node
(to decide if a node is a "stub"). tiktoken downloads that BPE file from
`openaipublic.blob.core.windows.net` on first use and has no offline
fallback. In a network-restricted/self-hosted deployment (exactly the
"What This IS" requirement for this use-case) that call fails outright and
open-parse.DocumentParser().parse() crashes with a ProxyError/OSError deep
inside `openparse/utils.py::num_tokens`. This is a genuine, undocumented
self-hosting limitation, not a benchmarking artifact — recorded in
observations.md. We patch `tiktoken.get_encoding` to fall back to a cheap
length-based token estimate ONLY so extraction can proceed for evaluation;
this does not change open-parse's actual document parsing, chunking, or
layout logic, only its internal "is this node too short to matter"
token-count heuristic.

Usage:
    source .venv_openparse/bin/activate
    python run_openparse.py <input.pdf> <tool_output_dir>
"""
import json
import sys
import time
from pathlib import Path

import tiktoken


class _OfflineFallbackEncoding:
    """Rough length-based token estimate, used because tiktoken's real
    cl100k_base BPE file (hosted at openaipublic.blob.core.windows.net)
    cannot be downloaded in this network-restricted sandbox. We do NOT
    attempt the real download first: tiktoken has no local cache of the
    failure, so a per-node try/except approach re-attempts (and re-fails,
    with urllib3 retry/backoff) the network call on every single node in
    the document - observed to turn an 18-page PDF into a multi-minute
    hang. Going straight to the offline estimate is both faster and a more
    honest reflection of what actually happens in an air-gapped/self-hosted
    deployment with no outbound internet at all."""

    def encode(self, text: str, **kwargs):
        return list(range(max(1, len(text) // 4)))


def _get_encoding_offline_only(name):
    return _OfflineFallbackEncoding()


tiktoken.get_encoding = _get_encoding_offline_only  # must patch before importing openparse's first use

import openparse  # noqa: E402


def node_to_markdown(node) -> str:
    text = getattr(node, "text", "") or ""
    variant = getattr(node, "variant", None)
    variant_name = str(variant) if variant else ""
    if "table" in variant_name.lower():
        return text  # openparse tables are emitted as pre-formatted text/markdown already
    return text


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: run_openparse.py <input.pdf> <tool_output_dir>")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    stem = pdf_path.stem

    raw_dir = out_dir / "raw_output"
    md_dir = out_dir / "markdown_output"
    log_dir = out_dir / "logs"
    for d in (raw_dir, md_dir, log_dir):
        d.mkdir(parents=True, exist_ok=True)

    log_lines = [
        f"openparse version: {getattr(openparse, 'version', 'unknown')}",
        f"input: {pdf_path}",
        "config: base mode (no [ml] extra) - pdfminer.six backbone, no OCR, no ML table model",
        "workaround applied: tiktoken.get_encoding patched with offline length-based fallback "
        "(see module docstring) because openaipublic.blob.core.windows.net is blocked in this sandbox",
        f"started: {time.strftime('%Y-%m-%d %H:%M:%S')}",
    ]

    t0 = time.time()
    error = None
    doc = None
    try:
        parser = openparse.DocumentParser()
        doc = parser.parse(str(pdf_path), ocr=False)
    except Exception as exc:  # noqa: BLE001
        error = repr(exc)
    elapsed = time.time() - t0
    log_lines.append(f"elapsed_seconds: {elapsed:.2f}")

    if error:
        log_lines.append(f"ERROR: {error}")
        (log_dir / f"{stem}.log").write_text("\n".join(log_lines), encoding="utf-8")
        print(f"[open-parse] FAILED on {pdf_path.name}: {error}")
        sys.exit(2)

    nodes = doc.nodes
    md_parts = [node_to_markdown(n) for n in nodes]
    md_text = "\n\n".join(p for p in md_parts if p)
    (md_dir / f"{stem}.md").write_text(md_text, encoding="utf-8")

    node_records = []
    for i, n in enumerate(nodes):
        node_records.append(
            {
                "index": i,
                "variant": str(getattr(n, "variant", None)),
                "bbox": [b.__dict__ if hasattr(b, "__dict__") else str(b) for b in (getattr(n, "bbox", None) or [])],
                "text_preview": (getattr(n, "text", "") or "")[:200],
                "num_pages": getattr(n, "num_pages", None),
            }
        )

    raw_record = {
        "tool": "open-parse",
        "mode": "base (no [ml] extra)",
        "input_file": str(pdf_path),
        "elapsed_seconds": elapsed,
        "n_nodes": len(nodes),
        "content_char_count": len(md_text),
        "nodes": node_records,
    }
    (raw_dir / f"{stem}.json").write_text(json.dumps(raw_record, indent=2, default=str), encoding="utf-8")

    log_lines.append(f"n_nodes: {len(nodes)}")
    log_lines.append(f"content_char_count: {len(md_text)}")
    (log_dir / f"{stem}.log").write_text("\n".join(log_lines), encoding="utf-8")

    print(f"[open-parse] OK {pdf_path.name}: {elapsed:.1f}s, {len(nodes)} nodes, {len(md_text)} chars")


if __name__ == "__main__":
    main()
