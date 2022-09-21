# Mlflow MLserver Docker

- [MLflow](https://mlflow.org/)
- [mlserver](https://mlserver.readthedocs.io/)

This is a utility package and CLI for building mlserver docker images based on MLflow models on a
remote tracking server.

Currently, the S3 backend is the only officially supported backend, but any backend should work just
fine as long as you have all the required dependencies installed. If you're interested in other
backends let me know.

## Installation

I recommend using [pipx](https://pypa.github.io/pipx/), but you can use any method you like such as
`poetry` or plain `pip`.

```sh
pipx install mlflow-mlserver-docker
```

## Usage

Configure access to
[the mlflow tracking server](https://mlflow.org/docs/latest/tracking.html#where-runs-are-recorded)
and
[the S3 backend](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#configuring-credentials)
using environment variables, following their respective documentation.

```sh
mlflow-mlserver-docker build runs:/fg8934ug54eg9hrdegu904/model --tag myimage:mytag
```

Any
[mlflow artifact URL](https://mlflow.org/docs/latest/python_api/mlflow.artifacts.html#mlflow.artifacts.download_artifacts)
should work fine, as long as the model uses the MLflow packaging format and contains `conda.yaml`. I
have only tested it with `scikit-learn` models logged with `mlflow.autolog()`.

## Development

```sh
poetry install
```

Make sure `docker` is running.

## Run image locally

```sh
docker run -it -p 8080:8080 myimage:mytag
```
