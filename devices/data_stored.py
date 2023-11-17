import json
from script import *

def update_data(user_input):
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
    else:
        # On récupère les valeurs des capteurs
        temp_value_salon = get_value_temperature(tempsensor1)  # valeur de température du salon
        temp_value_cuisine = get_value_temperature(tempsensor1)  # valeur de température de la cuisine
        temp_value_chambre = get_value_temperature(tempsensor1)  # valeur de température de la chambre
        temp_value_sdb = get_value_temperature(tempsensor1)  # valeur de température de la salle de bain
        light_value = get_value_light()  # valeur de luminosité
        slider_value = get_value_slider()  # valeur du slider

    # On choisit le mode de lavage
    if float(slider_value) > 0 and float(slider_value) < 0.33:
        mode = "eco"
        time = "30"
    elif float(slider_value) >= 0.33 and float(slider_value) < 0.66:
        mode = "normal"
        time = "60"
    elif float(slider_value) >= 0.66 and float(slider_value) < 1:
        mode = "long"
        time = "90"
    # On gère le cas où on ne veut pas mettre de data pour un test
    else:
        mode = "none"
        time = "0"

    # Créez un dictionnaire Python avec ces valeurs, en utilisant des clés pour chaque capteur
    data = {
        "salon": {
            "temperature": temp_value_salon,
            "light": light_value
            },
        "cuisine":{
            "temperature": temp_value_cuisine,
            "light": light_value
            },
        "chambre":{
            "temperature": temp_value_chambre,
            "light": light_value
            },
        "salle-de-bain":{
            "temperature": temp_value_sdb,
            "light": light_value,
            "homeappliance":{
                "machine-a-laver": [mode, time]
                }
            }
        }
    
    if data["salle-de-bain"]["homeappliance"]["machine-a-laver"][0] == "none":
        data["salle-de-bain"]["homeappliance"] = {}

    # Spécifiez le nom du fichier JSON dans lequel vous souhaitez enregistrer les données
    json_filename = "sensor_data.json"

    # Ouvrez le fichier en mode écriture et enregistrez les données au format JSON
    with open(json_filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)  # indent est utilisé pour une sortie formatée

    print(f"Données enregistrées dans {json_filename}")