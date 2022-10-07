from matplotlib.pyplot import legend
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from os.path import join


def plot_measurement(path,test=False):
    df = pd.read_csv(path, sep='\t', decimal='.')
    df  = sort_df_time(df, sort='time')
    if not test:
        y_col = 'resistance_multimeter_measured'
    else:
        y_col = "mfc_measured_value"
    fig = px.line(
        df,
        x="timestamp",
        y=y_col,
        title=path[path.rfind('_')+1:path.rfind('.')],
        labels={"timestamp": "time [s]", y_col: "resistance [Ohm]"})
    fig.update_layout(showlegend=False)
    path_fig = join(path[:path.rfind('\\')],
                    path[path.rfind('\\')+1:path.rfind('.')] + '.html')
    fig.write_html(path_fig)
    fig.show()


def plot_all_measurement_line(path,test=False):
    print('plotting line ##################################')
    df = pd.read_csv(path, sep='\t', decimal='.')
    df  = sort_df_time(df, sort='time')
    if not test:
        y_col = 'resistance_multimeter_measured'
    else:
        y_col = "mfc_measured_value"
    hoover_info = df.columns
    fig = px.line(
        df,
        x='time',
        y=y_col,
        color='id',
        hover_data=hoover_info,
        title=path[path.rfind('_')+1:path.rfind('.')],
        labels={"time": "time [s]",
                y_col: "resistance [Ohm]",
                "id": "step"}
    )
    path_fig = join(path[:path.rfind('\\')],
                    path[path.rfind('\\')+1:path.rfind('.')] + '_line.html')
    fig.write_html(path_fig)
    fig.show()
    


def plot_all(path, test=False):
    df = pd.read_csv(path, sep='\t', decimal='.')
    df = sort_df_time(df)
    hoover_info = df.columns
    if not test:
        y_col = 'resistance_multimeter_measured'
    else:
        y_col = "mfc_measured_value"
    fig = px.line(
        df,
        x='timestamp',
        y=y_col,
        color='id',
        hover_data=hoover_info,
        title=path[path.rfind('_')+1:path.rfind('.')],
        labels={"timestamp": "time [s]",
                y_col: "resistance [Ohm]",
                "id": "step"}
    )
    path_fig = join(path[:path.rfind('\\')],
                    path[path.rfind('\\')+1:path.rfind('.')] + '.html')
    fig.write_html(path_fig)
    fig.show()

def sort_df_time(df, test=False, sort='timestamp'):
    new_time = []
    for stamp in df['timestamp']:
        if stamp.find('.') >= 0:
            new_time.append(datetime.strptime(stamp, "%H:%M:%S.%f"))
        else:
            new_time.append(datetime.strptime(stamp, "%H:%M:%S"))
    df['timestamp'] = [(i - new_time[0]).total_seconds() for i in new_time]
  
    new_time = []
    for stamp in df['time']:
        if stamp.find('.') >= 0:
            new_time.append(datetime.strptime(stamp, "%H:%M:%S.%f"))
        else:
            new_time.append(datetime.strptime(stamp, "%H:%M:%S"))
    df['time'] = [(i - new_time[0]).total_seconds() for i in new_time]

    df = df.sort_values(by=sort)
    return df


if __name__ == '__main__':
    # path = "data\\program_10-07-2022_12-36-19\\program_10-07-2022_12-36-19_measure2.csv"
    # plot_measurement(path)

    path = 'data\\program_10-07-2022_17-24-38\\program_10-07-2022_17-24-38.csv'
    # plot_all(path)
    plot_all_measurement_line(path,test=True)