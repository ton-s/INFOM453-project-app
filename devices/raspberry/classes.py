# Définition des classes observables (Observable classes)

# Classe pour le capteur de température
class TemperatureObservable:
    def __init__(self):
        # Initialisation des attributs
        self.observers = []  # Liste d'observateurs
        self.temperature = None  # Température actuelle
        self.last_notified_temperature = None  # Dernière température notifiée aux observateurs
        self.seuil_changement_temperature = 0.5  # Seuil de changement de température pour déclencher une notification
        self.has_changed = False  # Indicateur de changement

    # Méthode pour ajouter un observateur
    def add_observer(self, observer):
        self.observers.append(observer)

    # Méthode pour retirer un observateur
    def remove_observer(self, observer):
        self.observers.remove(observer)

    # Méthode pour notifier tous les observateurs
    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.temperature)

    # Méthode pour mettre à jour la température en fonction des données du capteur
    def update_temperature(self, temp_sensor):
        # On vérifie à quel capteur on a affaire
        if "Temperature Sensor" in str(temp_sensor):
            new_temperature = temp_sensor.getTemperature()
        elif "Voltage Ratio Input" in str(temp_sensor):
            new_temperature = temp_sensor.getVoltageRatio()
            new_temperature = (new_temperature * 222.2) - 61.711
            # Arrondi à 2 décimales
            new_temperature = float("%.2f" % new_temperature)
        else:
            print("Capteur inconnu")
        
        # Vérifie si la température a changé de manière significative
        if self.temperature is None or abs(new_temperature - self.last_notified_temperature) >= self.seuil_changement_temperature:
            self.temperature = new_temperature
            self.last_notified_temperature = new_temperature
            self.notify_observers()  # Notifie les observateurs du changement
            self.has_changed = True  # Marque le changement
        return self.temperature

# Classe pour le capteur de luminosité
class LightObservable:
    def __init__(self):
        # Initialisation des attributs
        self.observers = []  # Liste d'observateurs
        self.illuminance = None  # Luminosité actuelle
        self.last_notified_illuminance = None  # Dernière luminosité notifiée aux observateurs
        self.seuil_changement_luminance = 50  # Seuil de changement de luminosité pour déclencher une notification
        self.has_changed = False  # Indicateur de changement

    # Mêmes méthodes que pour la luminosité
    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.illuminance)

    def update_light(self, lightSensor):
        new_illuminance = lightSensor.getIlluminance()
        if self.illuminance is None or abs(new_illuminance - self.last_notified_illuminance) >= self.seuil_changement_luminance:
            self.illuminance = new_illuminance
            self.last_notified_illuminance = new_illuminance
            self.notify_observers()
            self.has_changed = True
        return self.illuminance

# Classe pour le capteur de curseur (slider)
class SliderObservable:
    def __init__(self):
        # Initialisation des attributs
        self.observers = []  # Liste d'observateurs
        self.voltage_ratio = None  # Ratio de tension actuel du curseur
        self.last_notified_voltage_ratio = None  # Dernier ratio de tension notifié aux observateurs
        self.seuil_changement_slider = 0.1  # Seuil de changement du curseur pour déclencher une notification
        self.has_changed = False  # Indicateur de changement

    # Mêmes méthodes que pour la luminosité
    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.voltage_ratio)

    def update_slider(self, slider):
        new_voltage_ratio = slider.getVoltageRatio()
        if self.voltage_ratio is None or abs(new_voltage_ratio - self.last_notified_voltage_ratio) >= self.seuil_changement_slider:
            self.voltage_ratio = new_voltage_ratio
            self.last_notified_voltage_ratio = new_voltage_ratio
            self.notify_observers()
            self.has_changed = True
        return self.voltage_ratio

# Définition des classes observatrices (Observer classes)

# Classe observatrice pour la température
class TemperatureObserver:
    def update(self, temperature):
        print(f"Temperature: {temperature}")

# Classe observatrice pour la luminosité
class LightObserver:
    def update(self, illuminance):
        print(f"Illuminance: {illuminance}")

# Classe observatrice pour le curseur
class SliderObserver:
    def update(self, voltage_ratio):
        print(f"Slider Voltage Ratio: {voltage_ratio}")

# Définition des classes pour le fichier JSON

# Classe représentant une machine avec des données
class Machine:
    def __init__(self, name, mode, power, time_work):
        # Initialisation des attributs
        self.name = name
        self.mode = mode
        self.power = power
        self.time_work = time_work

    # Méthode pour obtenir les données de la machine sous forme de dictionnaire
    def get_machine(self):
        if self.mode or self.power or self.time_work:
            return {
                self.name: [
                    self.mode,
                    self.power,
                    self.time_work
                ]
            }
        else:
            return {}  # Retourne un dictionnaire vide si la machine n'a pas de données

# Classe représentant les données d'une pièce pour le fichier JSON
class RoomData:
    def __init__(self, room_name, temperature, light):
        # Initialisation des attributs
        self.data = {
            room_name: {
                "temperature": str(temperature),
                "light": str(light)
            }
        }

    # Méthode pour ajouter les données de la machine à l'objet
    def set_machine(self, machine):
        self.data[list(self.data.keys())[0]]["homeappliance"] = machine.get_machine()

    # Méthode pour obtenir les données de la pièce sous forme de dictionnaire
    def to_dict(self):
        return self.data

# Classe représentant les données d'une maison pour le fichier JSON
class House:
    def __init__(self, rooms):
        # Initialisation des attributs
        self.rooms = rooms

    # Méthode pour obtenir les données de la maison sous forme de dictionnaire
    def to_dict(self):
        house_data = {}
        for room in self.rooms:
            room_dict = room.to_dict()
            room_name = list(room_dict.keys())[0]
            house_data[room_name] = room_dict[room_name]
        return house_data