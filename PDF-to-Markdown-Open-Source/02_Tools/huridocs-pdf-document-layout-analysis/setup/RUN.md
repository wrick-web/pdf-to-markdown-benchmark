# huridocs/pdf-document-layout-analysis — Run commands (for a machine with Docker)

```bash
docker pull huridocs/pdf-document-layout-analysis:v0.0.31

# CPU profile
docker run -p 5060:5060 -d --rm --name huridocs-layout \
  huridocs/pdf-document-layout-analysis:v0.0.31

# Per benchmark PDF:
curl -X POST -F 'file=@01_Benchmark_PDFs/PDF1_Hybrid_Earnings_Report_Target2015.pdf' \
     http://localhost:5060/ -o 02_Tools/huridocs-pdf-document-layout-analysis/raw_output/PDF1.json

curl -X POST -F 'file=@01_Benchmark_PDFs/PDF2_Financial_Report_Sumitomo.pdf' \
     http://localhost:5060/ -o 02_Tools/huridocs-pdf-document-layout-analysis/raw_output/PDF2.json

curl -X POST -F 'file=@01_Benchmark_PDFs/PDF3_Scanned_Research_Paper.pdf' \
     http://localhost:5060/ -o 02_Tools/huridocs-pdf-document-layout-analysis/raw_output/PDF3.json

docker stop huridocs-layout
```

Confirm the exact endpoint path/params/Markdown-export flag against the
README of the tag you pull — this project could not exercise the live
service to verify firsthand (no Docker daemon in the research sandbox).
GPU compose profile and LightGBM-vs-VGT model selection are documented in
the repo's `docker-compose.yml` / README.
