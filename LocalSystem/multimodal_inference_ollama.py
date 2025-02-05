import base64
import ollama

model_name = 'llama3.2-vision:11b'
response = ollama.chat(model= model_name, messages=[
  {
    'role': 'user',
    'content': 'Are there any humans in this photo?Only answer with yes or no',
    'images': ['test.png']
  }
])
print(response['message']['content'])

