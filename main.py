import cv2
import time
import serial
from Facemesh_module import FaceMeshDetector
from GUI_module import GUI

# ----------------------- Arduino Serial ----------------------------
use_arduino = False # Set True if connect to arduino
if use_arduino == True:
    arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2)

# ----------------------- Camera setup ----------------------------
cap = cv2.VideoCapture(0)
frame_width  = 1280
frame_height = 720
prev_fps_time = 0
new_fps_time = 0

# ----------------------- Initialize Module----------------------------
detector = FaceMeshDetector()
gui = GUI(frame_width, frame_height)

# ----------------------- Selection variables ----------------------------
hover_start_time = None
hover_duration = 2 
selected_box = None
last_sent = None 

# ----------------------- Main Code ----------------------------
while True:
    success, img = cap.read()
    if not success:
        print("End of video or failed read")               
        break
    img = cv2.flip(img, 1)
    img = cv2.resize(img, (frame_width, frame_height))
    img, faces = detector.findFaceMesh(img, draw=False)

    # ----------------------- GUI display ----------------------------
    gui_button_boundaries = gui.guiPosition()
    gui.guiDisplay(img)

    # ----------------------- Start Application ----------------------------
    if faces:
        cursor_x, cursor_y = faces[0][4] # nose
        cv2.circle(img, (cursor_x, cursor_y), 8, (0, 0, 255), cv2.FILLED)

        current_time = time.time()

        # Check hover position
        in_next_selection = gui_button_boundaries[2][0] < cursor_x < gui_button_boundaries[2][2] and gui_button_boundaries[2][1] < cursor_y < gui_button_boundaries[2][3]
        in_end_button = gui_button_boundaries[3][0] < cursor_x < gui_button_boundaries[3][2] and gui_button_boundaries[3][1] < cursor_y < gui_button_boundaries[3][3]
        in_A = gui_button_boundaries[4][0] < cursor_x < gui_button_boundaries[4][2] and gui_button_boundaries[4][1] < cursor_y < gui_button_boundaries[4][3]
        in_B = gui_button_boundaries[5][0] < cursor_x < gui_button_boundaries[5][2] and gui_button_boundaries[5][1] < cursor_y < gui_button_boundaries[5][3]
        in_C = gui_button_boundaries[6][0] < cursor_x < gui_button_boundaries[6][2] and gui_button_boundaries[6][1] < cursor_y < gui_button_boundaries[6][3]
        in_D = gui_button_boundaries[7][0] < cursor_x < gui_button_boundaries[7][2] and gui_button_boundaries[7][1] < cursor_y < gui_button_boundaries[7][3]
        in_E = gui_button_boundaries[8][0] < cursor_x < gui_button_boundaries[8][2] and gui_button_boundaries[8][1] < cursor_y < gui_button_boundaries[8][3]
        in_F = gui_button_boundaries[9][0] < cursor_x < gui_button_boundaries[9][2] and gui_button_boundaries[9][1] < cursor_y < gui_button_boundaries[9][3]
        in_G = gui_button_boundaries[10][0] < cursor_x < gui_button_boundaries[10][2] and gui_button_boundaries[10][1] < cursor_y < gui_button_boundaries[10][3]
        in_H = gui_button_boundaries[11][0] < cursor_x < gui_button_boundaries[11][2] and gui_button_boundaries[11][1] < cursor_y < gui_button_boundaries[11][3]
        in_I = gui_button_boundaries[12][0] < cursor_x < gui_button_boundaries[12][2] and gui_button_boundaries[12][1] < cursor_y < gui_button_boundaries[12][3]
   

        if in_A or in_B or in_C or in_D or in_E or in_F or in_G or in_H or in_I or in_next_selection or in_end_button:
            if hover_start_time is None:
                hover_start_time = current_time  # Start timing
            elapsed = current_time - hover_start_time

            # update progress bar
            progress = min(elapsed / hover_duration, 1.0)
            cv2.rectangle(img, (int(gui_button_boundaries[13][0]), int(gui_button_boundaries[13][1])), (int(gui_button_boundaries[13][0]) + int(progress * (int(gui_button_boundaries[13][2]) - int(gui_button_boundaries[13][0]))), int(gui_button_boundaries[13][3])), (71,230,121), cv2.FILLED)

            if elapsed >= hover_duration:
                if in_A:
                    selected_box = "A"
                elif in_B:
                    selected_box = "B"
                elif in_C:
                    selected_box = "C"
                elif in_D:
                    selected_box = "D"
                elif in_E:
                    selected_box = "E"
                elif in_F:
                    selected_box = "F"
                elif in_G:
                    selected_box = "G"
                elif in_H:
                    selected_box = "H"
                elif in_I:
                    selected_box = "I"
                elif in_next_selection:
                    selected_box = "X"
                elif in_end_button:
                    selected_box = "Z"
                
                if (use_arduino == True) and (selected_box != last_sent):
                    arduino.write(selected_box.encode())
                    print(f"Sent to Arduino: {selected_box}")
                    last_sent = selected_box
                
        else:
            hover_start_time = None  # reset if nose moves out

    if selected_box == "A":
        gui.drawTextCenter(img, "Select: A", gui_button_boundaries[1], font_scale=2)
    elif selected_box == "B":
        gui.drawTextCenter(img, "Select: B", gui_button_boundaries[1], font_scale=2)
    elif selected_box == "C":
        gui.drawTextCenter(img, "Select: C", gui_button_boundaries[1], font_scale=2)
    elif selected_box == "D":
        gui.drawTextCenter(img, "Select: D", gui_button_boundaries[1], font_scale=2)
    elif selected_box == "E":
        gui.drawTextCenter(img, "Select: E", gui_button_boundaries[1], font_scale=2)
    elif selected_box == "F":
        gui.drawTextCenter(img, "Select: F", gui_button_boundaries[1], font_scale=2)
    elif selected_box == "G":
        gui.drawTextCenter(img, "Select: G", gui_button_boundaries[1], font_scale=2)
    elif selected_box == "H":
        gui.drawTextCenter(img, "Select: H", gui_button_boundaries[1], font_scale=2)
    elif selected_box == "I":
        gui.drawTextCenter(img, "Select: I", gui_button_boundaries[1], font_scale=2)
    elif selected_box == "X":
        gui.drawTextCenter(img, "Next", gui_button_boundaries[1], font_scale=2)
    elif selected_box == "Z":
        gui.drawTextCenter(img, "END", gui_button_boundaries[1], font_scale=2)

    # FPS
    new_fps_time = time.time()
    fps = 1 / (new_fps_time - prev_fps_time)
    prev_fps_time = new_fps_time
    gui.fpsDisplay(img, fps)
    
    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
    
cv2.destroyAllWindows()
