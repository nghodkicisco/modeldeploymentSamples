
#Licensed under the MIT License 

import base64
import ollama

model_name = 'llama3.2:3b'
response = ollama.chat(model= model_name, messages=[
  {
    'role': 'user',
    'content': 'Can you describe kubernetes in 3 sentences',
  }
])
print(response['message']['content'])

