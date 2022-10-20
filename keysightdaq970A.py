import pyvisa 
import time

# PW datasheet A1s2d3f4!

address_keysightdaq970a = 'USB0::0x2A8D::0x5101::MY58018230::INSTR'


class KeysightDAQ970a():
    def __init__(self, address):
        rm = pyvisa.ResourceManager()
        self.client =  rm.open_resource(address)
        self.client.timeout=5000      #set a delay
        self.client.write("*CLS")     #clear 
        self.client.write("*RST") 
        self.channels = [11,12,13,14,15,16,17,18,19,20]
        self.client.write("CONF:RES (@111,112,113,114,115,116,117,118,119,120)")  # set channels to resustance
        # self.client.write(f'DISP:TEXT "DetGef"')
        

    def set_param(self):
        self.client.write("ACQ:RES DEF,DEF,DEF,(@111)")
        pass

    def get_data(self):
        self.client.write('READ?')
        vals = [float(i) for i in self.client.read().split(',')] 
        data = {}
        for i, n in zip(self.channels, vals):
            data[i]=n
        return data
                    



    def close(self):
        self.client.close()



keysightdaq970a = KeysightDAQ970a(address_keysightdaq970a)
# keysightdaq970a. set_param()
print(keysightdaq970a.get_data())
keysightdaq970a.close()