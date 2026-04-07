from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

csv_content = """id,name,value,category
1,Alice,10.5,A
2,Bob,20.0,B
3,Carol,5.25,A
4,Dan,100.11,C
"""

files = {"file": ("q-fastapi-file-validation.csv", csv_content, "text/csv")}
headers = {"X-Upload-Token-8513": "t5rdgy8333d1very"}

resp = client.post("/upload", headers=headers, files=files)
print("Status:", resp.status_code)
try:
    print(resp.json())
except Exception:
    print(resp.text)
