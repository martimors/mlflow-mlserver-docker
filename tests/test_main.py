from mlflow_mlserver_docker.main import download_and_build


def test_main():  # noqa: D103
    run_id = "runs:/3bc11c8e9c804c65bc6973dbeedffe35/model"
    download_and_build(run_id)
