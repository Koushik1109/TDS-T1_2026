import requests

URL = "http://localhost:8000/upload"
headers = {
    "Origin": "http://example.com",
    "Access-Control-Request-Method": "POST",
}

resp = requests.options(URL, headers=headers)
print("Status:", resp.status_code)
print("Access-Control-Allow-Origin:", resp.headers.get("Access-Control-Allow-Origin"))
print("Access-Control-Allow-Methods:", resp.headers.get("Access-Control-Allow-Methods"))
print("Access-Control-Allow-Headers:", resp.headers.get("Access-Control-Allow-Headers"))
