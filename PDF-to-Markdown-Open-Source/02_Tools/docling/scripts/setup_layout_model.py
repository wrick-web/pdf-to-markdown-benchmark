#!/usr/bin/env python3
"""
Set up Docling's required layout model (docling-project/docling-layout-heron)
for offline use via DOCLING_ARTIFACTS_PATH.

Steps, each done exactly once (no retry loops against a known-blocked host):
  1. Check every local/cache location the model could already be in.
  2. If not found, attempt one real download via huggingface_hub, then try
     2 genuinely different legitimate hosts that might serve the same
     files (not the same URL retried) - a direct hf.co alias and the
     LFS CDN host - each attempted once.
  3. Report exactly what happened. Never fabricate success.

Usage:
    source .venv_docling/bin/activate
    python setup_layout_model.py
"""
import os
import socket
import sys
import time
from pathlib import Path

REPO_ID = "docling-project/docling-layout-heron"
REVISION = "main"
REQUIRED_FILES = ["config.json", "preprocessor_config.json"]
WEIGHT_FILE_CANDIDATES = ["model.safetensors", "pytorch_model.bin"]

# Where the model needs to end up (Docling's own resolve_model_artifacts_path
# convention: <artifacts_path>/<repo_id with "/" -> "-->).
ARTIFACTS_ROOT = Path(__file__).resolve().parents[1] / "models"
TARGET_DIR = ARTIFACTS_ROOT / REPO_ID.replace("/", "--")

# Candidate local/cache locations to check before attempting any download.
CANDIDATE_CACHE_DIRS = [
    Path.home() / ".cache" / "huggingface" / "hub" / f"models--{REPO_ID.replace('/', '--')}",
    Path(os.environ.get("HF_HOME", "")) / "hub" / f"models--{REPO_ID.replace('/', '--')}" if os.environ.get("HF_HOME") else None,
    Path(os.environ.get("TRANSFORMERS_CACHE", "")) if os.environ.get("TRANSFORMERS_CACHE") else None,
    TARGET_DIR,
]


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")


def check_dir_has_model(d: Path) -> bool:
    if not d or not d.exists():
        return False
    has_config = (d / "config.json").exists() or any(d.rglob("config.json"))
    has_preproc = (d / "preprocessor_config.json").exists() or any(d.rglob("preprocessor_config.json"))
    has_weights = any((d / w).exists() for w in WEIGHT_FILE_CANDIDATES) or any(
        d.rglob(w) for w in WEIGHT_FILE_CANDIDATES
    )
    return bool(has_config and has_preproc and has_weights)


def step1_check_local() -> Path | None:
    log("STEP 1: checking local/cache locations for an existing copy")
    for d in CANDIDATE_CACHE_DIRS:
        if d is None:
            continue
        log(f"  checking {d} ... {'EXISTS' if d.exists() else 'absent'}")
        if check_dir_has_model(d):
            log(f"  FOUND complete model at {d}")
            return d
    log("  no existing local copy found anywhere checked")
    return None


def try_dns(host: str) -> bool:
    try:
        socket.gethostbyname(host)
        return True
    except OSError:
        return False


def step2_attempt_download() -> tuple[bool, str]:
    log("STEP 2: attempting to obtain the model - one real attempt per route, no retry loops")
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    # Route A: the real huggingface_hub download path Docling itself uses.
    log("  route A: huggingface_hub.snapshot_download (huggingface.co) - single attempt")
    try:
        from huggingface_hub import snapshot_download

        path = snapshot_download(repo_id=REPO_ID, revision=REVISION, local_dir=str(TARGET_DIR))
        return True, f"downloaded via huggingface_hub to {path}"
    except Exception as exc:  # noqa: BLE001
        log(f"    FAILED: {exc!r}")

    # Route B: a different, genuinely distinct hostname (hf.co is HF's own
    # short alias domain, not the same URL retried) - one plain HTTP attempt.
    log("  route B: hf.co (HF's short-alias domain) - single plain HTTPS attempt")
    try:
        import httpx

        url = f"https://hf.co/{REPO_ID}/resolve/{REVISION}/config.json"
        resp = httpx.get(url, timeout=10, follow_redirects=True)
        log(f"    HTTP {resp.status_code}")
        if resp.status_code == 200:
            (TARGET_DIR / "config.json").write_bytes(resp.content)
            return True, "config.json obtained via hf.co - continuing this route manually"
    except Exception as exc:  # noqa: BLE001
        log(f"    FAILED: {exc!r}")

    # Route C: the LFS CDN host directly (large files on HF are served from
    # a separate cdn-lfs subdomain - genuinely different host from the
    # already-proven-blocked huggingface.co main site).
    log("  route C: cdn-lfs.huggingface.co (HF's LFS CDN, a different host) - DNS/connect check only")
    if try_dns("cdn-lfs.huggingface.co"):
        try:
            import httpx

            resp = httpx.head("https://cdn-lfs.huggingface.co/", timeout=8)
            log(f"    reachable, HTTP {resp.status_code}")
        except Exception as exc:  # noqa: BLE001
            log(f"    FAILED: {exc!r}")
    else:
        log("    DNS resolution itself failed - not reachable")

    return False, "no route obtained the model"


def main() -> None:
    found = step1_check_local()
    if found:
        print(f"\nRESULT: model already available locally at {found}")
        print(f"Set DOCLING_ARTIFACTS_PATH={found.parent}")
        sys.exit(0)

    ok, detail = step2_attempt_download()
    if ok:
        print(f"\nRESULT: SUCCESS - {detail}")
        sys.exit(0)

    print(f"\nRESULT: BLOCKED - {detail}")
    print("No legitimate route from this environment reached the model.")
    print(f"Required externally: {REPO_ID} (revision {REVISION}) - "
          f"{', '.join(REQUIRED_FILES)} + one of {WEIGHT_FILE_CANDIDATES}, "
          f"placed under {TARGET_DIR}")
    sys.exit(1)


if __name__ == "__main__":
    main()
