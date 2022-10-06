from test_device import TestDevice


from multimeter import Multimeter
from powersupply import PowerSupply
from mfc import MFC
from os.path import join
import json
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path
import os


program_path = 'test_program.csv'
programs_defaultpath = 'programs'
default_data_path = 'data'


address_powersupply = 'ASRL11::INSTR'
address_multimeter = 'USB0::0x05E6::0x6500::04544803::INSTR'
mfc_ip = "192.168.2.100"
mfc_port = 502
mfc_max_flow = 1000
buffer_size = 5

class Experiment():
    def __init__(self, test=False):
        self.test = test
        if self.test:
            self.multimeter = TestDevice('multimeter')
            self.powersupply = TestDevice('powersupply')
            self.mfc = TestDevice('mfc')
        else:
            # define defices and create instances of classes
            self.powersupply = PowerSupply(address_powersupply)
            self.multimeter = Multimeter(address_multimeter)
            self.fc = MFC(mfc_ip, mfc_port, mfc_max_flow)

        self.buffer_size = buffer_size  # change for experiments --> number of points in buffer to wirte to file
        self.read_program()
        self.create_folder_structure()

    def create_folder_structure(self):
        _time = datetime.now().strftime("_%m-%d-%Y_%H-%M-%S")
        self.name = program_path[:program_path.find('.csv')] + _time
        self.data_path = join(default_data_path, self.name) # path to folder with data of measurement
        Path(self.data_path).mkdir(parents=True, exist_ok=True)
        # self.file_entire_path = join(self.data_path, _name)


    def read_program(self): # reading program as pd.df
        _path_program = join(programs_defaultpath, program_path)
        self.program = pd.read_csv(_path_program, decimal='.', delimiter='\t')
        self.program.set_index('step_id', inplace=True)
        print(f'reading {program_path}')


    def start(self):  # startung measurement
        self.start_time = datetime.now()
        self.data_entire = []
        for step_id in self.program.index:
            self.step = self.program.loc[step_id]
            print(f'starting step {step_id}')
            print(self.step)
            self.step_id = step_id
            self.set_parameters()
            self.step_loop()
        self.close_devices()
    
    def set_parameters(self):  # set parameters for every step in measurement
        if self.test:
            # powersupply
            self.powersupply.set_value_1(self.step['voltage [V]'])
            self.powersupply.set_value_2(self.step['current [A]'])
            self.powersupply.set_value_3(self.step['power [W]'])

            # mfc
            self.mfc.set_value_1(self.step['flow_total [ml/min]'])

        else:
            # powersupply
            print('\n\n\n', self.step)
            self.powersupply.set_voltage(self.step['voltage [V]'])
            self.powersupply.set_current(self.step['current [A]'])
            self.powersupply.set_power(self.step['power [W]'])
            self.powersupply.supply_on()
            
            # mfc
            self.mfc.set_point(self.step['flow_total [ml/min]'])

    def close_devices(self):  # close connections to all devices
        self.multimeter.close()
        self.powersupply.close()
        self.mfc.close()

    def step_loop(self):  # loop during single steps, for saving data
        i = 0
        sampling_interval = timedelta(seconds=(1/(self.step['samplingrate [Hz]'])))
        step_start_time = datetime.now()
        last_measure = step_start_time - sampling_interval
        step_name = self.step['step_name']
        file_name = f'{self.name}_{step_name}.csv'
        self.filepath = join(self.data_path, file_name)
        print(self.filepath)
        while datetime.now() <= step_start_time + timedelta(minutes=self.step['duration [min]']):
            pass
            # self.get_data()
        # self.save_data(last=True)
#######################################






    def get_data(self): #gettung data from devices
        this_time = datetime.now()
        if this_time >= self.last_fetched + self.interval: #checking interval
            self.i += 1
            self.last_fetched = this_time
            # colecting data
            self.latest_data = {'id': self.program[self.step_id]['name'], 'time': datetime.now().strftime('%m_%d_%Y %H-%M-%S'),
                                'timestamp': round_time(str(datetime.now() - self.step_start_time), 2)}
            self.latest_data.update(self.devices['powersupply'].get_data())
            self.latest_data.update(self.devices['multimeter'].get_data())
            self.latest_data.update(self.devices['mfc'].get_data())
            # appending data to file
            self.data.append(self.latest_data)
            self.data_entire.append(self.latest_data)
            self.save_data()

    # save data every {buffersize} value, appends if exists, creates new if not
    def save_data(self, last=False):
        if len(self.data) > self.buffer_size or last:
            df = pd.DataFrame(self.data)
            if not os.path.isfile(self.filepath):
                df.to_csv(self.filepath, header='column_names',
                          index=False, sep='\t', decimal='.')
            else:
                df.to_csv(self.filepath, mode='a', header=False,
                          index=False, sep='\t', decimal='.')

            if not os.path.isfile(self.file_entire_path):
                df.to_csv(self.file_entire_path, header='column_names',
                          index=False, sep='\t', decimal='.')
            else:
                df.to_csv(self.file_entire_path, mode='a',
                          header=False, index=False, sep='\t', decimal='.')

            self.data = []

    


def round_time(string, dec):
    if string.find('.') >= 0:
        string = string.split('.')
        string = string[0]+'.' + \
            str(round(float('0.'+string[1]), dec)).split('.')[1]
    return string


if __name__ == '__main__':
    experiment = Experiment(test=True)
    experiment.start()