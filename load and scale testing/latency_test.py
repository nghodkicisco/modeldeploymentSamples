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


#input_queries=["allow access to jira for tmathew", "Isolate guest when accessing content category gaming", "Isolate guest when accessing content category gaming", "give tmathew@cisco.com access to vpcs", "allow any source access to any destination on port 80", "allow marketing access to social media", "create internet access rule to allow everyone access to jira on port 80", "create internet access rule to allow everyone access to jira on port 80", "Allow backup-server-3 to access servers-eng1 and block access to China_Banned_Websites. Call the rule 'Server AUTH'", "Allow Backup-server-1 access to Servers-Eng1", "Allow backup-server-3 to access servers-eng1 and block access to China_Banned_Websites. Call the rule 'Server AUTH'", "Warn user jsmith1 when accessing cryptocurrency. Call rule 'crypto-policy'. Isolate 'guest user' when accessing cryptocurrency. Name the rule 'guest crypto policy'", "create internet access rule to allow everyone access to jira on port 80", "qetest1@cisco.com cannot access pornography", "allow any access to private app jira and block any to jira", "allow any access to private app jira and block any to jira", "create private access rule to block any to any", "allow 10.1.1.2 access to 192.1.2.3 on port 80 and tcp protocol", "allow marketing access to social media", "give tmathew@cisco.com access to vpcs", "allow eng1", "give eng1 access to jira but not jsmith8", "create internet access rule to allow everyone access to jira on port 80", "allow any access to private app jira and block any to jira", "Isolate guest when accessing content category gaming", "Allow Sammuel Johnson acces to content categry ads and destination list Servers-Eng1. Call this rule 'onboarding Sammuel Johnson 2'", "allow any access to private app jira and block any to jira", "give eng1 and jsmith access to jira", "Allow backup-server-3 to access servers-eng1 and block access to China_Banned_Websites. Call the rule 'Server AUTH'", "allow any source access to any destination on port 80", "allow any source access to any destination on port 80", "qetest1@cisco.com cannot access pornography", "Warn user jsmith1 when accessing cryptocurrency. Call rule 'crypto-policy'. Isolate 'guest user' when accessing cryptocurrency. Name the rule 'guest crypto policy'", "allow any access to private app jira and block any to jira", "allow access to jira for tmathew", "give eng1 access to jira but not jsmith8", "allow marketing access to social media", "allow 10.1.1.2 access to 192.1.2.3 on port 80 and tcp protocol", "give eng1 access to jira but not jsmith8", "allow access to jira for tmathew", "Warn user jsmith2 when accessing cryptocurrency. Call rule 'crypto-policy'.", "Warn guest", "allow any access to private app jira and block any to jira", "give tmathew@cisco.com access to vpcs", "Allow Sammuel Johnson acces to content categry ads and destination list Servers-Eng1. Call this rule 'onboarding Sammuel Johnson 2'", "give eng1 and jsmith access to jira", "give test - server - 1 access to jira", "Warn guest", "allow access to jira for Eng1.", "allow any access to private app jira and block any to jira", "Warn user jsmith1 when accessing cryptocurrency. Call rule 'crypto-policy'. Isolate 'guest user' when accessing cryptocurrency. Name the rule 'guest crypto policy'", "block jsmith1 from china_banned_websites. name the rule 'js1 china policy2'", "Warn sammuel johnson when visiting porn websites. Call rule 'NO PORN SJ'", "Warn sammuel johnson when visiting porn websites. Call rule 'NO PORN SJ'", "Allow Backup-server-1 access to Servers-Eng1", "Warn any user when accessing content category gaming and block any group when accessing destination list 'india banned websites'", "qetest1@cisco.com cannot access pornography", "give test - server - 1 access to jira"]
#input_queries=["allow access to jira for tmathew", "Isolate guest when accessing content category gaming", "Isolate guest when accessing content category gaming", "give tmathew@cisco.com access to vpcs"]
max_time=0
endpoint_name = "CLLorax-1"
#endpoint_name = "opencve-llama3-v1"
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

# async def main():
#     for endpoint in endpoint_name:
#         for input in input_queries:
#             response= query_endpoint({"inputs": input}, endpoint)
#             print(f"Request completed for {endpoint} with response {response}")


async def main():
    input = "Invoke the command to delete the camera wireless profile 'prof001' from the network 'net002'"

    prompt = f'[INST] {input} [/INST]'
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 512,
            "adapter_id": "nghodki/meraki",
            "adapter_source": "hub"
        }
    }

    response, time= query_endpoint(payload, endpoint_name)

    print(f"response {response[0]['generated_text']} in {time} seconds")

while True:
    asyncio.run(main())