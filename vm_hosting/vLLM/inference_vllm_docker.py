from openai import OpenAI
openai_api_key = "EMPTY"
openai_api_base = "http://<EC2-IP Address>:8000/v1"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)
models = client.models.list()
model = models.data[0].id
completion = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello, what is 2+4?"},
    ]
)
print(completion.choices[0].message.content)