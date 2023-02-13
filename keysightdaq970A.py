import pyvisa
import time
import pandas as pd
from matplotlib import pyplot as plt

# PW datasheet A1s2d3f4!

address_keysightdaq970a = 'USB0::0x2A8D::0x5101::MY58018230::INSTR'
card_slot = 1


class KeysightDAQ970a():
    def __init__(self, address):
        self.i = 0
        self.rm = pyvisa.ResourceManager()
        self.client = self.rm.open_resource(address)
        self.client.timeout = 10000  # set a delay
        self.client.read_termination = '\n'
        print(self.client.query("*IDN?"))
        self.client.query('*RST;*OPC?;*CLS')
        self.client.write(":SYSTem:BEEPer:STATe 0")
        self.scanlist = "102,103"

    def get_errors(self):
        err = self.client.query("SYST:ERR?")
        return err

    def set_param(self):
        msg_conf = f"ACQ:RES DEF,DEF,DEF,(@102)\n"
        print(msg_conf)
        self.client.write(msg_conf)

        msg_conf = f"RES:APER:ENAB ON ,(@102)\n" 
        print(msg_conf)
        self.client.write(msg_conf)

        msg_conf = f"RES:APER 10E-01 ,(@102)\n"
        print(msg_conf)
        self.client.write(msg_conf)


    def get_data(self):
        t = time.time()
        self.i += 1
        msg = f"MEAS:RES? ,(@102)"
        print(msg)
        data = self.client.query(msg)
        data = [float(i) for i in data.split(',')]
        print(time.time()-t)
        return data

    def close(self):
        self.client.close()
        self.rm.close()


if __name__ == '__main__':
    keysightdaq970a = KeysightDAQ970a(address_keysightdaq970a)
    keysightdaq970a.set_param()
    print(keysightdaq970a.get_errors())
    print(keysightdaq970a.get_data())
    print(keysightdaq970a.get_errors())
    keysightdaq970a.close()
