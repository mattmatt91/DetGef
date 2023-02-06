import pyfirmata
import time


offset = 22
n_relais = 16


class Relaisboard():
    def __init__(self, address='COM17', n_relais=n_relais, offset=offset):
        self.board = pyfirmata.ArduinoDue(address)
        self.pins = [
            [self.board.get_pin(f'd:{i+offset}:o'), False] for i in range(n_relais)]
        self.close_all()

    def close_all(self):
        for i in range(len(self.pins)):
            self.pins[i][0].write(0)
            self.pins[i][1] = False

    def set_state(self, pin,  state):
        self.pins[pin][0].write(state)
        self.pins[pin][1] = state

    def close(self):
        self.board.exit()

    def get_state(self, *pins):
        result = {}
        for pin in pins:
            result[f'valve{pin}'] = self.pins[pin][1]
        return result


if __name__ == '__main__':
    relaisboard = Relaisboard('COM17')
    while True:
        for i in range(n_relais):
            relaisboard.set_state(i, True)
            time.sleep(0.1)
            # print(relaisboard.get_state(2,4, i))
            relaisboard.set_state(i, False)

    relaisboard.close()
