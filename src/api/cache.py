"""Simple LRU cache for API responses to avoid recomputing identical requests."""
from functools import lru_cache
import json

@lru_cache(maxsize=1024)
def cached_predict_key(payload_json: str):
    # payload_json must be a stable JSON string
    # In real use, include auth scope and model version in the key
    return payload_json

def cache_key_from_payload(payload: dict):
    # Stable deterministic json dump to use as cache key
    return json.dumps(payload, sort_keys=True, separators=(',', ':'))
