import tkinter as tk
from tkinter import scrolledtext  # Tkinter 모듈을 가져옴
import openai  # OpenAI API와 상호 작용하기 위한 모듈
import tkinter.filedialog as filedialog
import pandas as pd
from youtube_download_audio import download_songs_in_csv
from generate_image import generate_images_for_songs
from generate_video_using_images import generate_video_using_images
from generate_video_using_mp4 import generate_video_using_mp4

openai.api_key = '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'  # OpenAI API 키 설정

# CSV 저장이 더 잘 되도록 예시 명시하기.

def ask_to_gpt_35_turbo(messages):
    # GPT-3.5 Turbo 모델에 메시지를 보내 응답을 받는 함수
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',  # 사용할 모델 선택
        temperature=0.1,  # 출력 다양성 조절을 위한 옵션
        messages=messages  # 이전 메시지와 사용자 입력을 포함하는 메시지 목록
    )
    return response.choices[0].message.content  # 응답 중 첫 번째 응답의 내용 반환


def save_dataframe_to_csv(dataframe):
    filename = filedialog.asksaveasfilename(defaultextension=".csv")
    if filename:
        dataframe.to_csv(filename, sep=';', index=False)
        return f'파일을 저장했습니다. 저장 경로는 다음과 같습니다. \n {filename} \n 이 플레이리스트의 음원을 다운로드 하시겠습니까?', filename
    return '저장을 취소했습니다.', None


def extract_csv_to_dataframe(response):
    lines = response.strip().split('\n')
    csv_lines = [line for line in lines if ';' in line]

    csv_data = list()
    if csv_lines:
        for line in csv_lines[1:]:
            csv_data.append(line.split(';'))
    
    if len(csv_data) > 0:
        df = pd.DataFrame(csv_data, columns=csv_lines[0].split(';'))
        df['Title'] = df['Title'].apply(lambda x: x.strip())
        return df

    return None

