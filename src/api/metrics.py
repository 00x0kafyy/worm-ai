from prometheus_client import Counter, Histogram

REQUESTS = Counter('wormai_requests_total', 'Total requests')
INFERENCE_LATENCY = Histogram('wormai_inference_latency_seconds', 'Inference latency')
