
#Licensed under the MIT License 

import boto3
import json
import os, time

#Global variables
endpoint_name = "CLlorax-1"
os.environ["AWS_DEFAULT_REGION"] ="us-west-2"

#Function to query the endpoint
def query_endpoint(payload: dict, endpoint_name: str) -> dict:
    client = boto3.client("sagemaker-runtime", region_name=os.environ["AWS_DEFAULT_REGION"])
    response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="application/json",
        Body=json.dumps(payload),
        CustomAttributes="accept_eula=true",
    )
    response = response["Body"].read().decode("utf8")
    response = json.loads(response)
    return response

#Input variables
input = [{"prompt": "Invoke the command to delete the camera wireless profile 'prof001' from the network \'net002\'", "adapter_id": "<Huggingface repo ID>"},{"prompt":"Retrieve latest CVEs for vendors on page 3", "adapter_id":"<Huggingface repo ID>"}]

#Select input
select_input = 1

#Set payload
payload_adapter = {
"inputs": input[select_input]["prompt"],
    "parameters": {
        "max_new_tokens": 64,
        "adapter_id": input[select_input]["adapter_id"],
        "adapter_source": "hub"
    }
}

#Query endpoint
response = query_endpoint(payload_adapter, endpoint_name)
print(response)