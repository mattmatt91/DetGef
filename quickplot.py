import pandas as pd
from matplotlib import pyplot as plt
"""
path1 = 'C:\\Users\\Matthias\\Desktop\\tests\\inert_lamp\\results_10_05_2022 13-52-53.csv'
path2 = 'C:\\Users\\Matthias\\Desktop\\tests\\inert_dark\\results_10_05_2022 13-53-54.csv'
path3 = 'C:\\Users\\Matthias\\Desktop\\tests\\ipa_lamp\\results_10_05_2022 13-57-30.csv'
path4 = 'C:\\Users\\Matthias\\Desktop\\tests\\ipa_dark\\results_10_05_2022 13-56-18.csv'



df1 = pd.read_csv(path1, delimiter='\t', decimal='.')
df2 = pd.read_csv(path2, delimiter='\t', decimal='.')
df3 = pd.read_csv(path3, delimiter='\t', decimal='.')
df4 = pd.read_csv(path4, delimiter='\t', decimal='.')

df_new = pd.DataFrame()
df_new['il'] = df1['voltage_multimeter']
df_new['id'] = df2['voltage_multimeter']
df_new['ipal'] = df3['voltage_multimeter']
df_new['ipad'] = df4['voltage_multimeter']


df_new.plot()
plt.show()
"""

path = 'C:\\Users\\Matthias\\Desktop\\DetGef\\DetGef\\data\\gaslampaan\\results_10_05_2022 14-32-12.csv'
df = pd.read_csv(path, delimiter='\t', decimal='.')
df['voltage_multimeter'].plot(grid=True)
plt.show()