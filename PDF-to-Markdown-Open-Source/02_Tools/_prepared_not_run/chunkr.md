# Chunkr (lumina-ai-inc)

- Repo: https://github.com/lumina-ai-inc/chunkr
- **License: AGPL-3.0** (confirmed via raw `LICENSE`) — a materially
  different, copyleft/network-use license class from every other tool on
  this list. A paid commercial-license alternative is offered by the
  vendor. **Review this explicitly before using Chunkr in anything that
  might be redistributed or offered as a service.**
- v2.2.1 (July 2025) — changelog notes replacing VGT with a YOLO-based
  model "more practical for consumer hardware"

## Why it's compelling
Rust core; genuine CPU and Mac-ARM `docker-compose` profiles alongside the
GPU one (unusual breadth of hardware support for a Docker-only tool).
Converts PDF/DOCX/PPTX/XLSX/images into "Structured HTML & Markdown." The
open-source edition uses unnamed "community/open-source models" (vs.
proprietary models in the paid Cloud/Enterprise tiers) — exactly which
models these are was not confirmed from available docs.

## Requirements
- Docker Compose (no plain pip path) — this sandbox has no Docker daemon
- Heavier ops footprint than a pip package: multi-service stack (worker +
  API + storage), not a single binary/library call

## Reproduce on a machine with Docker
```bash
git clone https://github.com/lumina-ai-inc/chunkr.git
cd chunkr
docker compose -f docker-compose.cpu.yaml up -d   # or the Mac-ARM / GPU compose file
curl -X POST -F 'file=@path/to/file.pdf' http://localhost:8000/api/v1/task -o result.json
```

## Blocked here because
No Docker daemon in this sandbox. Independent of the network-egress
blockers that stopped the Hugging-Face-dependent tools above.
