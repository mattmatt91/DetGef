

import pyvisa as visa
'''


Initialize the 34970A/72A and dirvers
load visa lib and open connection
Visa address used 'GPIB0::12::INSTR' can be found in Keysight Connection Expert
'''
rm = visa.ResourceManager()
v34970A_2 = rm.open_resource('USB0::0x2A8D::0x5101::MY58018230::INSTR')    

v34970A_2.timeout=5000      #set a delay
v34970A_2.write("*CLS")     #clear 
v34970A_2.write("*RST")     #reset 

'''Set Variables'''
scanIntervals = 10      #Delay in secs, between scans
numberScans = 3         #Number of scan sweeps to measure
channelDelay = 0.1      #Delay, in secs, between relay closure and measurement 
points = 0              #number of data points stored
voltage = 2.00          #voltage value to DAC from -12 to 12

'''
scanlist does not have to include all configured channels
In this example 103 is excluded to illustrate
'''
scanlist = "(@101,102,110:112)"
#setup channels configuration
v34970A_2.write("CONF:TEMP TC,T,(@101)")  
v34970A_2.write("CONF:TEMP TC,K,(@102)")  
v34970A_2.write("CONF:TEMP THER,5000,(@103)")  
v34970A_2.write("CONF:VOLT:DC (@110,111,112)")  
#setup scan list
v34970A_2.write("ROUTE:SCAN " + scanlist) 
v34970A_2.write("ROUTE:SCAN:SIZE?") 
numberChannels = int(v34970A_2.read())+1
#reading format
v34970A_2.write("FORMAT:READING:CHAN ON")
v34970A_2.write("FORMAT:READING:TIME ON")  
#channel delay
v34970A_2.write("ROUT:CHAN:DELAY " + str(channelDelay)+","+scanlist)
#setup when scanning starts and interval rate
v34970A_2.write("TRIG:COUNT "+str(numberScans)) 
v34970A_2.write("TRIG:SOUR TIMER")
v34970A_2.write("TRIG:TIMER " + str(scanIntervals))
#start the scan and retrieve the scan time

'''wait until there is a data available'''
points = 0
while (points==0):
    v34970A_2.write("DATA:POINTS?")
    points=int(v34970A_2.read())

'''
The data points are printed 
data, time, channel
'''
for chan in range(1, numberChannels):
    v34970A_2.write("DATA:REMOVE? 1")
    print (v34970A_2.read())
    points = 0
    #wait for data
    while (points==0):
        v34970A_2.write("DATA:POINTS?")
        points=int(v34970A_2.read())
#      
# '''Print Inserted cards'''
# v34970A_2.write("SYST:CTYPE? 100") 
# print(v34970A_2.read())  
# v34970A_2.write("SYST:CTYPE? 200") 
# print(v34970A_2.read())
# v34970A_2.write("SYST:CTYPE? 300") 
# print(v34970A_2.read() )
# 
# '''Write to DAC at port 200'''
# v34970A_2.write("SOURCE:VOLTAGE "+str(voltage)+" (@205)\n")     
# 
'''Close'''    
v34970A_2.close()
print('close instrument connection')