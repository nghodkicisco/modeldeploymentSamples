import base64
import ollama

model_name = 'deepseek-r1:7b'

response = ollama.chat(model= model_name, messages=[
  {
    'role': 'user',
    'content': 'Can you describe kubernetes in 3 sentences',
    #'images': ['test.png']
  }
])
print(response['message']['content'])