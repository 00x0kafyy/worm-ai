
Quick usage
-----------
- Install minimal free stack: scripts/setup_fast_env.sh
- Build a FAISS index (examples fallback): python scripts/build_faiss_index.py
- Run API: uvicorn src.api.main:app --host 0.0.0.0 --port 8000
- Export ONNX placeholder: python scripts/export_onnx.py
