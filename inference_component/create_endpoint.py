
#Licensed under the MIT License 

import sagemaker
import boto3
import time
from sagemaker.huggingface import HuggingFaceModel, get_huggingface_llm_image_uri

#variables
endpoint_config_name = 'demo-ic'
variant_name = 'AllTraffic'
initial_instance_count = 1
model_data_download_timeout_in_seconds = 1200
container_startup_health_check_timeout_in_seconds = 1200
max_instance_count = 4
instance_type = 'ml.g5.12xlarge'
endpoint_name = 'demo-ic'

iam_client = boto3.client('iam')
role = iam_client.get_role(RoleName='admin')['Role']['Arn']

#get imageuri
image_uri = sagemaker.image_uris.retrieve(
        framework="pytorch",
        region="us-west-2",
        py_version="py310",
        image_scope="inference",
        version="2.0.1",
        instance_type="ml.g5.12xlarge",
    )

sagemaker_client = boto3.client('sagemaker')
#Create endpoint configuration

resp_epconf = sagemaker_client.create_endpoint_config(
    EndpointConfigName=endpoint_config_name,
    ExecutionRoleArn=role,
    ProductionVariants=[
        {
            "VariantName": variant_name,
            "InstanceType": instance_type,
            "InitialInstanceCount": 1,
            "ModelDataDownloadTimeoutInSeconds": model_data_download_timeout_in_seconds,
            "ContainerStartupHealthCheckTimeoutInSeconds": container_startup_health_check_timeout_in_seconds,
            "ManagedInstanceScaling": {
                "Status": "ENABLED",
                "MinInstanceCount": initial_instance_count,
                "MaxInstanceCount": max_instance_count,
            },
            "RoutingConfig": {"RoutingStrategy": "LEAST_OUTSTANDING_REQUESTS"},
        }
    ],
)
print("Endpoint configuration created")

#Create endpoint
resp_ep = sagemaker_client.create_endpoint(
    EndpointName=endpoint_name,
    EndpointConfigName=endpoint_config_name,
)
# #Adding timer to give sufficient time for sagemaker to create endpoint
time.sleep(240)
print("Endpoint created")
s3_buckets = ['s3://<Model Package 1>.tar.gz','s3://<Model Package 2>.tar.gz']
models = ['demo-ic-1', 'demo-ic-2']

#Create model objects
for model_name, bucket in zip(models, s3_buckets):
    sagemaker_client.create_model(
        ModelName=model_name,
        ExecutionRoleArn=role,
        PrimaryContainer={
            "Image": image_uri,
            "ModelDataUrl": bucket,
        },
    )
    print("Model object for model "+model_name+" created")

