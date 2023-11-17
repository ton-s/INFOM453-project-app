from Phidget22.Phidget import *
from Phidget22.Devices.LightSensor import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.Devices.VoltageRatioInput import *
import time
import json


def save_sensor_data(sensor_data):
    # Spécifiez le nom du fichier JSON dans lequel vous souhaitez enregistrer les données
    json_filename = "test.json"
    
    # Ouvrez le fichier en mode écriture et enregistrez les données au format JSON
    with open(json_filename, 'w') as json_file:
        json.dump(sensor_data, json_file, indent=4)  # indent est utilisé pour une sortie formatée


def update_data_with_seuil(user_input):

    # On gère le cas où on veut donner les data nous même (Testing)
    if user_input == "test":
        # On demande la température de chaque pièce
        print("Salon")
        temp_value_salon = input("Enter the temperature (°C) : ")
        print("Cuisine")
        temp_value_cuisine = input("Enter the temperature (°C) : ")
        print("Chambre")
        temp_value_chambre = input("Enter the temperature (°C) : ")
        print("Salle de bain")
        temp_value_sdb = input("Enter the temperature (°C) : ")
        light_value = input("Enter the brightness (Lumens) : ")

        slider_value = input("Enter the slider value (%) : ")
        # On choisit le mode de lavage
        if float(slider_value) <= 0.33:
            mode = "eco"
        elif float(slider_value) > 0.33 and float(slider_value) <= 0.66:
            mode = "normal"
        else:
            mode = "long"

        sensor_data = {
            "salon": {
                "temperature": temp_value_salon,
                "light": light_value
            },
            "cuisine": {
                "temperature": temp_value_cuisine,
                "light": light_value
            },
            "chambre": {
                "temperature": temp_value_chambre,
                "light": light_value
            },
            "salle-de-bain": {
                "temperature": temp_value_sdb,
                "light": light_value,
                "homeappliance": {
                    "machine-a-laver": [
                        mode,
                        slider_value
                    ]
                }
            }
        }

        save_sensor_data(sensor_data)

    else:
        
        # Créez un dictionnaire pour stocker les valeurs des capteurs
        sensor_data = {
            "salon": {
                "temperature": "19.56",
                "light": "361.28"
            },
            "cuisine": {
                "temperature": "19.56",
                "light": "361.28"
            },
            "chambre": {
                "temperature": "19.56",
                "light": "361.28"
            },
            "salle-de-bain": {
                "temperature": "19.56",
                "light": "361.28",
                "homeappliance": {
                    "machine-a-laver": [
                        "eco",
                        "0.1799"
                    ]
                }
            }
        }

        # Définissez les seuils de changement pour chaque capteur
        seuil_changement_illuminance = 50
        seuil_changement_temperature = 0.5
        seuil_changement_slider = 0.1
        
        def onIlluminanceChange(self, illuminance):
            changement = abs(illuminance - float(sensor_data["salon"]["light"]))
            
            if changement >= seuil_changement_illuminance:
                print("Illuminance: " + str(illuminance))
                sensor_data["salon"]["light"] = illuminance
                sensor_data["cuisine"]["light"] = illuminance
                sensor_data["chambre"]["light"] = illuminance
                sensor_data["salle-de-bain"]["light"] = illuminance
                save_sensor_data(sensor_data)

        def onTemperatureChange(self, temperature):
            changement_temperature = abs(temperature - float(sensor_data["salon"]["temperature"]))
            
            if changement_temperature >= seuil_changement_temperature:
                print("Temperature: " + str(temperature))
                sensor_data["salon"]["temperature"] = temperature
                sensor_data["cuisine"]["temperature"] = temperature
                sensor_data["chambre"]["temperature"] = temperature
                sensor_data["salle-de-bain"]["temperature"] = temperature
                save_sensor_data(sensor_data)

        def onVoltageRatioChange(self, voltageRatio):
            changement_slider = abs(voltageRatio - float(sensor_data["salle-de-bain"]["homeappliance"]["machine-a-laver"][1]))
            
            if changement_slider >= seuil_changement_slider:
                print("Slider Value: " + str(voltageRatio))
                sensor_data["salle-de-bain"]["homeappliance"]["machine-a-laver"][1] = voltageRatio
                # On choisit le mode de lavage
                if float(voltageRatio) <= 0.33:
                    sensor_data["salle-de-bain"]["homeappliance"]["machine-a-laver"][0] = "eco"
                elif float(voltageRatio) > 0.33 and float(voltageRatio) <= 0.66:
                    sensor_data["salle-de-bain"]["homeappliance"]["machine-a-laver"][0] = "normal"
                else:
                    sensor_data["salle-de-bain"]["homeappliance"]["machine-a-laver"][0] = "long"
                save_sensor_data(sensor_data)
        
        light_sensor = LightSensor()
        light_sensor.setOnIlluminanceChangeHandler(onIlluminanceChange)
        light_sensor.open()

        temperature_sensor = TemperatureSensor()
        temperature_sensor.setOnTemperatureChangeHandler(onTemperatureChange)
        temperature_sensor.open()

        slider_sensor = VoltageRatioInput()
        slider_sensor.setHubPort(2)
        slider_sensor.setIsHubPortDevice(True)
        slider_sensor.setOnVoltageRatioChangeHandler(onVoltageRatioChange)
        slider_sensor.open()
        
        #while True:
         #  time.sleep(1)

#update_data_with_seuil("real")