from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import time, json
from src.api.cache import cache_key_from_payload
from functools import lru_cache

requests_total = Counter('wormai_requests_total', 'Total requests')
inference_latency_seconds = Counter('wormai_inference_latency_seconds', 'Total inference latency seconds')

app = FastAPI(title='worm-ai API')

API_KEY = 'REPLACE_WITH_REAL_KEY'

@lru_cache(maxsize=1024)
def _cached_predict(payload_json: str):
    # Placeholder model compute - replace with actual inference call
    # Keep results JSON-serializable
    return {'result': f'computed for {payload_json[:200]}'}

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.get('/metrics')
def metrics():
    return JSONResponse(content=generate_latest().decode('utf-8'), media_type=CONTENT_TYPE_LATEST)

@app.post('/predict')
async def predict(request: Request):
    # Simple auth placeholder
    api_key = request.headers.get('x-api-key')
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail='Unauthorized')

    requests_total.inc()
    start = time.time()

    payload = await request.json()
    key = cache_key_from_payload(payload)

    # Use LRU cache for fast repeated queries
    result = _cached_predict(key)

    latency = time.time() - start
    inference_latency_seconds.inc(latency)
    return JSONResponse(content=result)
