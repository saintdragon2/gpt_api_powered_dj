import os
import openai
from api_keys import openai_api_key
from base64 import b64decode

openai.api_key = openai_api_key

response = openai.Image.create(
    prompt="A Ferrari is cruising through the big city at night.",
    n=1,
    size="512x512",
    response_format='b64_json'
)

# print(response['data'][0]['url'])
b64_data = response['data'][0]['b64_json']

image_data = b64decode(b64_data)

with open('./ferrari.png', mode='wb') as png:
    png.write(image_data)