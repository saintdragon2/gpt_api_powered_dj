import openai
from api_keys import openai_api_key
from base64 import b64decode

openai.api_key = openai_api_key

def text_to_image_prompt_generator(song_title, artist):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0.5,
        messages=[
            {
                'role': 'system', 
                'content': """
                You are an AI assistant designed to create DALL·E-2 prompts.

                When the user provides information about a song, imagine the song's lyrics and the representative image of its mood.
                Based on the imagined image, generate a text prompt for the text-to-image model, DALL·E-2.
                """
            },
            {'role': 'user', 'content': 'Stronger - Kelly Clarkson'},
            {'role': 'assistant', 'content': 'Create an image of a person standing on top of a mountain, surrounded by vibrant rays of sunlight, radiating confidence and strength.'},
            {'role': 'user', 'content': f'{song_title} - {artist}'},
        ]
    )

    return response.choices[0].message.content

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
    song_title = 'Billie Jean'
    artist = 'Michael Jackson'

    prompt = text_to_image_prompt_generator(song_title, artist)
    print(prompt)
    result = generate_dalle_image(
        'Create a Photo. ' + prompt,
        'yesterday_beatles'
    )

    print(result)