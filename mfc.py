Skip to content
Product
Solutions
Open Source
Pricing
Search
Sign in
Sign up
mattmatt91
/
DetGef
Public
Code
Issues
Pull requests
Actions
Projects
Security
Insights
DetGef/mfc.py /
@mattmatt91
mattmatt91 Add files via upload
Latest commit 0b5af33 4 days ago
 History
 1 contributor
132 lines (93 sloc)  3.7 KB

from distutils.log import debug
from msilib.schema import Error
from urllib import response
from pyModbusTCP.client import ModbusClient # Modbus TCP Client
from pyModbusTCP import utils 
import struct
import os, time
from ast import literal_eval
import converters




def ints_to_float(arr):
    a = arr[0].to_bytes(2, "big")
    b = arr[1].to_bytes(2, "big")
    arr = a+b
    aa = bytearray(arr)
    return(struct.unpack('>f', aa)[0])

def ints_to_long(arr):
    a = arr[0].to_bytes(2, "big")
    b = arr[1].to_bytes(2, "big")
    arr = a+b
    aa = bytearray(arr)
    return(struct.unpack('>l', aa)[0])

def float_to_ints(flo):
    arr = struct.pack('>f',flo)
    a = arr[:2]
    b = arr[2:]
    int_a = int.from_bytes(a, "big")  
    int_b = int.from_bytes(b, "big")  
    return [int_a, int_b]




class MFC():
    def __init__(self, host, port, max_flow):
        self.bus = ModbusClient(host=host, port=port, auto_open=True)
        time.sleep(0.2) 
        self.bus.open()
        self.max_flow = max_flow
        self.reset()
     
    def open_valve(self,state):
        self.bus.write_single_coil(int('0xE001', 16), state)

    def close_valve(self,state):
        self.bus.write_single_coil(int('0xE002', 16), state)

    def valve_state(self):
        return self.bus.read_coils(int('0xE001', 16), bit_nb=1)

    def reset(self):
        self.bus.write_single_coil(int('0xE000', 16), '0xFF00h')
        time.sleep(1)
        self.bus.write_single_coil(int('0xE000', 16), '0x0000')

    def zero_flow(self):
        self.bus.write_single_coil(int('0xE003', 16), '0xFF00h')

    def get_temp(self):
        response = self.bus.read_input_registers(int('0x4002', 16), 2)
        return ints_to_float(response)

    def get_flow_total(self):
        response = self.bus.read_input_registers(int('0x400A', 16), 2)
        return ints_to_long(response)

    def get_flow(self):
        response = self.bus.read_input_registers(int('0x4000', 16), 2)
        return ints_to_float(response)  

    def get_valve_pos(self):
        response =  self.bus.read_input_registers(int('0x4004', 16), 2)
        return ints_to_float(response)


    def get_point(self):
        response = self.bus.read_holding_registers(int('0xA000', 16), 2)
        return ints_to_float(response)

    def set_point(self, flo): # set ccm from 0 to 1000
        if flo > self.max_flow:
            raise ValueError("flow can't be bigger than max_flow")
        flo_rel = flo/self.max_flow
        data = float_to_ints(flo_rel)
        self.bus.write_multiple_registers(int('0xA000', 16), data)
    


if __name__ == '__main__':
    host="192.168.2.100"
    port=502
    max_flow = 1000

    mfc = MFC(host, port, max_flow)
    # mfc.zero_flow()

    # open close valve
    mfc.open_valve(1)
    print(mfc.valve_state())
    time.sleep(1)
    mfc.close_valve(0)
    print(mfc.valve_state())
    
    print(mfc.get_temp())
    print(mfc.get_flow())
    print(mfc.get_flow_total())

    mfc.set_point(100)
    print(mfc.get_point())
    print(mfc.get_valve_pos())







# https://pymodbustcp.readthedocs.io/en/latest/package/module_utils.html#module-pyModbusTCP.utils

# Flow Set Point write requires a 4 byte hex value input derived from a Decimal floating point value to a
# 32 bit Hex representation based upon IEEE754 Standard for Floating Point Arithmetic.

#Flow, Temperature, Valve Position, and Flow Hours when queried will return a 4 byte hex value that
# can be converted into decimal using a 32 bit precision Hex representation to Decimal conversion
# based upon IEEE754 Standard for Floating Point Arithmetic. Flow Total when queried returns a 4
# byte long interger.