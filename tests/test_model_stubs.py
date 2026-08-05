from src.models.ensemble import Ensemble
from src.models.instruction_tuning import instruction_tune
from src.models.distill import distill

class DummyModel:
    def predict(self, payload):
        return {'result': 'dummy'}

def test_ensemble():
    e = Ensemble([DummyModel()])
    out = e.predict({'x':1})
    assert out.get('result') == 'dummy'

def test_instruction_tune(tmp_path):
    res = instruction_tune('data/placeholder', str(tmp_path))
    assert res['status'].startswith('instruction_tune')

def test_distill(tmp_path):
    res = distill('teacher', 'student', None, str(tmp_path / 'student.json'))
    assert res['status'] == 'distill_stub'
