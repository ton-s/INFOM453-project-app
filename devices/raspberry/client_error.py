import json
import asyncio
import websockets
from update_data import *
from arduino import *

# Configuration de l'URL WebSocket
#websocket_url = "ws://localhost:8765/"
#websocket_url = "ws://192.168.1.14/ws/"
websocket_url = "ws://192.168.74.144/ws/"

# Fonction asynchrone qui gère l'envoie de données (client)
async def main():
    while True:
        try:
            # Connexion aux websockets
            async with websockets.connect(websocket_url) as websocket:
                while True:
                    # Chargez les nouvelles données depuis le fichier JSON
                    with open("sensor_data.json", 'r') as json_file:
                        # Mise à jour des données des capteurs
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

                    # On vérifie si des données ont été modifiées avant de renvoyer le JSON
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
                        # On remet le string sous forme de dict
                        received_data = json.loads(received_data)
                        room = list(received_data.keys())[0]
                        light_intensity = received_data[room]["light"]
                        action_motor = received_data[room]["curtains"]
                        print(type(room), room, type(light_intensity), light_intensity, type(action_motor), action_motor)
                        # Caster en int pour pas récupérer un float
                        # Si on envoie une seule fois ça ne marche pas
                        send_intensity(room, int(light_intensity), action_motor)
                        send_intensity(room, int(light_intensity), action_motor)
                    except TimeoutError:
                        print("Timeout Error : Pas de messages reçus par le serveur")

        except Exception as e:
            print(f"Erreur de connexion WebSocket : {e}")
            print("Tentative de reconnexion dans 5 secondes...")
            await asyncio.sleep(5)

# Appel de la fonction principale
if __name__ == "__main__":
    asyncio.run(main())
