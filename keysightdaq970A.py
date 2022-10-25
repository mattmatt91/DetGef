import pyvisa
import time
import pandas as pd
from matplotlib import pyplot as plt

# PW datasheet A1s2d3f4!

address_keysightdaq970a = 'USB0::0x2A8D::0x5101::MY58018230::INSTR'
card_slot = 2

class KeysightDAQ970a():
    def __init__(self, address):
        self.i = 0
        self.rm = pyvisa.ResourceManager()
        self.client = self.rm.open_resource(address)
        self.client.timeout = 10000  # set a delay
        self.client.read_termination = '\n'
        print(self.client.query("*IDN?"))
        self.client.query('*RST;*OPC?;*CLS')
        print(self.client.query('SYST:CTYP? 2'))
        
        self.scanlist = [card_slot*100+ i+1 for i in range(20)] # ,114,115,116,117,118,119,120]
        # set channels to resustance  # set channels to resustance
        self.client.write(":SYSTem:BEEPer:STATe 0")

    def set_param(self):
        pass




    def get_errors(self):
        err = self.client.query("SYST:ERR?")
        return err

    def get_data(self):
        query = f"MEAS:RES? 100,0.0001, (@{self.scanlist[0]}:{self.scanlist[-1]})"
        print(self.i)
        self.i +=1
        data = self.client.query(query)
        data= [float(i) for i in data.split(',')]
        return data


    def close(self):
        self.client.close()
        self.rm.close()



keysightdaq970a=KeysightDAQ970a(address_keysightdaq970a)
keysightdaq970a.set_param()
data = []
for i in range(10):
    time.sleep(1)
    keysightdaq970a.get_errors()
    data.append(keysightdaq970a.get_data())
    print('___________________________')
df = pd.DataFrame(data)
print(df)

keysightdaq970a.close()
