from importlib.resources import path
import pandas as pd

path = 'data\\program_10-12-2022_14-13-29\\program_10-12-2022_14-13-29.csv'

df = pd.read_csv(path, decimal='.', sep='\t')
print(df.isnull().sum())
print(df.info)
df.fillna(method="ffill" ,inplace=True)
print('\n\n\n', df.isnull().sum())
print(df.info)
