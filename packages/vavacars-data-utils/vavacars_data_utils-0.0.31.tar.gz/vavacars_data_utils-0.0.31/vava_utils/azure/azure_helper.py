import logging

from azureml.core import Environment
from azureml.core import Workspace
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice, LocalWebservice, Webservice
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.model import Model

from vava_utils.utils.singleton import singleton


@singleton
class Azure_Helper:
    
    def __init__(self, config):
        """
        Azure helper constructor.

        Parameters:
            config: dictionary with the following keys for Azure authentication and setting up Workspace.
                - tenant_id
                - service_principal_id
                - service_principal_password
                - subscription_id
                - resource_group
                - workspace_name
        """
        self.auth = ServicePrincipalAuthentication(
            tenant_id=config["tenant_id"],
            service_principal_id=config["service_principal_id"],
            service_principal_password=config["service_principal_password"],
        )
        self.ws = Workspace(
            subscription_id=config["subscription_id"],
            resource_group=config["resource_group"],
            workspace_name=config["workspace"],
            auth=self.auth,
        )

    def register_model(self, path, name, **kwargs):
        """
        Register a new model version in Azure ML

        Args:
            path (str): local model file path
            name (str): model name

        Returns:
            Model: Azure Model instance
        """
        return Model.register(model_path=path, model_name=name, workspace=self.ws, **kwargs)

    def download_model(self, name, path='.', **kwargs):
        """
        Download model file from a registered Azure ML Model

        Args:
            name (str): remote model name
            path (str): local path to download model, default is '.'
        """
        Model(name=name, workspace=self.ws).download(path)

    def deploy_endpoint(self, deploy_cfg, update=False, local=False):
        """
        Deploy Azure ML endpoint

        Args:
            deploy_cfg (dict): Dictionary with deployment config parameters.
                - name (str): endpoint name
                - models (list(str)): list of model names used in the endpoint
                - inference: InferenceConfig class parameters
                    - source_directory (str): local directoy with all required files (include dependencies)
                    - entry_script (str): entrypoint script
                - environment: Environment clas paramenters
                    - name (str): environment name
                    - python_packages list(str): list of required python packages
                - deploy: Webservice.deploy_configuration parameters
                    - cpu_cores (int)
                    - memory_gb (int)
                    - auth_enabled (bool)
                - local: Only when local=True, LocalWebservice.deploy_configuration parameters
                    port (int):
            update (bool, optional): True if updating a previously created Endpoint. Defaults to False.
            local (bool, optional): Deploy as local endpoint. Defaults to False.

        Returns:
            Webservice: instance of Azure Webservice
        """
            
        models = [Model(name=model_name, workspace=self.ws) for model_name in deploy_cfg['models']]
        
        env = Environment(name=deploy_cfg['environment']['name'])
        for package in deploy_cfg['environment']['python_packages']:
            env.python.conda_dependencies.add_pip_package(package)
        inference_config = InferenceConfig(environment=env, **deploy_cfg['inference'])
        
        if update:
            service = AciWebservice(name=deploy_cfg['name'], workspace=self.ws)
            service.update(models=models, inference_config=inference_config)
        else:
            if local:
                deployment_config = LocalWebservice.deploy_configuration(**deploy_cfg['local'])
            else:
                deployment_config = AciWebservice.deploy_configuration(**deploy_cfg['deploy'])
            service = Model.deploy(
                workspace=self.ws,
                name=deploy_cfg['name'],
                models=models,
                inference_config=inference_config,
                deployment_config=deployment_config,
                overwrite=True,
            )
        try:
            service.wait_for_deployment(show_output=True)
            logging.info(f"Completed: {service.state}, see first logs. Key={service.get_keys()}")
            logging.info(f"Endpoint URL: {service.scoring_uri}")
        except Exception as e:
            logging.warn(f"Exception ({e}) when updating endpoint: {service.get_logs()}")

        logging.info(f"Completed, logs: {service.get_logs()}")

        return service
