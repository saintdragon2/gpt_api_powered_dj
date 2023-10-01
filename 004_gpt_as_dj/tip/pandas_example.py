import pandas as pd

data = {
    'name': ['Alice', 'Bob', 'Charlie', 'Dave'],
    'age': [25, 43, 18, 15],
    'city': ['Seoul', 'Tokyo', 'Busan', 'LA']
}

df = pd.DataFrame(data)
print(df)

print('------------------------------')

df_playlist = pd.read_csv('./004_gpt_as_dj/tip/playlist.csv', sep=';')
print(df_playlist)