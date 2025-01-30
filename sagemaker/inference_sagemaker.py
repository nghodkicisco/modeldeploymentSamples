import boto3
import os, json
# test inference
def query_endpoint(payload: dict, endpoint_name: str) -> dict:
    client = boto3.client("sagemaker-runtime", region_name=os.environ["AWS_DEFAULT_REGION"])
    response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="application/json",
        Body=json.dumps(payload),
        CustomAttributes="accept_eula=true",
    )
    #print(response)
    response = response["Body"].read().decode("utf8")
    response = json.loads(response)
    return response

payload = {"inputs": ["What software versions of Apache are affected by CVE-2021-44228?"]}
endpoint = "clmlsreendpoint"

outut= query_endpoint(payload,endpoint)

print(outut)