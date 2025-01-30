import json
import sagemaker
from sagemaker import Model
import boto3
from sagemaker.huggingface import HuggingFaceModel, get_huggingface_llm_image_uri

try:
    role = sagemaker.get_execution_role()
except ValueError:
    iam = boto3.client('iam')
    role = iam.get_role(RoleName='aiml')['Role']['Arn']

#model_ID = "cjsanjay/llama-3-8B-gorilla-meraki_v2"
model_ID = "meta-llama/Meta-Llama-3-8B"

image_uri = "422940237045.dkr.ecr.us-west-2.amazonaws.com/lorax:latest"


# Hub Model configuration. https://huggingface.co/models
hub = {
    'HF_MODEL_ID': model_ID,
    'SM_NUM_GPUS': json.dumps(1),
    'HF_TOKEN': "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",
    'MAX_INPUT_LENGTH': json.dumps(4096),  # Max length of input text
    'MAX_TOTAL_TOKENS': json.dumps(8192),  # Max length of the generation (including input text)
}

# create Hugging Face Model Class
lorax_model = Model(
    image_uri=image_uri,
    role=role,
    env=hub
)

# deploy model to SageMaker Inference
predictor = lorax_model.deploy(
    endpoint_name="CLLorax-1",
    initial_instance_count=1,
    instance_type="ml.g5.2xlarge",
    container_startup_health_check_timeout=1600,
)

# send request
out = predictor.predict({"inputs": "[INST] Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May? [/INST]", "parameters": {"max_new_tokens": 64}})
print(out)
