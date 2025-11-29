import pygame
import time
from PySide6.QtCore import QThread, Signal

class JoystickThread(QThread):
    # Signal: (Servo Index, Step Amount)
    # Example: (0, 5) means "Increase Base by 5 degrees"
    move_signal = Signal(int, int)
    
    # Signal: Trigger Home function
    home_signal = Signal()
    
    # Signal: Log status to GUI
    joystick_status_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self._is_running = True
        self.current_servo_index = None # Track which motor is selected

        # --- MAPPING: Joystick Buttons -> Servo Index ---
        # Based on your provided code:
        self.servo_buttons = {
            4: 0,  # Base
            1: 1,  # Shoulder
            0: 2,  # Elbow
            3: 3,  # Wrist
            7: 4   # Gripper
        }

    def run(self):
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            self.joystick_status_signal.emit("Error: No Joystick Detected")
            return

        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        self.joystick_status_signal.emit(f"Joystick: Activate")

        while self._is_running:
            pygame.event.pump()

            # Check Idle button
            if joystick.get_button(9):
                self.current_servo_index = None
                self.joystick_status_signal.emit("Joystick: Idle")
                time.sleep(0.5)

            # CHECK HOME BUTTON
            if joystick.get_button(6):
                self.home_signal.emit()
                self.joystick_status_signal.emit("Joystick: Home")
                time.sleep(0.5)

            # CHECK SERVO SELECTION BUTTONS
            for btn_id, servo_idx in self.servo_buttons.items():
                if joystick.get_button(btn_id):
                    self.current_servo_index = servo_idx
                    # Map index to name for display
                    names = ["Base", "Shoulder", "Elbow", "Wrist", "Gripper"]
                    self.joystick_status_signal.emit(f"Joystick: {names[servo_idx]}")
                    time.sleep(0.2)

            # CHECK D-PAD (HAT)
            if self.current_servo_index is not None:
                hat_x, hat_y = joystick.get_hat(0)
                
                if hat_y == 1:   # UP on D-Pad
                    self.move_signal.emit(self.current_servo_index, 5)
                    time.sleep(0.1) # Speed limit
                elif hat_y == -1: # DOWN on D-Pad
                    self.move_signal.emit(self.current_servo_index, -5)
                    time.sleep(0.1)

            time.sleep(0.05)

        # Cleanup
        pygame.quit()

    def stop(self):
        self._is_running = False
        self.wait()