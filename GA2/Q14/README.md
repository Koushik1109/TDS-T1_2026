# eShopCo Latency Monitoring API

Serverless FastAPI endpoint for monitoring deployment latency from storefront telemetry pings.

## Endpoint

**POST** `/api/latency`

### Request Body

```json
{
  "regions": ["amer", "apac"],
  "threshold_ms": 176
}
```

### Response (per region)

- `avg_latency` – mean latency (ms)
- `p95_latency` – 95th percentile latency (ms)
- `avg_uptime` – mean uptime (0–1)
- `breaches` – count of records above threshold

## Deploy to Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Use the generated URL, e.g. `https://your-project.vercel.app/api/latency`

## Note on Telemetry File

If your course provides an official `q-vercel-latency.json` with a different structure, replace the project’s copy. Expected record format:

```json
{"region": "amer", "latency_ms": 145, "uptime": 0.98}
```
