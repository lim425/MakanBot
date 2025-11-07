#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pca = Adafruit_PWMServoDriver();

// Default pulse range (good starting point for most servos)
#define SERVOMIN 160
#define SERVOMAX 550

void setup() {
  Serial.begin(9600);
  pca.begin();
  pca.setPWMFreq(50);  // Standard 50Hz for hobby servos
  delay(1000);

  moveServo(0, 0);
  delay(2000);
  moveServo(0, 90);
  delay(2000);
  moveServo(0, 180);
  delay(2000);
}

void loop() {

}

// Function to map angle to PWM signal
void moveServo(uint8_t servoNum, int angle) {
  int pulse = map(angle, 0, 180, SERVOMIN, SERVOMAX);
  pca.setPWM(servoNum, 0, pulse);
  Serial.print("Servo "); Serial.print(servoNum);
  Serial.print(" -> "); Serial.print(angle);
  Serial.print("° | pulse: "); Serial.println(pulse);
}
