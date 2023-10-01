import pandas as pd

def extract_csv_data(response):
    # 세미콜론(;)으로 구분된 CSV 데이터를 판다스 데이터프레임으로 추출하는 함수
    csv_data = response.strip().split('\n')  # 응답을 줄 단위로 분할
    csv_data = [line.split(';') for line in csv_data]  # 각 줄을 세미콜론으로 분할하여 2차원 리스트 생성
    header = csv_data[0]  # 헤더 정보 추출
    data = csv_data[1:]  # 데이터 추출
    df = pd.DataFrame(data, columns=header)  # 판다스 데이터프레임 생성
    return df


some_string = """
다음은 요청하신 플레이리스트의 CSV 포맷입니다. 

Title;Artist;Released
Dynamite;BTS;2020
강남스타일;PSY;2010
좋은날;아이유;2013

어떤가요?
"""

df = extract_csv_data(some_string)
print(df)