import pandas as pd
from youtube_search import YoutubeSearch
import yt_dlp     
import re

# 곡 제목과 아티스트명으로 검증 후 mp3 내려받기

def is_relevant_video_title(video_title, song_title, song_artist):
    video_title = video_title.lower()
    song_title = song_title.lower()
    song_artist = song_artist.lower()

    title_words = song_title.split()
    artist_words = song_artist.split()

    title_matches = sum([word in video_title for word in title_words])
    artist_mathces = sum([word in video_title for word in artist_words])

    return title_matches >= len(title_words) * 0.5 and artist_mathces >= len(artist_words) * 0.5


def sanitize_filename(filename):
    # 허용되지 않는 문자를 밑줄(_)로 대체합니다.
    filename = re.sub(r'[\/:*?"<>|]', '_', filename)

    # 띄어쓰기도 언더바(_)로 대체합니다.
    filename = re.sub(r'\s+', '_', filename)

    # 여러 개의 연속된 밑줄을 하나로 줄입니다.
    filename = re.sub(r'_+', '_', filename)

    # 파일명의 앞뒤 공백을 제거합니다.
    filename = filename.strip()

    return filename

def download_song(title, artist):
    query = f"{title} {artist} audio"

    file_name = sanitize_filename(f'{title}-{artist}')

    # YouTube에서 검색
    videos_search = YoutubeSearch(query, max_results=5)
    results = videos_search.to_dict()

    for searched in results:
        video = searched
        video_title = video['title']

        if is_relevant_video_title(video_title, title, artist):

            video_url = f"https://www.youtube.com{searched['url_suffix']}"

            # yt-dlp 설정
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
                'ffmpeg_location': 'C:/github/gpt_api_powered_dj/ffmpeg-2023-09-29-full_build/bin',
                'outtmpl': f'./mp3/{file_name}.%(ext)s'
            }

            # 음원 다운로드
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            print(f"다운로드 완료: {title} - {artist}")

            return f'./mp3/{file_name}.mp3'
    else:
        print(f"검색 결과 없음: {title} - {artist}")
    
    return None

def download_music_from_youtube(csv_file):
    # CSV 파일 읽기
    df = pd.read_csv(csv_file, delimiter=';', encoding='UTF-8')

    mp3s = []
    # YouTube 검색 및 음원 다운로드
    for index, row in df.iterrows():
        title = row['Title']
        artist = row['Artist']

        mp3_file_path = download_song(title, artist)
        mp3s.append(mp3_file_path)
    
    df['mp3'] = mp3s
    df = df.fillna('None')
    print(df)

    df.to_csv(csv_file, index=False, encoding='UTF-8', sep=';')
        

if __name__ == '__main__':
    # CSV 파일 경로 지정
    csv_file = './playlist/80년대_한국록음악.csv'

    # 함수 호출
    download_music_from_youtube(csv_file)
