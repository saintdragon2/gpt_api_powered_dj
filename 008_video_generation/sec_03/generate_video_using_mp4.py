from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips, TextClip, CompositeVideoClip
import pandas as pd
import os


def create_text_clip(text, fontsize, duration, position, start):
    text_clip = TextClip(text, fontsize=fontsize, color='white', font='Malgun-Gothic-Bold')
    text_clip = text_clip.set_position(position).set_duration(duration).set_start(start)

    return text_clip


def combine_videos_and_music(mp3_files, video_files, titles, artists, output_file):
    # MP3 파일의 재생 시간을 계산하여 플레이리스트의 총 길이를 구합니다.
    audio_clips = [AudioFileClip(mp3_file) for mp3_file in mp3_files]
    final_audio = concatenate_audioclips(audio_clips)
    playlist_duration = final_audio.duration 

    # 비디오 파일을 연결합니다.
    video_clips = [VideoFileClip(video_file) for video_file in video_files]
    final_video = concatenate_videoclips(video_clips, method="compose")

    # 비디오의 길이를 얻습니다.
    video_duration = final_video.duration

    # 비디오의 길이가 플레이리스트의 총 길이보다 짧으면 비디오를 반복재생합니다.
    while video_duration < playlist_duration:
        final_video = concatenate_videoclips([final_video, final_video], method="compose")
        video_duration = final_video.duration

    # 비디오의 길이가 플레이리스트의 총 길이보다 길면 비디오를 자릅니다.
    if video_duration > playlist_duration:
        final_video = final_video.subclip(0, playlist_duration)

    # MP3 파일을 비디오에 추가합니다.
    final_video = final_video.set_audio(final_audio)

    # 테스트 할 때만 빠른 렌더링을 위해 사용 (실제 사용시 주석처리!)
    final_video = final_video.resize(height=180)

    start_time = 0
    text_clips = list()

    video_width, video_height = final_video.size
    title_fontsize = int(video_height * 0.05)
    artist_fontsize = int(title_fontsize * 0.8)
    left_margin = title_fontsize
    title_y = int(video_height * 0.7)
    artist_y = int(title_y + title_fontsize * 1.2)

    for i, audio_clip in enumerate(audio_clips):
        title = titles[i]
        artist = artists[i]
        title_text_clip = create_text_clip(title, title_fontsize, audio_clip.duration, (left_margin, title_y), start_time)
        artist_text_clip = create_text_clip(artist, artist_fontsize, audio_clip.duration, (left_margin, artist_y), start_time)

        text_clips.append([title_text_clip, artist_text_clip])

        start_time += audio_clip.duration

    composite_clips = [final_video]
    for text_group in text_clips:
        for text in text_group:
            composite_clips.append(text)

    final_video = CompositeVideoClip(composite_clips)


    # 최종 비디오를 저장합니다. fps는 frame per second 이므로, 실제 사용시에는 60으로 설정하거나, 없애주세요.
    final_video.write_videofile(output_file, audio_codec='aac', fps=1)

    # 임시 오디오 파일을 삭제합니다.
    if os.path.exists("temp-audio.m4a"):
        os.remove("temp-audio.m4a")

    return output_file

def generate_video_using_mp4(csv_file, video_files):
    df_playlist = pd.read_csv(csv_file, sep=';')
    # mp3가 없는 경우 (Not found), 해당 행을 삭제
    df_playlist = df_playlist.loc[df_playlist['mp3'] != 'Not found']
    # index를 다시 설정
    df_playlist.reset_index(inplace=True)
    # reset_index를 하면, df_playlist에 새로운 'index' 컬럼이 생기므로, 그 컬럼을 삭제
    df_playlist.drop(columns=['index'], inplace=True)
    print(df_playlist)

    mp3_files = df_playlist['mp3']
    titles = df_playlist['Title']
    artists = df_playlist['Artist']

    dir, csv_file_full_name = os.path.split(csv_file)
    file_name, ext = os.path.splitext(csv_file_full_name)

    output_file = f"./videos/{file_name}.mp4"

    output_result = combine_videos_and_music(mp3_files, video_files, titles, artists, output_file)
    return f'MP4 파일을 이용해 플레이리스트 동영상 생성에 성공했습니다. \n {output_result}'

if __name__ == '__main__':
    video_files = [
        "./videos/raw_video/DJI_20230502091254_0073_D_1000_1080.MP4", 
        "./videos/raw_video/DJI_20230502091254_0073_D_1015_1080.MP4"
    ]


    csv_file = './playlist/댄스음악3.csv'
    
    result = generate_video_using_mp4(csv_file, video_files)
