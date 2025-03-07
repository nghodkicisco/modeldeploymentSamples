
#Licensed under the MIT License 

import boto3
import time

#Create sageMaker client
sagemaker_client = boto3.client('sagemaker')

#variables for inference component
endpoint_name = 'demo-ic'
variant_name = 'AllTraffic'
inference_components = ['demo-ic-1', 'demo-ic-2']
models = ['demo-ic-1', 'demo-ic-2']

#Function for creating inference Component
def create_inference_component(inference_component, model_name):

    resp_ic = sagemaker_client.create_inference_component(
        InferenceComponentName=inference_component,
        EndpointName=endpoint_name,
        VariantName=variant_name,
        Specification={
            "ModelName": model_name,
            "StartupParameters": {
                "ModelDataDownloadTimeoutInSeconds": 1200,
                "ContainerStartupHealthCheckTimeoutInSeconds": 1200,
            },
            "ComputeResourceRequirements": {"NumberOfAcceleratorDevicesRequired": 1.0, "MinMemoryRequiredInMb": 2048}
        },
        RuntimeConfig={"CopyCount": 1},
    )

#Create inference components
for ic,model in zip(inference_components, models):
    create_inference_component(ic, model)
    while True:
        desc = sagemaker_client.describe_inference_component(
            InferenceComponentName=ic
        )
        status = desc["InferenceComponentStatus"]
        print("Inference Component "+ic+" deployment is "+status)
        if status == "InService":
            break
        time.sleep(30)
    print("Inference Component "+ic+" is deployed")