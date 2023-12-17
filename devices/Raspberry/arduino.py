import serial
import time

def send_intensity(room, intensity_led, action_motor):
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600)
        time.sleep(2)

        # Création d'une liste avec les données
        data = [room, intensity_led, action_motor]

        # Envoyer les données à l'Arduino
        ser.write(bytes(str(data)))

    except serial.SerialException as e:
        print(f"Une erreur s'est produite : {e}")

    finally:
        # Fermer la connexion série
        ser.close()

# Exemple d'utilisation avec des valeurs arbitraires
send_intensity("chambre", 75, "false")  # Chambre 1, luminosité 75, rideau fermé
