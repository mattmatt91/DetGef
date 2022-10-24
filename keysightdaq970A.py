import pyvisa
import time

# PW datasheet A1s2d3f4!

address_keysightdaq970a = 'USB0::0x2A8D::0x5101::MY58018230::INSTR'
scanIntervals = 10  # Delay in secs, between scans
numberScans = 3  # Number of scan sweeps to measure
channelDelay = 0.1  # Delay, in secs, between relay closure and measurement
points = 0


class KeysightDAQ970a():
    def __init__(self, address):
        self.rm = pyvisa.ResourceManager()
        self.client = self.rm.open_resource(address)
        self.client.timeout = 5000  # set a delay
        print(self.client.query('*RST;*OPC?'))
        self.channels = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        self.scanlist = "(@111,112,113,114,115,116,117,118,119,120)"
        # set channels to resustance  # set channels to resustance
        self.client.write(":SYSTem:BEEPer:STATe 0")





    def set_param(self):
        pass

    def get_errors(self):
        print(self.client.query(":SYST:ERR?"))


    def get_data(self):
        result = self.client.query(f"MEAS? {self.scanlist}").split(',')
        for i in result:
            print(i)

    def close(self):
        self.client.close()
        self.rm.close()



keysightdaq970a = KeysightDAQ970a(address_keysightdaq970a)
keysightdaq970a.set_param()
for i in range(10):
    time.sleep(1)
    keysightdaq970a.get_errors()
    print(keysightdaq970a.get_data())
    
keysightdaq970a.close()
