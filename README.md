# Mlflow Mlserver Docker

This is a utility package for building mlserver docker images based on MLflow models on a remote
tracking server.

Currently, the S3 backend is the only officially supported backend, but any backend should work just
fine as long as you have all the required dependencies installed. If you're interested in other
backends let me know.

## Installation

```
pip install mlflow-mlserver-docker
```

## Usage

```sh
mlflow-mlserver-docker build runs:/fg8934ug54eg9hrdegu904/model
```
