# huridocs/pdf-document-layout-analysis — Observations

Repo: https://github.com/huridocs/pdf-document-layout-analysis · Apache-2.0.
**Status: prepared-not-run** — blocked at the infrastructure layer (no Docker daemon in this sandbox), not attempted against any benchmark PDF.

## Setup

Installation method: **Docker only** — the project ships as a Docker image (`huridocs/pdf-document-layout-analysis:v0.0.31` and later tags), with CPU and GPU `docker-compose` profiles. There is no plain `pip install` path for the full service (it's a FastAPI microservice with bundled models, not a standalone Python package).

**Blocker found:** this sandbox has the `docker` CLI installed but no daemon:
```
$ docker ps
failed to connect to the docker API at unix:///var/run/docker.sock:
check if the path is correct and if the daemon is running:
dial unix /var/run/docker.sock: connect: no such file or directory
```
No amount of network access fixes this — Docker-based tools cannot be started in this container at all. This is an infrastructure-layer blocker, independent of the Hugging Face/network blockers that stopped PaddleOCR-VL.

## Why it's still a strong Tier A candidate

Distinctive design: a dual-model layout+OCR pipeline with a genuine **classical, CPU-only path** — `VGT` (Vision Grid Transformer) for GPU, or `LightGBM` (a classical gradient-boosted ensemble of token classifiers, not a neural network) for CPU-only deployments, reported at ~0.42s/page on CPU vs ~13.5s/page for the GPU-preferred VGT model run on CPU. Table structure via RapidTable (HTML tables), formula recognition via LaTeX-OCR, OCR via Tesseract (150+ languages), reading order via Poppler with a header-first/footer-last heuristic. Outputs Markdown, HTML, and JSON. This LightGBM path is one of the very few genuinely non-neural, CPU-first options found in this cycle's entire research pass — worth prioritizing on a machine that has Docker.

## Reproducing this on a machine with Docker

```bash
docker pull huridocs/pdf-document-layout-analysis:v0.0.31
# CPU-only:
docker run -p 5060:5060 -d --rm huridocs/pdf-document-layout-analysis:v0.0.31
# then, per PDF:
curl -X POST -F 'file=@/path/to/PDF1_Hybrid_Earnings_Report_Target2015.pdf' \
     http://localhost:5060/ -o result.json
# Markdown/HTML export endpoints and the LightGBM-vs-VGT model selection
# flag are documented at the repo's README/docs — confirm exact endpoint
# names against the version you pull, since this project could not
# exercise the live API here to confirm request/response shapes firsthand.
```

A ready-to-run copy of this exact command sequence is in
`02_Tools/huridocs-pdf-document-layout-analysis/setup/RUN.md`.

## Evidence
- `logs/docker_daemon_check.log` — the `docker ps` failure captured verbatim.
