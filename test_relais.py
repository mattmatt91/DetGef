
import pyfirmata
import time


board = pyfirmata.ArduinoDue('COM17')
offset = 22
pins = [board.get_pin(f'd:{i+offset}:o') for i in range(16)]
while True: 
    for pin in pins:
        pin.write(1)
    time.sleep(0.01)
    for pin in pins:
        pin.write(0)
    time.sleep(0.01)