from turtle import color
import pyvisa
from time import sleep
from colorama import Fore as cf


class Multimeter():
    def __init__(self, address):
        rm = pyvisa.ResourceManager()
        # print(rm.list_resources())
        print(cf.GREEN,"init multimeter", cf.RESET)
        self.client =  rm.open_resource(address)
        self.get_identity()
        self.reset()
        self.set_SCPI()
        self.set_DC()

    def get_identity(self):
        print(cf.RED, self.client.query("*IDN?"),cf.RESET)

    def set_SCPI(self):
        self.client.write('*LANG SCPI')
        print('using: ', cf.RED, self.client.query("*LANG?"), cf.RESET)
        
    def reset(self):
        self.client.write('*RST')
        
        
    def set_DC(self):
        self.client.write("SENS:FUNC 'VOLT:DC'")

    def read_voltage(self): 
        return float(self.client.query(":READ?"))
    
    def get_data(self):
        data = {}
        data['voltage_multimeter'] = self.read_voltage()
        return data

    def close(self):
        pass


if __name__ == '__main__':
    # multimeter = Multimeter('USB0::0x05E6::0x6500::04517856::INSTR')
    multimeter = Multimeter('USB0::0x05E6::0x6500::04517856::INSTR')
    sleep(1)
    for i in range(10):
        multimeter.read_voltage()
        sleep(0.5)
    
