import json
import random
from re import T
import time
from datetime import date, datetime, timedelta
import numpy as np
from threading import Thread
from queue import Queue
import pandas as pd
import os
from main import Experiment
from matplotlib import pyplot as plt

from flask import Flask, Response, render_template, stream_with_context

test= False


application = Flask(__name__)
e = Experiment(test=False)



@application.route('/')
def index():
    return render_template('index.html')


@application.route('/chart-data')
def chart_data():
    def load_data_from_file():
        data = []
        files = e.get_file_path()
        if len(files) >0:
            dfs = []
            for file in files:
                if os.path.isfile(file):
                    dfs.append(pd.read_csv(file, decimal='.', sep='\t'))
            df_loaded = pd.concat(dfs).dropna()
            df_loaded.reset_index(drop=True, inplace=True)
            df_loaded.fillna(method="ffill" ,inplace=True)
            dict_loaded = df_loaded.to_dict('index')
            for i in dict_loaded:
                data.append(dict_loaded[i])
        else:
            print('no fiels to read')
        return data

    def read_data():
        data = load_data_from_file()
        while True:
            for x in e.get_out_buffer():
                data.append(x)
            json_data = json.dumps(data)
            if len(json_data) > 0:
                yield f"data:{json_data}\n\n"
            data = []
            time.sleep(0.5)

    response = Response(stream_with_context(
        read_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


if __name__ == '__main__':

    Thread(target=e.start).start()
    time.sleep(2)
    application.run(port=2222, host="127.0.0.1")
