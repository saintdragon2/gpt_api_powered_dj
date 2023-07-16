import re
import openai
from diffusers import StableDiffusionPipeline
import torch

openai.api_key = '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'  # OpenAI API 키 설정

def text_to_image_prompt_generator(song_title, artist):
    # GPT-3.5 Turbo 모델에 메시지를 보내 응답을 받는 함수
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',  # 사용할 모델 선택
        temperature=0.1,  # 출력 다양성 조절을 위한 옵션
        messages=[
            {"role": "system", "content": "You are an AI assistant desinged to generate prompts for text-to-image models. When a user provides a song title and artist, you should summarize the song's lyrics in English in a sentence, and indicate its genre and mood."},
            {"role": "user", "content": f'{song_title} - {artist}'}
        ]
    )
    return response.choices[0].message.content  # 응답 중 첫 번째 응답의 내용 반환

def sanitize_filename(filename):
    # 정규식 패턴을 사용하여 오류를 발생시킬 수 있는 문자와 띄어쓰기를 찾아 언더바로 대체합니다.
    sanitized_filename = re.sub(r'[^\w\s-]', '', filename)
    sanitized_filename = re.sub(r'[\s]+', '_', sanitized_filename)
    
    return sanitized_filename


def generate_dreamlike_image(song_title, artist):
    model_id = "dreamlike-art/dreamlike-diffusion-1.0"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")

    about = text_to_image_prompt_generator(song_title, artist)
    print(about)

    
    negative_prompt = '''
    text, deformed, ugly, additional arms, additional legs, additional head, two heads
    '''

    prompt = f"dreamlikeart, {about}, dramatic lighting, illustration by greg rutkowski, yoji shinkawa, concept art, trending on artstation, digital art"
    image = pipe(prompt=prompt, negative_prompt=negative_prompt).images[0]


    file_name = f'{song_title}_{artist}'
    file_name = sanitize_filename(file_name)
    
    file_path = f"./dreamlike_diffusion/{file_name}.jpg"
    image.save(file_path)

    return file_path


if __name__=='__main__':
    # response = generate_dreamlike_image('강남스타일', 'PSY')
    # print(response)
    result = generate_dreamlike_image('Beat It', 'Michael Jackson')
    print(result)