#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// ---------------- Servo Configuration ----------------
struct ServoData {
  const char* name;
  int channel;
  int servoMin;
  int servoMax;
  int currentAngle;
};

ServoData servos[] = {
  {"BASE", 0, 120, 570, 90},
  {"SHOULDER", 1, 130, 600, 180},
  {"ELBOW", 2, 280, 620, 5},
  {"WRIST", 3, 140, 600, 90},
  {"GRIPPER", 4, 125, 600, 0},
  
};

const int NUM_SERVOS = sizeof(servos) / sizeof(servos[0]);

// ---------------- Helper Functions ----------------
int angleToPulse(int servoIndex, int angle) {
  return map(angle, 0, 180, servos[servoIndex].servoMin, servos[servoIndex].servoMax);
}

void moveServo(int servoIndex, int targetAngle, int stepDelay = 50) {

  int current_angle = servos[servoIndex].currentAngle;
  int step = (targetAngle > current_angle) ? 1 : -1;

  // Move gradually 1° at a time until target reached
  for (int angle = current_angle; angle != targetAngle; angle += step) {
    int pulse = angleToPulse(servoIndex, angle);
    pwm.setPWM(servos[servoIndex].channel, 0, pulse);
    servos[servoIndex].currentAngle = angle; // Update current angle
    delay(stepDelay); // Control movement speed
  }

  // Ensure final position reached exactly
  int pulse = angleToPulse(servoIndex, targetAngle);
  pwm.setPWM(servos[servoIndex].channel, 0, pulse);
  servos[servoIndex].currentAngle = targetAngle;
}

// ---------------- Setup ----------------
void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(50);
  delay(500);

  for (int i = 0; i < NUM_SERVOS; i++) {
    int pulse = angleToPulse(i, servos[i].currentAngle);
    pwm.setPWM(servos[i].channel, 0, pulse);
  }

  Serial.println("Robotic Arm Ready!");
  Serial.println("Enter: <servo_channel> <angle>");
  Serial.println("Example: 0 90");
}

// ---------------- Loop ----------------
void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n'); // read until newline
    Serial.println(input);
    input.trim(); // remove spaces/newlines

    if (input.length() > 0) {
      int spaceIndex = input.indexOf(' ');
      if (spaceIndex == -1) {
        Serial.println("Invalid format. Use: <channel> <angle>");
        return;
      }

      int channel = input.substring(0, spaceIndex).toInt();
      int targetAngle = input.substring(spaceIndex + 1).toInt();

      if (channel < 0 || channel >= NUM_SERVOS) {
        Serial.println("Error: Invalid servo channel!");
        return;
      }

      if (targetAngle < 0 || targetAngle > 180) {
        Serial.println("Error: Angle must be between 0 and 180!");
        return;
      }

      Serial.print("Moving servo ");
      Serial.print(servos[channel].name);
      Serial.print(" (channel ");
      Serial.print(channel);
      Serial.print(") to ");
      Serial.print(targetAngle);
      Serial.println("°");

      moveServo(channel, targetAngle, 25);
    }
  }
}
