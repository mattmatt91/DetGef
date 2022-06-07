from collections import deque

import time
from tokenize import Name
import numpy as np
from datetime import datetime, timedelta
import os
from colorama import Fore, init, Back, Style

offset_canvas = (8, 42)
rows_canvas = 10
cols_canvas = 80

cyan_f = '\033[36m'
green_f = '\033[32m'
red_f = '\033[31m'
white_f = '\033[37m'
reset_f = '\033[m'
underline_f = '\033[4m'


banner =   [" .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .---------------. ", 
            "| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. ",
            "| |  ________    | || |  _________   | || |  _________   | || |    ______    | || |  _________   | || |  _________   | ",
            "| | |_   ___ `.  | || | |_   ___  |  | || | |  _   _  |  | || |  .' ___  |   | || | |_   ___  |  | || | |_   ___  |  | ",
            "| |   | |   `. \ | || |   | |_  \_|  | || | |_/ | | \_|  | || | / .'   \_|   | || |   | |_  \_|  | || |   | |_  \_|  | ",
            "| |   | |    | | | || |   |  _|  _   | || |     | |      | || | | |    ____  | || |   |  _|  _   | || |   |  _|      | ",
            "| |  _| |___.' / | || |  _| |___/ |  | || |    _| |_     | || | \ `.___]  _| | || |  _| |___/ |  | || |  _| |_       | ",
            "| | |________.'  | || | |_________|  | || |   |_____|    | || |  `._____.'   | || | |_________|  | || | |_____|      | ",
            "| |              | || |              | || |              | || |              | || |              | || |              | ",
            "| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' ",
            "'----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' "]

while len(banner) <= rows_canvas:
    banner.append((''.join(''*len(banner[0]))))

banner = [i + (' '*(cols_canvas - len(i))) for i in banner]

def set_cursor(row, col):
    return f'\033[{row};{col}H'

def set_cursor_canvas(row, col):
    return set_cursor(row+offset_canvas[0]+1, col+offset_canvas[1]+1)

def clear_canvas():
    for i in range(rows_canvas):
        print(set_cursor_canvas(i+1, 0) + '\033[0K', end='')

def draw_canvas():
    # clear_canvas()
    i = 0
    for row in banner:
        print(red_f + set_cursor_canvas(i+1, 0) + row + reset_f, end='')
        # shifting text
        _deque = deque(list(row))
        _deque.rotate((int(np.sin(time.time()+1)/0.50)))
        new_row = ''.join(list(_deque))
        banner[i] = new_row
        i += 1
    

class Console_monitor():
    def __init__(self,programs, framerate=20):
        self.programs = programs
        self.start_time_global = datetime.now()
        _duration_global = 0
        self.steps  = {}
        i = 0
        for step in programs:
            _duration_global += programs[step]['duration']['value']
            self.steps[i] = (programs[step]['name'])
            i+=1
        self.duration_global = timedelta(seconds=_duration_global)
        self.stop_time_global = self.start_time_global + self.duration_global
        self. update_interval = timedelta(seconds=1/framerate)
        os.system('cls')
        self.last_update = datetime.now()

    def new_program(self, step_id):
        duration = self.programs[step_id]['duration']['value']
        name = self.programs[step_id]['name']
        self.start_time = datetime.now()
        self.duration = timedelta(seconds=duration)
        self.stop_time = datetime.now() + self.duration
        self.name = name
        self.step_id = int(step_id)
        print(set_cursor(3, 1) + '\033[X0')
        
    def update(self, sensor_data):
        if datetime.now() >= self.last_update + self.update_interval:
            self.last_update = datetime.now()
            progress = datetime.now() - self.start_time
            percent = int(100*(progress.total_seconds() /
                          self.duration.total_seconds()))
            progress_global = datetime.now() - self.start_time_global
            percent_global = int(100*(progress_global.total_seconds() /
                          self.duration_global.total_seconds()))
            bar = green_f + 'total\t\t' + percent*'█' + ' ' + \
                (100-percent)*'-'+'┃' + cyan_f + f'{percent}% ' + reset_f
            bar_total = cyan_f +  'experiment\t' + percent_global*'█' + ' ' + \
                (100-percent_global)*'-'+'┃' + cyan_f + f'{percent_global}% ' + reset_f
            step_string = '┃ '
            for step in self.steps:
                if self.step_id == step:
                    step_string += (red_f + self.steps[step] + reset_f + ' ┃ ' )
                else:
                    step_string += (self.steps[step] + ' ┃ ' )
            print(set_cursor(3, 1) + f'step {(int(self.step_id)+1)} of {len(self.programs)}')
            print(set_cursor(3, 20), step_string)
            print(set_cursor(5, 1) + bar_total)
            print(set_cursor(6, 1) + bar)
            print(set_cursor(8, 2) + '┍' + '━'*35 + '┑')
            i = 8
            for sensor in sensor_data:
                i += 1

                print(set_cursor(i, 2) + '│' + green_f + sensor + ':' + set_cursor(i, 16) + cyan_f + str(sensor_data[sensor]) + set_cursor(i, 38) + reset_f + '│')
            i += 1
            print(set_cursor(i, 2) + '┕' + '━'*35 + '┙')
            i += 1
            print(set_cursor(
                i, 1) + f'{cyan_f}remeaning time:\t{green_f}{(self.stop_time_global-datetime.now())}')
            i += 1
            print(set_cursor(
                i, 1) + f'{cyan_f}finished at:\t{green_f}{self.stop_time_global}')
            print(Fore.RESET, end='')
            if datetime.now() > self.stop_time:
                i += 2
                print(set_cursor(i, 1) +
                      f'\n{red_f + self.name + reset_f} finished')
            draw_canvas()

if __name__ == '__main__':
    start_time = datetime.now()
    duration = timedelta(seconds=20)
    name = 'TEST'
    console_monitor = Console_monitor(program = 'program')
    # implement test program
    while True:
        sensor_data = {}
        for i in range(8):
            sensor_data[f'sensor{i}'] = round(
                np.random.randint(5)*(np.random.rand(1)[0] % 9), 3)

        console_monitor.update(sensor_data)
