"""Placeholder script to export a HuggingFace model to ONNX or write a placeholder file if transformers missing."""
import os

OUT_ONNX = 'models/model.onnx'

try:
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    from transformers.onnx import export
    HAS_TRANSFORMERS = True
except Exception:
    HAS_TRANSFORMERS = False

if __name__ == '__main__':
    os.makedirs('models', exist_ok=True)
    if not HAS_TRANSFORMERS:
        with open(OUT_ONNX, 'wb') as f:
            f.write(b'ONNX_PLACEHOLDER')
        print('Transformers not available; wrote placeholder ONNX file to', OUT_ONNX)
    else:
        print('Transformers available - ONNX export not implemented in this stub script')
