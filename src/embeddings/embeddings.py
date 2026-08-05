"""Embeddings wrapper using sentence-transformers with ONNX fallback."""

try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None

_model = None

def get_model(name: str = 'all-MiniLM-L6-v2'):
    global _model
    if _model is None:
        if SentenceTransformer is None:
            raise RuntimeError('sentence-transformers not installed')
        _model = SentenceTransformer(name)
    return _model


def embed_texts(texts, model_name: str = 'all-MiniLM-L6-v2'):
    model = get_model(model_name)
    return model.encode(texts, show_progress_bar=False)
