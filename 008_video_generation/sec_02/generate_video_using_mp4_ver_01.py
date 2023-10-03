from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips
import subprocess
import os


def combine_videos_and_music(mp3_files, video_files, output_file):
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


    # final_video = final_video.resize(height=360)
    # 최종 비디오를 저장합니다.
    print('save video')
    final_video.write_videofile(output_file, fps=5)

    # 임시 오디오 파일을 삭제합니다.
    if os.path.exists("temp-audio.m4a"):
        os.remove("temp-audio.m4a")


if __name__ == '__main__':
    # 예시 사용법:
    mp3_files = [
        "./mp3/Uptown_Funk-Mark_Ronson_ft._Bruno_Mars.mp3", 
        "./mp3/Kill_This_Love-블랙핑크.mp3"
    ]
    video_files = [
        "./videos/raw_video/DJI_20230502091254_0073_D_1000_1080.MP4", 
        "./videos/raw_video/DJI_20230502091254_0073_D_1015_1080.MP4"
    ]
    output_file = "output_video2.mp4"
    combine_videos_and_music(mp3_files, video_files, output_file)
