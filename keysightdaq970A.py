import pyvisa
import time


class KeysightDAQ970a():
    def __init__(self, address='TCPIP::K-DAQ970A-8230.local::5025::SOCKET'):
        rm = pyvisa.ResourceManager()
        # print(rm.list_resources())
        self.client = rm.open_resource(address)
        self.aper_toggle = False
        self.aperture = 0.06
        self.nplc = 1
        self.client.timeout = 10000  # set a delay
        self.client.read_termination = '\n'
        self.scanlist = "(@101) # ,102,103,104)"
        print(self.client.query("*IDN?"))
        self.client.write("*RST")
        self.client.write(":SYSTem:BEEPer:STATe 0")

    def set_up(self):
        # set resistance
        self.client.write(f"SENSe:RESistance ")

        # # set autorange
        # self.client.write("CONF:RES")
        # self.client.write("RES:RANG:AUTO 1")
# 
        # # aperture or nplc
        # if self.aperture:
        #     # disables aperture
        #     self.client.write(f"CONF:FRES")
        #     self.client.write(f"FRES:NPLC {self.nplc}")
        # else:
        #     self.client.write(
        #         f":SENSe:RESistance:APERture:ENABle 1")
        #     self.client.write(
        #         f":SENSe:RESistance:APERture {self.aperture}")

    def get_errors(self):
        err = self.client.query("SYST:ERR?")
        return err

    def get_data(self):
        # self.client.write(":READ?")
        sensors = ['S1', 'S2', 'S3', 'S4']
        try:
            data = self.client.query(f"READ? {self.scanlist}")
            data = [float(i) for i in data.split(',')]
        except:
             data = [None for _ in sensors]
        result = {}
        for sensor, value in zip(sensors, data):
            result[sensor + "_res_measured"] = value
        return result

    def close(self):
        self.client.close()


if __name__ == '__main__':
    keysightdaq970a = KeysightDAQ970a()
    print('after init: ',keysightdaq970a.get_errors())
    try:
        keysightdaq970a.set_up()
        print('after setup: ',keysightdaq970a.get_errors())
        print(keysightdaq970a.get_data())
        print('after fetch: ',keysightdaq970a.get_errors())
        if 0:
            for i in range(10):
                print(keysightdaq970a.get_data())
                print(keysightdaq970a.get_errors())
                time.sleep(1)
    finally:
            keysightdaq970a.close()
