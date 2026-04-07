"""
Latency monitoring endpoint for eShopCo storefront telemetry.
"""
import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


class LatencyRequest(BaseModel):
    regions: list[str]
    threshold_ms: int


def load_telemetry() -> list[dict]:
    data_path = Path(__file__).parent / "q-vercel-latency.json"
    with open(data_path) as f:
        return json.load(f)


def compute_metrics(records: list[dict], threshold_ms: int) -> dict:
    if not records:
        return {"avg_latency": 0, "p95_latency": 0, "avg_uptime": 0, "breaches": 0}

    latencies = sorted(r["latency_ms"] for r in records)
    uptimes = [r["uptime"] for r in records]
    breaches = sum(1 for r in records if r["latency_ms"] > threshold_ms)
    avg_latency = sum(latencies) / len(latencies)
    p95_idx = min(int(0.95 * len(latencies)), len(latencies) - 1)
    p95_latency = latencies[p95_idx]
    avg_uptime = sum(uptimes) / len(uptimes)

    return {
        "avg_latency": round(avg_latency, 2),
        "p95_latency": round(p95_latency, 2),
        "avg_uptime": round(avg_uptime, 4),
        "breaches": breaches,
    }


@app.post("/api/latency")
async def latency_metrics(request: LatencyRequest):
    telemetry = load_telemetry()
    regions = {}
    for region in request.regions:
        region_records = [r for r in telemetry if r.get("region") == region]
        regions[region] = compute_metrics(region_records, request.threshold_ms)
    return {"regions": regions}
