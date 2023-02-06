# was ist der senke betrieb (Netzteil)?
# warum müssen die setter zwei mal aufgerufen werden?

import pyvisa
from time import sleep



class PowerSupply():
    def __init__(self, address):
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        # print(colorama.Fore.GREEN, 'init powersupply')
        # print(colorama.Fore.RESET)
        self.client =  rm.open_resource(address)
        self.reset()
        # self.get_info()


    def reset(self):
        self.client.write('*RST')
        self.client.write('SYST:LOCK ON')
        self.client.write('POW:STAG:AFT:REM AUTO')
        self.client.write('SYST:CONF:OUTP:REST AUTO')
        sleep(1)


    def get_info(self):
        string = self.client.query('*IDN?')
        print(string)



    def set_voltage(self, voltage):
        self.client.write(f'VOLT {float(voltage)}')
        self.client.write(f'VOLT {float(voltage)}') # warum klappt das erst beim zweiten mal?
        print(self.client.query('VOLTage?').split()[0])
        print(float(voltage))
        if float(self.client.query('VOLTage?').split()[0]) != float(voltage):
            print('error while setting voltage')

    def set_current(self, current):
        self.client.write(f'CURR {float(current)}')
        self.client.write(f'CURR {float(current)}') # warum klappt das erst beim zweiten mal?
        if float(self.client.query('CURRent?').split()[0]) != float(current):
            raise ValueError('error while setting current')

    def set_power(self, power):
        self.client.write(f'POW {float(power)}')
        self.client.write(f'POW {float(power)}') # warum klappt das erst beim zweiten mal?
        if float(self.client.query('POWer?').split()[0]) != float(power):
            raise ValueError('error while setting power')

    def set_input_resistance(self, resistance):
        self.client.write(f'POW {float(resistance)}')
        self.client.write(f'POW {float(resistance)}') # warum klappt das erst beim zweiten mal?
        if float(self.client.query('POWer?').split()[0]) != float(resistance):
            raise ValueError('error while setting input resistance')


    def get_voltage_set(self):
        string = self.client.query(f'VOLT?') 
        return float(string.split()[0])
        
    def get_current_set(self):
        string = self.client.query(f'CURR?')
        return float(string.split()[0])

    def get_power_set(self):
        string = self.client.query(f'POWER?')
        return float(string.split()[0])

    def get_voltage_actual(self):
        string = self.client.query(f'MEAS:VOLT?') 
        return float(string.split()[0])
        
    def get_current_actual(self):
        string = self.client.query(f'MEAS:CURR?')
        return float(string.split()[0])

    def get_power_actual(self):
        string = self.client.query(f'MEAS:POW?')
        return float(string.split()[0])

    def get_all_set(self):
        data =  {'power_set':self.get_power_set(),
            'current_set_ps':self.get_current_set(),
            'voltage_set_ps':self.get_voltage_set()}
        return data

    def get_all_actual(self):
        data =  {'power_actual':self.get_power_actual(),
        'current_actual_ps':self.get_current_actual(),
        'voltage_actual_ps':self.get_voltage_actual()}
        return data

    def get_all_actual_arr(self):
        string =  self.client.query(f'MEAS:ARR?') 
        return string.split(',')

    def get_data(self):
        try:
            data = self.get_all_actual() | self.get_all_set()
            return data
        except Exception as e:
            print(f'Error reading powersupply: {e}, returning empty dict')
            return {}

            

    def supply_on(self):
        self.client.write('OUTP ON')

    def supply_off(self):
        self.client.write('OUTP OFF')

    def get_errors(self):
        string = self.client.query('SYSTEM:ERROR:ALL?')
        return string.split(',')
    
    def close(self):
        self.supply_off()

    

    

if __name__ == '__main__':
    powersupply = PowerSupply('ASRL11::INSTR')
    # powersupply = PowerSupply('ASRL5::INSTR')
    i = 0
    while True:
        i += 1
        i = i%5
        powersupply.set_voltage(i)
        powersupply.set_current(10) # was ist der senke betrieb?
        powersupply.set_power(200)
        powersupply.set_input_resistance(10)
        powersupply.supply_on()
        sleep(0.1)
        print(powersupply.get_data())
        powersupply.get_errors()
        powersupply.get_data()
    