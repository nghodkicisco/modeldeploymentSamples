#Copyright Cisco Systems, Inc. and its affiliates
#Licensed under the MIT License 


import boto3
import os, json
# test inference
def query_endpoint(payload: dict, endpoint_name: str) -> dict:
    client = boto3.client("sagemaker-runtime", region_name=os.environ["AWS_DEFAULT_REGION"])
    response = client.invoke_endpoint(
        InferenceComponentName="ciscolive-demo-ic-1",
        EndpointName=endpoint_name,
        ContentType="application/json",
        Body=json.dumps(payload),
        CustomAttributes="accept_eula=true",
    )
    #print(response)
    response = response["Body"].read().decode("utf8")
    response = json.loads(response)
    return response

payload = {"inputs": ["how many policies are there?"]}
endpoint = "ciscolive-demo-ic"

outut= query_endpoint(payload,endpoint)

print(outut)