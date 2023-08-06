import os
from azureml.core import Workspace, Experiment, Datastore, RunConfiguration, Environment
from azureml.widgets import RunDetails
from azureml.data.data_reference import DataReference
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import DockerConfiguration

from azureml.pipeline.core import Pipeline, PipelineData
from azureml.pipeline.steps import PythonScriptStep

from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException
from numpy import array

class Makana():
  
    def getServicePrincipal():
        svc_pr = ServicePrincipalAuthentication(
            tenant_id="178c68b2-1cda-43eb-b33d-7f2d26724ce1",
            service_principal_id="71f42381-770f-4155-9ac7-5807110bdcaa",
            service_principal_password="Z9u2]:TTgBOi[@0N7r39Xf@RJ9qvuv7D")
        return svc_pr

    def InitializeWorkspace(svc_pr: ServicePrincipalAuthentication):
        ws = Workspace(
            subscription_id="e7895078-e8b9-4698-994e-2c1c128c2043",
            resource_group="textsearch-demo",
            workspace_name="textsearch-ml-ws",
            auth=svc_pr)
        print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep = '\n')
        # cts = ws.compute_targets
        # for ct in cts:
        #     print(ct)
        return ws
    
    def GetDefaultDataStore(ws: Workspace):
        # Default datastore
        def_blob_store = ws.get_default_datastore()
        print("Blobstore's name: {}".format(def_blob_store.name))
        
        return def_blob_store    
    
    def GetDataStore(name: str, ws: Workspace):
        # The following call GETS the Azure Blob Store associated with your workspace.
        # Note that workspaceblobstore is **the name of this store and CANNOT BE CHANGED and must be used as is** 
        def_blob_store = Datastore(ws, name)
        print("Blobstore's name: {}".format(def_blob_store.name))
        return def_blob_store
    
    def GetCompute(computeName: str, ws: Workspace):
        try:
            aml_compute = AmlCompute(ws, computeName)
            print("found existing compute target.")
            return aml_compute
        except ComputeTargetException:
            print("Compute Not Found")
                
    def CreateCompute(computeName: str,ws: Workspace, vm_size: str, min_nodes: int, max_nodes: int):
        print("creating new compute target")
        
        provisioning_config = AmlCompute.provisioning_configuration(vm_size = vm_size,
                                                                    min_nodes = min_nodes, 
                                                                    max_nodes = max_nodes)    
        aml_compute = ComputeTarget.create(ws, computeName, provisioning_config)
        aml_compute.wait_for_completion(show_output=True, min_node_count=None, timeout_in_minutes=20)
        return aml_compute
    
    def CreateDataReference(data_reference_name: str, def_blob_store: Datastore, path_on_datastore: str):
        blob_input_data = DataReference(
            datastore=def_blob_store,
            data_reference_name=data_reference_name,
            path_on_datastore=path_on_datastore)
        print("DataReference object created")
        return blob_input_data
    
    def CreatePipelineData(name: str, def_blob_store: Datastore):
        pipeline_data = PipelineData(
            name,
            datastore=def_blob_store,
            output_overwrite=True)
        print("PipelineData object for" + name + "created")

        return pipeline_data
    
    def InitializeCondaDependencies(channels: array=None, pipPackages: array=None , condaPackages: array=None):
        dependencies=CondaDependencies()
        if channels:
            for channel in channels:
                dependencies.add_channel(channel)
        if pipPackages:
            for package in pipPackages:
                dependencies.add_pip_package(package)
        if condaPackages:
            for package in condaPackages:
                dependencies.add_conda_package(package)
        
        run_config=RunConfiguration(conda_dependencies=dependencies)
        docker_config = DockerConfiguration(use_docker=True)
        run_config.docker=docker_config
        return run_config

    

    def CreatePythonScriptStep(source_directory: str, name: str, script_name: str, arguments: array, inputs: array, outputs: array,
                                aml_compute: AmlCompute, run_config: RunConfiguration):
        
        print('Source directory for the step is {}.'.format(os.path.realpath(source_directory)))
        pythonScriptStep = PythonScriptStep(name=name,
                         script_name=script_name, 
                         arguments=arguments,
                         inputs=inputs,
                         outputs=outputs,
                         compute_target=aml_compute, 
                         runconfig=run_config,
                         source_directory=source_directory,
                         allow_reuse=True)
        print(name + "Step Created")
        
        return pythonScriptStep
        
    def SubmitPipeline(pythonScriptSteps: array , ws: Workspace):
        
        # list of steps to run
        # steps = [cleanTextStep, createModelStep]
        # print("Step lists created")
        
        pipeline = Pipeline(workspace=ws, steps=pythonScriptSteps)
        print ("Pipeline is built")

        pipeline.validate()
        print("Pipeline validation complete")
        
        # Submit syntax
        # submit(experiment_name, 
        #        pipeline_parameters=None, 
        #        continue_on_step_failure=False, 
        #        regenerate_outputs=False)

        pipeline_run = Experiment(ws, 'textsearch_pipeline').submit(pipeline, regenerate_outputs=False)
        print("Pipeline is submitted for execution")
        return pipeline_run
    
    def WaitForComletionPipeline(pipelineRun: Experiment):
        
        # RunDetails(pipeline_run).show()
        abc = pipelineRun.wait_for_completion()
        # published_pipeline = pipelineRun.publish_pipeline(name="text search pipeline", description="text search", version="1.0")
        # published_pipeline
        return pipelineRun