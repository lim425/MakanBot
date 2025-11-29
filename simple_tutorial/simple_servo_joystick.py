import pygame
import serial
import time

# --- Arduino Serial Setup ---
use_arduino = True
if use_arduino:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2)

# --- Initialize pygame and joystick ---
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick detected.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

# --- Servo ---
servo_buttons = {
    4: 0,  # Base
    1: 1,  # Shoulder
    0: 2,  # Elbow
    3: 3,  # Wrist
    7: 4   # Gripper
}

# --- Home position waypoints ---
home_waypoints = [
    [90, 130, 90, 90, 0],
    [90, 180, 5, 90, 0]
]

# --- Initialize servo angles ---
servo_angles = [90, 180, 5, 90, 0]
current_servo = None

print("Use buttons to select servo, D-Pad (hat) up/down to move servo.")
print("Press Button 6 to move arm to home position.")

try:
    while True:
        pygame.event.pump()

        # --- Go Home Position ---
        if joystick.get_button(6):
            print("Moving to home position...")
            for waypoint in home_waypoints:
                for servo_id, angle in enumerate(waypoint):
                    servo_angles[servo_id] = angle
                    cmd = f"{servo_id} {angle}\n"
                    if use_arduino:
                        ser.write(cmd.encode())
                    print(f"Sent: {cmd.strip()}")
                    time.sleep(0.1)
                time.sleep(0.5)
            print("Reached home position.")
            time.sleep(0.5)

        # --- Joystick servo control ---
        for button, servo_id in servo_buttons.items():
            if joystick.get_button(button):
                current_servo = servo_id
                time.sleep(0.2)  # debounce

                # --- Read D-Pad (Hat) ---
                hat_x, hat_y = joystick.get_hat(0)

                if hat_y == 1:  # D-pad up → increase angle
                    servo_angles[current_servo] = min(180, servo_angles[current_servo] + 5)
                elif hat_y == -1:  # D-pad down → decrease angle
                    servo_angles[current_servo] = max(0, servo_angles[current_servo] - 5)

                # Only send if D-pad is pressed
                if hat_y != 0:
                    cmd = f"{current_servo} {servo_angles[current_servo]}\n"
                    if use_arduino:
                        ser.write(cmd.encode())
                    print(f"{cmd.strip()}")

                time.sleep(0.05)

        if current_servo is None:
            continue


except KeyboardInterrupt:
    print("Exiting...")
finally:
    pygame.quit()
    if use_arduino:
        ser.close()
