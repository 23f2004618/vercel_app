# api/latency.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import json
import os

app = FastAPI()

# Enable CORS for all origins

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["POST"],
allow_headers=["*"],
)

# Load telemetry data once at startup

with open(os.path.join(os.path.dirname(**file**), "telemetry.json"), "r") as f:
telemetry = json.load(f)

@app.post("/api/latency")
async def latency_metrics(req: Request):
body = await req.json()
regions = body.get("regions", [])
threshold = body.get("threshold_ms", 9999)

```
results = {}
for region in regions:
    data = telemetry.get(region, [])
    if not data:
        continue

    latencies = np.array([d["latency_ms"] for d in data])
    uptimes = np.array([d["uptime"] for d in data])

    avg_latency = float(np.mean(latencies))
    p95_latency = float(np.percentile(latencies, 95))
    avg_uptime = float(np.mean(uptimes))
    breaches = int(np.sum(latencies > threshold))

    results[region] = {
        "avg_latency": avg_latency,
        "p95_latency": p95_latency,
        "avg_uptime": avg_uptime,
        "breaches": breaches,
    }

return results
```
