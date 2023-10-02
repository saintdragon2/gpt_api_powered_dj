import pandas as pd
from youtube_search import YoutubeSearch
import yt_dlp

def download_song(title, artist):
    query = f"{title} {artist} audio"

    # YouTube에서 검색
    videos_search = YoutubeSearch(query, max_results=1)
    results = videos_search.to_dict()

    if len(results) > 0:
        video_url = f"https://www.youtube.com{results[0]['url_suffix']}"

        # yt-dlp 설정
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'ffmpeg_location': 'C:/github/gpt_api_powered_dj/ffmpeg-2023-09-29-full_build/bin',
            'outtmpl': f'{title} - {artist}.%(ext)s'
        }

        # 음원 다운로드
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        print(f"다운로드 완료: {title} - {artist}")
    else:
        print(f"검색 결과 없음: {title} - {artist}")

def download_music_from_youtube(csv_file):
    # CSV 파일 읽기
    df = pd.read_csv(csv_file, delimiter=';', encoding='UTF-8')

    # YouTube 검색 및 음원 다운로드
    for index, row in df.iterrows():
        title = row['Title']
        artist = row['Artist']

        download_song(title, artist)
        


# CSV 파일 경로 지정
csv_file = './playlist/댄스음악.csv'

# 함수 호출
download_music_from_youtube(csv_file)