def main():
    def on_send():
        user_input = user_entry.get()  # 입력 필드에서 사용자 입력을 가져옴

        if user_input.lower() == 'quit':  # 사용자가 'quit'를 입력하면 프로그램 종료
            window.destroy()
            return

        messages.append(
            {'role': 'user', 'content': user_input},  # 사용자 메시지를 메시지 목록에 추가
        )

        conversation.config(state=tk.NORMAL)  # 채팅 히스토리 텍스트 상태를 편집 가능한 상태로 변경
        conversation.insert(tk.END, 'You: ' + user_input + '\n', 'user')  # 사용자 입력을 채팅 히스토리에 추가
        window.update_idletasks()

        thinking_popup = show_popup_message(window, '생각 중...')
        
        response = ask_to_gpt_35_turbo(messages)  # 메시지 목록을 GPT-3.5 Turbo 모델에 전달하여 응답 받음
        
        # Extract CSV content to pandas DataFrame
        dataframe = extract_csv_to_dataframe(response)
        if dataframe is not None:
            thinking_popup.destroy()
            
            global csv_file_path
            file_save_result, csv_file_path = save_dataframe_to_csv(dataframe)
            print(file_save_result)
            if '음원을 다운로드합니다!' in response or 'DOWNLOAD_MP3' in response:
                response = response.replace('음원을 다운로드합니다!', '')
                response = response.replace('DOWNLOAD_MP3', '')
                print('불필요한 동작 방지!!!')

            if file_save_result == '저장을 취소했습니다.':
                response = file_save_result + '\n저장이 되지 않았습니다.'
            else:
                response += "\n" + file_save_result 

        if '음원을 다운로드합니다!' in response or 'DOWNLOAD_MP3' in response:
            print(response)
            mp3_download_result = download_songs_in_csv(csv_file_path)
            for k, mp3_path in mp3_download_result.items():
                if mp3_path != 'Not found':
                    response += f'\n{k}\t다운로드 성공했습니다. {mp3_path}'
                else:
                    response += f'\n{k}\t일치하는 곡을 찾지 못했습니다. '
            response += '\n\n 곡에 어울리는 이미지를 생성하시겠습니까?'

        if '이미지를 생성합니다!' in response or 'GENERATE_IMAGES' in response:
            print(response)
            response = generate_images_for_songs(csv_file_path)
            response += '\n\n플레이리스트 영상을 생성하시겠습니까? 이미지를 이용하거나 동영상을 이용해 플레이리스트 영상을 만들 수 있습니다.'

        if '이미지를 이용해 플레이리스트 영상을 생성합니다' in response or 'GENERATE_PLAYLIST_VIDEO_USING_IMAGES' in response:
            print(response)
            video_file_path = generate_video_using_images(csv_file_path)
            response = f'아래 경로에 이미지를 이용한 플레이리스트 영상을 저장했습니다. \n {video_file_path}'

        if '동영상을 이용해 플레이리스트 영상을 생성합니다' in response or 'GENERATE_PLAYLIST_VIDEO_USING_VIDEOS' in response:
            print(response)
            video_files = list()
            from glob import glob
            for g in glob('./raw_video/p1080/*.MP4')[:10]:
                video_files.append(g)
            video_file_path = generate_video_using_mp4(csv_file_path, video_files)
            response = f'아래 경로에 동영상을 이용한 플레이리스트 영상을 저장했습니다. \n {video_file_path}'

        
        if thinking_popup:
            thinking_popup.destroy()
        
        messages.append(
            {'role': 'assistant', 'content': response},  # 응답을 메시지 목록에 추가
        )

        conversation.insert(tk.END, 'Assistant: ' + response + '\n', 'assistant')  # 응답을 채팅 히스토리에 추가
        conversation.config(state=tk.DISABLED)  # 채팅 히스토리 텍스트 상태를 읽기 전용 상태로 변경
        conversation.see(tk.END)  # 채팅 히스토리 스크롤을 맨 아래로 이동

        user_entry.delete(0, tk.END)  # 입력 필드를 비움

    def show_popup_message(window, message):
        popup = tk.Toplevel(window)
        popup.title('GPT-3.5')

        label = tk.Label(popup, text=message)
        label.pack(expand=True, fill=tk.BOTH)

        popup_width = 400
        popup_height = 100

        popup.geometry(f'{popup_width}x{popup_height}')

        # 팝업 창 중앙 위치
        window_x = window.winfo_x()
        window_y = window.winfo_y()
        window_width = window.winfo_width()
        window_height = window.winfo_height()

        popup_x = window_x + window_width // 2 - popup_width // 2
        popup_y = window_y + window_height // 2 - popup_height // 2
        popup.geometry(f'+{popup_x}+{popup_y}')

        popup.transient(window)
        popup.attributes('-topmost', True)
        popup.update()

        return popup

    window = tk.Tk()  # Tkinter의 기본 윈도우를 생성
    window.title("GPT powered DJ")  # 윈도우 제목 설정
    font = ('맑은 고딕', 10)

    conversation = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED, font=font)  # 채팅 히스토리를 보여주기 위한 텍스트 위젯 생성
    conversation.configure(spacing1=3, spacing3=3)
    conversation.tag_configure('user', background='#c9daf8')
    conversation.tag_configure('assistant', background='#e4e4e4')
    conversation.pack(fill=tk.BOTH, expand=True,  padx=10, pady=10)  # 텍스트 위젯을 윈도우에 배치

    input_frame = tk.Frame(window)  # 입력 필드와 전송 버튼을 담기 위한 프레임 생성
    input_frame.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)  # 프레임을 윈도우에 배치

    user_entry = tk.Entry(input_frame)  # 사용자 입력을 받기 위한 입력 필드 생성
    user_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)  # 입력 필드를 프레임에 배치

    send_button = tk.Button(input_frame, text="Send", command=on_send)  # 전송 버튼 생성
    send_button.pack(side=tk.RIGHT)  # 전송 버튼을 프레임에 배치

    window.bind('<Return>', lambda event: on_send())

    messages = [
        {
            'role': 'system', 
            'content': """
            You are a DJ assistant who creates playlists. Your user will be Korean, so communicate in Korean. But you must not translate artists' name and song title into Korean.
                - When you show a playlist, it must contain the title, artist, and release year of each song. You must ask the user if they want to save the playlist into CSV like this: "이 플레이리스트를 CSV로 저장하시겠습니까?"
                - If the user wants to save the playlist into CSV, show the playlist in CSV format seperated by ';'. The CSV format must starts with new line. The CSV header must be in English and it must formatted as follows: 'Title;Artist;Release Year' 
                - If the user wants to download audio files (or 음원) you must respond exactly as follows: '음원을 다운로드합니다! DOWNLOAD_MP3'
                - If the user wants to genereate images (or 이미지) for the songs, you must respond exactly as follows: "이미지를 생성합니다! GENERATE_IMAGES"
                - If the user request to generate playlist video using images (or 이미지), you must respond exactly as follows: "이미지를 이용해 플레이리스트 영상을 생성합니다. GENERATE_PLAYLIST_VIDEO_USING_IMAGES"
                - If the user request to generate playlist video using videos (or 동영상 or mp4), you must respond exactly as follows: "동영상을 이용해 플레이리스트 영상을 생성합니다. GENERATE_PLAYLIST_VIDEO_USING_VIDEOS"
            """
        },  
        {
            'role': 'assistant',
            'content': """
            1. "Shape of You" - Ed Sheeran (2017)
            2. "Someone Like You" - Adele (2011)
            3. "Love Yourself" - Justin Bieber (2015)

            이 플레이리스트를 CSV로 저장하시겠습니까?
            """
        },
        {
            'role': 'user',
            'content': '응'
        },
        {
            'role': 'assistant',
            'content': """
            Title;Artist;Release Year
            Shape of You;Ed Sheeran;2017
            Someone Like You;Adele;2011
            Love Yourself;Justin Bieber;2015
            """
        }

    ]

    window.mainloop()  # Tkinter 윈도우 이벤트 루프 실행


if __name__=='__main__':
    main()