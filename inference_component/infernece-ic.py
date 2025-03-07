
#Licensed under the MIT License 

import boto3
import os, json

# Function to query endpoint
def query_endpoint(payload: dict, endpoint_name: str, inference_component_name: str) -> dict:
    client = boto3.client("sagemaker-runtime", region_name=os.environ["AWS_DEFAULT_REGION"])
    response = client.invoke_endpoint(
        InferenceComponentName=inference_component_name,
        EndpointName=endpoint_name,
        ContentType="application/json",
        Body=json.dumps(payload),
        CustomAttributes="accept_eula=true",
    )
    print(response)
    response = response["Body"].read().decode("utf8")
    response = json.loads(response)
    return response

# Variables
payload1 = {"inputs": ["how many policies are there?"]}
payload2 = {"inputs": ["Create a policy for the network"]}
endpoint = "demo-ic"
inference_components = ['demo-ic-1', 'demo-ic-2']

# Query endpoint
for ic in inference_components:
    output = query_endpoint(payload1, endpoint, ic)
    print(output)
    output = query_endpoint(payload2, endpoint, ic)
    print(output)