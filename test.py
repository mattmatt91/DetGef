
import pyvisa
rm = pyvisa.ResourceManager()
print(rm.list_resources())
address  = 'TCPIP0::169.254.6.147::5924::SOCKET'
address  = 'visa://K-DAQ970A-8230/ASRL1::INSTR'
client = rm.open_resource(address)
print(client.ask('*IDN?'))

# visa://hostname/ASRL1::INSTR
