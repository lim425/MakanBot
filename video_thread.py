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
                    in_home = gui_button_boundaries[2][0] < cursor_x < gui_button_boundaries[2][2] and gui_button_boundaries[2][1] < cursor_y < gui_button_boundaries[2][3]
                    in_finish = gui_button_boundaries[3][0] < cursor_x < gui_button_boundaries[3][2] and gui_button_boundaries[3][1] < cursor_y < gui_button_boundaries[3][3]
                    in_voice = gui_button_boundaries[4][0] < cursor_x < gui_button_boundaries[4][2] and gui_button_boundaries[4][1] < cursor_y < gui_button_boundaries[4][3]
                    in_pick = gui_button_boundaries[5][0] < cursor_x < gui_button_boundaries[5][2] and gui_button_boundaries[5][1] < cursor_y < gui_button_boundaries[5][3]
                    in_feed = gui_button_boundaries[6][0] < cursor_x < gui_button_boundaries[6][2] and gui_button_boundaries[6][1] < cursor_y < gui_button_boundaries[6][3]

                    if in_home or in_finish or in_voice or in_pick or in_feed :
                        if self.hover_start_time is None:
                            self.hover_start_time = current_time
                        elapsed = current_time - self.hover_start_time

                        # update progress bar
                        progress = min(elapsed / self.hover_duration, 1.0)
                        cv2.rectangle(img, (int(gui_button_boundaries[7][0]), int(gui_button_boundaries[7][1])), (int(gui_button_boundaries[7][0]) + int(progress * (int(gui_button_boundaries[7][2]) - int(gui_button_boundaries[7][0]))), int(gui_button_boundaries[7][3])), (71,230,121), cv2.FILLED)

                        if elapsed >= self.hover_duration:
                            if in_pick:
                                self.selected_box = "PICK"
                            elif in_feed:
                                self.selected_box = "FEED"
                            elif in_home:
                                self.selected_box = "HOME"
                            elif in_finish:
                                self.selected_box = "FINISH"
                            elif in_voice:
                                self.selected_box = "VOICE"

                            if self.selected_box != self.last_sent:
                                command = f'{self.selected_box}'
                                self.head_gesture_signal.emit(command)
                                self.last_sent = self.selected_box
                    
                    else:
                        self.hover_start_time = None
                
                if self.selected_box == "PICK":
                    self.gui.drawTextCenter(img, "Picking Food", gui_button_boundaries[1], font_scale=2)
                elif self.selected_box == "FEED":
                    self.gui.drawTextCenter(img, "Feeding Food", gui_button_boundaries[1], font_scale=2)
                elif self.selected_box == "HOME":
                    self.gui.drawTextCenter(img, "Return Home", gui_button_boundaries[1], font_scale=2)
                elif self.selected_box == "FINISH":
                    self.gui.drawTextCenter(img, "Finish Eat", gui_button_boundaries[1], font_scale=2)
                elif self.selected_box == "VOICE":
                    self.gui.drawTextCenter(img, "Voice Control", gui_button_boundaries[1], font_scale=2)
   
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
