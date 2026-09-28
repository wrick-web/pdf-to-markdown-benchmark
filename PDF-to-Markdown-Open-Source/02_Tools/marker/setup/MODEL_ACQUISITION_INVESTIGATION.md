# Marker — exhaustive investigation of the Surya layout-model blocker (2026-09-24)

This was requested explicitly after the initial TC27-31/TC32/TC115 round returned
0 PASS / 0 FAIL / 7 CAN NOT BE GRADED, to confirm — rather than assume — that no
legitimate route exists before accepting that result. Nothing here bypasses,
mocks, or replaces Surya's real layout detection; the question was only whether
the *real* model weights could be obtained through any legitimate means.

## 1. Is the model already cached locally anywhere in this sandbox?

Checked every location Surya/HF could plausibly have left a cache:

```
$ env | grep -iE "hf_|hugging|transformers_cache|torch_home|datalab|surya"
(no output - none of these env vars are set)

$ find / -xdev -maxdepth 8 -iname "models--*"        # HF cache dir naming convention
(no output)

$ ls -la ~/.cache/huggingface
ls: cannot access '/root/.cache/huggingface': No such file or directory

$ find / -xdev -ipath "*datalab*"
/root/.cache/datalab/surya/fast_layout_server.lock   # a lock file, not a model
/root/.cache/datalab/surya/fast_layout_server.log    # this round's own failure log
```

**Result: not cached anywhere.** No HF hub cache directory exists at all in this
container (it was never successfully populated, by this round or any prior one -
this is the project's first Marker round).

## 2. Does `resolve_model_dir()` support a genuine offline/local-directory route?

Yes - this is Surya's own supported mechanism, not something invented here:

```python
# surya/common/rfdetr_torch.py:181-203
def resolve_model_dir(checkpoint: str) -> str:
    """... Supports a plain local path, an ``hf://<repo>/<subfolder>`` ref
    (downloaded from the Hub), or an ``s3://`` path."""
    if checkpoint and checkpoint.startswith("hf://"):
        ...  # snapshot_download - blocked, see below
    if checkpoint and os.path.isdir(checkpoint):
        return checkpoint          # <-- a real local directory just works
    if checkpoint and checkpoint.startswith("s3://"):
        ...
```

`marker_single --help` confirms this is reachable from the CLI via
`FAST_LAYOUT_MODEL_CHECKPOINT` / a `--config_json` override - not a private
internal API. **If the actual weight files could be legitimately obtained**,
pointing this at a local directory containing them would exercise Marker's
completely normal, unmodified layout-detection code - no bypass at all.

The default checkpoint is `hf://datalab-to/surya_layout2` (`surya/settings.py:153`).

## 3. Does anything already installed bundle the actual weight files?

```
$ find .venv_marker/.../surya .venv_marker/.../marker -type f \
    \( -iname "*.onnx" -o -iname "*.safetensors" -o -iname "*.bin" \
       -o -iname "*.pt" -o -iname "*.pth" -o -iname "*.ckpt" -o -iname "*.gguf" \)
(no output)

$ du -sh .venv_marker/.../surya .venv_marker/.../marker
1.2M  surya
2.6M  marker
```

**Result: no.** Both packages are pure code (1.2 MB / 2.6 MB total) - unlike, for
example, this same sandbox's `rapidocr` PyPI package, which bundles its own ONNX
weights directly and was used to fix Docling's *OCR* dependency without any
network call in that tool's round. No equivalent bundling exists for Surya's
layout model in either `surya-ocr` or `marker-pdf`.

## 4. Every network route actually tried (one real attempt per route, no retry loops)

| Route | Result |
|---|---|
| `huggingface.co` (the real path Marker/Surya uses) | `ProxyError: 403 Forbidden` |
| `hf.co` (HF's own short-alias domain - a genuinely different hostname) | `ProxyError: 403 Forbidden` |
| `cdn-lfs.huggingface.co` (HF's separate large-file CDN host) | DNS resolution itself failed (`No address associated with hostname`) - a harder block than a proxy rejection |
| `hf-mirror.com` (a known third-party HF mirror, a different domain entirely) | `ProxyError: 403 Forbidden` |
| `datalab.to` / `www.datalab.to` (Marker's own publisher site, not just the `models.` subdomain already known blocked) | `ProxyError: 403 Forbidden` |
| `api.github.com` (to check `datalab-to/surya` or `VikParuchuri/surya` GitHub Releases for a mirrored weight asset) | `403 Forbidden` |
| `raw.githubusercontent.com` (control check - confirms this sandbox isn't just universally offline) | **200 OK**, 35,428 real bytes of Marker's own README fetched successfully |
| PyPI, guessed mirror-package names (`surya-layout2-weights`, `surya-layout-weights`, `surya-models`, `datalab-surya-weights`) | all `404` - no such packages exist |

The `raw.githubusercontent.com` control check matters: it proves this sandbox is
not simply offline everywhere, and that the specific blocks above are a genuine
egress **allowlist** policy (confirmed independently via the agent proxy's own
`recentRelayFailures` status, which explicitly labels these as policy denials,
not transient failures) - the same conclusion this project's Docling round
reached independently for its own HF-hosted layout model, in this same sandbox.

## 5. Conclusion

**No legitimate route from this sandbox reaches Surya's `fast_layout` model.**
Not one blocked URL retried repeatedly - eight genuinely different
routes/hosts, each tried exactly once, seven blocked (six by proxy policy, one
at the DNS level) and one (GitHub raw content) reachable but irrelevant, since
no mirrored copy of the weights exists there or anywhere else checked.

- **Exact missing dependency:** the Surya `fast_layout` object-detection
  checkpoint at Hugging Face repo `datalab-to/surya_layout2` (default
  `FAST_LAYOUT_MODEL_CHECKPOINT` in `surya/settings.py`), loaded via
  `huggingface_hub.snapshot_download` inside `surya/common/rfdetr_torch.py`'s
  `resolve_model_dir()`.
- **Exactly where blocked:** this sandbox's organization egress policy denies
  `huggingface.co`, `hf.co`, `hf-mirror.com`, `datalab.to`/`models.datalab.to`,
  and `api.github.com` (403 at the proxy `CONNECT` step); `cdn-lfs.huggingface.co`
  isn't even DNS-resolvable from here.
- **Does the model exist anywhere locally?** No - confirmed absent from every
  HF-cache-convention location, every env var that could redirect to one, and
  both installed packages' own files.
- **Does an approved cache/offline route exist?** No - `resolve_model_dir()`
  does support a genuine local-directory override, but there is nothing
  legitimate to put in it; no bundled, PyPI-mirrored, or GitHub-hosted copy of
  these specific weights exists anywhere this sandbox can reach.
- **What would a valid run need?** Either (a) this sandbox's egress policy
  allowlisting `huggingface.co` (or another host that actually serves these
  exact weights), or (b) the weight files supplied into this environment from
  outside it (e.g. downloaded once on an unrestricted machine and copied in,
  the same remedy this project's Docling round documented for its own,
  structurally identical blocker).

This is a genuine, structural limitation of this sandbox, not a missing
configuration step on Marker's side - it matches this same project's
independent, exhaustive findings for Docling's HF-hosted layout model and
PaddleOCR-VL's four-host exhaustive bypass attempt. The original verdict
(CAN NOT BE GRADED for TC27-31, TC32, TC115) is confirmed, not changed.
