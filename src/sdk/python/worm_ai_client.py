import requests

class WormAIClient:
    def __init__(self, url: str):
        self.url = url.rstrip('/')

    def predict(self, payload: dict):
        resp = requests.post(f"{self.url}/predict", json=payload, stream=True)
        return resp.iter_lines()
