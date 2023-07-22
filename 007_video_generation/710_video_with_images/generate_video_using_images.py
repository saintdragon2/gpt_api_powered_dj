from moviepy.editor import *

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


if __name__ == '__main__':
    video_path = create_video(
        './music_files/Happy__Pharrell_Williams.mp3',
        './dreamlike_diffusion/Happy_Pharrell_Williams_info.jpg'
    )