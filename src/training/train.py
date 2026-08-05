"""Training stub that logs metrics to MLflow and saves a metric file for CI gates."""
import random, json, os

try:
    import mlflow
except Exception:
    mlflow = None

METRIC_FILE = 'train_metrics.json'

def train():
    # Fake training loop producing a validation accuracy
    val_acc = 0.8 + random.random() * 0.2
    metrics = {'val_accuracy': val_acc}

    # Log to MLflow if available
    if mlflow:
        mlflow.start_run()
        mlflow.log_metric('val_accuracy', val_acc)
        mlflow.end_run()

    # Persist metric for CI gating
    with open(METRIC_FILE, 'w') as f:
        json.dump(metrics, f)
    print('Training stub completed. Metrics:', metrics)

if __name__ == '__main__':
    train()
