
#Licensed under the MIT License 

import os
import json
import time
from locust import User, task, between
import boto3

endpoint_name = "CLLorax-1"
os.environ["AWS_DEFAULT_REGION"] ="us-west-2"


def query_endpoint(payload: dict, endpoint_name: str) -> dict:
    client = boto3.client("sagemaker-runtime", region_name=os.environ["AWS_DEFAULT_REGION"])
    response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="application/json",
        Body=json.dumps(payload),
        CustomAttributes="accept_eula=true",
    )

    response_body = response["Body"].read().decode("utf8")
    return json.loads(response_body)


class SageMakerEndpointUser(User):
    input_queries = ["Invoke the command to delete the camera wireless profile \'prof001\' from the network \'net002\'"]
    @task
    def query_task_classifier(self):
        for input in self.input_queries:
            prompt = f'[INST]{input}[/INST]'
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 64,
                    "adapter_id": "<Huggingface repo ID>",
                    "adapter_source": "hub"
                }
            }
            endpoint_name = "CLLorax-1"
            self.common_helper(payload, endpoint_name)


    def common_helper(self, payload, endpoint_name):
        start_time = time.time()
        try:
            result = query_endpoint(payload, endpoint_name)
            # In real usage, you should determine the success condition properly
            self.environment.events.request.fire(
                request_type="SageMaker",
                name=endpoint_name,
                response_time=int((time.time() - start_time) * 1000),
                response=result,
                response_length=len(result),
            )
        except Exception as e:
            # Fire a failure event
            print("Failure")
            self.environment.events.request.fire(
                request_type="SageMaker",
                name=endpoint_name,
                response_time=int((time.time() - start_time) * 1000),
                exception=e,
            )


# Set environment variables
os.environ["AWS_DEFAULT_REGION"] = "us-west-2"
