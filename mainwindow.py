import sys
import cv2
import numpy as np
import serial
import time
from PySide6.QtCore import Qt, Slot, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QSizePolicy
from ui_mainwindow import Ui_MainWindow
from video_thread import VideoThread
from voice_thread import VoiceThread
from joystick_thread import JoystickThread

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        
        # Variable to track the camera thread
        self.camera_thread = None
        self.voice_thread = None
        self.joystick_thread = None
        
        # Arduino Initialization
        self.use_arduino = True
        self.manual_last_sent_time = 0
        if self.use_arduino:
            try:
                self.arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
                time.sleep(2)
            except Exception as e:
                print(f"Error connecting to Arduino: {e}")
                self.use_arduino = False

        # Waypoint
        self.sequence_timer = QTimer()
        self.sequence_timer.setInterval(2000)
        self.sequence_timer.timeout.connect(self.execute_next_step)
        self.current_waypoints = []
        self.step_index = 0
        self.waypoints = {
            "PICK": [
                [90, 180, 50, 90, 0],
                [90, 110, 65, 50, 0], 
                [90, 75, 60, 5, 0],
                [90, 50, 45, 5, 0],
            ],
            "FEED": [
                [90, 50, 45, 5, 0],
                [90, 100, 55, 35, 0],
                [90, 120, 50, 35, 0],
                [120, 120, 50, 55, 0]  
            ],
            "HOME": [
                [90, 130, 90, 90, 0],
                [90, 180, 0, 90, 0] 
            ]
        }


        # TAB WIDGET
        self.tabWidget.currentChanged.connect(self.on_tab_changed)
        # Check if we started on the Head Gesture tab (Index 1)
        if self.tabWidget.currentIndex() == 1:
            self.start_camera()
        if self.tabWidget.currentIndex() == 2:
            self.start_voice()

        # Spin Box Buttons
        step = 5
        self.button_base_minus.clicked.connect(lambda: self.step_servo(self.spinBox_base, -step))
        self.button_base_plus.clicked.connect(lambda: self.step_servo(self.spinBox_base, step))
        self.button_shoulder_minus.clicked.connect(lambda: self.step_servo(self.spinBox_shoulder, -step))
        self.button_shoulder_plus.clicked.connect(lambda: self.step_servo(self.spinBox_shoulder, step))
        self.button_elbow_minus.clicked.connect(lambda: self.step_servo(self.spinBox_elbow, -step))
        self.button_elbow_plus.clicked.connect(lambda: self.step_servo(self.spinBox_elbow, step))
        self.button_wrist_minus.clicked.connect(lambda: self.step_servo(self.spinBox_wrist, -step))
        self.button_wrist_plus.clicked.connect(lambda: self.step_servo(self.spinBox_wrist, step))
        self.button_gripper_minus.clicked.connect(lambda: self.step_servo(self.spinBox_gripper, -step))
        self.button_gripper_plus.clicked.connect(lambda: self.step_servo(self.spinBox_gripper, step))
        # Spin Boxes
        self.spinBox_base.valueChanged.connect(lambda val: self.manual_control(val, 0))
        self.spinBox_shoulder.valueChanged.connect(lambda val: self.manual_control(val, 1))
        self.spinBox_elbow.valueChanged.connect(lambda val: self.manual_control(val, 2))
        self.spinBox_wrist.valueChanged.connect(lambda val: self.manual_control(val, 3))
        self.spinBox_gripper.valueChanged.connect(lambda val: self.manual_control(val, 4))
        # Function Buttons
        self.checkbox_joystick.toggled.connect(self.checkbox_joystick_pressed)
        self.button_home.clicked.connect(self.home_button_pressed)
        self.checkbox_gripper.toggled.connect(self.checkbox_gripper_pressed)
        
    
    # ========================== General Function ==========================
    
    # Tab Switching Logic
    def on_tab_changed(self, index):
        # index 0: manual control, 1: head control, 2: voice control
        if index == 1:
            self.start_camera()
        else:
            self.stop_camera()

        if index == 2:
            self.start_voice()
        else:
            self.stop_voice()

    # Update System Status
    @Slot(str)
    def update_system_status(self, text):
        self.statusBar().showMessage(text, 3000)

    @Slot(str)
    def handle_command(self, command):
        print(f"Receive command: {command}")
        # Safety: Stop any running sequence if a new command comes
        self.sequence_timer.stop()

        if command in self.waypoints:
            # Load the data
            self.current_waypoints = self.waypoints[command]
            self.step_index = 0
            # Do the first move immediately
            self.execute_next_step()
            # Start the timer for the remaining steps
            self.sequence_timer.start()
        elif command == "HEAD":
            self.tabWidget.setCurrentIndex(1)
            self.on_tab_changed(1)
        elif command == "VOICE":
            self.tabWidget.setCurrentIndex(2)
            self.on_tab_changed(2)
        elif command == "FINISH":
            self.sequence_timer.stop()
            self.stop_camera()
            self.stop_voice()

    def execute_next_step(self):
        # Check if timer are finish or not
        if self.step_index >= len(self.current_waypoints):
            self.sequence_timer.stop() # Stop the alarm
            print("Sequence Complete")
            self.update_system_status("Sequence Complete")
            return
        # Get angles for the current step
        angles = self.current_waypoints[self.step_index]
        print(f"Executing Step {self.step_index + 1}: {angles}")
        self.update_system_status(f"Executing Step {self.step_index + 1}: {angles}")
        self.spinBox_base.setValue(angles[0])
        self.spinBox_shoulder.setValue(angles[1])
        self.spinBox_elbow.setValue(angles[2])
        self.spinBox_wrist.setValue(angles[3])
        self.spinBox_gripper.setValue(angles[4])
        # Prepare for next step
        self.step_index += 1

    # ========================== Munual FUNCTIONS ==========================

    def step_servo(self, spinbox, step):
        new_value = spinbox.value() + step
        spinbox.setValue(new_value)
        self.update_system_status("Moving Robotic Arm...")

    def manual_control(self, value, servo_idx):
        command = f"{servo_idx} {value}\n"  
        print(f"Command send: {command.strip()}")
        
        # Send to Arduino
        if self.use_arduino:
            try:
                self.arduino.write(command.encode())
                # time.sleep(0.1)
            except Exception as e:
                print(f"Serial Error: {e}")
                self.update_system_status(f"Serial Error: {e}")
        
    def home_button_pressed(self):
        print("Return to home position")
        self.update_system_status("Return to home position")
        self.handle_command("HOME")


    def checkbox_gripper_pressed(self, checked):
        if checked:
            self.spinBox_gripper.setValue(0)
            self.update_system_status("Close gripper")
        else:
            self.spinBox_gripper.setValue(70)
            self.update_system_status("Open gripper")


    # ========================== JOYSTICK FUNCTIONS ==========================

    def checkbox_joystick_pressed(self, checked):
        if checked:
            self.start_joystick()
        else:
            self.stop_joystick()

    def start_joystick(self):
        if self.joystick_thread is None:
            print("Starting Joystick Thread...")
            self.update_system_status("Starting Joystick Control...")
            self.joystick_thread = JoystickThread()
            self.joystick_thread.move_signal.connect(self.handle_joystick_move)
            self.joystick_thread.home_signal.connect(self.home_button_pressed)
            self.joystick_thread.joystick_status_signal.connect(self.log_status_joystick)
            self.joystick_thread.start()

    def stop_joystick(self):
        if self.joystick_thread is not None:
            print("Stopping Joystick...")
            self.update_system_status("Stopping Joystick Control...")
            self.label_joystick_status.setText("Joystick: Not Activate")
            self.joystick_thread.stop()
            self.joystick_thread = None

    @Slot(int, int)
    def handle_joystick_move(self, servo_idx, step):
        spinbox_map = {
            0: self.spinBox_base,
            1: self.spinBox_shoulder,
            2: self.spinBox_elbow,
            3: self.spinBox_wrist,
            4: self.spinBox_gripper
        }

        if servo_idx in spinbox_map:
            self.step_servo(spinbox_map[servo_idx], step)

    @Slot(str)
    def log_status_joystick(self, text):
        print(text)
        self.label_joystick_status.setText(text)


    # ========================== CAMERA FUNCTIONS ==========================

    def start_camera(self):
        if self.camera_thread is None:
            print("Starting Head Control...")
            self.update_system_status("Starting Head Control...")
            self.camera_thread = VideoThread()
            self.camera_thread.change_pixmap_signal.connect(self.update_image)
            self.camera_thread.head_gesture_signal.connect(self.handle_head_command)
            self.camera_thread.start()

    def stop_camera(self):
        if self.camera_thread is not None:
            print("Stopping Head Control...")
            self.update_system_status("Stopping Head Control...")
            self.camera_thread.stop()
            self.camera_thread = None 
            self.label_camera.clear()
            self.label_camera.setText("Camera Off")
            
    @Slot(np.ndarray)
    def update_image(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image).scaled(
            self.label_camera.width(), 
            self.label_camera.height(), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        self.label_camera.setPixmap(pixmap)

    @Slot(str)
    def handle_head_command(self, command):
        self.handle_command(command)


    # ========================== VOICE FUNCTIONS ==========================

    def start_voice(self):
        if self.voice_thread is None:
            print("Starting Voice Control...")
            self.update_system_status("Starting Voice Control...")
            self.voice_thread = VoiceThread()
            self.voice_thread.log_signal.connect(self.update_voice_log)
            self.voice_thread.user_text_signal.connect(self.update_voice_input)
            self.voice_thread.status_signal.connect(self.update_voice_status)
            self.voice_thread.command_signal.connect(self.handle_voice_command)
            self.voice_thread.start()

    def stop_voice(self):
        if self.voice_thread is not None:
            print("Stopping Voice Control...")
            self.update_system_status("Stopping Voice Control...")
            self.voice_thread.stop()
            self.voice_thread = None
            self.update_voice_status("Status: Voice Control OFF")

    @Slot(str)
    def update_voice_log(self, text):
        self.text_voice_log.appendPlainText(text)

    @Slot(str)
    def update_voice_input(self, text):
        self.text_voice_input.setPlainText(text)

    @Slot(str)
    def update_voice_status(self, text):
        self.label_voice_status.setText(text)

    @Slot(str)
    def handle_voice_command(self, command):
        self.handle_command(command)

    def closeEvent(self, event):
        self.stop_camera()
        self.stop_voice()
        self.stop_joystick()
        if self.use_arduino:
            self.arduino.close()
        event.accept()