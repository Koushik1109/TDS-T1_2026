import requests

URL = "http://localhost:8000/upload"
HEADERS = {"X-Upload-Token-8513": "t5rdgy8333d1very"}

with open("q-fastapi-file-validation.csv", "rb") as f:
    files = {"file": ("q-fastapi-file-validation.csv", f, "text/csv")}
    resp = requests.post(URL, headers=HEADERS, files=files)
    print(resp.status_code)
    try:
        print(resp.json())
    except Exception:
        print(resp.text)
