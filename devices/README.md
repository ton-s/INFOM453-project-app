# Appareils connectés

## Overview
Ce répertoire contient l'ensemble des programmes côté appareils connectés nécessaires pour collecter et transmettre des données telles que la température, la luminosité, et d'autres informations externes. Ces programmes sont conçus pour assurer la communication entre les appareils et l'application, permettant ainsi la collecte et l'envoi des données pour diverses analyses ou utilisations.

## Contenu
```
devices/
    arduino/ - Contient le code relatif à l'Arduino
        lights_and_motor.ino - Fichier ino qui contient le code de l'Arduino pour gérer les mises à jour des lampes dans chaque pièce, ainsi que le moteur pour ouvrir et fermer la fenêtre de la chambre
    raspberry/ - Contient le code relatif au Raspberry Pi
        arduino.py - Fichier python qui contient la fonction d'envoi des données depuis l'application à l'Arduino
        classes.py - Fichier python qui contient les classes permettant de mettre à jour les données récoltées par les différents capteurs si un seuil est dépassé          (Pattern Observer)
        client_error.py - Fichier python qui contient la connexion du côté client de l'application et donc permet au Raspberry de se connecter à l'applicaiton
        sensor_data.json - Fichier json qui contient les données des capteurs (température, luminosité, slider)
        server.py - Fichier python TEST qui contient la connexion du côté serveur pour tester la connexion client-serveur en local
        update_data.py - Fichier python qui contient toutes les fonctions nécessaires à la mise à jour des données dans le fichier json
```

## Pré-requis pour utiliser les devices (Raspberry & Arduino)

```
pip install pyserial
pip install Phidget22
pip install asyncio
pip install websockets
```

## Initialisation du Raspberry Pi 4
Guide d'installation : https://www.raspberrypi.com/documentation/computers/getting-started.html 

## Lancement de la partie Raspberry Pi 4
- Lancer la connexion ssh (avec id = identifiant)
```shell
ssh id@raspberrypi.local
```
- Lancer le serveur VNC virtuel
```shell
vncserver-virtual
```
- Ouvrir l'application RealVNC Viewer (https://www.realvnc.com/fr/connect/download/viewer/)
- Ajouter une nouvelle session en saisissant l'adresse IP donné dans le terminal où le serveur virtuel a été lancé
```shell
192.162.x.x
```
- Connexion à l'interface du Raspberry Pi 4 (avec identifiant et mot de passe)
- Lancer le code depuis un IDE supportant Python (VSCode)
- Créer un environnement virtuel et l'activer
```shell
cd devices/raspberry
python -m venv env
./env/Scripts/activate (Windows)
source ./env/bin/activate (Linux)
```
- Installer les dépendances nécessaires (voir plus haut)
```shell
pip install ...
```
- Mettre à jour l'adresse IP pour les connexion websockets si besoin dans le fichier "client_error.py"
```shell
websocket_url = "ws://192.168.x.x/ws/"
```
- Lancer le fichier "client_error.py"
```shell
python client_error.py
```

## Initialisation de l'Arduino
Guide d'installation : https://www.arduino.cc/en/Guide 
