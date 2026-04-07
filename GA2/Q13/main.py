from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv
from pathlib import Path
from typing import List, Dict, Optional
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow GET from any origin
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Default CSV path can be overridden via the CSV_PATH environment variable.
CSV_PATH = Path(os.environ.get("CSV_PATH", Path(__file__).parent / "students.csv"))


def load_students() -> List[Dict[str, str]]:
    students: List[Dict[str, str]] = []
    if not CSV_PATH.exists():
        return students
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                sid = int(row.get("studentId", 0))
            except Exception:
                sid = 0
            students.append({"studentId": sid, "class": row.get("class", "")})
    return students


@app.get("/api")
@app.get("/api/")
def get_students(class_: Optional[List[str]] = Query(default=None, alias="class")):
    data = load_students()
    if class_:
        class_set = set(class_)
        data = [s for s in data if s["class"] in class_set]
    return {"students": data}


@app.get("/")
def root():
    return {"message": "FastAPI student service. Use /api or /api?class=1A&class=1B"}


if __name__ == "__main__":
    import uvicorn

    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("main:app", host=host, port=port, reload=False)
