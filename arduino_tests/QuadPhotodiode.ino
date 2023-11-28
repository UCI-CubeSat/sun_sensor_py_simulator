#include "filters.h"

#define photodiodePin1 A0
#define photodiodePin2 A1
#define photodiodePin3 A2
#define photodiodePin4 A3

KALMAN pin1(1, 1, 0.01); 
KALMAN pin2(1, 1, 0.01); 
KALMAN pin3(1, 1, 0.01); 
KALMAN pin4(1, 1, 0.01); 

void setup() {
  Serial.begin(115200);
  pinMode(photodiodePin1, OUTPUT);
  pinMode(photodiodePin2, OUTPUT); 
  pinMode(photodiodePin3, OUTPUT);
  pinMode(photodiodePin4, OUTPUT); 
  Serial.println("Begin"); 
}

void loop() {
  int value1 = pin1.updateEstimate(analogRead(photodiodePin1));
  int value2 = pin2.updateEstimate(analogRead(photodiodePin2));
  int value3 = pin3.updateEstimate(analogRead(photodiodePin3));
  int value4 = pin4.updateEstimate(analogRead(photodiodePin4));

  Serial.print(value1);
  Serial.print("\t");
  Serial.print(value2);
  Serial.print("\t");
  Serial.print(value3);
  Serial.print("\t");
  Serial.println(value4);

  delay(50);
}
