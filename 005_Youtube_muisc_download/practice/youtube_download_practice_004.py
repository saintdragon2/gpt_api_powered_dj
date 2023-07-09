import pandas as pd
from youtube_search import YoutubeSearch
import yt_dlp
import re

# 유투브에서 5개 검색하고 일치하는 영상 찾기

# 유투브에서 검색된 제목이 연관이 있는지 판단
def is_relevent_video_title(video_title, song_title, song_artist, threshold=0.5):
    video_title = video_title.lower()
    song_title = song_title.lower()
    song_artist = song_artist.lower()

    title_words = song_title.split()
    artist_words = song_artist.split()
    
    title_matches = sum([word in video_title for word in title_words])
    artist_matches = sum([word in video_title for word in artist_words])
    
    return title_matches >= len(title_words) * threshold and artist_matches >= len(artist_words) * threshold

def sanitize_filename(filename):
    # 정규식 패턴을 사용하여 오류를 발생시킬 수 있는 문자와 띄어쓰기를 찾아 언더바로 대체합니다.
    sanitized_filename = re.sub(r'[^\w\s-]', '', filename)
    sanitized_filename = re.sub(r'[\s]+', '_', sanitized_filename)
    
    return sanitized_filename

def download_song(title, artist):
    # 유튜브에서 검색어 조합하기
    query = f"{title} {artist} official audio"
    
    # 검색어로 유튜브 검색
    search_results = YoutubeSearch(query, max_results=5).to_dict()

    file_name = sanitize_filename(f'{title}__{artist}')

    if len(search_results) == 0:
        print(f"검색 결과 없음: {title} - {artist}")
        return None
    
    for searched in search_results:
        video_id = searched['id']
        searched_title = searched['title']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # 제목이 맞는지 판단
        if is_relevent_video_title(searched_title, title, artist):
            # YouTube 영상 다운로드
            try:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': f'./music_files/{file_name}.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '320',
                    }],
                    'ffmpeg_location': './ffmpeg-2023-07-06-git-f00222e81f-full_build/bin'
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                
                print(f"다운로드 완료: {title} - {artist}")
                return f'./music_files/{file_name}.mp3'
            except:
                print(f"다운로드 실패: {title} - {artist}")
        else:
            print(f"검색된 제목과 입력된 제목이 일치하지 않습니다: {searched_title} vs {title}")        
    
    return None


def download_songs_in_csv(file_path):
    # CSV 파일 열기
    df = pd.read_csv(file_path, delimiter=';')
    
    mp3_files = list()

    # YouTube에서 검색하여 첫 번째 영상의 음원을 다운로드
    for _, row in df.iterrows():
        title = row['Title']
        artist = row['Artist']
        
        mp3_file_path = download_song(title, artist)
        mp3_files.append(mp3_file_path)
    
    df['mp3_file'] = mp3_files
    df['mp3_file'].fillna('Not Found', inplace=True)
    df.to_csv(file_path, sep=';', index=False)

if __name__ == '__main__':
    # CSV 파일 경로
    file_path = 'playlist/2010s_hiphop.csv'

    download_songs_in_csv(file_path)

