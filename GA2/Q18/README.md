# FastAPI File Validation Service

Simple FastAPI app that validates uploaded files and analyzes CSVs.

Endpoint
- POST `/upload` — accepts multipart form field `file`.
- Requires header `X-Upload-Token-8513: t5rdgy8333d1very`.

Validation rules
- Allowed extensions: `.csv`, `.json`, `.txt`
- Max file size: 76 KB
- Returns `401` for missing/invalid token, `400` for unsupported file types, `413` for oversized payload.

CSV analysis
- Returns JSON with `email`, `filename`, `rows`, `columns`, `totalValue`, and `categoryCounts`.

Run locally (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Test upload (PowerShell)
```powershell
Invoke-RestMethod -Uri http://localhost:8000/upload -Method Post -Headers @{ 'X-Upload-Token-8513'='t5rdgy8333d1very' } -Form @{ file = Get-Item q-fastapi-file-validation.csv }
```

Files
- `main.py` — FastAPI app
- `q-fastapi-file-validation.csv` — sample CSV
- `post_real.py` — test uploader
