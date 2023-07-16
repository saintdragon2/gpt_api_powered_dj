from base64 import b64decode
from pathlib import Path
import re
import openai

openai.api_key = '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'  # OpenAI API 키 설정

def dalle2_prompt_generator(song_title, artist):
    # GPT-3.5 Turbo 모델에 메시지를 보내 응답을 받는 함수
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',  # 사용할 모델 선택
        temperature=0.1,  # 출력 다양성 조절을 위한 옵션
        messages=[
            {"role": "system", 
             "content": """
                You are an AI assistant desinged to generate prompts for Dalle-2. 
                When a user provides a information about song, envision an image that reprents the song's lyrics, genre and mood.
                Based on the image you've envisioned, generate a Dalle-2 prompt in a sentence, avoiding crime-related words such as gangs or drugs.
                If the prompt contains any violent or sexual expressions that are not suitable for a 12-year-old child to hear, present them in a more subdued manner.
                Refrrain from mentioning any famous persons' name or the artist of the song.
            """
            },
            {"role": "user", "content": "Beat It - Michael Jackson"},
            {"role": "assistant", "content": "In a bustling city under the shimmering lights, a diverse group of individuals joyfully dance together, embracing their differences and spreading a message of harmony and resilience."},
            {"role": "user", "content": "Stronger - Kelly Clarkson"}, 
            {"role": "assistant", "content": "In a world full of challenges, a person finds the strength within to rise above adversity and embrace their true potential. They discover that every setback is an opportunity for growth and transformation, becoming a beacon of inspiration for others."},
            {"role": "user", "content": f'{song_title} - {artist}'},
        ]
    )
    return response.choices[0].message.content  # 응답 중 첫 번째 응답의 내용 반환

def sanitize_filename(filename):
    # 정규식 패턴을 사용하여 오류를 발생시킬 수 있는 문자와 띄어쓰기를 찾아 언더바로 대체합니다.
    sanitized_filename = re.sub(r'[^\w\s-]', '', filename)
    sanitized_filename = re.sub(r'[\s]+', '_', sanitized_filename)
    
    return sanitized_filename

def generate_dalle_image(song_title, artist):
    openai.api_key = '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'  # OpenAI API 키 설정

    prompt = dalle2_prompt_generator(song_title, artist)
    print(prompt)

    DATA_DIR = Path.cwd() / 'dalle2_results'
    DATA_DIR.mkdir(exist_ok=True)
    print(DATA_DIR)

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size='512x512',
        response_format='b64_json'
    )


    b64_data = response['data'][0]['b64_json']
    image_data = b64decode(b64_data)

    file_name = f'{song_title}_{artist}'
    file_name = sanitize_filename(file_name)

    image_file = DATA_DIR / f'{file_name}.png'

    # with open(file_name, mode='w', encoding='UTF-8') as file:
    #     json.dump(response, file)

    with open(image_file, mode='wb') as png:
        png.write(image_data)

    return image_file


if __name__ == '__main__':
    # img_file = generate_dalle_image("One Kiss", 'Dua Lipa')
    img_file = generate_dalle_image("When I was your man", 'Bruno Mars')
    print(img_file)
    

