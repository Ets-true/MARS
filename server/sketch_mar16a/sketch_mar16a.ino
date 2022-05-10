
/*
Keyestudio smart home Kit for Arduino
Project 8
Fan
http://www.keyestudio.com
*/
#include "LiquidCrystal_I2C.h"
#include <Servo.h>

LiquidCrystal_I2C lcd (0x27,16,2);
Servo window;
Servo door;

char inChar;
int tonepin = 3;

void setup () {
   Serial.begin(9600);
   Serial.setTimeout(1);
   pinMode (2, INPUT);
   pinMode (3, INPUT);
   pinMode (A0, INPUT);
   pinMode (A1, INPUT);
   pinMode (7, OUTPUT); //define D7 pin as output
   pinMode (6, OUTPUT); //define  D6 pin as output
   pinMode (5, OUTPUT);
   pinMode (tonepin, OUTPUT);
   window.attach (10);
   door.attach(9);
   window.write (0);
   door.write(0);
   lcd.init (); // initialize the lcd
   lcd.init (); // Print a message to the LCD.
   lcd.backlight ();
   lcd.setCursor (0,0);
}
void loop () {
   Serial.println("{ \"Motion\": "+String(digitalRead(2))+", \"CO2\": "+String(analogRead(A0))+", \"Illumination\": "+String(analogRead(A1))+", \"Moisture\": "+String(analogRead(3))+" }");
   if (Serial.available() > 0){
      inChar = Serial.read();
      if (inChar == 'e'){
        digitalWrite (7, LOW);
        digitalWrite (6, HIGH); // Reverse rotation of the motor
      }
      if (inChar == 'd'){
        digitalWrite (7, LOW);
        digitalWrite (6, LOW); // Reverse rotation of the motor
      }
      if (inChar == 'w'){
        window.write (180);
      }
      if (inChar == 'n'){
        window.write (0);
      }
      if (inChar == 'o'){
        door.write (180);
      }
      if (inChar == 'b'){
        door.write (0);
      }
      if (inChar == 'm'){
        analogWrite (5, 255);
      }
      if (inChar == 'p'){
        analogWrite (5, 0);
      }
      if (inChar == 'a'){
        String fans_char = Serial.readStringUntil('#');
        int fans_val = String(fans_char).toInt();
        digitalWrite(7, LOW);
        analogWrite(6, fans_val);
      }
      if (inChar == 'r'){
        String window_char = Serial.readStringUntil('#');
        int window_val = String(window_char).toInt();
        window.write (window_val);
      }
      if (inChar == 'v'){
        String door_char = Serial.readStringUntil('#');
        int door_val = String(door_char).toInt();
        door.write (door_val);
      }
      if (inChar == 'l'){
        String led = Serial.readStringUntil('#');
        int led_val = String(led).toInt();
        analogWrite (5, led_val);
      }
      if (inChar == 'q'){
        String window_char = Serial.readStringUntil('#');
        lcd.clear();
        lcd.print (window_char);
      }
      if (inChar == 'u'){
        tone (tonepin, HIGH);
      }
      if (inChar == 't'){
        noTone (tonepin);
      }
      if (inChar == 'f'){
        String frequency_char = Serial.readStringUntil('#');
        int frequency = String(frequency_char).toInt();
        tone (tonepin, frequency);
      }
   }
   else
    delay(500);
}
//
