# total bytes 256  modbus message
# 1 byte slave id, functioncode 1 byte, 0-252 bytes message, crc 2 bytes
# functioncode is number from table 

from pymodbus.client.sync import ModbusTcpClient

from time import sleep

host = '192.168.2.100'  #ip of your raspberry pi
client = ModbusTcpClient(host)

client.connect()

wr = client.read_coils(0x06)
print(wr)
# sleep(1)


# create client object
client = ModbusSerial(host)

# connect to device
client.connect()

# set/set information
rr = client.read_coils(0x01)
client.write_coil(0x01, 10)

# disconnect device
client.close()