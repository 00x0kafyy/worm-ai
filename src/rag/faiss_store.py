"""FAISS-compatible vector store with in-memory fallback."""
import numpy as np

class FaissStoreFallback:
    def __init__(self):
        self.vectors = []
        self.docs = []

    def upsert(self, ids, vectors, docs):
        for i,v,d in zip(ids, vectors, docs):
            self.vectors.append(np.array(v))
            self.docs.append({'id': i, 'doc': d})

    def query(self, vector, k=5):
        if len(self.vectors) == 0:
            return []
        vec = np.array(vector)
        dists = [np.linalg.norm(vec - v) for v in self.vectors]
        idx = np.argsort(dists)[:k]
        return [self.docs[i] for i in idx]

# Try to import faiss and provide a wrapper if available
try:
    import faiss
    class FaissStore:
        def __init__(self, dim:int=768):
            self.dim = dim
            self.index = faiss.IndexFlatL2(dim)
            self.ids = []
            self.docs = []

        def upsert(self, ids, vectors, docs):
            arr = np.array(vectors).astype('float32')
            self.index.add(arr)
            self.ids.extend(ids)
            self.docs.extend(docs)

        def query(self, vector, k=5):
            arr = np.array([vector]).astype('float32')
            D, I = self.index.search(arr, k)
            results = []
            for i in I[0]:
                if i < len(self.docs):
                    results.append(self.docs[i])
            return results
except Exception:
    FaissStore = FaissStoreFallback

__all__ = ['FaissStore', 'FaissStoreFallback']
