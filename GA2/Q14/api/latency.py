"""
Serverless FastAPI function for Vercel: POST /api/latency
"""
import json
from pathlib import Path
from typing import List

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
)


class LatencyRequest(BaseModel):
    regions: List[str]
    threshold_ms: int


def load_telemetry() -> list[dict]:
    data_path = Path(__file__).parent.parent / "q-vercel-latency.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_metrics(records: list[dict], threshold_ms: int) -> dict:
    if not records:
        return {"avg_latency": 0, "p95_latency": 0, "avg_uptime": 0, "breaches": 0}

    latencies = sorted(r.get("latency_ms", 0) for r in records)
    uptimes = [r.get("uptime", 0) for r in records]
    breaches = sum(1 for r in records if r.get("latency_ms", 0) > threshold_ms)
    avg_latency = sum(latencies) / len(latencies)
    # 95th percentile (nearest-rank)
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
