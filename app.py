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

from flask import Flask, Response, render_template, stream_with_context

application = Flask(__name__)
e = Experiment(test=True)



@application.route('/')
def index():
    return render_template('index.html')


@application.route('/chart-data')
def chart_data():
    def generate_random_data():
        data = []
        try:
            path = e.get_file_path()
            df_loaded = pd.read_csv(path, decimal='.', sep='\t')
            dict_loaded = df_loaded.to_dict('index')
            data = [dict_loaded[i] for i in dict_loaded]
            # print(data)
        except:
            print('file not found ')
        while True:
            for x in e.get_out_buffer():
                data.append(x)
            json_data = json.dumps(data)
            if len(json_data) > 0:
                yield f"data:{json_data}\n\n"
            data = []
            time.sleep(0.5)

    response = Response(stream_with_context(
        generate_random_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


if __name__ == '__main__':
    Thread(target=e.start).start()
    time.sleep(2)
    application.run(port=2222)
