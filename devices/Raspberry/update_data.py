# Add Phidgets Library
from Phidget22.Phidget import *
from Phidget22.Devices.LightSensor import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.Devices.VoltageRatioInput import *
import time
import json
from classes import *

# Create Phidgets sensors
lightSensor = LightSensor()
tempsensor1 = TemperatureSensor()
tempsensor2 = VoltageRatioInput()
tempsensor3 = VoltageRatioInput()
slider = VoltageRatioInput()

# Address Phidgets sensors
lightSensor.setHubPort(0)
tempsensor1.setHubPort(1)
tempsensor2.setHubPort(3)
tempsensor2.setIsHubPortDevice(True)
tempsensor3.setHubPort(4)
tempsensor3.setIsHubPortDevice(True)
slider.setHubPort(2)
slider.setIsHubPortDevice(True)

# Open Phidgets sensors
lightSensor.openWaitForAttachment(1000)
tempsensor1.openWaitForAttachment(1000)
tempsensor2.openWaitForAttachment(1000)
tempsensor3.openWaitForAttachment(1000)
slider.openWaitForAttachment(5000)

# Create Observable instances
temperature_observable = TemperatureObservable()
temperature_observable2 = TemperatureObservable()
temperature_observable3 = TemperatureObservable()
light_observable = LightObservable()
slider_observable = SliderObservable()

ls_observable = [temperature_observable,
                 temperature_observable2,
                 temperature_observable3,
                 light_observable,
                 slider_observable]

# Create Observer instances
temperature_observer = TemperatureObserver()
temperature_observer2 = TemperatureObserver()
temperature_observer3 = TemperatureObserver()
light_observer = LightObserver()
slider_observer = SliderObserver()

# Add Observers to Observables
temperature_observable.add_observer(temperature_observer)
temperature_observable2.add_observer(temperature_observer2)
temperature_observable3.add_observer(temperature_observer3)
light_observable.add_observer(light_observer)
slider_observable.add_observer(slider_observer)

# Variable pour le verrouillage de la machine à laver
machine_lock = False

# Variable pour la durée restante du cycle de lavage
remaining_wash_time = 0

# Méthode pour savoir si les données ont changées
def get_changed(observable):
    # On check si la variable has_changed a été mise à True
    if observable.has_changed:
        observable.has_changed = False
        return True
    else:
        return False
    
# Méthode qui met à jour les données du fichier json
def update_data_observer(user_input):
    global machine_lock
    global remaining_wash_time
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
    # Valeurs réelles
    else:
        temp_value_salon = temperature_observable.update_temperature(tempsensor1)
        temp_value_cuisine = temperature_observable.update_temperature(tempsensor1)
        temp_value_chambre = temperature_observable2.update_temperature(tempsensor2)
        temp_value_sdb = temperature_observable3.update_temperature(tempsensor3)
        light_value = light_observable.update_light(lightSensor)
        slider_value = slider_observable.update_slider(slider)
    # Gestion de la machine à laver
    if not machine_lock and remaining_wash_time == 0:
        if 0 < float(slider_value) < 0.33:
            mode = "eco"
            time_work = "30"
            power = "1250"
            remaining_wash_time=30
        elif 0.33 <= float(slider_value) < 0.66:
            mode = "normal"
            time_work = "60"
            power = "1500"
            remaining_wash_time=60
        elif 0.66 <= float(slider_value) < 1:
            mode = "long"
            time_work = "90"
            power = "1750"
            remaining_wash_time=90
        machine_lock = True
    elif remaining_wash_time == 0:
        machine_lock = False
        mode = ""
        time_work = ""
        power = ""
    else:
        mode = ""
        time_work = ""
        power = ""
    print("Temps de lavage : ", remaining_wash_time)

    # Initialisation de l'appartement
    # Exemple d'utilisation
    mach1 = Machine("machine-a-laver", mode, power, time_work)
    room1 = RoomData("salon", temp_value_salon, light_value)
    room2 = RoomData("cuisine", temp_value_cuisine, light_value)
    room3 = RoomData("salle-de-bain", temp_value_sdb, light_value)
    room4 = RoomData("chambre", temp_value_chambre, light_value)

    # Utilisez set_machine uniquement pour les pièces avec un appareil électroménager
    room3.set_machine(mach1)
    # Mes pièces
    rooms = [room1, room2, room3, room4]
    # L'appartement
    house = House(rooms)
    data2 = house.to_dict()
    # Pour simuler le temps qui passe (timework)
    if remaining_wash_time > 0:
        remaining_wash_time -= 10

    # Spécifiez le nom du fichier JSON dans lequel vous souhaitez enregistrer les données
    json_filename = "sensor_data.json"

    # Ouvrez le fichier en mode écriture et enregistrez les données au format JSON
    with open(json_filename, 'w') as json_file:
        json.dump(data2, json_file, indent=4)  # indent est utilisé pour une sortie formatée

    print(f"Données enregistrées dans {json_filename}")