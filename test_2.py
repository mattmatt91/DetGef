import sys
import pyvisa as visa  # PyVISA library

ADDRESS = 'USB0::0x2A8D::0x5101::MY58018230::INSTR'

rm = visa.ResourceManager()


FlexDCA = rm.open_resource(ADDRESS)
FlexDCA.timeout = 10000  # 10s
FlexDCA.write_termination = '\n'
FlexDCA.read_termination = '\n'
print('\nVISA termination string (write) set to newline: ASCII ',
      ord(FlexDCA.write_termination))
print('VISA termination string (read) set to newline: ASCII ',
      ord(FlexDCA.read_termination))
print('FlexDCA ID string:\n  ', FlexDCA.query('*IDN?'), flush=True)
FlexDCA.query('*RST;*OPC?')
# FlexDCA.write(':SYSTem:GTLocal')
FlexDCA.close()