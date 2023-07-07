import tkinter as tk
from tkinter import scrolledtext  # Tkinter 모듈을 가져옴
import openai  # OpenAI API와 상호 작용하기 위한 모듈

openai.api_key = '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'  # OpenAI API 키 설정

def ask_to_gpt_35_turbo(messages):
    # GPT-3.5 Turbo 모델에 메시지를 보내 응답을 받는 함수
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',  # 사용할 모델 선택
        temperature=0.5,  # 출력 다양성 조절을 위한 옵션
        messages=messages  # 이전 메시지와 사용자 입력을 포함하는 메시지 목록
    )
    return response.choices[0].message.content  # 응답 중 첫 번째 응답의 내용 반환

def send_message():
    user_input = user_entry.get()  # 입력 필드에서 사용자 입력을 가져옴

    if user_input.lower() == 'quit':  # 사용자가 'quit'를 입력하면 프로그램 종료
        window.destroy()
        return

    messages.append(
        {'role': 'user', 'content': user_input},  # 사용자 메시지를 메시지 목록에 추가
    )

    response = ask_to_gpt_35_turbo(messages)  # 메시지 목록을 GPT-3.5 Turbo 모델에 전달하여 응답 받음

    messages.append(
        {'role': 'assistant', 'content': response},  # 응답을 메시지 목록에 추가
    )

    conversation.config(state=tk.NORMAL)  # 채팅 히스토리 텍스트 상태를 편집 가능한 상태로 변경
    conversation.insert(tk.END, 'You: ' + user_input + '\n', 'user')  # 사용자 입력을 채팅 히스토리에 추가
    conversation.insert(tk.END, 'Assistant: ' + response + '\n', 'assistant')  # 응답을 채팅 히스토리에 추가
    conversation.config(state=tk.DISABLED)  # 채팅 히스토리 텍스트 상태를 읽기 전용 상태로 변경
    conversation.see(tk.END)  # 채팅 히스토리 스크롤을 맨 아래로 이동

    user_entry.delete(0, tk.END)  # 입력 필드를 비움

window = tk.Tk()  # Tkinter의 기본 윈도우를 생성
window.title("Chat with GPT-3.5 Turbo")  # 윈도우 제목 설정
# root.geometry("400x500")  # 윈도우 크기 설정

conversation = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED)  # 채팅 히스토리를 보여주기 위한 텍스트 위젯 생성
conversation.tag_configure('user', background='#c9daf8')
conversation.tag_configure('assistant', background='#e4e4e4')
conversation.pack(fill=tk.BOTH, expand=True,  padx=10, pady=10)  # 텍스트 위젯을 윈도우에 배치

input_frame = tk.Frame(window)  # 입력 필드와 전송 버튼을 담기 위한 프레임 생성
input_frame.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)  # 프레임을 윈도우에 배치

user_entry = tk.Entry(input_frame)  # 사용자 입력을 받기 위한 입력 필드 생성
user_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)  # 입력 필드를 프레임에 배치

send_button = tk.Button(input_frame, text="Send", command=send_message)  # 전송 버튼 생성
send_button.pack(side=tk.RIGHT)  # 전송 버튼을 프레임에 배치

window.bind('<Return>', lambda event: send_message())

messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},  # 초기 시스템 메시지를 메시지 목록에 추가
]

window.mainloop()  # Tkinter 윈도우 이벤트 루프 실행
