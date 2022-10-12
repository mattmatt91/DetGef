from importlib.resources import path
import pandas as pd
from matplotlib import pyplot as plt

path = 'data\\program_10-12-2022_14-13-29\\program_10-12-2022_14-13-29.csv'

df = pd.read_csv(path, decimal='.', sep='\t')
print(df.isnull().sum())
print(df.info)
df.fillna(method="ffill" ,inplace=True)
print('\n\n\n', df.isnull().sum())
print(df.info)
df.set_index('time', inplace=True)
drops  =['timestamp', 'power_actual', 'current_actual_ps',
       'voltage_actual_ps', 'power_set', 'current_set_ps', 'voltage_set_ps', 'temp', 'flow', 'flow_total',
       'valve_state', 'point', 'valve_pos']
for to_drop in drops:
    df.drop(to_drop, axis=1,  inplace=True)
df['diff'] = df['resistance_multimeter_measured'].diff()
print(df.head)
df.plot()
plt.show()
