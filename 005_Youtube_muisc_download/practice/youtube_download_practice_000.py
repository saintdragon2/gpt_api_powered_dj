# CSV 파일을 pandas로 열어서, 
# Title, Artist 정보로 유투브에서 검색한 뒤, 
# 첫번째 영상의 음원을 다운로드 받고 싶다. 
import pandas as pd
from youtube_search import YoutubeSearch
import yt_dlp

# CSV 파일 경로
csv_path = 'playlist\summer.csv'

# CSV 파일 열기
df = pd.read_csv(csv_path, delimiter=';')

# YouTube에서 검색하여 첫 번째 영상의 음원을 다운로드
for _, row in df.iterrows():
    title = row['Title']
    artist = row['Artist']
    
    # 유튜브에서 검색어 조합하기
    query = f"{title} {artist} official audio"
    
    # 검색어로 유튜브 검색
    results = YoutubeSearch(query, max_results=1).to_dict()
    
    if results:
        video_id = results[0]['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # YouTube 영상 다운로드
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': './music_files/%(title)s.%(ext)s',
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
        except:
            print(f"다운로드 실패: {title} - {artist}")
    else:
        print(f"검색 결과 없음: {title} - {artist}")
