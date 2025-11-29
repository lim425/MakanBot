import cv2
import serial
import time
import numpy as np

use_arduino = True
if use_arduino:
    arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2)

# Create window
cv2.namedWindow("Robotic Arm Control")
cv2.resizeWindow("Robotic Arm Control", 1280, 720)

# Servo channels
servo_names = ["BASE", "SHOULDER", "ELBOW", "WRIST", "GRIPPER"]

cv2.createTrackbar("BASE", "Robotic Arm Control", 90, 180, lambda x: None)
cv2.createTrackbar("SHOULDER", "Robotic Arm Control", 180, 180, lambda x: None)
cv2.createTrackbar("ELBOW", "Robotic Arm Control", 5, 180, lambda x: None)
cv2.createTrackbar("WRIST", "Robotic Arm Control", 90, 180, lambda x: None)
cv2.createTrackbar("GRIPPER", "Robotic Arm Control", 0, 180, lambda x: None)

prev_values = [90] * len(servo_names)
while True:
    for i, name in enumerate(servo_names):
        val = cv2.getTrackbarPos(name, "Robotic Arm Control")
        if val != prev_values[i]:
            cmd = f"{i} {val}\n"
            if use_arduino:
                arduino.write(cmd.encode())
                time.sleep(0.1)
            print("Sent:", cmd.strip())
            prev_values[i] = val

    if cv2.waitKey(1) & 0xff == ord("q"):
        break

cv2.destroyAllWindows()
if use_arduino:
    arduino.close()
