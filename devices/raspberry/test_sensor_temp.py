from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.Devices.TemperatureSensor import *
import time

ch = TemperatureSensor()

ch.setHubPort(1)

ch.openWaitForAttachment(1000)



tc = VoltageRatioInput() # Handle for the thermocouple
ic = VoltageRatioInput() # Handle for the integrated temperature chip

#tc.setDeviceSerialNumber(672195)
ic.setDeviceSerialNumber(672195)
tc.setIsHubPortDevice(True)
ic.setIsHubPortDevice(True)
tc.setHubPort(0)
ic.setHubPort(2)

tc.openWaitForAttachment(5000)
ic.openWaitForAttachment(5000)

# Vous pouvez également extraire les informations spécifiques à partir de l'objet
#print("Temperature Sensor Details:", ch.getDeviceDetails())
#print("Voltage Ratio Input Details:", tc.getDeviceDetails())

sensor = tc

if "Temperature Sensor" in str(sensor):
    # C'est un capteur de température, faites quelque chose spécifique à la température
    print("C'est un capteur de température.")
elif "Voltage Ratio Input" in str(sensor):
    # C'est un capteur de voltage ratio, faites quelque chose spécifique à ce type de capteur
    print("C'est un capteur de voltage ratio.")
else:
    print("Type de capteur non reconnu.")

print(ch, tc)

while True:
    print(tc.getVoltageRatio())
    print(ic.getVoltageRatio())
    result = (tc.getVoltageRatio() * 222.2) - 61.111
    result2 = (tc.getVoltageRatio() * 222.2) - 61.111
    x="%.2f" % result
    x2="%.2f" % result2
    print(type(x))
    #print(result)
    print(x)
    print(x2)
    print(ch.getTemperature())

    time.sleep(2)