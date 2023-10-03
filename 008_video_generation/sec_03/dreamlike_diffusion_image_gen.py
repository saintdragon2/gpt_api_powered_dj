import re
import openai
from api_keys import openai_api_key

from diffusers import StableDiffusionPipeline
import torch

openai.api_key = openai_api_key

def text_to_image_prompt_generator(song_title, artist):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0.5,
        messages=[
            {'role': 'system', 'content': 'You are an AI assistant designed to generate prompts for a text-to-image model. When a user provides the title and artist of a song, you need to summarize the song lyrics in one sentence in English and indicate the genre and mood.'},
            {'role': 'user', 'content': f'{song_title} - {artist}'},
        ]
    )

    return response.choices[0].message.content


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

def generate_dreamlike_image(song_title, artist):
    model_id = "dreamlike-art/dreamlike-diffusion-1.0"

    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")

    # prompt = "dreamlikeart, A rich man driving Ferrari in New York and many people are watching him, In style of by Jordan Grimmer and greg rutkowski, crisp lines and color, complex background, particles, lines, wind, concept art, sharp focus, vivid colors"
    about = text_to_image_prompt_generator(song_title, artist)
    print(about)


    prompt = f"dreamlikeart, {about}, In style of by Jordan Grimmer and greg rutkowski, crisp lines and color, complex background, particles, lines, wind, concept art, sharp focus."
    image = pipe(prompt).images[0]

    file_name = sanitize_filename(f'{song_title}__{artist}')
    file_name = './dreamlike_diffusion/' + file_name + '.jpg'

    image.save(file_name)

    return file_name


if __name__ == '__main__':
    generate_dreamlike_image('Gravity', 'John Mayer')

