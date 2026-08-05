"""Active learning scaffold: select uncertain samples and manage labeling loop."""
import json, random

class ActiveLearner:
    def __init__(self, unlabeled_pool_path: str):
        self.pool_path = unlabeled_pool_path
        try:
            with open(self.pool_path) as f:
                self.pool = json.load(f)
        except Exception:
            self.pool = []

    def select_candidates(self, k=10):
        """Select k candidates for labeling (uncertainty sampling stub)."""
        # Placeholder: random sampling; replace with model-based uncertainty
        return random.sample(self.pool, min(k, len(self.pool)))

    def mark_labeled(self, items):
        """Remove labeled items from pool and persist."""
        ids = {i.get('id') for i in items if isinstance(i, dict) and 'id' in i}
        self.pool = [p for p in self.pool if p.get('id') not in ids]
        with open(self.pool_path, 'w') as f:
            json.dump(self.pool, f)
        return len(ids)
