import logging
from typing import List, Optional

import typer
from mlflow import __version__ as mlflow_version

from mlflow_mlserver_docker.main import download_and_build

from . import __version__

logging.basicConfig(level=logging.DEBUG)

app = typer.Typer(
    help="Simple CLI tool that helps you package an MLflow model on an MLflow tacking server into a docker image capable of serving an mlserver-compliant inference webservice."
)


@app.command(help="Display the version")
def version():
    """Display the version information."""
    print("mlflow-mlserver-docker: ", __version__)
    print("mlflow: ", mlflow_version)


@app.command(help="Download model artifact and build into mlserver image")
def build(  # noqa: D103
    artifact_uri: str = typer.Argument(  # noqa: B008
        ...,
        help="See https://www.mlflow.org/docs/latest/python_api/mlflow.artifacts.html for possible formats",
    ),
    tag: Optional[List[str]] = typer.Option(  # noqa: B008
        None,
        help="Tag the image (multiple values allowed!), otherwise no tag will be used",
    ),
    log_level: str = typer.Option("INFO"),  # noqa: B008
):
    logging.getLogger().setLevel(log_level)
    download_and_build(artifact_uri, tag)


if __name__ == "__main__":
    app()
