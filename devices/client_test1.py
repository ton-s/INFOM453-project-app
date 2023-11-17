#!/usr/bin/env python

import time
import json
from websockets.sync.client import connect
from data_stored import *
from sensor_observer import *

# Connexion aux websockets
# Local : localhost:8765
with connect("ws://192.168.1.14/ws/") as websocket:
    # On demande le mode d'exécution
    mode = input("Execution mode (test/real): ")
    
    # Initialiser les anciennes données avec des données vides
    old_data = {}
    
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
        
        # Vérifiez si les données ont changé
        if old_data != new_data:
            # Envoie des données uniquement si elles ont changé
            websocket.send(json.dumps(new_data))
            # Mettez à jour old_data avec les nouvelles données
            old_data = new_data
        
        # Laps de temps qui détermine à quelle fréquence les données sont envoyées
        time.sleep(5)
