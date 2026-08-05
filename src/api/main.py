from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import time, json

requests_total = Counter('wormai_requests_total', 'Total requests')
inference_latency_seconds = Counter('wormai_inference_latency_seconds', 'Total inference latency seconds')

app = FastAPI(title='worm-ai API')

API_KEY = 'REPLACE_WITH_REAL_KEY'

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

    # Placeholder streaming SSE response
    async def gen():
        yield 'data: {"status":"starting"}\n\n'
        await request.body()
        time.sleep(0.1)
        yield 'data: {"partial":"hello"}\n\n'
        yield 'data: {"result":"final placeholder"}\n\n'

    latency = time.time() - start
    inference_latency_seconds.inc(latency)
    return StreamingResponse(gen(), media_type='text/event-stream')
