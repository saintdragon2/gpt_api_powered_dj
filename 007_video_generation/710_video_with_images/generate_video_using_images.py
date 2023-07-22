from moviepy.editor import *
import pandas as pd


def create_video(mp3_path, img_path):
    # 오디오 파일 로드
    audioclip = AudioFileClip(mp3_path)

    # 이미지 로드
    imgclip = ImageClip(img_path, duration=audioclip.duration)

    # 오디오와 이미지 합성
    videoclip = imgclip.set_audio(audioclip)

    # 출력 파일 경로 설정
    dir, file_full_name = os.path.split(img_path)
    file_name, ext = os.path.splitext(file_full_name)

    output_path = f"./videos/{file_name}.mp4"

    # 동영상 파일 쓰기
    videoclip.write_videofile(output_path, fps=24)

    # 생성된 동영상 파일 경로 반환
    return output_path


def create_videos_from_playlist_csv(csv_file_path):
    df_playlist = pd.read_csv(csv_file_path, sep=';')

    videos = list()
    for i, row in df_playlist.iterrows():
        if row['mp3_file'] != 'Not Found':
            video = create_video(row['mp3_file'], row['info_image_file'])
            videos.append(video)
    return videos

def concatenate_videos(video_paths, output_path):
    clips = []
    for path in video_paths:
        clips.append(VideoFileClip(path))
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path, fps=24)


def generate_video_using_images(csv_file_path):
    videos = create_videos_from_playlist_csv(csv_file_path)

    dir, file_full_name = os.path.split(csv_file_path)
    file_name, ext = os.path.splitext(file_full_name)
    video_file_path = f"./videos/{file_name}.mp4"

    concatenate_videos(videos, video_file_path)

    return video_file_path

if __name__ == '__main__':
    # video_path = create_video(
    #     './music_files/Happy__Pharrell_Williams.mp3',
    #     './dreamlike_diffusion/Happy_Pharrell_Williams_info.jpg'
    # )

    csv_file_path = 'playlist/coffee_pop.csv'
    # videos = create_videos_from_playlist_csv(csv_file_path)

    video_path = generate_video_using_images(csv_file_path)
    print(video_path)