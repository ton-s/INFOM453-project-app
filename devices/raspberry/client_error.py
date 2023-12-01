import time
import json
import asyncio
import websockets
from update_data import *

# Configuration de l'URL WebSocket
websocket_url = "ws://localhost:8765/"
#websocket_url = "ws://192.168.1.14/ws/"

# On demande le mode d'exécution
mode = input("Execution mode (test/real): ")

def main_not_asnyc():
    while True:
        try:
            # Connexion aux websockets
            with websockets.connect(websocket_url) as websocket:
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
                    #received_data = asyncio.wait_for(websocket.recv(), timeout=3)
                    #print(f"Received data from server: {received_data}")

                    # Laps de temps qui détermine à quelle fréquence les données sont envoyées
                    #await asyncio.sleep(3)  # Utilisez asyncio.sleep pour éviter le blocage

        except Exception as e:
            print(f"Erreur de connexion WebSocket : {e}")
            print("Tentative de reconnexion dans 5 secondes...")
            time.sleep(5)

async def main():
    while True:
        try:
            # Connexion aux websockets
            async with websockets.connect(websocket_url) as websocket:
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

                    # On récupère les changements de chaque capteur
                    temp1_changed = get_changed(temperature_observable)
                    temp2_changed = get_changed(temperature_observable2)
                    temp3_changed = get_changed(temperature_observable3)
                    light_changed = get_changed(light_observable)
                    # On envoie les données du slider seulement quand il est pas vide
                    slider_changed = new_data["salle-de-bain"]["homeappliance"] != {}

                    # On vérifie si des données ont été modifiées avant de renvoyer le json
                    if (temp1_changed or 
                    temp2_changed or 
                    temp3_changed or 
                    light_changed or 
                    slider_changed):
                        await websocket.send(json.dumps(new_data))
                        print("!!! Data envoyées !!!")
                    else:
                        print("Pas besoin d'envoyer les anciennes valeurs")

                    # Recevoir des données du serveur WebSocket
                    try:
                        received_data = await asyncio.wait_for(websocket.recv(), timeout=5)
                        print(f"Received data from server: {received_data}")
                    except TimeoutError:
                        print("Timeout Error : Pas de messages reçus par le serveur")

                    time.sleep(2)

                    # Laps de temps qui détermine à quelle fréquence les données sont envoyées
                    #await asyncio.sleep(3)  # Utilisez asyncio.sleep pour éviter le blocage

        except Exception as e:
            print(f"Erreur de connexion WebSocket : {e}")
            print("Tentative de reconnexion dans 5 secondes...")
            await asyncio.sleep(5)

# Call function
if __name__ == "__main__":
    asyncio.run(main())
    #main_not_asnyc()
