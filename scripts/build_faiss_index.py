"""Build a FAISS index from example documents and save it to disk (models/faiss_index.pkl)."""
import os, json, pickle

try:
    from src.embeddings.embeddings import embed_texts
    from src.rag.faiss_store import FaissStore
except Exception as e:
    print('Local imports failed:', e)
    raise

DOCS_FILE = 'examples/documents.json'
OUT_INDEX = 'models/faiss_index.pkl'

if __name__ == '__main__':
    if not os.path.exists(DOCS_FILE):
        # create sample docs
        docs = [{'id': str(i), 'text': f'Sample document {i} content about worms and AI.'} for i in range(20)]
        os.makedirs(os.path.dirname(DOCS_FILE) or '.', exist_ok=True)
        with open(DOCS_FILE, 'w') as f:
            json.dump(docs, f)
    else:
        with open(DOCS_FILE) as f:
            docs = json.load(f)

    texts = [d['text'] for d in docs]
    emb = embed_texts(texts)

    ids = [d['id'] for d in docs]
    store = FaissStore()
    store.upsert(ids, emb.tolist(), docs)

    with open(OUT_INDEX, 'wb') as f:
        pickle.dump(store, f)

    print('Built FAISS index with', len(ids), 'documents ->', OUT_INDEX)
