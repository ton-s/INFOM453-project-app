#Add Phidgets Library
from Phidget22.Phidget import *
from Phidget22.Devices.LightSensor import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.Devices.VoltageRatioInput import *

#Create
lightSensor = LightSensor()
tempsensor1 = TemperatureSensor()
slider = VoltageRatioInput()

#Address
lightSensor.setHubPort(0)
#lightSensor.setIsHubPortDevice(True)
tempsensor1.setHubPort(1)
#tempsensor.setIsHubPortDevice(True)
slider.setHubPort(2)
slider.setIsHubPortDevice(True)

#Open
lightSensor.openWaitForAttachment(1000)
tempsensor1.openWaitForAttachment(1000)
slider.openWaitForAttachment(5000)

# Methods get
def get_value_temperature(sensor):
    result = sensor.getTemperature()
    return str(result)

def get_value_light():
    result = lightSensor.getIlluminance()
    return str(result)

def get_value_slider():
    result = slider.getVoltageRatio()
    return str(result)

temp_value_salon = get_value_temperature(tempsensor1)  # valeur de température du salon
temp_value_chambre = get_value_temperature(tempsensor1) 