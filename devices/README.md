# Appareils connectés

## Overview
Ce répertoire contient l'ensemble des programmes côté appareils connectés nécessaires pour collecter et transmettre des données telles que la température, la luminosité, et d'autres informations externe. Ces programmes sont conçus pour assurer la communication entre les appareils et l'application, permettant ainsi la collecte et l'envoi des données pour diverses analyses ou utilisations.

## Contenu
```
devices/
    arduino/ - Contient le code relatif à l'Arduino
        lights_and_motor.ino - *Fichier ino* qui contient le code de l'Arduino pour gérer les mises à jour des lampes dans chaque pièce, ainsi que le moteur pour ouvrir et fermer la fenêtre de la chambre
    raspberry/ - Contient le code relatif à l'Arduino
        arduino.py - *Fichier python* qui contient la fonction d'envoi des données depuis l'application à l'Arduino
        classes.py - *Fichier python* qui contient les classes permettant de mettre à jour les données récoltées par les différents capteurs si un seuil est dépassé          (Pattern Observer)
        client_error.py - *Fichier python* qui contient la connexion du côté client de l'application et donc permet au Raspberry de se connecter à l'applicaiton
        sensor_data.json - *Fichier json* qui contient les données des capteurs (température, luminosité, slider)
        server.py - *Fichier python TEST* qui contient la connexion du côté serveur pour tester la connexion client-serveur en local
        update_data.py - *Fichier python* qui contient toutes les fonctions nécessaires à la mise à jour des données dans le fichier json
```

