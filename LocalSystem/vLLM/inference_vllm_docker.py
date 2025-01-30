from openai import OpenAI
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)
models = client.models.list()
model = models.data[0].id
completion = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "Can you describe kubernetes in 3 sentences"},
        {"role": "user", "content": "Hello"},
    ]
)

print(completion.choices[0].message.content)