import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # wait for Arduino reset

print("Start serial receiver")

while True:
    line = ser.readline().decode().strip()
    if line.startswith("Done"):
        print(f"Received: {line}")