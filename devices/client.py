#!/usr/bin/env python

import time
import json
from websockets.sync.client import connect
from data_stored import *
#from sensor_observer import *

# Connexion aux websockets
# Local : ws://localhost:8765/
# abraod : ws://192.168.1.14/ws/ ws://138.48.255.213/ws/
with connect("ws://localhost:8765/") as websocket:
    # On demande le mode d'exécution
    mode = input("Execution mode (test/real): ")
    
    # Initialiser les anciennes données avec des données vides
    old_data = {
        "salon": {
            "temperature": "20.0",
            "light": "23.4397"
        },
        "cuisine": {
            "temperature": "20.0",
            "light": "23.4397"
        },
        "chambre": {
            "temperature": "20.0",
            "light": "23.4397"
        },
        "salle-de-bain": {
            "temperature": "20.0",
            "light": "23.4397",
            "homeappliance": {
                "machine-a-laver": [
                    "normal",
                    "60"
                ]
            }
        }
    }
    
    # Définissez les seuils de changement pour chaque capteur
    seuil_changement_temperature = 0.5
    seuil_changement_luminance = 50
    seuil_changement_slider = 0.1
    
    while True:
        # Chargez les nouvelles données depuis le fichier JSON
        with open("sensor_data.json", 'r') as json_file:
            # Mise à jour des données des capteurs
            # On spécifie le mode
            if mode == "test":
                update_data("test")
            else:
                update_data("real")
            # Chargez les nouvelles données
            new_data = json.load(json_file)
        
        # Vérifiez si les données ont changé de manière significative
        temperature_changed = False
        luminance_changed = False
        slider_changed = False
        # On va chercher les éléments du json pour voir s'ils ont bougés selon le seuil
        for room, sensors in new_data.items():
            for sensor, values in sensors.items():
                if sensor == "temperature" and "temperature" in old_data.get(room, {}):
                    temperature_diff = abs(float(values) - float(old_data[room]["temperature"]))
                    if temperature_diff >= seuil_changement_temperature:
                        temperature_changed = True
                
                if sensor == "light" and "light" in old_data.get(room, {}):
                    luminance_diff = abs(float(values) - float(old_data[room]["light"]))
                    if luminance_diff >= seuil_changement_luminance:
                        luminance_changed = True
                
                if sensor == "homeappliance" and "homeappliance" in old_data.get(room, {}):
                    print("1", old_data[room]["homeappliance"])
                    print("2", values)
                    print("3", old_data[room]["homeappliance"] == values)

                    if old_data[room]["homeappliance"] == values:
                        #new_data["machine-a-laver"]["homeappliance"] = {}
                        old_data["machine-a-laver"]["homeappliance"] = {}
                        slider_changed = True
                    print("*")
                    if old_data[room]["homeappliance"] != {} and values != {}:
                        print("**")
                        slider_diff = abs(float(values["machine-a-laver"][1]) - float(old_data[room]["homeappliance"]["machine-a-laver"][1]))
                        if slider_diff >= seuil_changement_slider:
                            print("***")
                            slider_changed = True
                    else:
                        print("*_*")
                        slider_changed = False
                    
                    
        
        if temperature_changed or luminance_changed or slider_changed:
            # Envoie des données uniquement si des changements significatifs sont détectés
            websocket.send(json.dumps(new_data))
            print("data changed !")
            print(new_data)
            print("data sended !!!")
            # Mettez à jour old_data avec les nouvelles données
            old_data = new_data
        else:
            print("data unchanged...")
            print(new_data)
        
        # Laps de temps qui détermine à quelle fréquence les données sont envoyées
        time.sleep(5)
