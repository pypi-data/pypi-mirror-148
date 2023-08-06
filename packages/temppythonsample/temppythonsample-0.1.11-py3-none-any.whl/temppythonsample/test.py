import os
import makana

# source_directory = './temppythonsample'
# print('Source directory for the step is {}.'.format(os.path.realpath(source_directory)))

svc_pr = makana.Makana.getServicePrincipal()

ws = makana.Makana.InitializeWorkspace(svc_pr)

# Default datastore
def_blob_store = makana.Makana.GetDefaultDataStore(ws)

# The following call GETS the Azure Blob Store associated with your workspace.
# Note that workspaceblobstore is **the name of this store and CANNOT BE CHANGED and must be used as is** 

def_blob_store = makana.Makana.GetDataStore("workspaceblobstore",ws)
  
# Get Existing Compute
aml_compute = makana.Makana.GetCompute("aml-Compute", ws)

# Create Compute

# aml_compute = makana.Makana.CreateCompute("Sample-Compute",ws, "STANDARD_D2_V2", 1, 4)

blob_input_data = makana.Makana.CreateDataReference("source_data", def_blob_store,"textsearch/input_data_small.csv")

clean_text_data = makana.Makana.CreatePipelineData("clean_text_output", def_blob_store)

trained_model = makana.Makana.CreatePipelineData("trained_model", def_blob_store)

dependencies = makana.Makana.InitializeCondaDependencies(["conda-forge"],["pandas"], ["gensim==3.8.0","scikit-learn"])

step1 = makana.Makana.CreatePythonScriptStep("./source_directory","clean_text","cleantext.py", ["--read-from-file", blob_input_data, "--save-to-file-path", clean_text_data],
                                             [blob_input_data], [clean_text_data], aml_compute, dependencies)

step2 = makana.Makana.CreatePythonScriptStep("./source_directory","create_model","createmodel.py", ["--glove-vector-file", "glove.6B.50d.txt", "--input-data-file", clean_text_data, "--save-model-path", trained_model, "--debug-logging"],
                                             [clean_text_data], [trained_model], aml_compute, dependencies)

pipeline = makana.Makana.SubmitPipeline([step1,step2], ws)

pipeline_run = makana.Makana.WaitForComletionPipeline(pipeline)