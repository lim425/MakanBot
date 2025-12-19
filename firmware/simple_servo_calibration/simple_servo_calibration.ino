#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// Base: min=120 (0), max=570(180)
// Shoulder: min=130 (0), max=600(180)
// Elbow: min=120 (0), max=590(180)
// Wrist: min=140 (0), max=600(180)
// Gripper: min=125 (0), max=600(180)


// Start with safe range for 180° servo
int servoChannel = 0; // Channel where your servo is connected

void setup() {
  Serial.begin(9600);
  Serial.println("Servo Calibration Mode");
  Serial.println("Send a number from 150–600 in Serial Monitor to move servo");
  Serial.println("Try slowly until you find safe min and max without strain.");

  pwm.begin();
  pwm.setPWMFreq(50); // Standard 50 Hz for servos
  delay(500);
}

void loop() {
  // Check if you send something through Serial Monitor
  if (Serial.available()) {
    int val = Serial.parseInt();
    if (val > 0) {
      Serial.print("Moving servo to pulse length: ");
      Serial.println(val);
      pwm.setPWM(servoChannel, 0, val);
      delay(500);
    }
  }
}
