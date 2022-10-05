from numpy import random
class TestDevice(object):
    
    def __init__(self, name):
        self.name = name
        self.value_1 = 0
        self.value_2 = 0
        print(f'init {self.name}')

    def set_value_1(self, value):
        self.value_1 = value

    def set_value_2(self, value):
        self.value_2 = value

    def measure_value(self):
        return random.random_sample()

    def close(self):
        del self 

    def __del__(self):
        print(f'closing {self.name}')


if __name__ == '__main__':
    my_device = TestDevice('testdevice')

    print(my_device.measure_value())

    my_device.close()



