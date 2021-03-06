test = True

if not test:
    from multimeter import Multimeter
    from powersupply import PowerSupply
    from gas import Gas
import not_GUI
from outro import doit
from os.path import join
import json
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path
import os


program_path = 'test_program1.json'
programs_defaultpath = 'programs'
default_data_path = 'data'

address_gas = ''
address_powersupply = 'ASRL11::INSTR'
address_multimeter = 'USB0::0x05E6::0x6500::04517856::INSTR'
PORT_gas = 'COM12'

buffer_size = 5


class Dummy():
    def __init__(self):
        pass

    def get_data(self):
    
        return {'dummy1': 1, 'dummy2': 2.5, 'dummy3': 1, 'dummy4': 2.5, 'dummy5': 5, 'dummy6': 2.5}

    def close(self):
        return False

class Experiment():
    def __init__(self):
        if test:
            dummy = Dummy()
            self.devices = {"dummy": dummy}
        else:
            powersupply = PowerSupply(address_powersupply)
            gas = Gas(address_gas)
            multimeter = Multimeter(address_multimeter)
            self.devices = {"gas": gas, "powersupply": powersupply,
                        "multimeter": multimeter}
            self.devices = { "multimeter":multimeter, "powersupply":powersupply}
            self.devices = {"powersupply":powersupply}
            self.devices = {"dummy":Dummy()}
        self.buffer_size = buffer_size  # change for experiments
        self.read_program()
        _name = program_path[:program_path.find(
            '.json')] + datetime.now().strftime("_%m-%d-%Y_%H-%M-%S")
        self.data_path = join(default_data_path, _name)
        Path(self.data_path).mkdir(parents=True, exist_ok=True)
        _name = f"results_{datetime.now().strftime('%m_%d_%Y %H-%M-%S')}.csv"
        self.file_entire_path = join(self.data_path, _name)
        self.bar = not_GUI.Console_monitor(self.program)

    def start(self):
        self.start_time = datetime.now()
        self.data_entire = []
        for step_id in self.program:
            self.step_id = step_id
            self.bar.new_program(self.step_id)
            self.set_parameters()
            self.step_loop()
        self.close_devices()
        doit()

    def close_devices(self):
        if test:
            self.devices['dummy'].close()
        else:
            for device in self.devices:
                self.devices[device].close()

    def set_parameters(self):
        if test:
            pass
        else:
            # powersupply
            self.devices['powersupply'].set_voltage(
                self.program[self.step_id]['voltage']['value'])
            self.devices['powersupply'].set_current(
                self.program[self.step_id]['current']['value'])
            self.devices['powersupply'].set_power(
                self.program[self.step_id]['power']['value'])
            self.devices['powersupply'].supply_on()

            # multimeter

            # gas
            self.devices['gas'].set_flow_ppm(
                self.program[self.step_id]['flow'], self.program[self.step_id]['flow'])
            self.devices['gas'].open_all_valves()

    def step_loop(self):
        self.i = 0
        self.interval = timedelta(
            seconds=(1/(self.program[self.step_id]['samplingrate']['value'])))
        self.step_start_time = datetime.now()
        self.last_fetched = self.step_start_time - self.interval
        # creating directory
        _name = f"step{str(self.step_id)}_{self.program[self.step_id]['name']}{datetime.now().strftime('%m_%d_%Y %H-%M-%S')}.csv"
        self.filepath = join(self.data_path, _name)
        self.data = []
        while datetime.now() <= self.step_start_time + timedelta(seconds=self.program[self.step_id]['duration']['value']):
            self.get_data()
            self.bar.update(self.latest_data)
        self.save_data(last=True)

    def get_data(self):
        this_time = datetime.now()
        if this_time >= self.last_fetched + self.interval:
            self.i += 1
            self.last_fetched = this_time
            self.latest_data = {'id': self.program[self.step_id]['name'], 'time': datetime.now().strftime('%m_%d_%Y %H-%M-%S'),
                                'timestamp': round_time(str(datetime.now() - self.step_start_time), 2)}
            # self.latest_data.update(self.devices['powersupply'].get_data())
            # self.latest_data.update(self.devices['multimeter'].get_data())
            # self.latest_data.update(self.devices['dummy'].get_data())
            if test:
                self.latest_data.update(self.devices['dummy'].get_data())
            else:
                for device in self.devices:
                    self.latest_data.update(self.devices[device].get_data())

            self.data.append(self.latest_data)
            self.data_entire.append(self.latest_data)
            self.save_data()

    # save data every 100 value, appends if exists, creates new if not

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

    # reading json with program

    def read_program(self):
        _path_program = join(programs_defaultpath, program_path)
        f = open(_path_program)
        self.program = json.load(f)
        print(f'reading {program_path}')
        f.close()

def round_time(string, dec):
    if string.find('.') >= 0:
        string = string.split('.')
        string = string[0]+'.' + \
            str(round(float('0.'+string[1]), dec)).split('.')[1]
    return string


if __name__ == '__main__':
    experiment = Experiment()
    experiment.start()
