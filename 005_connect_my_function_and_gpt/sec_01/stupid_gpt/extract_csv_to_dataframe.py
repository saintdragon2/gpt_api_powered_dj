import pandas as pd
import chardet 

some_string = """
다음은 요청하신 플레이리스트의 CSV 포맷입니다. 

Title;Artist;Released
Dynamite;BTS;2020
강남스타일;PSY;2010
좋은날;아이유;2013

어떤가요?   
"""

def extract_csv_to_dataframe(response):
    if ';' in response:
        response_lines = response.strip().split('\n')
        csv_data = []

        for line in response_lines:
            if ';' in line:
                csv_data.append(line.split(';'))

        if len(csv_data) > 0:
            df = pd.DataFrame(csv_data[1:], columns=csv_data[0])
            return df
    else:
        return None


print(chardet.detect(some_string.encode()))    
df = extract_csv_to_dataframe(some_string)
df.to_csv('sss.csv', sep=';')
print(df)