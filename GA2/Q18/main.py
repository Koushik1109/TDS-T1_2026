from fastapi import FastAPI, UploadFile, File, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import csv
from collections import Counter
from decimal import Decimal, InvalidOperation

app = FastAPI()

# Allow POST from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

EXPECTED_TOKEN = "t5rdgy8333d1very"
MAX_BYTES = 76 * 1024  # 76 KB
ALLOWED_EXTS = {".csv", ".json", ".txt"}


def _get_ext(filename: str) -> str:
    filename = filename or ""
    if "." in filename:
        return filename[filename.rfind("."):].lower()
    return ""


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    x_upload_token_8513: str | None = Header(None, convert_underscores=False, alias="X-Upload-Token-8513"),
):
    # Auth
    if x_upload_token_8513 != EXPECTED_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    # File type
    ext = _get_ext(file.filename)
    if ext not in ALLOWED_EXTS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file type")

    # Read bytes and check size
    content = await file.read()
    if len(content) > MAX_BYTES:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Payload too large")

    # If CSV, parse and compute stats
    if ext == ".csv":
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to decode CSV as UTF-8")

        rows = 0
        total_value = Decimal("0")
        category_counter = Counter()
        reader = csv.DictReader(text.splitlines())
        columns = reader.fieldnames or []

        for row in reader:
            rows += 1
            # sum 'value' column if present
            v = row.get("value")
            if v not in (None, ""):
                try:
                    total_value += Decimal(v)
                except (InvalidOperation, ValueError):
                    pass
            # count category
            cat = row.get("category")
            if cat not in (None, ""):
                category_counter[cat] += 1

        response = {
            "email": "24ds3000006@ds.study.iitm.ac.in",
            "filename": file.filename,
            "rows": rows,
            "columns": columns,
            "totalValue": float(round(total_value, 2)),
            "categoryCounts": dict(category_counter),
        }
        return response

    # For allowed non-CSV types, respond with basic metadata
    return {"filename": file.filename, "message": "File accepted (no CSV analysis for this type)"}
