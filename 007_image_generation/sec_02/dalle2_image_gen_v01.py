import openai
from api_keys import openai_api_key
from base64 import b64decode

openai.api_key = openai_api_key

def generate_dalle_image(prompt, image_file_name, size="512x512"):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size=size,
        response_format='b64_json'
    )
    b64_data = response['data'][0]['b64_json']

    image_data = b64decode(b64_data)

    img_file = f'./dalle2_images/{image_file_name}.png'

    with open(img_file, mode='wb') as png:
        png.write(image_data)

    return img_file


if __name__ == '__main__':
    result = generate_dalle_image(
        'A man is dancing with his wife',
        'dancing_couple'
    )

    print(result)