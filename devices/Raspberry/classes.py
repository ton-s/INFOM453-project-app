# Define Observable classes
class TemperatureObservable:
    def __init__(self):
        self.observers = []
        self.temperature = None
        self.last_notified_temperature = None
        self.seuil_changement_temperature = 0.5
        self.has_changed = False

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.temperature)

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
        if self.temperature is None or abs(new_temperature - self.last_notified_temperature) >= self.seuil_changement_temperature:
            self.temperature = new_temperature
            self.last_notified_temperature = new_temperature
            self.notify_observers()
            self.has_changed = True
        return self.temperature

class LightObservable:
    def __init__(self):
        self.observers = []
        self.illuminance = None
        self.last_notified_illuminance = None
        self.seuil_changement_luminance = 50
        self.has_changed = False

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

class SliderObservable:
    def __init__(self):
        self.observers = []
        self.voltage_ratio = None
        self.last_notified_voltage_ratio = None
        self.seuil_changement_slider = 0.1
        self.has_changed = False

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

# Define Observer classes
class TemperatureObserver:
    def update(self, temperature):
        print(f"Temperature: {temperature}")

class LightObserver:
    def update(self, illuminance):
        print(f"Illuminance: {illuminance}")

class SliderObserver:
    def update(self, voltage_ratio):
        print(f"Slider Voltage Ratio: {voltage_ratio}")

# Classes pour le fichier json
class Machine:
    def __init__(self, name, mode, power, time_work):
        self.name = name
        self.mode = mode
        self.power = power
        self.time_work = time_work

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

class RoomData:
    def __init__(self, room_name, temperature, light):
        self.data = {
            room_name: {
                "temperature": str(temperature),
                "light": str(light)
            }
        }

    def set_machine(self, machine):
        self.data[list(self.data.keys())[0]]["homeappliance"] = machine.get_machine()

    def to_dict(self):
        return self.data

class House:
    def __init__(self, rooms):
        self.rooms = rooms

    def to_dict(self):
        house_data = {}
        for room in self.rooms:
            room_dict = room.to_dict()
            room_name = list(room_dict.keys())[0]
            house_data[room_name] = room_dict[room_name]
        return house_data

"""TEST
# Exemple d'utilisation
mach1 = Machine("machine-a-laver", "eco", "1250", "30")
mach2 = Machine("machine-a-laver", "", "", "")
room1 = RoomData("salon", 22.5, 800)
room2 = RoomData("cuisine", 21.0, 700)
room3 = RoomData("salle-de-bain", 21.0, 700)
room4 = RoomData("chambre", 21.0, 700)

# Utilisez set_machine uniquement pour les pièces avec un appareil électroménager
room3.set_machine(mach1)
room2.set_machine(mach2)  # Pour une pièce avec une machine sans données

rooms = [room1, room2, room3, room4]

house = House(rooms)
house_json = house.to_dict()
print(type(house_json))"""
