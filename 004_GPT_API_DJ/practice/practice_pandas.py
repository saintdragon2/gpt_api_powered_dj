import pandas as pd


df = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=['a', 'b', 'c'])

df['d'] = df['a'] + df['b']

df.to_csv('./practice.csv', sep=';')
print(df)