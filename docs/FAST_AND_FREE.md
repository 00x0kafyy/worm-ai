Fast & Free guide

Goal: run worm-ai with zero paid services while maximizing throughput/low latency on typical CPUs.

Principles
- Use small open-source models (all free) and quantize them.
- Run locally or on any VM (no managed paid DBs/services).
- Use local FAISS for vector search and ONNXRuntime/OpenVINO for fast inference.
- Cache and batch requests to reduce repeat compute.

Recommended stack (free):
- Models: sentence-transformers/all-MiniLM-L6-v2 (embeddings), google/flan-t5-small (generation), or tiny OPT/Distil models for cheap responses.
- Embeddings runtime: sentence-transformers (PyTorch) + onnxruntime for exported models.
- Vector DB: faiss-cpu (local, persistent index file).
- Model export & accel: ONNX export + onnxruntime (CPU optimized), or OpenVINO. For LLMs on CPU, use ggml builds + llama.cpp for GGML models.
- Registry/storage: local filesystem or DVC with local remote; MLflow can run locally without paid services.

Quick recipes
1) Environment (minimal):
   bash scripts/setup_fast_env.sh

2) Use small embedding model + FAISS:
   - Run a script to embed docs using sentence-transformers, build a FAISS index, and save it to disk.
   - Query by embedding and return top-k quickly from disk-backed index.

3) Quantize and run ONNX model:
   - Export model to ONNX, then run onnxruntime with optimization level ALL and/or apply dynamic quantization.

4) Caching & batching:
   - Enable the API LRU cache for repeated queries and group short-window requests into batches.

Operations & costs
- All components above can run on a single CPU machine. Costs = compute + storage on your host (no vendor lock-in).

Notes and tradeoffs
- Free + fast favors smaller models and precomputation (indexes, caches). Expect lower generative quality vs large paid models but excellent latency and zero ongoing costs.

