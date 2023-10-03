from moviepy.editor import *
import pandas as pd
import os 

def create_video(mp3_path, image_path):
    # 이미지를 불러오고 크기를 조정합니다.
    image = ImageClip(image_path)
    image = image.set_duration(AudioFileClip(mp3_path).duration)  # 동영상 길이와 맞춥니다.

    # mp3 파일을 불러옵니다.
    audio = AudioFileClip(mp3_path)

    # 이미지와 오디오를 조합하여 동영상을 만듭니다.
    video = image.set_audio(audio)

    dir, image_file_full_name = os.path.split(image_path)
    file_name, ext = os.path.splitext(image_file_full_name)

    print(image_file_full_name)
    print(file_name)
    print(ext)

    # 동영상을 저장합니다.
    output_path = f"./videos/{file_name}.mp4"  # 원하는 경로와 파일명으로 변경 가능
    video.write_videofile(output_path, codec='libx264', fps=24)

    return output_path

def create_videos_from_playlist_csv(csv_file):
    df_playlist = pd.read_csv(csv_file, sep=';')

    videos = list()

    for i, row in df_playlist.iterrows():
        if row['mp3'] != 'Not found':
            video = create_video(row['mp3'], row['info_image_file'])
            videos.append(video)
    
    return videos

def combine_videos(video_paths, output_path):
    clips = [VideoFileClip(video_path) for video_path in video_paths]

    # 동영상을 연결하여 하나의 큰 동영상으로 만듭니다.
    final_video = concatenate_videoclips(clips)

    # 합쳐진 동영상을 저장합니다.
    final_video.write_videofile(output_path, codec='libx264')

    return output_path

def generate_video_using_images(csv_file):
    video_paths = create_videos_from_playlist_csv(csv_file)

    dir, csv_file_full_name = os.path.split(csv_file)
    file_name, ext = os.path.splitext(csv_file_full_name)

    output_video_path = f"./videos/{file_name}.mp4"
    combine_videos(video_paths, output_video_path)
    print("동영상이 합쳐졌습니다:", output_video_path)

    return f"동영상이 생성되었습니다. 파일 경로는 다음과 같습니다. \n {output_video_path}"

if __name__ == '__main__':
    result_str = generate_video_using_images("./playlist/댄스음악.csv")

    print(result_str)