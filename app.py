import json
import random
import time
from datetime import date, datetime, timedelta
import numpy as np
from threading import Thread
from queue import Queue
import pandas as pd
import os

from flask import Flask, Response, render_template, stream_with_context

application = Flask(__name__)


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/chart-data')
def chart_data():
    def generate_random_data():
        data = m.full_buffer
        m.out_queue = Queue()
        try:
            df_loaded = pd.read_csv('data.csv')
            print(df_loaded.to_dict('index'))
        except:
            print('file not found ')
        while True:
            # json_data = json.dumps(
            #     [{'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), 'value1': random.random() * 100, 'value2': random.random() * 50} for _ in range(10)])
            for x in m.get_out_buffer():
                data.append(x)
            json_data = json.dumps(data)
            data = []
            # print(json_data)
            if len(json_data) > 0:
                yield f"data:{json_data}\n\n"
            time.sleep(0.51)

    response = Response(stream_with_context(
        generate_random_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


class Measure():
    def __init__(self) -> None:
        self.buffer = []
        self.full_buffer = []
        self.out_queue = Queue()
        self.last_measure = datetime.now()
        self.delay = 0.1
        self.buffersize = 20
        try:
            os.remove('data.csv')
        except:
            pass

    def write_to_file(self, flag):
        df = pd.DataFrame(self.buffer)
        if flag:
            flag = False
            df.to_csv('data.csv', index=False, header=True)
        else:
            df.to_csv('data.csv', mode='a', index=False, header=False)
        return False

    def start(self):
        flag = True
        i = 0
        while True:
            if datetime.now() - self.last_measure >= timedelta(seconds=self.delay):

                self.last_measure = datetime.now()
                self.buffer.append({'time': datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S.%f'), 'value1': np.sin(i), 'value2': np.cos(i)})
                i += 1
            if len(self.buffer) > self.buffersize:
                for x in self.buffer:
                    self.out_queue.put(x)
                    self.full_buffer.append(x)
                    pass
                flag = self.write_to_file(flag)
                self.buffer = []
            time.sleep(0.01)

    def get_out_buffer(self):
        data = []
        while (not self.out_queue.empty()):
            data.append(self.out_queue.get())
        return data


if __name__ == '__main__':
    m = Measure()
    Thread(target=m.start).start()
    time.sleep(2)
    application.run(port=2222)
