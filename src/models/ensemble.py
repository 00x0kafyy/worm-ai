"""Ensemble stub: combine multiple model outputs."""

class Ensemble:
    def __init__(self, models):
        # models: list of callables or model objects with a predict(payload) method
        self.models = models

    def predict(self, payload):
        # Call each model and average numeric scores or concat text outputs as placeholder
        outputs = []
        for m in self.models:
            try:
                out = m.predict(payload)
            except Exception:
                out = None
            outputs.append(out)
        # Simple placeholder: return first non-null
        for o in outputs:
            if o is not None:
                return o
        return {'error': 'no model output'}
