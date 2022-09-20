FROM continuumio/miniconda3:4.12.0

WORKDIR /app

COPY models/ models/
COPY model-settings.json .

# Ignore hadolint error for file not found (it is downloaded)
# hadolint ignore=SC1091
RUN conda env create -f models/model/conda.yaml && \
    conda init bash && \
    . /root/.bashrc && \
    conda run --no-capture-output -n mlflow-env python -m pip install mlserver-mlflow==1.1.0

# Inference
EXPOSE 8080
# gRPC
EXPOSE 8081
# Prometheus
EXPOSE 8082

ENTRYPOINT [ "conda", "run", "--no-capture-output", "-n", "mlflow-env", "mlserver" ]
CMD [ "start", "." ]