# download mlflow model
import json
import logging
import tempfile
from os import environ
from pathlib import Path
from typing import List, Optional

from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
from mlflow import MlflowException
from mlflow import artifacts as mlflow_artifacts
from python_on_whales import docker

logger = logging.getLogger(__name__)


def _download_model_artifact(artifact_uri: str, path: Path) -> None:
    """Get the model URI from the tracking server and download it.

    Args:
        artifact_uri (str): The uri for the artifact to download
        path (Path): Where to download the model to

    Raises:
        ValueError: Download failed because of a known configuration issue.
        MlflowException: Download failed because of an unhandled MLflow error.
    """
    try:
        mlflow_artifacts.download_artifacts(artifact_uri=artifact_uri, dst_path=path / "models")
    except MlflowException as e:
        if not environ.get("MLFLOW_TRACKING_URI"):
            raise ValueError(
                "Could not reach the MLflow tracking server because MLFLOW_TRACKING_URI was not set."
            ) from e
        raise e
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise ValueError(
            "Tried to download artifact from AWS S3, but found no complete credentials set."
        ) from e
    except ClientError as e:
        raise ValueError(
            "The AWS SDK could not reach the resource because of client configuration errors."
        ) from e
    logger.debug("Downloaded model %s to %s", artifact_uri, path)


def _create_mode_settings_file(run_id: str, path: Path) -> None:
    model_config = {
        "name": "mlflow-model",
        "implementation": "mlserver_mlflow.MLflowRuntime",
        "parameters": {
            "uri": "/app/models/model",
            "version": run_id,
        },
    }

    with open(path / "model-settings.json", "w") as f:
        json.dump(model_config, f)

    logger.debug("Wrote model config to %s: %s", path, model_config)


def _build_model_service_image(path: Path, tags: Optional[List[str]] = None):
    if not tags:
        logger.warning("No tags provided, will build image without tags.")
    else:
        logger.debug("Found provided tags %s", tags)

    image = docker.build(
        path,
        tags=tags,
        file=Path(__file__).parent / "Dockerfile",
    )
    logger.debug("Successfully built image %s", image.id)


def download_and_build(artifact_uri: str, tag: Optional[List[str]]):
    """Download model artifact to local disc and build into docker image.

    Args:
        artifact_uri (str): URI of the artifact to download
        tag (Optional[List[str]]): List of tags to apply to the built image
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        _download_model_artifact(artifact_uri, tmpdir_path)
        _create_mode_settings_file(artifact_uri, tmpdir_path)
        _build_model_service_image(tmpdir_path, tag)
