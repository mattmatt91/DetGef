from matplotlib.pyplot import plot
from test_device import TestDevice
from plot_measurements import plot_measurement, plot_all, plot_all_measurement_line
from multimeter import Multimeter
from powersupply import PowerSupply
from mfc import MFC
from os.path import join
import json
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path
import os
from time import sleep


program_path = 'program.csv'
programs_defaultpath = 'programs'
default_data_path = 'data'


address_powersupply = 'ASRL11::INSTR'
address_multimeter = 'USB0::0x05E6::0x6500::04544803::INSTR'
mfc_ip = "192.168.2.100"
mfc_port = 502
mfc_max_flow = 1000
buffer_size = 5
update_plot = 2  # sek


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

        # change for experiments --> number of points in buffer to wirte to file
        self.buffer_size = buffer_size
        self.read_program()
        self.create_folder_structure()

    def create_folder_structure(self):
        _time = datetime.now().strftime("_%m-%d-%Y_%H-%M-%S")
        self.name = program_path[:program_path.find('.csv')] + _time
        # path to folder with data of measurement
        self.data_path = join(default_data_path, self.name)
        Path(self.data_path).mkdir(parents=True, exist_ok=True)

    def read_program(self):  # reading program as pd.df
        _path_program = join(programs_defaultpath, program_path)
        self.program = pd.read_csv(_path_program, decimal='.', delimiter='\t')
        self.program.set_index('step_id', inplace=True)
        print(f'reading {program_path}')

    def start(self):  # startung measurement
        self.files = []
        self.global_start = datetime.now()
        for step_id in self.program.index:
            self.step = self.program.loc[step_id]
            print(f'starting step {step_id}')
            print(self.step)
            self.step_id = step_id
            self.set_parameters()
            sleep(1)
            self.step_loop()
        self.merge_files()
        self.close_devices()

    def merge_files(self):
        path_merged = join(self.data_path, f'{self.name}.csv')
        dfs = []
        for file in self.files:
            dfs.append(pd.read_csv(file, decimal='.', sep='\t'))
        df_merged = pd.concat(dfs)
        df_merged.to_csv(path_merged, decimal='.', sep='\t', index=False)
        plot_all(path_merged, test=True)

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
        self.sampling_interval = timedelta(
            seconds=(1/(self.step['samplingrate [Hz]'])))
        step_name = self.step['step_name']
        print(self.step['samplingrate [Hz]'])
        file_name = f'{self.name}_{step_name}.csv'
        self.filepath = join(self.data_path, file_name)
        print(self.filepath)
        self.files.append(self.filepath)
        self.get_data()

    def get_buffer(self):  # for live plot
        if self.last_full_buffer == None:
            return None
        else:
            buf = self.last_full_buffer
            self.last_full_buffer = None
            return buf

    def get_data(self):  # gettung data from devices
        step_start_time = datetime.now()
        last_measure = step_start_time - self.sampling_interval
        buffer = []
        self.last_full_buffer = None
        flag = True

        while datetime.now() <= step_start_time + timedelta(minutes=self.step['duration [min]']):
            this_time = datetime.now()
            if this_time >= last_measure + self.sampling_interval:  # checking interval
                last_measure = this_time
                # colecting data
                data = {'id': self.step['step_name'], 'time': str(datetime.now() - self.global_start),
                        'timestamp': str(datetime.now() - step_start_time)}
                data.update(self.powersupply.get_data())
                data.update(self.multimeter.get_data())
                data.update(self.mfc.get_data())
                buffer.append(data)
                if len(buffer) > self.buffer_size:
                    df_buffer = pd.DataFrame(buffer)
                    if flag:
                        df_buffer.to_csv(self.filepath, sep='\t',
                                         decimal='.', index=False)
                        flag = False
                    else:
                        df_buffer.to_csv(
                            self.filepath, sep='\t', decimal='.', mode='a', index=False, header=False)
                    self.last_full_buffer = buffer
                    buffer = []
        df_buffer.to_csv(self.filepath, sep='\t', decimal='.',
                         mode='a', index=False, header=False)
        self.last_full_buffer = buffer
        buffer = []
        plot_measurement(self.filepath, test=True)
        plot_all_measurement_line(self.filepath, test=True)


if __name__ == '__main__':
    experiment = Experiment(test=True)
    experiment.start()
