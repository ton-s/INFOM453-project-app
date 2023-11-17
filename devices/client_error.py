import time
import json
from websockets.sync.client import connect
from test2 import *

# Configuration de l'URL WebSocket
websocket_url = "ws://localhost:8765/"
#websocket_url = "ws://192.168.1.14/ws/"

# On demande le mode d'exécution
mode = input("Execution mode (test/real): ")

while True:
    try:
        # Connexion aux websockets
        with connect(websocket_url) as websocket:
            while True:
                # Chargez les nouvelles données depuis le fichier JSON
                with open("sensor_data.json", 'r') as json_file:
                    # Mise à jour des données des capteurs
                    if mode == "test":
                        update_data_observer("test")
                    else:
                        update_data_observer("real")
                    # Chargez les nouvelles données
                    new_data = json.load(json_file)

                websocket.send(json.dumps(new_data))

                # Recevoir des données du serveur WebSocket
                received_data = websocket.recv()
                print(f"Received data from server: {received_data}")

                # Laps de temps qui détermine à quelle fréquence les données sont envoyées
                time.sleep(3)

    except Exception as e:
        print(f"Erreur de connexion WebSocket : {e}")
        print("Tentative de reconnexion dans 5 secondes...")
        time.sleep(5)  # Attendre un certain temps avant de réessayer la connexion
