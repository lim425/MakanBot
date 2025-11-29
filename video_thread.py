import cv2
import numpy as np
import time
from PySide6.QtCore import QThread, Signal
from GUI_module import GUI
from Facemesh_module import FaceMeshDetector


class VideoThread(QThread):
    change_pixmap_signal = Signal(np.ndarray)
    head_gesture_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self._is_running = True
        self.hover_start_time = None
        self.hover_duration = 2 
        self.selected_box = None
        self.last_sent = None         
        self.frame_width = 1280
        self.frame_height = 720
        self.prev_fps_time = 0
        self.new_fps_time = 0
        self.detector = FaceMeshDetector()
        self.gui = GUI(self.frame_width, self.frame_height)

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, self.frame_width)
        cap.set(4, self.frame_height)
        
        gui_button_boundaries = []
        
        while self._is_running:
            ret, img = cap.read()
            if ret:
                img = cv2.flip(img, 1)
                img, faces = self.detector.findFaceMesh(img, draw=False)
                
                # GUI Overlay
                gui_button_boundaries = self.gui.guiPosition()
                self.gui.guiDisplay(img)

                if faces:
                    cursor_x, cursor_y = faces[0][4] # nose
                    cv2.circle(img, (cursor_x, cursor_y), 8, (0, 0, 255), cv2.FILLED)

                    current_time = time.time()

                    # Check hover position
                    in_next_selection = gui_button_boundaries[2][0] < cursor_x < gui_button_boundaries[2][2] and gui_button_boundaries[2][1] < cursor_y < gui_button_boundaries[2][3]
                    in_home_button = gui_button_boundaries[3][0] < cursor_x < gui_button_boundaries[3][2] and gui_button_boundaries[3][1] < cursor_y < gui_button_boundaries[3][3]
                    in_A = gui_button_boundaries[4][0] < cursor_x < gui_button_boundaries[4][2] and gui_button_boundaries[4][1] < cursor_y < gui_button_boundaries[4][3]
                    in_B = gui_button_boundaries[5][0] < cursor_x < gui_button_boundaries[5][2] and gui_button_boundaries[5][1] < cursor_y < gui_button_boundaries[5][3]
                    in_C = gui_button_boundaries[6][0] < cursor_x < gui_button_boundaries[6][2] and gui_button_boundaries[6][1] < cursor_y < gui_button_boundaries[6][3]
                    in_D = gui_button_boundaries[7][0] < cursor_x < gui_button_boundaries[7][2] and gui_button_boundaries[7][1] < cursor_y < gui_button_boundaries[7][3]
                    in_E = gui_button_boundaries[8][0] < cursor_x < gui_button_boundaries[8][2] and gui_button_boundaries[8][1] < cursor_y < gui_button_boundaries[8][3]
                    in_F = gui_button_boundaries[9][0] < cursor_x < gui_button_boundaries[9][2] and gui_button_boundaries[9][1] < cursor_y < gui_button_boundaries[9][3]
                    in_G = gui_button_boundaries[10][0] < cursor_x < gui_button_boundaries[10][2] and gui_button_boundaries[10][1] < cursor_y < gui_button_boundaries[10][3]
                    in_H = gui_button_boundaries[11][0] < cursor_x < gui_button_boundaries[11][2] and gui_button_boundaries[11][1] < cursor_y < gui_button_boundaries[11][3]
                    in_J = gui_button_boundaries[12][0] < cursor_x < gui_button_boundaries[12][2] and gui_button_boundaries[12][1] < cursor_y < gui_button_boundaries[12][3]


                    if in_A or in_B or in_C or in_D or in_E or in_F or in_G or in_H or in_J or in_next_selection or in_home_button:
                        if self.hover_start_time is None:
                            self.hover_start_time = current_time
                        elapsed = current_time - self.hover_start_time

                        # update progress bar
                        progress = min(elapsed / self.hover_duration, 1.0)
                        cv2.rectangle(img, (int(gui_button_boundaries[13][0]), int(gui_button_boundaries[13][1])), (int(gui_button_boundaries[13][0]) + int(progress * (int(gui_button_boundaries[13][2]) - int(gui_button_boundaries[13][0]))), int(gui_button_boundaries[13][3])), (71,230,121), cv2.FILLED)

                        if elapsed >= self.hover_duration:
                            if in_A:
                                self.selected_box = "A"
                            elif in_B:
                                self.selected_box = "B"
                            elif in_C:
                                self.selected_box = "C"
                            elif in_D:
                                self.selected_box = "D"
                            elif in_E:
                                self.selected_box = "E"
                            elif in_F:
                                self.selected_box = "F"
                            elif in_G:
                                self.selected_box = "G"
                            elif in_H:
                                self.selected_box = "H"
                            elif in_J:
                                self.selected_box = "J"
                            elif in_next_selection:
                                self.selected_box = "NEXT"
                            elif in_home_button:
                                self.selected_box = "HOME"

                            if self.selected_box != self.last_sent:
                                command = f'{self.selected_box}'
                                self.head_gesture_signal.emit(command)
                                self.last_sent = self.selected_box
                    
                    else:
                        self.hover_start_time = None
                
                if self.selected_box == "A":
                    self.gui.drawTextCenter(img, "Select: A", gui_button_boundaries[1], font_scale=2)
                elif self.selected_box == "B":
                    self.gui.drawTextCenter(img, "Select: B", gui_button_boundaries[1], font_scale=2)
                elif self.selected_box == "C":
                    self.gui.drawTextCenter(img, "Select: C", gui_button_boundaries[1], font_scale=2)
                elif self.selected_box == "D":
                    self.gui.drawTextCenter(img, "Select: D", gui_button_boundaries[1], font_scale=2)
                elif self.selected_box == "E":
                    self.gui.drawTextCenter(img, "Select: E", gui_button_boundaries[1], font_scale=2)
                elif self.selected_box == "F":
                    self.gui.drawTextCenter(img, "Select: F", gui_button_boundaries[1], font_scale=2)
                elif self.selected_box == "G":
                    self.gui.drawTextCenter(img, "Select: G", gui_button_boundaries[1], font_scale=2)
                elif self.selected_box == "H":
                    self.gui.drawTextCenter(img, "Select: H", gui_button_boundaries[1], font_scale=2)
                elif self.selected_box == "J":
                    self.gui.drawTextCenter(img, "Select: J", gui_button_boundaries[1], font_scale=2)
                elif self.selected_box == "NEXT":
                    self.gui.drawTextCenter(img, "Next", gui_button_boundaries[1], font_scale=2)
                elif self.selected_box == "HOME":
                    self.gui.drawTextCenter(img, "HOME", gui_button_boundaries[1], font_scale=2)
   
                # FPS
                self.new_fps_time = time.time()
                fps = 1 / (self.new_fps_time - self.prev_fps_time)
                self.prev_fps_time = self.new_fps_time
                self.gui.fpsDisplay(img, fps)

                self.change_pixmap_signal.emit(img)
            else:
                break
        
        cap.release()

    def stop(self):
        self._is_running = False
        self.wait()
