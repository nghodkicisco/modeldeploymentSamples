
import boto3
import json
import os, time


endpoint_name = "CLLorax-1"
#endpoint_name = "opencve-llama3-v1"
os.environ["AWS_DEFAULT_REGION"] ="us-west-2"

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

prompt = '[/INST]Please remove the action batch having actionBatchId \'actionBatch007\' in the organization identified by the organizationId \'org2690\'[/INST]'
#input_queries = ["Invoke the command to delete the camera wireless profile 'prof001' from the network 'net002'.","Please remove the action batch having actionBatchId 'actionBatch007' in the organization identified by the organizationId 'org2690'"]


input_meraki = "Invoke the command to delete the camera wireless profile 'prof001' from the network 'net002'"
input_opencve = "Retrieve latest CVEs for vendors on page 3"
input = [{"prompt": "Invoke the command to delete the camera wireless profile 'prof001' from the network \'net002\'", "adapter_id": "nghodki/meraki"},{"prompt":"Retrieve latest CVEs for vendors on page 3", "adapter_id":"nghodki/opencve"}]
select_input = 1
payload_adapter = {
"inputs": input[select_input]["prompt"],
    "parameters": {
        "max_new_tokens": 64,
        "adapter_id": input[select_input]["adapter_id"],
        "adapter_source": "hub"
    }
}

response = query_endpoint(payload_adapter, endpoint_name)
print(response)
# while True:
#     start_time = time.time()
#     response = query_endpoint(payload_adapter, endpoint_name)
#     end_time = time.time()
#     print(f'{response} in {end_time - start_time} seconds')