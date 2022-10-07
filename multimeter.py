from turtle import color
import pyvisa
from time import sleep



class Multimeter():
    def __init__(self, address):
        rm = pyvisa.ResourceManager()
        # print(rm.list_resources())
        # print(cf.GREEN,"init multimeter", cf.RESET)
        self.client =  rm.open_resource(address)
        # self.get_identity()
        self.reset()
        self.set_SCPI()
        self.set_resistance()

    def get_identity(self):
        print(cf.RED, self.client.query("*IDN?"),cf.RESET)

    def set_SCPI(self):
        self.client.write('*LANG SCPI')
        # print('using: ', cf.RED, self.client.query("*LANG?"), cf.RESET)
        
    def reset(self):
        self.client.write('*RST')
        
    def set_voltage_DC(self):
        self.client.write("SENS:FUNC 'VOLT:DC'")

    def read_value(self): 
        return float(self.client.query(":READ?"))
    
    def set_resistance(self): # set multimeter to measure resistance
        self.client.write("SENS:FUNC 'RES'")


    def set_resistance(self): # set multimeter to measure resistance
        self.client.write("SENS:FUNC 'RES'")
        return float(self.client.query(":READ?"))

    def get_data(self):
        try:
            data = {}
            data['resistance_multimeter_measured'] = self.read_value()
            return data
        except Exception as e:
            print(f'Error reading multimeter: {e}, returning empty dict')
            return {}

    def close(self):
        pass


if __name__ == '__main__':
    multimeter = Multimeter('USB0::0x05E6::0x6500::04544803::INSTR')
    multimeter.set_resistance()
    sleep(1)
    for i in range(1000):
        print(multimeter.read_value())

        sleep(0.01)
    
