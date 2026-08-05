from src.data.synthetic import generate_synthetic
from src.data.active_learning import ActiveLearner
from src.rag.faiss_store import FaissStore
import json, tempfile

def test_synthetic():
    syn = generate_synthetic(['hello'], n=2)
    assert len(syn) == 2

def test_active_learning(tmp_path):
    pool = [{'id': str(i), 'text': f'text {i}'} for i in range(5)]
    p = tmp_path / 'pool.json'
    p.write_text(json.dumps(pool))
    al = ActiveLearner(str(p))
    c = al.select_candidates(3)
    assert len(c) == 3
    labeled = c[:2]
    al.mark_labeled(labeled)
    remaining = json.loads(p.read_text())
    assert len(remaining) == 3

def test_faiss_store():
    store = FaissStore()
    ids = ['a','b']
    vecs = [[0.0,0.0],[1.0,1.0]]
    docs = [{'id':'a','text':'zero'},{'id':'b','text':'one'}]
    store.upsert(ids, vecs, docs)
    res = store.query([0.1,0.1], k=1)
    assert len(res) == 1
