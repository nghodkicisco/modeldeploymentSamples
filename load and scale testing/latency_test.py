
#Licensed under the MIT License 

import os
import time

# os.environ["AWS_DEFAULT_REGION"] ="us-west-2"
# endpoint_name=["mme-endpoint-test-1"]

import json
import os
import traceback
from datetime import datetime
from asyncer import asyncify
import aioboto3
import boto3
import asyncio


max_time=0
endpoint_name = "CLLorax-1"
os.environ["AWS_DEFAULT_REGION"] ="us-west-2"

def query_endpoint(payload: dict, endpoint_name: str) -> dict:
    client = boto3.client("sagemaker-runtime", region_name=os.environ["AWS_DEFAULT_REGION"])
    start_time = time.time()
    response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="application/json",
        Body=json.dumps(payload),
        CustomAttributes="accept_eula=true",
    )
    response = response["Body"].read().decode("utf8")
    end_time = time.time()
    response = json.loads(response)
    return response, end_time-start_time


async def main():
    input = "Invoke the command to delete the camera wireless profile 'prof001' from the network 'net002'"

    prompt = f'[INST] {input} [/INST]'
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 512,
            "adapter_id": "<HuggingFace repo id>",
            "adapter_source": "hub"
        }
    }

    response, time= query_endpoint(payload, endpoint_name)

    print(f"response {response[0]['generated_text']} in {time} seconds")

while True:
    asyncio.run(main())