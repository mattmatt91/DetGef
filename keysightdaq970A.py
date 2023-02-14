import pyvisa
import time
import pandas as pd
from matplotlib import pyplot as plt

# PW datasheet A1s2d3f4!address_keysightdaq970a = 'USB0::0x2A8D::0x5101::MY58018230::0::INSTR'# home
address_keysightdaq970a = 'USB0::0x2A8D::0x5101::MY58018230::INSTR'  # rhb


class KeysightDAQ970a():
    def __init__(self, address):
        self.i = 0
        self.rm = pyvisa.ResourceManager()
        self.client = self.rm.open_resource(address)
        self.client.timeout = 2000  # set a delay
        self.client.read_termination = '\n'
        self.scanlist = "(@201,202,203,204)"
        self.client.write("*RST")
        # print(self.client.query("*IDN?"))
        self.client.write(":SYSTem:BEEPer:STATe 0")

    def get_errors(self):
        err = self.client.query("SYST:ERR?")
        return err

    def set_param(self):
        self.client.write(f":ROUTe:SCAN  {self.scanlist}")
        self.client.write(
            f":CONFigure:FRESistance AUTO,DEFault, {self.scanlist}")
        self.client.write(f":SENSe:RESistance:RANGe:AUTO 1, {self.scanlist}")
        self.client.write(
            f":SENSe:RESistance:APERture:ENABle 1, {self.scanlist}")
        self.client.write(f":SENSe:RESistance:APERture 0.02, {self.scanlist}")
        self.client.write(f":SENSe:RESistance:NPLCycles 0.06, {self.scanlist}")

    def get_data(self):
        # self.client.write(":READ?")
        self.client.write(":INITiate")
        data = self.client.query(":FETCh?")
        data = [float(i) for i in data.split(',')]
        sensors = ['S1', 'S2', 'S3', 'S4']
        result = {}
        for sensor, value in zip(sensors, data):
            result[sensor + "_resistance_multimeter_measured"] = value
        return result

    def close(self):
        self.client.close()
        self.rm.close()


if __name__ == '__main__':
    keysightdaq970a = KeysightDAQ970a(address_keysightdaq970a)
    keysightdaq970a.set_param()
    print(keysightdaq970a.get_errors())
    for i in range(10):
        print(keysightdaq970a.get_data())
        print(keysightdaq970a.get_errors())
        time.sleep(1)
    keysightdaq970a.close()
