#include <Servo.h>
#include <string.h>

Servo myservo;
int salleManger = 2;//jaune c & s
int chambre = 3;//rouge h
int salleBain = 4;//blanc b
int pos = 180;

void setup() {
    Serial.begin(9600);
    pinMode(salleManger, OUTPUT);
    pinMode(chambre, OUTPUT);
    pinMode(salleBain, OUTPUT);
    myservo.attach(1);
}

void loop() {

    if (Serial.available() >= 4) {
        // On traite le message
        char room = Serial.read();
        int intensity = Serial.read();
        char openWindow = Serial.read();

        // On allume la led en fonction de la pièce
        if (room == 'c' || room == 's') {
            analogWrite(salleManger, intensity);
        } else if (room == 'b') {
            analogWrite(salleBain, intensity);
        } else if (room == 'h') {
            analogWrite(chambre, intensity);
        }

        // On s'occupe du moteur
        if (openWindow == 't') {
          pos = 180;
          myservo.write(pos);
        }
        else {
          pos = 0;
          myservo.write(pos);
        }
    }
}
