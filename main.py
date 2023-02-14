
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
from queue import Queue
from relaisboard import Relaisboard
from colorama import Fore, Back, Style
from keysightdaq970A import KeysightDAQ970a

program_path = 'program.csv'
programs_defaultpath = 'programs'
default_data_path = 'data'


address_powersupply = 'ASRL11::INSTR'
address_multimeter = 'USB0::0x05E6::0x6500::04544803::INSTR'
address_keysight = 'USB0::0x2A8D::0x5101::MY58018230::INSTR'
relaisboard_port = 'COM13'
buffer_size = 10
update_plot = 2  # sek

test = False


class Experiment():
    def __init__(self, test=False):
      
        # define defices and create instances of classes
        print(Fore.GREEN + 'init ' + Fore.RESET + 'powersupply')
        self.powersupply = PowerSupply(address_powersupply)
        print(Fore.GREEN + 'init ' + Fore.RESET + 'multimeter')
        # self.multimeter = Multimeter(address_multimeter)
        self.multimeter_keysight = KeysightDAQ970a(address_keysight)
        print(Fore.GREEN + 'init ' + Fore.RESET + 'relays')
        self.relaisboard = Relaisboard()
        print(Fore.GREEN + 'init ' + Fore.RESET + 'mfcs')
        self.mfcs = {}
        with open('properties_mfc.json', 'r') as f:
            properties_mfc = json.load(f)
        for mfc in properties_mfc:
            _mfc = properties_mfc[mfc]
            self.mfcs[mfc] = MFC(
                _mfc["ip"], _mfc["port"], _mfc["flow_max"])

        # change for experiments --> number of points in buffer to wirte to file
        self.buffer_size = buffer_size
        print('ceate folder structure')
        self.create_folder_structure()  # run before read_program
        print('reading program')
        self.read_program()

    def create_folder_structure(self):
        _time = datetime.now().strftime("_%m-%d-%Y_%H-%M-%S")
        self.name = program_path[:program_path.find('.csv')] + _time
        # path to folder with data of measurement
        self.data_path = join(default_data_path, self.name)
        Path(self.data_path).mkdir(parents=True, exist_ok=True)

    def read_program(self):  # reading program as pd.df
        _path_program = join(programs_defaultpath, program_path)
        self.program = pd.read_csv(_path_program, decimal=',', delimiter=';')
        path_program_save = join(self.data_path, f'{self.name}_properties.csv')
        self.program.to_csv(path_program_save, decimal=',',
                            sep=';', index=False)
        self.program.set_index('step_id', inplace=True)
        print(f'reading {program_path}')

    def start(self):  # startung measurement
        self.files = {}
        self.global_start = datetime.now()
        for step_id in self.program.index:
            self.step = self.program.loc[step_id]
            self.step_id = step_id
            print(Fore.RED + f'starting step ' + Style.RESET_ALL + f'{step_id}')
            print(self.step)
            self.set_parameters()
            self.step_loop()
        self.mergefiles()
        self.close_devices()

        

    def mergefiles(self):
        path_merged = join(self.data_path, f'{self.name}_merged.csv')
        dfs = []
        for file in self.files:
            df = pd.read_csv(self.files[file], decimal=',', sep=';')
            df.set_index('time', inplace=True)
            dfs.append(df)
        df_merged = pd.concat(dfs)
        df_merged.to_csv(path_merged, decimal=',', sep=';', index=True)
        # plot_all(path_merged, test=False)
        # plot_all_measurement_line(path_merged, test=False)

    def set_parameters(self):  # set parameters for every step in measurement
        # powersupply
        self.powersupply.set_voltage(float(self.step['voltage [V]']))
        self.powersupply.set_current(float(self.step['current [A]']))
        self.powersupply.set_power(float(self.step['power [W]']))
        self.powersupply.supply_on()

        # mfc
        for mfc in self.mfcs:
            self.mfcs[mfc].set_point(float(self.step[f'{mfc} [ml/min]']))

        # relais
        # msg = [(f'valve{valve}', self.step['valve{valve}']) for valve in range(len(self.relaisboard.pins))] # list of tuple with pin and state
        # print(f'mgs relais: {msg}')
        # self.relaisboard.set_states(msg)

        self.multimeter_keysight.set_param()

    def close_devices(self):  # close connections to all devices
        # self.multimeter.close()
        self.multimeter_keysight.close()
        self.powersupply.close()
        for mfc in self.mfcs:
            self.mfcs[mfc].close()
        # self.relaisboard.close()

    def step_loop(self):  # loop during single steps, for saving data
        self.out_queue = Queue()
        self.sampling_interval = timedelta(
            seconds=(1/(self.step['samplingrate [Hz]'])))

        step_name = self.step['step_name']
        file_name = f'{self.name}_{step_name}_{self.step_id}.csv'
        self.filepath = join(self.data_path, file_name)
        print(self.filepath)
        self.files[self.step_id] = self.filepath
        self.get_data()

    def write_to_file(self, buffer, flag=False):
        df = pd.DataFrame(buffer)
        if flag:
            df.to_csv(self.filepath, sep=';',
                      decimal=',', index=False)
        else:
            df.to_csv(
                self.filepath, sep=';', decimal=',', mode='a', index=False, header=False)
        return False

    def get_out_buffer(self):
        data = []
        while not self.out_queue.empty():
            data.append(self.out_queue.get())
        return data

    def get_file_path(self):
        return self.files

    def kill(self):
        exit()

    def get_data(self):  # gettung data from devices
        step_start_time = datetime.now()
        last_measure = step_start_time - self.sampling_interval
        buffer = []
        flag = True

        while datetime.now() <= step_start_time + timedelta(minutes=float(self.step['duration [min]'])):
            this_time = datetime.now()
            if this_time >= last_measure + self.sampling_interval:  # checking interval
                last_measure = this_time
                # colecting data
                data = {'id': self.step['step_name'], 'time': str(datetime.now() - self.global_start),
                        'timestamp': str(datetime.now() - step_start_time)}
                data.update(self.powersupply.get_data())
                # data.update(self.multimeter.get_data())
                data.update(self.multimeter_keysight.get_data())
                for mfc in self.mfcs:
                    data.update(self.mfcs[mfc].get_data())
                # putting data to buffer and queqe

                self.out_queue.put(data)
                buffer.append(data)
                if len(buffer) > self.buffer_size:
                    flag = self.write_to_file(buffer, flag)
                    buffer = []
                sleep(0.05)
        self.write_to_file(buffer, flag)
        # plot_measurement(self.filepath, test=False)


if __name__ == '__main__':
    print(Fore.GREEN + 'init ' + Fore.RESET + 'measurement')
    experiment = Experiment(test=test)
    print('starting measurement')
    experiment.start()
