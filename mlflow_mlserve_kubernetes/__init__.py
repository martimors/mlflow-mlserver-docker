from mlflow.deployments import BaseDeploymentClient
from mlflow.exceptions import MlflowException

def run_local(target, name, model_uri, flavor=None, config=None):  # pylint: disable=W0613
    """
    .. Note::
        This function is kept here only for documentation purpose and not implementing the
        actual feature. It should be implemented in the plugin's top level namescope and should
        be callable with ``plugin_module.run_local``
    Deploys the specified model locally, for testing. This function should be defined
    within the plugin module. Also note that this function has a signature which is very
    similar to :py:meth:`BaseDeploymentClient.create_deployment` since both does logically
    similar operation.
    :param target: Which target to use. This information is used to call the appropriate plugin
    :param name:  Unique name to use for deployment. If another deployment exists with the same
                     name, create_deployment will raise a
                     :py:class:`mlflow.exceptions.MlflowException`
    :param model_uri: URI of model to deploy
    :param flavor: (optional) Model flavor to deploy. If unspecified, default flavor is chosen.
    :param config: (optional) Dict containing updated target-specific config for the deployment
    :return: None
    """
    raise NotImplementedError(
        "This function should be implemented in the deployment plugin. It is"
        "kept here only for documentation purpose and shouldn't be used in"
        "your application"
    )


def target_help():
    """
    Return a string containing detailed documentation on the current deployment target, to be
    displayed when users invoke the ``mlflow deployments help -t <target-name>`` CLI. This
    method should be defined within the module specified by the plugin author.
    The string should contain:
    * An explanation of target-specific fields in the ``config`` passed to ``create_deployment``,
      ``update_deployment``
    * How to specify a ``target_uri`` (e.g. for AWS SageMaker, ``target_uri`` have a scheme of
      "sagemaker:/<aws-cli-profile-name>", where aws-cli-profile-name is the name of an AWS
      CLI profile https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html)
    * Any other target-specific details.
    """
    return """
    Build docker images with mlserver, mlflow, pyfunc. Output kubernetes manifests to deploy them
    to kubernetes.

    target_uri should have the form k8s://context/namespace. Default namespace is `default`.
    """

class KubernetesDeploymentClient(BaseDeploymentClient):
    def __init__(self, target_uri):
        super().__init__(target_uri)
    
    def create_deployment(self, name, model_uri, flavor=None, config=None, endpoint=None):
        return super().create_deployment(name, model_uri, flavor, config, endpoint)
    
    def update_deployment(self, name, model_uri=None, flavor=None, config=None, endpoint=None):
        return super().update_deployment(name, model_uri, flavor, config, endpoint)
    
    def delete_deployment(self, name, config=None, endpoint=None):
        return super().delete_deployment(name, config, endpoint)
    
    def list_deployments(self, endpoint=None):
        return super().list_deployments(endpoint)
    
    def get_deployment(self, name, endpoint=None):
        return super().get_deployment(name, endpoint)
    
    def predict(self, deployment_name=None, df=None, endpoint=None):
        return super().predict(deployment_name, df, endpoint)