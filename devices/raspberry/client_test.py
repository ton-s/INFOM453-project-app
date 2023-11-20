#!/usr/bin/env python

import time
import json
from websockets.sync.client import connect
from sensor_observer import *


# Connexion aux websockets
# Local : localhost:8765
with connect("ws://localhost:8765") as websocket:
    # On demande le mode d'exécution
    mode = input("Execution mode (test/real): ")
    while(True):
        # Code pour charger les données depuis un fichier JSON
        with open("test.json", 'r') as json_file:
            old_data = json.load(json_file)
        # Mise à jour des données des capteurs
        # On spécifie le mode
        if mode == "test":
            print("test")
            update_data_with_seuil("test")
        else:
            print("eral")
            update_data_with_seuil("real")
        # Chargement des data
        with open("test.json", 'r') as json_file:
            new_data = json.load(json_file)
        # Envoie des données
        if old_data != new_data:
            websocket.send(json.dumps(new_data))

        # Mettez à jour old_data avec new_data pour la prochaine itération
        old_data = new_data
        # Laps de temps qui détermine à quelle fréquence sont envoyées les data
        time.sleep(5)