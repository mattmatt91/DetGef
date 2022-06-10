import serial
from time import sleep
from pandas import json_normalize


port = 'COM12'
ppm0_H2 = 1000
cnls = {"air_dry":
        {"cnl": 1,
         "flow_max": 500,
         "flow_min": 500*0.05,
         "correction_factor": 1,
         },
        "air_wet":
            {"cnl": 2,
             "flow_max": 500,
             "flow_min": 500*0.05,
             "correction_factor": 1,
             },
            "H2":
            {"cnl": 3,
             "flow_max": 20,
             "flow_min": 20*0.05,
             "correction_factor": 2,
             },
        }


class Gas():

    def __init__(self, PORT):
        self.ser = serial.Serial(port=PORT,
                                 baudrate=9600,
                                 xonxoff=True, timeout=1,
                                 parity=serial.PARITY_ODD,
                                 stopbits=serial.STOPBITS_ONE,
                                 bytesize=serial.EIGHTBITS)
        self.flow = 0  # ml/min
        self.get_id()
        # set up cnls
        self.cnls = cnls
        self.set_gfc_all_cnl()
        self.close_all_valves()

    def reset(self):
        self.ser.write(self.convert_to_ascii('RE\r\n'))

    def get_id(self):
        self.ser.write(self.convert_to_ascii('ID R \r\n'))
        id = self.ser.readline().decode("utf-8")
        print(f'connected with: {self.ser.portstr}')
        print(f'gas controller: {id}')
        return id

    def close(self):
        self.close_all_valves()
        self.ser.close()

    # set
    def set_gfc(self, cnl, factor):  # values between 10 and 180, set flow for cnl
        self.ser.write(self.convert_to_ascii(f'GC{cnl}{factor}\r'))
        if self.get_gasfactor(cnl) != factor:  # check if value has benn set
            raise f'Failed to set gasfactor correction for cnl {cnl}'

    def set_gfc_all_cnl(self):
        for cnl in self.cnls:
            self.set_gfc(cnl, self.cnls[cnl]['correction_factor'])

    def set_flow_cnl(self, cnl, flow):  # values between 0 and 1000, set flow for cnl
        self.ser.write(self.convert_to_ascii(f'FS{cnl} {flow}\r\n'))
        if self.get_flow_set(cnl) != flow:  # check if value has benn set
            raise f'Failed to set flow for cnl {cnl}'

    def set_flow_ppm(self, flow, ppm):  # set the global flow and ppn of analyt
        self.flow = flow
        self.ppmH2 = ppm
        proportionH2 = (self.ppmH2/ppm0_H2)
        proportionWet = 0.5
        proportionDry = 1 - proportionH2 - proportionWet
        proportions = {'air_dry': proportionDry,
                       'air_wet': proportionWet, 'H2': proportionH2}
        mapped_values = self.proportions_to_promil(proportions)
        for cnl in self.cnls:
            self.set_flow_cnl(self.cnls[cnl]['cnl'], mapped_values[cnl])

    # valves
    def open_valve_cnl(self, cnl):  # set flow for cnl
        self.ser.write(self.convert_to_ascii(f'ON{cnl}\r\n'))

    def close_valve_cnl(self, cnl):  # , set flow for cnl
        self.ser.write(self.convert_to_ascii(f'OF{cnl}\r\n'))

    def open_all_valves(self):
        for cnl in self.cnls:
            self.open_valve_cnl(cnl)

    def close_all_valves(self):
        for cnl in self.cnls:
            self.close_valve_cnl(cnl)

    # get
    def get_flow_set(self, cnl):
        self.ser.write(self.convert_to_ascii(f'FS{cnl}R\r\n'))
        response = self.byteslist_to_float(
            self.ser.readlines().decode("utf-8"))
        # does this function work well?
        value = (response/1000) * self.cnls[cnl]['flow_max']
        return value

    def get_flow_act(self, cnl):  # returns the actual concentraion
        # check which format is returned !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.ser.write(self.convert_to_ascii(f'FL{cnl}\r\n'))
        response = self.byteslist_to_float(
            self.ser.readlines().decode("utf-8"))
        # does this function work well?
        value = (response/1000) * self.cnls[cnl]['flow_max']
        return value

    def get_gfc(self, cnl):
        self.ser.write(self.convert_to_ascii(f'GC{cnl}R\r\n'))
        response = self.byteslist_to_float(
            self.ser.readlines().decode("utf-8"))
        return response

    def get_flow_set_all_cnls(self):
        response = {}
        for cnl in self.cnls:
            response[cnl] = self.get_flow_set(cnl)
        return response

    def get_flow_act_all_cnls(self):
        response = {}
        for cnl in self.cnls:
            response[cnl] = self.get_flow_act(cnl)
        return response

    def get_gfc_all_cnls(self):
        response = {}
        for cnl in self.cnls:
            response[cnl] = self.get_gfc(cnl)
        return response

    def get_data(self, nested=False):
        response = {}
        response['flow_set'] = self.get_flow_set_all_cnls()
        response['flow_act'] = self.get_flow_act_all_cnls()
        response['gcf'] = self.get_flow_gcf_all_cnls()
        if not nested:
            response = json_normalize(response, '_').to_dict(
                orient='records')[0]  # prüfen warum indix
            return response

    def get_cnl_number(self, cnl):
        return self.cnls[cnl]['cnl']

    # calculate flows
    # convert proportions of gas  mapped values for mixer:
    def proportions_to_promil(self, proportions):
        mapped_values = {}
        for cnl in proportions:
            abs_value = proportions[cnl]*self.flow
            if self.cnls[cnl]['flow_min'] <= abs_value and self.cnls[cnl]['flow_max'] >= abs_value:
                mapped_values[cnl] = int(
                    (abs_value/self.cnls[cnl]['flow_max'])*1000)
            else:
                return Exception(f"flow ({abs_value}ml) out of range for cnl {cnl} ")
        return mapped_values

    @staticmethod
    def convert_to_ascii(text):
        ascii = [ord(i) for i in text]
        return ascii

    @staticmethod
    def byteslist_to_float(list_of_bytes):
        print(list_of_bytes)
        value = float(''.join([i.decode() for i in list_of_bytes]))
        print(value)
        return value


if __name__ == '__main__':
    gas = Gas(port)

    gas.set_flow_cnl_ppm(flow=80, ppm=50)
    gas.open_all_valves()
    for i in range(10):
        print(gas.get_data())
        sleep(1)
    gas.set_flow_cnl_ppm(flow=80, ppm=30)
    for i in range(10):
        print(gas.get_data())
        sleep(1)
    gas.close_all_valves(1)
    gas.close()
