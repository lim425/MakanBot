import serial
import time

# --- Configure serial port ---
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # wait for Arduino to reset

# --- Send command ---
while True:
    cmd = input("Enter command (A, B, or number): ")
    arduino.write(cmd.encode())  # send to Arduino
    print(f"Sent: {cmd}")

