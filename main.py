import cv2
import time
import serial
from facemeshModule import FaceMeshDetector

# ----------------------- Arduino Serial ----------------------------
use_arduino = False
if use_arduino == True:
    arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2)

# ----------------------- Camera setup ----------------------------
cap = cv2.VideoCapture(0)
frame_width  = 1280
frame_height = 720
scale_x = frame_width / 1280
scale_y = frame_height / 720
scale = (scale_x + scale_y) / 2
prev_fps_time = 0
new_fps_time = 0

# ----------------------- Facemesh detector ----------------------------
detector = FaceMeshDetector()

# ----------------------- Selection variables ----------------------------
hover_start_time = None
hover_duration = 2 
selected_box = None
last_sent = None 

# ----------------------- Text & Label ----------------------------
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = max(1, int(1 * scale))
thickness = max(3, int(3 * scale))
text_color = (72, 52, 33)
def draw_text_center(img, text, box, font=font, font_scale=font_scale, color=text_color, thickness=thickness):
    (x1, y1, x2, y2) = box
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = x1 + (x2 - x1 - text_size[0]) / 2
    text_y = y1 + (y2 - y1 + text_size[1]) / 2
    cv2.putText(img, text, (int(text_x), int(text_y)), font, font_scale, color, thickness)

# ----------------------- GUI offset & position ----------------------------
offset = 30 * scale_x     # offset (horizontal) between each button
offset1 = 20 * scale_y    # offset between gui box and the promt display
offset2 = 50 * scale_y    # offset between promt display and finish button
offset3 = 120 * scale_y   # height of the next_selection_button end_button
offset4 = 40 * scale_y    # offset between finsih_eat_button and buttonA,B,C
offset5 = 80 * scale_y    # height of the button A-I
offset6 = 20 * scale_y    # offset between buttonG,H,I and progress bar
offset7 = 40 * scale_y    # height of the progress bar
offset8 = 30 * scale_x    # width of the button
# Position
gui_box = (frame_width//2, 0, frame_width, frame_height)
prompt_display = (gui_box[0]+offset1, offset1, gui_box[2]-offset1, gui_box[3]//4)
next_selection_button = (prompt_display[0], (prompt_display[3])+offset2, (((prompt_display[2]-prompt_display[0])//4)+offset8)+prompt_display[0], (prompt_display[3])+offset3)
end_button = (next_selection_button[2]+offset, (prompt_display[3])+offset2, (((prompt_display[2]-prompt_display[0])//4)+offset8)+next_selection_button[2]+offset, (prompt_display[3])+offset3)
buttonA = (next_selection_button[0], next_selection_button[3]+offset4, next_selection_button[2], next_selection_button[3]+offset4+offset5)
buttonB = (buttonA[2]+offset, buttonA[1], (((prompt_display[2]-prompt_display[0])//4)+offset8)+buttonA[2]+offset, buttonA[3])
buttonC = (buttonB[2]+offset, buttonB[1], (((prompt_display[2]-prompt_display[0])//4)+offset8)+buttonB[2]+offset, buttonB[3])
buttonD=(buttonA[0], buttonA[3]+offset, buttonA[2], buttonA[3]+offset+offset5)
buttonE=(buttonB[0], buttonB[3]+offset, buttonB[2], buttonB[3]+offset+offset5)
buttonF=(buttonC[0], buttonC[3]+offset, buttonC[2], buttonC[3]+offset+offset5)
buttonG=(buttonD[0], buttonD[3]+offset, buttonD[2], buttonD[3]+offset+offset5)
buttonH=(buttonE[0], buttonE[3]+offset, buttonE[2], buttonE[3]+offset+offset5)
buttonI=(buttonF[0], buttonF[3]+offset, buttonF[2], buttonF[3]+offset+offset5)
progress_bar = (prompt_display[0], buttonG[3]+offset6, prompt_display[2], buttonG[3]+offset6+offset7)

while True:
    success, img = cap.read()
    if not success:
        print("End of video or failed read")               
        break
    img = cv2.flip(img, 1)
    img = cv2.resize(img, (frame_width, frame_height))
    img, faces = detector.findFaceMesh(img, draw=False)

    # ----------------------- GUI display ----------------------------
    # GUI
    cv2.rectangle(img, (gui_box[0], gui_box[1]), (gui_box[2], gui_box[3]), (212, 61, 104), -1)
    # Prompt Display
    cv2.rectangle(img, (int(prompt_display[0]), int(prompt_display[1])), (int(prompt_display[2]), int(prompt_display[3])), (61, 212, 207), -1)
    # Function button
    cv2.rectangle(img, (int(next_selection_button[0]), int(next_selection_button[1])), (int(next_selection_button[2]), int(next_selection_button[3])), (104, 212, 61), -1)
    cv2.rectangle(img, (int(end_button[0]), int(end_button[1])), (int(end_button[2]), int(end_button[3])), (61, 61, 212), -1)
    # Progress Bar
    cv2.rectangle(img, (int(progress_bar[0]), int(progress_bar[1])), (int(progress_bar[2]), int(progress_bar[3])), (70, 62, 57), -1)
    # Buttons
    cv2.rectangle(img, (int(buttonA[0]), int(buttonA[1])), (int(buttonA[2]), int(buttonA[3])), (196, 186, 173), -1)
    cv2.rectangle(img, (int(buttonB[0]), int(buttonB[1])), (int(buttonB[2]), int(buttonB[3])), (196, 186, 173), -1)
    cv2.rectangle(img, (int(buttonC[0]), int(buttonC[1])), (int(buttonC[2]), int(buttonC[3])), (196, 186, 173), -1)
    cv2.rectangle(img, (int(buttonD[0]), int(buttonD[1])), (int(buttonD[2]), int(buttonD[3])), (196, 186, 173), -1)
    cv2.rectangle(img, (int(buttonE[0]), int(buttonE[1])), (int(buttonE[2]), int(buttonE[3])), (196, 186, 173), -1)
    cv2.rectangle(img, (int(buttonF[0]), int(buttonF[1])), (int(buttonF[2]), int(buttonF[3])), (196, 186, 173), -1)
    cv2.rectangle(img, (int(buttonG[0]), int(buttonG[1])), (int(buttonG[2]), int(buttonG[3])), (196, 186, 173), -1)
    cv2.rectangle(img, (int(buttonH[0]), int(buttonH[1])), (int(buttonH[2]), int(buttonH[3])), (196, 186, 173), -1)
    cv2.rectangle(img, (int(buttonI[0]), int(buttonI[1])), (int(buttonI[2]), int(buttonI[3])), (196, 186, 173), -1)
    # Button Info
    draw_text_center(img, "NEXT", next_selection_button)
    draw_text_center(img, "END", end_button)
    draw_text_center(img, "A", buttonA)
    draw_text_center(img, "B", buttonB)
    draw_text_center(img, "C", buttonC)
    draw_text_center(img, "D", buttonD)
    draw_text_center(img, "E", buttonE)
    draw_text_center(img, "F", buttonF)
    draw_text_center(img, "G", buttonG)
    draw_text_center(img, "H", buttonH)
    draw_text_center(img, "I", buttonI)

    # Application
    if faces:
        cursor_x, cursor_y = faces[0][4] # nose
        cv2.circle(img, (cursor_x, cursor_y), 8, (0, 0, 255), cv2.FILLED)

        current_time = time.time()

        # Check hover position
        in_next_selection = next_selection_button[0] < cursor_x < next_selection_button[2] and next_selection_button[1] < cursor_y < next_selection_button[3]
        in_end_button = end_button[0] < cursor_x < end_button[2] and end_button[1] < cursor_y < end_button[3]
        in_A = buttonA[0] < cursor_x < buttonA[2] and buttonA[1] < cursor_y < buttonA[3]
        in_B = buttonB[0] < cursor_x < buttonB[2] and buttonB[1] < cursor_y < buttonB[3]
        in_C = buttonC[0] < cursor_x < buttonC[2] and buttonC[1] < cursor_y < buttonC[3]
        in_D = buttonD[0] < cursor_x < buttonD[2] and buttonD[1] < cursor_y < buttonD[3]
        in_E = buttonE[0] < cursor_x < buttonE[2] and buttonE[1] < cursor_y < buttonE[3]
        in_F = buttonF[0] < cursor_x < buttonF[2] and buttonF[1] < cursor_y < buttonF[3]
        in_G = buttonG[0] < cursor_x < buttonG[2] and buttonG[1] < cursor_y < buttonG[3]
        in_H = buttonH[0] < cursor_x < buttonH[2] and buttonH[1] < cursor_y < buttonH[3]
        in_I = buttonI[0] < cursor_x < buttonI[2] and buttonI[1] < cursor_y < buttonI[3]
   

        if in_A or in_B or in_C or in_D or in_E or in_F or in_G or in_H or in_I or in_next_selection or in_end_button:
            if hover_start_time is None:
                hover_start_time = current_time  # Start timing
            elapsed = current_time - hover_start_time

            # update progress bar
            progress = min(elapsed / hover_duration, 1.0)
            cv2.rectangle(img, (int(progress_bar[0]), int(progress_bar[1])), (int(progress_bar[0]) + int(progress * (int(progress_bar[2]) - int(progress_bar[0]))), int(progress_bar[3])), (71,230,121), cv2.FILLED)

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
        draw_text_center(img, "Select: A", prompt_display, font_scale=2)
    elif selected_box == "B":
        draw_text_center(img, "Select: B", prompt_display, font_scale=2)
    elif selected_box == "C":
        draw_text_center(img, "Select: C", prompt_display, font_scale=2)
    elif selected_box == "D":
        draw_text_center(img, "Select: D", prompt_display, font_scale=2)
    elif selected_box == "E":
        draw_text_center(img, "Select: E", prompt_display, font_scale=2)
    elif selected_box == "F":
        draw_text_center(img, "Select: F", prompt_display, font_scale=2)
    elif selected_box == "G":
        draw_text_center(img, "Select: G", prompt_display, font_scale=2)
    elif selected_box == "H":
        draw_text_center(img, "Select: H", prompt_display, font_scale=2)
    elif selected_box == "I":
        draw_text_center(img, "Select: I", prompt_display, font_scale=2)
    elif selected_box == "X":
        draw_text_center(img, "Next", prompt_display, font_scale=2)
    elif selected_box == "Z":
        draw_text_center(img, "END", prompt_display, font_scale=2)

    # FPS
    new_fps_time = time.time()
    fps = 1 / (new_fps_time - prev_fps_time)
    prev_fps_time = new_fps_time
    cv2.putText(img, f'FPS: {int(fps)}', (20, int(70*scale_y)), cv2.FONT_HERSHEY_PLAIN, int(3*scale), (72, 52, 33), int(3*scale))
    
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
    
cv2.destroyAllWindows()
