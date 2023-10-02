import time
from dreamlike_diffusion_image_gen import generate_dreamlike_image
from dalle2_image_gen import generate_dalle_image
import pandas as pd
import torch

def generate_images_for_songs(csv_file):
    df_playlist = pd.read_csv(csv_file, sep=';')
    print(df_playlist)

    is_cuda_or_mps_available = torch.cuda.is_available() or torch.backends.mps.is_available()

    image_file_path = list()

    response_str = '다음 곡의 이미지를 생성했습니다. '

    for i, row in df_playlist.iterrows():
        if row['mp3'] == 'Not found':
            image_file_path.append(None)
            response_str += f"\n{row['Title']} - {row['Artist']}: 음원이 없어서 이미지를 생성하지 않았습니다. "
        else:
            if is_cuda_or_mps_available:
                image_file = generate_dreamlike_image(row['Title'], row['Artist'])
            else:
                try:
                    image_file = generate_dalle_image(row['Title'], row['Artist'])
                except:
                    print('Something went to wrong...')
                    image_file = None
                time.sleep(5)

            image_file_path.append(image_file)
            response_str += f"\n{row['Title']} - {row['Artist']}: 이미지 생성 성공! {image_file}"

    df_playlist['image_file'] = image_file_path
    df_playlist.to_csv(csv_file, sep=';', index=False, lineterminator='\n')

    return response_str

if __name__ == '__main__':
    # csv_file = "./playlist/80년대_한국록음악.csv"
    csv_file = "./playlist/댄스음악.csv"
    result = generate_images_for_songs(csv_file)
    print('--------------------')
    print(result)

            