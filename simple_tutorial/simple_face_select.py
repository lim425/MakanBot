import cv2
import time
from facemeshModule import FaceMeshDetector

cap = cv2.VideoCapture(0)
frame_width  = 1280
frame_height = 720

prev_fps_time = 0
new_fps_time = 0

detector = FaceMeshDetector()

# Selection variables
hover_start_time = None
hover_duration = 2  # seconds needed to select
selected_box = None

while True:
    success, img = cap.read()
    if not success:
        print("End of video or failed read")               
        break
    img = cv2.flip(img, 1)
    img = cv2.resize(img, (frame_width, frame_height))
    img, faces = detector.findFaceMesh(img, draw=False)

    # Define box positions
    left_box = (100, 200, 400, 500)   # (x1, y1, x2, y2)
    right_box = (880, 200, 1180, 500)

    # Draw boxes
    cv2.rectangle(img, (left_box[0], left_box[1]), (left_box[2], left_box[3]), (255, 0, 0), 3)
    cv2.rectangle(img, (right_box[0], right_box[1]), (right_box[2], right_box[3]), (0, 255, 0), 3)
    cv2.putText(img, "LEFT", (left_box[0]+80, left_box[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
    cv2.putText(img, "RIGHT", (right_box[0]+70, right_box[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    # Application
    if faces:
        x4, y4 = faces[0][4]
        cv2.circle(img, (x4, y4), 8, (0, 255, 0), cv2.FILLED)
        # print("Landmark 4:", x4, y4)

        current_time = time.time()

        in_left = left_box[0] < x4 < left_box[2] and left_box[1] < y4 < left_box[3]
        in_right = right_box[0] < x4 < right_box[2] and right_box[1] < y4 < right_box[3]

        if in_left or in_right:
            if hover_start_time is None:
                hover_start_time = current_time  # Start timing
            elapsed = current_time - hover_start_time

            # Draw a progress bar
            cv2.rectangle(img, (550, 650), (750, 670), (255, 0, 0), 5)
            cv2.rectangle(img, (550, 650), (550 + int((elapsed/hover_duration)*200), 670), (0,255,0), cv2.FILLED)

            if elapsed >= hover_duration:
                selected_box = "LEFT" if in_left else "RIGHT"
                print(f"✅ Selected: {selected_box}")
                hover_start_time = None
        else:
            hover_start_time = None  # reset if nose moves out

    
     # Highlight selected box
    if selected_box == "LEFT":
        cv2.rectangle(img, (left_box[0], left_box[1]), (left_box[2], left_box[3]), (0,255,255), -1)
        cv2.putText(img, "LEFT SELECTED!", (450, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,255), 3)
    elif selected_box == "RIGHT":
        cv2.rectangle(img, (right_box[0], right_box[1]), (right_box[2], right_box[3]), (0,255,255), -1)
        cv2.putText(img, "RIGHT SELECTED!", (450, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,255), 3)

    # FPS
    new_fps_time = time.time()
    fps = 1 / (new_fps_time - prev_fps_time)
    prev_fps_time = new_fps_time

    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)
    
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cv2.destroyAllWindows()
