import pyfirmata
import time

valves = {'valve0': {'pin': 2, 'state': True},
          'valve1': {'pin': 3, 'state': True},
          'valve2': {'pin': 4, 'state': True},
          'valve3': {'pin': 5, 'state': True},
          'valve4': {'pin': 6, 'state': True},
          'valve5': {'pin': 7, 'state': True},
          'valve6': {'pin': 8, 'state': True},
          'valve7': {'pin': 9, 'state': True},
          'valve8': {'pin': 10, 'state': True},
          'valve9': {'pin': 11, 'state': True},
          'valve10': {'pin': 12, 'state': True},
          'valve11': {'pin': 13, 'state': True}}


class Relaisboard():
    def __init__(self, address):
        self.board = pyfirmata.Arduino(address)
        self.num_pins = 11
        offset_pins = 2
        self.pins = valves
        self.close_all()

    def close_all(self):
        for i in self.pins:
            self.board.digital[self.pins[i]['pin']].write(True)

    def get_state(self, *pins):
        response = {}
        for pin in pins:
            response[pin] =  not self.pins[pin]['state']
        return response

    def get_all_states(self):
        response = {}
        for pin in self.pins:
            response[pin] =  not self.pins[pin]['state']
        return response

    def set_state(self, *pins): # tuple with pin and state
        for pin in pins:
            self.board.digital[self.pins[pin[0]]['pin']].write(not pin[1])
            self.pins[pin[0]]['state'] = not pin[1]

    def set_states(self, pins): # tuple with pin and state
        for pin in pins:
            self.board.digital[self.pins[pin[0]]['pin']].write(not pin[1])
            self.pins[pin[0]]['state'] = not pin[1]

    def close(self):
        self.board.exit()

if __name__ == '__main__':
    relaisboard = Relaisboard('COM7')

    print(relaisboard.get_state('valve1', 'valve2', 'valve11'))
    relaisboard.set_state(('valve1',True), ('valve2',True), ('valve11',False))
    time.sleep(1)
    print(relaisboard.get_state('valve1', 'valve2', 'valve11'))
    relaisboard.set_state(('valve1',False), ('valve2',True), ('valve11',True))
    time.sleep(1)
    print(relaisboard.get_all_states())
    
    relaisboard.close()
