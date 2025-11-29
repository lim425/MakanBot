#include <Wire.h>

// ---------------- Setup ----------------
void setup() {
  Serial.begin(9600);
  Serial.println("Start serial transmitter");

}

// ---------------- Loop ----------------
int i = 0;
void loop() {
  for (int i; i <= 100; i+=1){
    Serial.println("Done abc");
    delay(1000);
  }

}
