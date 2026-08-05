Model Improvements (stubs added)

This document describes the planned implementations added as stubs on branch implement/overpowered-suggestions:

- Ensemble: basic wrapper to combine multiple model outputs (src/models/ensemble.py)
- Instruction-tuning: placeholder pipeline for SFT + RLHF/DPO (src/models/instruction_tuning.py)
- Distillation: knowledge distillation stub (src/models/distill.py)
- ONNX/TensorRT: export and optimize pipeline stubs (src/inference/optimize.py)

Next steps: wire real model loading, implement training loops, integrate with MLflow registry, and add metric-based CI gates.
