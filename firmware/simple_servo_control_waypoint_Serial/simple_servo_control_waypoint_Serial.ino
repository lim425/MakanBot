#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// ---------------- Servo Configuration ----------------
struct ServoData {
  const char* name;
  int channel;
  int servoMin; // Minimum pulse width value (for 0°)
  int servoMax; // // Maximum pulse width value (for 180°)
  int currentAngle; // track current position
};

ServoData servos[] = {
  {"BASE", 0, 120, 570, 90},
  {"SHOULDER", 1, 130, 600, 180},
  {"ELBOW", 2, 280, 620, 0},
  {"WRIST", 3, 140, 600, 90}
};

const int NUM_SERVOS = sizeof(servos) / sizeof(servos[0]);

// ---------------- Waypoint Configuration ----------------
struct Waypoint {
  const char* name;
  int angles[NUM_SERVOS]; // angle for each servo
};

// Define your arm poses here:
Waypoint waypoints[] = {
  {"HOME", {90, 180, 0, 90}},
  {"PICK", {180, 65, 80, 180}},
  {"FEED", {90, 90, 130, 0}}
};

const int NUM_WAYPOINTS = sizeof(waypoints) / sizeof(waypoints[0]);

// ---------------- Helper Functions ----------------

// Convert angle (0–180°) into PCA9685 pulse width
int angleToPulse(int servoIndex, int angle) {
  return map(angle, 0, 180, servos[servoIndex].servoMin, servos[servoIndex].servoMax);
}

// Smoothly move a single servo to a target angle
void moveServo(int servoIndex, int targetAngle, int stepDelay = 10) {

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


// Find waypoint by name
int findWaypointIndex(const char* waypointName) {
  for (int i = 0; i < NUM_WAYPOINTS; i++) {
    if (strcmp(waypoints[i].name, waypointName) == 0)
      return i;
  }
  return -1;
}

// ---------------- Sequential Move to Waypoint ----------------
void moveToWaypoint(const char* waypointName, int stepDelay = 10) {
  int wpIndex = findWaypointIndex(waypointName);
  if (wpIndex == -1) {
    Serial.print("Error: Unknown waypoint ");
    Serial.println(waypointName);
    return;
  }

  Serial.print("\n➡ Moving to waypoint: ");
  Serial.println(waypointName);

  // Move servos one by one (sequential)
  for (int i = 0; i < NUM_SERVOS; i++) {
    int targetAngle = waypoints[wpIndex].angles[i];
    Serial.print("  → Moving ");
    Serial.print(servos[i].name);
    Serial.print(" to ");
    Serial.print(targetAngle);
    Serial.println("°");
    moveServo(i, targetAngle, stepDelay);
    delay(200); // small pause between each servo
  }

  Serial.print("✅ Reached waypoint: ");
  Serial.println(waypointName);
}

// ---------------- Setup ----------------
void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(50);
  delay(500);

  // Initialize the robotics arm
  for (int i = 0; i < NUM_SERVOS; i++) {
    int pulse = angleToPulse(i, servos[i].currentAngle);
    pwm.setPWM(servos[i].channel, 0, pulse);
  }
  Serial.println("Robotic Arm Initialized");
  Serial.println("\nType A for HOME, B for PICK, C for FEED");

}

// ---------------- Loop ----------------
void loop() {

  if (Serial.available()) {
    char command = Serial.read();
    command = toupper(command); // convert to uppercase
    Serial.print("Received command: ");
    Serial.println(command);

    switch (command) {
      case 'A':
        moveToWaypoint("HOME", 50);
        break;
      case 'B':
        moveToWaypoint("PICK", 50);
        break;
      case 'C':
        moveToWaypoint("FEED", 50);
        break;
      default:
        Serial.println("Type A (HOME), B (PICK), or C (FEED).");
        break;
    }
  }
}