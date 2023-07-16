from base64 import b64decode
from pathlib import Path
import openai

def generate_dalle_image(prompt, image_file_name):
    openai.api_key = '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'  # OpenAI API 키 설정

    PROMPT = prompt #'Ferrari is crusing throught the big city in the night'
    DATA_DIR = Path.cwd() / 'dalle2_results'
    DATA_DIR.mkdir(exist_ok=True)
    print(DATA_DIR)

    response = openai.Image.create(
        prompt=PROMPT,
        n=1,
        size='512x512',
        response_format='b64_json'
    )

    file_name = DATA_DIR / f"dalle2-{response['created']}.json"

    b64_data = response['data'][0]['b64_json']
    image_data = b64decode(b64_data)

    image_file = DATA_DIR / f'{image_file_name}.png'

    # with open(file_name, mode='w', encoding='UTF-8') as file:
    #     json.dump(response, file)

    with open(image_file, mode='wb') as png:
        png.write(image_data)


if __name__ == '__main__':
    generate_dalle_image('A man is dancing in the night in the middle of Gangnam, Seoul.', 'dancing_man')