from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI(title='worm-ai API')

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/predict')
def predict():
    # Placeholder streaming response
    def gen():
        yield 'data: starting\n\n'
        yield 'data: result placeholder\n\n'
    return StreamingResponse(gen(), media_type='text/event-stream')
