
from multimeter import Multimeter
# from powersupply import PowerSupply
# from gas import Gas
import not_GUI 

from os.path import join
import json
from datetime import datetime, timedelta
from textwrap import indent
from unicodedata import numeric
import pandas as pd
from pathlib import Path
import os


program_path = 'test_program1.json'
programs_defaultpath = 'programs' 
default_data_path = 'data'

address_gas = ''
address_powersupply = ''
address_multimeter = 'USB0::0x05E6::0x6500::04517856::INSTR'


# gas = Gas(address_gas)
# powersupply = Powersupply(address_powersupply)
multimeter = Multimeter(address_multimeter)

class Experiment():
    def __init__(self, powersupply, multimeter, gas, dummy):
        # self.devices = {"gas":gas, "powersupply": powersupply, "multimeter":multimeter}
        self.devices = { "multimeter":multimeter}
        self.devices = {'dummy':dummy}
        self.read_program()
        _name = program_path[:program_path.find('.json')] + datetime.now().strftime("_%m-%d-%Y_%H-%M-%S")
        self.data_path = join(default_data_path, _name)
        Path(self.data_path).mkdir(parents=True, exist_ok=True)

    def start(self):
        self.set_parameters()
        self.start_time = datetime.now()
        for step_id in self.program:
            self.print_step(step_id)
            self.step_loop(step_id)


    def set_parameters(self):
        # powersupply
        pass
        # multimeter
        pass
        # gas
        pass

            

    def step_loop(self, step_id):
        self.step_start_time = datetime.now()
        # self.last_update = datetime.now() -timedelta(milliseconds=samplingrate)
        
        self.rate = int(1000*(1/(self.program[step_id]['samplingrate']['value'])))  
        self.last_saved = datetime.now() -timedelta(milliseconds=self.rate)
        
        #creating directory
        _name = f"step {str(step_id)} {self.program[step_id]['name']} {datetime.now().strftime('%m_%d_%Y %H-%M-%S')}.csv"
        self.filepath = join(self.data_path, _name)
        self.data = []

        
        while datetime.now() <= self.step_start_time + timedelta(seconds=self.program[step_id]['duration']['value']):
            self.get_data()
            self.safe_data()

    def get_data(self):
        this_time = datetime.now()
        if this_time >= self.last
        data = {'time': this_time.strftime('%m_%d_%Y %H-%M-%S'), 'timestamp': (this_time- self.step_start_time).strftime('%m_%d_%Y %H-%M-%S')}
        for device in self.devices:
            data.update(self.devices[device].get_data())
        self.data.append(data)
                
    
    def save_data(self):
        return 'data'
    
    def save_df(self):
        if datetime.now() >= timedelta(milliseconds=self.rate)+ self.last_saved:
            self.last_saved = datetime.now()
            _values = self.get_values_smoothed()
            _df = pd.concat([pd.DataFrame(), pd.Series(_values)]).T   
            
            if not os.path.isfile(self.filepath):
                _df.to_csv(self.filepath, header='column_names', index=False, sep='\t', decimal='.')
            else: 
                _df.to_csv(self.filepath, mode='a', header=False, index=False, sep='\t', decimal='.')
            self.data = self.data[len(self.data)-1:]

 

    def read_program(self):
        _path_program = join(programs_defaultpath, program_path)
        f = open(_path_program)
        self.program = json.load(f)
        f.close()










if __name__ == '__main__':
    experiment = Experiment('powersupply', multimeter, 'gas', )
    experiment.start()

  
        