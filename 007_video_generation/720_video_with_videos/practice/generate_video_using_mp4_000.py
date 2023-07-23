import moviepy.editor as mp
import pandas as pd
from glob import glob

def combine_videos_and_music(mp3_files, video_files):
    # 영상 파일을 합치기
    video_clips = [mp.VideoFileClip(video_file) for video_file in video_files]
    concat_video = mp.concatenate_videoclips(video_clips)

    # 음악 파일을 합치기
    audio_clips = [mp.AudioFileClip(mp3_file) for mp3_file in mp3_files]
    concat_audio = mp.concatenate_audioclips(audio_clips)

    # 하나로 합친 동영상의 길이와 플레이리스트 길이 비교
    video_duration = concat_video.duration
    audio_duration = concat_audio.duration

    if video_duration > audio_duration:
        concat_video = concat_video.subclip(0, audio_duration)
    while video_duration < audio_duration:
        remainder = audio_duration - video_duration
        if remainder > video_duration:
            remainder = video_duration
        extra_video = concat_video.subclip(0, remainder)
        concat_video = mp.concatenate_videoclips([concat_video, extra_video])
        
        video_duration = concat_video.duration

    # 영상의 소리를 없애고 플레이리스트로 대체
    concat_video = concat_video.set_audio(concat_audio)

    # 결과 저장
    output_filename = "combined_video.mp4"
    # concat_video = concat_video.resize(height=360)
    # concat_video.write_videofile(output_filename, fps=20)
    concat_video.write_videofile(output_filename)

    return output_filename


if __name__ == '__main__':
    df = pd.read_csv('playlist/coffee_pop.csv', sep=';')

    mp3_files = df['mp3_file'].to_list()
    video_files = list()

    for g in glob('./raw_video/p1080/*.MP4')[:10]:
        video_files.append(g)
    
    combine_videos_and_music(
        mp3_files,
        video_files
    )