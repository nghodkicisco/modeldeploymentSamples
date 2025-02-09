#Copyright Cisco Systems, Inc. and its affiliates
#Licensed under the MIT License 

import os
import json
import boto3
import argparse
from sagemaker.pytorch.model import PyTorchModel

#Argument parser
parser = argparse.ArgumentParser(
                    prog='Deploy Model to Sagemaker',
                    description='This script deploys the model to sagemaker',
                    epilog='Usage: python3 deploy_sagemaker_ml.py --model_path <path to model.tar.gz> --endpoint_name <name of endpoint> --region <aws region> --role <role name>')

parser.add_argument('--model_path', type=str, help='Path to model', required=True)
parser.add_argument('--endpoint_name', type=str, help='Name of endpoint', required=True)
parser.add_argument('--region', type=str, help='AWS region', default='us-west-2')
parser.add_argument('--role', type=str, help='Role name', required=True)
argparse = parser.parse_args()

# Set environment variables
os.environ["AWS_DEFAULT_REGION"] = argparse.region
endpoint_name=argparse.endpoint_name
s3_uri=argparse.model_path
iam_client = boto3.client('iam')
role = iam_client.get_role(RoleName=argparse.role)['Role']['Arn']

# Download the model package
def download_model(s3_uri):
    s3 = boto3.client('s3')
    bucket = s3_uri.split('/')[2]
    key = '/'.join(s3_uri.split('/')[3:])
    model = key.split('/')[-1]
    s3.download_file(bucket, key, model)
    print("Model package downloaded successfully")
    return model

#unzip the model package in folder model_to_deploy without printing the output
def silent_unzip(model):
    os.system("mkdir model_to_deploy")
    os.system("tar -xzf "+model+" -C model_to_deploy")
    print("Model package unzipped successfully")

# check if inference.py and requirements.txt and code directory exists in above extracted directory or subfolders
def check_files(directory):
    check = 0
    for root, dirs, files in os.walk(directory):
        if 'inference.py' in files and 'requirements.txt' in files:
            check += 1
        if 'code' in dirs:
            check += 1
    if check == 2:
        return True
    else:
        return False

# delete the model package and model_to_deploy folder
def delete_files():
    os.system("rm -rf " + model)
    os.system("rm -rf model_to_deploy")

model = download_model(s3_uri)
silent_unzip(model)

#verify if code/ directory exists in above extracted directory as subfolder
if check_files("model_to_deploy"):
    print("Code directory includes inference.py and requirements.txt")
    delete_files()
else:
    print("Code directory does not exist")
    print("Exiting")
    delete_files()
    exit(1)


# Deploy model to SageMaker
pt_model = PyTorchModel(
    # path to your trained SageMaker model
    model_data=s3_uri,
    role=role,                      # IAM role the sagemaker endpoint will use
    framework_version="2.0",        # PyTorch version used (actual: 2.1.1)
    py_version='py310',             # Python version used
)
# deploy model to SageMaker Inference
predictor = pt_model.deploy(
    endpoint_name=endpoint_name,
    initial_instance_count=3,
    instance_type="ml.g4dn.2xlarge"
)

# test inference
def query_endpoint(payload: dict, endpoint_name: str) -> dict:
    client = boto3.client("sagemaker-runtime", region_name=os.environ["AWS_DEFAULT_REGION"])
    response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="application/json",
        Body=json.dumps(payload),
        CustomAttributes="accept_eula=true",
    )
    print(response)
    response = response["Body"].read().decode("utf8")
    response = json.loads(response)
    return response

response= query_endpoint({"inputs": ["How many policies are there?"]}, endpoint_name)
print(response)