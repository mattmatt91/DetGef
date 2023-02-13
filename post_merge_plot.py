import pandas as pd
import plotly.express as px
import os
from matplotlib import pyplot as plt
path = 'C:\\Users\\49157\Desktop\\Rene_060223_02-06-2023_14-34-12\\Rene_060223_02-06-2023_14-34-12'

list_files_all =  [os.path.join(path, i) for i in os.listdir(path)]
properties = None
steps = {}
for file in list_files_all:
    if file.find('properties')>= 0:
        properties = pd.read_csv(file, delimiter=';', decimal=',')
        # list_files_all.remove(file)
for file in list_files_all:
    for step in properties['step_name']:
        if file.find(step)>=0:
            steps[step] = file
dfs_order = []
for step in steps:
    # print(step, steps[step])
    df = pd.read_csv(steps[step], delimiter=';', decimal=',')
    dfs_order.append(df)

df_entire = pd.concat(dfs_order)
df_entire.sort_values(by='time', inplace = True)
#df_entire.set_index('time', inplace=True)
print(df_entire.columns)
fig = px.scatter(df, x='time', y='voltage_actual_ps')
fig.show()

# print(properties)
# list_files_all.remove

