# download mlflow model
import json
from mlflow import artifacts as mlflow_artifacts
from pathlib import Path

model_path = Path("models")

mlflow_artifacts.download_artifacts(
    run_id="3bc11c8e9c804c65bc6973dbeedffe35", dst_path="models"
)

# build docker image
model_config = {
    "name": "testmodel",
    "implementation": "mlserver_mlflow.MLflowRuntime",
    "parameters": {"uri": str(model_path)},
}

with open("model-settings.json", "w") as f:
    json.dump(model_config, f)

# synth
