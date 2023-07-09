import pandas as pd


df = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=['a', 'b', 'c'])
df['s'] = [10, 100]
print(df)