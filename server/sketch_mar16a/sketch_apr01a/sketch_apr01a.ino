#include "AltSoftSerial.h"
AltSoftSerial BTserial;
// https://www.pjrc.com/teensy/td_libs_AltSoftSerial.html
 
char c=' ';
boolean NL = true;
 
void setup() 
{
   Serial.begin(9600);
   Serial.print("Sketch:   ");   Serial.println(__FILE__);
   Serial.print("Uploaded: ");   Serial.println(__DATE__);
   Serial.println(" ");
   BTserial.begin(9600);  
   Serial.println("BTserial started at 9600");
}
 
void loop()
{
   // Чтение из модуля Bluetooth и отправка в Arduino Serial Monitor:
   if (BTserial.available())
   {
      c = BTserial.read();
      Serial.write(c);
   } 
 
   // Чтение из Serial Monitor и отправка в модуль Bluetooth:
   if (Serial.available())
   {
      c = Serial.read();
      // Символы CR и LF (/r и /n) не отправляются к HM-10 в качестве
      // окончания строки:
      if (c!=10 & c!=13 ) 
      {
         BTserial.write(c);
      }
      // Эхо пользовательского ввода в главное окно.
      // Если новая строка, то печатается символ ">".
      if (NL) { Serial.print("\r\n>");  NL = false; }
      Serial.write(c);
      if (c==10) { NL = true; }
   }
}
