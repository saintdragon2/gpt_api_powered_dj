import openai
from api_keys import openai_api_key
from base64 import b64decode
import re

openai.api_key = openai_api_key


def sanitize_filename(filename):
    # 허용되지 않는 문자를 밑줄(_)로 대체합니다.
    filename = re.sub(r'[\/:*?"<>|]', '_', filename)

    # 띄어쓰기도 언더바(_)로 대체합니다.
    filename = re.sub(r'\s+', '_', filename)

    # 여러 개의 연속된 밑줄을 하나로 줄입니다.
    filename = re.sub(r'_+', '_', filename)

    # 파일명의 앞뒤 공백을 제거합니다.
    filename = filename.strip()

    return filename

def text_to_image_prompt_generator(song_title, artist):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0.5,
        messages=[
            {
                'role': 'system', 
                'content': """
                You are an AI assistant designed to generate DALL·E-2 prompts.

                - When the user provides information about a song, imagine the lyrics and an image representing the mood.
                - Based on the imagined image, create a text prompt for the text-to-image model, DALL·E-2.
                - Be cautious not to mention the names of famous individuals or artists of the songs.
                - Avoid using words like 'gangster' or 'drug.'
                - Avoid making racially discriminatory remarks.
                - Modify any violent or sexual content that is not suitable for children under the age of 15 to be expressed in a milder manner.
                """
            },
            {'role': 'user', 'content': 'Stronger - Kelly Clarkson'},
            {'role': 'assistant', 'content': 'Create an image of a person standing on top of a mountain, surrounded by vibrant rays of sunlight, radiating confidence and strength.'},
            {'role': 'user', 'content': f'{song_title} - {artist}'},
        ]
    )

    return response.choices[0].message.content

def generate_dalle_image(song_title, artist, size="512x512"):
    prompt = text_to_image_prompt_generator(song_title, artist)
    print('---------------!')
    print(prompt)
    print('---------------')

    prompt = 'Create a Photo. ' + prompt 

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size=size,
        response_format='b64_json'
    )
    b64_data = response['data'][0]['b64_json']

    image_data = b64decode(b64_data)

    image_file_name = sanitize_filename(f'{song_title}_{artist}')

    img_file = f'./dalle2_images/{image_file_name}.png'

    with open(img_file, mode='wb') as png:
        png.write(image_data)

    return img_file


if __name__ == '__main__':
    song_title = 'Billie Jean'
    artist = 'Michael Jackson'
    
    result = generate_dalle_image(song_title, artist)

    print(result)