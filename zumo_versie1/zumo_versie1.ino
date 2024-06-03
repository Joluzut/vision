#include <Wire.h>
#include <Zumo32U4.h>
#include <TimerOne.h>
// Change next line to this if you are using the older Zumo 32U4
// with a black and green LCD display:
// Zumo32U4LCD display;
Zumo32U4OLED display;
Zumo32U4Motors motors;
Zumo32U4ButtonA buttonA;
const int fromNicla = 14; // PC7

String bitString = ""; // Global string to store bits

void setup() {
    pinMode(fromNicla, INPUT_PULLUP);
    display.init();
    display.clear();
  //     for (int speed = 0; speed <= 100; speed++)
  // {
  //   motors.setLeftSpeed(speed);
  //   motors.setRightSpeed(speed);
  //   delay(2);
  // }
}

void dataRead() {
    delayMicroseconds(500); // Small delay if necessary
    String bitString = "";
    String bitType = "";
    int signal = digitalRead(fromNicla);
    if (signal == LOW) {
        bitType += "0";
    } else {
        bitType += "1";
    }

   delayMicroseconds(500);// Small delay if necessary
    signal = digitalRead(fromNicla);
    if (signal == LOW) {
        bitType += "0";
    } else {
        bitType += "1";
    }
    
    delayMicroseconds(500);// Small delay if necessary
    signal = digitalRead(fromNicla);
    if (signal == LOW) {
        bitString += "0";
    } else {
        bitString += "1";
    }
    delayMicroseconds(500); // Small delay if necessary
    signal = digitalRead(fromNicla);
    if (signal == LOW) {
        bitString += "0";
    } else {
        bitString += "1";
    }
   delayMicroseconds(500); // Small delay if necessary
    signal = digitalRead(fromNicla);
    if (signal == LOW) {
        bitString += "0";
    } else {
        bitString += "1";
    }
     delayMicroseconds(500); // Small delay if necessary
    signal = digitalRead(fromNicla);
    if (signal == LOW) {
        bitString += "0";
    } else {
        bitString += "1";
    }
    delayMicroseconds(500);
        signal = digitalRead(fromNicla);
    if (signal == LOW) {
        bitString += "0";
    } else {
        bitString += "1";
    }
    delayMicroseconds(500);
        signal = digitalRead(fromNicla);
    if (signal == LOW) {
        bitString += "0";
    } else {
        bitString += "1";
    }
    delayMicroseconds(500);
    signal = digitalRead(fromNicla);
      if (signal == LOW) {
       display.clear();
        display.print(bitType);
       display.gotoXY(0, 1);
    display.print(bitString);
    checkType(bitType, bitString);
    } else {
       return;
    }
    
}

void loop() {
  delay(5000);
  while(1){
    int signal = digitalRead(fromNicla);
    if (signal == HIGH) {
        dataRead();
        
    }
  }
}
