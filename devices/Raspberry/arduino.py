import serial
import time

def send_intensity(intensity_led1, intensity_led2, intensity_led3):
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600)  # Assurez-vous de remplacer '/dev/ttyUSB0' par le bon port série
        time.sleep(2)  # Attendez que la connexion soit établie
        intensities = [intensity_led1, intensity_led2, intensity_led3]
        ser.write(bytes(intensities))  # Envoyer les intensités à l'Arduino
    except serial.SerialException as e:
        print(f"Une erreur s'est produite : {e}")
    # Pour être sûr que la connexion se ferme bien si une exception arrive ou pas
    finally:
        ser.close()

# Exemple d'utilisation avec des valeurs d'intensité arbitraires
send_intensity(50, 75, 100)
