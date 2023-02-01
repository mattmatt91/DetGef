import pyfirmata
import time
# layout for arduino nano
list_relais = {0: {'pin': 'd:2:o', 'state': True},
          1: {'pin': 'd:3:o', 'state': True},
          2: {'pin': 'd:4:o', 'state': True},
          3: {'pin': 'd:5:o', 'state': True},
          4: {'pin': 'd:6:o', 'state': True},
          5: {'pin': 'd:7:o', 'state': True},
          6: {'pin': 'd:8:o', 'state': True},
          7: {'pin': 'd:9:o', 'state': True},
          8: {'pin': 'd:10:o', 'state': True},
          9: {'pin': 'd:11:o', 'state': True},
          10: {'pin': 'd:12:o', 'state': True},
          11: {'pin': 'd:13:o', 'state': True},
          12: {'pin': 'a:0:p', 'state': True},  # analog pins
          13: {'pin': 'a:1:p', 'state': True},
          14: {'pin': 'a:2:p', 'state': True},
          15: {'pin': 'a:3:p', 'state': True}
          }


class Relaisboard():
    def __init__(self, address):
        self.board = pyfirmata.Arduino(address)
        self.pins = self.init_pins()
        self.close_all()

    def init_pins(self):
        pins = {}
        for pin in list_relais:
            pins[pin] = self.board.get_pin(list_relais[pin]['pin'])
        return pins

    def close_all(self):
        for pin in self.pins:
            self.pins[pin].write(0)
            time.sleep(0.1)
            print(pin, self.pins[pin])
            self.pins[pin].write(1)
            time.sleep(0.1)
    
    def set_state(self, *pins): # tuple with pin and state
       for pin in pins:
           self.board.digital[self.pins[pin[0]]['pin']].write(not pin[1])
           self.pins[pin[0]]['state'] = not pin[1]

    def close(self):
        self.board.exit()
            
   # def get_state(self, *pins):
   #     response = {}
   #     for pin in pins:
   #         response[pin] =  not self.pins[pin]['state']
   #     return response

   # def get_all_states(self):
   #     response = {}
   #     for pin in self.pins:
   #         response[pin] =  not self.pins[pin]['state']
   #     return response


   # def set_states(self, pins): # tuple with pin and state
   #     for pin in pins:
   #         self.board.digital[self.pins[pin[0]]['pin']].write(not pin[1])
   #         self.pins[pin[0]]['state'] = not pin[1]


if __name__ == '__main__':

    relaisboard = Relaisboard('COM14')
    exit()
    while True:
        for i in relaisboard.pins:
                relaisboard.set_state((i,True))
        time.sleep(0.1)
        for i in relaisboard.pins:
            relaisboard.set_state((i,False))
        time.sleep(0.1)


 
    
    relaisboard.close()
