from experiment import Experiment
from flask import Flask, render_template, jsonify
import pandas as pd
import json

from threading import Thread
from time import sleep



experiment = Experiment()
app = Flask()

@app.route('/')
def draw():
    
    # labels = [i for i in df['time']]
    # data = [i for i in df['data']]
    return render_template("index.html", data=data, labels=labels)



if __name__ == "__main__":
    Thread(target=experiment.start).start()
    app.run(host='localhost', port=8050, debug=False)
    