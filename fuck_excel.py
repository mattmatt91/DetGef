import pandas as pd


df = pd.DataFrame()

df['step_id'] = [0,1,2]
df['step_name'] = ['heating up', ' measure1', 'measure2']
df['voltage [V]'] = [2.2,3.0, 3.1]
df['power [W]'] = [1,1,1]
df['current [A]'] = [1,1,1]
df['flow_total [ml/min]'] = [500, 600, 600]
df['tanalyt_c [ppm]'] = [100, 300, 300]
df['samplingrate [Hz]'] = [1, 10, 10]
df['duration [min]'] = [0.1,0.2,0.2]
for i in range(12):
    df[f'valve{i}'] = False



print(df)
df.to_csv('programs\\program.csv', decimal='.', sep='\t', index=False)