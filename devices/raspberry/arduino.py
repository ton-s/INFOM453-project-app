import serial
import time

# Data reçue : {room: {'light': 122.5, 'curtains': False}}
# room = 'chambre'(h), 'cuisine'(c), 'salon'(s), 'salle-de-bain'(b)

def send_intensity_test(intensity_led1, intensity_led2, intensity_led3):
    ser = serial.Serial('/dev/ttyACM0', 9600)  # Assurez-vous de remplacer '/dev/ttyUSB0' par le bon port série
    time.sleep(2)  # Attendez que la connexion soit établie
    ser.write(bytes([intensity_led1, intensity_led2, intensity_led3]))  # Envoyer les intensités à l'Arduino
    ser.close()

def send_intensity(room, intensity_led, action_motor):
    # On traite les inputs pour l'arduino
    # Rooms
    if room == "chambre":
        room_to_light = 'h'
    elif room == "cuisine":
        room_to_light = 'c'
    elif room == "salon":
        room_to_light = 's'
    elif room == "salle-de-bain":
        room_to_light = 'b'
    # Motor
    if action_motor == True:
        motor = "t"
    else:
        motor = "f"

    try:
        ser = serial.Serial('/dev/ttyACM0', 9600)
        time.sleep(2)

        print("Envoi des données à l'arduino")

        # Création d'une liste avec les données
        data = [ord(room_to_light), int(intensity_led), ord(motor)]

        # Envoyer les données à l'Arduino
        ser.write(bytes(data))

    except serial.SerialException as e:
        print(f"Une erreur s'est produite : {e}")

    finally:
        # Fermer la connexion série
        ser.close()
