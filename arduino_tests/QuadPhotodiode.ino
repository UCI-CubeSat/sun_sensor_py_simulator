#include "filters.h"

#define photodiodePin1 A0
#define photodiodePin2 A1
#define photodiodePin3 A2
#define photodiodePin4 A3

KALMAN pin1(1, 1, 0.01); 
KALMAN pin2(1, 1, 0.01); 
KALMAN pin3(1, 1, 0.01); 
KALMAN pin4(1, 1, 0.01); 

float digitalToAnalog(float analogValue); 

void setup() {
  Serial.begin(9600);
  analogReadResolution(14);

  pinMode(photodiodePin1, INPUT);
  pinMode(photodiodePin2, INPUT); 
  pinMode(photodiodePin3, INPUT);
  pinMode(photodiodePin4, INPUT); 
  Serial.println("Begin"); 
}

void loop() {
  // float value1 = digitalToAnalog(pin1.updateEstimate(analogRead(photodiodePin1)));
  // float value2 = digitalToAnalog(pin2.updateEstimate(analogRead(photodiodePin2)));
  // float value3 = digitalToAnalog(pin3.updateEstimate(analogRead(photodiodePin3)));
  // float value4 = digitalToAnalog(pin4.updateEstimate(analogRead(photodiodePin4)));
  float value1 = analogRead(photodiodePin1); 
  float value2 = analogRead(photodiodePin2); 
  float value3 = analogRead(photodiodePin3); 
  float value4 = analogRead(photodiodePin4); 

  Serial.print(value1);
  Serial.print("\t");
  Serial.print(value2);
  Serial.print("\t");
  Serial.print(value3);
  Serial.print("\t");
  Serial.println(value4);

  delay(50);
}

float digitalToAnalog(float digitalValue){ 
  return((digitalValue * 5.00)/16383);
}
